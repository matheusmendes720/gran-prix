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

# ❌ REMOVED: External API configs (not used in deployment - using precomputed data)
# External APIs are disabled in production deployment

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
    Comprehensive health check endpoint (Simplified for deployment)
    Checks internal services only - NO external APIs, NO ML services
    """
    health_status: Dict[str, Any] = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "service": "nova-corrente-api",
        "services": {},
        # ❌ REMOVED: external_apis (not used in deployment - using precomputed data)
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
    
    # ❌ REMOVED: External API Clients checks (not used in deployment)
    # External APIs are disabled in production - data is precomputed locally
    
    # Check ML Dependencies (NO ML allowed in deployment)
    try:
        ml_packages_to_check = ['torch', 'tensorflow', 'sklearn', 'mlflow', 'xgboost', 'lightgbm', 'prophet', 'pmdarima']
        ml_violations = []
        
        # Try to import and check each ML package
        for package in ml_packages_to_check:
            try:
                __import__(package)
                ml_violations.append(package)
            except ImportError:
                pass  # Good - ML package not installed
        
        health_status["ml_dependencies"] = {
            "status": "compliant" if len(ml_violations) == 0 else "non_compliant",
            "message": "No ML dependencies detected" if len(ml_violations) == 0 else f"ML dependencies detected: {ml_violations}",
            "checked_packages": ml_packages_to_check,
            "violations": ml_violations
        }
        
        # If ML dependencies found, mark as degraded
        if len(ml_violations) > 0:
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["ml_dependencies"] = {
            "status": "error",
            "message": f"Error checking ML dependencies: {str(e)}",
            "checked_packages": [],
            "violations": []
        }
    
    # Determine overall status
    if health_status["services"].get("database", {}).get("status") == "error":
        health_status["status"] = "unhealthy"
    elif any(
        svc.get("status") == "error" 
        for svc in health_status["services"].values()
    ):
        health_status["status"] = "degraded"
    elif health_status.get("ml_dependencies", {}).get("status") == "non_compliant":
        health_status["status"] = "degraded"
    
    return health_status


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check - checks if service is ready to accept traffic
    Simplified for deployment - NO ML models, NO external APIs
    """
    try:
        db_ready = db_service.test_connection()
        return {
            "status": "ready" if db_ready else "not_ready",
            "timestamp": datetime.now().isoformat(),
            "database": "connected" if db_ready else "disconnected",
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@router.get("/health/live")
async def liveness_check():
    """Liveness check - checks if service is alive"""
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
    }

