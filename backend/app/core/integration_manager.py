"""
Integration Manager - Central coordinator for all service integrations
Handles initialization, health checks, and orchestration of all services
"""
from typing import Dict, Any, Optional
from datetime import date, datetime
import logging

logger = logging.getLogger('nova_corrente.integration_manager')


class IntegrationManager:
    """
    Central manager for all backend integrations:
    - Inner Data Services (database, features, analytics) - Read-only
    - NO ML Services in deployment
    - NO External API Clients in deployment (using precomputed data)
    """
    
    def __init__(self):
        """Initialize integration manager"""
        self.services: Dict[str, Any] = {}
        # ❌ REMOVED: external_clients (not used in deployment)
        self.initialized = False
        
    async def initialize_all(self) -> Dict[str, Any]:
        """
        Initialize all services and external API clients
        
        Returns:
            Dictionary with initialization status
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            # ❌ REMOVED: external_clients (not used in deployment)
            'status': 'initializing'
        }
        
# Logger is already defined at module level
        
        try:
            # Initialize Inner Data Services
            logger.info("Initializing inner data services...")
            
            # Database Service
            try:
                from backend.services.database_service import db_service
                db_healthy = db_service.test_connection()
                self.services['database'] = db_service
                results['services']['database'] = {
                    'status': 'healthy' if db_healthy else 'unhealthy',
                    'connected': db_healthy
                }
                logger.info("✅ Database service initialized")
            except Exception as e:
                logger.error(f"❌ Database service error: {e}")
                results['services']['database'] = {'status': 'error', 'error': str(e)}
            
            # ❌ REMOVED: External Data Service (not used in deployment - using precomputed data)
            # External APIs are disabled in production - data is precomputed locally
            
            # Integration Service
            try:
                from backend.services.integration_service import integration_service
                self.services['integration'] = integration_service
                results['services']['integration'] = {'status': 'healthy'}
                logger.info("✅ Integration service initialized")
            except Exception as e:
                logger.error(f"❌ Integration service error: {e}")
                results['services']['integration'] = {'status': 'error', 'error': str(e)}
            
            # Feature Service
            try:
                from backend.services.feature_service import feature_service
                self.services['feature'] = feature_service
                results['services']['feature'] = {'status': 'healthy'}
                logger.info("✅ Feature service initialized")
            except Exception as e:
                logger.error(f"❌ Feature service error: {e}")
                results['services']['feature'] = {'status': 'error', 'error': str(e)}
            
            # Material Service
            try:
                from backend.services.material_service import material_service
                self.services['material'] = material_service
                results['services']['material'] = {'status': 'healthy'}
                logger.info("✅ Material service initialized")
            except Exception as e:
                logger.error(f"❌ Material service error: {e}")
                results['services']['material'] = {'status': 'error', 'error': str(e)}
            
            # Analytics Service
            try:
                from backend.services.analytics_service import analytics_service
                self.services['analytics'] = analytics_service
                results['services']['analytics'] = {'status': 'healthy'}
                logger.info("✅ Analytics service initialized")
            except Exception as e:
                logger.error(f"❌ Analytics service error: {e}")
                results['services']['analytics'] = {'status': 'error', 'error': str(e)}
            
            # ❌ REMOVED: Prediction Service (ML not used in deployment - using precomputed results)
            # ML processing runs locally and generates precomputed results
            
            # ❌ REMOVED: External API Clients (not used in deployment - using precomputed data)
            # External APIs are disabled in production:
            # - INMET (Climate) - disabled
            # - BACEN (Economic) - disabled
            # - ANATEL (5G) - disabled
            # - OpenWeatherMap - disabled
            # - Expanded API Integration - disabled
            # Data is precomputed locally and read-only in deployment
            logger.info("⚠️ External API clients disabled in deployment - using precomputed data")
            
            # Determine overall status
            service_errors = sum(1 for svc in results['services'].values() if svc.get('status') == 'error')
            if service_errors == 0:
                results['status'] = 'healthy'
            elif service_errors < len(results['services']):
                results['status'] = 'degraded'
            else:
                results['status'] = 'unhealthy'
            
            self.initialized = True
            logger.info(f"🎉 Integration manager initialized: {results['status']}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Integration manager initialization error: {e}")
            results['status'] = 'error'
            results['error'] = str(e)
            return results
    
    def get_service(self, service_name: str) -> Optional[Any]:
        """Get a service by name"""
        return self.services.get(service_name)
    
    # ❌ REMOVED: get_external_client() - External API clients not used in deployment
    
    # ❌ REMOVED: refresh_all_external_data() - External APIs disabled in deployment
    # Data refresh is done locally in ML processing environment, not in deployment


# Global integration manager instance
integration_manager = IntegrationManager()

