#!/usr/bin/env python3
"""Check comprehensive dataset"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
dataset_file = BASE_DIR / 'data' / 'processed' / 'unified_comprehensive_ml_ready.csv'

if dataset_file.exists():
    df = pd.read_csv(dataset_file)
    print("="*80)
    print("COMPREHENSIVE UNIFIED DATASET")
    print("="*80)
    print(f"\nRecords: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    
    print(f"\nColumns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    if 'dataset_source' in df.columns:
        print(f"\nDataset Sources:")
        print(df['dataset_source'].value_counts())
    
    print(f"\nSample data:")
    print(df.head())
    
    print(f"\nData types:")
    print(df.dtypes)
else:
    print(f"Dataset not found: {dataset_file}")

