"""FastAPI blueprint exposing storytelling datasets for the frontend."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from data_sources.storytelling_loader import (
    get_alerts_by_status,
    get_family_timeseries,
    get_kpi_snapshot,
    list_familias,
)


router = APIRouter(prefix="/storytelling", tags=["storytelling"])


class KPIResponse(BaseModel):
    series_total: int
    series_with_forecast: int
    critical_series: int
    generated_at: str | None


class AlertResponse(BaseModel):
    series_key: str
    familia: str | None
    region: str | None
    reorder_point: float | None
    safety_stock: float | None
    current_stock: float | None
    days_to_rupture: float | None
    stock_status: str | None


class TimeseriesResponse(BaseModel):
    series_key: str
    ds: str
    forecast_qty: float | None
    actual_qty: float | None
    lower: float | None = None
    upper: float | None = None
    familia: str | None = None
    category: str | None = None
    region: str | None = None


def get_default_familia() -> str:
    familias = list_familias()
    if len(familias) == 0:
        raise ValueError("Nenhuma família disponível nas séries de storytelling.")
    return str(familias[0])


@router.get("/kpis", response_model=KPIResponse)
def storytelling_kpis():
    return get_kpi_snapshot()


@router.get("/alerts", response_model=list[AlertResponse])
def storytelling_alerts(status: list[str] = Query(default=None)):
    df = get_alerts_by_status(statuses=status)
    return df.to_dict(orient="records")


@router.get("/timeseries", response_model=list[TimeseriesResponse])
def storytelling_timeseries(
    familia: str = Depends(get_default_familia),
    series_key: str | None = None,
):
    df = get_family_timeseries(familia)
    if series_key:
        df = df[df["series_key"] == series_key]
    return df.to_dict(orient="records")

