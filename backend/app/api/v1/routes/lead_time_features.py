"""
Lead time features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    LeadTimeFeatures,
    SupplierLeadTime,
    LeadTimeCategory,
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/lead-time", tags=["features", "lead-time"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_lead_time_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get lead time features"""
    try:
        where_clauses = ["feature_category = 'LEAD_TIME'"]
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
            
            if mat_id not in features_by_material:
                features_by_material[mat_id] = {}
            
            features_by_material[mat_id][feature_name] = feature_value
        
        # Flatten to list
        data = []
        for mat_id, features in features_by_material.items():
            lead_time_days = float(features.get("lead_time_days", 0.0))
            
            # Determine category
            if lead_time_days < 7:
                category = LeadTimeCategory.FAST
            elif lead_time_days < 14:
                category = LeadTimeCategory.NORMAL
            elif lead_time_days < 30:
                category = LeadTimeCategory.SLOW
            else:
                category = LeadTimeCategory.VERY_SLOW
            
            feature_obj = {
                "material_id": mat_id,
                "lead_time_days": lead_time_days,
                "base_lead_time_days": float(features.get("base_lead_time_days", 0.0)),
                "total_lead_time_days": float(features.get("total_lead_time_days", 0.0)),
                "customs_delay_days": float(features.get("customs_delay_days", 0.0)),
                "strike_risk": float(features.get("strike_risk", 0.0)),
                "is_critical_lead_time": bool(features.get("is_critical_lead_time", False)),
                "lead_time_category": category.value,
                "supplier_lead_time_mean": float(features.get("supplier_lead_time_mean", 0.0)),
                "supplier_lead_time_std": float(features.get("supplier_lead_time_std", 0.0)),
            }
            data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=len(data),
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lead time features: {str(e)}")


@router.get("/suppliers", response_model=List[SupplierLeadTime])
async def get_supplier_lead_times():
    """Get supplier lead time analytics"""
    try:
        query = """
            SELECT 
                f.fornecedor_id,
                f.nome_fornecedor as fornecedor_nome,
                AVG(fm.lead_time_padrao) as lead_time_medio,
                STDDEV(fm.lead_time_padrao) as lead_time_std,
                MIN(fm.lead_time_padrao) as lead_time_min,
                MAX(fm.lead_time_padrao) as lead_time_max,
                COUNT(fm.material_id) as total_pedidos,
                (100 - (STDDEV(fm.lead_time_padrao) / AVG(fm.lead_time_padrao) * 100)) as reliability_score
            FROM Fornecedor f
            LEFT JOIN Fornecedor_Material fm ON f.fornecedor_id = fm.fornecedor_id
            GROUP BY f.fornecedor_id, f.nome_fornecedor
            HAVING lead_time_medio IS NOT NULL
            ORDER BY lead_time_medio
        """
        
        results = db_service.execute_query(query)
        
        return [
            SupplierLeadTime(
                fornecedor_id=int(row.get("fornecedor_id")),
                fornecedor_nome=row.get("fornecedor_nome", ""),
                lead_time_medio=float(row.get("lead_time_medio", 0.0)),
                lead_time_std=float(row.get("lead_time_std", 0.0)),
                lead_time_min=float(row.get("lead_time_min", 0.0)),
                lead_time_max=float(row.get("lead_time_max", 0.0)),
                total_pedidos=int(row.get("total_pedidos", 0)),
                reliability_score=float(row.get("reliability_score", 0.0)),
            )
            for row in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching supplier lead times: {str(e)}")


@router.get("/materials", response_model=FeatureCategoryResponse)
async def get_material_lead_times(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get material-specific lead times"""
    try:
        query = """
            SELECT 
                m.material_id,
                m.nome_material,
                AVG(fm.lead_time_padrao) as avg_lead_time,
                MIN(fm.lead_time_padrao) as min_lead_time,
                MAX(fm.lead_time_padrao) as max_lead_time,
                COUNT(DISTINCT fm.fornecedor_id) as supplier_count
            FROM Material m
            LEFT JOIN Fornecedor_Material fm ON m.material_id = fm.material_id
            GROUP BY m.material_id, m.nome_material
            HAVING avg_lead_time IS NOT NULL
            ORDER BY avg_lead_time
            LIMIT :limit OFFSET :offset
        """
        
        results = db_service.execute_query(query, {"limit": limit, "offset": offset})
        
        data = [
            {
                "material_id": int(row.get("material_id")),
                "material_name": row.get("nome_material", ""),
                "avg_lead_time": float(row.get("avg_lead_time", 0.0)),
                "min_lead_time": float(row.get("min_lead_time", 0.0)),
                "max_lead_time": float(row.get("max_lead_time", 0.0)),
                "supplier_count": int(row.get("supplier_count", 0)),
            }
            for row in results
        ]
        
        metadata = FeatureMetadata(
            total_count=len(data),
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching material lead times: {str(e)}")


@router.get("/risks", response_model=FeatureCategoryResponse)
async def get_lead_time_risks():
    """Get lead time risk indicators"""
    try:
        query = """
            SELECT 
                m.material_id,
                m.nome_material,
                AVG(fm.lead_time_padrao) as avg_lead_time,
                STDDEV(fm.lead_time_padrao) as lead_time_std,
                CASE 
                    WHEN AVG(fm.lead_time_padrao) > 30 THEN 'VERY_HIGH'
                    WHEN AVG(fm.lead_time_padrao) > 14 THEN 'HIGH'
                    WHEN AVG(fm.lead_time_padrao) > 7 THEN 'MEDIUM'
                    ELSE 'LOW'
                END as risk_level,
                CASE 
                    WHEN STDDEV(fm.lead_time_padrao) / AVG(fm.lead_time_padrao) > 0.5 THEN 1
                    ELSE 0
                END as is_high_variability
            FROM Material m
            LEFT JOIN Fornecedor_Material fm ON m.material_id = fm.material_id
            GROUP BY m.material_id, m.nome_material
            HAVING avg_lead_time IS NOT NULL
            ORDER BY avg_lead_time DESC
        """
        
        results = db_service.execute_query(query)
        
        data = [
            {
                "material_id": int(row.get("material_id")),
                "material_name": row.get("nome_material", ""),
                "avg_lead_time": float(row.get("avg_lead_time", 0.0)),
                "lead_time_std": float(row.get("lead_time_std", 0.0)),
                "risk_level": row.get("risk_level", "LOW"),
                "is_high_variability": bool(row.get("is_high_variability", False)),
            }
            for row in results
        ]
        
        metadata = FeatureMetadata(
            total_count=len(data),
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lead time risks: {str(e)}")

