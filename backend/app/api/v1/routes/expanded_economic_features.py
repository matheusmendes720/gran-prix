"""
Expanded Economic Features API endpoints
Extended Brazilian APIs - Extended BACEN, IPEA, COMEX
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/economic-extended", tags=["features", "economic-extended"])


@router.get("/bacen-extended", response_model=FeatureCategoryResponse)
async def get_bacen_extended(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get extended BACEN economic series (IPCA-15, IGP-M, IBC-Br, etc.)"""
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
                ipca_15,
                igp_m,
                ibc_br,
                reservas_estrangeiras_usd,
                operacoes_credito,
                volatilidade_cambio,
                taxa_inflacao,
                taxa_inflacao_anual,
                taxa_cambio_brl_usd,
                taxa_selic
            FROM IndicadoresEconomicosExtended
            WHERE {where_clause}
            ORDER BY data_referencia DESC
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia", "")),
                "ipca_15": float(row.get("ipca_15", 0.0)) if row.get("ipca_15") else None,
                "igp_m": float(row.get("igp_m", 0.0)) if row.get("igp_m") else None,
                "ibc_br": float(row.get("ibc_br", 0.0)) if row.get("ibc_br") else None,
                "reservas_estrangeiras_usd": float(row.get("reservas_estrangeiras_usd", 0.0)) if row.get("reservas_estrangeiras_usd") else None,
                "operacoes_credito": float(row.get("operacoes_credito", 0.0)) if row.get("operacoes_credito") else None,
                "volatilidade_cambio": float(row.get("volatilidade_cambio", 0.0)) if row.get("volatilidade_cambio") else None,
                "taxa_inflacao": float(row.get("taxa_inflacao", 0.0)) if row.get("taxa_inflacao") else None,
                "taxa_inflacao_anual": float(row.get("taxa_inflacao_anual", 0.0)) if row.get("taxa_inflacao_anual") else None,
                "taxa_cambio_brl_usd": float(row.get("taxa_cambio_brl_usd", 0.0)) if row.get("taxa_cambio_brl_usd") else None,
                "taxa_selic": float(row.get("taxa_selic", 0.0)) if row.get("taxa_selic") else None,
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
        raise HTTPException(status_code=500, detail=f"Error fetching extended BACEN data: {str(e)}")


@router.get("/ipea", response_model=FeatureCategoryResponse)
async def get_ipea_data(
    regiao: Optional[str] = Query(None, description="Filter by region"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get IPEA regional economic data"""
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
        raise HTTPException(status_code=500, detail=f"Error fetching IPEA data: {str(e)}")







