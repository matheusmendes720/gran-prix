"""
Download Baltic Dry Index historical data (Investing.com) using Playwright context.

The script navigates to the Investing.com Baltic Dry Historical Data page to obtain the
necessary cookies, then calls the authenticated JSON endpoint for the desired date range.
Results are saved to CSV and staged via the manual ingest helper.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
from playwright.sync_api import sync_playwright

from scripts.etl.manual import baltic_dry_ingest
from scripts.etl.transform import external_to_silver
from scripts.etl.feature import build_external_features

INVESTING_URL = "https://www.investing.com/indices/baltic-dry-historical-data"
ENDPOINT = "https://api.investing.com/api/financialdata/historical/940793"
DEFAULT_START = dt.date(2021, 1, 1)
DEFAULT_END = dt.date(2025, 11, 10)


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Baltic Dry Index from Investing.com via Playwright.")
    parser.add_argument("--start-date", type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(), default=DEFAULT_START)
    parser.add_argument("--end-date", type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(), default=DEFAULT_END)
    parser.add_argument("--output-dir", type=Path, default=Path("data/manual/baltic"))
    parser.add_argument("--skip-transform", action="store_true")
    parser.add_argument("--timestamp", type=str, default=None, help="Override run stamp for ingest staging.")
    parser.add_argument("--headless", action="store_true", default=False, help="Run browser headless (default: False for resilience).")
    return parser.parse_args(args)


def fetch_bdi_dataframe(start: dt.date, end: dt.date, headless: bool) -> pd.DataFrame:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
        page = context.new_page()
        page.goto(INVESTING_URL, wait_until="domcontentloaded", timeout=120000)
        # Accept cookies if banner appears
        try:
            page.locator("button:has-text('Accept All')").first.click(timeout=5000)
        except Exception:
            pass
        script = """
        async ({ endpoint, start, end }) => {
            const params = new URLSearchParams({
                "start-date": start,
                "end-date": end,
                "time-frame": "Daily",
                "add-missing-rows": "false"
            });
            const response = await fetch(`${endpoint}?${params.toString()}`, {
                method: "GET",
                headers: {
                    "domain-id": "www",
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
                credentials: "include"
            });
            if (!response.ok) {
                throw new Error(`Fetch failed: ${response.status} ${response.statusText}`);
            }
            return await response.json();
        }
        """
        data = page.evaluate(script, {"endpoint": ENDPOINT, "start": start.isoformat(), "end": end.isoformat()})
        browser.close()

    if not data or "data" not in data:
        raise ValueError("Unexpected JSON payload from Investing API.")

    rows = data["data"]
    df = pd.DataFrame(rows)
    # Response includes columns like date, value, open, high, low; keep closing value.
    if "row" in df.columns:
        # Some responses nest data under 'row'
        df = pd.json_normalize(df["row"])
    column_candidates = ["value", "close", "Price"]
    value_col = next((col for col in column_candidates if col in df.columns), None)
    date_col = next((col for col in ["date", "Date"] if col in df.columns), None)
    if not value_col or not date_col:
        raise ValueError("Could not identify date/value columns in API response.")

    df = df[[date_col, value_col]].rename(columns={date_col: "date", value_col: "value"})
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["date", "value"]).sort_values("date")
    return df


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    output_dir = options.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_csv_path = output_dir / f"bdi_investing_{options.start_date}_{options.end_date}.csv"

    df = fetch_bdi_dataframe(options.start_date, options.end_date, headless=options.headless)
    df.to_csv(raw_csv_path, index=False)

    run_stamp = options.timestamp or dt.datetime.utcnow().strftime("%Y%m%d")
    staged_path = baltic_dry_ingest.ingest(raw_csv_path, run_stamp)  # type: ignore[arg-type]

    if not options.skip_transform:
        external_to_silver.transform_all()
        build_external_features.main()

    print(f"Investing BDI data saved to {raw_csv_path} and staged via {staged_path}.")


if __name__ == "__main__":
    main()

