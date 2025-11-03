"""
Prophet model service for Nova Corrente
Prophet with Brazilian holiday regressors
"""
from typing import Dict, Any, List, Optional, Tuple
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np

from backend.config.ml_config import PROPHET_CONFIG
from backend.services.ml_models.model_registry import model_registry
from backend.services.feature_engineering.external_features import external_feature_extractor
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.ml_models.prophet')


class ProphetModel:
    """
    Prophet forecasting model with Brazilian holidays
    """
    
    def __init__(self):
        """Initialize Prophet model"""
        self.model = None
        self.config = PROPHET_CONFIG
    
    def _get_brazilian_holidays(self) -> pd.DataFrame:
        """
        Get Brazilian holidays for Prophet
        
        Returns:
            DataFrame with holidays
        """
        try:
            from backend.services.database_service import db_service
            
            query = """
                SELECT data_referencia as ds, nome_feriado as holiday
                FROM CalendarioBrasil
                WHERE is_feriado = TRUE
            """
            
            result = db_service.execute_query(query)
            
            if result:
                df = pd.DataFrame(result)
                df['ds'] = pd.to_datetime(df['ds'])
                return df
            
            return pd.DataFrame(columns=['ds', 'holiday'])
        except Exception as e:
            logger.warning(f"Error getting Brazilian holidays: {e}")
            return pd.DataFrame(columns=['ds', 'holiday'])
    
    def train(
        self,
        data: pd.DataFrame,
        date_column: str = 'ds',
        value_column: str = 'y',
        external_regressors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Train Prophet model
        
        Args:
            data: DataFrame with date and value columns
            date_column: Name of date column
            value_column: Name of value column
            external_regressors: Optional list of external regressor column names
        
        Returns:
            Dictionary with training results and metrics
        """
        try:
            from prophet import Prophet
            
            # Prepare data
            df = data[[date_column, value_column]].copy()
            df.columns = ['ds', 'y']
            df['ds'] = pd.to_datetime(df['ds'])
            df = df.sort_values('ds')
            
            # Get Brazilian holidays
            holidays = self._get_brazilian_holidays()
            
            # Initialize Prophet
            self.model = Prophet(
                yearly_seasonality=self.config['yearly_seasonality'],
                weekly_seasonality=self.config['weekly_seasonality'],
                daily_seasonality=self.config['daily_seasonality'],
                seasonality_mode=self.config['seasonality_mode'],
                growth=self.config['growth'],
                changepoint_prior_scale=self.config['changepoint_prior_scale'],
                holidays=holidays if not holidays.empty else None,
            )
            
            # Add external regressors
            if external_regressors:
                for regressor in external_regressors:
                    if regressor in data.columns:
                        df[regressor] = data[regressor].values
                        self.model.add_regressor(regressor)
            
            # Fit model
            self.model.fit(df)
            
            logger.info("Prophet model trained successfully")
            
            return {
                'status': 'success',
                'model': self.model,
            }
        except ImportError:
            logger.error("Prophet (fbprophet) not installed. Install with: pip install prophet")
            raise
        except Exception as e:
            logger.error(f"Error training Prophet model: {e}")
            raise
    
    def predict(
        self,
        periods: int = 30,
        external_regressors: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Generate predictions
        
        Args:
            periods: Number of periods to forecast
            external_regressors: Optional DataFrame with external regressor values
        
        Returns:
            DataFrame with predictions and confidence intervals
        """
        try:
            if self.model is None:
                raise ValueError("Model not trained. Call train() first.")
            
            from prophet import Prophet
            
            # Create future DataFrame
            future = self.model.make_future_dataframe(periods=periods)
            
            # Add external regressors if provided
            if external_regressors is not None:
                for col in external_regressors.columns:
                    if col != 'ds':
                        # Merge external regressors
                        future = future.merge(
                            external_regressors[['ds', col]],
                            on='ds',
                            how='left'
                        )
            
            # Predict
            forecast = self.model.predict(future)
            
            logger.info(f"Generated {periods} period forecast")
            
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
        except Exception as e:
            logger.error(f"Error generating Prophet predictions: {e}")
            raise
    
    def evaluate(
        self,
        test_data: pd.DataFrame,
        date_column: str = 'ds',
        value_column: str = 'y'
    ) -> Dict[str, float]:
        """
        Evaluate model on test data
        
        Args:
            test_data: Test DataFrame
            date_column: Name of date column
            value_column: Name of value column
        
        Returns:
            Dictionary with evaluation metrics
        """
        try:
            if self.model is None:
                raise ValueError("Model not trained. Call train() first.")
            
            # Prepare test data
            test_df = test_data[[date_column, value_column]].copy()
            test_df.columns = ['ds', 'y']
            test_df['ds'] = pd.to_datetime(test_df['ds'])
            
            # Generate predictions for test period
            forecast = self.model.predict(test_df[['ds']])
            
            # Merge actual values
            merged = forecast.merge(test_df, on='ds', how='inner')
            
            # Calculate metrics
            y_true = merged['y'].values
            y_pred = merged['yhat'].values
            
            # Remove NaN values
            mask = ~(np.isnan(y_true) | np.isnan(y_pred))
            y_true = y_true[mask]
            y_pred = y_pred[mask]
            
            if len(y_true) == 0:
                return {
                    'mape': float('inf'),
                    'rmse': float('inf'),
                    'mae': float('inf'),
                }
            
            # MAPE
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
            
            # RMSE
            rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
            
            # MAE
            mae = np.mean(np.abs(y_true - y_pred))
            
            metrics = {
                'mape': float(mape),
                'rmse': float(rmse),
                'mae': float(mae),
            }
            
            logger.info(f"Prophet evaluation metrics: {metrics}")
            
            return metrics
        except Exception as e:
            logger.error(f"Error evaluating Prophet model: {e}")
            raise


# Singleton instance
prophet_model = ProphetModel()

