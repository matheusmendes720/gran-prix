"""
Feature vector data structure with metadata
"""
from typing import Dict, Any, List, Optional
import numpy as np
from datetime import datetime

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.data_structures')


class FeatureVector:
    """
    Feature vector with metadata and category organization
    """
    def __init__(
        self,
        material_id: int,
        features: Dict[str, float],
        feature_categories: Optional[Dict[str, str]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize feature vector
        
        Args:
            material_id: Material ID
            features: Dictionary of feature name -> value
            feature_categories: Optional mapping of feature -> category
            timestamp: Timestamp of feature extraction
        """
        self.material_id = material_id
        self.features = features.copy()
        self.feature_categories = feature_categories or {}
        self.timestamp = timestamp or datetime.now()
        
        logger.debug(f"FeatureVector initialized for material {material_id} with {len(features)} features")
    
    def get_feature(self, feature_name: str, default: float = 0.0) -> float:
        """
        Get feature value
        
        Args:
            feature_name: Feature name
            default: Default value if not found
        
        Returns:
            Feature value
        """
        return self.features.get(feature_name, default)
    
    def get_features_by_category(self, category: str) -> Dict[str, float]:
        """
        Get features by category
        
        Args:
            category: Feature category
        
        Returns:
            Dictionary of feature name -> value for category
        """
        result = {}
        for feature_name, value in self.features.items():
            if self.feature_categories.get(feature_name) == category:
                result[feature_name] = value
        return result
    
    def to_array(self, feature_names: Optional[List[str]] = None) -> np.ndarray:
        """
        Convert to numpy array
        
        Args:
            feature_names: Optional ordered list of feature names
        
        Returns:
            Numpy array of feature values
        """
        if feature_names:
            return np.array([self.features.get(name, 0.0) for name in feature_names])
        else:
            return np.array(list(self.features.values()))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'material_id': self.material_id,
            'features': self.features,
            'feature_categories': self.feature_categories,
            'timestamp': self.timestamp.isoformat(),
            'num_features': len(self.features),
        }
    
    def merge(self, other: 'FeatureVector', overwrite: bool = True) -> 'FeatureVector':
        """
        Merge with another feature vector
        
        Args:
            other: Other feature vector
            overwrite: Overwrite existing features
        
        Returns:
            Merged feature vector
        """
        merged_features = self.features.copy()
        merged_categories = self.feature_categories.copy()
        
        if overwrite:
            merged_features.update(other.features)
            merged_categories.update(other.feature_categories)
        else:
            for key, value in other.features.items():
                if key not in merged_features:
                    merged_features[key] = value
                    merged_categories[key] = other.feature_categories.get(key, 'UNKNOWN')
        
        return FeatureVector(
            material_id=self.material_id,
            features=merged_features,
            feature_categories=merged_categories,
            timestamp=max(self.timestamp, other.timestamp)
        )
    
    def validate(self, required_features: Optional[List[str]] = None) -> bool:
        """
        Validate feature vector
        
        Args:
            required_features: Optional list of required feature names
        
        Returns:
            True if valid
        """
        if required_features:
            missing = [f for f in required_features if f not in self.features]
            if missing:
                logger.warning(f"Missing required features: {missing}")
                return False
        
        # Check for NaN or infinite values
        for name, value in self.features.items():
            if not np.isfinite(value):
                logger.warning(f"Invalid feature value for {name}: {value}")
                return False
        
        return True
    
    def fill_missing(self, default_value: float = 0.0):
        """Fill missing or invalid values with default"""
        for name, value in self.features.items():
            if not np.isfinite(value):
                self.features[name] = default_value
    
    def normalize(self, method: str = 'standard') -> 'FeatureVector':
        """
        Normalize feature values
        
        Args:
            method: Normalization method ('standard', 'minmax', 'robust')
        
        Returns:
            Normalized feature vector (new instance)
        """
        values = np.array(list(self.features.values()))
        
        if method == 'standard':
            # Z-score normalization
            mean = np.mean(values)
            std = np.std(values)
            normalized_values = (values - mean) / (std + 1e-8)
        elif method == 'minmax':
            # Min-max normalization
            min_val = np.min(values)
            max_val = np.max(values)
            normalized_values = (values - min_val) / (max_val - min_val + 1e-8)
        elif method == 'robust':
            # Robust normalization (using median and IQR)
            median = np.median(values)
            q75 = np.percentile(values, 75)
            q25 = np.percentile(values, 25)
            iqr = q75 - q25
            normalized_values = (values - median) / (iqr + 1e-8)
        else:
            normalized_values = values
        
        # Create normalized feature dictionary
        normalized_features = dict(zip(self.features.keys(), normalized_values))
        
        return FeatureVector(
            material_id=self.material_id,
            features=normalized_features,
            feature_categories=self.feature_categories.copy(),
            timestamp=self.timestamp
        )

