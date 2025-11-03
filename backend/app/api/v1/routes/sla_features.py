"""
SLA features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    SLAFeatures,
    SLAPenalty,
    SLAViolation,
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/sla", tags=["features", "sla"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_sla_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    tier_nivel: Optional[str] = Query(None, description="Filter by tier level"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get SLA features"""
    try:
        where_clauses = []
        params = {}
        
        if material_id:
            where_clauses.append("m.material_id = :material_id")
            params["material_id"] = material_id
        
        if tier_nivel:
            where_clauses.append("m.tier_nivel = :tier_nivel")
            params["tier_nivel"] = tier_nivel
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                m.material_id,
                m.nome_material,
                m.tier_nivel,
                m.sla_penalty_brl,
                m.disponibilidade_target,
                AVG(CASE WHEN mf.feature_name = 'downtime_hours_monthly' THEN mf.feature_value ELSE 0 END) as downtime_hours_monthly,
                AVG(CASE WHEN mf.feature_name = 'sla_violation_risk' THEN mf.feature_value ELSE 0 END) as sla_violation_risk
            FROM Material m
            LEFT JOIN MaterialFeatures mf ON m.material_id = mf.material_id 
                AND mf.feature_category = 'SLA'
            WHERE {where_clause}
            GROUP BY m.material_id, m.nome_material, m.tier_nivel, m.sla_penalty_brl, m.disponibilidade_target
            ORDER BY m.sla_penalty_brl DESC
            LIMIT :limit OFFSET :offset
        """
        params["limit"] = limit
        params["offset"] = offset
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "material_id": int(row.get("material_id")),
                "material_name": row.get("nome_material", ""),
                "tier_nivel": row.get("tier_nivel", ""),
                "sla_penalty_brl": float(row.get("sla_penalty_brl", 0.0)),
                "availability_target": float(row.get("disponibilidade_target", 0.0)),
                "downtime_hours_monthly": float(row.get("downtime_hours_monthly", 0.0)),
                "sla_violation_risk": float(row.get("sla_violation_risk", 0.0)),
                "availability_actual": None,  # Could be calculated from downtime
            }
            for row in results
        ]
        
        metadata = FeatureMetadata(
            total_count=len(data),
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching SLA features: {str(e)}")


@router.get("/penalties", response_model=List[SLAPenalty])
async def get_sla_penalties(
    tier_nivel: Optional[str] = Query(None, description="Filter by tier level"),
):
    """Get SLA penalties by material/tier"""
    try:
        where_clauses = []
        params = {}
        
        if tier_nivel:
            where_clauses.append("m.tier_nivel = :tier_nivel")
            params["tier_nivel"] = tier_nivel
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                m.material_id,
                m.nome_material,
                m.tier_nivel,
                m.sla_penalty_brl,
                m.disponibilidade_target,
                (100 - AVG(CASE WHEN mf.feature_name = 'downtime_hours_monthly' THEN (mf.feature_value / 730 * 100) ELSE 0 END)) as availability_actual
            FROM Material m
            LEFT JOIN MaterialFeatures mf ON m.material_id = mf.material_id 
                AND mf.feature_category = 'SLA'
            WHERE {where_clause}
            GROUP BY m.material_id, m.nome_material, m.tier_nivel, m.sla_penalty_brl, m.disponibilidade_target
            ORDER BY m.sla_penalty_brl DESC
        """
        
        results = db_service.execute_query(query, params)
        
        penalties = []
        for row in results:
            availability_actual = float(row.get("availability_actual", 0.0))
            availability_target = float(row.get("disponibilidade_target", 0.0))
            sla_penalty = float(row.get("sla_penalty_brl", 0.0))
            
            # Calculate penalty risk
            if availability_actual < availability_target:
                penalty_risk = (availability_target - availability_actual) / 100 * sla_penalty
            else:
                penalty_risk = 0.0
            
            penalties.append(SLAPenalty(
                material_id=int(row.get("material_id")),
                material_name=row.get("nome_material", ""),
                tier_nivel=row.get("tier_nivel", ""),
                sla_penalty_brl=sla_penalty,
                availability_target=availability_target,
                availability_actual=availability_actual if availability_actual > 0 else None,
                penalty_risk_brl=penalty_risk,
            ))
        
        return penalties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching SLA penalties: {str(e)}")


