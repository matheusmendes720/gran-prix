"""
ML Model configuration and hyperparameters for Nova Corrente
"""
from typing import Dict, Any

# Prophet Configuration
PROPHET_CONFIG: Dict[str, Any] = {
    'yearly_seasonality': True,
    'weekly_seasonality': True,
    'daily_seasonality': False,
    'seasonality_mode': 'additive',
    'growth': 'linear',
    'changepoint_prior_scale': 0.05,
    'seasonality_prior_scale': 10.0,
    'holidays_prior_scale': 10.0,
    'mcmc_samples': 0,  # Set to > 0 for uncertainty intervals
    'interval_width': 0.95,
    'uncertainty_samples': 1000,
}

# ARIMA Configuration
ARIMA_CONFIG: Dict[str, Any] = {
    'max_p': 5,
    'max_d': 2,
    'max_q': 5,
    'seasonal': True,
    'm': 7,  # Weekly seasonality
    'stepwise': True,
    'trace': False,
    'error_action': 'ignore',
    'suppress_warnings': True,
    'max_order': 10,
}

# LSTM Configuration
LSTM_CONFIG: Dict[str, Any] = {
    'sequence_length': 30,  # Days of history
    'forecast_horizon': 30,  # Days ahead
    'lstm_units': [64, 32],
    'dense_units': [16, 1],
    'dropout_rate': 0.2,
    'activation': 'relu',
    'optimizer': 'adam',
    'loss': 'mse',
    'metrics': ['mae', 'mape'],
    'batch_size': 32,
    'epochs': 100,
    'validation_split': 0.2,
    'early_stopping_patience': 10,
    'learning_rate': 0.001,
}

# Ensemble Configuration
ENSEMBLE_CONFIG: Dict[str, Any] = {
    'prophet_weight': 0.3,
    'arima_weight': 0.3,
    'lstm_weight': 0.4,
    'performance_based_weights': True,  # Adjust weights based on recent performance
    'min_training_samples': 90,  # Minimum days of data
}

# Model Evaluation Metrics
EVALUATION_METRICS: Dict[str, Any] = {
    'mape_threshold_excellent': 10.0,
    'mape_threshold_good': 15.0,
    'mape_threshold_acceptable': 20.0,
    'rmse_penalty_factor': 1.0,
    'mae_penalty_factor': 1.0,
}

# Cross-Validation Configuration
CV_CONFIG: Dict[str, Any] = {
    'n_splits': 5,
    'test_size': 0.2,
    'gap': 0,  # Gap between train and test
    'min_train_size': 90,  # Minimum training samples
}

# Model Storage
MODEL_STORAGE: Dict[str, Any] = {
    'base_path': 'models/',
    'prophet_path': 'models/prophet/',
    'arima_path': 'models/arima/',
    'lstm_path': 'models/lstm/',
    'ensemble_path': 'models/ensemble/',
    'save_format': 'pkl',  # For Prophet/ARIMA
    'tensorflow_format': 'h5',  # For LSTM
}

