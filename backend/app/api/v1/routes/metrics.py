"""
Metrics endpoints
"""
from fastapi import APIRouter
from app.api.v1.schemas.metrics import MetricsResponse

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/", response_model=MetricsResponse)
async def get_metrics():
    """Get system-wide metrics"""
    # TODO: Implement actual metrics retrieval
    # from app.core.analytics.service import AnalyticsService
    
    return MetricsResponse(
        total_items=100,
        data_points=10000,
        trained_models=5,
        system_health="healthy",
    )

