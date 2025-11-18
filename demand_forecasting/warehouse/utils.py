from __future__ import annotations

from datetime import datetime
from pathlib import Path

import polars as pl

from demand_forecasting.flows.utils import PROJECT_ROOT, ensure_directory


WAREHOUSE_ROOT = PROJECT_ROOT / "data" / "warehouse"


def gold_snapshot_folder(execution_ts: datetime) -> Path:
    folder = WAREHOUSE_ROOT / "gold" / execution_ts.strftime("%Y%m%dT%H%M%S")
    return ensure_directory(folder)


def concat_parquet(files: list[Path]) -> pl.DataFrame:
    if not files:
        return pl.DataFrame()
    frames = [pl.read_parquet(path) for path in files]
    return pl.concat(frames, how="vertical_relaxed")

