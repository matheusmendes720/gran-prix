"""
Data loading and preprocessing module for demand forecasting.
Handles CSV/Excel ingestion, feature engineering, and data validation.
"""
import pandas as pd
import numpy as np
from datetime import datetime
import holidays
from typing import Dict, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """Handles data loading and preprocessing for demand forecasting."""
    
    def __init__(self, file_path: str, country: str = 'BR'):
        """
        Initialize data loader.
        
        Args:
            file_path: Path to CSV/Excel file
            country: Country code for holidays (default: 'BR' for Brazil)
        """
        self.file_path = file_path
        self.country = country
        
        # Initialize holidays
        if hasattr(holidays, 'country_holidays'):
            self.country_holidays = holidays.country_holidays(country)
        else:
            self.country_holidays = holidays.BR()
        
        self.processed_data: Optional[Dict] = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV/Excel file.
        
        Returns:
            DataFrame with loaded data
        
        Raises:
            ValueError: If file format is unsupported or date column missing
        """
        try:
            if self.file_path.endswith('.csv'):
                df = pd.read_csv(self.file_path)
            elif self.file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(self.file_path)
            else:
                raise ValueError(f"Unsupported file format: {self.file_path}")
            
            # Ensure date column exists and is datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            elif 'Date' in df.columns:
                df['date'] = pd.to_datetime(df['Date'])
                df = df.rename(columns={'Date': 'date'})
            else:
                raise ValueError("Date column not found. Expected 'date' or 'Date'")
            
            df.sort_values('date', inplace=True)
            df.reset_index(drop=True, inplace=True)
            
            return df
        
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def engineer_features(self, df: pd.DataFrame, external_features: bool = True) -> pd.DataFrame:
        """
        Engineer time-based and external features.
        
        Args:
            df: Input DataFrame
            external_features: Whether to include external features (weather, economic)
        
        Returns:
            DataFrame with engineered features
        """
        df = df.copy()
        
        # Temporal features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['weekday'] = df['date'].dt.weekday
        df['weekend'] = df['weekday'].apply(lambda x: 1 if x >= 5 else 0)
        df['quarter'] = df['date'].dt.quarter
        
        # Week of year
        try:
            df['week_of_year'] = df['date'].dt.isocalendar().week
        except AttributeError:
            # Fallback for older pandas
            df['week_of_year'] = df['date'].dt.week
        
        # Cyclical encoding for seasonality
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['day_sin'] = np.sin(2 * np.pi * df['day'] / 31)
        df['day_cos'] = np.cos(2 * np.pi * df['day'] / 31)
        
        # Holidays
        df['holiday'] = df['date'].apply(lambda x: 1 if x in self.country_holidays else 0)
        
        # Lag features (useful for models)
        quantity_col = None
        for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
            if col in df.columns:
                quantity_col = col
                break
        
        if quantity_col is None and len(df.select_dtypes(include=[np.number]).columns) > 0:
            # Use first numeric column
            quantity_col = df.select_dtypes(include=[np.number]).columns[0]
        
        if quantity_col:
            df[f'{quantity_col}_lag1'] = df[quantity_col].shift(1)
            df[f'{quantity_col}_lag7'] = df[quantity_col].shift(7)
            df[f'{quantity_col}_lag30'] = df[quantity_col].shift(30)
            
            # Rolling statistics
            df[f'{quantity_col}_rolling_mean_7'] = df[quantity_col].rolling(window=7, min_periods=1).mean()
            df[f'{quantity_col}_rolling_mean_30'] = df[quantity_col].rolling(window=30, min_periods=1).mean()
            df[f'{quantity_col}_rolling_std_7'] = df[quantity_col].rolling(window=7, min_periods=1).std()
        
        if external_features:
            # External features placeholder (integrate with APIs later)
            np.random.seed(42)  # For reproducibility
            df['temperature'] = np.random.uniform(20, 35, len(df))
            df['inflation'] = np.random.uniform(3, 6, len(df))
            # TODO: Integrate OpenWeather API for temperature
            # TODO: Integrate IBGE API for inflation data
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isna().any():
                # Try forward fill, then backward fill, then zero
                df[col] = df[col].fillna(method='ffill').fillna(method='bfill').fillna(0)
        
        return df
    
    def preprocess(self, external_features: bool = True, min_years: int = 2) -> Dict[str, pd.DataFrame]:
        """
        Load and preprocess data, returning dictionary grouped by Item_ID.
        
        Args:
            external_features: Whether to include external features
            min_years: Minimum years of data required
        
        Returns:
            Dictionary with Item_ID as keys and preprocessed DataFrames as values
        
        Raises:
            ValueError: If insufficient data or Item_ID column missing
        """
        df = self.load_data()
        
        # Validate minimum data requirement
        date_range = (df['date'].max() - df['date'].min()).days / 365.25
        if date_range < min_years:
            raise ValueError(
                f"Insufficient data: {date_range:.2f} years. Required: {min_years} years minimum."
            )
        
        # Feature engineering
        df = self.engineer_features(df, external_features)
        
        # Group by Item_ID
        if 'Item_ID' not in df.columns:
            # Check alternative column names
            if 'item_id' in df.columns:
                df['Item_ID'] = df['item_id']
            elif 'ItemId' in df.columns:
                df['Item_ID'] = df['ItemId']
            else:
                raise ValueError(
                    "Item_ID column not found. Required for multi-item forecasting. "
                    "Expected 'Item_ID', 'item_id', or 'ItemId'"
                )
        
        grouped = df.groupby('Item_ID')
        processed_dict = {}
        
        for item_id, group_df in grouped:
            group_df = group_df.set_index('date').sort_index()
            # Ensure continuous date index
            date_range = pd.date_range(
                start=group_df.index.min(),
                end=group_df.index.max(),
                freq='D'
            )
            group_df = group_df.reindex(date_range, method='ffill')
            processed_dict[item_id] = group_df
        
        self.processed_data = processed_dict
        return processed_dict
    
    def train_test_split(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into train and test sets based on time.
        
        Args:
            df: DataFrame to split
            test_size: Proportion of data for testing (default 0.2)
        
        Returns:
            Tuple of (train, test) DataFrames
        """
        split_idx = int(len(df) * (1 - test_size))
        train = df.iloc[:split_idx]
        test = df.iloc[split_idx:]
        return train, test

