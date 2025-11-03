"""
LSTM neural network for demand forecasting.
Deep learning approach for complex pattern recognition.
"""
import numpy as np
import pandas as pd
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    # Create dummy Sequential for type hints when TensorFlow not available
    Sequential = type('Sequential', (), {})
    print("Warning: TensorFlow not available. LSTM model cannot be used.")
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class LSTMForecaster:
    """LSTM neural network for demand forecasting."""
    
    def __init__(self, look_back: int = 30, units: int = 50, epochs: int = 50, 
                 batch_size: int = 32, verbose: int = 0):
        """
        Initialize LSTM forecaster.
        
        Args:
            look_back: Number of time steps to look back (default: 30)
            units: Number of LSTM units (default: 50)
            epochs: Number of training epochs (default: 50)
            batch_size: Batch size for training (default: 32)
            verbose: Verbosity level (default: 0)
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required for LSTM model")
        
        self.look_back = look_back
        self.units = units
        self.epochs = epochs
        self.batch_size = batch_size
        self.verbose = verbose
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.fitted = False
    
    def _prepare_data(self, series: pd.Series, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare data for LSTM training.
        
        Args:
            series: Time series data
            test_size: Proportion of data for testing
        
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        # Scale data
        scaled = self.scaler.fit_transform(series.values.reshape(-1, 1))
        
        # Create sequences
        X, y = [], []
        for i in range(self.look_back, len(scaled)):
            X.append(scaled[i - self.look_back:i, 0])
            y.append(scaled[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        # Train-test split
        split_idx = int(len(X) * (1 - test_size))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        return X_train, X_test, y_train, y_test
    
    def fit(self, series: pd.Series, validation_split: float = 0.2, verbose: Optional[int] = None):
        """
        Train LSTM model.
        
        Args:
            series: Time series data to train on
            validation_split: Proportion of data for validation
            verbose: Verbosity level (overrides init value if provided)
        
        Returns:
            Trained LSTM model
        
        Raises:
            ImportError: If TensorFlow not available
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required for LSTM model")
        
        if verbose is None:
            verbose = self.verbose
        
        # Prepare data
        X_train, X_test, y_train, y_test = self._prepare_data(series, validation_split)
        
        # Build model
        self.model = Sequential([
            LSTM(self.units, return_sequences=True, input_shape=(self.look_back, 1)),
            Dropout(0.2),
            LSTM(self.units, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='mean_squared_error',
            metrics=['mae']
        )
        
        # Early stopping callback
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Train
        self.model.fit(
            X_train, y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_data=(X_test, y_test),
            verbose=verbose,
            shuffle=False,
            callbacks=[early_stopping]
        )
        
        self.fitted = True
        return self.model
    
    def forecast(self, series: pd.Series, steps: int = 30) -> np.ndarray:
        """
        Generate forecasts.
        
        Args:
            series: Historical series to base forecast on
            steps: Number of periods to forecast
        
        Returns:
            Array of forecasted values
        
        Raises:
            ValueError: If model not fitted
        """
        if not self.fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Get last look_back values from series
        if len(series) < self.look_back:
            raise ValueError(
                f"Series length ({len(series)}) must be at least look_back ({self.look_back})"
            )
        
        # Scale last look_back values
        last_values = series.tail(self.look_back).values
        scaled_last = self.scaler.transform(last_values.reshape(-1, 1))
        
        # Generate forecasts iteratively
        forecast = []
        inputs = scaled_last.reshape(1, self.look_back, 1)
        
        for _ in range(steps):
            pred = self.model.predict(inputs, verbose=0)[0, 0]
            forecast.append(pred)
            
            # Update inputs with new prediction (rolling window)
            inputs = np.append(inputs[:, 1:, :], [[[pred]]], axis=1)
        
        # Inverse transform
        forecast = np.array(forecast).reshape(-1, 1)
        forecast = self.scaler.inverse_transform(forecast)
        
        # Clip unrealistic values
        historical_max = series.max()
        historical_min = series.min()
        forecast = np.clip(forecast, max(0, historical_min * 0.5), historical_max * 1.5)
        
        return forecast.flatten()

