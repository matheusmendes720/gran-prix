import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

try:
    print("[START] Fixing Date Coverage for ML Pipeline")
    
    # Load ML-ready dataset
    data_path = 'D:/codex/datamaster/senai/gran_prix/data/processed/nova_corrente/nova_corrente_enriched_ml_ready.csv'
    df = pd.read_csv(data_path, low_memory=False)
    print(f"[OK] Loaded dataset: {df.shape}")
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Get unique items and sites
    items = df['item_id'].unique()[:5]  # Limit to first 5 items
    sites = df['site_id'].unique()[:3]   # Limit to first 3 sites
    
    print(f"[INFO] Processing {len(items)} items and {len(sites)} sites")
    
    # Filter data
    df_filtered = df[
        (df['item_id'].isin(items)) & 
        (df['site_id'].isin(sites))
    ].copy()
    
    # Get date range
    min_date = df_filtered['date'].min()
    max_date = df_filtered['date'].max()
    all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
    
    print(f"[INFO] Date range: {min_date.date()} to {max_date.date()} ({len(all_dates)} days)")
    
    # Create complete date-item-site grid
    complete_grid = []
    item_stats = df_filtered.groupby('item_id')['Quantity_Consumed'].agg(['mean', 'std']).fillna(0).to_dict()
    
    for date in all_dates:
        date_str = date.strftime('%Y-%m-%d')
        for item in items:
            for site in sites:
                # Check if record exists
                existing = df_filtered[
                    (df_filtered['date'] == date) & 
                    (df_filtered['item_id'] == item) & 
                    (df_filtered['site_id'] == site)
                ]
                
                if not existing.empty:
                    # Use existing record
                    record = existing.iloc[0].to_dict()
                    record['date'] = date_str
                else:
                    # Create synthetic record for missing date
                    base_demand = item_stats['mean'].get(item, 100)
                    seasonal_adj = 1.0 + 0.2 * np.sin(2 * np.pi * date.dayofyear / 365)
                    random_var = np.random.normal(1.0, 0.1)
                    
                    demand = max(0, int(base_demand * seasonal_adj * random_var))
                    
                    # Get base record structure
                    base_record = df_filtered.iloc[0].to_dict() if not df_filtered.empty else {
                        'year': date.year,
                        'month': date.month,
                        'day': date.day,
                        'day_of_year': date.timetuple().tm_yday,
                        'gdp_growth_rate': 2.5,
                        'inflation_rate': 4.0,
                        'temperature_avg_c': 25.0,
                        'precipitation_mm': 0.0
                    }
                    
                    record = base_record.copy()
                    record.update({
                        'date': date_str,
                        'item_id': item,
                        'site_id': site,
                        'Quantity_Consumed': demand,
                        'year': date.year,
                        'month': date.month,
                        'day': date.day,
                        'day_of_year': date.timetuple().tm_yday,
                        'dataset_source': 'synthetic_fill'
                    })
                
                complete_grid.append(record)
    
    # Create complete dataset
    complete_df = pd.DataFrame(complete_grid)
    complete_df['date'] = pd.to_datetime(complete_df['date'])
    
    # Sort and reset index
    complete_df = complete_df.sort_values(['date', 'item_id', 'site_id']).reset_index(drop=True)
    
    print(f"[OK] Complete dataset: {complete_df.shape}")
    print(f"[OK] Date coverage: {len(complete_df['date'].unique())} unique dates")
    
    # Validate date coverage
    expected_dates = pd.date_range(start=min_date, end=max_date, freq='D')
    actual_dates = set(complete_df['date'].unique())
    missing_dates = set(expected_dates) - actual_dates
    
    print(f"[INFO] Missing dates: {len(missing_dates)}")
    
    # Save complete dataset
    output_path = 'D:/codex/datamaster/senai/gran_prix/data/processed/nova_corrente/nova_corrente_complete_ml_ready.csv'
    complete_df.to_csv(output_path, index=False)
    
    print(f"[OK] Complete ML-ready dataset saved: {output_path}")
    print("[SUCCESS] Date coverage fixed!")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
    raise