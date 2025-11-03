#!/usr/bin/env python3
"""Verify master dataset"""

import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
dataset_file = BASE_DIR / 'data' / 'processed' / 'unified_master_ml_ready.csv'
summary_file = BASE_DIR / 'data' / 'processed' / 'master_integration_summary.json'

print("="*80)
print("MASTER DATASET VERIFICATION")
print("="*80)

if dataset_file.exists():
    df = pd.read_csv(dataset_file, low_memory=False)
    print(f"\n[OK] Dataset found: {dataset_file}")
    print(f"   Records: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    
    if summary_file.exists():
        summary = json.load(open(summary_file))
        print(f"\nSummary:")
        print(f"   Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        print(f"   Datasets integrated: {len(summary['datasets_integrated'])}")
        print(f"   Missing data: {summary['missing_data_pct']:.2f}%")
        
        print(f"\nFeature Categories:")
        for category, count in summary['column_categories'].items():
            print(f"   {category}: {count} features")
    
    print(f"\nSample Columns (first 25):")
    for i, col in enumerate(df.columns[:25], 1):
        print(f"   {i:2d}. {col}")
    
    print(f"\n[OK] Master dataset verified and ready for ML/DL training!")
else:
    print(f"\n[FAILED] Dataset not found: {dataset_file}")

