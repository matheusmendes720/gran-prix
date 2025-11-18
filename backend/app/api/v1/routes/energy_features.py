"""
Energy features API endpoints
Extended Brazilian APIs - Energy & Utilities
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/energy", tags=["features", "energy"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_energy_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get energy-related features (6 features)"""
    try:
        where_clauses = ["feature_category = 'ENERGY'"]
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
                    "energy_consumption_mwh": float(features.get("energy_consumption_mwh", 0.0)),
                    "power_outages_count": int(features.get("power_outages_count", 0)),
                    "grid_reliability": float(features.get("grid_reliability", 0.0)),
                    "energy_price": float(features.get("energy_price", 0.0)),
                    "power_outage_risk": float(features.get("power_outage_risk", 0.0)),
                    "grid_stability_score": float(features.get("grid_stability_score", 0.0)),
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=total_count,
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching energy features: {str(e)}")


@router.get("/aneel", response_model=FeatureCategoryResponse)
async def get_aneel_data(
    regiao: Optional[str] = Query(None, description="Filter by region"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get ANEEL energy data"""
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
                consumo_energia,
                interrupcoes_energia,
                confiabilidade_rede,
                preco_energia
            FROM DadosEnergia
            WHERE {where_clause}
            ORDER BY data_referencia DESC, regiao
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "regiao": row.get("regiao", ""),
                "consumo_energia": float(row.get("consumo_energia", 0.0)),
                "interrupcoes_energia": int(row.get("interrupcoes_energia", 0)),
                "confiabilidade_rede": float(row.get("confiabilidade_rede", 0.0)),
                "preco_energia": float(row.get("preco_energia", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching ANEEL data: {str(e)}")


@router.get("/fuel-prices", response_model=FeatureCategoryResponse)
async def get_fuel_prices(
    regiao: Optional[str] = Query(None, description="Filter by region"),
    tipo_combustivel: Optional[str] = Query(None, description="Filter by fuel type"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get fuel prices from ANP"""
    try:
        where_clauses = []
        params = {}
        
        if regiao:
            where_clauses.append("regiao = :regiao")
            params["regiao"] = regiao
        
        if tipo_combustivel:
            where_clauses.append("tipo_combustivel = :tipo_combustivel")
            params["tipo_combustivel"] = tipo_combustivel
        
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
                tipo_combustivel,
                preco_medio,
                preco_minimo,
                preco_maximo,
                variacao_preco
            FROM DadosCombustiveis
            WHERE {where_clause}
            ORDER BY data_referencia DESC, regiao, tipo_combustivel
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "regiao": row.get("regiao", ""),
                "tipo_combustivel": row.get("tipo_combustivel", ""),
                "preco_medio": float(row.get("preco_medio", 0.0)),
                "preco_minimo": float(row.get("preco_minimo", 0.0)),
                "preco_maximo": float(row.get("preco_maximo", 0.0)),
                "variacao_preco": float(row.get("variacao_preco", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching fuel prices: {str(e)}")









