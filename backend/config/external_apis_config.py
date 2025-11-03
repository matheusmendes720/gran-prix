"""
External API configuration for Brazilian data sources
"""
import os
from typing import Dict, Any, Optional

# INMET (Climate Data) Configuration
INMET_CONFIG: Dict[str, Any] = {
    'base_url': 'https://apitempo.inmet.gov.br/',
    'station_code': 'A001',  # Salvador/BA station
    'api_key': os.getenv('INMET_API_KEY', ''),
    'timeout': 30,
    'retry_attempts': 3,
    'retry_delay': 5,  # seconds
    'cache_duration': 3600,  # 1 hour cache
}

# BACEN (Economic Data) Configuration
BACEN_CONFIG: Dict[str, Any] = {
    'base_url': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.',
    'series_codes': {
        'ipca': 433,  # IPCA inflation index
        'selic': 11,  # SELIC interest rate
        'exchange_rate': 1,  # USD/BRL exchange rate
        'gdp': 4380,  # GDP index
    },
    'api_key': os.getenv('BACEN_API_KEY', ''),
    'timeout': 30,
    'retry_attempts': 3,
    'retry_delay': 5,
    'cache_duration': 86400,  # 24 hours cache
}

# ANATEL (5G Expansion) Configuration
ANATEL_CONFIG: Dict[str, Any] = {
    'base_url': 'https://www.gov.br/anatel/',
    'data_endpoint': 'dadosabertos/',  # Data portal endpoint
    'scraping_enabled': True,  # Fallback to scraping if API unavailable
    'api_key': os.getenv('ANATEL_API_KEY', ''),
    'timeout': 60,
    'retry_attempts': 3,
    'retry_delay': 10,
    'cache_duration': 86400,  # 24 hours cache
}

# OpenWeatherMap (Alternative Climate Source)
OPENWEATHER_CONFIG: Dict[str, Any] = {
    'base_url': 'https://api.openweathermap.org/data/2.5/',
    'api_key': os.getenv('OPENWEATHER_API_KEY', ''),
    'city': 'Salvador,BR',
    'timeout': 30,
    'retry_attempts': 3,
    'cache_duration': 3600,  # 1 hour cache
}

# Rate Limiting
RATE_LIMIT_CONFIG: Dict[str, Any] = {
    'requests_per_minute': 60,
    'requests_per_hour': 1000,
    'enable_rate_limiting': True,
}

# Brazilian Calendar Configuration
BRAZILIAN_CALENDAR_CONFIG: Dict[str, Any] = {
    'holiday_source': 'internal',  # 'internal' or 'api'
    'regions': ['NORTE', 'NORDESTE', 'SUDESTE', 'SUL', 'CENTRO-OESTE'],
    'update_frequency': 'yearly',  # Update frequency
}

# External Features Configuration
EXTERNAL_FEATURES: Dict[str, Any] = {
    'climate_features': [
        'temperature_avg',
        'temperature_max',
        'temperature_min',
        'precipitation_mm',
        'humidity_percent',
        'wind_speed_kmh',
        'is_extreme_heat',
        'is_heavy_rain',
        'corrosion_risk',
        'field_work_disruption',
    ],
    'economic_features': [
        'taxa_inflacao',
        'taxa_inflacao_anual',
        'taxa_cambio_brl_usd',
        'pib_crescimento',
        'taxa_selic',
        'is_high_inflation',
        'is_currency_devaluation',
    ],
    '5g_features': [
        'cobertura_5g_percentual',
        'investimento_5g_brl_billions',
        'torres_5g_ativas',
        'is_5g_milestone',
        'taxa_expansao_5g',
    ],
}

