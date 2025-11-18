"""
Download macroeconomic series from Banco Central do Brasil (BACEN).

Currently collects:
    - PTAX exchange rates for USD, EUR, CNY.
    - Selic (bcdata.sgs.432) daily series.

Raw JSON files are written to:
    data/landing/external_factors-raw/macro/bacen/<series>/<YYYYMMDD>.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Dict, Iterable, Optional

import requests

from . import configure_logging, ensure_directory


logger = configure_logging("bacen")

LANDING_ROOT = Path("data/landing/external_factors-raw/macro/bacen")
REQUEST_TIMEOUT = 60

PTAX_URL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
)
SELlC_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"


def today_str() -> str:
    return dt.datetime.utcnow().strftime("%Y%m%d")


def save_json(data: Dict, output_path: Path) -> None:
    ensure_directory(output_path.parent)
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def fetch_ptax(currency: str, start: dt.date, end: dt.date) -> Dict:
    params = {
        "@moeda": f"'{currency}'",
        "@dataInicial": f"'{start.strftime('%m-%d-%Y')}'",
        "@dataFinalCotacao": f"'{end.strftime('%m-%d-%Y')}'",
        "$format": "json",
    }
    logger.info("Fetching PTAX for %s (%s -> %s)", currency, start, end)
    resp = requests.get(PTAX_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fetch_selic(start: dt.date, end: dt.date) -> Dict:
    all_rows: list = []
    chunk_start = start
    chunk_days = 1825  # 5 years per request to respect API limit

    while chunk_start <= end:
        chunk_end = min(chunk_start + dt.timedelta(days=chunk_days), end)
        params = {
            "formato": "json",
            "dataInicial": chunk_start.strftime("%d/%m/%Y"),
            "dataFinal": chunk_end.strftime("%d/%m/%Y"),
        }
        logger.info("Fetching Selic series chunk (%s -> %s)", chunk_start, chunk_end)
        resp = requests.get(SELlC_URL, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        if not resp.text.strip():
            logger.warning("Empty response for chunk %s -> %s", chunk_start, chunk_end)
            chunk_start = chunk_end + dt.timedelta(days=1)
            continue

        try:
            all_rows.extend(resp.json())
        except ValueError as exc:  # JSONDecodeError
            logger.warning("Failed to decode Selic chunk %s -> %s: %s", chunk_start, chunk_end, exc)
        chunk_start = chunk_end + dt.timedelta(days=1)

    return {"data": all_rows}


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download BACEN PTAX and Selic series.")
    parser.add_argument("--start", type=str, default="2015-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=dt.date.today().isoformat(), help="End date (YYYY-MM-DD)")
    parser.add_argument(
        "--currencies",
        type=str,
        nargs="+",
        default=["USD", "EUR", "CNY"],
        help="Currency codes to fetch from PTAX",
    )
    parser.add_argument("--skip-selic", action="store_true", help="Skip Selic series download")
    parser.add_argument("--output-dir", type=Path, default=LANDING_ROOT, help="Landing directory")
    return parser.parse_args(args)


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)
    start = dt.datetime.strptime(options.start, "%Y-%m-%d").date()
    end = dt.datetime.strptime(options.end, "%Y-%m-%d").date()
    run_stamp = today_str()

    for currency in options.currencies:
        try:
            data = fetch_ptax(currency.upper(), start, end)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to fetch PTAX for %s: %s", currency, exc)
            continue
        out_path = (
            options.output_dir
            / "ptax"
            / currency.lower()
            / run_stamp
            / "ptax.json"
        )
        save_json(data, out_path)

    if not options.skip_selic:
        try:
            data = fetch_selic(start, end)
            out_path = options.output_dir / "selic" / run_stamp / "selic.json"
            save_json(data, out_path)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to fetch Selic series: %s", exc)

    logger.info("BACEN download finished.")


if __name__ == "__main__":
    main()

