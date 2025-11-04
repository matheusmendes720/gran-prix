"""
Business features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    BusinessFeatures,
    Top5Family,
    TierAnalytics,
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/business", tags=["features", "business"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_business_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get Nova Corrente business features"""
    try:
        where_clauses = []
        params = {}
        
        if material_id:
            where_clauses.append("m.material_id = :material_id")
            params["material_id"] = material_id
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        # Get total count
        count_query = f"""
            SELECT COUNT(DISTINCT m.material_id) as total
            FROM Material m
            WHERE {where_clause}
        """
        count_result = db_service.execute_query(count_query, params, fetch_one=True)
        total_count = count_result.get("total", 0) if count_result else 0
        
        # Get business features
        query = f"""
            SELECT 
                m.material_id,
                m.nome_material as material,
                f.nome_familia as familia_nome,
                fn.nome_fornecedor as fornecedor_nome,
                me.site_id,
                m.tier_nivel
            FROM Material m
            LEFT JOIN Familia f ON m.familia_id = f.familia_id
            LEFT JOIN Fornecedor_Material fm ON m.material_id = fm.material_id
            LEFT JOIN Fornecedor fn ON fm.fornecedor_id = fn.fornecedor_id
            LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id
            WHERE {where_clause}
            GROUP BY m.material_id, m.nome_material, f.nome_familia, fn.nome_fornecedor, me.site_id, m.tier_nivel
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset
        
        results = db_service.execute_query(query, params)
        
        data = []
        for row in results:
            feature_obj = {
                "material_id": int(row.get("material_id", 0)),
                "item_id": str(row.get("material_id", "")),
                "material": row.get("material", ""),
                "produto_servico": "",
                "quantidade": 0.0,
                "unidade_medida": "",
                "solicitacao": "",
                "data_requisitada": None,
                "data_solicitado": None,
                "data_compra": None,
                "familia_nome": row.get("familia_nome", ""),
                "fornecedor_nome": row.get("fornecedor_nome", ""),
                "site_id": row.get("site_id", ""),
            }
            data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=total_count,
            date_range=None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching business features: {str(e)}")


@router.get("/top5-families", response_model=List[Top5Family])
async def get_top5_families():
    """Get top 5 families statistics"""
    try:
        query = """
            SELECT 
                f.familia_id,
                f.nome_familia,
                COUNT(me.movimentacao_id) as total_movimentacoes,
                COUNT(DISTINCT m.material_id) as items_unicos,
                COUNT(DISTINCT me.site_id) as sites,
                AVG(CASE WHEN me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada ELSE 0 END) as demanda_media
            FROM Familia f
            JOIN Material m ON f.familia_id = m.familia_id
            LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id
            WHERE f.nome_familia IN (
                'MATERIAL ELETRICO',
                'FERRO E AÇO',
                'EPI',
                'MATERIAL CIVIL',
                'FERRAMENTAS E EQUIPAMENTOS'
            )
            GROUP BY f.familia_id, f.nome_familia
            ORDER BY total_movimentacoes DESC
        """
        
        results = db_service.execute_query(query)
        
        total_mov = sum(row.get("total_movimentacoes", 0) for row in results)
        
        families = []
        for row in results:
            mov_count = row.get("total_movimentacoes", 0)
            percent = (mov_count / total_mov * 100) if total_mov > 0 else 0
            
            families.append(Top5Family(
                familia_id=int(row.get("familia_id")),
                familia_nome=row.get("nome_familia", ""),
                total_movimentacoes=int(mov_count),
                percentual=round(percent, 2),
                items_unicos=int(row.get("items_unicos", 0)),
                sites=int(row.get("sites", 0)),
                demanda_media=float(row.get("demanda_media", 0.0)),
            ))
        
        return families
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching top 5 families: {str(e)}")


@router.get("/tiers", response_model=List[TierAnalytics])
async def get_tier_analytics():
    """Get tier-based analytics"""
    try:
        query = """
            SELECT 
                tier_nivel,
                COUNT(*) as total_materiais,
                AVG(sla_penalty_brl) as avg_sla_penalty_brl,
                AVG(disponibilidade_target) as avg_availability_target,
                SUM(sla_penalty_brl) as total_penalty_risk_brl,
                SUM(CASE WHEN score_importancia > 80 THEN 1 ELSE 0 END) as critical_materials
            FROM Material
            WHERE tier_nivel IS NOT NULL
            GROUP BY tier_nivel
            ORDER BY 
                CASE tier_nivel
                    WHEN 'TIER_1' THEN 1
                    WHEN 'TIER_2' THEN 2
                    WHEN 'TIER_3' THEN 3
                    ELSE 4
                END
        """
        
        results = db_service.execute_query(query)
        
        return [
            TierAnalytics(
                tier_nivel=row.get("tier_nivel", ""),
                total_materiais=int(row.get("total_materiais", 0)),
                avg_sla_penalty_brl=float(row.get("avg_sla_penalty_brl", 0.0)),
                avg_availability_target=float(row.get("avg_availability_target", 0.0)),
                total_penalty_risk_brl=float(row.get("total_penalty_risk_brl", 0.0)),
                critical_materials=int(row.get("critical_materials", 0)),
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tier analytics: {str(e)}")


@router.get("/materials", response_model=FeatureCategoryResponse)
async def get_material_business_context(
    tier_nivel: Optional[str] = Query(None, description="Filter by tier level"),
    familia_id: Optional[int] = Query(None, description="Filter by family ID"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get material business context"""
    try:
        where_clauses = []
        params = {}
        
        if tier_nivel:
            where_clauses.append("m.tier_nivel = :tier_nivel")
            params["tier_nivel"] = tier_nivel
        
        if familia_id:
            where_clauses.append("m.familia_id = :familia_id")
            params["familia_id"] = familia_id
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                m.material_id,
                m.nome_material,
                m.tier_nivel,
                m.sla_penalty_brl,
                m.disponibilidade_target,
                m.score_importancia,
                f.nome_familia
            FROM Material m
            LEFT JOIN Familia f ON m.familia_id = f.familia_id
            WHERE {where_clause}
            ORDER BY m.score_importancia DESC, m.material_id
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset
        
        results = db_service.execute_query(query, params)
        
        data = []
        for row in results:
            feature_obj = {
                "material_id": int(row.get("material_id", 0)),
                "nome_material": row.get("nome_material", ""),
                "tier_nivel": row.get("tier_nivel", ""),
                "sla_penalty_brl": float(row.get("sla_penalty_brl", 0.0)),
                "disponibilidade_target": float(row.get("disponibilidade_target", 0.0)),
                "score_importancia": float(row.get("score_importancia", 0.0)),
                "familia_nome": row.get("nome_familia", ""),
            }
            data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=len(data),
            date_range=None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching material business context: {str(e)}")





