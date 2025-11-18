"""Build storytelling-ready datasets for Nova Corrente dashboards.

Usage
-----
    python -m scripts.storytelling.build_storytelling_assets \
        --gold-path data/warehouse/gold/20251111T164236/FactDemand.parquet \
        --forecasts-dir data/outputs/nova_corrente/forecasts \
        --output-dir data/outputs/nova_corrente/storytelling
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import timedelta
from pathlib import Path
from typing import Dict, List

import pandas as pd
import polars as pl


SERIES_SANITIZER = re.compile(r"[^0-9A-Za-z_.-]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate storytelling assets for dashboards.")
    parser.add_argument(
        "--gold-path",
        type=Path,
        required=True,
        help="Path to Gold FactDemand parquet (e.g. data/warehouse/gold/<ts>/FactDemand.parquet).",
    )
    parser.add_argument(
        "--forecasts-dir",
        type=Path,
        required=True,
        help="Directory containing forecast parquet files and prescriptive JSONs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/outputs/nova_corrente/storytelling"),
        help="Directory to write storytelling datasets.",
    )
    parser.add_argument(
        "--history-days",
        type=int,
        default=365,
        help="Number of historical days to retain for actuals (default: 365).",
    )
    return parser.parse_args()


def sanitize_series_key(item_id: str, site_id: str | int) -> str:
    raw = f"item{item_id}_site{site_id}"
    safe = SERIES_SANITIZER.sub("_", raw).strip("_")
    return safe or f"series_{abs(hash(raw))}"


def sanitize_filename(stem: str) -> str:
    return SERIES_SANITIZER.sub("_", stem).strip("_")


def load_fact_metadata(gold_path: Path, history_days: int) -> Dict[str, pd.DataFrame]:
    if not gold_path.exists():
        raise FileNotFoundError(f"Gold FactDemand parquet not found: {gold_path}")

    fact = pl.read_parquet(gold_path)
    fact = fact.with_columns(pl.col("date").cast(pl.Date))

    max_date = fact.select(pl.col("date").max()).item()
    cutoff = max_date - timedelta(days=history_days)

    meta_cols = [
        "item_id",
        "site_id",
        "familia",
        "category",
        "region",
        "deposito",
    ]
    metadata = (
        fact.select(meta_cols)
        .unique(subset=["item_id", "site_id"], keep="first")
        .with_columns(pl.col("item_id").cast(pl.Utf8))
    )
    metadata_pd = metadata.to_pandas()
    metadata_pd["series_key"] = metadata_pd.apply(
        lambda row: sanitize_series_key(row["item_id"], row["site_id"]), axis=1
    )

    actuals = (
        fact.filter(pl.col("date") >= pl.lit(cutoff))
        .select(["date", "item_id", "site_id", "qty_consumed"])
        .with_columns(pl.col("item_id").cast(pl.Utf8))
    )
    actuals_pd = actuals.to_pandas()
    actuals_pd["series_key"] = actuals_pd.apply(
        lambda row: sanitize_series_key(row["item_id"], row["site_id"]), axis=1
    )
    actuals_pd.rename(columns={"date": "ds", "qty_consumed": "actual_qty"}, inplace=True)
    actuals_pd["ds"] = pd.to_datetime(actuals_pd["ds"])

    return {"metadata": metadata_pd, "actuals": actuals_pd}


def load_forecasts(forecasts_dir: Path) -> pd.DataFrame:
    if not forecasts_dir.exists():
        raise FileNotFoundError(f"Forecast directory not found: {forecasts_dir}")

    rows: List[pd.DataFrame] = []
    parquet_files = sorted(forecasts_dir.glob("item*_site*.parquet"))
    for path in parquet_files:
        try:
            df = pd.read_parquet(path)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[storytelling] ⚠️ Could not read {path.name}: {exc}")
            continue

        stem = path.stem
        series_key = sanitize_filename(stem)

        df = df.copy()
        df["series_key"] = series_key
        df.rename(columns={"forecast": "forecast_qty"}, inplace=True)
        df["ds"] = pd.to_datetime(df["ds"])
        rows.append(df)

    if not rows:
        raise RuntimeError(f"No forecast parquet files found in {forecasts_dir}")

    combined = pd.concat(rows, ignore_index=True)
    return combined


def load_prescriptions(forecasts_dir: Path) -> pd.DataFrame:
    records = []
    json_files = sorted(forecasts_dir.glob("item*_site*_prescriptive.json"))
    for path in json_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"[storytelling] ⚠️ Invalid JSON {path.name}: {exc}")
            continue

        stem = path.stem.replace("_prescriptive", "")
        series_key = sanitize_filename(stem)
        record = {"series_key": series_key, "source_file": path.name}
        record.update(data)
        records.append(record)

    if not records:
        raise RuntimeError(f"No prescriptive JSON files found in {forecasts_dir}")

    return pd.DataFrame(records)


def compute_summary(metadata: pd.DataFrame, prescriptions: pd.DataFrame) -> Dict[str, object]:
    critical = prescriptions[prescriptions.get("stock_status") == "critical"]
    summary = {
        "series_total": int(len(metadata)),
        "series_with_forecast": int(prescriptions["series_key"].nunique()),
        "critical_series": int(critical["series_key"].nunique()),
        "timestamp": pd.Timestamp.utcnow().isoformat(),
    }
    return summary


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fact_data = load_fact_metadata(args.gold_path, args.history_days)
    metadata = fact_data["metadata"]
    actuals = fact_data["actuals"]

    forecasts = load_forecasts(args.forecasts_dir)
    prescriptions = load_prescriptions(args.forecasts_dir)

    # Merge actuals + forecasts
    timeseries = (
        forecasts.merge(metadata, on="series_key", how="left")
        .merge(actuals, on=["series_key", "ds", "item_id", "site_id"], how="left")
    )
    timeseries["familia"] = timeseries["familia"].fillna("UNKNOWN")
    timeseries["category"] = timeseries["category"].fillna("UNKNOWN")
    timeseries["region"] = timeseries["region"].fillna("UNKNOWN")

    timeseries_path = args.output_dir / "storytelling_timeseries.parquet"
    timeseries.to_parquet(timeseries_path, index=False)

    # Prescriptive alerts with metadata
    prescriptive = prescriptions.merge(metadata, on="series_key", how="left")
    prescriptive_path = args.output_dir / "storytelling_prescriptions.parquet"
    prescriptive.to_parquet(prescriptive_path, index=False)

    # Summary JSON
    summary = compute_summary(metadata, prescriptions)
    summary_path = args.output_dir / "storytelling_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("[storytelling] Generated storytelling datasets:")
    print(f"  - {timeseries_path}")
    print(f"  - {prescriptive_path}")
    print(f"  - {summary_path}")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()

