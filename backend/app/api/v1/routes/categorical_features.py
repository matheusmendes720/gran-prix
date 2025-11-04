"""
Categorical features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    CategoricalFeatures,
    FamilyEncoding,
    SiteEncoding,
    SupplierEncoding,
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/categorical", tags=["features", "categorical"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_categorical_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get categorical features"""
    try:
        where_clauses = ["feature_category = 'CATEGORICAL'"]
        params = {}
        
        if material_id:
            where_clauses.append("material_id = :material_id")
            params["material_id"] = material_id
        
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
                m.material_id,
                f.nome_familia as familia,
                mf.feature_value as familia_encoded,
                me.site_id,
                fn.nome_fornecedor as fornecedor
            FROM Material m
            LEFT JOIN MaterialFeatures mf ON m.material_id = mf.material_id 
                AND mf.feature_category = 'CATEGORICAL'
                AND mf.feature_name = 'familia_encoded'
            LEFT JOIN Familia f ON m.familia_id = f.familia_id
            LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id
            LEFT JOIN Fornecedor_Material fm ON m.material_id = fm.material_id
            LEFT JOIN Fornecedor fn ON fm.fornecedor_id = fn.fornecedor_id
            WHERE {where_clause.replace('material_id', 'm.material_id')}
            GROUP BY m.material_id, f.nome_familia, mf.feature_value, me.site_id, fn.nome_fornecedor
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset
        
        results = db_service.execute_query(query, params)
        
        data = []
        for row in results:
            feature_obj = {
                "material_id": int(row.get("material_id", 0)),
                "familia": row.get("familia", ""),
                "familia_encoded": int(row.get("familia_encoded", 0)) if row.get("familia_encoded") else 0,
                "deposito": "",  # Could be derived from site
                "site_id": row.get("site_id", ""),
                "fornecedor": row.get("fornecedor", ""),
            }
            data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=total_count,
            date_range=None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categorical features: {str(e)}")


@router.get("/families", response_model=List[FamilyEncoding])
async def get_family_encodings():
    """Get family encodings"""
    try:
        query = """
            SELECT 
                f.familia_id,
                f.nome_familia,
                COUNT(DISTINCT m.material_id) as total_materiais,
                ROW_NUMBER() OVER (ORDER BY f.familia_id) as familia_encoded
            FROM Familia f
            LEFT JOIN Material m ON f.familia_id = m.familia_id
            GROUP BY f.familia_id, f.nome_familia
            ORDER BY f.familia_id
        """
        
        results = db_service.execute_query(query)
        
        return [
            FamilyEncoding(
                familia_id=int(row.get("familia_id")),
                familia_nome=row.get("nome_familia", ""),
                familia_encoded=int(row.get("familia_encoded", 0)),
                total_materiais=int(row.get("total_materiais", 0)),
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching family encodings: {str(e)}")


@router.get("/sites", response_model=List[SiteEncoding])
async def get_site_encodings():
    """Get site encodings"""
    try:
        query = """
            SELECT 
                site_id,
                COUNT(DISTINCT material_id) as total_materiais
            FROM MovimentacaoEstoque
            WHERE site_id IS NOT NULL
            GROUP BY site_id
            ORDER BY total_materiais DESC
        """
        
        results = db_service.execute_query(query)
        
        return [
            SiteEncoding(
                site_id=row.get("site_id", ""),
                site_nome=None,
                total_materiais=int(row.get("total_materiais", 0)),
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching site encodings: {str(e)}")


@router.get("/suppliers", response_model=List[SupplierEncoding])
async def get_supplier_encodings():
    """Get supplier encodings"""
    try:
        query = """
            SELECT 
                fn.fornecedor_id,
                fn.nome_fornecedor,
                COUNT(DISTINCT fm.material_id) as total_materiais
            FROM Fornecedor fn
            LEFT JOIN Fornecedor_Material fm ON fn.fornecedor_id = fm.fornecedor_id
            GROUP BY fn.fornecedor_id, fn.nome_fornecedor
            ORDER BY total_materiais DESC
        """
        
        results = db_service.execute_query(query)
        
        return [
            SupplierEncoding(
                fornecedor_id=int(row.get("fornecedor_id")),
                fornecedor_nome=row.get("nome_fornecedor", ""),
                fornecedor_encoded=None,
                total_materiais=int(row.get("total_materiais", 0)),
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching supplier encodings: {str(e)}")





