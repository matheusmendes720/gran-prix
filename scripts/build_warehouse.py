"""Build the Gold warehouse snapshot aligning internal data with external dimensions."""

import argparse
from datetime import datetime
from pathlib import Path

from demand_forecasting.warehouse.builder import WORKBOOK_PATH, WarehouseBuilder


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build warehouse gold snapshot")
    parser.add_argument(
        "--execution-ts",
        type=str,
        default=None,
        help="Optional ISO timestamp for the snapshot (default: now UTC)",
    )
    parser.add_argument(
        "--workbook",
        type=str,
        default=None,
        help="Override path to dadosSuprimentos.xlsx",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    execution_ts = datetime.fromisoformat(args.execution_ts) if args.execution_ts else None
    workbook_path = Path(args.workbook) if args.workbook else WORKBOOK_PATH
    builder = WarehouseBuilder(execution_ts=execution_ts, workbook_path=workbook_path)
    path = builder.run()
    print(f"Gold snapshot created at {path}")  # noqa: T201


if __name__ == "__main__":  # pragma: no cover - convenience script
    main()

