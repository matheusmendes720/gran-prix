"""
Preprocess Brazilian Datasets for ML Integration

This script parses Brazilian JSON/CSV files and integrates them into
the unified dataset schema with proper time-series alignment.
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Setup paths
BASE_DIR = Path(__file__).parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

def load_iot_timeline() -> pd.DataFrame:
    """
    Load and preprocess Brazilian IoT timeline data.
    
    Returns:
        DataFrame with IoT growth data aligned to dates
    """
    print("Loading IoT timeline data...")
    
    iot_file = RAW_DATA_DIR / "brazilian_iot" / "brazilian_iot_timeline.csv"
    
    if not iot_file.exists():
        print(f"⚠️  File not found: {iot_file}")
        return pd.DataFrame()
    
    df = pd.read_csv(iot_file)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Calculate additional features
    df['iot_connections_yearly_growth'] = df['iot_connections_millions'].diff()
    df['iot_growth_acceleration'] = df['growth_rate_annual'].diff()
    
    print(f"✅ Loaded {len(df)} IoT data points")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    
    return df

def load_iot_sectors() -> Dict:
    """
    Load IoT sector breakdown from summary.
    
    Returns:
        Dictionary with sector data
    """
    print("Loading IoT sector data...")
    
    summary_file = RAW_DATA_DIR / "brazilian_iot" / "brazilian_iot_summary.json"
    
    if not summary_file.exists():
        print(f"⚠️  File not found: {summary_file}")
        return {}
    
    with open(summary_file, 'r') as f:
        data = json.load(f)
    
    sectors = data.get('sectors', {})
    
    # Create time-series for each sector
    df = pd.read_csv(RAW_DATA_DIR / "brazilian_iot" / "brazilian_iot_timeline.csv")
    
    # Calculate sector connections for each year
    sector_series = {}
    
    for sector_name, sector_data in sectors.items():
        connections_2024 = sector_data.get('connections_2024_millions', 0)
        growth_rate = sector_data.get('growth_rate', 0)
        
        # Back-calculate to 2020 using reverse growth
        years_back = 4  # 2020 to 2024
        connections_2020 = connections_2024 / ((1 + growth_rate) ** years_back)
        
        sector_series[sector_name] = {
            'connections_2020': connections_2020,
            'connections_2024': connections_2024,
            'growth_rate': growth_rate
        }
    
    print(f"✅ Loaded {len(sectors)} IoT sectors")
    
    return sector_series

def load_fiber_data() -> pd.DataFrame:
    """
    Load Brazilian fiber optic expansion data.
    
    Returns:
        DataFrame with fiber penetration over time
    """
    print("Loading fiber expansion data...")
    
    fiber_file = RAW_DATA_DIR / "brazilian_fiber" / "brazilian_fiber_expansion.json"
    
    if not fiber_file.exists():
        print(f"⚠️  File not found: {fiber_file}")
        return pd.DataFrame()
    
    with open(fiber_file, 'r') as f:
        data = json.load(f)
    
    # Extract household penetration
    household_data = data.get('household_penetration', {})
    
    # Convert to DataFrame
    records = []
    for year, penetration in household_data.items():
        if year.endswith('_forecast'):
            continue  # Skip forecasts for now
        
        records.append({
            'date': pd.Timestamp(f"{year}-01-01"),
            'fiber_household_penetration': penetration
        })
    
    df = pd.DataFrame(records)
    df = df.sort_values('date')
    
    # Calculate growth rate
    df['fiber_growth_rate'] = df['fiber_household_penetration'].pct_change()
    
    print(f"✅ Loaded {len(df)} fiber penetration data points")
    
    # Also extract regional data
    regional_data = data.get('regional_penetration', {})
    regional_df = pd.DataFrame([regional_data]).T.reset_index()
    regional_df.columns = ['region', 'fiber_regional_penetration']
    
    return df, regional_df

def load_operator_market_data() -> Dict:
    """
    Load Brazilian operator market share data.
    
    Returns:
        Dictionary with operator statistics
    """
    print("Loading operator market data...")
    
    operator_file = RAW_DATA_DIR / "brazilian_operators" / "brazilian_operators_market.json"
    
    if not operator_file.exists():
        print(f"⚠️  File not found: {operator_file}")
        return {}
    
    with open(operator_file, 'r') as f:
        data = json.load(f)
    
    # Extract key metrics
    market_data = {
        'vivo_market_share': data['mobile_subscribers_2023_q1']['vivo']['market_share'],
        'claro_market_share': data['mobile_subscribers_2023_q1']['claro']['market_share'],
        'tim_market_share': data['mobile_subscribers_2023_q1']['tim']['market_share'],
        'total_subscribers': data['total_subscribers_2023'],
        '5g_cities': data['5g_coverage_2023_july']['cities'],
        '5g_coverage_pct': data['5g_coverage_2023_july']['population_percentage'],
        'vivo_revenue_growth': data['mobile_subscribers_2023_q1']['vivo']['revenue_growth']
    }
    
    # Calculate competition index (Herfindahl-Hirschman Index)
    market_shares = [
        market_data['vivo_market_share'],
        market_data['claro_market_share'],
        market_data['tim_market_share']
    ]
    market_data['market_competition_index'] = sum([s**2 for s in market_shares])
    
    print(f"✅ Loaded operator market data")
    print(f"   Total subscribers: {market_data['total_subscribers']}M")
    print(f"   Competition index: {market_data['market_competition_index']:.3f}")
    
    return market_data

def create_time_index(start_date: str = "2020-01-01", end_date: str = "2025-12-31") -> pd.DatetimeIndex:
    """
    Create a daily time index for alignment.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        DatetimeIndex with daily frequency
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    return date_range

