#!/usr/bin/env python3
"""
Data Preprocessing Script for Nova Corrente Demand Forecasting System
Standardizes and cleans datasets from multiple sources
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Setup logging
project_root = Path(__file__).parent.parent.parent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(project_root / 'data' / 'processed' / 'preprocessing_log.txt')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatasetPreprocessor:
    """Preprocess and standardize datasets"""
    
    def __init__(self, config_path: str = None):
        # Get project root (2 levels up from src/pipeline)
        project_root = Path(__file__).parent.parent.parent
        if config_path is None:
            config_path = str(project_root / "config" / "datasets_config.json")
        else:
            # If relative path, make it relative to project root
            if not Path(config_path).is_absolute():
                config_path = str(project_root / config_path)
        self.config_path = config_path
        self.project_root = project_root
        self.raw_data_dir = project_root / "data" / "raw"
        self.processed_data_dir = project_root / "data" / "processed"
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.unified_schema = self.config.get('unified_schema', {})
        self.preprocessing_config = self.config.get('preprocessing', {})
    
    def find_data_files(self, dataset_dir: Path) -> List[Path]:
        """Find all data files (CSV, Excel, Parquet) in directory"""
        data_files = []
        extensions = ['.csv', '.xlsx', '.xls', '.parquet', '.json']
        
        for ext in extensions:
            data_files.extend(dataset_dir.rglob(f'*{ext}'))
        
        return sorted(data_files)
    
    def load_dataset(self, dataset_id: str, dataset_info: Dict) -> Optional[pd.DataFrame]:
        """Load dataset from raw data directory"""
        dataset_dir = self.raw_data_dir / dataset_id
        
        if not dataset_dir.exists():
            logger.warning(f"Dataset directory not found: {dataset_dir}")
            return None
        
        data_files = self.find_data_files(dataset_dir)
        
        if not data_files:
            logger.warning(f"No data files found in {dataset_dir}")
            return None
        
        # Try to load the first suitable file
        for file_path in data_files:
            try:
                logger.info(f"Attempting to load: {file_path}")
                
                if file_path.suffix == '.csv':
                    # Try comma separator first, then semicolon
                    try:
                        df = pd.read_csv(file_path, encoding='utf-8', low_memory=False, sep=',')
                    except Exception:
                        logger.info(f"Comma separator failed, trying semicolon...")
                        df = pd.read_csv(file_path, encoding='utf-8', low_memory=False, sep=';')
                elif file_path.suffix in ['.xlsx', '.xls']:
                    df = pd.read_excel(file_path)
                elif file_path.suffix == '.parquet':
                    df = pd.read_parquet(file_path)
                elif file_path.suffix == '.json':
                    df = pd.read_json(file_path)
                else:
                    continue
                
                logger.info(f"Successfully loaded {file_path.name}: {len(df)} rows, {len(df.columns)} columns")
                return df
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")
                continue
        
        return None
    
    def standardize_date_column(self, df: pd.DataFrame, date_col: str, dataset_id: str = None) -> pd.DataFrame:
        """Standardize date column format"""
        if date_col not in df.columns:
            logger.warning(f"Date column '{date_col}' not found")
            return df
        
        try:
            # Special handling for Zenodo dataset where date comes from 'step' (numeric index)
            if dataset_id == 'zenodo_milan_telecom' and pd.api.types.is_numeric_dtype(df[date_col]):
                # Convert step (0, 1, 2...) to datetime starting from a base date
                # Original period: Nov 2013 - Jan 2014 (~60 days, but we have 116K steps)
                # Steps are likely in smaller units (minutes/seconds), not days
                # Use a base date and treat steps as minutes (1 step = 1 minute)
                base_date = pd.to_datetime('2013-11-01')
                # Use nanoseconds precision to avoid overflow
                df[date_col] = base_date + pd.to_timedelta(df[date_col].astype('int64'), unit='m')
                logger.info(f"Converted numeric step to datetime for {dataset_id}, base: {base_date}, unit: minutes")
            else:
                # Try to parse as datetime
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            
            # Remove rows with invalid dates
            initial_count = len(df)
            df = df.dropna(subset=[date_col])
            if len(df) < initial_count:
                logger.warning(f"Removed {initial_count - len(df)} rows with invalid dates")
            
            df = df.sort_values(date_col)
            logger.info(f"Standardized date column: {date_col}")
        except Exception as e:
            logger.error(f"Error standardizing date column: {e}")
        
        return df
    
    def map_columns(self, df: pd.DataFrame, mapping: Dict) -> pd.DataFrame:
        """Map dataset columns to unified schema"""
        df_mapped = df.copy()
        
        # Rename columns according to mapping
        rename_dict = {}
        for unified_col, source_col in mapping.items():
            if source_col and source_col in df.columns:
                rename_dict[source_col] = unified_col
            elif source_col is None:
                # Column doesn't exist in source, will be added later
                pass
        
        df_mapped = df_mapped.rename(columns=rename_dict)
        logger.info(f"Mapped columns: {rename_dict}")
        
        return df_mapped
    
    def add_missing_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add missing required columns with default values"""
        required_cols = self.unified_schema.get('required_columns', [])
        
        for col in required_cols:
            if col not in df.columns:
                if col == 'date':
                    logger.error("Date column is required but missing!")
                    continue
                elif col in ['item_name', 'site_id', 'category']:
                    df[col] = 'unknown'
                elif col in ['quantity', 'cost']:
                    df[col] = 0.0
                elif col == 'lead_time':
                    df[col] = 14  # Default lead time
                else:
                    df[col] = None
                
                logger.info(f"Added missing column '{col}' with default value")
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer time-based features"""
        if 'date' not in df.columns:
            logger.warning("Date column missing, skipping feature engineering")
            return df
        
        try:
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['day'] = df['date'].dt.day
            df['weekday'] = df['date'].dt.weekday
            df['weekend'] = (df['weekday'] >= 5).astype(int)
            df['quarter'] = df['date'].dt.quarter
            
            # Cyclical encoding for month
            df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
            df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
            
            # Day of year
            df['day_of_year'] = df['date'].dt.dayofyear
            
            logger.info("Engineered time-based features")
        except Exception as e:
            logger.error(f"Error engineering features: {e}")
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values according to config"""
        method = self.preprocessing_config.get('fill_missing', 'forward_fill')
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        if method == 'forward_fill':
            df[numeric_cols] = df[numeric_cols].fillna(method='ffill').fillna(0)
            df[categorical_cols] = df[categorical_cols].fillna(method='ffill').fillna('unknown')
        elif method == 'backward_fill':
            df[numeric_cols] = df[numeric_cols].fillna(method='bfill').fillna(0)
            df[categorical_cols] = df[categorical_cols].fillna(method='bfill').fillna('unknown')
        elif method == 'mean':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            df[categorical_cols] = df[categorical_cols].fillna('unknown')
        else:
            df = df.dropna()
        
        logger.info(f"Handled missing values using method: {method}")
        return df
    
    def remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove outliers using IQR method"""
        if 'quantity' not in df.columns:
            return df
        
        try:
            Q1 = df['quantity'].quantile(0.25)
            Q3 = df['quantity'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            initial_count = len(df)
            df = df[(df['quantity'] >= lower_bound) & (df['quantity'] <= upper_bound)]
            removed = initial_count - len(df)
            
            if removed > 0:
                logger.info(f"Removed {removed} outliers using IQR method")
        except Exception as e:
            logger.warning(f"Error removing outliers: {e}")
        
        return df
    
    def aggregate_to_daily(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate data to daily level"""
        if 'date' not in df.columns or 'quantity' not in df.columns:
            logger.warning("Cannot aggregate: missing date or quantity columns")
            return df
        
        # Group by date and item (and site if available)
        group_cols = ['date']
        if 'item_id' in df.columns:
            group_cols.append('item_id')
        if 'site_id' in df.columns:
            group_cols.append('site_id')
        
        # Aggregate quantities
        agg_dict = {'quantity': 'sum'}
        if 'cost' in df.columns:
            agg_dict['cost'] = 'sum'
        if 'lead_time' in df.columns:
            agg_dict['lead_time'] = 'first'  # Keep lead_time (should be constant per item)
        
        # Keep first value for categorical columns
        categorical_cols = ['item_name', 'category', 'site_id']
        for col in categorical_cols:
            if col in df.columns:
                agg_dict[col] = 'first'
        
        df_daily = df.groupby(group_cols, as_index=False).agg(agg_dict)
        logger.info(f"Aggregated to daily level: {len(df_daily)} rows")
        
        return df_daily
    
    def preprocess_dataset(self, dataset_id: str, dataset_info: Dict) -> Optional[pd.DataFrame]:
        """Preprocess a single dataset"""
        logger.info(f"\n{'='*70}")
        logger.info(f"Preprocessing: {dataset_info.get('name', dataset_id)}")
        logger.info(f"{'='*70}")
        
        # Load dataset
        df = self.load_dataset(dataset_id, dataset_info)
        if df is None:
            return None
        
        logger.info(f"Initial shape: {df.shape}")
        
        # Map columns
        mapping = dataset_info.get('columns_mapping', {})
        df = self.map_columns(df, mapping)
        
        # Standardize date
        if 'date' in df.columns:
            df = self.standardize_date_column(df, 'date', dataset_id)
        
        # Add missing columns
        df = self.add_missing_columns(df)
        
        # Engineer features
        df = self.engineer_features(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Remove outliers
        df = self.remove_outliers(df)
        
        # Aggregate to daily if needed
        aggregation = self.preprocessing_config.get('aggregation_level', 'daily')
        if aggregation == 'daily':
            df = self.aggregate_to_daily(df)
        
        # Add dataset source identifier
        df['dataset_source'] = dataset_id
        
        logger.info(f"Final shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}")
        
        # Save preprocessed dataset
        output_path = self.processed_data_dir / f"{dataset_id}_preprocessed.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Saved preprocessed dataset to: {output_path}")
        
        return df
    
    def preprocess_all_datasets(self, selected_datasets: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """Preprocess all datasets"""
        results = {}
        datasets = self.config.get('datasets', {})
        
        if selected_datasets:
            datasets = {k: v for k, v in datasets.items() if k in selected_datasets}
        
        for dataset_id, dataset_info in datasets.items():
            try:
                df = self.preprocess_dataset(dataset_id, dataset_info)
                if df is not None:
                    results[dataset_id] = df
            except Exception as e:
                logger.error(f"Error preprocessing {dataset_id}: {e}")
        
        return results

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Preprocess datasets for Nova Corrente demand forecasting'
    )
    parser.add_argument(
        '--datasets',
        nargs='+',
        help='Specific datasets to preprocess (by ID). If not specified, processes all.'
    )
    parser.add_argument(
        '--config',
        default='config/datasets_config.json',
        help='Path to datasets configuration file'
    )
    
    args = parser.parse_args()
    
    preprocessor = DatasetPreprocessor(config_path=args.config)
    results = preprocessor.preprocess_all_datasets(selected_datasets=args.datasets)
    
    logger.info(f"\n{'='*70}")
    logger.info("PREPROCESSING SUMMARY")
    logger.info(f"{'='*70}")
    logger.info(f"Successfully preprocessed: {len(results)}/{len(preprocessor.config.get('datasets', {}))} datasets")

if __name__ == "__main__":
    main()


