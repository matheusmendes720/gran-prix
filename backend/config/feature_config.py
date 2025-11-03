"""
Feature engineering configuration for Nova Corrente ML features
"""
from typing import Dict, Any, List

# Feature Categories
FEATURE_CATEGORIES: List[str] = [
    'TEMPORAL',
    'VOLUME',
    'RELACIONAL',
    'STATISTICAL',
    'CLIMATE',
    'ECONOMIC',
    '5G',
    'SLA',
    'HIERARCHICAL',
    'CATEGORICAL',
    'BUSINESS',
]

# Temporal Features Configuration
TEMPORAL_FEATURES: Dict[str, Any] = {
    'cyclical_encoding': True,  # Use sin/cos for cyclical features
    'lag_features': [1, 7, 30, 365],  # Days to lag
    'moving_averages': [7, 30, 90],  # Window sizes
    'brazilian_calendar': True,
    'holiday_features': True,
    'seasonal_features': True,
}

# Statistical Features Configuration
STATISTICAL_FEATURES: Dict[str, Any] = {
    'volatility_windows': [7, 30],  # Days for volatility calculation
    'coefficient_of_variation': True,
    'skewness': True,
    'kurtosis': False,  # Optional
    'autocorrelation_lags': [1, 7, 30],
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

# Hierarchical Features Configuration
HIERARCHICAL_FEATURES: Dict[str, Any] = {
    'aggregation_levels': ['familia', 'site', 'fornecedor'],
    'aggregation_metrics': ['mean', 'sum', 'count', 'std'],
    'include_ratios': True,  # Material vs family/site averages
}

# Feature Engineering Pipeline
FEATURE_PIPELINE: Dict[str, Any] = {
    'enable_caching': True,
    'cache_duration': 3600,  # 1 hour
    'parallel_processing': True,
    'batch_size': 100,  # Materials per batch
    'validation': True,
    'handle_missing': 'forward_fill',  # 'forward_fill', 'backward_fill', 'interpolate', 'drop'
}

# Feature Selection
FEATURE_SELECTION: Dict[str, Any] = {
    'correlation_threshold': 0.95,  # Remove highly correlated features
    'importance_threshold': 0.01,  # Minimum feature importance
    'max_features': 73,  # Total number of features (as per spec)
}

# Feature Scaling
FEATURE_SCALING: Dict[str, Any] = {
    'method': 'standard',  # 'standard', 'minmax', 'robust', 'none'
    'fit_on_training_only': True,
}

