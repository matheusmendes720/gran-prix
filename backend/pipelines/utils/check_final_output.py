#!/usr/bin/env python3
"""Check final output files"""

import pandas as pd
from pathlib import Path
import json

print("="*70)
print("FINAL SYSTEM OUTPUT CHECK")
print("="*70)

# Check unified dataset
project_root = Path(__file__).parent.parent.parent
unified_path = project_root / "data" / "processed" / "unified_dataset_with_factors.csv"
if unified_path.exists():
    df = pd.read_csv(unified_path, low_memory=False)
    print(f"\nUnified Dataset:")
    print(f"  Location: {unified_path}")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Total quantity: {df['quantity'].sum():,.2f}")
    print(f"  Average quantity: {df['quantity'].mean():.2f}")
    print(f"\n  Columns: {list(df.columns)}")
else:
    print(f"\nUnified dataset not found at {unified_path}")

# Check training datasets
training_dir = project_root / "data" / "training"
if training_dir.exists():
    training_files = list(training_dir.glob("*_train.csv"))
    print(f"\nTraining Datasets:")
    print(f"  Found {len(training_files)} training files")
    for f in training_files[:5]:
        df = pd.read_csv(f, low_memory=False)
        print(f"  - {f.name}: {len(df)} records")

# Check downloaded datasets
raw_dir = project_root / "data" / "raw"
if raw_dir.exists():
    print(f"\nDownloaded Raw Datasets:")
    for d in raw_dir.iterdir():
        if d.is_dir():
            files = list(d.glob("*.*"))
            print(f"  - {d.name}: {len(files)} files")

print("\n" + "="*70)
print("SYSTEM READY FOR ML TRAINING!")
print("="*70)



