"""
Regional features API endpoints
Extended Brazilian APIs - Regional Economic & Market Data
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/regional", tags=["features", "regional"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_regional_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    regiao: Optional[str] = Query(None, description="Filter by region"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get regional-related features (6 features)"""
    try:
        where_clauses = ["feature_category = 'REGIONAL'"]
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
                    "regional_gdp": float(features.get("regional_gdp", 0.0)),
                    "regional_growth_rate": float(features.get("regional_growth_rate", 0.0)),
                    "regional_employment": float(features.get("regional_employment", 0.0)),
                    "regional_industrial_prod": float(features.get("regional_industrial_prod", 0.0)),
                    "regional_construction_idx": float(features.get("regional_construction_idx", 0.0)),
                    "regional_development_idx": float(features.get("regional_development_idx", 0.0)),
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=total_count,
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching regional features: {str(e)}")


@router.get("/ipea", response_model=FeatureCategoryResponse)
async def get_regional_ipea(
    regiao: Optional[str] = Query(None, description="Filter by region"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get regional economic data from IPEA"""
    try:
        where_clauses = []
        params = {}
        
        if regiao:
            where_clauses.append("regiao = :regiao")
            params["regiao"] = regiao
        
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
                regiao,
                pib_regional,
                emprego_setor,
                producao_industrial,
                indice_construcao,
                indice_desenvolvimento
            FROM DadosIpea
            WHERE {where_clause}
            ORDER BY data_referencia DESC, regiao
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "regiao": row.get("regiao", ""),
                "pib_regional": float(row.get("pib_regional", 0.0)),
                "emprego_setor": int(row.get("emprego_setor", 0)),
                "producao_industrial": float(row.get("producao_industrial", 0.0)),
                "indice_construcao": float(row.get("indice_construcao", 0.0)),
                "indice_desenvolvimento": float(row.get("indice_desenvolvimento", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching regional IPEA data: {str(e)}")






