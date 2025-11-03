"""
Time series data structure for Nova Corrente ML features
"""
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime, date

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.data_structures')


class TimeSeries:
    """
    Time series wrapper with indexing and temporal operations
    """
    def __init__(
        self,
        data: pd.DataFrame,
        date_column: str = 'data_referencia',
        value_column: Optional[str] = None,
        material_id: Optional[int] = None
    ):
        """
        Initialize time series
        
        Args:
            data: DataFrame with time series data
            date_column: Name of date column
            value_column: Name of value column (if single value)
            material_id: Optional material ID for context
        """
        self.data = data.copy()
        self.date_column = date_column
        self.value_column = value_column
        self.material_id = material_id
        
        # Ensure date column is datetime
        if self.date_column in self.data.columns:
            self.data[self.date_column] = pd.to_datetime(self.data[self.date_column])
            self.data = self.data.sort_values(self.date_column)
            self.data = self.data.set_index(self.date_column)
        
        logger.debug(f"TimeSeries initialized with {len(self.data)} records")
    
    @property
    def start_date(self) -> Optional[datetime]:
        """Get start date of time series"""
        if self.data.index.empty:
            return None
        return self.data.index.min()
    
    @property
    def end_date(self) -> Optional[datetime]:
        """Get end date of time series"""
        if self.data.index.empty:
            return None
        return self.data.index.max()
    
    @property
    def length(self) -> int:
        """Get length of time series"""
        return len(self.data)
    
    @property
    def frequency(self) -> str:
        """Detect frequency of time series"""
        if len(self.data) < 2:
            return 'unknown'
        
        # Calculate median time difference
        time_diffs = self.data.index.to_series().diff().dropna()
        median_diff = time_diffs.median()
        
        # Convert to frequency string
        if median_diff <= pd.Timedelta(days=1):
            return 'D'  # Daily
        elif median_diff <= pd.Timedelta(days=7):
            return 'W'  # Weekly
        elif median_diff <= pd.Timedelta(days=30):
            return 'M'  # Monthly
        else:
            return 'unknown'
    
    def get_value(self, date: datetime) -> Optional[float]:
        """
        Get value at specific date
        
        Args:
            date: Target date
        
        Returns:
            Value at date or None
        """
        try:
            # Find closest date
            if date in self.data.index:
                if self.value_column:
                    return float(self.data.loc[date, self.value_column])
                return float(self.data.loc[date].iloc[0])
            
            # Interpolate or use nearest
            nearest_idx = self.data.index.get_indexer([date], method='nearest')[0]
            if nearest_idx >= 0:
                date_nearest = self.data.index[nearest_idx]
                if self.value_column:
                    return float(self.data.loc[date_nearest, self.value_column])
                return float(self.data.loc[date_nearest].iloc[0])
            
            return None
        except Exception as e:
            logger.error(f"Error getting value for date {date}: {e}")
            return None
    
    def get_range(
        self,
        start_date: datetime,
        end_date: datetime,
        fill_method: str = 'forward'
    ) -> pd.DataFrame:
        """
        Get time series data for date range
        
        Args:
            start_date: Start date
            end_date: End date
            fill_method: Method to fill missing dates ('forward', 'backward', 'interpolate', 'none')
        
        Returns:
            DataFrame with data for range
        """
        try:
            # Create date range
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Reindex and fill
            result = self.data.reindex(date_range, method=fill_method)
            
            return result
        except Exception as e:
            logger.error(f"Error getting range: {e}")
            return pd.DataFrame()
    
    def resample(self, freq: str = 'D', method: str = 'mean') -> 'TimeSeries':
        """
        Resample time series to different frequency
        
        Args:
            freq: Target frequency ('D', 'W', 'M', etc.)
            method: Aggregation method ('mean', 'sum', 'max', 'min')
        
        Returns:
            Resampled TimeSeries
        """
        try:
            resampled = self.data.resample(freq)
            
            if method == 'mean':
                result_data = resampled.mean()
            elif method == 'sum':
                result_data = resampled.sum()
            elif method == 'max':
                result_data = resampled.max()
            elif method == 'min':
                result_data = resampled.min()
            else:
                result_data = resampled.mean()
            
            result_data = result_data.reset_index()
            return TimeSeries(
                result_data,
                date_column=self.date_column,
                value_column=self.value_column,
                material_id=self.material_id
            )
        except Exception as e:
            logger.error(f"Error resampling: {e}")
            return self
    
    def add_lag_features(self, lags: List[int]) -> pd.DataFrame:
        """
        Add lag features to time series
        
        Args:
            lags: List of lag periods (e.g., [1, 7, 30])
        
        Returns:
            DataFrame with lag features added
        """
        try:
            result = self.data.copy()
            
            if self.value_column:
                for lag in lags:
                    result[f'{self.value_column}_lag_{lag}'] = (
                        result[self.value_column].shift(lag)
                    )
            else:
                # If no specific value column, use first numeric column
                numeric_cols = result.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    base_col = numeric_cols[0]
                    for lag in lags:
                        result[f'{base_col}_lag_{lag}'] = (
                            result[base_col].shift(lag)
                        )
            
            return result
        except Exception as e:
            logger.error(f"Error adding lag features: {e}")
            return self.data
    
    def add_moving_averages(self, windows: List[int]) -> pd.DataFrame:
        """
        Add moving average features
        
        Args:
            windows: List of window sizes (e.g., [7, 30, 90])
        
        Returns:
            DataFrame with moving averages added
        """
        try:
            result = self.data.copy()
            
            if self.value_column:
                base_col = self.value_column
            else:
                numeric_cols = result.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    base_col = numeric_cols[0]
                else:
                    return result
            
            for window in windows:
                result[f'{base_col}_ma_{window}'] = (
                    result[base_col].rolling(window=window).mean()
                )
            
            return result
        except Exception as e:
            logger.error(f"Error adding moving averages: {e}")
            return self.data
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame with date as column"""
        result = self.data.copy()
        result = result.reset_index()
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'material_id': self.material_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'length': self.length,
            'frequency': self.frequency,
            'columns': list(self.data.columns),
        }