@router.get("/availability", response_model=FeatureCategoryResponse)
async def get_sla_availability(
    tier_nivel: Optional[str] = Query(None, description="Filter by tier level"),
):
    """Get availability targets and actuals"""
    try:
        where_clauses = []
        params = {}
        
        if tier_nivel:
            where_clauses.append("m.tier_nivel = :tier_nivel")
            params["tier_nivel"] = tier_nivel
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                m.material_id,
                m.nome_material,
                m.tier_nivel,
                m.disponibilidade_target,
                (100 - AVG(CASE WHEN mf.feature_name = 'downtime_hours_monthly' THEN (mf.feature_value / 730 * 100) ELSE 0 END)) as availability_actual,
                AVG(CASE WHEN mf.feature_name = 'downtime_hours_monthly' THEN mf.feature_value ELSE 0 END) as downtime_hours_monthly
            FROM Material m
            LEFT JOIN MaterialFeatures mf ON m.material_id = mf.material_id 
                AND mf.feature_category = 'SLA'
            WHERE {where_clause}
            GROUP BY m.material_id, m.nome_material, m.tier_nivel, m.disponibilidade_target
            ORDER BY m.disponibilidade_target DESC
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "material_id": int(row.get("material_id")),
                "material_name": row.get("nome_material", ""),
                "tier_nivel": row.get("tier_nivel", ""),
                "availability_target": float(row.get("disponibilidade_target", 0.0)),
                "availability_actual": float(row.get("availability_actual", 0.0)),
                "downtime_hours_monthly": float(row.get("downtime_hours_monthly", 0.0)),
            }
            for row in results
        ]
        
        metadata = FeatureMetadata(
            total_count=len(data),
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching SLA availability: {str(e)}")


@router.get("/violations", response_model=List[SLAViolation])
async def get_sla_violations(
    min_risk: float = Query(0.5, ge=0.0, le=1.0, description="Minimum violation risk threshold"),
):
    """Get SLA violation risks"""
    try:
        query = """
            SELECT 
                m.material_id,
                m.nome_material,
                m.tier_nivel,
                AVG(CASE WHEN mf.feature_name = 'sla_violation_risk' THEN mf.feature_value ELSE 0 END) as sla_violation_risk,
                m.sla_penalty_brl
            FROM Material m
            LEFT JOIN MaterialFeatures mf ON m.material_id = mf.material_id 
                AND mf.feature_category = 'SLA'
            GROUP BY m.material_id, m.nome_material, m.tier_nivel, m.sla_penalty_brl
            HAVING sla_violation_risk >= :min_risk
            ORDER BY sla_violation_risk DESC
        """
        
        results = db_service.execute_query(query, {"min_risk": min_risk})
        
        violations = []
        for row in results:
            risk = float(row.get("sla_violation_risk", 0.0))
            sla_penalty = float(row.get("sla_penalty_brl", 0.0))
            
            if risk >= 0.8:
                violation_level = "CRITICAL"
            elif risk >= 0.6:
                violation_level = "HIGH"
            elif risk >= 0.4:
                violation_level = "MEDIUM"
            else:
                violation_level = "LOW"
            
            estimated_penalty = risk * sla_penalty
            
            violations.append(SLAViolation(
                material_id=int(row.get("material_id")),
                material_name=row.get("nome_material", ""),
                tier_nivel=row.get("tier_nivel", ""),
                sla_violation_risk=risk,
                violation_level=violation_level,
                estimated_penalty_brl=estimated_penalty,
            ))
        
        return violations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching SLA violations: {str(e)}")

