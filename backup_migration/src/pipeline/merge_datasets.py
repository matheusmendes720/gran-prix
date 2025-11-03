#!/usr/bin/env python3
"""
Dataset Merger Script for Nova Corrente Demand Forecasting System
Merges multiple preprocessed datasets into unified structure
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
project_root = Path(__file__).parent.parent.parent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(project_root / 'data' / 'processed' / 'merge_log.txt')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatasetMerger:
    """Merge multiple datasets into unified structure"""
    
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
        self.processed_data_dir = project_root / "data" / "processed"
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.unified_schema = self.config.get('unified_schema', {})
    
    def load_preprocessed_datasets(self, selected_datasets: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """Load all preprocessed datasets"""
        datasets = {}
        
        # Find all preprocessed CSV files
        preprocessed_files = list(self.processed_data_dir.glob("*_preprocessed.csv"))
        
        for file_path in preprocessed_files:
            dataset_id = file_path.stem.replace('_preprocessed', '')
            
            # Filter if selected_datasets specified
            if selected_datasets and dataset_id not in selected_datasets:
                continue
            
            try:
                logger.info(f"Loading preprocessed dataset: {file_path.name}")
                df = pd.read_csv(file_path, low_memory=False)
                
                # Ensure date column is datetime
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                
                datasets[dataset_id] = df
                logger.info(f"Loaded {dataset_id}: {len(df)} rows, {len(df.columns)} columns")
            except Exception as e:
                logger.error(f"Error loading {file_path.name}: {e}")
        
        return datasets
    
    def validate_schema(self, df: pd.DataFrame, dataset_id: str) -> bool:
        """Validate dataset against unified schema"""
        required_cols = self.unified_schema.get('required_columns', [])
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            logger.warning(f"{dataset_id}: Missing required columns: {missing_cols}")
            return False
        
        logger.info(f"{dataset_id}: Schema validation passed")
        return True
    
    def standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize data types according to unified schema"""
        df = df.copy()
        data_types = self.unified_schema.get('data_types', {})
        
        for col, dtype in data_types.items():
            if col not in df.columns:
                continue
            
            try:
                if dtype == 'datetime64[ns]':
                    df[col] = pd.to_datetime(df[col])
                elif dtype == 'string':
                    df[col] = df[col].astype(str)
                elif dtype == 'float64':
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                elif dtype == 'int64':
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                
                logger.debug(f"Standardized {col} to {dtype}")
            except Exception as e:
                logger.warning(f"Error standardizing {col} to {dtype}: {e}")
        
        return df
    
    def merge_datasets(self, datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Merge multiple datasets into unified structure"""
        logger.info(f"\n{'='*70}")
        logger.info("MERGING DATASETS")
        logger.info(f"{'='*70}")
        
        # Get unified schema columns
        required_cols = self.unified_schema.get('required_columns', [])
        optional_cols = self.unified_schema.get('optional_columns', [])
        
        all_cols = required_cols + optional_cols
        common_cols = set(required_cols)
        
        # Standardize all datasets
        standardized_datasets = []
        for dataset_id, df in datasets.items():
            # Validate schema
            if not self.validate_schema(df, dataset_id):
                logger.warning(f"Skipping {dataset_id} due to schema validation failure")
                continue
            
            # Standardize data types
            df_std = self.standardize_data_types(df)
            
            # Select only common columns
            available_cols = [col for col in all_cols if col in df_std.columns]
            
            # Add dataset source if not present
            if 'dataset_source' not in df_std.columns:
                df_std['dataset_source'] = dataset_id
            
            # Select columns in priority order
            priority_cols = required_cols + ['dataset_source'] + [col for col in optional_cols if col in df_std.columns]
            df_std = df_std[[col for col in priority_cols if col in df_std.columns]]
            
            standardized_datasets.append(df_std)
            logger.info(f"{dataset_id}: Prepared {len(df_std)} rows with {len(df_std.columns)} columns")
        
        if not standardized_datasets:
            logger.error("No datasets to merge!")
            return pd.DataFrame()
        
        # Concatenate all datasets
        logger.info("\nConcatenating datasets...")
        merged_df = pd.concat(standardized_datasets, ignore_index=True, sort=False)
        
        logger.info(f"Merged dataset shape: {merged_df.shape}")
        logger.info(f"Columns: {list(merged_df.columns)}")
        
        # Remove duplicates if any
        initial_count = len(merged_df)
        merged_df = merged_df.drop_duplicates(
            subset=['date', 'item_id', 'site_id'] if all(col in merged_df.columns for col in ['date', 'item_id', 'site_id']) 
            else ['date', 'item_id'],
            keep='first'
        )
        
        duplicates_removed = initial_count - len(merged_df)
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate records")
        
        # Sort by date
        if 'date' in merged_df.columns:
            merged_df = merged_df.sort_values('date').reset_index(drop=True)
        
        return merged_df
    
    def handle_conflicts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle conflicts in merged data (e.g., same item on same date from different sources)"""
        # Group by date and item to identify conflicts
        if not all(col in df.columns for col in ['date', 'item_id', 'dataset_source']):
            return df
        
        conflict_cols = ['date', 'item_id']
        if 'site_id' in df.columns:
            conflict_cols.append('site_id')
        
        conflicts = df.groupby(conflict_cols).size()
        conflicts = conflicts[conflicts > 1]
        
        if len(conflicts) > 0:
            logger.info(f"Found {len(conflicts)} conflicting records (same date/item from multiple sources)")
            logger.info("Keeping first occurrence and aggregating quantities")
            
            # For conflicts, aggregate quantities and keep first values for other columns
            agg_dict = {'quantity': 'sum'}
            if 'cost' in df.columns:
                agg_dict['cost'] = 'sum'
            
            # Keep first value for categorical columns
            categorical_cols = ['item_name', 'category', 'site_id', 'dataset_source']
            for col in categorical_cols:
                if col in df.columns:
                    agg_dict[col] = 'first'
            
            # Aggregate numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col not in agg_dict and col not in conflict_cols:
                    agg_dict[col] = 'mean'
            
            # Group and aggregate
            df = df.groupby(conflict_cols, as_index=False).agg(agg_dict)
            logger.info(f"After conflict resolution: {len(df)} rows")
        
        return df
    
    def create_unified_dataset(self, selected_datasets: Optional[List[str]] = None) -> pd.DataFrame:
        """Create unified dataset from all preprocessed datasets"""
        logger.info("Starting dataset merge process...")
        
        # Load preprocessed datasets
        datasets = self.load_preprocessed_datasets(selected_datasets=selected_datasets)
        
        if not datasets:
            logger.error("No preprocessed datasets found!")
            return pd.DataFrame()
        
        logger.info(f"\nFound {len(datasets)} preprocessed datasets to merge")
        
        # Merge datasets
        merged_df = self.merge_datasets(datasets)
        
        if merged_df.empty:
            logger.error("Failed to merge datasets!")
            return pd.DataFrame()
        
        # Handle conflicts
        merged_df = self.handle_conflicts(merged_df)
        
        # Final validation
        logger.info("\nFinal dataset statistics:")
        logger.info(f"  Total rows: {len(merged_df)}")
        logger.info(f"  Total columns: {len(merged_df.columns)}")
        logger.info(f"  Date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
        
        if 'quantity' in merged_df.columns:
            logger.info(f"  Total quantity: {merged_df['quantity'].sum():,.2f}")
            logger.info(f"  Average quantity: {merged_df['quantity'].mean():.2f}")
        
        # Count by dataset source
        if 'dataset_source' in merged_df.columns:
            logger.info("\nRecords by source:")
            source_counts = merged_df['dataset_source'].value_counts()
            for source, count in source_counts.items():
                logger.info(f"  {source}: {count:,} records")
        
        # Save unified dataset
        output_path = self.processed_data_dir / "unified_dataset.csv"
        merged_df.to_csv(output_path, index=False)
        logger.info(f"\nSaved unified dataset to: {output_path}")
        
        return merged_df

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Merge preprocessed datasets for Nova Corrente demand forecasting'
    )
    parser.add_argument(
        '--datasets',
        nargs='+',
        help='Specific datasets to merge (by ID). If not specified, merges all available.'
    )
    parser.add_argument(
        '--config',
        default='config/datasets_config.json',
        help='Path to datasets configuration file'
    )
    
    args = parser.parse_args()
    
    merger = DatasetMerger(config_path=args.config)
    unified_df = merger.create_unified_dataset(selected_datasets=args.datasets)
    
    if unified_df.empty:
        logger.error("Failed to create unified dataset!")
        exit(1)
    
    logger.info("\n✓ Dataset merge completed successfully!")

if __name__ == "__main__":
    main()


