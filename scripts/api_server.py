"""
Flask API server for demand forecasting.
RESTful API for generating forecasts and managing inventory.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, request, jsonify
from flask_cors import CORS
from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.ensemble import EnsembleForecaster
from demand_forecasting.inventory.reorder_point import ReorderPointCalculator
from demand_forecasting.inventory.alerts import AlertSystem
from demand_forecasting.utils.config import Config
from demand_forecasting.utils.model_persistence import ModelPersistence
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

config = Config()
model_persistence = ModelPersistence()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/forecast', methods=['POST'])
def generate_forecast():
    """
    Generate demand forecast for an item.
    
    Request body:
    {
        "item_id": "CONN-001",
        "data": [...],  # Historical data
        "forecast_days": 30,
        "lead_time": 14,
        "current_stock": 100,
        "service_level": 0.95
    }
    """
    try:
        data = request.json
        
        item_id = data.get('item_id')
        historical_data = data.get('data')
        forecast_days = data.get('forecast_days', 30)
        lead_time = data.get('lead_time', 14)
        current_stock = data.get('current_stock', 0)
        service_level = data.get('service_level', 0.95)
        
        if not item_id or not historical_data:
            return jsonify({'error': 'item_id and data are required'}), 400
        
        # Convert data to DataFrame
        df = pd.DataFrame(historical_data)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
        
        # Get quantity column
        quantity_col = None
        for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
            if col in df.columns:
                quantity_col = col
                break
        
        if quantity_col is None:
            quantity_col = df.select_dtypes(include=['number']).columns[0]
        
        # Load or train model
        # Try loading existing model first
        ensemble = model_persistence.load_model(item_id, 'ensemble')
        
        if ensemble is None:
            # Train new model
            ensemble = EnsembleForecaster(
                weights=config.get('models.ensemble.weights'),
                use_lstm=config.get('models.ensemble.use_lstm', True)
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
        
        # Generate forecast
        future_exog = None
        if 'temperature' in df.columns or 'holiday' in df.columns:
            # Generate future external features
            future_exog = pd.DataFrame({
                col: [df[col].tail(30).mean()] * forecast_days
                if col in df.columns else [0] * forecast_days
                for col in ['temperature', 'holiday']
            })
        
        forecast = ensemble.forecast(forecast_days, df, future_exog, quantity_col)
        
        # Calculate reorder point
        pp_calc = ReorderPointCalculator(service_level=service_level)
        pp_metrics = pp_calc.compute_all(forecast, lead_time, current_stock)
        
        # Check alerts
        alert_system = AlertSystem()
        alert = alert_system.check_reorder_alert(
            current_stock,
            pp_metrics['reorder_point'],
            pp_metrics['days_to_rupture'],
            item_id
        )
        
        # Prepare response
        forecast_dates = pd.date_range(
            start=datetime.now(),
            periods=len(forecast),
            freq='D'
        )
        
        response = {
            'item_id': item_id,
            'forecast': [
                {
                    'date': date.strftime('%Y-%m-%d'),
                    'value': float(value)
                }
                for date, value in zip(forecast_dates, forecast.values)
            ],
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
                'message': alert['message'],
                'units_needed': int(alert['units_needed'])
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/train', methods=['POST'])
def train_model():
    """
    Train model for an item.
    
    Request body:
    {
        "item_id": "CONN-001",
        "data": [...],  # Historical data
        "save_model": true
    }
    """
    try:
        data = request.json
        
        item_id = data.get('item_id')
        historical_data = data.get('data')
        save_model = data.get('save_model', True)
        
        if not item_id or not historical_data:
            return jsonify({'error': 'item_id and data are required'}), 400
        
        # Convert data to DataFrame
        df = pd.DataFrame(historical_data)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
        
        # Get quantity column
        quantity_col = None
        for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
            if col in df.columns:
                quantity_col = col
                break
        
        if quantity_col is None:
            quantity_col = df.select_dtypes(include=['number']).columns[0]
        
        # Train model
        ensemble = EnsembleForecaster(
            weights=config.get('models.ensemble.weights'),
            use_lstm=config.get('models.ensemble.use_lstm', True)
        )
        
        # External regressors
        exog = None
        exog_cols = ['temperature', 'holiday']
        available_exog = [col for col in exog_cols if col in df.columns]
        if available_exog:
            exog = df[available_exog]
        
        train_exog = exog if exog is not None else None
        fit_results = ensemble.fit(df, quantity_col, train_exog)
        
        # Save model if requested
        model_path = None
        if save_model:
            metadata = {
                'item_id': item_id,
                'training_date': datetime.now().isoformat(),
                'data_points': len(df),
                'fit_results': {k: str(v) for k, v in fit_results.items()}
            }
            model_path = model_persistence.save_model(ensemble, item_id, 'ensemble', metadata)
        
        response = {
            'item_id': item_id,
            'status': 'success',
            'fit_results': {k: 'success' if 'Fitted' in str(v) else str(v) 
                           for k, v in fit_results.items()},
            'model_path': model_path,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/items', methods=['GET'])
def list_items():
    """List all items with trained models."""
    models = model_persistence.list_models()
    
    items = {}
    for model_path in models:
        parts = Path(model_path).stem.split('_')
        if len(parts) >= 3:
            item_id = parts[0]
            model_type = parts[1]
            
            if item_id not in items:
                items[item_id] = {
                    'models': [],
                    'latest_training': None
                }
            
            items[item_id]['models'].append(model_type)
            
            # Load metadata
            metadata = model_persistence.load_metadata(model_path)
            if metadata and 'training_date' in metadata:
                training_date = metadata['training_date']
                if items[item_id]['latest_training'] is None or \
                   training_date > items[item_id]['latest_training']:
                    items[item_id]['latest_training'] = training_date
    
    return jsonify(items), 200


@app.route('/models/<item_id>', methods=['DELETE'])
def delete_model(item_id):
    """Delete trained model for an item."""
    models = model_persistence.list_models(item_id=item_id)
    
    deleted = 0
    for model_path in models:
        if model_persistence.delete_model(model_path):
            deleted += 1
    
    return jsonify({
        'item_id': item_id,
        'deleted': deleted,
        'timestamp': datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Start demand forecasting API server')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host address')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print("Demand Forecasting API Server")
    print(f"{'='*60}")
    print(f"Starting server on http://{args.host}:{args.port}")
    print(f"Debug mode: {args.debug}")
    print(f"{'='*60}\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug)









