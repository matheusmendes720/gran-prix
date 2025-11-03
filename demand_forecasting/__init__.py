"""
Nova Corrente Demand Forecasting System
Modular Python-based system for daily demand prediction
"""
from .data_loader import DataLoader
from .models.arima_model import ARIMAForecaster
from .models.prophet_model import ProphetForecaster
from .models.lstm_model import LSTMForecaster
from .models.ensemble_model import EnsembleForecaster
from .pp_calculator import PPCalculator
from .pipeline import DemandForecastingPipeline

__version__ = '1.0.0'
__all__ = [
    'DataLoader',
    'ARIMAForecaster',
    'ProphetForecaster',
    'LSTMForecaster',
    'EnsembleForecaster',
    'PPCalculator',
    'DemandForecastingPipeline'
]
