"""
Items endpoints
"""
from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=List[str])
async def list_items():
    """List all available items"""
    # TODO: Implement actual item list retrieval
    # from app.core.forecasting.service import ForecastingService
    
    return [
        "CONN-001",
        "CABO-001",
        "EQUIP-001",
    ]

