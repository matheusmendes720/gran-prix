"""
Health check endpoints with full service status
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Any

try:
    from backend.services.database_service import db_service
except ImportError:
    import sys
    from pathlib import Path
    # Try to find backend directory in parent paths
    backend_dir = Path(__file__).parent.parent.parent.parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    # Also try adding backend parent (project root) to path
    project_root = backend_dir.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    try:
        from backend.services.database_service import db_service
    except ImportError:
        # Last resort: try direct import
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "database_service",
            backend_dir / "services" / "database_service.py"
        )
        if spec and spec.loader:
            db_service_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(db_service_module)
            db_service = db_service_module.db_service

try:
    from backend.config.external_apis_config import (
        INMET_CONFIG,
        BACEN_CONFIG,
        ANATEL_CONFIG,
        OPENWEATHER_CONFIG,
    )
except ImportError:
    INMET_CONFIG = {}
    BACEN_CONFIG = {}
    ANATEL_CONFIG = {}
    OPENWEATHER_CONFIG = {}

try:
    from backend.config.logging_config import get_logger
    logger = get_logger('nova_corrente.health')
except ImportError:
    import logging
    logger = logging.getLogger('nova_corrente.health')

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint
    Checks all internal services and external API clients
    """
    health_status: Dict[str, Any] = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "nova-corrente-api",
        "services": {},
        "external_apis": {},
    }
    
    # Check Database Service
    try:
        db_healthy = db_service.test_connection()
        health_status["services"]["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "connected": db_healthy,
        }
    except Exception as e:
        health_status["services"]["database"] = {
            "status": "error",
            "error": str(e),
        }
        health_status["status"] = "degraded"
    
    # Check External API Clients
    # INMET (Climate)
    try:
        inmet_configured = bool(INMET_CONFIG.get('api_key') or INMET_CONFIG.get('base_url'))
        health_status["external_apis"]["inmet"] = {
            "status": "configured" if inmet_configured else "not_configured",
            "configured": inmet_configured,
        }
    except Exception as e:
        health_status["external_apis"]["inmet"] = {
            "status": "error",
            "error": str(e),
        }
    
    # BACEN (Economic)
    try:
        bacen_configured = bool(BACEN_CONFIG.get('api_key') or BACEN_CONFIG.get('base_url'))
        health_status["external_apis"]["bacen"] = {
            "status": "configured" if bacen_configured else "not_configured",
            "configured": bacen_configured,
        }
    except Exception as e:
        health_status["external_apis"]["bacen"] = {
            "status": "error",
            "error": str(e),
        }
    
    # ANATEL (5G)
    try:
        anatel_configured = bool(ANATEL_CONFIG.get('api_key') or ANATEL_CONFIG.get('base_url'))
        health_status["external_apis"]["anatel"] = {
            "status": "configured" if anatel_configured else "not_configured",
            "configured": anatel_configured,
        }
    except Exception as e:
        health_status["external_apis"]["anatel"] = {
            "status": "error",
            "error": str(e),
        }
    
    # OpenWeatherMap
    try:
        openweather_configured = bool(OPENWEATHER_CONFIG.get('api_key'))
        health_status["external_apis"]["openweather"] = {
            "status": "configured" if openweather_configured else "not_configured",
            "configured": openweather_configured,
        }
    except Exception as e:
        health_status["external_apis"]["openweather"] = {
            "status": "error",
            "error": str(e),
        }
    
    # Determine overall status
    if health_status["services"].get("database", {}).get("status") == "error":
        health_status["status"] = "unhealthy"
    elif any(
        svc.get("status") == "error" 
        for svc in health_status["services"].values()
    ):
        health_status["status"] = "degraded"
    
    return health_status


@router.get("/health/ready")
async def readiness_check():
    """Readiness check - checks if service is ready to accept traffic"""
    # TODO: Add actual readiness checks (database, ML models, etc.)
    return {
        "status": "ready",
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/health/live")
async def liveness_check():
    """Liveness check - checks if service is alive"""
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
    }

