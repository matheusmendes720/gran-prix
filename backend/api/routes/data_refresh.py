"""
Data Refresh Endpoint
Manually triggers reload of precomputed ML results from storage.

This endpoint does NOT trigger ML processing - it only reloads
precomputed results that were generated in a separate ML environment.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os
from pathlib import Path

router = APIRouter(prefix="/api/v1/data", tags=["data"])


class DataRefreshRequest(BaseModel):
    """Data refresh request model"""
    source: str = "ml_results"  # Source of data to refresh
    force: bool = False  # Force refresh even if data is recent


class DataRefreshResponse(BaseModel):
    """Data refresh response model"""
    status: str
    job_id: str
    estimated_completion: Optional[str] = None
    message: str


def verify_api_key(x_api_key: Optional[str] = Header(None)) -> bool:
    """Verify API key for admin access"""
    expected_key = os.getenv("ADMIN_API_KEY", "change-this-in-production")
    if not x_api_key or x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid API key")
    return True


@router.post("/refresh", response_model=DataRefreshResponse)
async def refresh_data(
    request: DataRefreshRequest,
    authorized: bool = Depends(verify_api_key)
):
    """
    Trigger data refresh to reload precomputed ML results.
    
    This endpoint:
    - Requires admin API key authentication
    - Triggers reload of precomputed ML results from storage
    - Does NOT trigger ML processing (ML runs in separate environment)
    - Returns job ID for tracking refresh status
    
    **Note:** This is a manual trigger only. ML processing runs separately
    and outputs results to shared storage. This endpoint only reloads those results.
    """
    try:
        # Get ML results path from environment
        ml_results_path = Path(os.getenv("ML_RESULTS_PATH", "./data/ml_results"))
        
        if not ml_results_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"ML results path not found: {ml_results_path}"
            )
        
        # Generate job ID
        job_id = f"refresh_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # TODO: Implement actual data refresh logic
        # This would:
        # 1. Read new Parquet files from ml_results_path
        # 2. Validate schema (model_version, generated_at, source, dataset_id)
        # 3. Load into gold layer (Parquet or DuckDB)
        # 4. Update cache (Redis)
        # 5. Return job ID for tracking
        
        # For now, return success
        return DataRefreshResponse(
            status="triggered",
            job_id=job_id,
            estimated_completion=datetime.now().isoformat(),
            message=f"Data refresh triggered for source: {request.source}. Results will be loaded from: {ml_results_path}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error triggering data refresh: {str(e)}"
        )

