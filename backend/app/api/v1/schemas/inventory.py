"""
Inventory schemas
"""
from pydantic import BaseModel
from typing import Literal


class InventoryResponse(BaseModel):
    """Inventory response"""
    item_id: str
    current_stock: int
    reorder_point: int
    safety_stock: int
    days_to_rupture: int
    alert_level: Literal["normal", "medium", "high", "critical"]


class ReorderPointCalculation(BaseModel):
    """Reorder point calculation result"""
    average_demand: float
    lead_time_demand: float
    safety_stock: float
    reorder_point: float
    service_level: float

