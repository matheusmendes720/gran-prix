"""
Prediction result data structure with confidence intervals
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, date
import numpy as np

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.data_structures')


class PredictionResult:
    """
    Prediction result with confidence intervals and metadata
    """
    def __init__(
        self,
        material_id: int,
        prediction_type: str,
        value: float,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
        confidence_level: float = 0.95,
        probability: Optional[float] = None,
        model_id: Optional[int] = None,
        model_name: Optional[str] = None,
        horizon: Optional[int] = None,
        reference_date: Optional[date] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize prediction result
        
        Args:
            material_id: Material ID
            prediction_type: Type of prediction ('DEMANDA', 'REORDER_POINT', etc.)
            value: Predicted value
            lower_bound: Lower confidence bound
            upper_bound: Upper confidence bound
            confidence_level: Confidence level (default 0.95)
            probability: Probability for classification (optional)
            model_id: Model ID used
            model_name: Model name
            horizon: Forecast horizon in days
            reference_date: Date being predicted
            metadata: Additional metadata
        """
        self.material_id = material_id
        self.prediction_type = prediction_type
        self.value = float(value)
        self.lower_bound = float(lower_bound) if lower_bound is not None else None
        self.upper_bound = float(upper_bound) if upper_bound is not None else None
        self.confidence_level = confidence_level
        self.probability = float(probability) if probability is not None else None
        self.model_id = model_id
        self.model_name = model_name
        self.horizon = horizon
        self.reference_date = reference_date
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        
        logger.debug(
            f"PredictionResult created: material={material_id}, "
            f"type={prediction_type}, value={value}"
        )
    
    @property
    def confidence_interval(self) -> tuple:
        """Get confidence interval as tuple"""
        return (self.lower_bound, self.upper_bound)
    
    @property
    def confidence_width(self) -> Optional[float]:
        """Get width of confidence interval"""
        if self.lower_bound is not None and self.upper_bound is not None:
            return self.upper_bound - self.lower_bound
        return None
    
    @property
    def is_within_bounds(self) -> bool:
        """Check if value is within confidence bounds"""
        if self.lower_bound is not None and self.upper_bound is not None:
            return self.lower_bound <= self.value <= self.upper_bound
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'material_id': self.material_id,
            'prediction_type': self.prediction_type,
            'value': self.value,
            'lower_bound': self.lower_bound,
            'upper_bound': self.upper_bound,
            'confidence_level': self.confidence_level,
            'probability': self.probability,
            'model_id': self.model_id,
            'model_name': self.model_name,
            'horizon': self.horizon,
            'reference_date': self.reference_date.isoformat() if self.reference_date else None,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat(),
        }
    
    def apply_bounds_validation(self, min_value: float = 0.0, max_value: Optional[float] = None):
        """
        Validate and clip prediction values to reasonable bounds
        
        Args:
            min_value: Minimum allowed value (default 0.0)
            max_value: Maximum allowed value (None for no limit)
        """
        if self.value < min_value:
            logger.warning(f"Prediction value {self.value} below minimum {min_value}, clipping")
            self.value = min_value
        
        if max_value is not None and self.value > max_value:
            logger.warning(f"Prediction value {self.value} above maximum {max_value}, clipping")
            self.value = max_value
        
        if self.lower_bound is not None:
            self.lower_bound = max(self.lower_bound, min_value)
        
        if self.upper_bound is not None:
            self.upper_bound = max(self.upper_bound, min_value)
            if max_value is not None:
                self.upper_bound = min(self.upper_bound, max_value)


class PredictionBatch:
    """
    Batch of predictions for multiple materials/dates
    """
    def __init__(self, predictions: List[PredictionResult]):
        """
        Initialize prediction batch
        
        Args:
            predictions: List of prediction results
        """
        self.predictions = predictions
        self.timestamp = datetime.now()
    
    def get_by_material(self, material_id: int) -> List[PredictionResult]:
        """Get predictions for specific material"""
        return [p for p in self.predictions if p.material_id == material_id]
    
    def get_by_type(self, prediction_type: str) -> List[PredictionResult]:
        """Get predictions of specific type"""
        return [p for p in self.predictions if p.prediction_type == prediction_type]
    
    def get_by_date(self, reference_date: date) -> List[PredictionResult]:
        """Get predictions for specific date"""
        return [
            p for p in self.predictions
            if p.reference_date and p.reference_date == reference_date
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert batch to dictionary"""
        return {
            'predictions': [p.to_dict() for p in self.predictions],
            'count': len(self.predictions),
            'timestamp': self.timestamp.isoformat(),
        }
    
    def aggregate_statistics(self) -> Dict[str, Any]:
        """Calculate aggregate statistics for batch"""
        if not self.predictions:
            return {}
        
        values = [p.value for p in self.predictions]
        
        return {
            'mean': np.mean(values),
            'median': np.median(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'count': len(values),
        }

