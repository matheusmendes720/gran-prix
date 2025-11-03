"""
LSTM model service for Nova Corrente
LSTM multivariate time-series
"""
from typing import Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd

from backend.config.ml_config import LSTM_CONFIG
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.ml_models.lstm')


class LSTMModel:
    """LSTM multivariate time-series model"""
    
    def __init__(self):
        self.model = None
        self.config = LSTM_CONFIG
        self.scaler = None
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_val: Optional[np.ndarray] = None, y_val: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Train LSTM model"""
        try:
            from tensorflow import keras
            from tensorflow.keras import layers
            
            sequence_length = self.config['sequence_length']
            n_features = X_train.shape[2] if len(X_train.shape) == 3 else X_train.shape[1]
            
            # Build model
            self.model = keras.Sequential([
                layers.LSTM(self.config['lstm_units'][0], return_sequences=True, input_shape=(sequence_length, n_features)),
                layers.LSTM(self.config['lstm_units'][1], return_sequences=False),
                layers.Dense(self.config['dense_units'][0], activation=self.config['activation']),
                layers.Dropout(self.config['dropout_rate']),
                layers.Dense(self.config['dense_units'][1]),
            ])
            
            self.model.compile(
                optimizer=self.config['optimizer'],
                loss=self.config['loss'],
                metrics=self.config['metrics']
            )
            
            # Train
            validation_data = (X_val, y_val) if X_val is not None else None
            
            history = self.model.fit(
                X_train, y_train,
                batch_size=self.config['batch_size'],
                epochs=self.config['epochs'],
                validation_data=validation_data,
                validation_split=self.config['validation_split'] if validation_data is None else None,
                verbose=0
            )
            
            logger.info("LSTM model trained successfully")
            return {'status': 'success', 'model': self.model, 'history': history.history}
        except ImportError:
            logger.error("TensorFlow not installed. Install with: pip install tensorflow")
            raise
        except Exception as e:
            logger.error(f"Error training LSTM model: {e}")
            raise
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate predictions"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        try:
            predictions = self.model.predict(X, verbose=0)
            return predictions.flatten()
        except Exception as e:
            logger.error(f"Error generating LSTM predictions: {e}")
            raise
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        try:
            y_pred = self.predict(X_test)
            y_true = y_test.flatten()
            
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
            rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
            mae = np.mean(np.abs(y_true - y_pred))
            
            return {'mape': float(mape), 'rmse': float(rmse), 'mae': float(mae)}
        except Exception as e:
            logger.error(f"Error evaluating LSTM model: {e}")
            raise


lstm_model = LSTMModel()

