"""
ARIMA model service for Nova Corrente
ARIMA/ARIMAX with external regressors
"""
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from backend.config.ml_config import ARIMA_CONFIG
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.ml_models.arima')


class ARIMAModel:
    """ARIMA/ARIMAX forecasting model"""
    
    def __init__(self):
        self.model = None
        self.config = ARIMA_CONFIG
    
    def train(self, data: pd.Series, exog: Optional[pd.DataFrame] = None, order: tuple = None) -> Dict[str, Any]:
        """Train ARIMA model"""
        try:
            from statsmodels.tsa.arima.model import ARIMA
            
            order = order or (2, 1, 2)
            
            if exog is not None:
                self.model = ARIMA(data, order=order, exog=exog).fit()
            else:
                self.model = ARIMA(data, order=order).fit()
            
            logger.info("ARIMA model trained successfully")
            return {'status': 'success', 'model': self.model}
        except Exception as e:
            logger.error(f"Error training ARIMA model: {e}")
            raise
    
    def predict(self, periods: int = 30, exog: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Generate predictions"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        try:
            forecast = self.model.forecast(steps=periods, exog=exog)
            conf_int = self.model.get_forecast(steps=periods, exog=exog).conf_int()
            
            df = pd.DataFrame({
                'yhat': forecast.values,
                'yhat_lower': conf_int.iloc[:, 0].values,
                'yhat_upper': conf_int.iloc[:, 1].values,
            })
            
            return df
        except Exception as e:
            logger.error(f"Error generating ARIMA predictions: {e}")
            raise
    
    def evaluate(self, test_data: pd.Series) -> Dict[str, float]:
        """Evaluate model"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        try:
            forecast = self.model.forecast(steps=len(test_data))
            
            y_true = test_data.values
            y_pred = forecast.values
            
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
            rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
            mae = np.mean(np.abs(y_true - y_pred))
            
            return {'mape': float(mape), 'rmse': float(rmse), 'mae': float(mae)}
        except Exception as e:
            logger.error(f"Error evaluating ARIMA model: {e}")
            raise


arima_model = ARIMAModel()

