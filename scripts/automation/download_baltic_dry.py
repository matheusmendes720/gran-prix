"""
Automated Baltic Dry Index downloader using Playwright request context.

Downloads the FRED DBDIY series as CSV, filters to desired date range,
stages it via the manual ingest helper, and optionally triggers the Silver
and Feature transformations.
"""

from __future__ import annotations

import argparse
import datetime as dt
from io import BytesIO
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
from playwright.sync_api import sync_playwright

from scripts.etl.manual import baltic_dry_ingest
from scripts.etl.transform import external_to_silver
from scripts.etl.feature import build_external_features


DEFAULT_START = dt.date(2021, 1, 1)
DEFAULT_END = dt.date(2025, 11, 10)
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=BDIY"


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Baltic Dry Index via Playwright.")
    parser.add_argument("--start-date", type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(), default=DEFAULT_START)
    parser.add_argument("--end-date", type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(), default=DEFAULT_END)
    parser.add_argument("--output-dir", type=Path, default=Path("data/manual/baltic"))
    parser.add_argument("--skip-transform", action="store_true", help="Skip running Silver/Feature transforms after ingest.")
    parser.add_argument("--timestamp", type=str, default=None, help="Override run stamp for landing directory.")
    return parser.parse_args(args)


def download_csv(start: dt.date, end: dt.date, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.get(FRED_URL, timeout=60000)
        if not response.ok:
            raise RuntimeError(f"Failed to download BDI CSV: {response.status} {response.status_text}")
        csv_bytes = response.body()
    df = pd.read_csv(BytesIO(csv_bytes))
    if "DATE" not in df.columns or "BDIY" not in df.columns:
        raise ValueError("Unexpected CSV format from FRED BDI download.")
    df["DATE"] = pd.to_datetime(df["DATE"])
    mask = (df["DATE"].dt.date >= start) & (df["DATE"].dt.date <= end)
    df = df.loc[mask, ["DATE", "BDIY"]].rename(columns={"DATE": "date", "BDIY": "value"})
    df.to_csv(output_path, index=False)
    return output_path


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    output_dir = options.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_csv_path = output_dir / f"bdi_fred_{options.start_date}_{options.end_date}.csv"

    try:
        download_csv(options.start_date, options.end_date, raw_csv_path)
    except Exception as exc:
        raise SystemExit(f"Failed to download Baltic Dry Index CSV: {exc}") from exc

    run_stamp = options.timestamp or dt.datetime.utcnow().strftime("%Y%m%d")
    staged_path = baltic_dry_ingest.ingest(raw_csv_path, run_stamp)  # type: ignore[arg-type]

    if not options.skip_transform:
        external_to_silver.transform_all()
        build_external_features.main()

    print(f"Baltic Dry Index data downloaded to {raw_csv_path} and staged via {staged_path}.")


if __name__ == "__main__":
    main()

