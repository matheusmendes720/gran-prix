"""
Download logistics benchmark indicators (container traffic, air freight) from the World Bank API.

Serves as an open proxy for freight/shipping benchmarks while API access keys for
providers like Freightos or Drewry are pending.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd
import requests

from . import configure_logging, ensure_directory


logger = configure_logging("freight")

BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
LANDING_DIR = Path("data/landing/external_factors-raw/logistics/freight")
REQUEST_TIMEOUT = 60


@dataclass
class IndicatorConfig:
    name: str
    indicator_id: str
    countries: List[str]


INDICATORS: List[IndicatorConfig] = [
    IndicatorConfig(
        name="container_port_traffic_teu",
        indicator_id="IS.SHP.GOOD.TU",
        countries=["BR", "WLD"],
    ),
    IndicatorConfig(
        name="air_freight_mtkm",
        indicator_id="IS.AIR.GOOD.MT.K1",
        countries=["BR", "WLD"],
    ),
]


def fetch_indicator(indicator: IndicatorConfig, start_year: Optional[int] = None) -> pd.DataFrame:
    records: List[Dict] = []
    for country in indicator.countries:
        url = BASE_URL.format(country=country, indicator=indicator.indicator_id)
        params = {"format": "json", "per_page": 2000}
        logger.info("Fetching %s for %s (%s)", indicator.name, country, indicator.indicator_id)
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list) or len(data) < 2:
            logger.warning("Unexpected response for %s %s", indicator.name, country)
            continue
        entries = data[1]
        for entry in entries:
            value = entry.get("value")
            date = entry.get("date")
            if value is None or date is None:
                continue
            try:
                year = int(date)
            except ValueError:
                continue
            if start_year and year < start_year:
                continue
            records.append(
                {
                    "date": dt.datetime(year, 1, 1),
                    "country": entry.get("countryiso3code", country),
                    "metric": indicator.name,
                    "value": float(value),
                }
            )
    if not records:
        return pd.DataFrame(columns=["date", "country", "metric", "value"])
    df = pd.DataFrame(records)
    df.sort_values(["metric", "country", "date"], inplace=True)
    return df


def save_indicator(df: pd.DataFrame, indicator_name: str, run_stamp: str) -> None:
    ensure_directory(LANDING_DIR / run_stamp)
    output_path = LANDING_DIR / run_stamp / f"{indicator_name}.csv"
    df.to_csv(output_path, index=False)
    logger.info("Saved %s rows of %s to %s", len(df), indicator_name, output_path)


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download freight/shipping benchmark indicators.")
    parser.add_argument(
        "--start-year",
        type=int,
        default=2000,
        help="Earliest year to include (default: 2000).",
    )
    parser.add_argument(
        "--timestamp",
        type=str,
        default=None,
        help="Override output timestamp (YYYYMMDD).",
    )
    return parser.parse_args(args)


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    run_stamp = options.timestamp or dt.datetime.utcnow().strftime("%Y%m%d")
    for indicator in INDICATORS:
        try:
            df = fetch_indicator(indicator, start_year=options.start_year)
        except requests.RequestException as exc:
            logger.exception("Failed to download indicator %s: %s", indicator.name, exc)
            continue
        if df.empty:
            logger.warning("Indicator %s returned no data.", indicator.name)
            continue
        save_indicator(df, indicator.name, run_stamp)


if __name__ == "__main__":
    main()

