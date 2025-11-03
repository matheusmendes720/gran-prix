"""
Ensemble model service for Nova Corrente
Weighted ensemble of all models
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from backend.services.ml_models.prophet_model import prophet_model
from backend.services.ml_models.arima_model import arima_model
from backend.services.ml_models.lstm_model import lstm_model
from backend.config.ml_config import ENSEMBLE_CONFIG
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.ml_models.ensemble')


class EnsembleModel:
    """Weighted ensemble of Prophet, ARIMA, and LSTM"""
    
    def __init__(self):
        self.config = ENSEMBLE_CONFIG
        self.weights = {
            'prophet': self.config['prophet_weight'],
            'arima': self.config['arima_weight'],
            'lstm': self.config['lstm_weight'],
        }
    
    def predict(
        self,
        prophet_forecast: Optional[pd.DataFrame] = None,
        arima_forecast: Optional[pd.DataFrame] = None,
        lstm_forecast: Optional[np.ndarray] = None
    ) -> pd.DataFrame:
        """Generate ensemble predictions"""
        try:
            predictions = []
            
            if prophet_forecast is not None and self.weights['prophet'] > 0:
                pred_prophet = prophet_forecast['yhat'].values * self.weights['prophet']
                lower_prophet = prophet_forecast['yhat_lower'].values * self.weights['prophet']
                upper_prophet = prophet_forecast['yhat_upper'].values * self.weights['prophet']
                predictions.append({
                    'yhat': pred_prophet,
                    'yhat_lower': lower_prophet,
                    'yhat_upper': upper_prophet,
                })
            
            if arima_forecast is not None and self.weights['arima'] > 0:
                pred_arima = arima_forecast['yhat'].values * self.weights['arima']
                lower_arima = arima_forecast['yhat_lower'].values * self.weights['arima']
                upper_arima = arima_forecast['yhat_upper'].values * self.weights['arima']
                predictions.append({
                    'yhat': pred_arima,
                    'yhat_lower': lower_arima,
                    'yhat_upper': upper_arima,
                })
            
            if lstm_forecast is not None and self.weights['lstm'] > 0:
                pred_lstm = lstm_forecast * self.weights['lstm']
                # LSTM doesn't provide confidence intervals, estimate
                std_lstm = np.std(lstm_forecast) if len(lstm_forecast) > 1 else 0
                lower_lstm = pred_lstm - 1.96 * std_lstm * self.weights['lstm']
                upper_lstm = pred_lstm + 1.96 * std_lstm * self.weights['lstm']
                predictions.append({
                    'yhat': pred_lstm,
                    'yhat_lower': lower_lstm,
                    'yhat_upper': upper_lstm,
                })
            
            if not predictions:
                raise ValueError("No model predictions provided")
            
            # Aggregate
            ensemble_yhat = np.sum([p['yhat'] for p in predictions], axis=0)
            ensemble_lower = np.min([p['yhat_lower'] for p in predictions], axis=0)
            ensemble_upper = np.max([p['yhat_upper'] for p in predictions], axis=0)
            
            df = pd.DataFrame({
                'yhat': ensemble_yhat,
                'yhat_lower': ensemble_lower,
                'yhat_upper': ensemble_upper,
            })
            
            logger.info("Generated ensemble predictions")
            return df
        except Exception as e:
            logger.error(f"Error generating ensemble predictions: {e}")
            raise


ensemble_model = EnsembleModel()

