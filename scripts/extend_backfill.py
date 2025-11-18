import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

try:
    print("[START] Extended Historical Backfill Process")
    
    data_dir = Path('D:/codex/datamaster/senai/gran_prix/data')
    
    # Load backfilled dataset
    backfilled_path = data_dir / 'processed/nova_corrente/nova_corrente_enriched_backfilled.csv'
    backfilled = pd.read_csv(backfilled_path)
    print(f"[OK] Loaded backfilled data: {backfilled.shape}")
    
    factors_path = data_dir / 'processed/ml_ready/brazilian_demand_factors_enriched.csv'
    brazilian_factors = pd.read_csv(factors_path)
    print(f"[OK] Loaded Brazilian Factors: {brazilian_factors.shape}")
    
    # Current timeline analysis
    backfilled['date'] = pd.to_datetime(backfilled['date'])
    current_start = backfilled['date'].min()
    current_end = backfilled['date'].max()
    current_days = (current_end - current_start).days + 1
    current_months = current_days / 30.44  # Average days per month
    
    print(f"[INFO] Current timeline: {current_start.date()} to {current_end.date()}")
    print(f"[INFO] Current duration: {current_days} days ({current_months:.1f} months)")
    
    # Need minimum 24 months = 730+ days
    target_months = 24
    target_days = int(target_months * 30.44)
    additional_days_needed = max(0, target_days - current_days)
    
    if additional_days_needed <= 0:
        print("[OK] Already meets minimum 24-month requirement")
    else:
        print(f"[INFO] Need {additional_days_needed} additional days to reach {target_months} months")
        
        # Extend further back
        new_start = current_start - timedelta(days=additional_days_needed)
        extended_end = current_start - timedelta(days=1)
        
        extended_dates = pd.date_range(start=new_start, end=extended_end, freq='D')
        print(f"[INFO] Extended period: {new_start.date()} to {extended_end.date()} ({len(extended_dates)} days)")
        
        # Generate additional records
        extended_records = []
        items = backfilled['item_id'].unique()
        sites = backfilled['site_id'].unique()
        
        # Calculate item statistics from existing data
        if 'quantidade' in backfilled.columns:
            item_stats = backfilled.groupby('item_id')['quantidade'].agg(['mean', 'std']).fillna(0).to_dict()
        else:
            item_stats = {item: {'mean': 100, 'std': 20} for item in items}
        
        for date in extended_dates:
            date_str = date.strftime('%Y-%m-%d')
            
            # Get matching factors
            matching = brazilian_factors[brazilian_factors['date'] == date_str]
            if not matching.empty:
                factors = matching.iloc[0]
            else:
                # Use seasonal approximation based on month
                month_factors = brazilian_factors[brazilian_factors['month'] == date.month]
                if not month_factors.empty:
                    factors = month_factors.select_dtypes(include=[np.number]).mean()
                else:
                    factors = brazilian_factors.select_dtypes(include=[np.number]).mean()
            
            for item in items:
                for site in sites:
                    # Base demand with stronger seasonal pattern for historical data
                    base_demand = item_stats['mean'].get(item, 100)
                    
                    # Enhanced seasonal adjustment
                    seasonal_factor = 1.0 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
                    monthly_adjustment = 1.0 + 0.2 * np.sin(2 * np.pi * date.month / 12)
                    
                    # Economic impact for older periods (higher inflation in 2022-2023)
                    year_factor = 1.2 if date.year <= 2023 else 1.0
                    
                    # Random variation
                    random_noise = np.random.normal(1.0, 0.15)  # Higher variation for older data
                    
                    demand = int(base_demand * seasonal_factor * monthly_adjustment * year_factor * random_noise)
                    
                    record = {
                        'date': date_str,
                        'item_id': item,
                        'site_id': site,
                        'quantidade': max(0, demand),
                        'year': date.year,
                        'month': date.month,
                        'day': date.day,
                        'day_of_year': date.timetuple().tm_yday,
                        'gdp_growth_rate': factors.get('gdp_growth_rate', 2.5),
                        'inflation_rate': factors.get('inflation_rate', 5.0 if date.year <= 2023 else 4.0),
                        'temperature_avg_c': factors.get('temperature_avg_c', 25.0),
                        'precipitation_mm': factors.get('precipitation_mm', 0.0),
                        'dataset_source': 'extended_backfill',
                        'backfill_confidence': 0.7  # Lower confidence for extended data
                    }
                    extended_records.append(record)
        
        extended_data = pd.DataFrame(extended_records)
        print(f"[OK] Generated {len(extended_records)} extended records")
        
        # Combine all data
        extended_data['date'] = pd.to_datetime(extended_data['date'])
        combined = pd.concat([extended_data, backfilled], ignore_index=True)
        combined = combined.sort_values(['date', 'item_id', 'site_id']).reset_index(drop=True)
        
        # Update timeline statistics
        new_total_days = (combined['date'].max() - combined['date'].min()).days + 1
        new_total_months = new_total_days / 30.44
        
        print(f"[OK] Extended dataset: {combined.shape}")
        print(f"[OK] New timeline: {combined['date'].min().date()} to {combined['date'].max().date()}")
        print(f"[OK] Total duration: {new_total_days} days ({new_total_months:.1f} months)")
        
        # Save extended dataset
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        extended_path = data_dir / 'outputs/nova_corrente/historical_backfill' / f'nova_corrente_extended_{timestamp}.csv'
        extended_path.parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(extended_path, index=False)
        
        # Update pipeline version
        pipeline_path = data_dir / 'processed/nova_corrente/nova_corrente_enriched_extended.csv'
        combined.to_csv(pipeline_path, index=False)
        
        print(f"[OK] Extended dataset saved: {extended_path}")
        print(f"[OK] Pipeline version updated: {pipeline_path}")
        
        backfilled = combined  # Use for further processing
    
    print("[SUCCESS] Extended backfill completed!")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
    raise