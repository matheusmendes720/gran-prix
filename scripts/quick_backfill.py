"""
Quick Historical Backfill for Nova Corrente
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

def run_backfill():
    print("[START] Historical Backfill Process")
    
    data_dir = Path('D:/codex/datamaster/senai/gran_prix/data')
    
    # Load datasets
    nova_path = data_dir / 'processed/nova_corrente/nova_corrente_enriched.csv'
    nova_corrente = pd.read_csv(nova_path)
    print(f"[OK] Loaded Nova Corrente: {nova_corrente.shape}")
    
    factors_path = data_dir / 'processed/ml_ready/brazilian_demand_factors_enriched.csv'
    brazilian_factors = pd.read_csv(factors_path)
    print(f"[OK] Loaded Brazilian Factors: {brazilian_factors.shape}")
    
    # Create backfill period (extend to 730+ days total)
    nova_dates = pd.to_datetime(nova_corrente['date'])
    current_start = nova_dates.min()
    
    # Need 730 days total, we have 381, so need 349 more days
    backfill_start = current_start - timedelta(days=349)
    backfill_end = current_start - timedelta(days=1)
    
    backfill_dates = pd.date_range(start=backfill_start, end=backfill_end, freq='D')
    print(f"[OK] Backfill period: {backfill_start.date()} to {backfill_end.date()} ({len(backfill_dates)} days)")
    
    # Generate backfill records
    backfill_records = []
    items = nova_corrente['item_id'].unique()
    sites = nova_corrente['site_id'].unique()
    
    # Get patterns from current data
    item_stats = nova_corrente.groupby('item_id')['quantidade'].agg(['mean', 'std']).to_dict()
    
    for date in backfill_dates:
        date_str = date.strftime('%Y-%m-%d')
        
        # Get matching factors or use averages
        matching = brazilian_factors[brazilian_factors['date'] == date_str]
        if not matching.empty:
            factors = matching.iloc[0]
        else:
            factors = brazilian_factors.select_dtypes(include=[np.number]).mean()
        
        for item in items:
            for site in sites:
                # Base demand with seasonal adjustment
                base_demand = item_stats['mean'].get(item, 100)
                seasonal_adj = 1.0 + 0.2 * np.sin(2 * np.pi * date.dayofyear / 365)  # Seasonal pattern
                random_noise = np.random.normal(1.0, 0.1)
                
                demand = int(base_demand * seasonal_adj * random_noise)
                
                record = {
                    'date': date_str,
                    'item_id': item,
                    'site_id': site,
                    'quantidade': max(0, demand),
                    'year': date.year,
                    'month': date.month,
                    'day': date.day,
                    'day_of_year': date.timetuple().tm_yday,
                    'gdp_growth_rate': factors.get('gdp_growth_rate', 2.0),
                    'inflation_rate': factors.get('inflation_rate', 4.0),
                    'temperature_avg_c': factors.get('temperature_avg_c', 25.0),
                    'dataset_source': 'historical_backfill'
                }
                backfill_records.append(record)
    
    historical_data = pd.DataFrame(backfill_records)
    print(f"[OK] Generated {len(historical_data)} historical records")
    
    # Combine datasets
    historical_data['date'] = pd.to_datetime(historical_data['date'])
    nova_corrente['date'] = pd.to_datetime(nova_corrente['date'])
    
    combined = pd.concat([historical_data, nova_corrente], ignore_index=True)
    combined = combined.sort_values(['date', 'item_id', 'site_id']).reset_index(drop=True)
    
    total_days = (combined['date'].max() - combined['date'].min()).days + 1
    print(f"[OK] Combined dataset: {combined.shape} | Timeline: {total_days} days")
    
    # Save results
    output_dir = data_dir / 'outputs/nova_corrente/historical_backfill'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    main_path = output_dir / f'nova_corrente_backfilled_{timestamp}.csv'
    combined.to_csv(main_path, index=False)
    
    # Pipeline version
    pipeline_path = data_dir / 'processed/nova_corrente/nova_corrente_enriched_backfilled.csv'
    combined.to_csv(pipeline_path, index=False)
    
    print(f"[OK] Saved: {main_path}")
    print(f"[OK] Pipeline version: {pipeline_path}")
    
    return combined, main_path, pipeline_path

if __name__ == "__main__":
    try:
        combined, main_path, pipeline_path = run_backfill()
        print("[SUCCESS] Historical backfill completed!")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise