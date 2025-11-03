"""
Base model interface for all ML models.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np


class BaseModel(ABC):
    """Base interface for all forecasting models."""
    
    def __init__(self, **kwargs):
        """Initialize base model."""
        self.fitted = False
        self.model = None
    
    @abstractmethod
    def fit(self, data: pd.DataFrame, target_column: str, **kwargs) -> None:
        """
        Fit the model to training data.
        
        Args:
            data: Training data as DataFrame
            target_column: Name of target column
            **kwargs: Additional model-specific parameters
        """
        pass
    
    @abstractmethod
    def predict(self, steps: int, df: Optional[pd.DataFrame] = None, **kwargs) -> np.ndarray:
        """
        Generate predictions.
        
        Args:
            steps: Number of steps to forecast
            df: Optional input data
            **kwargs: Additional prediction parameters
            
        Returns:
            Array of predictions
        """
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """
        Save model to disk.
        
        Args:
            path: Path to save model
        """
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """
        Load model from disk.
        
        Args:
            path: Path to load model from
        """
        pass
    
    def get_params(self) -> Dict[str, Any]:
        """Get model parameters."""
        return {}
    
    def set_params(self, **params) -> None:
        """Set model parameters."""
        pass
    
    def get_feature_importance(self) -> Optional[Dict[str, float]]:
        """Get feature importance if available."""
        return None
    
    def validate(self, data: pd.DataFrame, target_column: str) -> Dict[str, float]:
        """
        Validate model on data.
        
        Args:
            data: Validation data
            target_column: Name of target column
            
        Returns:
            Dictionary of validation metrics
        """
        if not self.fitted:
            raise ValueError("Model must be fitted before validation")
        
        # Basic validation - should be overridden by subclasses
        predictions = self.predict(len(data))
        actual = data[target_column].values
        
        from backend.ml.evaluation.metrics import calculate_metrics
        return calculate_metrics(actual, predictions)

