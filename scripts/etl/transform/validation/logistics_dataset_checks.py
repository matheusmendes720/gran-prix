"""
Validation helpers for logistics external datasets.

Usage:
    python -m scripts.etl.transform.validation.logistics_dataset_checks
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ...external import configure_logging

logger = configure_logging("logistics_validation")

SILVER_ROOT = Path("data/silver/external_factors")

EXPECTED_LOGISTICS_DATASETS = {
    "anp_fuel_daily.parquet": {"min_rows": 500, "min_date": "2021-01-01"},
    "freight_worldbank.parquet": {"min_rows": 1, "min_date": "2021-01-01"},
    "baltic_dry.parquet": {"min_rows": 50, "min_date": "2021-01-01"},
    "../freight/xeneta_xsi_c.parquet": {"min_rows": 1, "min_date": "2009-01-01"},
    "../freight/drewry_wci_alternatives.parquet": {"min_rows": 1, "min_date": "2009-01-01"},
    "../freight/antt_logistics_kpis.parquet": {"min_rows": 1, "min_date": "2021-01-01"},
}

LOGISTICS_ROOT = SILVER_ROOT / "logistics"
FREIGHT_ROOT = SILVER_ROOT.parent / "freight"

LOGISTICS_DATASETS = {}
for name in EXPECTED_LOGISTICS_DATASETS:
    if name.startswith("../freight/"):
        relative = name.split("../freight/")[-1]
        LOGISTICS_DATASETS[name] = (FREIGHT_ROOT / relative).resolve()
    else:
        LOGISTICS_DATASETS[name] = (LOGISTICS_ROOT / name).resolve()


def validate_dataset(name: str, path: Path) -> bool:
    if not path.exists():
        logger.warning("Dataset %s missing at %s", name, path)
        return False

    df = pd.read_parquet(path)
    if df.empty:
        logger.warning("Dataset %s is empty.", name)
        return False

    if "date" not in df.columns:
        logger.warning("Dataset %s missing 'date' column.", name)
        return False

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isna().all():
        logger.warning("Dataset %s has invalid date values.", name)
        return False

    missing_value_ratio = df.isna().mean().max()
    if missing_value_ratio > 0.5:
        logger.warning(
            "Dataset %s has high missing ratio (%.2f).",
            name,
            missing_value_ratio,
        )
        return False

    logger.info(
        "Dataset %s validated (%s rows, %s -> %s).",
        name,
        len(df),
        df['date'].min().date(),
        df['date'].max().date(),
    )
    return True


def validate_all() -> bool:
    status = []
    for name, path in LOGISTICS_DATASETS.items():
        valid = validate_dataset(name, path)
        status.append(valid)
    overall = all(status)
    if overall:
        logger.info("All logistics datasets validated successfully.")
    else:
        logger.warning("Some logistics datasets failed validation.")
    return overall


if __name__ == "__main__":
    ok = validate_all()
    if not ok:
        raise SystemExit(1)

