"""
Industrial features API endpoints
Extended Brazilian APIs - Industrial Production & Manufacturing
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/industrial", tags=["features", "industrial"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_industrial_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get industrial-related features (5 features)"""
    try:
        where_clauses = ["feature_category = 'INDUSTRIAL'"]
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
                    "industrial_production_index": float(features.get("industrial_production_index", 0.0)),
                    "electrical_equipment_production": float(features.get("electrical_equipment_production", 0.0)),
                    "component_demand": float(features.get("component_demand", 0.0)),
                    "production_demand_ratio": float(features.get("production_demand_ratio", 0.0)),
                    "industrial_activity_level": float(features.get("industrial_activity_level", 0.0)),
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=total_count,
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching industrial features: {str(e)}")


@router.get("/abinee", response_model=FeatureCategoryResponse)
async def get_abinee_data(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get ABINEE electrical industry data"""
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
                producao_equipamentos_eletricos,
                demanda_componentes,
                importacao_materiais_eletricos,
                exportacao_equipamentos
            FROM DadosAbinee
            WHERE {where_clause}
            ORDER BY data_referencia DESC
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "producao_equipamentos_eletricos": float(row.get("producao_equipamentos_eletricos", 0.0)),
                "demanda_componentes": float(row.get("demanda_componentes", 0.0)),
                "importacao_materiais_eletricos": float(row.get("importacao_materiais_eletricos", 0.0)),
                "exportacao_equipamentos": float(row.get("exportacao_equipamentos", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching ABINEE data: {str(e)}")


@router.get("/pim", response_model=FeatureCategoryResponse)
async def get_pim_index(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get IBGE PIM (Industrial Production Index)"""
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
                pim_producao_industrial
            FROM DadosIbgeExtended
            WHERE {where_clause}
            ORDER BY data_referencia DESC
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "pim_producao_industrial": float(row.get("pim_producao_industrial", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching PIM index: {str(e)}")









