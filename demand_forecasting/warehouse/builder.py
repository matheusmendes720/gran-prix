from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import polars as pl

from demand_forecasting.flows.utils import LANDING_ROOT, PROJECT_ROOT, ensure_directory
from demand_forecasting.validation.utils import write_validation_result
from demand_forecasting.validation.validators import validate_fact_backfill, validate_fact_demand

from .utils import concat_parquet, gold_snapshot_folder


WORKBOOK_PATH = PROJECT_ROOT / "docs" / "proj" / "dadosSuprimentos.xlsx"
BACKFILL_PATH = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_fact_backfill.parquet"


@dataclass
class WarehouseBuilder:
    execution_ts: datetime | None = None
    workbook_path: Path = WORKBOOK_PATH

    def __post_init__(self) -> None:
        self.execution_ts = self.execution_ts or datetime.utcnow()
        if not self.workbook_path.exists():
            raise FileNotFoundError(
                f"Workbook '{self.workbook_path}' not found. Ensure it is available before running."
            )
        self._processed_fact_cache: Optional[pd.DataFrame] = None

    # ------------------------------------------------------------------
    # Workbook loaders
    # ------------------------------------------------------------------
    def _load_excel(self, sheet_name: str) -> pl.DataFrame:
        frame = pd.read_excel(self.workbook_path, sheet_name=sheet_name)
        return pl.from_pandas(frame)

    def _load_processed_fact(self) -> pd.DataFrame:
        if self._processed_fact_cache is None:
            fallback_path = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_processed.csv"
            if not fallback_path.exists():
                raise FileNotFoundError(
                    "Fallback dataset 'nova_corrente_processed.csv' not found; ensure workbook sheets exist or processed data is available."
                )
            self._processed_fact_cache = pd.read_csv(fallback_path)
        return self._processed_fact_cache

    def build_dim_item(self) -> pl.DataFrame:
        try:
            df = self._load_excel("Itens")
            expected_cols = {"item_id", "item_name", "category", "sku"}
            missing = expected_cols - set(df.columns)
            if missing:
                raise ValueError(f"Missing columns in Itens sheet: {missing}")
            return df.with_columns(pl.col("item_id").cast(pl.Int64))
        except Exception:
            processed = self._load_processed_fact()
            items = (
                processed[["item_id", "material", "category"]]
                .drop_duplicates()
                .rename(columns={"material": "item_name"})
            )
            items["sku"] = items["item_id"].astype(str)
            return pl.from_pandas(items)

    def build_dim_site(self) -> pl.DataFrame:
        try:
            df = self._load_excel("Sites")
            expected_cols = {"site_id", "region", "latitude", "longitude"}
            missing = expected_cols - set(df.columns)
            if missing:
                raise ValueError(f"Missing columns in Sites sheet: {missing}")
            return df.with_columns(
                pl.col("site_id").cast(pl.Int64),
                pl.col("latitude").cast(pl.Float64),
                pl.col("longitude").cast(pl.Float64),
            )
        except Exception:
            processed = self._load_processed_fact()
            sites = (
                processed[["site_id", "deposito"]]
                .drop_duplicates()
                .rename(columns={"deposito": "region"})
            )
            return pl.from_pandas(sites)

    def build_dim_supplier(self) -> pl.DataFrame:
        try:
            df = self._load_excel("Fornecedores")
            expected_cols = {"supplier_id", "lead_time_days"}
            missing = expected_cols - set(df.columns)
            if missing:
                raise ValueError(f"Missing columns in Fornecedores sheet: {missing}")
            return df.with_columns(pl.col("supplier_id").cast(pl.Int64))
        except Exception:
            processed = self._load_processed_fact()
            suppliers = (
                processed[["fornecedor", "lead_time_days"]]
                .rename(columns={"fornecedor": "supplier_id"})
                .drop_duplicates()
            )
            return pl.from_pandas(suppliers)

    def build_dim_operational(self) -> pl.DataFrame:
        try:
            df = self._load_excel("SLAs")
            return df.with_columns(pl.col("sla_id").cast(pl.Int64))
        except Exception:
            fallback = pd.DataFrame(
                {
                    "sla_id": [1],
                    "sla_tier": ["default"],
                    "response_hours": [24],
                }
            )
            return pl.from_pandas(fallback)

    def build_fact_demand(self) -> pl.DataFrame:
        try:
            df = self._load_excel("ConsumoHistorico")
            expected_cols = {"date", "item_id", "site_id", "qty_consumed"}
            missing = expected_cols - set(df.columns)
            if missing:
                raise ValueError(f"Missing columns in ConsumoHistorico sheet: {missing}")
            return df.with_columns(
                pl.col("date").cast(pl.Date),
                pl.col("item_id").cast(pl.Int64),
                pl.col("site_id").cast(pl.Int64),
                pl.col("qty_consumed").cast(pl.Float64),
            )
        except Exception:
            processed = self._load_processed_fact()
            fact = processed.rename(columns={"quantidade": "qty_consumed"})[
                ["date", "item_id", "site_id", "qty_consumed", "lead_time_days", "fornecedor"]
            ]
            fact["date"] = pd.to_datetime(fact["date"]).dt.date
            grouped = (
                fact.groupby(["date", "item_id", "site_id"], as_index=False)
                .agg({
                    "qty_consumed": "sum",
                    "lead_time_days": "mean",
                    "fornecedor": "first",
                })
            )
            fact_df = pl.from_pandas(grouped)

            if BACKFILL_PATH.exists():
                backfill_df = pl.read_parquet(BACKFILL_PATH)
                if backfill_df.is_empty():
                    return fact_df
                # Align columns and types
                if "quantidade" in backfill_df.columns and "qty_consumed" not in backfill_df.columns:
                    backfill_df = backfill_df.rename({"quantidade": "qty_consumed"})
                backfill_df = backfill_df.with_columns(
                    pl.col("date").cast(pl.Date),
                    pl.col("item_id").cast(pl.Utf8),
                    pl.col("site_id").cast(pl.Int64),
                    pl.col("qty_consumed").cast(pl.Float64),
                )
                if "lead_time_days" in backfill_df.columns:
                    backfill_df = backfill_df.with_columns(pl.col("lead_time_days").cast(pl.Float64))
                else:
                    backfill_df = backfill_df.with_columns(pl.lit(None).alias("lead_time_days"))
                if "fornecedor" not in backfill_df.columns:
                    backfill_df = backfill_df.with_columns(pl.lit(None).alias("fornecedor"))

                actual_start = fact_df["date"].min()
                payload = validate_fact_backfill(backfill_df.to_pandas(), actual_start)
                payload["metadata"] = {"execution_ts": self.execution_ts.isoformat()}
                write_validation_result("fact-demand-backfill", payload)

                fact_cols = set(fact_df.columns)
                back_cols = set(backfill_df.columns)
                for missing in fact_cols - back_cols:
                    backfill_df = backfill_df.with_columns(pl.lit(None).alias(missing))
                for missing in back_cols - fact_cols:
                    fact_df = fact_df.with_columns(pl.lit(None).alias(missing))

                column_order: list[str] = list(fact_df.columns)
                for name in backfill_df.columns:
                    if name not in column_order:
                        column_order.append(name)
                backfill_df = backfill_df.select(column_order)
                fact_df = fact_df.select(column_order)

                fact_df = pl.concat([backfill_df, fact_df], how="vertical").sort(["date", "item_id", "site_id"])

            return fact_df

    # ------------------------------------------------------------------
    # External dimensions
    # ------------------------------------------------------------------
    def build_dim_weather(self) -> pl.DataFrame:
        files = list((LANDING_ROOT / "silver" / "climate").glob("**/climate-*.parquet"))
        return concat_parquet(files)

    def build_dim_economic(self) -> pl.DataFrame:
        files = list((LANDING_ROOT / "silver" / "economic").glob("**/economic-*.parquet"))
        return concat_parquet(files)

    def build_dim_regulatory(self) -> pl.DataFrame:
        files = list((LANDING_ROOT / "silver" / "regulatory").glob("**/regulatory-*.parquet"))
        return concat_parquet(files)

    def build_dim_calendar(self, fact: pl.DataFrame) -> pl.DataFrame:
        return fact.select(pl.col("date").unique().alias("date")).with_columns(
            pl.col("date").alias("calendar_date"),
            pl.col("date").dt.weekday().alias("weekday"),
            pl.col("date").dt.month().alias("month"),
            pl.col("date").dt.year().alias("year"),
        )

    # ------------------------------------------------------------------
    # Merge
    # ------------------------------------------------------------------
    def merge_fact(self, fact: pl.DataFrame, dim_weather: pl.DataFrame, dim_economic: pl.DataFrame) -> pl.DataFrame:
        result = fact
        if not dim_weather.is_empty():
            result = result.join(dim_weather, on="date", how="left")
        if not dim_economic.is_empty():
            result = result.join(dim_economic, left_on="date", right_on="observed_at", how="left")
        return result

    # ------------------------------------------------------------------
    # Persist
    # ------------------------------------------------------------------
    def persist_tables(self, tables: Dict[str, pl.DataFrame]) -> Path:
        snapshot_dir = gold_snapshot_folder(self.execution_ts)
        for name, df in tables.items():
            path = snapshot_dir / f"{name}.parquet"
            ensure_directory(path.parent)
            if df.is_empty():
                pl.DataFrame().write_parquet(path)
            else:
                df.write_parquet(path)
        return snapshot_dir

    # ------------------------------------------------------------------
    def run(self) -> Path:
        dim_item = self.build_dim_item()
        dim_site = self.build_dim_site()
        dim_supplier = self.build_dim_supplier()
        dim_operational = self.build_dim_operational()
        fact_demand = self.build_fact_demand()

        dim_weather = self.build_dim_weather()
        dim_economic = self.build_dim_economic()
        dim_regulatory = self.build_dim_regulatory()

        fact_enriched = self.merge_fact(fact_demand, dim_weather, dim_economic)
        dim_calendar = self.build_dim_calendar(fact_demand)

        validation_payload = validate_fact_demand(fact_demand.to_pandas())
        validation_payload["metadata"] = {"execution_ts": self.execution_ts.isoformat()}
        write_validation_result("fact-demand", validation_payload)

        tables = {
            "DimItem": dim_item,
            "DimSite": dim_site,
            "DimSupplier": dim_supplier,
            "DimOperational": dim_operational,
            "DimWeather": dim_weather,
            "DimEconomic": dim_economic,
            "DimRegulatory": dim_regulatory,
            "DimCalendar": dim_calendar,
            "FactDemand": fact_enriched,
        }

        return self.persist_tables(tables)

