"""Utility helpers to load Nova Corrente storytelling outputs for dashboards.

These functions read the artifacts created by
`scripts.storytelling.build_storytelling_assets` and expose convenient
dataframes/dicts ready for notebooks, Streamlit apps, or API layers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Optional

import pandas as pd


DEFAULT_ROOT = Path("../../data/outputs/nova_corrente/storytelling").resolve()


def _resolve_path(path: Optional[Path], filename: str) -> Path:
    base = path if path is not None else DEFAULT_ROOT
    file_path = Path(base) / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Storytelling artifact not found: {file_path}")
    return file_path


def load_timeseries(root: Optional[Path] = None) -> pd.DataFrame:
    """Return timeseries dataframe with actuals, forecasts and metadata."""
    path = _resolve_path(root, "storytelling_timeseries.parquet")
    df = pd.read_parquet(path)
    df["ds"] = pd.to_datetime(df["ds"])
    return df


def load_prescriptions(root: Optional[Path] = None) -> pd.DataFrame:
    """Return prescriptive recommendations dataframe with metadata."""
    path = _resolve_path(root, "storytelling_prescriptions.parquet")
    df = pd.read_parquet(path)
    return df


def load_summary(root: Optional[Path] = None) -> Dict[str, object]:
    """Return summary KPI dictionary."""
    path = _resolve_path(root, "storytelling_summary.json")
    return pd.read_json(path, typ="series").to_dict()


def get_kpi_snapshot(root: Optional[Path] = None) -> Dict[str, object]:
    """Convenience wrapper for quick KPI cards in dashboards."""
    summary = load_summary(root)
    return {
        "series_total": summary.get("series_total", 0),
        "series_with_forecast": summary.get("series_with_forecast", 0),
        "critical_series": summary.get("critical_series", 0),
        "generated_at": summary.get("timestamp"),
    }


def get_alerts_by_status(
    root: Optional[Path] = None, statuses: Optional[Iterable[str]] = None
) -> pd.DataFrame:
    """Filter prescriptions by stock status."""
    df = load_prescriptions(root)
    if statuses is not None:
        df = df[df["stock_status"].isin(list(statuses))]
    return df.sort_values(["stock_status", "series_key"])


def get_family_timeseries(
    familia: str, root: Optional[Path] = None
) -> pd.DataFrame:
    """Return timeseries filtered by família for charting."""
    df = load_timeseries(root)
    return (
        df[df["familia"] == familia]
        .sort_values(["series_key", "ds"])
        .reset_index(drop=True)
    )


def list_familias(root: Optional[Path] = None) -> pd.Series:
    """List available famílias present in storytelling timeseries."""
    df = load_timeseries(root)
    return df["familia"].dropna().unique()

