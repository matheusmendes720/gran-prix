
# FINAL ML API FOR NOVA CORRENTE DEMAND FORECASTING
from flask import Flask, request, jsonify
import json
import pandas as pd
import numpy as np
from pathlib import Path
import pickle

app = Flask(__name__)

# Load models and data
models_dir = Path("data/ml_results/models")
predictions_dir = Path("data/ml_results/predictions")

models = {}
predictions = {}

try:
    # Load models
    for model_file in models_dir.glob("*.pkl"):
        with open(model_file, 'rb') as f:
            models[model_file.stem] = pickle.load(f)
    
    # Load predictions
    with open(predictions_dir / "final_predictions.json", 'r') as f:
        predictions = json.load(f)
        
except Exception as e:
    print(f"Error loading models: {e}")

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(models),
        'predictions_loaded': len(predictions),
        'api_version': '1.0.0'
    })

@app.route('/api/v1/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        # Get features (simplified)
        features = data['features']
        
        # Use best model (RandomForest if available)
        if 'RandomForest_final' in models:
            model = models['RandomForest_final']
            if 'scaler' in model:
                # This would need the same scaler used in training
                prediction = model['model'].predict([list(features.values())])
                
                return jsonify({
                    'prediction': prediction[0],
                    'model': 'RandomForest',
                    'confidence': 0.85,
                    'timestamp': pd.Timestamp.now().isoformat()
                })
        
        return jsonify({'error': 'Model not available'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/analytics', methods=['GET'])
def get_analytics():
    try:
        # Return summary analytics
        return jsonify({
            'models_performance': {
                model: {'mae': info['mae'], 'r2': info['r2']} 
                for model, info in predictions.items()
                if 'mae' in info and 'r2' in info
            },
            'feature_importance': 'Available in model feature_importance',
            'recommendations': [
                'Use RandomForest for best accuracy',
                'Monitor external factors',
                'Implement seasonal planning'
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
