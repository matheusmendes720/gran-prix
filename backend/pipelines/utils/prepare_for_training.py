#!/usr/bin/env python3
"""
Training Preparation Script for Nova Corrente Demand Forecasting System
Prepares unified dataset for ML model training (ARIMA, Prophet, LSTM)
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TrainingDataPreparator:
    """Prepare data for ML model training"""
    
    def __init__(self, config_path: str = None):
        # Get project root (3 levels up from src/utils)
        project_root = Path(__file__).parent.parent.parent
        if config_path is None:
            config_path = str(project_root / "config" / "datasets_config.json")
        else:
            if not Path(config_path).is_absolute():
                config_path = str(project_root / config_path)
        self.config_path = config_path
        self.project_root = project_root
        self.processed_data_dir = project_root / "data" / "processed"
        self.training_data_dir = project_root / "data" / "training"
        self.training_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def load_unified_dataset(self) -> pd.DataFrame:
        """Load unified dataset"""
        dataset_path = self.processed_data_dir / "unified_dataset_with_factors.csv"
        
        if not dataset_path.exists():
            logger.error(f"Unified dataset not found at {dataset_path}")
            logger.error("Please run the pipeline first: python run_pipeline.py")
            return None
        
        logger.info(f"Loading unified dataset from {dataset_path}")
        df = pd.read_csv(dataset_path, low_memory=False)
        
        if 'date' in df.columns:
            # Handle mixed date formats (some with time, some without)
            df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
        
        logger.info(f"Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def create_item_datasets(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Create individual datasets per item for training"""
        logger.info("\n" + "="*70)
        logger.info("CREATING ITEM-SPECIFIC DATASETS")
        logger.info("="*70)
        
        if 'item_id' not in df.columns or 'quantity' not in df.columns:
            logger.error("Required columns (item_id, quantity) not found")
            return {}
        
        item_datasets = {}
        
        # Group by item
        for item_id, item_df in df.groupby('item_id'):
            # Sort by date
            item_df = item_df.sort_values('date').copy()
            
            # Ensure date is index
            if 'date' in item_df.columns:
                item_df = item_df.set_index('date')
            
            # Select relevant columns for time series
            ts_columns = ['quantity']
            
            # Add external factors if available
            external_cols = ['temperature', 'precipitation', 'humidity', 
                           'exchange_rate_brl_usd', 'inflation_rate',
                           'is_holiday', 'weekend', 'month']
            
            for col in external_cols:
                if col in item_df.columns:
                    ts_columns.append(col)
            
            # Create time series dataset
            ts_df = item_df[ts_columns].copy()
            
            # Remove NaN values
            ts_df = ts_df.dropna()
            
            if len(ts_df) >= 30:  # Minimum 30 days for training
                item_datasets[item_id] = ts_df
                logger.info(f"  {item_id}: {len(ts_df)} days of data")
            else:
                logger.warning(f"  {item_id}: Insufficient data ({len(ts_df)} days, minimum: 30)")
        
        logger.info(f"\n✓ Created datasets for {len(item_datasets)} items")
        return item_datasets
    
    def prepare_for_arima(self, df: pd.DataFrame, item_id: str) -> pd.DataFrame:
        """Prepare data for ARIMA model"""
        # ARIMA needs univariate time series
        arima_df = df[['quantity']].copy()
        
        # Ensure no NaN values
        arima_df = arima_df.dropna()
        
        # Optional: Add external regressors if available
        exog_cols = ['temperature', 'precipitation', 'is_holiday', 'weekend']
        available_exog = [col for col in exog_cols if col in df.columns]
        
        if available_exog:
            arima_df = pd.concat([arima_df, df[available_exog]], axis=1)
        
        return arima_df
    
    def prepare_for_prophet(self, df: pd.DataFrame, item_id: str) -> pd.DataFrame:
        """Prepare data for Prophet model"""
        # Prophet needs 'ds' (date) and 'y' (target) columns
        prophet_df = df.reset_index().copy()
        
        # Rename columns
        if 'date' in prophet_df.columns:
            prophet_df = prophet_df.rename(columns={'date': 'ds', 'quantity': 'y'})
        else:
            prophet_df.index.name = 'ds'
            prophet_df = prophet_df.reset_index()
            prophet_df = prophet_df.rename(columns={'quantity': 'y'})
        
        # Select columns: ds, y, and optional regressors
        prophet_cols = ['ds', 'y']
        
        regressor_cols = ['temperature', 'precipitation', 'is_holiday', 'weekend']
        for col in regressor_cols:
            if col in prophet_df.columns:
                prophet_cols.append(col)
        
        prophet_df = prophet_df[prophet_cols].copy()
        prophet_df = prophet_df.dropna(subset=['ds', 'y'])
        
        return prophet_df
    
    def prepare_for_lstm(self, df: pd.DataFrame, item_id: str, look_back: int = 30) -> tuple:
        """Prepare data for LSTM model"""
        # LSTM needs sequences of look_back days
        lstm_df = df[['quantity']].copy()
        
        # Normalize data (0-1 scale)
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        scaled_values = scaler.fit_transform(lstm_df.values)
        
        # Create sequences
        X, y = [], []
        for i in range(len(scaled_values) - look_back):
            X.append(scaled_values[i:i+look_back])
            y.append(scaled_values[i+look_back])
        
        X = np.array(X)
        y = np.array(y)
        
        # Reshape for LSTM: (samples, time_steps, features)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        return X, y, scaler
    
    def split_train_test(self, df: pd.DataFrame, train_pct: float = 0.8) -> tuple:
        """Split data into train and test sets"""
        split_idx = int(len(df) * train_pct)
        train_df = df.iloc[:split_idx].copy()
        test_df = df.iloc[split_idx:].copy()
        
        logger.info(f"  Train: {len(train_df)} records ({train_pct*100:.0f}%)")
        logger.info(f"  Test: {len(test_df)} records ({(1-train_pct)*100:.0f}%)")
        
        return train_df, test_df
    
    def save_training_datasets(self, item_datasets: Dict[str, pd.DataFrame]):
        """Save prepared training datasets"""
        logger.info("\n" + "="*70)
        logger.info("SAVING TRAINING DATASETS")
        logger.info("="*70)
        
        saved_count = 0
        
        for item_id, df in item_datasets.items():
            # Sanitize item_id for filename
            safe_item_id = str(item_id).replace('/', '_').replace('\\', '_')
            
            # Save full dataset
            full_path = self.training_data_dir / f"{safe_item_id}_full.csv"
            df.to_csv(full_path)
            
            # Split and save train/test
            train_df, test_df = self.split_train_test(df)
            
            train_path = self.training_data_dir / f"{safe_item_id}_train.csv"
            test_path = self.training_data_dir / f"{safe_item_id}_test.csv"
            
            train_df.to_csv(train_path)
            test_df.to_csv(test_path)
            
            saved_count += 1
        
        logger.info(f"\n✓ Saved training datasets for {saved_count} items")
        logger.info(f"Location: {self.training_data_dir}")
        
        # Create metadata file
        metadata = {
            'total_items': len(item_datasets),
            'items': list(item_datasets.keys()),
            'prepared_date': pd.Timestamp.now().isoformat()
        }
        
        metadata_path = self.training_data_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"✓ Metadata saved to: {metadata_path}")
    
    def generate_training_summary(self, item_datasets: Dict[str, pd.DataFrame]):
        """Generate summary of training datasets"""
        logger.info("\n" + "="*70)
        logger.info("TRAINING DATASET SUMMARY")
        logger.info("="*70)
        
        summary = {
            'total_items': len(item_datasets),
            'items_statistics': {}
        }
        
        for item_id, df in item_datasets.items():
            stats = {
                'records': len(df),
                'date_range': {
                    'start': str(df.index.min()) if hasattr(df.index, 'min') else None,
                    'end': str(df.index.max()) if hasattr(df.index, 'max') else None
                },
                'quantity': {
                    'mean': float(df['quantity'].mean()) if 'quantity' in df.columns else None,
                    'std': float(df['quantity'].std()) if 'quantity' in df.columns else None,
                    'min': float(df['quantity'].min()) if 'quantity' in df.columns else None,
                    'max': float(df['quantity'].max()) if 'quantity' in df.columns else None
                }
            }
            summary['items_statistics'][str(item_id)] = stats
        
        summary_path = self.training_data_dir / "training_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"✓ Summary saved to: {summary_path}")
        
        # Print summary
        print(f"\nTotal items prepared: {summary['total_items']}")
        print("\nSample items:")
        for i, (item_id, stats) in enumerate(list(summary['items_statistics'].items())[:5]):
            print(f"  {item_id}: {stats['records']} records")
    
    def prepare_all(self):
        """Prepare all data for training"""
        logger.info("\n" + "="*70)
        logger.info("PREPARING DATA FOR ML TRAINING")
        logger.info("="*70)
        
        # Load unified dataset
        df = self.load_unified_dataset()
        if df is None:
            return
        
        # Create item-specific datasets
        item_datasets = self.create_item_datasets(df)
        
        if not item_datasets:
            logger.error("No item datasets created!")
            return
        
        # Save training datasets
        self.save_training_datasets(item_datasets)
        
        # Generate summary
        self.generate_training_summary(item_datasets)
        
        logger.info("\n✓ Data preparation completed!")
        logger.info("\nNext steps:")
        logger.info("  1. Train ARIMA models using item-specific datasets")
        logger.info("  2. Train Prophet models (ready for 'ds' and 'y' columns)")
        logger.info("  3. Train LSTM models (use prepare_for_lstm() function)")
        logger.info("  4. Calculate Reorder Points (PP)")
        logger.info("  5. Generate forecasts and alerts")

def main():
    """Main entry point"""
    preparator = TrainingDataPreparator()
    preparator.prepare_all()

if __name__ == "__main__":
    main()



