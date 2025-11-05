"""
Enhanced Flask API for Nova Corrente Dashboard
Integrated with database and all new services

⚠️ DEPRECATED: This Flask API is deprecated in favor of FastAPI (backend/app/main.py)
This file is kept for backward compatibility but should not be used in production deployment.

In deployment, use FastAPI endpoints only:
- NO ML Services (prediction_service, model_registry) - removed
- NO External Data Services (external_data_service) - removed
- Read-only analytics only
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date, timedelta
import json

# Import services
from backend.services.database_service import db_service
from backend.services.material_service import material_service
from backend.services.feature_service import feature_service
from backend.services.analytics_service import analytics_service
# ❌ REMOVED: prediction_service (ML not used in deployment)
# ❌ REMOVED: external_data_service (External APIs disabled in deployment)
from backend.services.integration_service import integration_service
from backend.services.feature_engineering.feature_pipeline import feature_pipeline
# ❌ REMOVED: model_registry (ML not used in deployment)
from backend.algorithms.reorder_point_calculator import reorder_point_calculator
from backend.algorithms.safety_stock_calculator import safety_stock_calculator
# ❌ DISABLED: orchestrator_service external API calls (disabled in deployment)
from backend.pipelines.orchestrator_service import orchestrator_service
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.api')

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db_healthy = db_service.test_connection()
        
        return jsonify({
            'status': 'healthy' if db_healthy else 'degraded',
            'database': 'connected' if db_healthy else 'disconnected',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0'
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/kpis', methods=['GET'])
def get_kpis():
    """Get real-time KPI metrics."""
    try:
        kpis = analytics_service.calculate_kpis()
        
        return jsonify({
            'status': 'success',
            'kpis': kpis,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting KPIs: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    """Get material by ID."""
    try:
        material = material_service.get_material(material_id)
        
        if not material:
            return jsonify({
                'status': 'error',
                'message': f'Material {material_id} not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'material': material
        })
    except Exception as e:
        logger.error(f"Error getting material: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/materials/<int:material_id>/forecast', methods=['GET'])
def get_material_forecast(material_id):
    """
    ⚠️ DEPRECATED: This endpoint uses ML services and is disabled in deployment.
    Use FastAPI endpoints instead: /api/v1/forecasts
    """
    return jsonify({
        'status': 'error',
        'message': 'This Flask endpoint is deprecated. Use FastAPI /api/v1/forecasts instead. ML services are disabled in deployment.'
    }), 410  # Gone - endpoint deprecated
    
    # ❌ DISABLED: ML prediction service not available in deployment
    # Original code commented out:
    # try:
    #     horizon = int(request.args.get('horizon', 30))
    #     context = material_service.get_material_context(material_id)
    #     forecast = prediction_service.generate_prediction(...)
        
        return jsonify({
            'status': 'success',
            'material_id': material_id,
            'forecast': forecast.to_dict(),
            'horizon': horizon
        })
    except Exception as e:
        logger.error(f"Error getting forecast: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/features/calculate', methods=['POST'])
def calculate_features():
    """Calculate features for material(s)."""
    try:
        data = request.get_json()
        material_id = data.get('material_id')
        date_ref = data.get('date_ref')
        
        if not material_id:
            return jsonify({
                'status': 'error',
                'message': 'material_id is required'
            }), 400
        
        # Parse date
        if date_ref:
            date_ref = datetime.fromisoformat(date_ref).date()
        else:
            date_ref = date.today()
        
        # Calculate features
        feature_vector = feature_pipeline.calculate_and_store_features(
            material_id,
            date_ref=date_ref,
            store_in_db=True
        )
        
        return jsonify({
            'status': 'success',
            'material_id': material_id,
            'features': feature_vector.to_dict(),
            'date_ref': date_ref.isoformat()
        })
    except Exception as e:
        logger.error(f"Error calculating features: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/models/train', methods=['POST'])
def train_model():
    """Train ML model."""
    try:
        data = request.get_json()
        model_type = data.get('model_type', 'FORECASTING')
        material_id = data.get('material_id')
        
        # Placeholder for model training
        # In production, would call ML model services
        
        return jsonify({
            'status': 'success',
            'message': f'Model training initiated for {model_type}',
            'material_id': material_id
        })
    except Exception as e:
        logger.error(f"Error training model: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/models/<int:model_id>/predict', methods=['GET'])
def get_model_predictions(model_id):
    """
    ⚠️ DEPRECATED: This endpoint uses ML services and is disabled in deployment.
    Use FastAPI endpoints instead: /api/v1/forecasts
    """
    return jsonify({
        'status': 'error',
        'message': 'This Flask endpoint is deprecated. Use FastAPI /api/v1/forecasts instead. ML services are disabled in deployment.'
    }), 410  # Gone - endpoint deprecated
    
    # ❌ DISABLED: ML prediction service not available in deployment
    # Original code commented out:
    # try:
    #     material_id = int(request.args.get('material_id', 0))
    #     horizon = int(request.args.get('horizon', 30))
    #     prediction = prediction_service.generate_prediction(...)
        
        return jsonify({
            'status': 'success',
            'model_id': model_id,
            'prediction': prediction.to_dict()
        })
    except Exception as e:
        logger.error(f"Error getting predictions: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/external-data/refresh', methods=['POST'])
def refresh_external_data():
    """
    ⚠️ DEPRECATED: This endpoint uses external APIs and is disabled in deployment.
    External APIs are disabled in production - data is precomputed locally.
    """
    return jsonify({
        'status': 'error',
        'message': 'This Flask endpoint is deprecated. External APIs are disabled in deployment. Data is precomputed locally.'
    }), 410  # Gone - endpoint deprecated
    
    # ❌ DISABLED: External APIs disabled in deployment
    # Original code commented out:
    # try:
    #     data = request.get_json()
    #     data_type = data.get('data_type', 'all')
    #     results['climate'] = external_data_service.refresh_climate_data(...)
    #     results['economic'] = external_data_service.refresh_economic_data(...)
    #     results['5g'] = external_data_service.refresh_5g_data(...)
        
        return jsonify({
            'status': 'success',
            'data_type': data_type,
            'results': results
        })
    except Exception as e:
        logger.error(f"Error refreshing external data: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/materials/<int:material_id>/reorder-point', methods=['GET'])
def calculate_reorder_point(material_id):
    """Calculate reorder point for material."""
    try:
        demand = float(request.args.get('demand', 10.0))
        lead_time = float(request.args.get('lead_time', 14.0))
        safety_stock = float(request.args.get('safety_stock', 0.0))
        
        pp = reorder_point_calculator.calculate(
            demand=demand,
            lead_time_days=lead_time,
            safety_stock=safety_stock
        )
        
        return jsonify({
            'status': 'success',
            'material_id': material_id,
            'reorder_point': pp,
            'demand': demand,
            'lead_time': lead_time,
            'safety_stock': safety_stock
        })
    except Exception as e:
        logger.error(f"Error calculating reorder point: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/materials/<int:material_id>/safety-stock', methods=['GET'])
def calculate_safety_stock(material_id):
    """Calculate safety stock for material."""
    try:
        demand_std = float(request.args.get('demand_std', 5.0))
        lead_time = float(request.args.get('lead_time', 14.0))
        service_level = float(request.args.get('service_level', 0.95))
        
        ss = safety_stock_calculator.calculate_simple(
            demand_std=demand_std,
            lead_time_days=lead_time,
            service_level=service_level
        )
        
        return jsonify({
            'status': 'success',
            'material_id': material_id,
            'safety_stock': ss,
            'demand_std': demand_std,
            'lead_time': lead_time,
            'service_level': service_level
        })
    except Exception as e:
        logger.error(f"Error calculating safety stock: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/pipeline/daily', methods=['POST'])
def run_daily_pipeline():
    """Run daily pipeline (external data refresh + feature calculation)."""
    try:
        data = request.get_json() or {}
        date_ref = data.get('date_ref')
        
        if date_ref:
            date_ref = datetime.fromisoformat(date_ref).date()
        else:
            date_ref = date.today()
        
        result = integration_service.run_daily_pipeline(date_ref=date_ref)
        
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        logger.error(f"Error running daily pipeline: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/pipeline/complete', methods=['POST'])
def run_complete_pipeline():
    """Run complete ETL pipeline for all data sources."""
    try:
        data = request.get_json() or {}
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date:
            start_date = datetime.fromisoformat(start_date).date()
        else:
            start_date = date.today() - timedelta(days=30)
        
        if end_date:
            end_date = datetime.fromisoformat(end_date).date()
        else:
            end_date = date.today()
        
        result = orchestrator_service.run_complete_pipeline(start_date, end_date)
        
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        logger.error(f"Error running complete pipeline: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/integration/expanded-features', methods=['POST'])
def generate_expanded_features():
    """Generate expanded features using all data sources (125+ features)."""
    try:
        data = request.get_json()
        material_id = data.get('material_id')
        date_ref = data.get('date_ref')
        
        if not material_id:
            return jsonify({
                'status': 'error',
                'message': 'material_id is required'
            }), 400
        
        if date_ref:
            date_ref = datetime.fromisoformat(date_ref).date()
        else:
            date_ref = date.today()
        
        features = integration_service.generate_expanded_features(
            material_id=material_id,
            date_ref=date_ref
        )
        
        return jsonify({
            'status': 'success',
            'material_id': material_id,
            'features': features,
            'num_features': len(features),
            'date': date_ref.isoformat()
        })
    except Exception as e:
        logger.error(f"Error generating expanded features: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

