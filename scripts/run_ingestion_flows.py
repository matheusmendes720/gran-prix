"""CLI helpers to execute ingestion flows locally."""

import argparse
from datetime import date, datetime

from demand_forecasting.flows import (
    climate_ingestion_flow,
    economic_ingestion_flow,
    regulatory_ingestion_flow,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Nova Corrente ingestion flows")
    parser.add_argument(
        "--climate",
        action="store_true",
        help="Run the daily climate ingestion flow",
    )
    parser.add_argument(
        "--economic",
        action="store_true",
        help="Run the weekly economic ingestion flow",
    )
    parser.add_argument(
        "--regulatory",
        action="store_true",
        help="Run the monthly regulatory ingestion flow",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Explicit ISO date (YYYY-MM-DD) for the run",
    )
    return parser.parse_args()


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def main() -> None:
    args = parse_args()
    selected = [args.climate, args.economic, args.regulatory]
    if not any(selected):
        args.climate = args.economic = args.regulatory = True

    run_date = _parse_date(args.date)

    if args.climate:
        climate_ingestion_flow(run_date=run_date)
    if args.economic:
        economic_ingestion_flow(week_end=run_date)
    if args.regulatory:
        regulatory_ingestion_flow(period=run_date)


if __name__ == "__main__":  # pragma: no cover - convenience script
    main()

