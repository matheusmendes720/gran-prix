"""
Normalize manually downloaded Freightos FBX CSV files into the logistics landing zone.

Expected input columns (case-insensitive):
    - Date
    - Value / Price / FBX

Usage:
    python -m scripts.etl.manual.freightos_ingest --source data/manual/freightos/fbx_global.csv
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

from ..external import configure_logging, ensure_directory


logger = configure_logging("freightos_ingest")

LANDING_ROOT = Path("data/landing/external_factors-raw/logistics/freightos")
START_DATE = pd.Timestamp("2021-01-01")

COLUMN_ALIASES = {
    "date": {"date", "Date"},
    "value": {"value", "Value", "price", "Price", "fbx", "FBX", "FBX Global Average"},
}


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest manual Freightos FBX CSV.")
    parser.add_argument("--source", type=Path, required=True, help="Path to downloaded CSV.")
    parser.add_argument("--timestamp", type=str, default=None, help="Override run stamp (YYYYMMDD).")
    return parser.parse_args(args)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    lower_map = {col.lower(): col for col in df.columns}

    def find_column(alias_set: set[str]) -> Optional[str]:
        for alias in alias_set:
            if alias.lower() in lower_map:
                return lower_map[alias.lower()]
        return None

    date_col = find_column(COLUMN_ALIASES["date"])
    value_col = find_column(COLUMN_ALIASES["value"])

    if not date_col or not value_col:
        raise ValueError(
            "Source file must contain a date column and a value/price/FBX column."
        )

    df = df[[date_col, value_col]].rename(columns={date_col: "date", value_col: "value"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(
        df["value"].astype(str).str.replace(",", ""),
        errors="coerce",
    )
    df = df.dropna(subset=["date", "value"])
    df = df[df["date"] >= START_DATE]
    df = df.sort_values("date")
    return df


def ingest(source_path: Path, run_stamp: str) -> Path:
    ensure_directory(LANDING_ROOT / run_stamp)
    target_path = LANDING_ROOT / run_stamp / "freightos_fbx.csv"

    df = pd.read_csv(source_path)
    df = normalize_columns(df)
    df.to_csv(target_path, index=False)
    logger.info("Ingested %s rows to %s", len(df), target_path)
    return target_path


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    if not options.source.exists():
        logger.error("Source file %s does not exist.", options.source)
        raise SystemExit(1)
    run_stamp = options.timestamp or dt.datetime.utcnow().strftime("%Y%m%d")
    ingest(options.source, run_stamp)


if __name__ == "__main__":
    main()

