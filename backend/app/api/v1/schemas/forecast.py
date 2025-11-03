"""
Forecast schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ForecastMetadata(BaseModel):
    """Forecast metadata"""
    model_type: str
    training_date: str
    data_points: int
    version: Optional[str] = None


class ForecastResponse(BaseModel):
    """Forecast response"""
    item_id: str
    forecast: List[float]
    dates: List[str]
    confidence_intervals: Optional[dict] = None
    metadata: Optional[ForecastMetadata] = None


class ForecastRequest(BaseModel):
    """Forecast request"""
    item_id: str = Field(..., description="Item identifier")
    forecast_days: int = Field(default=30, ge=1, le=365, description="Number of days to forecast")
    model_type: Optional[str] = Field(default=None, description="Model type to use")


class ForecastMetrics(BaseModel):
    """Forecast accuracy metrics"""
    mape: float = Field(..., description="Mean Absolute Percentage Error")
    rmse: float = Field(..., description="Root Mean Squared Error")
    mae: float = Field(..., description="Mean Absolute Error")
    mase: Optional[float] = Field(None, description="Mean Absolute Scaled Error")

