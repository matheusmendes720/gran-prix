"""
Main Execution Script for Nova Corrente Demand Forecasting System
Based on development plan and specifications
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add demand_forecasting to path
sys.path.insert(0, str(Path(__file__).parent))

from demand_forecasting import DemandForecastingPipeline


def create_sample_data(output_file: str = 'sample_demand_data.csv'):
    """
    Create sample data for testing if file doesn't exist.
    
    Parameters:
    -----------
    output_file : str
        Output file path
    """
    if Path(output_file).exists():
        print(f"Sample data file already exists: {output_file}")
        return
    
    print(f"Creating sample data: {output_file}")
    
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
    
    # Multiple items
    items = ['CONN-001', 'CONN-002', 'CABO-001']
    
    data_list = []
    for item_id in items:
        # Generate realistic demand patterns
        base_demand = 8 if 'CONN' in item_id else 5
        
        # Trend
        trend = np.linspace(base_demand, base_demand * 1.2, len(dates))
        
        # Seasonality
        seasonal = 2 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365.25)
        
        # Weekly pattern
        weekly = 1.5 * np.sin(np.arange(len(dates)) * 2 * np.pi / 7)
        
        # Noise
        noise = np.random.normal(0, 1, len(dates))
        
        # Demand
        demand = trend + seasonal + weekly + noise
        demand = np.maximum(0, demand)  # Ensure non-negative
        
        for i, date in enumerate(dates):
            data_list.append({
                'date': date,
                'Item_ID': item_id,
                'Quantity_Consumed': max(0, int(demand[i])),
                'Site_ID': f'SITE-{np.random.randint(1, 10):03d}',
                'Lead_Time': 14 if 'CONN' in item_id else 10
            })
    
    # Create dataframe
    df = pd.DataFrame(data_list)
    df.to_csv(output_file, index=False)
    print(f"Sample data created with {len(df)} records")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Items: {df['Item_ID'].unique().tolist()}")
    print(f"  Sites: {len(df['Site_ID'].unique())}")


def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("Nova Corrente Demand Forecasting System")
    print("Grand Prix SENAI - Demand Forecasting Solution")
    print("=" * 70)
    
    # Configuration
    config = {
        'service_level': 0.95,  # 95% service level
        'ensemble_weights': {
            'ARIMA': 0.4,
            'Prophet': 0.3,
            'LSTM': 0.3
        },
        'forecast_horizon': 30,  # 30 days ahead
        'use_ensemble': True,
        'external_features': True
    }
    
    # Data file
    data_file = 'sample_demand_data.csv'
    
    # Create sample data if needed
    if not Path(data_file).exists():
        create_sample_data(data_file)
    
    # Lead times (in days)
    lead_times = {
        'CONN-001': 14,
        'CONN-002': 14,
        'CABO-001': 10,
    }
    
    # Current stock levels
    current_stocks = {
        'CONN-001': 100,
        'CONN-002': 150,
        'CABO-001': 80,
    }
    
    # Initialize pipeline
    print("\nInitializing pipeline...")
    pipeline = DemandForecastingPipeline(config=config)
    
    # Run pipeline
    try:
        results = pipeline.run(
            data_file=data_file,
            lead_times=lead_times,
            current_stocks=current_stocks,
            target_col='Quantity_Consumed',
            output_dir='output'
        )
        
        # Display results summary
        print("\n" + "=" * 70)
        print("RESULTS SUMMARY")
        print("=" * 70)
        
        # Alerts
        if results['alerts']:
            print(f"\n🚨 ALERTS GENERATED: {len(results['alerts'])}")
            for alert_info in results['alerts']:
                print(f"\n{alert_info['alert']}")
        else:
            print("\n✅ No alerts generated - all items above reorder point")
        
        # Forecasts summary
        print(f"\n📊 FORECASTS GENERATED: {len(results['forecasts'])} items")
        for item_id, forecast_df in results['forecasts'].items():
            avg_forecast = forecast_df['forecast'].mean()
            print(f"  {item_id}: Avg daily forecast = {avg_forecast:.2f} units")
        
        # PP Summary
        print(f"\n📈 REORDER POINTS CALCULATED: {len(results['pp_results'])} items")
        for item_id, pp_info in results['pp_results'].items():
            if 'error' not in pp_info:
                print(f"  {item_id}:")
                print(f"    Current Stock: {pp_info['current_stock']:.1f}")
                print(f"    Reorder Point (PP): {pp_info['reorder_point']:.1f}")
                print(f"    Safety Stock: {pp_info['safety_stock']:.1f}")
                print(f"    Days to Rupture: {pp_info['days_to_rupture']:.1f}")
                print(f"    Status: {pp_info['stock_status'].upper()}")
        
        # Reports
        print(f"\n📄 REPORTS GENERATED:")
        for report_type, file_path in results['reports'].items():
            print(f"  {report_type}: {file_path}")
        
        print("\n" + "=" * 70)
        print("Pipeline execution completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error during pipeline execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

