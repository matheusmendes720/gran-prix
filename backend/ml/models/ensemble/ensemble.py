"""
Ensemble model combining ARIMA, Prophet, and LSTM forecasts.
Uses weighted average for robust predictions.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from demand_forecasting.models.arima_model import ARIMAForecaster
from demand_forecasting.models.prophet_model import ProphetForecaster
from demand_forecasting.models.lstm_model import LSTMForecaster
import warnings
warnings.filterwarnings('ignore')


class EnsembleForecaster:
    """Ensemble of ARIMA, Prophet, and LSTM models."""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None, use_lstm: bool = True):
        """
        Initialize ensemble forecaster.
        
        Args:
            weights: Dictionary of model weights (must sum to 1.0)
                    Default: {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3}
            use_lstm: Whether to use LSTM model (default: True)
        """
        if weights is None:
            if use_lstm:
                weights = {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3}
            else:
                weights = {'ARIMA': 0.5, 'Prophet': 0.5}
        
        # Validate weights sum to 1.0
        if abs(sum(weights.values()) - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {sum(weights.values())}")
        
        self.weights = weights
        self.use_lstm = use_lstm
        self.forecasters = {
            'ARIMA': ARIMAForecaster(),
            'Prophet': ProphetForecaster()
        }
        
        if use_lstm:
            try:
                self.forecasters['LSTM'] = LSTMForecaster()
            except ImportError:
                print("Warning: LSTM not available. Continuing without LSTM model.")
                self.use_lstm = False
                if 'LSTM' in self.weights:
                    # Redistribute LSTM weight
                    lstm_weight = self.weights.pop('LSTM')
                    total_remaining = sum(self.weights.values())
                    for key in self.weights:
                        self.weights[key] = self.weights[key] * (1 + lstm_weight / total_remaining)
        
        self.forecasts = {}
        self.fitted_models = {}
    
    def fit(self, df: pd.DataFrame, quantity_col: str = 'Quantity_Consumed', 
            exog: Optional[pd.DataFrame] = None) -> Dict:
        """
        Fit all models in the ensemble.
        
        Args:
            df: DataFrame with date index and quantity column
            quantity_col: Name of quantity column
            exog: External regressors (optional)
        
        Returns:
            Dictionary with fitting results for each model
        """
        series = df[quantity_col] if quantity_col in df.columns else df.iloc[:, 0]
        results = {}
        
        # Fit ARIMA
        if 'ARIMA' in self.forecasters:
            try:
                arima_result = self.forecasters['ARIMA'].auto_fit(series, exog)
                results['ARIMA'] = 'Fitted successfully'
                self.fitted_models['ARIMA'] = True
            except Exception as e:
                print(f"ARIMA fitting failed: {e}")
                results['ARIMA'] = f'Failed: {str(e)}'
                self.fitted_models['ARIMA'] = False
        
        # Fit Prophet
        if 'Prophet' in self.forecasters:
            try:
                regressors = list(exog.columns) if exog is not None and len(exog.columns) > 0 else None
                self.forecasters['Prophet'].fit(df, quantity_col, regressors)
                results['Prophet'] = 'Fitted successfully'
                self.fitted_models['Prophet'] = True
            except Exception as e:
                print(f"Prophet fitting failed: {e}")
                results['Prophet'] = f'Failed: {str(e)}'
                self.fitted_models['Prophet'] = False
        
        # Fit LSTM
        if 'LSTM' in self.forecasters and self.use_lstm:
            try:
                self.forecasters['LSTM'].fit(series)
                results['LSTM'] = 'Fitted successfully'
                self.fitted_models['LSTM'] = True
            except Exception as e:
                print(f"LSTM fitting failed: {e}")
                results['LSTM'] = f'Failed: {str(e)}'
                self.fitted_models['LSTM'] = False
        
        return results
    
    def forecast(self, steps: int = 30, df: Optional[pd.DataFrame] = None,
                 exog: Optional[pd.DataFrame] = None, quantity_col: str = 'Quantity_Consumed') -> pd.Series:
        """
        Generate ensemble forecast.
        
        Args:
            steps: Number of periods to forecast
            df: Historical DataFrame (for LSTM if needed)
            exog: Future external regressors (optional)
            quantity_col: Name of quantity column (for LSTM if needed)
        
        Returns:
            Ensemble forecast series
        
        Raises:
            ValueError: If no forecasts generated successfully
        """
        forecasts = {}
        
        # Get individual forecasts
        if 'ARIMA' in self.forecasters and self.fitted_models.get('ARIMA', False):
            try:
                arima_fc = self.forecasters['ARIMA'].forecast(steps, exog)
                forecasts['ARIMA'] = arima_fc.values if isinstance(arima_fc, pd.Series) else arima_fc
            except Exception as e:
                print(f"ARIMA forecast failed: {e}")
        
        if 'Prophet' in self.forecasters and self.fitted_models.get('Prophet', False):
            try:
                prophet_fc = self.forecasters['Prophet'].forecast(steps, regressors=exog)
                forecasts['Prophet'] = prophet_fc['yhat'].values
            except Exception as e:
                print(f"Prophet forecast failed: {e}")
        
        if 'LSTM' in self.forecasters and self.use_lstm and self.fitted_models.get('LSTM', False):
            try:
                if df is not None:
                    series = df[quantity_col] if quantity_col in df.columns else df.iloc[:, 0]
                    lstm_fc = self.forecasters['LSTM'].forecast(series, steps)
                    forecasts['LSTM'] = lstm_fc
                else:
                    print("Warning: LSTM requires historical data. Skipping LSTM forecast.")
            except Exception as e:
                print(f"LSTM forecast failed: {e}")
        
        if not forecasts:
            raise ValueError("No forecasts generated successfully. Check model fitting.")
        
        # Align lengths (take minimum length)
        min_length = min(len(fc) for fc in forecasts.values())
        for key in forecasts:
            forecasts[key] = forecasts[key][:min_length]
        
        # Weighted ensemble
        ensemble_fc = np.zeros(min_length)
        total_weight = 0
        
        for model_name, forecast in forecasts.items():
            if model_name in self.weights and self.fitted_models.get(model_name, False):
                weight = self.weights[model_name]
                ensemble_fc += forecast * weight
                total_weight += weight
        
        # Normalize if weights don't match available models
        if total_weight > 0:
            ensemble_fc = ensemble_fc / total_weight
        else:
            # Fallback: simple average
            ensemble_fc = np.mean([forecasts[k] for k in forecasts], axis=0)
        
        # Store individual forecasts for analysis
        self.forecasts = forecasts
        
        return pd.Series(ensemble_fc, name='Ensemble_Forecast')

