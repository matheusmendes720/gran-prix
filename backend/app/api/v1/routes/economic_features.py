"""
Economic features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    EconomicFeatures,
    BACENIndicators,
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/economic", tags=["features", "economic"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_economic_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get economic indicators"""
    try:
        where_clauses = ["feature_category = 'ECONOMIC'"]
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
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset
        
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
            
            features_by_material[mat_id][data_ref][feature_name] = feature_value
        
        # Flatten to list
        data = []
        for mat_id, dates in features_by_material.items():
            for date_ref, features in dates.items():
                feature_obj = {
                    "material_id": mat_id,
                    "data_referencia": date_ref,
                    "inflation_rate": float(features.get("inflation_rate", 0.0)),
                    "exchange_rate_brl_usd": float(features.get("exchange_rate_brl_usd", 0.0)),
                    "gdp_growth_rate": float(features.get("gdp_growth_rate", 0.0)),
                    "selic_rate": float(features.get("selic_rate", 0.0)),
                    "high_inflation": bool(features.get("high_inflation", False)),
                    "currency_devaluation": bool(features.get("currency_devaluation", False)),
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=len(data),
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching economic features: {str(e)}")


@router.get("/bacen", response_model=List[BACENIndicators])
async def get_bacen_indicators(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get BACEN indicators (inflation, exchange, GDP, SELIC)"""
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
                taxa_inflacao,
                taxa_cambio_brl_usd,
                pib_crescimento,
                taxa_selic,
                is_high_inflation,
                is_currency_devaluation
            FROM IndicadoresEconomicos
            WHERE {where_clause}
            ORDER BY data_referencia
        """
        
        results = db_service.execute_query(query, params)
        return [BACENIndicators(**dict(row)) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching BACEN indicators: {str(e)}")


@router.get("/trends", response_model=FeatureCategoryResponse)
async def get_economic_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get economic trends over time"""
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
                AVG(taxa_inflacao) as avg_inflation,
                AVG(taxa_cambio_brl_usd) as avg_exchange_rate,
                AVG(pib_crescimento) as avg_gdp_growth,
                AVG(taxa_selic) as avg_selic
            FROM IndicadoresEconomicos
            WHERE {where_clause}
            GROUP BY data_referencia
            ORDER BY data_referencia
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia")),
                "avg_inflation": float(row.get("avg_inflation", 0.0)),
                "avg_exchange_rate": float(row.get("avg_exchange_rate", 0.0)),
                "avg_gdp_growth": float(row.get("avg_gdp_growth", 0.0)),
                "avg_selic": float(row.get("avg_selic", 0.0)),
            }
            for row in results
        ]
        
        metadata = FeatureMetadata(
            total_count=len(data),
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching economic trends: {str(e)}")


@router.get("/impacts", response_model=FeatureCategoryResponse)
async def get_economic_impacts(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get calculated economic impacts"""
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
                COUNT(CASE WHEN is_high_inflation = 1 THEN 1 END) as high_inflation_days,
                COUNT(CASE WHEN is_currency_devaluation = 1 THEN 1 END) as currency_devaluation_days,
                AVG(taxa_inflacao) as avg_inflation,
                AVG(taxa_cambio_brl_usd) as avg_exchange_rate
            FROM IndicadoresEconomicos
            WHERE {where_clause}
            GROUP BY data_referencia
            ORDER BY data_referencia
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia")),
                "high_inflation_days": int(row.get("high_inflation_days", 0)),
                "currency_devaluation_days": int(row.get("currency_devaluation_days", 0)),
                "avg_inflation": float(row.get("avg_inflation", 0.0)),
                "avg_exchange_rate": float(row.get("avg_exchange_rate", 0.0)),
            }
            for row in results
        ]
        
        metadata = FeatureMetadata(
            total_count=len(data),
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching economic impacts: {str(e)}")

