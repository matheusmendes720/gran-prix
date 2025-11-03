"""
Scheduled forecasting task.
Run daily forecasts automatically (for cron/Airflow integration).
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.ensemble import EnsembleForecaster
from demand_forecasting.inventory.reorder_point import ReorderPointCalculator
from demand_forecasting.inventory.alerts import AlertSystem
from demand_forecasting.reporting.report_generator import ReportGenerator
from demand_forecasting.utils.config import Config
from demand_forecasting.utils.model_persistence import ModelPersistence
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')


class ScheduledForecaster:
    """Scheduled forecasting task runner."""
    
    def __init__(self, config_path: str = None):
        """Initialize scheduled forecaster."""
        self.config = Config(config_path)
        self.model_persistence = ModelPersistence()
        self.output_dir = Path(self.config.get('reporting.output_dir', 'reports'))
        self.output_dir.mkdir(exist_ok=True)
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
    
    def load_current_stocks(self, stocks_file: str = 'data/current_stocks.json') -> dict:
        """Load current stock levels from file or database."""
        stocks_path = Path(stocks_file)
        
        if stocks_path.exists():
            with open(stocks_path, 'r') as f:
                return json.load(f)
        
        # Return default if file doesn't exist
        return {}
    
    def save_current_stocks(self, stocks: dict, stocks_file: str = 'data/current_stocks.json'):
        """Save current stock levels to file."""
        stocks_path = Path(stocks_file)
        stocks_path.parent.mkdir(exist_ok=True)
        
        with open(stocks_path, 'w') as f:
            json.dump(stocks, f, indent=2)
    
    def run_daily_forecast(self, data_path: str = None, 
                          stocks_file: str = 'data/current_stocks.json') -> dict:
        """
        Run daily forecasting task.
        
        Args:
            data_path: Path to data file (uses config if None)
            stocks_file: Path to current stocks file
        
        Returns:
            Dictionary with results
        """
        timestamp = datetime.now()
        print(f"\n{'='*60}")
        print(f"Daily Forecast Run - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Load data
        data_path = data_path or self.config.get('data.path', 'data/nova_corrente_demand.csv')
        
        if not os.path.exists(data_path):
            print(f"Error: Data file not found: {data_path}")
            return {'status': 'error', 'message': f'Data file not found: {data_path}'}
        
        try:
            loader = DataLoader(data_path)
            data_dict = loader.preprocess(
                external_features=self.config.get('data.external_features', True),
                min_years=self.config.get('data.min_years', 2)
            )
        except Exception as e:
            print(f"Error loading data: {e}")
            return {'status': 'error', 'message': str(e)}
        
        print(f"Loaded data for {len(data_dict)} items\n")
        
        # Load current stocks
        current_stocks = self.load_current_stocks(stocks_file)
        
        # Initialize components
        pp_calculator = ReorderPointCalculator(
            service_level=self.config.get('forecasting.service_level', 0.95)
        )
        alert_system = AlertSystem(
            email_config=self.config.get('alerts.email_config') 
            if self.config.get('alerts.enabled', False) else None
        )
        report_gen = ReportGenerator()
        
        forecast_steps = self.config.get('forecasting.forecast_steps', 30)
        lead_time = self.config.get('forecasting.lead_time', 14)
        
        results = {}
        summary = {
            'timestamp': timestamp.isoformat(),
            'items_processed': 0,
            'items_with_alerts': 0,
            'total_alerts': 0
        }
        
        # Process each item
        for item_id, df in data_dict.items():
            print(f"Processing {item_id}...")
            
            try:
                # Get quantity column
                quantity_col = None
                for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
                    if col in df.columns:
                        quantity_col = col
                        break
                
                if quantity_col is None:
                    quantity_col = df.select_dtypes(include=['number']).columns[0]
                
                # Load or train model
                ensemble = self.model_persistence.load_model(item_id, 'ensemble')
                
                if ensemble is None:
                    print(f"  Training new model for {item_id}...")
                    
                    ensemble = EnsembleForecaster(
                        weights=self.config.get('models.ensemble.weights'),
                        use_lstm=self.config.get('models.ensemble.use_lstm', True)
                    )
                    
                    # External regressors
                    exog = None
                    exog_cols = ['temperature', 'holiday']
                    available_exog = [col for col in exog_cols if col in df.columns]
                    if available_exog:
                        exog = df[available_exog]
                    
                    train = df
                    train_exog = exog if exog is not None else None
                    ensemble.fit(train, quantity_col, train_exog)
                    
                    # Save model
                    metadata = {
                        'item_id': item_id,
                        'training_date': timestamp.isoformat(),
                        'data_points': len(df)
                    }
                    self.model_persistence.save_model(ensemble, item_id, 'ensemble', metadata)
                else:
                    print(f"  Using existing model for {item_id}")
                
                # Generate forecast
                future_exog = None
                if 'temperature' in df.columns or 'holiday' in df.columns:
                    future_exog = pd.DataFrame({
                        col: [df[col].tail(30).mean()] * forecast_steps
                        if col in df.columns else [0] * forecast_steps
                        for col in ['temperature', 'holiday']
                    })
                
                forecast = ensemble.forecast(forecast_steps, df, future_exog, quantity_col)
                
                # Calculate reorder point
                current_stock = current_stocks.get(item_id, 0)
                pp_metrics = pp_calculator.compute_all(forecast, lead_time, current_stock)
                
                # Check alerts
                alert = alert_system.check_reorder_alert(
                    current_stock,
                    pp_metrics['reorder_point'],
                    pp_metrics['days_to_rupture'],
                    item_id
                )
                
                # Store results
                results[item_id] = {
                    'forecast': forecast,
                    'pp_metrics': pp_metrics,
                    'alert': alert
                }
                
                summary['items_processed'] += 1
                
                if alert['alert_triggered']:
                    summary['items_with_alerts'] += 1
                    summary['total_alerts'] += 1
                    print(f"  ⚠️  ALERT: {alert['urgency'].upper()}")
                else:
                    print(f"  ✓ OK")
            
            except Exception as e:
                print(f"  ✗ Error: {e}")
                results[item_id] = {'error': str(e)}
        
        # Generate reports
        print(f"\n{'='*60}")
        print("Generating Reports...")
        print(f"{'='*60}")
        
        if results:
            date_str = timestamp.strftime('%Y%m%d')
            
            # CSV report
            csv_path = self.output_dir / f"forecast_report_{date_str}.csv"
            try:
                report_gen.generate_csv_report(results, str(csv_path))
                print(f"✓ CSV report: {csv_path}")
            except Exception as e:
                print(f"⚠️  CSV report error: {e}")
            
            # PDF report
            pdf_path = self.output_dir / f"forecast_report_{date_str}.pdf"
            try:
                report_gen.generate_pdf_report(results, str(pdf_path))
                print(f"✓ PDF report: {pdf_path}")
            except Exception as e:
                print(f"⚠️  PDF report error: {e}")
        
        # Save summary log
        log_path = self.log_dir / f"forecast_run_{date_str}.json"
        with open(log_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n{'='*60}")
        print("Summary:")
        print(f"{'='*60}")
        print(f"Items Processed: {summary['items_processed']}")
        print(f"Items with Alerts: {summary['items_with_alerts']}")
        print(f"Total Alerts: {summary['total_alerts']}")
        print(f"Log: {log_path}")
        print(f"{'='*60}\n")
        
        return {
            'status': 'success',
            'summary': summary,
            'results': results
        }


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run scheduled forecasting task')
    parser.add_argument('--data', type=str, default=None,
                       help='Path to data file (uses config if not provided)')
    parser.add_argument('--stocks', type=str, default='data/current_stocks.json',
                       help='Path to current stocks file')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to config file')
    
    args = parser.parse_args()
    
    forecaster = ScheduledForecaster(args.config)
    results = forecaster.run_daily_forecast(args.data, args.stocks)
    
    if results.get('status') == 'error':
        sys.exit(1)


if __name__ == '__main__':
    main()

