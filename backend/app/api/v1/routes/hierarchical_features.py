"""
Hierarchical features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    HierarchicalFeatures,
    FamilyAggregation,
    SiteAggregation,
    HierarchicalLevel,
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/hierarchical", tags=["features", "hierarchical"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_hierarchical_features(
    level: HierarchicalLevel = Query(HierarchicalLevel.FAMILY, description="Aggregation level"),
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get hierarchical aggregations"""
    try:
        where_clauses = ["feature_category = 'HIERARCHICAL'"]
        params = {}
        
        if material_id:
            where_clauses.append("material_id = :material_id")
            params["material_id"] = material_id
        
        where_clause = " AND ".join(where_clauses)
        
        query = f"""
            SELECT 
                material_id,
                feature_name,
                feature_value
            FROM MaterialFeatures
            WHERE {where_clause}
            ORDER BY material_id
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset
        
        results = db_service.execute_query(query, params)
        
        # Group by material
        features_by_material = {}
        for row in results:
            mat_id = row.get("material_id")
            feature_name = row.get("feature_name")
            feature_value = row.get("feature_value")
            
            if mat_id not in features_by_material:
                features_by_material[mat_id] = {"material_id": mat_id}
            
            features_by_material[mat_id][feature_name] = feature_value
        
        # Flatten to list
        data = []
        for mat_id, features in features_by_material.items():
            feature_obj = {
                "material_id": mat_id,
                "family_demand_ma_7": float(features.get("family_demand_ma_7", 0.0)),
                "family_demand_ma_30": float(features.get("family_demand_ma_30", 0.0)),
                "family_demand_std_7": float(features.get("family_demand_std_7", 0.0)),
                "family_demand_std_30": float(features.get("family_demand_std_30", 0.0)),
                "family_frequency": float(features.get("family_frequency", 0.0)),
                "site_demand_ma_7": float(features.get("site_demand_ma_7", 0.0)),
                "site_demand_ma_30": float(features.get("site_demand_ma_30", 0.0)),
                "site_frequency": float(features.get("site_frequency", 0.0)),
                "supplier_frequency": float(features.get("supplier_frequency", 0.0)),
                "supplier_lead_time_mean": float(features.get("supplier_lead_time_mean", 0.0)),
                "supplier_lead_time_std": float(features.get("supplier_lead_time_std", 0.0)),
            }
            data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=len(data),
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching hierarchical features: {str(e)}")


@router.get("/family", response_model=List[FamilyAggregation])
async def get_family_aggregations(
    family_id: Optional[int] = Query(None, description="Filter by family ID"),
):
    """Get family-level aggregations"""
    try:
        where_clauses = []
        params = {}
        
        if family_id:
            where_clauses.append("f.familia_id = :family_id")
            params["family_id"] = family_id
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                f.familia_id,
                f.nome_familia as familia_nome,
                COUNT(me.movimentacao_id) as total_movimentacoes,
                AVG(me.quantidade_movimentada) as demanda_media_7d,
                AVG(CASE WHEN me.data_movimentacao >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN me.quantidade_movimentada ELSE NULL END) as demanda_media_30d,
                STDDEV(me.quantidade_movimentada) as demanda_std_7d,
                STDDEV(CASE WHEN me.data_movimentacao >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN me.quantidade_movimentada ELSE NULL END) as demanda_std_30d,
                COUNT(DISTINCT DATE(me.data_movimentacao)) as frequency,
                COUNT(DISTINCT me.material_id) as total_materiais
            FROM Familia f
            LEFT JOIN Material m ON f.familia_id = m.familia_id
            LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id
                AND me.data_movimentacao >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            WHERE {where_clause}
            GROUP BY f.familia_id, f.nome_familia
            ORDER BY total_movimentacoes DESC
        """
        
        results = db_service.execute_query(query, params)
        
        return [
            FamilyAggregation(
                familia_id=int(row.get("familia_id")),
                familia_nome=row.get("familia_nome", ""),
                total_movimentacoes=int(row.get("total_movimentacoes", 0)),
                demanda_media_7d=float(row.get("demanda_media_7d", 0.0)),
                demanda_media_30d=float(row.get("demanda_media_30d", 0.0)),
                demanda_std_7d=float(row.get("demanda_std_7d", 0.0)),
                demanda_std_30d=float(row.get("demanda_std_30d", 0.0)),
                frequency=float(row.get("frequency", 0.0)),
                total_materiais=int(row.get("total_materiais", 0)),
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching family aggregations: {str(e)}")


@router.get("/site", response_model=List[SiteAggregation])
async def get_site_aggregations(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
):
    """Get site/tower-level aggregations"""
    try:
        where_clauses = []
        params = {}
        
        if site_id:
            where_clauses.append("me.site_id = :site_id")
            params["site_id"] = site_id
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                me.site_id,
                COUNT(me.movimentacao_id) as total_movimentacoes,
                AVG(me.quantidade_movimentada) as demanda_media_7d,
                AVG(CASE WHEN me.data_movimentacao >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN me.quantidade_movimentada ELSE NULL END) as demanda_media_30d,
                COUNT(DISTINCT DATE(me.data_movimentacao)) as frequency,
                COUNT(DISTINCT me.material_id) as total_materiais
            FROM MovimentacaoEstoque me
            WHERE {where_clause}
                AND me.site_id IS NOT NULL
                AND me.data_movimentacao >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY me.site_id
            ORDER BY total_movimentacoes DESC
        """
        
        results = db_service.execute_query(query, params)
        
        return [
            SiteAggregation(
                site_id=row.get("site_id", ""),
                total_movimentacoes=int(row.get("total_movimentacoes", 0)),
                demanda_media_7d=float(row.get("demanda_media_7d", 0.0)),
                demanda_media_30d=float(row.get("demanda_media_30d", 0.0)),
                frequency=float(row.get("frequency", 0.0)),
                total_materiais=int(row.get("total_materiais", 0)),
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching site aggregations: {str(e)}")


@router.get("/supplier", response_model=FeatureCategoryResponse)
async def get_supplier_aggregations(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get supplier-level aggregations"""
    try:
        query = """
            SELECT 
                f.fornecedor_id,
                f.nome_fornecedor as fornecedor_nome,
                COUNT(DISTINCT me.movimentacao_id) as supplier_frequency,
                AVG(fm.lead_time_padrao) as supplier_lead_time_mean,
                STDDEV(fm.lead_time_padrao) as supplier_lead_time_std
            FROM Fornecedor f
            LEFT JOIN Fornecedor_Material fm ON f.fornecedor_id = fm.fornecedor_id
            LEFT JOIN MovimentacaoEstoque me ON f.fornecedor_id = me.fornecedor_id
            GROUP BY f.fornecedor_id, f.nome_fornecedor
            HAVING supplier_frequency > 0
            ORDER BY supplier_frequency DESC
            LIMIT :limit OFFSET :offset
        """
        
        results = db_service.execute_query(query, {"limit": limit, "offset": offset})
        
        data = [
            {
                "fornecedor_id": int(row.get("fornecedor_id")),
                "fornecedor_nome": row.get("fornecedor_nome", ""),
                "supplier_frequency": float(row.get("supplier_frequency", 0.0)),
                "supplier_lead_time_mean": float(row.get("supplier_lead_time_mean", 0.0)),
                "supplier_lead_time_std": float(row.get("supplier_lead_time_std", 0.0)),
            }
            for row in results
        ]
        
        metadata = FeatureMetadata(
            total_count=len(data),
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching supplier aggregations: {str(e)}")

