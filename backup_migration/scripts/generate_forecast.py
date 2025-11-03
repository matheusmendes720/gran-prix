"""
Main execution script for demand forecasting.
Processes data, generates forecasts, calculates reorder points, and generates reports.
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.ensemble import EnsembleForecaster
from demand_forecasting.inventory.reorder_point import ReorderPointCalculator
from demand_forecasting.inventory.alerts import AlertSystem
from demand_forecasting.validation.metrics import ValidationMetrics
from demand_forecasting.reporting.report_generator import ReportGenerator
from demand_forecasting.reporting.visualization import Visualization
from demand_forecasting.utils.config import Config
import pandas as pd
from typing import Dict
import warnings
warnings.filterwarnings('ignore')


def main():
    """Main execution function."""
    print("=" * 60)
    print("Demand Forecasting System - Nova Corrente")
    print("=" * 60)
    
    # Load configuration
    config = Config()
    
    # Configuration parameters
    data_path = config.get('data.path', 'data/nova_corrente_demand.csv')
    forecast_steps = config.get('forecasting.forecast_steps', 30)
    lead_time = config.get('forecasting.lead_time', 14)
    service_level = config.get('forecasting.service_level', 0.95)
    
    # Create output directory
    output_dir = config.get('reporting.output_dir', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    # Current stock (in production, load from inventory system)
    # TODO: Load from inventory management system
    current_stocks = {
        'CONN-001': 100,
        'CABO-001': 150,
        # Add more items as needed
    }
    
    print(f"\nLoading data from: {data_path}")
    
    # Check if data file exists
    if not os.path.exists(data_path):
        print(f"Warning: Data file not found at {data_path}")
        print("Creating sample data file...")
        create_sample_data(data_path)
        print(f"Sample data created at {data_path}")
        print("Please update with your actual data.")
    
    # Initialize components
    try:
        loader = DataLoader(data_path)
        data_dict = loader.preprocess(
            external_features=config.get('data.external_features', True),
            min_years=config.get('data.min_years', 2)
        )
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    print(f"Loaded data for {len(data_dict)} items")
    
    # Initialize forecasters and calculators
    ensemble = EnsembleForecaster(
        weights=config.get('models.ensemble.weights'),
        use_lstm=config.get('models.ensemble.use_lstm', True)
    )
    pp_calculator = ReorderPointCalculator(service_level=service_level)
    alert_system = AlertSystem(
        email_config=config.get('alerts.email_config') if config.get('alerts.enabled') else None
    )
    metrics = ValidationMetrics()
    report_gen = ReportGenerator()
    viz = Visualization()
    
    results = {}
    
    print("\n" + "=" * 60)
    print("Processing Items...")
    print("=" * 60)
    
    # Process each item
    for item_id, df in data_dict.items():
        print(f"\nProcessing {item_id}...")
        
        # Prepare features
        quantity_col = None
        for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
            if col in df.columns:
                quantity_col = col
                break
        
        if quantity_col is None:
            # Use first numeric column
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                quantity_col = numeric_cols[0]
            else:
                print(f"  ⚠️  No quantity column found for {item_id}. Skipping.")
                continue
        
        # External regressors
        exog = None
        exog_cols = ['temperature', 'holiday']
        available_exog = [col for col in exog_cols if col in df.columns]
        if available_exog:
            exog = df[available_exog]
        
        # Split data for validation
        train, test = loader.train_test_split(df, test_size=0.2)
        
        print(f"  Training data: {len(train)} days")
        print(f"  Test data: {len(test)} days")
        
        # Fit models
        print("  Fitting ensemble models...")
        try:
            train_exog = exog.loc[train.index] if exog is not None else None
            fit_results = ensemble.fit(train, quantity_col, train_exog)
            
            for model_name, result in fit_results.items():
                if 'Fitted successfully' in str(result):
                    print(f"    ✓ {model_name}: Success")
                else:
                    print(f"    ✗ {model_name}: {result}")
        
        except Exception as e:
            print(f"  ⚠️  Error fitting models: {e}")
            continue
        
        # Generate forecast
        print("  Generating forecast...")
        try:
            # Generate future external features
            future_exog = None
            if exog is not None:
                # Use mean of last 30 days or last value
                future_exog = pd.DataFrame({
                    col: [exog[col].tail(30).mean()] * forecast_steps
                    if col in exog.columns else [0] * forecast_steps
                    for col in available_exog
                })
            
            forecast = ensemble.forecast(forecast_steps, train, future_exog, quantity_col)
            print(f"    Generated {len(forecast)}-day forecast")
        
        except Exception as e:
            print(f"  ⚠️  Error generating forecast: {e}")
            continue
        
        # Calculate reorder point
        current_stock = current_stocks.get(item_id, 0)
        pp_metrics = pp_calculator.compute_all(forecast, lead_time, current_stock)
        
        print(f"    Current Stock: {pp_metrics['current_stock']:.0f} units")
        print(f"    Reorder Point: {pp_metrics['reorder_point']:.0f} units")
        print(f"    Safety Stock: {pp_metrics['safety_stock']:.0f} units")
        print(f"    Avg Daily Demand: {pp_metrics['avg_daily_demand']:.2f} units")
        
        # Check alerts
        alert = alert_system.check_reorder_alert(
            current_stock,
            pp_metrics['reorder_point'],
            pp_metrics['days_to_rupture'],
            item_id,
            config.get('alerts.urgency_thresholds')
        )
        
        print(f"    Days to Rupture: {pp_metrics['days_to_rupture']:.1f} days")
        if alert['alert_triggered']:
            print(f"    ⚠️  ALERT: {alert['urgency'].upper()} - {alert['message']}")
        
        # Evaluate on test set if available
        if len(test) > 0 and len(test) >= 7:  # At least 7 days for meaningful evaluation
            print("  Evaluating on test set...")
            try:
                test_exog = exog.loc[test.index] if exog is not None else None
                test_forecast = ensemble.forecast(len(test), train, test_exog, quantity_col)
                
                eval_metrics = metrics.calculate_all(test[quantity_col], test_forecast)
                print(f"    MAPE: {eval_metrics['MAPE_percent']:.2f}%")
                print(f"    RMSE: {eval_metrics['RMSE']:.2f}")
                print(f"    MAE: {eval_metrics['MAE']:.2f}")
            
            except Exception as e:
                print(f"    ⚠️  Evaluation error: {e}")
        
        # Store results
        results[item_id] = {
            'forecast': forecast,
            'pp_metrics': pp_metrics,
            'alert': alert,
            'ensemble_forecasts': ensemble.forecasts
        }
    
    # Generate reports
    print("\n" + "=" * 60)
    print("Generating Reports...")
    print("=" * 60)
    
    if results:
        # CSV report
        csv_path = os.path.join(output_dir, f"forecast_report_{pd.Timestamp.now().strftime('%Y%m%d')}.csv")
        try:
            report_gen.generate_csv_report(results, csv_path)
            print(f"✓ CSV report: {csv_path}")
        except Exception as e:
            print(f"⚠️  CSV report error: {e}")
        
        # PDF report
        pdf_path = os.path.join(output_dir, f"forecast_report_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf")
        try:
            report_gen.generate_pdf_report(results, pdf_path)
            print(f"✓ PDF report: {pdf_path}")
        except Exception as e:
            print(f"⚠️  PDF report error: {e}")
        
        # Visualizations
        if config.get('reporting.visualizations', True):
            print("\nGenerating visualizations...")
            for item_id, item_results in results.items():
                try:
                    forecast = item_results['forecast']
                    train = data_dict[item_id].iloc[:int(len(data_dict[item_id]) * 0.8)]
                    historical = train.iloc[:, 0] if len(train.columns) > 0 else train.iloc[:, 0]
                    
                    # Forecast plot
                    viz_path = os.path.join(output_dir, f"forecast_{item_id}_{pd.Timestamp.now().strftime('%Y%m%d')}.png")
                    viz.plot_forecast(historical, forecast, item_id=item_id, save_path=viz_path)
                    
                    # Inventory metrics plot
                    metrics_path = os.path.join(output_dir, f"inventory_{item_id}_{pd.Timestamp.now().strftime('%Y%m%d')}.png")
                    viz.plot_inventory_metrics(item_results['pp_metrics'], item_id=item_id, save_path=metrics_path)
                    
                    print(f"  ✓ Visualizations for {item_id}")
                
                except Exception as e:
                    print(f"  ⚠️  Visualization error for {item_id}: {e}")
    
    # Alerts summary
    if alert_system.alerts_log:
        print("\n" + "=" * 60)
        print("Alerts Summary")
        print("=" * 60)
        summary = alert_system.get_alerts_summary()
        print(f"Total Alerts: {summary['total_alerts']}")
        print(f"By Urgency: {summary['by_urgency']}")
    
    print("\n" + "=" * 60)
    print("Forecasting Complete!")
    print("=" * 60)
    
    return results


def create_sample_data(file_path: str):
    """Create sample data file for testing."""
    import numpy as np
    
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    
    data = []
    items = ['CONN-001', 'CABO-001']
    
    for item in items:
        # Generate synthetic demand with seasonality
        base_demand = 10 if item == 'CONN-001' else 15
        trend = np.linspace(0, 5, len(dates))
        seasonal = 3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        noise = np.random.normal(0, 2, len(dates))
        
        demand = base_demand + trend + seasonal + noise
        demand = np.maximum(demand, 1)  # Ensure positive
        
        for date, qty in zip(dates, demand):
            data.append({
                'date': date,
                'Item_ID': item,
                'Quantity_Consumed': qty,
                'Site_ID': 'SITE-001',
                'Lead_Time': 14
            })
    
    df = pd.DataFrame(data)
    
    # Create directory if needed
    os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
    
    df.to_csv(file_path, index=False)
    print(f"Sample data created: {file_path}")


if __name__ == '__main__':
    results = main()