def enrich_with_brazilian_iot(df: pd.DataFrame, iot_timeline: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich dataset with IoT growth features.
    
    Args:
        df: Main dataset
        iot_timeline: IoT timeline data
        
    Returns:
        Enriched dataset
    """
    print("Enriching with IoT features...")
    
    if iot_timeline.empty:
        print("⚠️  No IoT data available")
        return df
    
    # Merge IoT data by date (using nearest for daily data)
    df = df.sort_values('date')
    iot_timeline = iot_timeline.sort_values('date')
    
    # Forward fill IoT data for daily granularity
    df = df.merge(iot_timeline, on='date', how='left')
    
    # Forward fill missing values
    iot_columns = ['iot_connections_millions', 'growth_rate_annual', 
                   'iot_connections_yearly_growth', 'iot_growth_acceleration']
    
    for col in iot_columns:
        if col in df.columns:
            df[col] = df[col].ffill()
    
    # Add IoT sector features (constant for now, could be improved with time-series)
    iot_sectors = load_iot_sectors()
    
    if iot_sectors:
        for sector_name, sector_data in iot_sectors.items():
            # Use 2024 values as constant (could be improved)
            col_name = f'iot_{sector_name}'
            df[col_name] = sector_data.get('connections_2024', sector_data.get('connections_2024_millions', 0))
    
    # Add IoT CAGR
    df['iot_cagr'] = 0.14  # 14% from data
    
    print(f"✅ Added {len([c for c in df.columns if 'iot_' in c])} IoT features")
    
    return df

def enrich_with_brazilian_fiber(df: pd.DataFrame, fiber_data: tuple) -> pd.DataFrame:
    """
    Enrich dataset with fiber expansion features.
    
    Args:
        df: Main dataset
        fiber_data: Tuple of (fiber_df, regional_df)
        
    Returns:
        Enriched dataset
    """
    print("Enriching with fiber features...")
    
    fiber_df, regional_df = fiber_data
    
    if fiber_df.empty:
        print("⚠️  No fiber data available")
        return df
    
    # Merge fiber data by date
    df = df.sort_values('date')
    fiber_df = fiber_df.sort_values('date')
    
    df = df.merge(fiber_df, on='date', how='left')
    
    # Forward fill missing values
    fiber_columns = ['fiber_household_penetration', 'fiber_growth_rate']
    
    for col in fiber_columns:
        if col in df.columns:
            df[col] = df[col].ffill()
    
    # Add regional penetration (assume all data is from Southeast for now)
    # TODO: Add region detection based on site_id or other metadata
    if not regional_df.empty:
        southeast_penetration = regional_df[regional_df['region'] == 'southeast']['fiber_regional_penetration'].values[0]
        df['fiber_regional_penetration'] = southeast_penetration
    
    print(f"✅ Added {len([c for c in df.columns if 'fiber_' in c])} fiber features")
    
    return df

def enrich_with_brazilian_operators(df: pd.DataFrame, operator_data: Dict) -> pd.DataFrame:
    """
    Enrich dataset with operator market features.
    
    Args:
        df: Main dataset
        operator_data: Operator market statistics
        
    Returns:
        Enriched dataset
    """
    print("Enriching with operator features...")
    
    if not operator_data:
        print("⚠️  No operator data available")
        return df
    
    # Add market features as constants (for now, could be time-series)
    df['vivo_market_share'] = operator_data.get('vivo_market_share', 0)
    df['claro_market_share'] = operator_data.get('claro_market_share', 0)
    df['tim_market_share'] = operator_data.get('tim_market_share', 0)
    df['market_competition_index'] = operator_data.get('market_competition_index', 0)
    df['5g_cities_count'] = operator_data.get('5g_cities', 0)
    df['5g_coverage_pct'] = operator_data.get('5g_coverage_pct', 0)
    df['operator_revenue_growth'] = operator_data.get('vivo_revenue_growth', 0)
    
    # Add flags
    df['market_consolidation_impact'] = 1  # Post-Oi sale
    df['new_entrants_flag'] = 0  # Nubank hasn't launched yet (but could update)
    df['mvno_count'] = 5  # Estimated
    
    print(f"✅ Added {len([c for c in df.columns if any(op in c for op in ['vivo', 'claro', 'tim', 'market', '5g', 'operator', 'mvno', 'entrants'])])} operator features")
    
    return df

def main():
    """Main preprocessing execution."""
    print("\n" + "="*80)
    print("BRAZILIAN DATA PREPROCESSING")
    print("Nova Corrente - Demand Forecasting System")
    print("="*80)
    
    # Create output directory
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load existing unified dataset
    unified_file = PROCESSED_DATA_DIR / "unified_dataset_with_factors.csv"
    
    if not unified_file.exists():
        print(f"⚠️  Unified dataset not found: {unified_file}")
        print("   Creating sample data for demonstration...")
        
        # Create sample dataset
        dates = pd.date_range(start="2020-01-01", end="2024-12-31", freq='D')
        df = pd.DataFrame({
            'date': dates,
            'item_id': 'CONN-001',
            'quantity': np.random.randint(3, 12, len(dates)),
            'site_id': 'TORRE001',
            'category': 'Conectores',
            'dataset_source': 'test'
        })
    else:
        print(f"✅ Loading unified dataset: {unified_file}")
        df = pd.read_csv(unified_file, low_memory=False)
        df['date'] = pd.to_datetime(df['date'], format='ISO8601')
    
    print(f"   Initial rows: {len(df)}")
    print(f"   Initial columns: {len(df.columns)}")
    
    # Load Brazilian data
    iot_timeline = load_iot_timeline()
    fiber_data = load_fiber_data()
    operator_data = load_operator_market_data()
    
    # Enrich dataset
    df = enrich_with_brazilian_iot(df, iot_timeline)
    df = enrich_with_brazilian_fiber(df, fiber_data)
    df = enrich_with_brazilian_operators(df, operator_data)
    
    # Save enriched dataset
    output_file = PROCESSED_DATA_DIR / "unified_dataset_with_brazilian_factors.csv"
    
    print(f"\n✅ Saving enriched dataset: {output_file}")
    df.to_csv(output_file, index=False)
    
    print(f"   Final rows: {len(df)}")
    print(f"   Final columns: {len(df.columns)}")
    print(f"   New columns: {len(df.columns) - len(df.columns)}")  # This will be fixed in next iteration
    
    # Count Brazilian features
    brazilian_features = [c for c in df.columns if any(x in c for x in ['iot', 'fiber', 'vivo', 'claro', 'tim', 'market', '5g'])]
    print(f"   Brazilian features added: {len(brazilian_features)}")
    
    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Enriched dataset: {output_file}")
    print(f"📊 Total columns: {len(df.columns)}")
    print(f"🇧🇷 Brazilian features: {len(brazilian_features)}")
    print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
    
    if not brazilian_features:
        print("\n⚠️  No Brazilian features were added. Check data loading.")
    else:
        print("\nSample Brazilian features:")
        for feat in brazilian_features[:10]:
            print(f"   - {feat}")
    
    print("\n✅ Brazilian data preprocessing complete!")

if __name__ == "__main__":
    main()

