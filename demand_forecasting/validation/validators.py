"""Lightweight validation utilities for pipeline datasets."""

from __future__ import annotations

from datetime import date
from typing import Dict

import pandas as pd


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_climate(df: pd.DataFrame, execution_date: date) -> Dict[str, object]:
    _ensure(not df.empty, "Climate dataset is empty")
    _ensure(df["date"].notna().all(), "Climate date column contains nulls")
    _ensure(df["region"].notna().all(), "Climate region column contains nulls")
    _ensure((df["temp_min_c"] >= -30).all() and (df["temp_min_c"] <= 60).all(), "temp_min_c out of bounds")
    _ensure((df["temp_max_c"] >= -20).all() and (df["temp_max_c"] <= 70).all(), "temp_max_c out of bounds")
    _ensure((df["precipitation_mm"] >= 0).all(), "precipitation_mm must be >= 0")
    _ensure((df["wind_speed_kmh"] >= 0).all() and (df["wind_speed_kmh"] <= 200).all(), "wind_speed_kmh out of bounds")
    _ensure((df["humidity_pct"] >= 0).all() and (df["humidity_pct"] <= 100).all(), "humidity_pct out of bounds")
    max_date = pd.to_datetime(df["date"]).max().date()

    return {
        "success": True,
        "row_count": int(len(df)),
        "date_range": [pd.to_datetime(df["date"]).min().date().isoformat(), max_date.isoformat()],
        "regions": df["region"].unique().tolist(),
    }


def validate_economic(df: pd.DataFrame) -> Dict[str, object]:
    _ensure(not df.empty, "Economic dataset is empty")
    _ensure(df["name"].isin(["ptax", "selic"]).all(), "Unexpected economic indicator name")
    _ensure(df["observed_at"].notna().all(), "Economic observed_at contains nulls")
    _ensure(df["value"].between(-1e6, 1e6).all(), "Economic values out of bounds")

    observed = pd.to_datetime(df["observed_at"])

    return {
        "success": True,
        "row_count": int(len(df)),
        "date_range": [observed.min().date().isoformat(), observed.max().date().isoformat()],
    }


def validate_regulatory(df: pd.DataFrame) -> Dict[str, object]:
    if df.empty:
        return {"success": True, "row_count": 0}
    _ensure(df["regulation_id"].notna().all(), "Regulation IDs contain nulls")
    _ensure(df["effective_date"].notna().all(), "Regulation effective_date contains nulls")
    _ensure(df["title"].notna().all(), "Regulation title contains nulls")
    _ensure(df["summary"].notna().all(), "Regulation summary contains nulls")
    _ensure((df["regulation_id"].str.len() >= 3).all(), "Regulation IDs too short")

    return {
        "success": True,
        "row_count": int(len(df)),
        "latest_effective": df["effective_date"].max().isoformat(),
    }


def validate_fact_demand(df: pd.DataFrame) -> Dict[str, object]:
    _ensure(not df.empty, "FactDemand dataset is empty")
    _ensure(df["date"].notna().all(), "FactDemand date contains nulls")
    _ensure(df["item_id"].notna().all(), "FactDemand item_id contains nulls")
    _ensure(df["site_id"].notna().all(), "FactDemand site_id contains nulls")
    _ensure(df["qty_consumed"].ge(0).all(), "qty_consumed must be >= 0")
    _ensure(df.duplicated(subset=["date", "item_id", "site_id"]).sum() == 0, "Duplicate fact rows detected")

    return {
        "success": True,
        "row_count": int(len(df)),
        "date_range": [pd.to_datetime(df["date"]).min().date().isoformat(), pd.to_datetime(df["date"]).max().date().isoformat()],
    }


def validate_fact_backfill(df: pd.DataFrame, actual_start: date) -> Dict[str, object]:
    _ensure(not df.empty, "Backfill dataset is empty")
    _ensure(df["date"].notna().all(), "Backfill date column contains nulls")
    _ensure(df["item_id"].notna().all(), "Backfill item_id contains nulls")
    _ensure(df["site_id"].notna().all(), "Backfill site_id contains nulls")
    value_column = "quantidade" if "quantidade" in df.columns else "qty_consumed"
    _ensure(value_column in df.columns, "Backfill dataset missing demand column")
    _ensure((pd.to_numeric(df[value_column]) >= 0).all(), "Backfill demand values must be >= 0")
    _ensure(df.duplicated(subset=["date", "item_id", "site_id"]).sum() == 0, "Duplicate backfill rows detected")

    dates = pd.to_datetime(df["date"])
    min_date = dates.min().date()
    max_date = dates.max().date()
    _ensure(max_date < actual_start, "Backfill overlaps actual demand timeline")
    _ensure((actual_start - min_date).days >= 365, "Backfill coverage shorter than 12 months")

    return {
        "success": True,
        "row_count": int(len(df)),
        "date_range": [min_date.isoformat(), max_date.isoformat()],
        "items": int(df["item_id"].nunique()),
        "sites": int(df["site_id"].nunique()),
    }

