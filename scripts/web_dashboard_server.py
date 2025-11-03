"""
Flask web server for interactive demand forecasting dashboard.
Serves HTML dashboard with real-time data from forecasting system.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.ensemble import EnsembleForecaster
from demand_forecasting.inventory.reorder_point import ReorderPointCalculator
from demand_forecasting.inventory.alerts import AlertSystem
from demand_forecasting.utils.config import Config
from demand_forecasting.utils.model_persistence import ModelPersistence
import pandas as pd
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

config = Config()
model_persistence = ModelPersistence()


@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('web_dashboard.html')


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/items')
def get_items():
    """Get list of available items."""
    try:
        data_path = config.get('data.path', 'data/nova_corrente_demand.csv')
        loader = DataLoader(data_path)
        data_dict = loader.preprocess(min_years=1)
        
        items = []
        for item_id, df in data_dict.items():
            items.append({
                'id': item_id,
                'records': len(df),
                'date_range': {
                    'start': df.index.min().strftime('%Y-%m-%d'),
                    'end': df.index.max().strftime('%Y-%m-%d')
                },
                'has_model': model_persistence.load_model(item_id, 'ensemble') is not None
            })
        
        return jsonify({'items': items, 'count': len(items)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/forecast/<item_id>')
def get_forecast(item_id):
    """Get forecast for specific item."""
    try:
        data_path = config.get('data.path', 'data/nova_corrente_demand.csv')
        loader = DataLoader(data_path)
        data_dict = loader.preprocess(min_years=1)
        
        if item_id not in data_dict:
            return jsonify({'error': f'Item {item_id} not found'}), 404
        
        df = data_dict[item_id]
        
        # Get quantity column
        quantity_col = None
        for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
            if col in df.columns:
                quantity_col = col
                break
        if quantity_col is None:
            quantity_col = df.select_dtypes(include=['number']).columns[0]
        
        # Load or train model
        ensemble = model_persistence.load_model(item_id, 'ensemble')
        
        if ensemble is None:
            # Train model
            ensemble = EnsembleForecaster(
                weights=config.get('models.ensemble.weights'),
                use_lstm=config.get('models.ensemble.use_lstm', True)
            )
            
            exog = None
            exog_cols = ['temperature', 'holiday']
            available_exog = [col for col in exog_cols if col in df.columns]
            if available_exog:
                exog = df[available_exog]
            
            ensemble.fit(df, quantity_col, exog)
        
        # Generate forecast
        forecast_steps = request.args.get('steps', default=30, type=int)
        
        future_exog = None
        if exog is not None:
            future_exog = pd.DataFrame({
                col: [exog[col].tail(30).mean()] * forecast_steps
                if col in exog.columns else [0] * forecast_steps
                for col in available_exog
            })
        
        forecast = ensemble.forecast(forecast_steps, df, future_exog, quantity_col)
        
        # Historical data
        historical = df[quantity_col].tail(90).reset_index()
        
        # Prepare response
        forecast_dates = pd.date_range(
            start=datetime.now(),
            periods=len(forecast),
            freq='D'
        )
        
        return jsonify({
            'item_id': item_id,
            'historical': [
                {'date': row['date'].strftime('%Y-%m-%d'), 
                 'value': float(row[quantity_col])}
                for _, row in historical.iterrows()
            ],
            'forecast': [
                {'date': date.strftime('%Y-%m-%d'), 
                 'value': float(value)}
                for date, value in zip(forecast_dates, forecast.values)
            ],
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/inventory/<item_id>')
def get_inventory(item_id):
    """Get inventory metrics for item."""
    try:
        # Get current stock from file
        stocks_file = Path('data/current_stocks.json')
        if stocks_file.exists():
            with open(stocks_file, 'r') as f:
                current_stocks = json.load(f)
        else:
            current_stocks = {}
        
        current_stock = current_stocks.get(item_id, 0)
        
        # Get forecast
        forecast_response = get_forecast(item_id)
        if forecast_response.status_code != 200:
            return forecast_response
        
        forecast_data = forecast_response.get_json()
        forecast_series = pd.Series([f['value'] for f in forecast_data['forecast']])
        
        # Calculate reorder point
        pp_calc = ReorderPointCalculator(
            service_level=config.get('forecasting.service_level', 0.95)
        )
        lead_time = config.get('forecasting.lead_time', 14)
        
        pp_metrics = pp_calc.compute_all(forecast_series, lead_time, current_stock)
        
        # Check alerts
        alert_system = AlertSystem()
        alert = alert_system.check_reorder_alert(
            current_stock,
            pp_metrics['reorder_point'],
            pp_metrics['days_to_rupture'],
            item_id
        )
        
        return jsonify({
            'item_id': item_id,
            'inventory_metrics': {
                'current_stock': float(pp_metrics['current_stock']),
                'reorder_point': float(pp_metrics['reorder_point']),
                'safety_stock': float(pp_metrics['safety_stock']),
                'avg_daily_demand': float(pp_metrics['avg_daily_demand']),
                'days_to_rupture': float(pp_metrics['days_to_rupture']),
                'lead_time': int(pp_metrics['lead_time']),
                'service_level': float(pp_metrics['service_level'])
            },
            'alert': {
                'triggered': alert['alert_triggered'],
                'urgency': alert['urgency'],
                'units_needed': int(alert['units_needed'])
            },
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics')
def get_metrics():
    """Get system-wide metrics."""
    try:
        data_path = config.get('data.path', 'data/nova_corrente_demand.csv')
        
        # Count datasets
        datasets_count = 0
        total_records = 0
        
        try:
            loader = DataLoader(data_path)
            data_dict = loader.preprocess(min_years=1)
            datasets_count = len(data_dict)
            total_records = sum(len(df) for df in data_dict.values())
        except:
            pass
        
        # Count models
        models = model_persistence.list_models()
        models_count = len(models)
        
        return jsonify({
            'datasets': datasets_count,
            'total_records': total_records,
            'trained_models': models_count,
            'status': 'online',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Web dashboard server')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host address')
    parser.add_argument('--port', type=int, default=8080, help='Port number')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create templates and static directories
    templates_dir = Path(__file__).parent.parent / 'templates'
    static_dir = Path(__file__).parent.parent / 'static'
    templates_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*60}")
    print("Demand Forecasting Web Dashboard Server")
    print(f"{'='*60}")
    print(f"Starting server on http://{args.host}:{args.port}")
    print(f"Dashboard: http://{args.host}:{args.port}/")
    print(f"API: http://{args.host}:{args.port}/api/")
    print(f"{'='*60}\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug)









