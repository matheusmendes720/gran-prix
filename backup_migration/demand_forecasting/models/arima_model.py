"""
ARIMA/SARIMA Model Implementation for Demand Forecasting
Phase 2: Model Implementation
Based on: MachineLearningMastery, MachineLearningPlus
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from math import sqrt
from typing import Tuple, Optional, Dict
import warnings
warnings.filterwarnings('ignore')


class ARIMAForecaster:
    """
    ARIMA/SARIMA forecaster with auto-tuning.
    """
    
    def __init__(self, seasonal: bool = True, m: int = 7):
        """
        Initialize ARIMA forecaster.
        
        Parameters:
        -----------
        seasonal : bool
            Whether to use SARIMA (seasonal ARIMA)
        m : int
            Seasonal period (7 for weekly, 365 for yearly)
        """
        self.seasonal = seasonal
        self.m = m
        self.model = None
        self.fitted_model = None
        self.order = None
        self.seasonal_order = None
    
    def _check_stationarity(self, series: pd.Series) -> bool:
        """
        Check if series is stationary using ADF test.
        
        Parameters:
        -----------
        series : pd.Series
            Time series data
        
        Returns:
        --------
        bool
            True if stationary (p < 0.05)
        """
        from statsmodels.tsa.stattools import adfuller
        
        result = adfuller(series.dropna())
        p_value = result[1]
        
        return p_value < 0.05
    
    def auto_select_order(self, series: pd.Series, max_p: int = 5, max_q: int = 5,
                         max_P: int = 2, max_Q: int = 2, seasonal: Optional[bool] = None) -> Tuple[Tuple, Optional[Tuple]]:
        """
        Automatically select ARIMA order using pmdarima.
        
        Parameters:
        -----------
        series : pd.Series
            Time series data
        max_p, max_q : int
            Maximum AR and MA orders
        max_P, max_Q : int
            Maximum seasonal AR and MA orders
        seasonal : Optional[bool]
            Whether to use seasonal (None = use self.seasonal)
        
        Returns:
        --------
        Tuple[Tuple, Optional[Tuple]]
            (order, seasonal_order)
        """
        if seasonal is None:
            seasonal = self.seasonal
        
        try:
            model_auto = auto_arima(
                series,
                seasonal=seasonal,
                m=self.m if seasonal else 1,
                start_p=0, start_q=0,
                max_p=max_p, max_q=max_q,
                start_P=0, start_Q=0,
                max_P=max_P, max_Q=max_Q,
                d=None,  # Auto-select differencing
                D=1 if seasonal else None,
                trace=False,
                error_action='ignore',
                suppress_warnings=True,
                stepwise=True
            )
            
            order = model_auto.order
            seasonal_order = model_auto.seasonal_order if seasonal else None
            
            return order, seasonal_order
            
        except Exception as e:
            print(f"Auto-ARIMA failed: {e}. Using default order (1,1,1)")
            return (1, 1, 1), (1, 1, 1, self.m) if seasonal else None
    
    def fit(self, series: pd.Series, exog: Optional[pd.DataFrame] = None,
            order: Optional[Tuple] = None, seasonal_order: Optional[Tuple] = None) -> Dict:
        """
        Fit ARIMA/SARIMA model.
        
        Parameters:
        -----------
        series : pd.Series
            Time series data
        exog : Optional[pd.DataFrame]
            Exogenous variables
        order : Optional[Tuple]
            ARIMA order (p, d, q). If None, auto-select
        seasonal_order : Optional[Tuple]
            Seasonal order (P, D, Q, m). If None, auto-select
        
        Returns:
        --------
        Dict
            Model information
        """
        # Auto-select order if not provided
        if order is None:
            order, seasonal_order = self.auto_select_order(series)
        
        self.order = order
        self.seasonal_order = seasonal_order
        
        # Create model
        if self.seasonal and seasonal_order:
            self.model = SARIMAX(
                series,
                order=order,
                seasonal_order=seasonal_order,
                exog=exog
            )
        else:
            self.model = ARIMA(series, order=order, exog=exog)
        
        # Fit model
        try:
            self.fitted_model = self.model.fit(disp=0)
            
            return {
                'order': order,
                'seasonal_order': seasonal_order,
                'aic': self.fitted_model.aic,
                'bic': self.fitted_model.bic,
                'summary': self.fitted_model.summary()
            }
        except Exception as e:
            raise ValueError(f"Model fitting failed: {e}")
    
    def forecast(self, steps: int = 30, exog: Optional[pd.DataFrame] = None,
                conf_int: bool = True, alpha: float = 0.05) -> pd.DataFrame:
        """
        Generate forecast.
        
        Parameters:
        -----------
        steps : int
            Number of steps ahead to forecast
        exog : Optional[pd.DataFrame]
            Future exogenous variables
        conf_int : bool
            Whether to return confidence intervals
        alpha : float
            Confidence interval level (e.g., 0.05 for 95% CI)
        
        Returns:
        --------
        pd.DataFrame
            Forecast with columns: 'forecast', 'lower', 'upper' (if conf_int)
        """
        if self.fitted_model is None:
            raise ValueError("Model must be fitted before forecasting")
        
        # Forecast
        forecast_result = self.fitted_model.forecast(
            steps=steps,
            exog=exog,
            alpha=alpha if conf_int else None
        )
        
        # Create dataframe
        if conf_int:
            forecast = pd.DataFrame({
                'forecast': forecast_result,
                'lower': self.fitted_model.get_forecast(
                    steps=steps,
                    exog=exog
                ).conf_int(alpha=alpha)['lower'],
                'upper': self.fitted_model.get_forecast(
                    steps=steps,
                    exog=exog
                ).conf_int(alpha=alpha)['upper']
            })
        else:
            forecast = pd.DataFrame({
                'forecast': forecast_result
            })
        
        return forecast
    
    def evaluate(self, test_series: pd.Series, forecast: pd.Series) -> Dict[str, float]:
        """
        Evaluate forecast performance.
        
        Parameters:
        -----------
        test_series : pd.Series
            Actual values
        forecast : pd.Series
            Forecasted values
        
        Returns:
        --------
        Dict[str, float]
            Dictionary of metrics (RMSE, MAE, MAPE)
        """
        # Align indices
        min_len = min(len(test_series), len(forecast))
        test_aligned = test_series.iloc[:min_len]
        forecast_aligned = forecast.iloc[:min_len]
        
        # Calculate metrics
        rmse = sqrt(mean_squared_error(test_aligned, forecast_aligned))
        mae = mean_absolute_error(test_aligned, forecast_aligned)
        
        # MAPE (handle division by zero)
        mape = np.mean(np.abs((test_aligned - forecast_aligned) / (test_aligned + 1e-8))) * 100
        
        return {
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape
        }


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
    trend = np.linspace(8, 12, len(dates))
    seasonal = 2 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    noise = np.random.normal(0, 1, len(dates))
    series = pd.Series(trend + seasonal + noise, index=dates)
    
    # Split train/test
    train_size = int(len(series) * 0.8)
    train_series = series.iloc[:train_size]
    test_series = series.iloc[train_size:]
    
    # Create forecaster
    forecaster = ARIMAForecaster(seasonal=True, m=7)
    
    # Fit model
    print("Fitting ARIMA model...")
    model_info = forecaster.fit(train_series)
    print(f"Order: {model_info['order']}")
    print(f"Seasonal Order: {model_info['seasonal_order']}")
    print(f"AIC: {model_info['aic']:.2f}")
    
    # Forecast
    print("\nGenerating forecast...")
    forecast_df = forecaster.forecast(steps=len(test_series))
    
    # Evaluate
    metrics = forecaster.evaluate(test_series, forecast_df['forecast'])
    print(f"\nPerformance Metrics:")
    print(f"RMSE: {metrics['RMSE']:.2f}")
    print(f"MAE: {metrics['MAE']:.2f}")
    print(f"MAPE: {metrics['MAPE']:.2f}%")
