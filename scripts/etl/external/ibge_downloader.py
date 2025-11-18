"""
Download IBGE SIDRA series required for Nova Corrente forecasting.

Currently collects:
    - IPCA (t=1737, v=63) – variação mensal (%)
    - IPCA-15 (t=1705, v=355, c315=7169) – variação mensal (%)
    - INPC (t=1736, v=44) – variação mensal (%)
    - PIB trimestral (t=5932, v=6561) – taxa trimestral (%)
    - PIB anual (t=5938, v=37) – preços correntes (mil R$)
    - Taxa de desocupação PNAD contínua (t=6381, v=4099)

Extend the TABLES dictionary to add new series.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Dict, Iterable, Optional

import requests

from . import configure_logging, ensure_directory


logger = configure_logging("ibge")

LANDING_ROOT = Path("data/landing/external_factors-raw/macro/ibge")
REQUEST_TIMEOUT = 60
BASE_URL = "https://apisidra.ibge.gov.br/values"


TABLES = {
    "ipca": {
        "table": "1737",
        "variables": "63",
        "frequency": "monthly",
    },
    "ipca15": {
        "table": "7062",
        "variables": "355",
        "frequency": "monthly",
        "dimensions": {"c315": "7169"},  # índice geral
        "period_mode": "all",
    },
    "inpc": {
        "table": "1736",
        "variables": "44",
        "frequency": "monthly",
    },
    "pib_quarterly": {
        "table": "5932",
        "variables": "6561",
        "frequency": "quarterly",
    },
    "pib_annual": {
        "table": "5938",
        "variables": "37",
        "frequency": "annual",
    },
    "unemployment": {
        "table": "6381",
        "variables": "4099",
        "frequency": "monthly",
    },
}


def build_period(start: dt.date, end: dt.date, frequency: str, mode: str) -> str:
    if mode == "all":
        return "all"

    if frequency == "monthly":
        return f"{start.strftime('%Y%m')}-{end.strftime('%Y%m')}"

    if frequency == "quarterly":
        def fmt(date: dt.date) -> str:
            quarter = (date.month - 1) // 3 + 1
            return f"{date.year}{quarter:02d}"

        return f"{fmt(start)}-{fmt(end)}"

    if frequency == "annual":
        return f"{start.year}-{end.year}"

    raise ValueError(f"Unsupported frequency: {frequency}")


def fetch_table(table_config: Dict, period: str) -> Dict:
    path_segments = ["t", table_config["table"], "n1", "all"]
    for dim_code, dim_value in table_config.get("dimensions", {}).items():
        path_segments.extend([dim_code, dim_value])
    path_segments.extend(["v", table_config["variables"], "p", period])
    url = f"{BASE_URL}/{'/'.join(path_segments)}"
    logger.info("Fetching IBGE SIDRA table %s with period %s", table_config["table"], period)
    resp = requests.get(url, params={"formato": "json"}, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def save_json(data: Dict, output_path: Path) -> None:
    ensure_directory(output_path.parent)
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download IBGE SIDRA tables.")
    parser.add_argument(
        "--tables",
        nargs="+",
        default=list(TABLES.keys()),
        help=f"Tables to fetch (default: {', '.join(TABLES.keys())})",
    )
    parser.add_argument("--start", type=str, default="2015-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=dt.date.today().isoformat(), help="End date (YYYY-MM-DD)")
    parser.add_argument("--output-dir", type=Path, default=LANDING_ROOT, help="Landing directory")
    parser.add_argument("--timestamp", type=str, default=None, help="Override output timestamp (YYYYMMDD)")
    return parser.parse_args(args)


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    run_stamp = options.timestamp or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
    start_date = dt.datetime.strptime(options.start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(options.end, "%Y-%m-%d").date()

    for table_name in options.tables:
        config = TABLES.get(table_name)
        if not config:
            logger.warning("Unknown table %s; skipping.", table_name)
            continue
        period = build_period(
            start_date,
            end_date,
            config["frequency"],
            config.get("period_mode", "range"),
        )
        try:
            data = fetch_table(config, period)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to fetch table %s: %s", table_name, exc)
            continue
        out_path = options.output_dir / table_name / run_stamp / f"{table_name}.json"
        save_json(data, out_path)

    logger.info("IBGE download finished.")


if __name__ == "__main__":
    main()
