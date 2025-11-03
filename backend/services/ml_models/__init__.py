"""ML models module for Nova Corrente"""
from .model_registry import model_registry, ModelRegistry
from .prophet_model import prophet_model, ProphetModel
from .arima_model import arima_model, ARIMAModel
from .lstm_model import lstm_model, LSTMModel
from .ensemble_model import ensemble_model, EnsembleModel

__all__ = [
    'model_registry', 'ModelRegistry',
    'prophet_model', 'ProphetModel',
    'arima_model', 'ARIMAModel',
    'lstm_model', 'LSTMModel',
    'ensemble_model', 'EnsembleModel',
]
