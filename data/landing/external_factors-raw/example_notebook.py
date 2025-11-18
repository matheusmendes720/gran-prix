"""
Freight Data Automation Example Notebook
Run with: python or jupyter notebook
"""

import pandas as pd
from datetime import datetime, timedelta
import os

print("="*60)
print("FREIGHT DATA AUTOMATION - EXAMPLE NOTEBOOK")
print("="*60)

# Step 1: One-time download
print("\n[Step 1] Downloading freight data...")
print("-" * 60)

try:
    from freight_data_automation import FreightAutomationOrchestrator

    orchestrator = FreightAutomationOrchestrator(output_dir="data/manual")
    results = orchestrator.download_all(skip_manual=True)
    orchestrator.print_status()
except Exception as e:
    print(f"Error: {e}")
    print("Note: Ensure Trading Economics API key is set")
    print("export TRADING_ECONOMICS_API_KEY='your_key'")

# Step 2: Load and inspect data
print("\n[Step 2] Loading and inspecting downloaded data...")
print("-" * 60)

data_files = [
    'data/manual/bdi_historical.csv',
    'data/manual/imf_shipping_cost_index.csv'
]

loaded_data = {}
for filepath in data_files:
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            name = os.path.basename(filepath).replace('.csv', '')
            loaded_data[name] = df

            print(f"\n✓ {name}")
            print(f"  Shape: {df.shape}")
            print(f"  Columns: {', '.join(df.columns)}")
            print(f"  Date range: {df.iloc[-1, 0]} to {df.iloc[0, 0]}")
            print(f"  Records: {len(df)}")
        except Exception as e:
            print(f"✗ {filepath}: {e}")

# Step 3: Data quality checks
print("\n[Step 3] Data quality analysis...")
print("-" * 60)

for name, df in loaded_data.items():
    print(f"\n{name}:")
    print(f"  Missing values: {df.isnull().sum().sum()}")
    print(f"  Data types: {dict(df.dtypes)}")
    if 'value' in df.columns:
        print(f"  Value range: {df['value'].min():.2f} - {df['value'].max():.2f}")
        print(f"  Mean: {df['value'].mean():.2f}")

# Step 4: Combine indices
print("\n[Step 4] Combining indices for feature engineering...")
print("-" * 60)

if len(loaded_data) >= 2:
    try:
        # Get BDI
        bdi = loaded_data.get('bdi_historical', None)
        if bdi is not None:
            bdi['date'] = pd.to_datetime(bdi['date'])
            bdi_indexed = bdi.set_index('date')[['value']].rename(columns={'value': 'bdi'})

            # Get IMF SCI
            imf = loaded_data.get('imf_shipping_cost_index', None)
            if imf is not None:
                imf['date'] = pd.to_datetime(imf['date'].astype(str))
                imf_indexed = imf.set_index('date')[['value']].rename(columns={'value': 'imf_sci'})

                # Merge
                merged = bdi_indexed.join(imf_indexed, how='inner')
                print(f"\nMerged dataset:")
                print(f"  Shape: {merged.shape}")
                print(f"  Date range: {merged.index[0].date()} to {merged.index[-1].date()}")
                print(f"  Common records: {len(merged)}")

                # Save combined
                merged.to_csv('data/manual/freight_indices_combined.csv')
                print(f"✓ Saved to data/manual/freight_indices_combined.csv")

                # Show sample
                print(f"\nSample data (first 5 rows):")
                print(merged.head())
    except Exception as e:
        print(f"Error combining: {e}")

# Step 5: Visualization prep
print("\n[Step 5] Visualization data preparation...")
print("-" * 60)

try:
    if 'bdi' in locals():
        # Resample to weekly for smoother visualization
        bdi_weekly = bdi_indexed.resample('W').mean()
        print(f"✓ BDI resampled to weekly: {len(bdi_weekly)} points")

        # Calculate rolling statistics
        bdi_weekly['ma_4w'] = bdi_weekly['bdi'].rolling(4).mean()
        bdi_weekly['volatility_4w'] = bdi_weekly['bdi'].rolling(4).std()

        print("✓ Added 4-week moving average and volatility")
        print(f"\nSample with indicators (last 5 rows):")
        print(bdi_weekly.tail())

        bdi_weekly.to_csv('data/manual/bdi_with_indicators.csv')
        print(f"✓ Saved to data/manual/bdi_with_indicators.csv")
except Exception as e:
    print(f"Error: {e}")

# Step 6: Ready for ML/BI
print("\n[Step 6] Ready for downstream processing...")
print("-" * 60)

print("""
Your data is ready for:
✓ Time series forecasting (ARIMA, Prophet)
✓ Demand prediction models
✓ Feature engineering for demand/inventory optimization
✓ Dashboard visualization (Plotly, Streamlit)
✓ Machine learning pipelines

Next steps:
1. Normalize/standardize the indices
2. Create lag features for forecasting
3. Combine with your internal telco data
4. Train models on combined dataset
""")

print("\n" + "="*60)
print("EXAMPLE COMPLETE")
print("="*60)
