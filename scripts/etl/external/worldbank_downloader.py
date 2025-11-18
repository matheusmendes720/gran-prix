"""
Download selected World Bank indicators for Brazil.

Currently collects:
    - GDP (NY.GDP.MKTP.CD)
    - PPP GDP (NY.GDP.PPP.CD)
    - GDP growth annual % (NY.GDP.MKTP.KD.ZG)

Results stored in:
    data/landing/external_factors-raw/global/worldbank/<indicator>/<YYYYMMDD>.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Dict, Iterable, Optional

import requests

from . import configure_logging, ensure_directory


logger = configure_logging("worldbank")

LANDING_ROOT = Path("data/landing/external_factors-raw/global/worldbank")
REQUEST_TIMEOUT = 60
BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"

INDICATORS = {
    "gdp_current_usd": "NY.GDP.MKTP.CD",
    "gdp_ppp": "NY.GDP.MKTP.PP.CD",
    "gdp_growth_pct": "NY.GDP.MKTP.KD.ZG",
}


def fetch_indicator(country: str, indicator: str, per_page: int = 2000) -> Dict:
    url = BASE_URL.format(country=country, indicator=indicator)
    params = {"format": "json", "per_page": per_page}
    logger.info("Fetching World Bank indicator %s for %s", indicator, country)
    resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def save_json(data: Dict, output_path: Path) -> None:
    ensure_directory(output_path.parent)
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download World Bank indicators.")
    parser.add_argument(
        "--country",
        type=str,
        default="BR",
        help="Country code (default: BR)",
    )
    parser.add_argument(
        "--indicators",
        nargs="+",
        default=list(INDICATORS.keys()),
        help=f"Indicators to fetch (default: {', '.join(INDICATORS.keys())})",
    )
    parser.add_argument("--output-dir", type=Path, default=LANDING_ROOT, help="Landing directory")
    parser.add_argument("--timestamp", type=str, default=None, help="Override output timestamp (YYYYMMDD)")
    return parser.parse_args(args)


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    run_stamp = options.timestamp or dt.datetime.utcnow().strftime("%Y%m%d")

    for name in options.indicators:
        indicator_code = INDICATORS.get(name)
        if not indicator_code:
            logger.warning("Unknown indicator %s; skipping.", name)
            continue
        try:
            data = fetch_indicator(options.country, indicator_code)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to fetch indicator %s: %s", name, exc)
            continue
        out_path = options.output_dir / name / run_stamp / f"{name}.json"
        save_json(data, out_path)

    logger.info("World Bank download finished.")


if __name__ == "__main__":
    main()

