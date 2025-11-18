from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class ClimateDailyReading(BaseModel):
    date: date
    temp_min_c: float = Field(alias="temp_min")
    temp_max_c: float = Field(alias="temp_max")
    precipitation_mm: float = Field(alias="precipitation")
    wind_speed_kmh: float = Field(alias="wind_speed", default=0.0)
    humidity_pct: Optional[float] = Field(alias="humidity", default=None)

    @validator("precipitation_mm", "temp_min_c", "temp_max_c", "wind_speed_kmh")
    def non_negative(cls, value: float) -> float:  # noqa: D401
        if value < 0:
            raise ValueError("Values must be non-negative")
        return value


class ClimateForecast(BaseModel):
    region: str
    updated_at: datetime
    days: List[ClimateDailyReading]


class EconomicIndicator(BaseModel):
    name: str
    value: float
    observed_at: date
    unit: str


class EconomicSnapshot(BaseModel):
    series: List[EconomicIndicator]
    source: str
    week_end: date


class RegulatoryChange(BaseModel):
    regulation_id: str
    title: str
    effective_date: date
    summary: str
    jurisdiction: str


class RegulatoryBulletin(BaseModel):
    issued_at: datetime
    items: List[RegulatoryChange]
    source: str

