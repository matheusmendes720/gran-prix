"""Services module for Nova Corrente"""
from .database_service import db_service, DatabaseService
from .material_service import material_service, MaterialService
from .feature_service import feature_service, FeatureService
from .analytics_service import analytics_service, AnalyticsService
from .prediction_service import prediction_service, PredictionService
from .external_data_service import external_data_service, ExternalDataService
from .integration_service import integration_service, IntegrationService
from .expanded_api_integration import expanded_api_integration, ExpandedAPIIntegration

__all__ = [
    'db_service', 'DatabaseService',
    'material_service', 'MaterialService',
    'feature_service', 'FeatureService',
    'analytics_service', 'AnalyticsService',
    'prediction_service', 'PredictionService',
    'external_data_service', 'ExternalDataService',
    'integration_service', 'IntegrationService',
    'expanded_api_integration', 'ExpandedAPIIntegration',
]
