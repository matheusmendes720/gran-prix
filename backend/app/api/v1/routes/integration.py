"""
Integration management endpoints
Endpoints for managing service integrations and external data refresh
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from datetime import date, datetime
from pydantic import BaseModel

try:
    from app.core.integration_manager import integration_manager
except ImportError:
    import sys
    from pathlib import Path
    backend_dir = Path(__file__).parent.parent.parent.parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    from app.core.integration_manager import integration_manager

try:
    from backend.config.logging_config import get_logger
    logger = get_logger('nova_corrente.api.integration')
except ImportError:
    import logging
    logger = logging.getLogger('nova_corrente.api.integration')

router = APIRouter(prefix="/integration", tags=["integration"])


class RefreshRequest(BaseModel):
    """Request model for data refresh"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    data_types: Optional[list[str]] = None


@router.get("/status")
async def get_integration_status() -> Dict[str, Any]:
    """
    Get comprehensive integration status
    Shows status of all inner services and outer API clients
    """
    try:
        if not integration_manager.initialized:
            await integration_manager.initialize_all()
        
        status = {
            'initialized': integration_manager.initialized,
            'services': {},
            'external_clients': {},
            'timestamp': datetime.now().isoformat(),
        }
        
        # Get service statuses
        for service_name, service in integration_manager.services.items():
            try:
                if service_name == 'database':
                    db_healthy = service.test_connection()
                    status['services'][service_name] = {
                        'status': 'healthy' if db_healthy else 'unhealthy',
                        'connected': db_healthy
                    }
                else:
                    status['services'][service_name] = {
                        'status': 'healthy',
                        'available': True
                    }
            except Exception as e:
                status['services'][service_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        # Get external client statuses
        for client_name, client_info in integration_manager.external_clients.items():
            if isinstance(client_info, dict):
                status['external_clients'][client_name] = client_info
            else:
                status['external_clients'][client_name] = {
                    'status': 'healthy',
                    'available': True
                }
        
        return status
        
    except Exception as e:
        logger.error(f"Error getting integration status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh")
async def refresh_external_data(request: RefreshRequest) -> Dict[str, Any]:
    """
    Refresh all external data sources
    
    Args:
        request: Refresh request with optional date range and data types
    
    Returns:
        Dictionary with refresh results
    """
    try:
        start_date = None
        end_date = None
        
        if request.start_date:
            start_date = date.fromisoformat(request.start_date)
        if request.end_date:
            end_date = date.fromisoformat(request.end_date)
        
        results = await integration_manager.refresh_all_external_data(
            start_date=start_date,
            end_date=end_date
        )
        
        return results
        
    except Exception as e:
        logger.error(f"Error refreshing external data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/services")
async def list_services() -> Dict[str, Any]:
    """List all available inner services"""
    return {
        'services': list(integration_manager.services.keys()),
        'count': len(integration_manager.services)
    }


@router.get("/external-clients")
async def list_external_clients() -> Dict[str, Any]:
    """List all available external API clients"""
    return {
        'clients': list(integration_manager.external_clients.keys()),
        'count': len(integration_manager.external_clients)
    }

