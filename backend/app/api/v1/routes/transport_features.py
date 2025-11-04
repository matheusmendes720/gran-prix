"""
Transport features API endpoints
Extended Brazilian APIs - Transport & Logistics
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/transport", tags=["features", "transport"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_transport_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get transport-related features (10 features)"""
    try:
        where_clauses = ["feature_category = 'TRANSPORT'"]
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
                    "transport_cost_index": float(features.get("transport_cost_index", 0.0)),
                    "logistics_performance": float(features.get("logistics_performance", 0.0)),
                    "highway_congestion": float(features.get("highway_congestion", 0.0)),
                    "port_congestion": float(features.get("port_congestion", 0.0)),
                    "port_wait_time_hours": float(features.get("port_wait_time_hours", 0.0)),
                    "delivery_impact_factor": float(features.get("delivery_impact_factor", 1.0)),
                    "total_congestion": float(features.get("total_congestion", 0.0)),
                    "logistics_efficiency_score": float(features.get("logistics_efficiency_score", 0.0)),
                    "transport_cost_multiplier": float(features.get("transport_cost_multiplier", 1.0)),
                    "delivery_delay_risk": float(features.get("delivery_delay_risk", 0.0)),
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=total_count,
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transport features: {str(e)}")


@router.get("/port-activity", response_model=FeatureCategoryResponse)
async def get_port_activity(
    porto: Optional[str] = Query(None, description="Filter by port name"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get port activity data from ANTAQ"""
    try:
        where_clauses = []
        params = {}
        
        if porto:
            where_clauses.append("porto = :porto")
            params["porto"] = porto
        
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
                porto,
                atividade_porto,
                volume_carga,
                movimentacao_conteineres,
                congestionamento_porto,
                tempo_espera_medio
            FROM DadosPortuarios
            WHERE {where_clause}
            ORDER BY data_referencia DESC, porto
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "porto": row.get("porto", ""),
                "atividade_porto": float(row.get("atividade_porto", 0.0)),
                "volume_carga": float(row.get("volume_carga", 0.0)),
                "movimentacao_conteineres": int(row.get("movimentacao_conteineres", 0)),
                "congestionamento_porto": float(row.get("congestionamento_porto", 0.0)),
                "tempo_espera_medio": int(row.get("tempo_espera_medio", 0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching port activity: {str(e)}")


@router.get("/highway-data", response_model=FeatureCategoryResponse)
async def get_highway_data(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get highway infrastructure data from DNIT"""
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
                manutencao_rodovias,
                fechamento_rodovias,
                projetos_infraestrutura,
                indice_trafego,
                impacto_entrega
            FROM DadosRodoviarios
            WHERE {where_clause}
            ORDER BY data_referencia DESC
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "manutencao_rodovias": int(row.get("manutencao_rodovias", 0)),
                "fechamento_rodovias": int(row.get("fechamento_rodovias", 0)),
                "projetos_infraestrutura": int(row.get("projetos_infraestrutura", 0)),
                "indice_trafego": float(row.get("indice_trafego", 0.0)),
                "impacto_entrega": float(row.get("impacto_entrega", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching highway data: {str(e)}")





