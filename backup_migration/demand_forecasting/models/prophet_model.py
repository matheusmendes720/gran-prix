"""
Prophet Model Implementation for Demand Forecasting
Phase 2: Model Implementation
Based on: Medium Article - Time Series Forecasting
"""
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
from typing import Dict, Optional, List
import holidays


class ProphetForecaster:
    """
    Prophet forecaster with external regressors support.
    """
    
    def __init__(self, daily_seasonality: bool = True, 
                 yearly_seasonality: bool = True,
                 weekly_seasonality: bool = True):
        """
        Initialize Prophet forecaster.
        
        Parameters:
        -----------
        daily_seasonality : bool
            Whether to model daily seasonality
        yearly_seasonality : bool
            Whether to model yearly seasonality
        weekly_seasonality : bool
            Whether to model weekly seasonality
        """
        self.daily_seasonality = daily_seasonality
        self.yearly_seasonality = yearly_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.model = None
        self.regressors = []
        self.br_holidays = holidays.BR()
    
    def prepare_data(self, df: pd.DataFrame, 
                    target_col: str = 'Quantity_Consumed') -> pd.DataFrame:
        """
        Prepare data for Prophet format.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe (date-indexed or with 'date' column)
        target_col : str
            Name of target column
        
        Returns:
        --------
        pd.DataFrame
            Prophet-formatted dataframe
        """
        prophet_df = df.reset_index().copy()
        
        # Ensure date column
        if 'date' in prophet_df.columns:
            prophet_df['ds'] = pd.to_datetime(prophet_df['date'])
        elif 'ds' in prophet_df.columns:
            prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])
        else:
            raise ValueError("No date column found. Expected 'date' or 'ds'")
        
        # Ensure target column
        if target_col in prophet_df.columns:
            prophet_df['y'] = prophet_df[target_col]
        elif 'y' in prophet_df.columns:
            pass  # Already named 'y'
        else:
            raise ValueError(f"Target column '{target_col}' not found")
        
        # Select required columns
        cols = ['ds', 'y']
        
        # Add regressors if available
        regressor_cols = ['temperature', 'holiday', 'inflation', 'gdp_growth',
                         'weekend', 'month_sin', 'month_cos']
        for col in regressor_cols:
            if col in prophet_df.columns:
                cols.append(col)
                self.regressors.append(col)
        
        prophet_df = prophet_df[cols].copy()
        
        return prophet_df
    
    def fit(self, df: pd.DataFrame, target_col: str = 'Quantity_Consumed',
            holidays_df: Optional[pd.DataFrame] = None) -> Dict:
        """
        Fit Prophet model.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        target_col : str
            Name of target column
        holidays_df : Optional[pd.DataFrame]
            Custom holidays dataframe (columns: 'ds', 'holiday')
        
        Returns:
        --------
        Dict
            Model information
        """
        # Prepare data
        prophet_df = self.prepare_data(df, target_col)
        
        # Create model
        self.model = Prophet(
            daily_seasonality=self.daily_seasonality,
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            holidays=holidays_df
        )
        
        # Add regressors
        for regressor in self.regressors:
            if regressor in prophet_df.columns:
                self.model.add_regressor(regressor)
        
        # Fit model
        try:
            self.model.fit(prophet_df)
            
            return {
                'regressors': self.regressors,
                'params': self.model.params
            }
        except Exception as e:
            raise ValueError(f"Model fitting failed: {e}")
    
    def forecast(self, periods: int = 30, 
                future_exog: Optional[pd.DataFrame] = None,
                freq: str = 'D') -> pd.DataFrame:
        """
        Generate forecast.
        
        Parameters:
        -----------
        periods : int
            Number of periods to forecast
        future_exog : Optional[pd.DataFrame]
            Future exogenous variables (date-indexed)
        freq : str
            Frequency string (e.g., 'D' for daily)
        
        Returns:
        --------
        pd.DataFrame
            Forecast with columns: 'ds', 'yhat', 'yhat_lower', 'yhat_upper'
        """
        if self.model is None:
            raise ValueError("Model must be fitted before forecasting")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=periods, freq=freq)
        
        # Add regressors if provided
        if future_exog is not None and len(self.regressors) > 0:
            future_exog = future_exog.reset_index()
            if 'date' in future_exog.columns:
                future_exog['ds'] = pd.to_datetime(future_exog['date'])
            
            # Merge regressors
            for regressor in self.regressors:
                if regressor in future_exog.columns:
                    future = future.merge(
                        future_exog[['ds', regressor]],
                        on='ds',
                        how='left'
                    )
                    # Fill missing with last known value
                    future[regressor].fillna(method='ffill', inplace=True)
                    future[regressor].fillna(method='bfill', inplace=True)
        
        # Predict
        forecast = self.model.predict(future)
        
        # Return only future periods
        forecast = forecast.tail(periods)
        
        # Rename for consistency
        forecast = forecast.rename(columns={
            'yhat': 'forecast',
            'yhat_lower': 'lower',
            'yhat_upper': 'upper'
        })
        
        return forecast[['ds', 'forecast', 'lower', 'upper']]
    
    def evaluate(self, test_df: pd.DataFrame, forecast_df: pd.DataFrame,
                 target_col: str = 'Quantity_Consumed') -> Dict[str, float]:
        """
        Evaluate forecast performance.
        
        Parameters:
        -----------
        test_df : pd.DataFrame
            Actual values (date-indexed or with 'date' column)
        forecast_df : pd.DataFrame
            Forecasted values
        target_col : str
            Name of target column in test_df
        
        Returns:
        --------
        Dict[str, float]
            Dictionary of metrics (RMSE, MAE, MAPE)
        """
        # Prepare test data
        test_data = test_df.reset_index()
        if 'date' in test_data.columns:
            test_data['ds'] = pd.to_datetime(test_data['date'])
        elif 'ds' in test_data.columns:
            test_data['ds'] = pd.to_datetime(test_data['ds'])
        else:
            raise ValueError("No date column found in test_df")
        
        # Get target
        if target_col in test_data.columns:
            actual = test_data[target_col]
        elif 'y' in test_data.columns:
            actual = test_data['y']
        else:
            raise ValueError(f"Target column '{target_col}' not found in test_df")
        
        # Align forecast with test data
        forecast_aligned = forecast_df.merge(
            test_data[['ds', target_col]] if target_col in test_data.columns else test_data[['ds']],
            on='ds',
            how='inner'
        )
        
        actual = test_data.set_index('ds')[target_col if target_col in test_data.columns else 'y']
        forecast_values = forecast_aligned.set_index('ds')['forecast']
        
        # Align indices
        common_idx = actual.index.intersection(forecast_values.index)
        actual_aligned = actual.loc[common_idx]
        forecast_aligned = forecast_values.loc[common_idx]
        
        # Calculate metrics
        rmse = sqrt(mean_squared_error(actual_aligned, forecast_aligned))
        mae = mean_absolute_error(actual_aligned, forecast_aligned)
        mape = np.mean(np.abs((actual_aligned - forecast_aligned) / (actual_aligned + 1e-8))) * 100
        
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
    
    # Create sample dataframe
    df = pd.DataFrame({
        'date': dates,
        'Quantity_Consumed': np.random.poisson(8, len(dates)) + 
                            2 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365),
        'temperature': np.random.uniform(15, 40, len(dates)),
        'holiday': [1 if d in holidays.BR() else 0 for d in dates]
    })
    df.set_index('date', inplace=True)
    
    # Split train/test
    train_size = int(len(df) * 0.8)
    train_df = df.iloc[:train_size]
    test_df = df.iloc[train_size:]
    
    # Create forecaster
    forecaster = ProphetForecaster()
    
    # Fit model
    print("Fitting Prophet model...")
    model_info = forecaster.fit(train_df, target_col='Quantity_Consumed')
    print(f"Regressors: {model_info['regressors']}")
    
    # Forecast
    print("\nGenerating forecast...")
    forecast_df = forecaster.forecast(periods=len(test_df))
    
    # Evaluate
    metrics = forecaster.evaluate(test_df, forecast_df, target_col='Quantity_Consumed')
    print(f"\nPerformance Metrics:")
    print(f"RMSE: {metrics['RMSE']:.2f}")
    print(f"MAE: {metrics['MAE']:.2f}")
    print(f"MAPE: {metrics['MAPE']:.2f}%")
