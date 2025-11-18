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
    - Inner Data Services (database, features, analytics, predictions)
    - Outer API Clients (BACEN, INMET, ANATEL, OpenWeatherMap, etc.)
    """
    
    def __init__(self):
        """Initialize integration manager"""
        self.services: Dict[str, Any] = {}
        self.external_clients: Dict[str, Any] = {}
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
            'external_clients': {},
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
            
            # External Data Service
            try:
                from backend.services.external_data_service import external_data_service
                self.services['external_data'] = external_data_service
                results['services']['external_data'] = {'status': 'healthy'}
                logger.info("✅ External data service initialized")
            except Exception as e:
                logger.error(f"❌ External data service error: {e}")
                results['services']['external_data'] = {'status': 'error', 'error': str(e)}
            
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
            
            # Prediction Service
            try:
                from backend.services.prediction_service import prediction_service
                self.services['prediction'] = prediction_service
                results['services']['prediction'] = {'status': 'healthy'}
                logger.info("✅ Prediction service initialized")
            except Exception as e:
                logger.error(f"❌ Prediction service error: {e}")
                results['services']['prediction'] = {'status': 'error', 'error': str(e)}
            
            # Initialize Outer API Clients
            logger.info("Initializing external API clients...")
            
            # INMET (Climate)
            try:
                from backend.config.external_apis_config import INMET_CONFIG
                self.external_clients['inmet'] = {
                    'config': INMET_CONFIG,
                    'configured': bool(INMET_CONFIG.get('api_key') or INMET_CONFIG.get('base_url')),
                    'status': 'configured' if (INMET_CONFIG.get('api_key') or INMET_CONFIG.get('base_url')) else 'not_configured'
                }
                results['external_clients']['inmet'] = self.external_clients['inmet'].copy()
                logger.info("✅ INMET (Climate) API client initialized")
            except Exception as e:
                logger.error(f"❌ INMET API client error: {e}")
                results['external_clients']['inmet'] = {'status': 'error', 'error': str(e)}
            
            # BACEN (Economic)
            try:
                from backend.config.external_apis_config import BACEN_CONFIG
                self.external_clients['bacen'] = {
                    'config': BACEN_CONFIG,
                    'configured': bool(BACEN_CONFIG.get('api_key') or BACEN_CONFIG.get('base_url')),
                    'status': 'configured' if (BACEN_CONFIG.get('api_key') or BACEN_CONFIG.get('base_url')) else 'not_configured'
                }
                results['external_clients']['bacen'] = self.external_clients['bacen'].copy()
                logger.info("✅ BACEN (Economic) API client initialized")
            except Exception as e:
                logger.error(f"❌ BACEN API client error: {e}")
                results['external_clients']['bacen'] = {'status': 'error', 'error': str(e)}
            
            # ANATEL (5G)
            try:
                from backend.config.external_apis_config import ANATEL_CONFIG
                self.external_clients['anatel'] = {
                    'config': ANATEL_CONFIG,
                    'configured': bool(ANATEL_CONFIG.get('api_key') or ANATEL_CONFIG.get('base_url')),
                    'status': 'configured' if (ANATEL_CONFIG.get('api_key') or ANATEL_CONFIG.get('base_url')) else 'not_configured'
                }
                results['external_clients']['anatel'] = self.external_clients['anatel'].copy()
                logger.info("✅ ANATEL (5G) API client initialized")
            except Exception as e:
                logger.error(f"❌ ANATEL API client error: {e}")
                results['external_clients']['anatel'] = {'status': 'error', 'error': str(e)}
            
            # OpenWeatherMap
            try:
                from backend.config.external_apis_config import OPENWEATHER_CONFIG
                self.external_clients['openweather'] = {
                    'config': OPENWEATHER_CONFIG,
                    'configured': bool(OPENWEATHER_CONFIG.get('api_key')),
                    'status': 'configured' if OPENWEATHER_CONFIG.get('api_key') else 'not_configured'
                }
                results['external_clients']['openweather'] = self.external_clients['openweather'].copy()
                logger.info("✅ OpenWeatherMap API client initialized")
            except Exception as e:
                logger.error(f"❌ OpenWeatherMap API client error: {e}")
                results['external_clients']['openweather'] = {'status': 'error', 'error': str(e)}
            
            # Expanded API Integration (25+ sources)
            try:
                from backend.services.expanded_api_integration import ExpandedAPIIntegration
                self.external_clients['expanded_api'] = ExpandedAPIIntegration()
                results['external_clients']['expanded_api'] = {'status': 'healthy'}
                logger.info("✅ Expanded API integration initialized (25+ sources)")
            except Exception as e:
                logger.error(f"❌ Expanded API integration error: {e}")
                results['external_clients']['expanded_api'] = {'status': 'error', 'error': str(e)}
            
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
    
    def get_external_client(self, client_name: str) -> Optional[Any]:
        """Get an external API client by name"""
        return self.external_clients.get(client_name)
    
    async def refresh_all_external_data(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Refresh all external data sources
        
        Args:
            start_date: Start date (default: 7 days ago)
            end_date: End date (default: today)
        
        Returns:
            Dictionary with refresh results
        """
        from datetime import timedelta
        
        if start_date is None:
            start_date = date.today() - timedelta(days=7)
        if end_date is None:
            end_date = date.today()
        
        results = {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'refreshed': {},
            'errors': [],
            'status': 'success'
        }
        
        integration_service = self.get_service('integration')
        if integration_service:
            try:
                refresh_results = integration_service.refresh_all_external_data(
                    start_date, end_date
                )
                results['refreshed'] = refresh_results
                logger.info(f"Refreshed {len(refresh_results)} external data sources")
            except Exception as e:
                logger.error(f"Error refreshing external data: {e}")
                results['errors'].append(str(e))
                results['status'] = 'error'
        else:
            logger.warning("Integration service not available")
            results['status'] = 'error'
            results['errors'].append("Integration service not initialized")
        
        return results


# Global integration manager instance
integration_manager = IntegrationManager()

