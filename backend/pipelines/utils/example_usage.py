#!/usr/bin/env python3
"""
Example Usage Script for Nova Corrente Dataset Pipeline
Demonstrates how to use the pipeline components programmatically
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from download_datasets import DatasetDownloader
from preprocess_datasets import DatasetPreprocessor
from merge_datasets import DatasetMerger
from add_external_factors import ExternalFactorsAdder
from run_pipeline import PipelineOrchestrator

def example_download_specific_datasets():
    """Example: Download only specific datasets"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Download Specific Datasets")
    print("="*70)
    
    downloader = DatasetDownloader()
    
    # Download only Kaggle daily demand dataset
    results = downloader.download_all_datasets(
        selected_datasets=['kaggle_daily_demand']
    )
    
    print(f"Download results: {results}")

def example_preprocess_and_merge():
    """Example: Preprocess and merge datasets"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Preprocess and Merge")
    print("="*70)
    
    preprocessor = DatasetPreprocessor()
    
    # Preprocess specific datasets
    preprocessed = preprocessor.preprocess_all_datasets(
        selected_datasets=['kaggle_daily_demand', 'kaggle_logistics_warehouse']
    )
    
    print(f"Preprocessed {len(preprocessed)} datasets")
    
    # Merge preprocessed datasets
    merger = DatasetMerger()
    unified_df = merger.create_unified_dataset(
        selected_datasets=['kaggle_daily_demand', 'kaggle_logistics_warehouse']
    )
    
    if not unified_df.empty:
        print(f"\nUnified dataset shape: {unified_df.shape}")
        print(f"Date range: {unified_df['date'].min()} to {unified_df['date'].max()}")
        print(f"\nFirst few rows:")
        print(unified_df.head())

def example_full_pipeline():
    """Example: Run complete pipeline"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Full Pipeline")
    print("="*70)
    
    orchestrator = PipelineOrchestrator()
    
    # Run full pipeline for specific datasets
    success = orchestrator.run_full_pipeline(
        selected_datasets=['kaggle_daily_demand', 'kaggle_logistics_warehouse'],
        skip_download=False,  # Set to True if datasets already downloaded
        skip_preprocess=False,
        skip_merge=False,
        skip_factors=False
    )
    
    if success:
        print("\n✓ Pipeline completed successfully!")
        print("\nNext steps:")
        print("  1. Check data/processed/unified_dataset_with_factors.csv")
        print("  2. Load dataset in your ML training script:")
        print("     df = pd.read_csv('data/processed/unified_dataset_with_factors.csv')")
        print("  3. Train ARIMA/Prophet/LSTM models")
        print("  4. Calculate Reorder Points (PP)")
        print("  5. Generate alerts and reports")

def example_load_final_dataset():
    """Example: Load and inspect final unified dataset"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Load Final Dataset")
    print("="*70)
    
    import pandas as pd
    
    project_root = Path(__file__).parent.parent.parent
    final_dataset_path = project_root / "data" / "processed" / "unified_dataset_with_factors.csv"
    
    if not final_dataset_path.exists():
        print(f"Dataset not found at {final_dataset_path}")
        print("Run the pipeline first:")
        print("  python run_pipeline.py")
        return
    
    df = pd.read_csv(final_dataset_path, low_memory=False)
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
    
    if 'quantity' in df.columns:
        print(f"\nQuantity statistics:")
        print(df['quantity'].describe())
    
    if 'dataset_source' in df.columns:
        print(f"\nRecords by source:")
        print(df['dataset_source'].value_counts())
    
    print(f"\nFirst few rows:")
    print(df.head())

def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("NOVA CORRENTE DATASET PIPELINE - USAGE EXAMPLES")
    print("="*70)
    
    print("\nChoose an example to run:")
    print("  1. Download specific datasets")
    print("  2. Preprocess and merge datasets")
    print("  3. Run full pipeline")
    print("  4. Load and inspect final dataset")
    print("  5. Run all examples")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == '1':
        example_download_specific_datasets()
    elif choice == '2':
        example_preprocess_and_merge()
    elif choice == '3':
        example_full_pipeline()
    elif choice == '4':
        example_load_final_dataset()
    elif choice == '5':
        example_download_specific_datasets()
        example_preprocess_and_merge()
        example_full_pipeline()
        example_load_final_dataset()
    else:
        print("Invalid choice. Running example 4 (load dataset)...")
        example_load_final_dataset()

if __name__ == "__main__":
    main()



