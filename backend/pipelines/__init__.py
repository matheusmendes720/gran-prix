"""ETL pipelines module for Nova Corrente"""
from .climate_etl import climate_etl, ClimateETL
from .economic_etl import economic_etl, EconomicETL
from .anatel_5g_etl import anatel_5g_etl, ANATEL5GETL
from .brazilian_calendar_etl import brazilian_calendar_etl, BrazilianCalendarETL
from .feature_calculation_etl import feature_calculation_etl, FeatureCalculationETL
from .orchestrator_service import orchestrator_service, OrchestratorService

__all__ = [
    'climate_etl', 'ClimateETL',
    'economic_etl', 'EconomicETL',
    'anatel_5g_etl', 'ANATEL5GETL',
    'brazilian_calendar_etl', 'BrazilianCalendarETL',
    'feature_calculation_etl', 'FeatureCalculationETL',
    'orchestrator_service', 'OrchestratorService',
]
