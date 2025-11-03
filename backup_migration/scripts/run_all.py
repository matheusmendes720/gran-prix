"""
Master script to run the entire demand forecasting system.
Orchestrates data loading, training, forecasting, and reporting.
"""
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

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
from demand_forecasting.utils.model_persistence import ModelPersistence
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')


def create_sample_data(data_path: str = 'data/nova_corrente_demand.csv'):
    """Create sample data if it doesn't exist."""
    print(f"\n{'='*60}")
    print("Creating Sample Data...")
    print(f"{'='*60}")
    
    data_file = Path(data_path)
    data_file.parent.mkdir(exist_ok=True, parents=True)
    
    import numpy as np
    
    dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    
    data = []
    items = ['CONN-001', 'CABO-001', 'FUS-001']
    
    for item in items:
        base_demand = {'CONN-001': 10, 'CABO-001': 15, 'FUS-001': 8}[item]
        trend = np.linspace(0, 5, len(dates))
        seasonal = 3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        noise = np.random.normal(0, 2, len(dates))
        
        demand = base_demand + trend + seasonal + noise
        demand = np.maximum(demand, 1)
        
        for date, qty in zip(dates, demand):
            data.append({
                'date': date,
                'Item_ID': item,
                'Quantity_Consumed': round(qty, 2),
                'Site_ID': 'SITE-001',
                'Lead_Time': 14
            })
    
    df = pd.DataFrame(data)
    df.to_csv(data_path, index=False)
    
    print(f"[OK] Sample data created: {data_path}")
    print(f"  Items: {items}")
    print(f"  Date range: {dates.min().date()} to {dates.max().date()}")
    print(f"  Total records: {len(df)}")
    
    return df


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Run complete demand forecasting system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with sample data (creates if needed)
  python scripts/run_all.py
  
  # Run with custom data file
  python scripts/run_all.py --data data/my_data.csv
  
  # Run without training models (use existing)
  python scripts/run_all.py --skip-training
  
  # Run without visualizations (faster)
  python scripts/run_all.py --no-viz
  
  # Run with custom config
  python scripts/run_all.py --config custom_config.yaml
        """
    )
    
    parser.add_argument('--data', type=str, default='data/nova_corrente_demand.csv',
                       help='Path to data file')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to config file')
    parser.add_argument('--skip-training', action='store_true',
                       help='Skip model training (use existing models)')
    parser.add_argument('--no-viz', action='store_true',
                       help='Skip visualization generation')
    parser.add_argument('--item', type=str, default=None,
                       help='Process specific item only')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create sample data file')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print(" "*25 + "DEMAND FORECASTING SYSTEM")
    print(" "*20 + "Nova Corrente - Complete Run")
    print("="*80)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data file: {args.data}")
    print(f"Config file: {args.config}")
    print("\n" + "="*80 + "\n")
    
    # Load configuration
    config = Config(args.config)
    
    # Check/create data file
    data_path = Path(args.data)
    if not data_path.exists() or args.create_sample:
        print("[WARNING] Data file not found or --create-sample specified")
        create_sample_data(str(data_path))
        print()
    
    if not data_path.exists():
        print(f"[ERROR] Data file not found: {args.data}")
        print("   Use --create-sample to create sample data")
        return 1
    
    # Initialize components
    output_dir = Path(config.get('reporting.output_dir', 'reports'))
    output_dir.mkdir(exist_ok=True, parents=True)
    
    model_persistence = ModelPersistence()
    
    # Load current stocks (create sample if needed)
    stocks_file = Path('data/current_stocks.json')
    if not stocks_file.exists():
        stocks_file.parent.mkdir(exist_ok=True, parents=True)
        sample_stocks = {
            'CONN-001': 100,
            'CABO-001': 150,
            'FUS-001': 80
        }
        with open(stocks_file, 'w') as f:
            json.dump(sample_stocks, f, indent=2)
        print(f"[OK] Created sample stocks file: {stocks_file}")
    
    with open(stocks_file, 'r') as f:
        current_stocks = json.load(f)
    
    # Load data
    print("\n" + "="*80)
    print("STEP 1: Loading and Preprocessing Data")
    print("="*80)
    
    try:
        loader = DataLoader(str(data_path))
        data_dict = loader.preprocess(
            external_features=config.get('data.external_features', True),
            min_years=config.get('data.min_years', 1)  # Reduced for sample data
        )
        print(f"[OK] Loaded data for {len(data_dict)} items")
        
        if args.item:
            if args.item not in data_dict:
                print(f"[ERROR] Item {args.item} not found in data")
                return 1
            data_dict = {args.item: data_dict[args.item]}
            print(f"[OK] Processing item: {args.item}")
    
    except Exception as e:
        print(f"[ERROR] Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Select items to process
    items_to_process = list(data_dict.keys())
    if args.item:
        items_to_process = [args.item]
    
    # Initialize components
    ensemble = EnsembleForecaster(
        weights=config.get('models.ensemble.weights'),
        use_lstm=config.get('models.ensemble.use_lstm', True)
    )
    pp_calculator = ReorderPointCalculator(
        service_level=config.get('forecasting.service_level', 0.95)
    )
    alert_system = AlertSystem(
        email_config=config.get('alerts.email_config') 
        if config.get('alerts.enabled', False) else None
    )
    metrics = ValidationMetrics()
    report_gen = ReportGenerator()
    viz = Visualization()
    
    forecast_steps = config.get('forecasting.forecast_steps', 30)
    lead_time = config.get('forecasting.lead_time', 14)
    
    results = {}
    summary = {
        'timestamp': datetime.now().isoformat(),
        'items_processed': 0,
        'items_with_alerts': 0,
        'total_alerts': 0,
        'training_performed': not args.skip_training
    }
    
    # Process each item
    print("\n" + "="*80)
    print("STEP 2: Processing Items")
    print("="*80)
    
    for item_id in items_to_process:
        print(f"\n{'─'*80}")
        print(f"Processing: {item_id}")
        print(f"{'─'*80}")
        
        try:
            df = data_dict[item_id]
            
            # Get quantity column
            quantity_col = None
            for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
                if col in df.columns:
                    quantity_col = col
                    break
            
            if quantity_col is None:
                quantity_col = df.select_dtypes(include=['number']).columns[0]
            
            print(f"  Quantity column: {quantity_col}")
            print(f"  Data points: {len(df)}")
            print(f"  Date range: {df.index.min().date()} to {df.index.max().date()}")
            
            # Train or load model
            if args.skip_training:
                print(f"\n  [Model] Loading existing model...")
                ensemble = model_persistence.load_model(item_id, 'ensemble')
                
                if ensemble is None:
                    print(f"  [WARNING] No existing model found, training new model...")
                    args.skip_training = False
            
            if not args.skip_training:
                print(f"\n  [Model] Training ensemble...")
                
                # Split data for training
                train, test = loader.train_test_split(df, test_size=0.2)
                print(f"    Training: {len(train)} days")
                print(f"    Test: {len(test)} days")
                
                # External regressors
                exog = None
                exog_cols = ['temperature', 'holiday']
                available_exog = [col for col in exog_cols if col in df.columns]
                if available_exog:
                    exog = df[available_exog]
                    train_exog = exog.loc[train.index]
                    print(f"    External regressors: {available_exog}")
                else:
                    train_exog = None
                
                # Fit models
                fit_results = ensemble.fit(train, quantity_col, train_exog)
                
                for model_name, result in fit_results.items():
                    if 'Fitted successfully' in str(result):
                        print(f"      [OK] {model_name}")
                    else:
                        print(f"      ✗ {model_name}: {result}")
                
                # Save model
                metadata = {
                    'item_id': item_id,
                    'training_date': datetime.now().isoformat(),
                    'data_points': len(train)
                }
                model_path = model_persistence.save_model(ensemble, item_id, 'ensemble', metadata)
                print(f"    [OK] Model saved: {model_path}")
            
            # Generate forecast
            print(f"\n  [Forecast] Generating {forecast_steps}-day forecast...")
            
            # Prepare future external features
            future_exog = None
            if exog is not None:
                future_exog = pd.DataFrame({
                    col: [exog[col].tail(30).mean()] * forecast_steps
                    if col in exog.columns else [0] * forecast_steps
                    for col in available_exog
                })
            
            forecast = ensemble.forecast(forecast_steps, df, future_exog, quantity_col)
            print(f"    [OK] Generated forecast: {len(forecast)} days")
            print(f"    Average daily demand: {forecast.mean():.2f}")
            
            # Calculate reorder point
            current_stock = current_stocks.get(item_id, 0)
            pp_metrics = pp_calculator.compute_all(forecast, lead_time, current_stock)
            
            print(f"\n  [Inventory] Calculating reorder point...")
            print(f"    Current Stock: {pp_metrics['current_stock']:.0f} units")
            print(f"    Reorder Point: {pp_metrics['reorder_point']:.0f} units")
            print(f"    Safety Stock: {pp_metrics['safety_stock']:.0f} units")
            print(f"    Days to Rupture: {pp_metrics['days_to_rupture']:.1f} days")
            
            # Check alerts
            alert = alert_system.check_reorder_alert(
                current_stock,
                pp_metrics['reorder_point'],
                pp_metrics['days_to_rupture'],
                item_id
            )
            
            if alert['alert_triggered']:
                print(f"    [ALERT] {alert['urgency'].upper()}")
                summary['items_with_alerts'] += 1
                summary['total_alerts'] += 1
            
            # Evaluate on test set
            if not args.skip_training and len(test) > 0 and len(test) >= 7:
                print(f"\n  [Evaluation] Evaluating on test set...")
                try:
                    test_exog = exog.loc[test.index] if exog is not None else None
                    test_forecast = ensemble.forecast(len(test), train, test_exog, quantity_col)
                    
                    test_quantity = test[quantity_col] if quantity_col in test.columns else test.iloc[:, 0]
                    eval_metrics = metrics.calculate_all(test_quantity, test_forecast)
                    
                    print(f"    MAPE: {eval_metrics['MAPE_percent']:.2f}%")
                    print(f"    RMSE: {eval_metrics['RMSE']:.2f}")
                    print(f"    MAE: {eval_metrics['MAE']:.2f}")
                    print(f"    R²: {eval_metrics['R2']:.2f}")
                except Exception as e:
                    print(f"    [WARNING] Evaluation error: {e}")
            
            # Store results
            results[item_id] = {
                'forecast': forecast,
                'pp_metrics': pp_metrics,
                'alert': alert,
                'ensemble_forecasts': ensemble.forecasts if hasattr(ensemble, 'forecasts') else {}
            }
            
            summary['items_processed'] += 1
            
        except Exception as e:
            print(f"  [ERROR] Error processing {item_id}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Generate reports
    print("\n" + "="*80)
    print("STEP 3: Generating Reports")
    print("="*80)
    
    if results:
        date_str = datetime.now().strftime('%Y%m%d')
        
        # CSV report
        csv_path = output_dir / f"forecast_report_{date_str}.csv"
        try:
            report_gen.generate_csv_report(results, str(csv_path))
            print(f"[OK] CSV report: {csv_path}")
        except Exception as e:
            print(f"[WARNING] CSV report error: {e}")
        
        # PDF report
        pdf_path = output_dir / f"forecast_report_{date_str}.pdf"
        try:
            report_gen.generate_pdf_report(results, str(pdf_path))
            print(f"[OK] PDF report: {pdf_path}")
        except Exception as e:
            print(f"[WARNING] PDF report error: {e}")
        
        # Visualizations
        if not args.no_viz:
            print(f"\n  Generating visualizations...")
            for item_id, item_results in results.items():
                try:
                    forecast = item_results['forecast']
                    df = data_dict[item_id]
                    
                    # Get quantity column
                    quantity_col = None
                    for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
                        if col in df.columns:
                            quantity_col = col
                            break
                    if quantity_col is None:
                        quantity_col = df.select_dtypes(include=['number']).columns[0]
                    
                    train = df.iloc[:int(len(df) * 0.8)]
                    historical = train[quantity_col] if quantity_col in train.columns else train.iloc[:, 0]
                    
                    # Forecast plot
                    viz_path = output_dir / f"forecast_{item_id}_{date_str}.png"
                    viz.plot_forecast(historical, forecast, item_id=item_id, save_path=str(viz_path))
                    
                    # Inventory metrics
                    metrics_path = output_dir / f"inventory_{item_id}_{date_str}.png"
                    viz.plot_inventory_metrics(item_results['pp_metrics'], item_id=item_id, save_path=str(metrics_path))
                    
                    print(f"    [OK] {item_id}")
                except Exception as e:
                    print(f"    [WARNING] {item_id}: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Items Processed: {summary['items_processed']}")
    print(f"Items with Alerts: {summary['items_with_alerts']}")
    print(f"Total Alerts: {summary['total_alerts']}")
    print(f"Training Performed: {summary['training_performed']}")
    print(f"\nReports Directory: {output_dir.absolute()}")
    print("="*80)
    
    if summary['total_alerts'] > 0:
        print("\n[ALERT SUMMARY]")
        print("─"*80)
        alert_summary = alert_system.get_alerts_summary()
        print(f"Total Alerts: {alert_summary['total_alerts']}")
        print(f"By Urgency: {alert_summary['by_urgency']}")
    
    print("\n[SUCCESS] Forecast run completed successfully!")
    print("="*80 + "\n")
    
    return 0


def main_wrapper():
    """Wrapper to handle exit codes properly."""
    try:
        return main()
    except KeyboardInterrupt:
        print("\n\n[WARNING] Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main_wrapper())

