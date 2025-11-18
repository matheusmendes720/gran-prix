"""
Data Loader and Preprocessor for Nova Corrente Demand Forecasting System
Phase 1: Setup and Data Prep
"""
import pandas as pd
import numpy as np
from datetime import datetime
import holidays
from typing import Dict, Optional, Tuple
from pathlib import Path


class DataLoader:
    """
    Load and preprocess demand data with external feature engineering.
    """
    
    def __init__(self, external_features: bool = True):
        """
        Initialize DataLoader.
        
        Parameters:
        -----------
        external_features : bool
            Whether to include external features (temperature, holidays, etc.)
        """
        self.external_features = external_features
        self.br_holidays = holidays.BR()
        self.processed_data = {}
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load CSV/Excel file.
        
        Parameters:
        -----------
        file_path : str
            Path to data file
        
        Returns:
        --------
        pd.DataFrame
            Loaded dataframe
        """
        path = Path(file_path)
        
        if path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif path.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        # Ensure date column exists
        date_cols = ['date', 'Date', 'DATE', 'dt', 'datetime']
        for col in date_cols:
            if col in df.columns:
                df['date'] = pd.to_datetime(df[col])
                break
        
        if 'date' not in df.columns:
            raise ValueError("No date column found. Expected: date, Date, DATE, dt, or datetime")
        
        df.sort_values('date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer temporal and cyclical features.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe with 'date' column
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with engineered features
        """
        df = df.copy()
        
        # Temporal features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['weekday'] = df['date'].dt.weekday
        df['weekend'] = df['weekday'].apply(lambda x: 1 if x >= 5 else 0)
        df['day_of_year'] = df['date'].dt.dayofyear
        df['week_of_year'] = df['date'].dt.isocalendar().week
        
        # Cyclical encoding for month (sin/cos)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Cyclical encoding for day of year
        df['day_of_year_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365.25)
        df['day_of_year_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365.25)
        
        # Holidays (Brazil-specific)
        df['holiday'] = df['date'].apply(lambda x: 1 if x in self.br_holidays else 0)
        
        # Lag features (previous day, week)
        if 'Quantity_Consumed' in df.columns:
            df['demand_lag_1'] = df['Quantity_Consumed'].shift(1)
            df['demand_lag_7'] = df['Quantity_Consumed'].shift(7)
            df['demand_lag_30'] = df['Quantity_Consumed'].shift(30)
            
            # Rolling statistics
            df['demand_rolling_mean_7'] = df['Quantity_Consumed'].rolling(window=7, min_periods=1).mean()
            df['demand_rolling_mean_30'] = df['Quantity_Consumed'].rolling(window=30, min_periods=1).mean()
            df['demand_rolling_std_7'] = df['Quantity_Consumed'].rolling(window=7, min_periods=1).std()
        
        # External features (simulated - replace with API calls in production)
        if self.external_features:
            df = self._add_external_features(df)
        
        return df
    
    def _add_external_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add external features (temperature, economic indicators).
        
        Note: In production, replace with actual API calls to:
        - OpenWeather API for temperature
        - IBGE API for economic data
        - ANATEL API for telecom indicators
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with external features
        """
        np.random.seed(42)  # For reproducibility
        
        # Simulate temperature (Brazil range: 15-40°C)
        df['temperature'] = np.random.uniform(15, 40, len(df))
        
        # Simulate economic indicators
        df['inflation'] = np.random.uniform(3, 6, len(df))  # % inflation
        df['gdp_growth'] = np.random.uniform(-2, 5, len(df))  # % GDP growth
        
        # Seasonal temperature variation
        df['temperature'] = df['temperature'] + 5 * np.sin(2 * np.pi * df['month'] / 12)
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values using forward fill for time series.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with missing values handled
        """
        df = df.copy()
        
        # Forward fill for time series data
        df.fillna(method='ffill', inplace=True)
        
        # If still missing, backward fill
        df.fillna(method='bfill', inplace=True)
        
        # If still missing (first/last rows), fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isna().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        return df
    
    def validate_data(self, df: pd.DataFrame, min_months: int = 18) -> Tuple[bool, str]:
        """
        Validate data quality and completeness.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        min_months : int
            Minimum months of data required
        
        Returns:
        --------
        Tuple[bool, str]
            (is_valid, message)
        """
        # Check date range
        date_range = (df['date'].max() - df['date'].min()).days
        months = date_range / 30.44
        
        if months < min_months:
            return False, f"Insufficient data: {months:.1f} months (minimum: {min_months})"
        
        # Check required columns
        required_cols = ['date']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            return False, f"Missing required columns: {missing}"
        
        # Check for Quantity_Consumed or target variable
        target_cols = ['Quantity_Consumed', 'quantity', 'demand', 'consumption']
        if not any(col in df.columns for col in target_cols):
            return False, f"No target variable found. Expected one of: {target_cols}"
        
        # Check for missing dates
        expected_dates = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
        missing_dates = set(expected_dates) - set(df['date'])
        if len(missing_dates) > 0.1 * len(expected_dates):  # More than 10% missing
            return False, f"Too many missing dates: {len(missing_dates)}"
        
        return True, "Data validation passed"
    
    def load_and_preprocess(self, file_path: str, 
                           group_by_item: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Complete pipeline: load, engineer features, handle missing values.
        
        Parameters:
        -----------
        file_path : str
            Path to data file
        group_by_item : bool
            Whether to group by Item_ID
        
        Returns:
        --------
        Dict[str, pd.DataFrame]
            Dictionary of {item_id: processed_dataframe}
        """
        # Load data
        df = self.load_data(file_path)
        
        # Validate
        is_valid, message = self.validate_data(df)
        if not is_valid:
            raise ValueError(f"Data validation failed: {message}")
        
        # Engineer features
        df = self.engineer_features(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Group by item if requested
        if group_by_item and 'Item_ID' in df.columns:
            grouped = df.groupby('Item_ID')
            result = {}
            for item_id, item_df in grouped:
                item_df = item_df.set_index('date').sort_index()
                result[item_id] = item_df
            return result
        else:
            # Return single dataframe
            df = df.set_index('date').sort_index()
            return {'all_items': df}
    
    def split_train_test(self, df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Time-based train-test split.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe (indexed by date)
        test_size : float
            Proportion of data for testing (last test_size% of dates)
        
        Returns:
        --------
        Tuple[pd.DataFrame, pd.DataFrame]
            (train_df, test_df)
        """
        split_idx = int(len(df) * (1 - test_size))
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]
        
        return train_df, test_df


# Example usage
if __name__ == "__main__":
    # Initialize loader
    loader = DataLoader(external_features=True)
    
    # Example: Create sample data for testing
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
    sample_data = pd.DataFrame({
        'date': dates,
        'Item_ID': ['CONN-001'] * len(dates),
        'Quantity_Consumed': np.random.poisson(8, len(dates)) + 
                            np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 2,
        'Site_ID': ['SITE-001'] * len(dates),
        'Lead_Time': [14] * len(dates)
    })
    
    # Save sample data
    sample_data.to_csv('sample_demand_data.csv', index=False)
    print("Sample data created: sample_demand_data.csv")
    
    # Load and preprocess
    try:
        data_dict = loader.load_and_preprocess('sample_demand_data.csv')
        print(f"\nLoaded {len(data_dict)} items")
        for item_id, item_df in data_dict.items():
            print(f"\n{item_id}:")
            print(f"  Date range: {item_df.index.min()} to {item_df.index.max()}")
            print(f"  Total records: {len(item_df)}")
            print(f"  Columns: {list(item_df.columns)}")
    except Exception as e:
        print(f"Error: {e}")

