"""
Fetch Baltic Dry Index (BDIY) observations from FRED and save to manual staging.

Usage:
    python -m scripts.automation.fetch_bdi_fred \
        --start-date 2021-01-01 --end-date 2025-11-10
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import requests

DEFAULT_START = dt.date(2021, 1, 1)
DEFAULT_END = dt.date(2025, 11, 10)
SERIES_ID = "BDIY"
MANUAL_DIR = Path("data/manual/baltic")


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Baltic Dry Index (BDIY) from FRED API.")
    parser.add_argument("--start-date", type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(), default=DEFAULT_START)
    parser.add_argument("--end-date", type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(), default=DEFAULT_END)
    parser.add_argument("--api-key", type=str, default=os.getenv("FRED_API_KEY"))
    parser.add_argument("--output", type=Path, default=None, help="Optional explicit output path.")
    return parser.parse_args(args)


def fetch_series(api_key: str, start: dt.date, end: dt.date) -> pd.DataFrame:
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": SERIES_ID,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start.isoformat(),
        "observation_end": end.isoformat(),
    }
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json().get("observations", [])
    if not data:
        raise ValueError("No observations returned from FRED.")
    df = pd.DataFrame(data)
    if "date" not in df or "value" not in df:
        raise ValueError("Unexpected payload structure from FRED.")
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"]).sort_values("date")
    return df[["date", "value"]]


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    api_key = options.api_key
    if not api_key:
        raise SystemExit("FRED API key required. Provide via --api-key or FRED_API_KEY env var.")

    df = fetch_series(api_key, options.start_date, options.end_date)

    MANUAL_DIR.mkdir(parents=True, exist_ok=True)
    output_path = options.output or MANUAL_DIR / f"BalticDry_FRED_{options.start_date}_{options.end_date}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")


if __name__ == "__main__":
    main()

