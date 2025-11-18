"""
Download macro fallback indicators from FRED (St. Louis Fed).

Series currently collected:
    - BRACDSADSMEI: Brazil 5-Year Credit Default Swap (CDS) Spread
    - PPPBRAA226GDPPT: PPP conversion factor (World Bank, annual)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Dict, Iterable, Optional

import requests

from . import configure_logging, ensure_directory

logger = configure_logging("fred")

LANDING_ROOT = Path("data/landing/external_factors-raw/macro/fred")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
REQUEST_TIMEOUT = 60

SERIES: Dict[str, Dict[str, str]] = {
    "cds": {
        "series_id": "DDSI06BRA156NWDB",
        "frequency": "monthly",
    },
    "ppp": {
        "series_id": "PPPTTLBRA618NUPN",
        "frequency": "annual",
    },
}


def fetch_observations(series_id: str, api_key: str, start: str, end: str) -> Optional[list]:
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start,
        "observation_end": end,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
        observations = payload.get("observations", [])
        if not observations:
            logger.warning("FRED returned empty observations for %s", series_id)
            return None
        return observations
    except requests.exceptions.HTTPError as exc:
        logger.error("FRED HTTP error for series %s: %s", series_id, exc)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Unexpected error fetching %s: %s", series_id, exc)
    return None


def save_payload(slug: str, payload: list, timestamp: str) -> Path:
    output_dir = LANDING_ROOT / slug / timestamp
    ensure_directory(output_dir)
    out_path = output_dir / f"{slug}.json"
    with out_path.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)
    logger.info("Saved %s records to %s", len(payload), out_path)
    return out_path


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download macro fallback series from FRED.")
    parser.add_argument(
        "--series",
        nargs="+",
        default=list(SERIES.keys()),
        help=f"Series slugs to download (options: {', '.join(SERIES.keys())})",
    )
    parser.add_argument("--start", type=str, default="2010-01-01", help="Observation start date (YYYY-MM-DD).")
    parser.add_argument("--end", type=str, default=dt.date.today().isoformat(), help="Observation end date (YYYY-MM-DD).")
    parser.add_argument("--timestamp", type=str, default=None, help="Override output timestamp (YYYYMMDD).")
    return parser.parse_args(args)


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    run_stamp = options.timestamp or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        logger.error("FRED_API_KEY environment variable not set. Aborting download.")
        return

    for slug in options.series:
        config = SERIES.get(slug)
        if not config:
            logger.warning("Unknown FRED series %s; skipping.", slug)
            continue

        logger.info(
            "Fetching FRED series '%s' (id=%s) from %s to %s",
            slug,
            config["series_id"],
            options.start,
            options.end,
        )
        observations = fetch_observations(config["series_id"], api_key, options.start, options.end)
        if not observations:
            continue
        save_payload(slug, observations, run_stamp)

    logger.info("FRED download finished.")


if __name__ == "__main__":
    main()

