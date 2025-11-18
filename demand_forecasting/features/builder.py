from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import json

import pandas as pd
import polars as pl

try:  # pragma: no cover - optional GPU dependency
    import cudf
    _HAS_CUDF = True
except ModuleNotFoundError:  # pragma: no cover
    cudf = None  # type: ignore
    _HAS_CUDF = False

from demand_forecasting.flows.utils import ensure_directory
from demand_forecasting.warehouse.utils import WAREHOUSE_ROOT
from demand_forecasting.validation.utils import write_validation_result

from .taxonomy import FEATURE_GROUPS


SCALER_MANIFEST_NAME = "scalers.json"


def _compute_basic_stats(df: pl.DataFrame) -> Dict[str, Dict[str, float]]:
    stats: Dict[str, Dict[str, float]] = {}
    for col, dtype in zip(df.columns, df.dtypes):
        if dtype.is_numeric():
            series = df[col].drop_nulls()
            if series.is_empty():
                continue
            stats[col] = {
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": float(series.mean()),
                "std": float(series.std()),
            }
    return stats


@dataclass
class TrainingSet:
    features: Any
    target: Any
    metadata: Dict[str, str]


class FeatureBuilder:
    def __init__(self, snapshot_path: Path | None = None) -> None:
        self.snapshot_path = snapshot_path or self._latest_snapshot()
        if self.snapshot_path is None or not self.snapshot_path.exists():
            raise FileNotFoundError(
                "Warehouse snapshot not found. Run 'scripts/build_warehouse.py' first."
            )
        self.feature_manifest_dir = ensure_directory(self.snapshot_path / "feature_manifests")
        self.scaler_manifest_path = self.feature_manifest_dir / SCALER_MANIFEST_NAME

        if not self.scaler_manifest_path.exists():
            self.scaler_manifest_path.write_text(json.dumps({}), encoding="utf-8")

    # ------------------------------------------------------------------
    def _latest_snapshot(self) -> Optional[Path]:
        gold_dir = WAREHOUSE_ROOT / "gold"
        if not gold_dir.exists():
            return None
        snapshots = sorted(gold_dir.glob("*/"))
        return snapshots[-1] if snapshots else None

    def _load(self, table: str) -> pl.DataFrame:
        path = self.snapshot_path / f"{table}.parquet"
        if not path.exists():
            raise FileNotFoundError(f"Table '{table}' not found in snapshot {self.snapshot_path}")
        return pl.read_parquet(path)

    def _log_feature_stats(self, name: str, df: pl.DataFrame) -> None:
        stats = _compute_basic_stats(df)
        payload = {"table": name, "rows": df.height, "stats": stats}
        write_validation_result(f"features-{name}", payload)

    def _update_scaler_manifest(self, stats: Dict[str, Dict[str, float]]) -> None:
        with self.scaler_manifest_path.open("r", encoding="utf-8") as fh:
            current = json.load(fh)
        current.update(stats)
        with self.scaler_manifest_path.open("w", encoding="utf-8") as fh:
            json.dump(current, fh, indent=2)

    # ------------------------------------------------------------------
    def temporal_features(self, fact: pl.DataFrame) -> pl.DataFrame:
        df = fact.sort("date")
        for lag in (1, 7, 28):
            df = df.with_columns(pl.col("qty_consumed").shift(lag).alias(f"lag_{lag}"))
        df = df.with_columns(
            pl.col("qty_consumed").rolling_mean(window_size=7).alias("rolling_mean_7"),
            pl.col("qty_consumed").rolling_std(window_size=7).alias("rolling_std_7"),
            pl.col("date").dt.weekday().alias("day_of_week"),
            pl.col("date").dt.week().alias("week_of_year"),
            pl.col("date").dt.month().alias("month"),
            pl.col("date").dt.year().alias("year"),
        )
        return df

    def climate_features(self) -> pl.DataFrame:
        df = self._load("DimWeather")
        return df.rename({
            "region": "region",
            "date": "date",
        })

    def economic_features(self) -> pl.DataFrame:
        df = self._load("DimEconomic")
        if df.is_empty():
            return df
        ptax = df.filter(pl.col("name") == "ptax").rename({"value": "ptax_value"})
        selic = df.filter(pl.col("name") == "selic").rename({"value": "selic_value"})
        return (
            ptax.join(selic, on="observed_at", how="outer")
            .rename({"observed_at": "date"})
            .select(["date", "ptax_value", "selic_value"])
        )

    def fiveg_features(self) -> pl.DataFrame:
        try:
            df = self._load("DimRegulatory")
        except FileNotFoundError:
            return pl.DataFrame()
        if df.is_empty():
            return df
        return df.select(
            pl.col("effective_date").alias("date"),
            pl.col("regulation_id").alias("deployment_phase"),
            pl.lit(None).alias("coverage_sites"),
        )

    def lead_time_features(self) -> pl.DataFrame:
        suppliers = self._load("DimSupplier")
        return suppliers.with_columns(
            pl.col("lead_time_days").rolling_std(window_size=4).over("supplier_id").alias(
                "lead_time_volatility"
            )
        )

    def sla_features(self) -> pl.DataFrame:
        operational = self._load("DimOperational")
        if "open_incidents_7d" not in operational.columns:
            operational = operational.with_columns(pl.lit(0).alias("open_incidents_7d"))
        return operational

    def hierarchical_features(self) -> pl.DataFrame:
        items = self._load("DimItem").rename({"category": "item_category"})
        sites = self._load("DimSite")
        return items.join(sites, how="left", on="site_id", suffix="_site")

    def business_features(self) -> pl.DataFrame:
        # Placeholder business context; align with docs when corporate data is available
        return pl.DataFrame(
            {
                "site_id": [],
                "item_id": [],
                "project_phase": [],
                "budget_segment": [],
            }
        )

    # ------------------------------------------------------------------
    def assemble_training_frame(self) -> pl.DataFrame:
        fact = self._load("FactDemand")
        self._log_feature_stats("fact_demand_raw", fact)
        fact_features = self.temporal_features(fact)
        self._log_feature_stats("fact_demand_temporal", fact_features)
        weather = self.climate_features()
        economic = self.economic_features()
        fiveg = self.fiveg_features()
        suppliers = self.lead_time_features()
        sla = self.sla_features()
        items = self._load("DimItem")
        sites = self._load("DimSite")

        df = fact_features.join(items, on="item_id", how="left")
        df = df.join(sites, on="site_id", how="left")
        if not weather.is_empty():
            df = df.join(weather, on=["date", "region"], how="left")
        if not economic.is_empty():
            df = df.join(economic, on="date", how="left")
        if not fiveg.is_empty():
            df = df.join(fiveg, on="date", how="left")
        df = df.join(suppliers, on="supplier_id", how="left") if "supplier_id" in df.columns else df
        df = df.join(sla, on="sla_id", how="left") if "sla_id" in df.columns else df

        self._log_feature_stats("assembled_training_frame", df)

        return df

    def build_training_set(self, target_column: str = "qty_consumed") -> TrainingSet:
        frame = self.assemble_training_frame().drop_nulls(subset=[target_column])
        feature_columns = {
            col
            for cols in FEATURE_GROUPS.values()
            for col in cols
            if col in frame.columns
        }
        feature_columns.update({"date", "item_id", "site_id"})

        feature_df = frame.select(sorted(feature_columns))
        self._log_feature_stats("feature_matrix", feature_df)
        self._update_scaler_manifest(_compute_basic_stats(feature_df))
        target = frame.select("date", target_column)

        feature_pd = feature_df.to_pandas()
        target_pd = target[target_column].to_pandas()

        if _HAS_CUDF:
            features_out = cudf.from_pandas(feature_pd)
            target_out = cudf.Series(target_pd)
            backend = "cudf"
        else:
            features_out = feature_pd
            target_out = target_pd
            backend = "pandas"

        metadata = {
            "snapshot": str(self.snapshot_path),
            "rows": str(len(feature_df)),
            "feature_columns": ",".join(sorted(feature_columns)),
            "backend": backend,
        }

        write_validation_result(
            "feature-set-metadata",
            {
                "metadata": metadata,
                "feature_stats": _compute_basic_stats(feature_df),
            },
        )

        return TrainingSet(features=features_out, target=target_out, metadata=metadata)

    def export_features(self, output_dir: Path | None = None) -> Path:
        output_dir = output_dir or ensure_directory(self.snapshot_path / "features")
        training_set = self.build_training_set()
        training_set.features.to_parquet(str(output_dir / "features.parquet"))
        training_set.target.to_frame(name="qty_consumed").to_parquet(
            str(output_dir / "target.parquet")
        )
        manifest_path = output_dir / "feature_manifest.json"
        columns = (
            list(training_set.features.columns)
            if hasattr(training_set.features, "columns")
            else list(feature_df.columns)
        )
        manifest_payload = {
            "feature_columns": columns,
            "metadata": training_set.metadata,
        }
        manifest_path.write_text(json.dumps(manifest_payload, indent=2), encoding="utf-8")
        return output_dir

