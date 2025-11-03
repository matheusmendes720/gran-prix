"""
Temporal features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    TemporalFeatures,
    CalendarFeatures,
    FeatureCategoryResponse,
    FeatureMetadata,
    DateRange
)

router = APIRouter(prefix="/features/temporal", tags=["features", "temporal"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_temporal_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Get temporal features for materials
    
    - **material_id**: Optional material ID filter
    - **start_date**: Optional start date filter
    - **end_date**: Optional end date filter
    - **limit**: Maximum number of results (1-1000)
    - **offset**: Offset for pagination
    """
    try:
        # Build query
        where_clauses = ["feature_category = 'TEMPORAL'"]
        params = {}
        
        if material_id:
            where_clauses.append("material_id = :material_id")
            params["material_id"] = material_id
        
        if start_date:
            where_clauses.append("DATE(data_coleta) >= :start_date")
            params["start_date"] = start_date
        
        if end_date:
            where_clauses.append("DATE(data_coleta) <= :end_date")
            params["end_date"] = end_date
        
        where_clause = " AND ".join(where_clauses)
        
        # Get total count
        count_query = f"""
            SELECT COUNT(DISTINCT material_id) as total
            FROM MaterialFeatures
            WHERE {where_clause}
        """
        count_result = db_service.execute_query(count_query, params, fetch_one=True)
        total_count = count_result.get("total", 0) if count_result else 0
        
        # Get features
        query = f"""
            SELECT 
                material_id,
                feature_name,
                feature_value,
                DATE(data_coleta) as data_referencia
            FROM MaterialFeatures
            WHERE {where_clause}
            ORDER BY material_id, data_coleta DESC
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset
        
        results = db_service.execute_query(query, params)
        
        # Transform to feature objects grouped by material_id and date
        features_by_material = {}
        for row in results:
            mat_id = row.get("material_id")
            feature_name = row.get("feature_name")
            feature_value = row.get("feature_value")
            data_ref = row.get("data_referencia")
            
            if mat_id not in features_by_material:
                features_by_material[mat_id] = {}
            
            if data_ref not in features_by_material[mat_id]:
                features_by_material[mat_id][data_ref] = {"material_id": mat_id, "data_referencia": str(data_ref)}
            
            features_by_material[mat_id][data_ref][feature_name] = feature_value
        
        # Flatten to list
        data = []
        for mat_id, dates in features_by_material.items():
            for date_ref, features in dates.items():
                # Ensure all temporal fields have defaults
                feature_obj = {
                    "material_id": mat_id,
                    "year": int(features.get("year", 0)),
                    "month": int(features.get("month", 0)),
                    "day": int(features.get("day", 0)),
                    "weekday": int(features.get("weekday", 0)),
                    "quarter": int(features.get("quarter", 0)),
                    "day_of_year": int(features.get("day_of_year", 0)),
                    "month_sin": float(features.get("month_sin", 0.0)),
                    "month_cos": float(features.get("month_cos", 0.0)),
                    "day_of_year_sin": float(features.get("day_of_year_sin", 0.0)),
                    "day_of_year_cos": float(features.get("day_of_year_cos", 0.0)),
                    "is_weekend": bool(features.get("is_weekend", False)),
                    "is_holiday": bool(features.get("is_holiday", False)),
                    "is_carnival": bool(features.get("is_carnival", False)),
                    "is_verao": bool(features.get("is_verao", False)),
                    "is_chuva_sazonal": bool(features.get("is_chuva_sazonal", False)),
                    "data_referencia": date_ref,
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=total_count,
            date_range={
                "start": start_date or "",
                "end": end_date or "",
            } if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(
            status="success",
            data=data,
            metadata=metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching temporal features: {str(e)}")


@router.get("/{material_id}", response_model=FeatureCategoryResponse)
async def get_temporal_features_by_material(material_id: int):
    """Get temporal features for a specific material"""
    return await get_temporal_features(material_id=material_id)


@router.get("/calendar", response_model=List[CalendarFeatures])
async def get_brazilian_calendar(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """
    Get Brazilian calendar features (holidays, carnival, etc.)
    
    - **start_date**: Optional start date filter
    - **end_date**: Optional end date filter
    """
    try:
        where_clauses = []
        params = {}
        
        if start_date:
            where_clauses.append("data_referencia >= :start_date")
            params["start_date"] = start_date
        
        if end_date:
            where_clauses.append("data_referencia <= :end_date")
            params["end_date"] = end_date
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                data_referencia,
                is_feriado,
                is_carnaval,
                is_natal,
                is_verao,
                is_chuva_sazonal,
                impact_demanda,
                descricao
            FROM CalendarioBrasil
            WHERE {where_clause}
            ORDER BY data_referencia
        """
        
        results = db_service.execute_query(query, params)
        
        return [
            CalendarFeatures(**dict(row))
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching calendar features: {str(e)}")


@router.get("/cyclical", response_model=FeatureCategoryResponse)
async def get_cyclical_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """
    Get cyclical encoding (sin/cos) features
    
    - **material_id**: Optional material ID filter
    - **start_date**: Optional start date filter
    - **end_date**: Optional end date filter
    """
    try:
        where_clauses = [
            "feature_category = 'TEMPORAL'",
            "feature_name IN ('month_sin', 'month_cos', 'day_of_year_sin', 'day_of_year_cos')"
        ]
        params = {}
        
        if material_id:
            where_clauses.append("material_id = :material_id")
            params["material_id"] = material_id
        
        if start_date:
            where_clauses.append("DATE(data_coleta) >= :start_date")
            params["start_date"] = start_date
        
        if end_date:
            where_clauses.append("DATE(data_coleta) <= :end_date")
            params["end_date"] = end_date
        
        where_clause = " AND ".join(where_clauses)
        
        query = f"""
            SELECT 
                material_id,
                feature_name,
                feature_value,
                DATE(data_coleta) as data_referencia
            FROM MaterialFeatures
            WHERE {where_clause}
            ORDER BY material_id, data_coleta DESC
        """
        
        results = db_service.execute_query(query, params)
        
        # Group by material and date
        features_by_material = {}
        for row in results:
            mat_id = row.get("material_id")
            feature_name = row.get("feature_name")
            feature_value = row.get("feature_value")
            data_ref = row.get("data_referencia")
            
            if mat_id not in features_by_material:
                features_by_material[mat_id] = {}
            
            if data_ref not in features_by_material[mat_id]:
                features_by_material[mat_id][data_ref] = {
                    "material_id": mat_id,
                    "data_referencia": str(data_ref),
                }
            
            features_by_material[mat_id][data_ref][feature_name] = float(feature_value)
        
        # Flatten to list
        data = []
        for mat_id, dates in features_by_material.items():
            for date_ref, features in dates.items():
                feature_obj = {
                    "material_id": mat_id,
                    "month_sin": float(features.get("month_sin", 0.0)),
                    "month_cos": float(features.get("month_cos", 0.0)),
                    "day_of_year_sin": float(features.get("day_of_year_sin", 0.0)),
                    "day_of_year_cos": float(features.get("day_of_year_cos", 0.0)),
                    "data_referencia": date_ref,
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=len(data),
            date_range={
                "start": start_date or "",
                "end": end_date or "",
            } if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(
            status="success",
            data=data,
            metadata=metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cyclical features: {str(e)}")

