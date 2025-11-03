"""
Startup and shutdown event handlers for FastAPI app
Initializes all services and external API clients
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger('nova_corrente.startup')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Nova Corrente API...")
    
    try:
        # Use Integration Manager for centralized initialization
        from app.core.integration_manager import integration_manager
        
        logger.info("Initializing all services and external API clients...")
        init_results = await integration_manager.initialize_all()
        
        # Store integration manager in app state
        app.state.integration_manager = integration_manager
        
        logger.info(f"✅ Startup complete - Status: {init_results['status']}")
        
        # Log summary
        healthy_services = sum(1 for svc in init_results['services'].values() if svc.get('status') == 'healthy')
        total_services = len(init_results['services'])
        logger.info(f"📊 Services: {healthy_services}/{total_services} healthy")
        
        configured_clients = sum(1 for client in init_results['external_clients'].values() if client.get('status') == 'configured' or client.get('status') == 'healthy')
        total_clients = len(init_results['external_clients'])
        logger.info(f"🌐 External APIs: {configured_clients}/{total_clients} configured")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}", exc_info=True)
        # Don't raise - allow app to start even if some services fail
    
    yield
    
    # Shutdown
    logger.info("Shutting down Nova Corrente API...")
    
    try:
        # Close database connections
        integration_manager = getattr(app.state, 'integration_manager', None)
        if integration_manager:
            db_service = integration_manager.get_service('database')
            if db_service and hasattr(db_service, '_SessionLocal'):
                if db_service._SessionLocal:
                    db_service._SessionLocal.close_all()
                    logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")
    
    logger.info("👋 Nova Corrente API shutdown complete")
