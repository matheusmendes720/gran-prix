"""
Climate features API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from backend.services.database_service import db_service
from app.api.v1.schemas.features import (
    ClimateFeatures,
    SalvadorClimate,
    ClimateRisk,
    FeatureCategoryResponse,
    FeatureMetadata,
)

router = APIRouter(prefix="/features/climate", tags=["features", "climate"])


@router.get("/", response_model=FeatureCategoryResponse)
async def get_climate_features(
    material_id: Optional[int] = Query(None, description="Filter by material ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Get climate features"""
    try:
        where_clauses = ["feature_category = 'CLIMATE'"]
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
                    "temperature_avg_c": float(features.get("temperature_avg_c", 0.0)),
                    "precipitation_mm": float(features.get("precipitation_mm", 0.0)),
                    "humidity_percent": float(features.get("humidity_percent", 0.0)),
                    "wind_speed_kmh": float(features.get("wind_speed_kmh", 0.0)),
                    "extreme_heat": bool(features.get("extreme_heat", False)),
                    "cold_weather": bool(features.get("cold_weather", False)),
                    "heavy_rain": bool(features.get("heavy_rain", False)),
                    "no_rain": bool(features.get("no_rain", False)),
                    "is_intense_rain": bool(features.get("is_intense_rain", False)),
                    "is_high_humidity": bool(features.get("is_high_humidity", False)),
                    "corrosion_risk": float(features.get("corrosion_risk", 0.0)),
                    "field_work_disruption": float(features.get("field_work_disruption", 0.0)),
                }
                data.append(feature_obj)
        
        metadata = FeatureMetadata(
            total_count=len(data),
            date_range={"start": start_date or "", "end": end_date or ""} if start_date or end_date else None,
            last_updated=datetime.now().isoformat(),
        )
        
        return FeatureCategoryResponse(status="success", data=data, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching climate features: {str(e)}")


@router.get("/salvador", response_model=List[SalvadorClimate])
async def get_salvador_climate(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get Salvador/BA climate data"""
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
                temperatura_media,
                precipitacao_mm,
                umidade_percentual,
                velocidade_vento_kmh,
                is_extreme_heat,
                is_heavy_rain,
                corrosion_risk,
                field_work_disruption
            FROM ClimaSalvador
            WHERE {where_clause}
            ORDER BY data_referencia
        """
        
        results = db_service.execute_query(query, params)
        return [SalvadorClimate(**dict(row)) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Salvador climate: {str(e)}")


@router.get("/risks", response_model=List[ClimateRisk])
async def get_climate_risks(
    min_risk: float = Query(0.5, ge=0.0, le=1.0, description="Minimum risk threshold"),
):
    """Get calculated climate risks (corrosion, field work disruption)"""
    try:
        query = """
            SELECT 
                m.material_id,
                m.nome_material as material_name,
                AVG(CASE WHEN mf.feature_name = 'corrosion_risk' THEN mf.feature_value ELSE 0 END) as corrosion_risk,
                AVG(CASE WHEN mf.feature_name = 'field_work_disruption' THEN mf.feature_value ELSE 0 END) as field_work_disruption
            FROM Material m
            LEFT JOIN MaterialFeatures mf ON m.material_id = mf.material_id 
                AND mf.feature_category = 'CLIMATE'
                AND mf.feature_name IN ('corrosion_risk', 'field_work_disruption')
            GROUP BY m.material_id, m.nome_material
            HAVING corrosion_risk >= :min_risk OR field_work_disruption >= :min_risk
            ORDER BY corrosion_risk DESC, field_work_disruption DESC
        """
        
        results = db_service.execute_query(query, {"min_risk": min_risk})
        
        risks = []
        for row in results:
            corrosion = float(row.get("corrosion_risk", 0.0))
            disruption = float(row.get("field_work_disruption", 0.0))
            max_risk = max(corrosion, disruption)
            
            if max_risk >= 0.7:
                risk_level = "HIGH"
            elif max_risk >= 0.4:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
            
            risks.append(ClimateRisk(
                material_id=int(row.get("material_id")),
                material_name=row.get("material_name", ""),
                corrosion_risk=corrosion,
                field_work_disruption=disruption,
                risk_level=risk_level,
            ))
        
        return risks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching climate risks: {str(e)}")


@router.get("/trends", response_model=FeatureCategoryResponse)
async def get_climate_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get climate trends over time"""
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
                AVG(temperatura_media) as avg_temperature,
                AVG(precipitacao_mm) as avg_precipitation,
                AVG(umidade_percentual) as avg_humidity,
                AVG(corrosion_risk) as avg_corrosion_risk,
                AVG(field_work_disruption) as avg_field_work_disruption
            FROM ClimaSalvador
            WHERE {where_clause}
            GROUP BY data_referencia
            ORDER BY data_referencia
        """
        
        results = db_service.execute_query(query, params)
        
        data = [
            {
                "data_referencia": str(row.get("data_referencia")),
                "avg_temperature": float(row.get("avg_temperature", 0.0)),
                "avg_precipitation": float(row.get("avg_precipitation", 0.0)),
                "avg_humidity": float(row.get("avg_humidity", 0.0)),
                "avg_corrosion_risk": float(row.get("avg_corrosion_risk", 0.0)),
                "avg_field_work_disruption": float(row.get("avg_field_work_disruption", 0.0)),
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
        raise HTTPException(status_code=500, detail=f"Error fetching climate trends: {str(e)}")

