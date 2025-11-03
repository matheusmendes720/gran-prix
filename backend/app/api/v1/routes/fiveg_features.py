"""
5G features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    FiveGFeatures,
    FiveGExpansion,
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/5g", tags=["features", "5g"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_5g_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get 5G expansion features"""
    try:
        where_clauses = ["feature_category = '5G'"]
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
            
            # Map feature names (handle '5g_' prefix)
            feature_key = feature_name.replace("5g_", "").replace("_", "_")
            features_by_material[mat_id][data_ref][feature_key] = feature_value
        
        # Flatten to list
        data = []
        for mat_id, dates in features_by_material.items():
            for date_ref, features in dates.items():
                feature_obj = {
                    "material_id": mat_id,
                    "data_referencia": date_ref,
                    "coverage_5g_percentual": float(features.get("coverage_pct", features.get("coverage_5g_percentual", 0.0))),
                    "investment_5g_brl_billions": float(features.get("investment_brl_billions", features.get("investment_5g_brl_billions", 0.0))),
                    "is_5g_milestone": bool(features.get("is_5g_milestone", False)),
                    "is_5g_active": bool(features.get("is_5g_active", False)),
                    "expansion_5g_rate": float(features.get("expansion_rate", features.get("expansion_5g_rate", 0.0))),
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=len(data),
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching 5G features: {str(e)}")


@router.get("/expansion", response_model=List[FiveGExpansion])
async def get_5g_expansion(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get 5G expansion metrics (coverage, investment)"""
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
                cobertura_5g_percentual,
                investimento_5g_brl_billions,
                torres_5g_ativas,
                municipios_5g,
                is_5g_milestone,
                taxa_expansao_5g
            FROM Expansao5G
            WHERE {where_clause}
            ORDER BY data_referencia
        """
        
        results = db_service.execute_query(query, params)
        return [FiveGExpansion(**dict(row)) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching 5G expansion: {str(e)}")


@router.get("/milestones", response_model=List[FiveGExpansion])
async def get_5g_milestones():
    """Get 5G expansion milestones"""
    try:
        query = """
            SELECT 
                data_referencia,
                cobertura_5g_percentual,
                investimento_5g_brl_billions,
                torres_5g_ativas,
                municipios_5g,
                is_5g_milestone,
                taxa_expansao_5g
            FROM Expansao5G
            WHERE is_5g_milestone = 1
            ORDER BY data_referencia
        """
        
        results = db_service.execute_query(query)
        return [FiveGExpansion(**dict(row)) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching 5G milestones: {str(e)}")


@router.get("/demand-impact", response_model=FeatureCategoryResponse)
async def get_5g_demand_impact(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get 5G impact on material demand"""
    try:
        where_clauses = []
        params = {}
        
        if start_date:
            where_clauses.append("e.data_referencia >= :start_date")
            params["start_date"] = start_date
        
        if end_date:
            where_clauses.append("e.data_referencia <= :end_date")
            params["end_date"] = end_date
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                e.data_referencia,
                e.cobertura_5g_percentual,
                COUNT(DISTINCT m.material_id) as materials_count,
                SUM(me.quantidade_movimentada) as total_demand,
                CASE 
                    WHEN e.cobertura_5g_percentual > 40 THEN 'HIGH_DEMAND'
                    WHEN e.cobertura_5g_percentual > 20 THEN 'MEDIUM_DEMAND'
                    ELSE 'LOW_DEMAND'
                END as demand_category
            FROM Expansao5G e
            LEFT JOIN MovimentacaoEstoque me ON DATE(me.data_movimentacao) = e.data_referencia
            LEFT JOIN Material m ON me.material_id = m.material_id
            WHERE {where_clause}
            GROUP BY e.data_referencia, e.cobertura_5g_percentual
            ORDER BY e.data_referencia
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia")),
                "cobertura_5g_percentual": float(row.get("cobertura_5g_percentual", 0.0)),
                "materials_count": int(row.get("materials_count", 0)),
                "total_demand": float(row.get("total_demand", 0.0)),
                "demand_category": row.get("demand_category", "LOW_DEMAND"),
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
        raise HTTPException(status_code=500, detail=f"Error fetching 5G demand impact: {str(e)}")

