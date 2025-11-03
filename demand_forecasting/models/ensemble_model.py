"""
Ensemble Model for Demand Forecasting
Phase 2: Model Implementation
Combines ARIMA, Prophet, and LSTM with weighted averaging
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from .arima_model import ARIMAForecaster
from .prophet_model import ProphetForecaster
from .lstm_model import LSTMForecaster


class EnsembleForecaster:
    """
    Ensemble forecaster combining multiple models.
    """
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize ensemble forecaster.
        
        Parameters:
        -----------
        weights : Optional[Dict[str, float]]
            Weights for each model. Default: equal weights (0.33 each)
            Example: {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3}
        """
        if weights is None:
            weights = {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3}
        
        # Normalize weights
        total = sum(weights.values())
        self.weights = {k: v / total for k, v in weights.items()}
        
        self.models = {}
        self.fitted = False
    
    def add_model(self, name: str, model, weight: Optional[float] = None):
        """
        Add a model to the ensemble.
        
        Parameters:
        -----------
        name : str
            Model name (e.g., 'ARIMA', 'Prophet', 'LSTM')
        model
            Model instance
        weight : Optional[float]
            Weight for this model. If None, use default or equal weight.
        """
        self.models[name] = model
        if weight is not None:
            self.weights[name] = weight
            # Renormalize
            total = sum(self.weights.values())
            self.weights = {k: v / total for k, v in self.weights.items()}
    
    def fit(self, train_data: pd.DataFrame, target_col: str = 'Quantity_Consumed',
            series_col: Optional[str] = None) -> Dict:
        """
        Fit all models in the ensemble.
        
        Parameters:
        -----------
        train_data : pd.DataFrame
            Training dataframe
        target_col : str
            Name of target column
        series_col : Optional[str]
            If provided, extract series from this column
        
        Returns:
        --------
        Dict
            Fitting results for each model
        """
        results = {}
        
        # Prepare data
        if series_col is not None:
            series = train_data[series_col]
        else:
            series = train_data[target_col]
        
        # Fit ARIMA
        if 'ARIMA' in self.models:
            print("Fitting ARIMA model...")
            try:
                arima = self.models['ARIMA']
                if not hasattr(arima, 'fitted_model') or arima.fitted_model is None:
                    arima.fit(series)
                results['ARIMA'] = {'status': 'success'}
            except Exception as e:
                results['ARIMA'] = {'status': 'failed', 'error': str(e)}
                print(f"ARIMA fitting failed: {e}")
        
        # Fit Prophet
        if 'Prophet' in self.models:
            print("Fitting Prophet model...")
            try:
                prophet = self.models['Prophet']
                prophet.fit(train_data, target_col=target_col)
                results['Prophet'] = {'status': 'success'}
            except Exception as e:
                results['Prophet'] = {'status': 'failed', 'error': str(e)}
                print(f"Prophet fitting failed: {e}")
        
        # Fit LSTM
        if 'LSTM' in self.models:
            print("Fitting LSTM model...")
            try:
                lstm = self.models['LSTM']
                if not lstm.fitted:
                    lstm.fit(series)
                results['LSTM'] = {'status': 'success'}
            except Exception as e:
                results['LSTM'] = {'status': 'failed', 'error': str(e)}
                print(f"LSTM fitting failed: {e}")
        
        self.fitted = True
        return results
    
    def forecast(self, steps: int = 30, 
                future_exog: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Generate ensemble forecast.
        
        Parameters:
        -----------
        steps : int
            Number of steps ahead to forecast
        future_exog : Optional[pd.DataFrame]
            Future exogenous variables
        
        Returns:
        --------
        pd.DataFrame
            Ensemble forecast with columns: 'forecast', 'lower', 'upper'
        """
        if not self.fitted:
            raise ValueError("Models must be fitted before forecasting")
        
        forecasts = {}
        
        # Forecast with each model
        for name, model in self.models.items():
            try:
                if name == 'ARIMA':
                    forecast_df = model.forecast(steps=steps, 
                                                exog=future_exog if future_exog is not None else None)
                    forecasts[name] = forecast_df['forecast'].values
                    
                elif name == 'Prophet':
                    forecast_df = model.forecast(periods=steps, 
                                                future_exog=future_exog)
                    forecasts[name] = forecast_df['forecast'].values
                    
                elif name == 'LSTM':
                    forecast = model.forecast(steps=steps)
                    forecasts[name] = forecast
                    
            except Exception as e:
                print(f"Forecast failed for {name}: {e}")
                continue
        
        # Ensemble (weighted average)
        if len(forecasts) == 0:
            raise ValueError("No successful forecasts")
        
        # Align lengths
        min_len = min(len(f) for f in forecasts.values())
        forecasts_aligned = {k: v[:min_len] for k, v in forecasts.items()}
        
        # Weighted average
        ensemble_forecast = np.zeros(min_len)
        ensemble_lower = np.zeros(min_len)
        ensemble_upper = np.zeros(min_len)
        
        total_weight = 0
        
        for name, forecast_values in forecasts_aligned.items():
            weight = self.weights.get(name, 1.0 / len(forecasts_aligned))
            ensemble_forecast += weight * forecast_values
            total_weight += weight
            
            # For confidence intervals, use max range
            # (simplified - in production, combine properly)
            if name == 'ARIMA':
                arima_forecast = model.forecast(steps=min_len)
                ensemble_lower = np.maximum(ensemble_lower, arima_forecast['lower'].values[:min_len])
                ensemble_upper = np.maximum(ensemble_upper, arima_forecast['upper'].values[:min_len])
            elif name == 'Prophet':
                prophet_forecast = model.forecast(periods=min_len)
                ensemble_lower = np.maximum(ensemble_lower, prophet_forecast['lower'].values[:min_len])
                ensemble_upper = np.maximum(ensemble_upper, prophet_forecast['upper'].values[:min_len])
        
        # Normalize
        ensemble_forecast /= total_weight
        
        # Create dataframe
        forecast_df = pd.DataFrame({
            'forecast': ensemble_forecast,
            'lower': ensemble_lower,
            'upper': ensemble_upper
        })
        
        return forecast_df
    
    def evaluate(self, test_data: pd.DataFrame, forecast_df: pd.DataFrame,
                target_col: str = 'Quantity_Consumed') -> Dict[str, float]:
        """
        Evaluate ensemble forecast.
        
        Parameters:
        -----------
        test_data : pd.DataFrame
            Actual test data
        forecast_df : pd.DataFrame
            Forecast dataframe
        target_col : str
            Name of target column
        
        Returns:
        --------
        Dict[str, float]
            Metrics (RMSE, MAE, MAPE)
        """
        actual = test_data[target_col].values
        forecast = forecast_df['forecast'].values
        
        # Align lengths
        min_len = min(len(actual), len(forecast))
        actual_aligned = actual[:min_len]
        forecast_aligned = forecast[:min_len]
        
        # Calculate metrics
        rmse = np.sqrt(np.mean((actual_aligned - forecast_aligned) ** 2))
        mae = np.mean(np.abs(actual_aligned - forecast_aligned))
        mape = np.mean(np.abs((actual_aligned - forecast_aligned) / (actual_aligned + 1e-8))) * 100
        
        return {
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape
        }


# Example usage
if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
    series = pd.Series(
        np.random.poisson(8, len(dates)) + 2 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365),
        index=dates
    )
    
    df = pd.DataFrame({
        'date': dates,
        'Quantity_Consumed': series.values,
        'temperature': np.random.uniform(15, 40, len(dates))
    })
    df.set_index('date', inplace=True)
    
    # Split train/test
    train_size = int(len(df) * 0.8)
    train_df = df.iloc[:train_size]
    test_df = df.iloc[train_size:]
    
    # Create ensemble
    ensemble = EnsembleForecaster(weights={'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3})
    
    # Add models
    ensemble.add_model('ARIMA', ARIMAForecaster(seasonal=True, m=7))
    ensemble.add_model('Prophet', ProphetForecaster())
    ensemble.add_model('LSTM', LSTMForecaster(look_back=30))
    
    # Fit
    print("Fitting ensemble models...")
    results = ensemble.fit(train_df, target_col='Quantity_Consumed')
    print(f"Fitting results: {results}")
    
    # Forecast
    print("\nGenerating ensemble forecast...")
    forecast_df = ensemble.forecast(steps=len(test_df))
    
    # Evaluate
    metrics = ensemble.evaluate(test_df, forecast_df)
    print(f"\nEnsemble Performance Metrics:")
    print(f"RMSE: {metrics['RMSE']:.2f}")
    print(f"MAE: {metrics['MAE']:.2f}")
    print(f"MAPE: {metrics['MAPE']:.2f}%")

