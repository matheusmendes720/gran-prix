"""
Employment features API endpoints
Extended Brazilian APIs - Employment & Labor Statistics
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/employment", tags=["features", "employment"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_employment_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get employment-related features (4 features)"""
    try:
        where_clauses = ["feature_category = 'EMPLOYMENT'"]
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
                    "employment_rate": float(features.get("employment_rate", 0.0)),
                    "net_employment_change": int(features.get("net_employment_change", 0)),
                    "labor_availability": float(features.get("labor_availability", 0.0)),
                    "hiring_activity": float(features.get("hiring_activity", 0.0)),
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=total_count,
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employment features: {str(e)}")


@router.get("/caged", response_model=FeatureCategoryResponse)
async def get_caged_data(
    regiao: Optional[str] = Query(None, description="Filter by region"),
    setor: Optional[str] = Query(None, description="Filter by sector"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get CAGED employment data"""
    try:
        where_clauses = []
        params = {}
        
        if regiao:
            where_clauses.append("regiao = :regiao")
            params["regiao"] = regiao
        
        if setor:
            where_clauses.append("setor = :setor")
            params["setor"] = setor
        
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
                setor,
                taxa_emprego,
                admissoes,
                demissoes,
                saldo_emprego,
                disponibilidade_mao_obra
            FROM DadosEmprego
            WHERE {where_clause}
            ORDER BY data_referencia DESC, regiao, setor
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "regiao": row.get("regiao", ""),
                "setor": row.get("setor", ""),
                "taxa_emprego": float(row.get("taxa_emprego", 0.0)),
                "admissoes": int(row.get("admissoes", 0)),
                "demissoes": int(row.get("demissoes", 0)),
                "saldo_emprego": int(row.get("saldo_emprego", 0)),
                "disponibilidade_mao_obra": float(row.get("disponibilidade_mao_obra", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching CAGED data: {str(e)}")


@router.get("/ibge-extended", response_model=FeatureCategoryResponse)
async def get_ibge_extended(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get extended IBGE statistics (PIM, PMS, PMC, PNAD)"""
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
                pim_producao_industrial,
                pms_receita_servicos,
                pmc_vendas_varejo,
                pnad_taxa_emprego,
                taxa_desemprego,
                pib_regional_bahia
            FROM DadosIbgeExtended
            WHERE {where_clause}
            ORDER BY data_referencia DESC
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "pim_producao_industrial": float(row.get("pim_producao_industrial", 0.0)),
                "pms_receita_servicos": float(row.get("pms_receita_servicos", 0.0)),
                "pmc_vendas_varejo": float(row.get("pmc_vendas_varejo", 0.0)),
                "pnad_taxa_emprego": float(row.get("pnad_taxa_emprego", 0.0)),
                "taxa_desemprego": float(row.get("taxa_desemprego", 0.0)),
                "pib_regional_bahia": float(row.get("pib_regional_bahia", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching IBGE extended data: {str(e)}")








