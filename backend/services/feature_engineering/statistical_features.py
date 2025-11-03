"""
Statistical feature engineering for Nova Corrente
Lag features, moving averages, volatility
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np

from backend.config.feature_config import STATISTICAL_FEATURES
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.features.statistical')


class StatisticalFeatureExtractor:
    """
    Extract statistical features from time series
    """
    
    def extract_lag_features(
        self,
        series: pd.Series,
        lags: List[int] = None
    ) -> Dict[str, float]:
        """
        Extract lag features
        
        Args:
            series: Time series data
            lags: List of lag periods (default from config)
        
        Returns:
            Dictionary of lag feature name -> value
        """
        if lags is None:
            lags = STATISTICAL_FEATURES.get('lag_features', [1, 7, 30, 365])
        
        features = {}
        
        for lag in lags:
            if len(series) > lag:
                lag_value = series.iloc[-lag]
                features[f'lag_{lag}'] = float(lag_value) if pd.notna(lag_value) else 0.0
            else:
                features[f'lag_{lag}'] = 0.0
        
        return features
    
    def extract_moving_averages(
        self,
        series: pd.Series,
        windows: List[int] = None
    ) -> Dict[str, float]:
        """
        Extract moving average features
        
        Args:
            series: Time series data
            windows: List of window sizes (default from config)
        
        Returns:
            Dictionary of moving average feature name -> value
        """
        if windows is None:
            windows = TEMPORAL_FEATURES.get('moving_averages', [7, 30, 90])
        
        features = {}
        
        for window in windows:
            if len(series) >= window:
                ma_value = series.iloc[-window:].mean()
                features[f'ma_{window}'] = float(ma_value) if pd.notna(ma_value) else 0.0
            else:
                features[f'ma_{window}'] = float(series.mean()) if len(series) > 0 else 0.0
        
        return features
    
    def extract_volatility_features(
        self,
        series: pd.Series,
        windows: List[int] = None
    ) -> Dict[str, float]:
        """
        Extract volatility features
        
        Args:
            series: Time series data
            windows: List of window sizes (default from config)
        
        Returns:
            Dictionary of volatility feature name -> value
        """
        if windows is None:
            windows = STATISTICAL_FEATURES.get('volatility_windows', [7, 30])
        
        features = {}
        
        for window in windows:
            if len(series) >= window:
                std_value = series.iloc[-window:].std()
                features[f'std_{window}'] = float(std_value) if pd.notna(std_value) else 0.0
                
                # Coefficient of variation
                mean_value = series.iloc[-window:].mean()
                if mean_value != 0:
                    cv = std_value / mean_value
                    features[f'cv_{window}'] = float(cv) if pd.notna(cv) else 0.0
                else:
                    features[f'cv_{window}'] = 0.0
            else:
                features[f'std_{window}'] = 0.0
                features[f'cv_{window}'] = 0.0
        
        return features
    
    def extract_statistical_summary(
        self,
        series: pd.Series
    ) -> Dict[str, float]:
        """
        Extract statistical summary features
        
        Args:
            series: Time series data
        
        Returns:
            Dictionary of statistical feature name -> value
        """
        if len(series) == 0:
            return {
                'mean': 0.0,
                'median': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'skewness': 0.0,
                'kurtosis': 0.0,
            }
        
        features = {
            'mean': float(series.mean()) if pd.notna(series.mean()) else 0.0,
            'median': float(series.median()) if pd.notna(series.median()) else 0.0,
            'std': float(series.std()) if pd.notna(series.std()) else 0.0,
            'min': float(series.min()) if pd.notna(series.min()) else 0.0,
            'max': float(series.max()) if pd.notna(series.max()) else 0.0,
        }
        
        # Skewness
        if len(series) > 2:
            features['skewness'] = float(series.skew()) if pd.notna(series.skew()) else 0.0
        else:
            features['skewness'] = 0.0
        
        # Kurtosis
        if STATISTICAL_FEATURES.get('kurtosis', False) and len(series) > 3:
            features['kurtosis'] = float(series.kurtosis()) if pd.notna(series.kurtosis()) else 0.0
        
        return features
    
    def extract_all_statistical_features(
        self,
        series: pd.Series,
        include_lags: bool = True,
        include_ma: bool = True,
        include_volatility: bool = True,
        include_summary: bool = True
    ) -> Dict[str, float]:
        """
        Extract all statistical features
        
        Args:
            series: Time series data
            include_lags: Include lag features
            include_ma: Include moving averages
            include_volatility: Include volatility features
            include_summary: Include summary statistics
        
        Returns:
            Dictionary of all statistical feature name -> value
        """
        features = {}
        
        if include_lags:
            features.update(self.extract_lag_features(series))
        
        if include_ma:
            features.update(self.extract_moving_averages(series))
        
        if include_volatility:
            features.update(self.extract_volatility_features(series))
        
        if include_summary:
            features.update(self.extract_statistical_summary(series))
        
        return features


# Import for reference
from backend.config.feature_config import TEMPORAL_FEATURES

# Singleton instance
statistical_feature_extractor = StatisticalFeatureExtractor()

