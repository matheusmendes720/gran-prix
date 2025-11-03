"""
Configuration module for Nova Corrente services
"""
from .database_config import (
    DATABASE_CONFIG,
    SQLALCHEMY_DATABASE_URI,
    ASYNC_DATABASE_URI,
    QUERY_TIMEOUT,
    ISOLATION_LEVEL,
)
from .ml_config import (
    PROPHET_CONFIG,
    ARIMA_CONFIG,
    LSTM_CONFIG,
    ENSEMBLE_CONFIG,
    EVALUATION_METRICS,
    CV_CONFIG,
    MODEL_STORAGE,
)
from .external_apis_config import (
    INMET_CONFIG,
    BACEN_CONFIG,
    ANATEL_CONFIG,
    OPENWEATHER_CONFIG,
    RATE_LIMIT_CONFIG,
    BRAZILIAN_CALENDAR_CONFIG,
)
from .feature_config import (
    FEATURE_CATEGORIES,
    TEMPORAL_FEATURES,
    STATISTICAL_FEATURES,
    EXTERNAL_FEATURES,
    HIERARCHICAL_FEATURES,
    FEATURE_PIPELINE,
    FEATURE_SELECTION,
    FEATURE_SCALING,
)
from .logging_config import (
    setup_logger,
    get_logger,
    LOG_DIR,
    LOG_LEVEL,
)

__all__ = [
    # Database
    'DATABASE_CONFIG',
    'SQLALCHEMY_DATABASE_URI',
    'ASYNC_DATABASE_URI',
    'QUERY_TIMEOUT',
    'ISOLATION_LEVEL',
    # ML
    'PROPHET_CONFIG',
    'ARIMA_CONFIG',
    'LSTM_CONFIG',
    'ENSEMBLE_CONFIG',
    'EVALUATION_METRICS',
    'CV_CONFIG',
    'MODEL_STORAGE',
    # External APIs
    'INMET_CONFIG',
    'BACEN_CONFIG',
    'ANATEL_CONFIG',
    'OPENWEATHER_CONFIG',
    'RATE_LIMIT_CONFIG',
    'BRAZILIAN_CALENDAR_CONFIG',
    # Features
    'FEATURE_CATEGORIES',
    'TEMPORAL_FEATURES',
    'STATISTICAL_FEATURES',
    'EXTERNAL_FEATURES',
    'HIERARCHICAL_FEATURES',
    'FEATURE_PIPELINE',
    'FEATURE_SELECTION',
    'FEATURE_SCALING',
    # Logging
    'setup_logger',
    'get_logger',
    'LOG_DIR',
    'LOG_LEVEL',
]

