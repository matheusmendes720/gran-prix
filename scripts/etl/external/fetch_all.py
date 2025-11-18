"""
Convenience entrypoint that triggers all external data downloads required for
Nova Corrente forecasting pipelines. Wraps individual source collectors in a
single CLI command so it can be scheduled via Airflow or Windows Task Scheduler.
"""

from __future__ import annotations

import argparse
import datetime as dt
from typing import Iterable, Optional

from . import configure_logging
from . import (
    anp_downloader,
    bacen_downloader,
    freight_downloader,
    ibge_downloader,
    openweather_ingest,
    worldbank_downloader,
)
from scripts.automation.freight_blockers.integration import run_freight_blockers_etl


logger = configure_logging("fetch_all")


def parse_args(args: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download all external data sources.")
    parser.add_argument("--skip-openweather", action="store_true", help="Skip OpenWeather ingestion")
    parser.add_argument("--skip-bacen", action="store_true", help="Skip BACEN PTAX/Selic download")
    parser.add_argument("--skip-ibge", action="store_true", help="Skip IBGE SIDRA download")
    parser.add_argument("--skip-worldbank", action="store_true", help="Skip World Bank indicators")
    parser.add_argument("--skip-anp", action="store_true", help="Skip ANP fuel price download")
    parser.add_argument("--skip-freight", action="store_true", help="Skip freight benchmark download")
    parser.add_argument(
        "--skip-freight-blockers",
        action="store_true",
        help="Skip automated Xeneta/SCFI/ANTT freight blockers",
    )
    parser.add_argument("--openweather-history-days", type=int, default=1460, help="Days for OpenWeather history")
    parser.add_argument("--openweather-daily", action="store_true", help="Force daily forecast download")
    parser.add_argument(
        "--start-date",
        type=str,
        default="2015-01-01",
        help="Start date (YYYY-MM-DD) for BACEN series",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=dt.date.today().isoformat(),
        help="End date (YYYY-MM-DD) for BACEN series",
    )
    parser.add_argument("--timestamp", type=str, default=None, help="Override timestamp for IBGE/World Bank landing")
    return parser.parse_args(args)


def main(cli_args: Optional[Iterable[str]] = None) -> None:
    options = parse_args(cli_args)

    if not options.skip_openweather:
        logger.info("Running OpenWeather ingestion...")
        openweather_ingest.main(
            [
                "--history-days",
                str(options.openweather_history_days),
                *(["--daily-forecast"] if options.openweather_daily else []),
            ]
        )

    if not options.skip_bacen:
        logger.info("Running BACEN downloader...")
        bacen_downloader.main(
            [
                "--start",
                options.start_date,
                "--end",
                options.end_date,
            ]
        )

    if not options.skip_ibge:
        logger.info("Running IBGE downloader...")
        ibge_args = [
            "--start",
            options.start_date,
            "--end",
            options.end_date,
        ]
        if options.timestamp:
            ibge_args.extend(["--timestamp", options.timestamp])
        ibge_downloader.main(ibge_args)

    if not options.skip_worldbank:
        logger.info("Running World Bank downloader...")
        wb_args = []
        if options.timestamp:
            wb_args.extend(["--timestamp", options.timestamp])
        worldbank_downloader.main(wb_args)

    if not options.skip_anp:
        logger.info("Running ANP downloader...")
        anp_downloader.main()

    if not options.skip_freight:
        logger.info("Running freight downloader...")
        freight_args = []
        if options.timestamp:
            freight_args.extend(["--timestamp", options.timestamp])
        freight_downloader.main(freight_args)

    if not options.skip_freight_blockers:
        logger.info("Running freight blockers automation...")
        try:
            run_freight_blockers_etl()
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Freight blockers automation failed: %s", exc)

    logger.info("All downloads completed.")


if __name__ == "__main__":
    main()

