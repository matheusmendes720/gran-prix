"""External data service for Nova Corrente - External API integrations"""
from typing import Dict, Any, Optional
from datetime import date
from backend.pipelines.climate_etl import climate_etl
from backend.pipelines.economic_etl import economic_etl
from backend.pipelines.anatel_5g_etl import anatel_5g_etl
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.services.external_data')


class ExternalDataService:
    """Service for external data management"""
    
    def refresh_climate_data(self, start_date: date, end_date: date) -> int:
        """Refresh climate data"""
        try:
            return climate_etl.run(start_date, end_date)
        except Exception as e:
            logger.error(f"Error refreshing climate data: {e}")
            raise
    
    def refresh_economic_data(self, start_date: date, end_date: date) -> int:
        """Refresh economic data"""
        try:
            return economic_etl.run(start_date, end_date)
        except Exception as e:
            logger.error(f"Error refreshing economic data: {e}")
            raise
    
    def refresh_5g_data(self, start_date: date, end_date: date) -> int:
        """Refresh 5G data"""
        try:
            return anatel_5g_etl.run(start_date, end_date)
        except Exception as e:
            logger.error(f"Error refreshing 5G data: {e}")
            raise


external_data_service = ExternalDataService()
