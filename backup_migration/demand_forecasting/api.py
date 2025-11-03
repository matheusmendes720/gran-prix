"""
Flask API for Nova Corrente Demand Forecasting System
RESTful API endpoints for integration with web dashboard and other systems
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Optional
import sys

# Add demand_forecasting to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from demand_forecasting import DemandForecastingPipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global pipeline instance
pipeline = None
config = {
    'service_level': 0.95,
    'ensemble_weights': {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3},
    'forecast_horizon': 30,
    'use_ensemble': True,
    'external_features': True
}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/config', methods=['GET', 'POST'])
def config_endpoint():
    """Get or update configuration."""
    global config, pipeline
    
    if request.method == 'GET':
        return jsonify(config)
    
    elif request.method == 'POST':
        new_config = request.json
        config.update(new_config)
        
        # Reinitialize pipeline with new config
        pipeline = DemandForecastingPipeline(config=config)
        
        return jsonify({
            'status': 'success',
            'config': config,
            'message': 'Configuration updated'
        })


@app.route('/api/forecast', methods=['POST'])
def forecast():
    """
    Generate forecast for given data.
    
    Request body:
    {
        'data': [{'date': '2022-01-01', 'Item_ID': 'CONN-001', 'Quantity_Consumed': 8, ...}, ...],
        'lead_times': {'CONN-001': 14},
        'current_stocks': {'CONN-001': 100}
    }
    """
    global pipeline
    
    try:
        if pipeline is None:
            pipeline = DemandForecastingPipeline(config=config)
        
        data = request.json
        
        # Save data to temporary file
        df = pd.DataFrame(data['data'])
        temp_file = 'temp_forecast_data.csv'
        df.to_csv(temp_file, index=False)
        
        # Generate forecast
        results = pipeline.run(
            data_file=temp_file,
            lead_times=data.get('lead_times', {}),
            current_stocks=data.get('current_stocks', {}),
            output_dir='api_output'
        )
        
        # Format response
        response = {
            'status': 'success',
            'forecasts': {},
            'pp_results': {},
            'alerts': []
        }
        
        # Format forecasts
        for item_id, forecast_df in results['forecasts'].items():
            response['forecasts'][item_id] = {
                'forecast': forecast_df['forecast'].tolist(),
                'lower': forecast_df.get('lower', []).tolist() if 'lower' in forecast_df.columns else [],
                'upper': forecast_df.get('upper', []).tolist() if 'upper' in forecast_df.columns else []
            }
        
        # Format PP results
        for item_id, pp_info in results['pp_results'].items():
            if 'error' not in pp_info:
                response['pp_results'][item_id] = pp_info
        
        # Format alerts
        for alert_info in results['alerts']:
            response['alerts'].append({
                'item_id': alert_info['item_id'],
                'message': alert_info['alert'],
                'pp_info': alert_info['pp_info']
            })
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/forecast/file', methods=['POST'])
def forecast_from_file():
    """
    Generate forecast from uploaded file.
    
    Request: multipart/form-data with 'file' field
    Query params: lead_times (JSON string), current_stocks (JSON string)
    """
    global pipeline
    
    try:
        if pipeline is None:
            pipeline = DemandForecastingPipeline(config=config)
        
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        # Save uploaded file
        upload_path = f'temp_upload_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        file.save(upload_path)
        
        # Parse lead_times and current_stocks from query params
        lead_times = json.loads(request.args.get('lead_times', '{}'))
        current_stocks = json.loads(request.args.get('current_stocks', '{}'))
        
        # Generate forecast
        results = pipeline.run(
            data_file=upload_path,
            lead_times=lead_times,
            current_stocks=current_stocks,
            output_dir='api_output'
        )
        
        # Format response (same as /api/forecast)
        response = {
            'status': 'success',
            'forecasts': {},
            'pp_results': {},
            'alerts': []
        }
        
        for item_id, forecast_df in results['forecasts'].items():
            response['forecasts'][item_id] = {
                'forecast': forecast_df['forecast'].tolist(),
                'lower': forecast_df.get('lower', []).tolist() if 'lower' in forecast_df.columns else [],
                'upper': forecast_df.get('upper', []).tolist() if 'upper' in forecast_df.columns else []
            }
        
        for item_id, pp_info in results['pp_results'].items():
            if 'error' not in pp_info:
                response['pp_results'][item_id] = pp_info
        
        for alert_info in results['alerts']:
            response['alerts'].append({
                'item_id': alert_info['item_id'],
                'message': alert_info['alert'],
                'pp_info': alert_info['pp_info']
            })
        
        # Cleanup
        Path(upload_path).unlink(missing_ok=True)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/items/<item_id>/forecast', methods=['GET'])
def forecast_item(item_id):
    """
    Get forecast for specific item.
    Requires data_file, lead_time, and current_stock as query params.
    """
    global pipeline
    
    try:
        if pipeline is None:
            pipeline = DemandForecastingPipeline(config=config)
        
        data_file = request.args.get('data_file')
        lead_time = int(request.args.get('lead_time', 14))
        current_stock = float(request.args.get('current_stock', 100))
        
        if not data_file:
            return jsonify({'status': 'error', 'message': 'data_file required'}), 400
        
        # Load data
        from demand_forecasting.data_loader import DataLoader
        loader = DataLoader()
        data_dict = loader.load_and_preprocess(data_file)
        
        if item_id not in data_dict:
            return jsonify({'status': 'error', 'message': f'Item {item_id} not found'}), 404
        
        # Generate forecast for this item
        item_df = data_dict[item_id]
        
        # Prepare models
        pipeline.prepare_models({item_id: item_df})
        pipeline.train_models({item_id: item_df})
        forecasts = pipeline.generate_forecasts({item_id: item_df})
        
        # Calculate PP
        pp_results = pipeline.calculate_reorder_points(
            forecasts=forecasts,
            lead_times={item_id: lead_time},
            current_stocks={item_id: current_stock}
        )
        
        response = {
            'status': 'success',
            'item_id': item_id,
            'forecast': forecasts[item_id].to_dict() if item_id in forecasts else {},
            'pp_info': pp_results.get(item_id, {})
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/metrics', methods=['POST'])
def calculate_metrics():
    """
    Calculate forecast accuracy metrics.
    
    Request body:
    {
        'actual': [8, 9, 10, ...],
        'forecast': [8.2, 9.1, 9.8, ...]
    }
    """
    try:
        data = request.json
        actual = np.array(data['actual'])
        forecast = np.array(data['forecast'])
        
        # Calculate metrics
        rmse = np.sqrt(np.mean((actual - forecast) ** 2))
        mae = np.mean(np.abs(actual - forecast))
        mape = np.mean(np.abs((actual - forecast) / (actual + 1e-8))) * 100
        
        return jsonify({
            'status': 'success',
            'metrics': {
                'RMSE': float(rmse),
                'MAE': float(mae),
                'MAPE': float(mape)
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/reports/<report_type>', methods=['GET'])
def get_report(report_type):
    """
    Get generated reports.
    
    report_type: 'forecasts', 'pp', 'alerts'
    """
    try:
        report_paths = {
            'forecasts': 'api_output/forecasts_report.csv',
            'pp': 'api_output/weekly_pp_report.csv',
            'alerts': 'api_output/alerts_report.csv'
        }
        
        if report_type not in report_paths:
            return jsonify({'status': 'error', 'message': 'Invalid report type'}), 400
        
        report_path = Path(report_paths[report_type])
        if not report_path.exists():
            return jsonify({'status': 'error', 'message': 'Report not found'}), 404
        
        df = pd.read_csv(report_path)
        return jsonify({
            'status': 'success',
            'report_type': report_type,
            'data': df.to_dict('records')
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


if __name__ == '__main__':
    # Initialize pipeline
    pipeline = DemandForecastingPipeline(config=config)
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

