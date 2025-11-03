"""
Metrics schemas
"""
from pydantic import BaseModel
from typing import Literal


class MetricsResponse(BaseModel):
    """System metrics response"""
    total_items: int
    data_points: int
    trained_models: int
    system_health: Literal["healthy", "degraded", "down"]

