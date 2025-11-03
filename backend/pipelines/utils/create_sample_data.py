#!/usr/bin/env python3
"""
Create Sample Dataset for Testing Pipeline
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Create directories
project_root = Path(__file__).parent.parent.parent
(project_root / 'data' / 'raw' / 'test_dataset').mkdir(parents=True, exist_ok=True)

# Generate sample data - 2 years of daily data
dates = pd.date_range('2023-01-01', periods=730, freq='D')

# Create sample dataset matching unified schema
df = pd.DataFrame({
    'Date': dates,
    'Product': 'CONN-001',
    'Order_Demand': np.random.randint(3, 12, 730),
    'Site': 'TORRE001',
    'Category': 'Conectores',
    'Cost': 300.0,
    'Lead_Time': 14
})

# Save to CSV
output_path = project_root / 'data' / 'raw' / 'test_dataset' / 'test_data.csv'
df.to_csv(output_path, index=False)

print(f"Sample dataset created!")
print(f"Location: {output_path}")
print(f"Records: {len(df)}")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())



