"""
Stage manually downloaded Baltic Dry Index CSV into the external landing zone.

Usage example:
    python -m scripts.etl.manual.baltic_dry_ingest --source data/manual/baltic/BalticDry.csv
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

from ..external import configure_logging, ensure_directory


logger = configure_logging("baltic_dry_ingest")

LANDING_ROOT = Path("data/landing/external_factors-raw/logistics/baltic_dry")
START_DATE = pd.Timestamp("2021-01-01")

COLUMN_ALIASES = {
    "date": {"DATE", "Date", "date"},
    "value": {"BDIY", "Value", "value", "Close", "Price"},
}


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest manual Baltic Dry Index CSV.")
    parser.add_argument("--source", type=Path, required=True, help="Path to downloaded CSV.")
    parser.add_argument("--timestamp", type=str, default=None, help="Override run stamp (YYYYMMDD).")
    return parser.parse_args(args)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns = {col.lower(): col for col in df.columns}

    date_col = next(
        (columns[name.lower()] for name_set in [COLUMN_ALIASES["date"]] for name in name_set if name.lower() in columns),
        None,
    )
    value_col = next(
        (columns[name.lower()] for name_set in [COLUMN_ALIASES["value"]] for name in name_set if name.lower() in columns),
        None,
    )

    if not date_col or not value_col:
        raise ValueError(
            f"Source file must contain a date column ({COLUMN_ALIASES['date']}) and value column ({COLUMN_ALIASES['value']})."
        )

    df = df[[date_col, value_col]].rename(columns={date_col: "date", value_col: "value"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["date", "value"])
    df = df[df["date"] >= START_DATE].sort_values("date")
    return df


def ingest(source_path: Path, run_stamp: str) -> Path:
    target_dir = LANDING_ROOT / run_stamp
    ensure_directory(target_dir)
    target_path = target_dir / "baltic_dry.csv"

    df = pd.read_csv(source_path, comment="#")
    df = normalize_columns(df)
    df.to_csv(target_path, index=False)
    logger.info("Ingested %s rows to %s", len(df), target_path)
    return target_path


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    if not options.source.exists():
        logger.error("Source file %s does not exist.", options.source)
        return
    run_stamp = options.timestamp or dt.datetime.utcnow().strftime("%Y%m%d")
    ingest(options.source, run_stamp)


if __name__ == "__main__":
    main()

