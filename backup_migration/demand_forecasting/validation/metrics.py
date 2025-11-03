"""
Validation metrics calculation module.
Implements MAPE, RMSE, MAE, and other forecasting metrics.
"""
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, mean_absolute_error
from math import sqrt
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class ValidationMetrics:
    """Calculate validation metrics for forecasting models."""
    
    def __init__(self):
        """Initialize validation metrics calculator."""
        pass
    
    def calculate_mape(self, actual: pd.Series, predicted: pd.Series) -> float:
        """
        Calculate Mean Absolute Percentage Error (MAPE).
        
        Args:
            actual: Actual values
            predicted: Predicted values
        
        Returns:
            MAPE as percentage (0-100)
        """
        # Align series
        common_index = actual.index.intersection(predicted.index)
        actual_aligned = actual.loc[common_index]
        predicted_aligned = predicted.loc[common_index]
        
        # Handle zero or negative values
        if (actual_aligned <= 0).any():
            # Alternative MAPE calculation
            abs_error = np.abs(actual_aligned - predicted_aligned)
            denom = np.maximum(actual_aligned.abs(), 1)
            mape = np.mean(abs_error / denom) * 100
        else:
            try:
                mape = mean_absolute_percentage_error(actual_aligned, predicted_aligned) * 100
            except Exception:
                # Fallback calculation
                abs_error = np.abs(actual_aligned - predicted_aligned)
                denom = np.maximum(actual_aligned.abs(), 1)
                mape = np.mean(abs_error / denom) * 100
        
        return mape
    
    def calculate_rmse(self, actual: pd.Series, predicted: pd.Series) -> float:
        """
        Calculate Root Mean Squared Error (RMSE).
        
        Args:
            actual: Actual values
            predicted: Predicted values
        
        Returns:
            RMSE value
        """
        # Align series
        common_index = actual.index.intersection(predicted.index)
        actual_aligned = actual.loc[common_index]
        predicted_aligned = predicted.loc[common_index]
        
        mse = mean_squared_error(actual_aligned, predicted_aligned)
        return sqrt(mse)
    
    def calculate_mae(self, actual: pd.Series, predicted: pd.Series) -> float:
        """
        Calculate Mean Absolute Error (MAE).
        
        Args:
            actual: Actual values
            predicted: Predicted values
        
        Returns:
            MAE value
        """
        # Align series
        common_index = actual.index.intersection(predicted.index)
        actual_aligned = actual.loc[common_index]
        predicted_aligned = predicted.loc[common_index]
        
        return mean_absolute_error(actual_aligned, predicted_aligned)
    
    def calculate_r2(self, actual: pd.Series, predicted: pd.Series) -> float:
        """
        Calculate R-squared (coefficient of determination).
        
        Args:
            actual: Actual values
            predicted: Predicted values
        
        Returns:
            R² value (can be negative)
        """
        # Align series
        common_index = actual.index.intersection(predicted.index)
        actual_aligned = actual.loc[common_index]
        predicted_aligned = predicted.loc[common_index]
        
        ss_res = np.sum((actual_aligned - predicted_aligned) ** 2)
        ss_tot = np.sum((actual_aligned - actual_aligned.mean()) ** 2)
        
        if ss_tot == 0:
            return 0.0
        
        r2 = 1 - (ss_res / ss_tot)
        return r2
    
    def calculate_all(self, actual: pd.Series, predicted: pd.Series) -> Dict:
        """
        Calculate all validation metrics.
        
        Args:
            actual: Actual values
            predicted: Predicted values
        
        Returns:
            Dictionary with all metrics
        """
        mape = self.calculate_mape(actual, predicted)
        rmse = self.calculate_rmse(actual, predicted)
        mae = self.calculate_mae(actual, predicted)
        r2 = self.calculate_r2(actual, predicted)
        
        # Additional metrics
        # Mean Error (bias)
        common_index = actual.index.intersection(predicted.index)
        actual_aligned = actual.loc[common_index]
        predicted_aligned = predicted.loc[common_index]
        mean_error = np.mean(predicted_aligned - actual_aligned)
        
        # Symmetric MAPE
        denominator = (actual_aligned.abs() + predicted_aligned.abs()) / 2
        smape = np.mean(np.abs(actual_aligned - predicted_aligned) / 
                       np.maximum(denominator, 1)) * 100
        
        return {
            'MAPE': mape / 100,  # As fraction
            'MAPE_percent': mape,  # As percentage
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2,
            'Mean_Error': mean_error,
            'SMAPE': smape
        }

