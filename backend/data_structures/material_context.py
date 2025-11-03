"""
Material context with all features and metadata
"""
from typing import Dict, Any, Optional
from datetime import datetime
from backend.data_structures.feature_vector import FeatureVector
from backend.data_structures.time_series import TimeSeries
from backend.data_structures.prediction_result import PredictionResult
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.data_structures')


class MaterialContext:
    """
    Complete material context with features, time series, and predictions
    """
    def __init__(
        self,
        material_id: int,
        material_name: str,
        features: Optional[FeatureVector] = None,
        time_series: Optional[TimeSeries] = None,
        predictions: Optional[list] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize material context
        
        Args:
            material_id: Material ID
            material_name: Material name
            features: Feature vector
            time_series: Time series data
            predictions: List of prediction results
            metadata: Additional metadata (family, tier, etc.)
        """
        self.material_id = material_id
        self.material_name = material_name
        self.features = features
        self.time_series = time_series
        self.predictions = predictions or []
        self.metadata = metadata or {}
        self.last_updated = datetime.now()
        
        logger.debug(f"MaterialContext initialized for material {material_id}")
    
    def get_feature(self, feature_name: str, default: float = 0.0) -> float:
        """Get feature value"""
        if self.features:
            return self.features.get_feature(feature_name, default)
        return default
    
    def get_latest_prediction(self, prediction_type: str = None) -> Optional[PredictionResult]:
        """Get latest prediction (optionally filtered by type)"""
        if not self.predictions:
            return None
        
        filtered = self.predictions
        if prediction_type:
            filtered = [p for p in filtered if p.prediction_type == prediction_type]
        
        if not filtered:
            return None
        
        # Sort by timestamp and return most recent
        filtered.sort(key=lambda x: x.timestamp, reverse=True)
        return filtered[0]
    
    def add_prediction(self, prediction: PredictionResult):
        """Add prediction to context"""
        self.predictions.append(prediction)
        self.last_updated = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'material_id': self.material_id,
            'material_name': self.material_name,
            'features': self.features.to_dict() if self.features else None,
            'time_series': self.time_series.to_dict() if self.time_series else None,
            'predictions': [p.to_dict() for p in self.predictions],
            'metadata': self.metadata,
            'last_updated': self.last_updated.isoformat(),
        }
    
    def validate(self) -> bool:
        """Validate material context"""
        if not self.material_id:
            logger.error("Material ID is required")
            return False
        
        if self.features:
            if not self.features.validate():
                logger.error(f"Invalid features for material {self.material_id}")
                return False
        
        return True

