"""
Anomaly detector for Nova Corrente
Isolation Forest / statistical anomaly detection
"""
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.algorithms.anomaly')


class AnomalyDetector:
    """
    Detect anomalies in material movements and demand patterns
    """
    
    def detect_statistical_anomalies(
        self,
        values: List[float],
        method: str = 'iqr',
        threshold: float = 3.0
    ) -> Dict[str, Any]:
        """
        Detect statistical anomalies using IQR or Z-score
        
        Args:
            values: List of values to check
            method: Method ('iqr' or 'zscore')
            threshold: Threshold multiplier for IQR or Z-score
        
        Returns:
            Dictionary with anomaly information
        """
        try:
            if len(values) < 3:
                return {
                    'is_anomaly': False,
                    'anomaly_score': 0.0,
                    'anomalies': [],
                }
            
            values_array = np.array(values)
            
            if method == 'iqr':
                # IQR method
                q25 = np.percentile(values_array, 25)
                q75 = np.percentile(values_array, 75)
                iqr = q75 - q25
                
                lower_bound = q25 - threshold * iqr
                upper_bound = q75 + threshold * iqr
                
                anomalies = []
                for i, val in enumerate(values):
                    if val < lower_bound or val > upper_bound:
                        anomalies.append({
                            'index': i,
                            'value': float(val),
                            'deviation': float(val - np.mean(values_array)),
                        })
            else:
                # Z-score method
                mean = np.mean(values_array)
                std = np.std(values_array)
                
                if std == 0:
                    return {
                        'is_anomaly': False,
                        'anomaly_score': 0.0,
                        'anomalies': [],
                    }
                
                z_scores = np.abs((values_array - mean) / std)
                anomalies = []
                
                for i, z_score in enumerate(z_scores):
                    if z_score > threshold:
                        anomalies.append({
                            'index': i,
                            'value': float(values[i]),
                            'z_score': float(z_score),
                            'deviation': float(values[i] - mean),
                        })
            
            is_anomaly = len(anomalies) > 0
            anomaly_score = len(anomalies) / len(values) if values else 0.0
            
            return {
                'is_anomaly': is_anomaly,
                'anomaly_score': float(anomaly_score),
                'anomalies': anomalies,
                'method': method,
            }
        except Exception as e:
            logger.error(f"Error detecting statistical anomalies: {e}")
            return {
                'is_anomaly': False,
                'anomaly_score': 0.0,
                'anomalies': [],
            }
    
    def detect_isolation_forest_anomalies(
        self,
        features: np.ndarray,
        contamination: float = 0.1,
        n_estimators: int = 100
    ) -> Dict[str, Any]:
        """
        Detect anomalies using Isolation Forest
        
        Args:
            features: Feature matrix (n_samples, n_features)
            contamination: Expected proportion of anomalies
            n_estimators: Number of trees
        
        Returns:
            Dictionary with anomaly information
        """
        try:
            from sklearn.ensemble import IsolationForest
            
            if len(features) < 2:
                return {
                    'is_anomaly': False,
                    'anomaly_score': 0.0,
                    'anomalies': [],
                }
            
            # Fit Isolation Forest
            iso_forest = IsolationForest(
                contamination=contamination,
                n_estimators=n_estimators,
                random_state=42
            )
            
            predictions = iso_forest.fit_predict(features)
            anomaly_scores = iso_forest.score_samples(features)
            
            # Find anomalies (predictions == -1)
            anomalies = []
            for i, pred in enumerate(predictions):
                if pred == -1:
                    anomalies.append({
                        'index': i,
                        'anomaly_score': float(anomaly_scores[i]),
                    })
            
            is_anomaly = len(anomalies) > 0
            avg_anomaly_score = float(np.mean(anomaly_scores)) if len(anomaly_scores) > 0 else 0.0
            
            return {
                'is_anomaly': is_anomaly,
                'anomaly_score': avg_anomaly_score,
                'anomalies': anomalies,
                'method': 'isolation_forest',
                'contamination': contamination,
            }
        except ImportError:
            logger.warning("scikit-learn not available, using statistical method")
            # Fallback to statistical method
            if len(features.shape) == 1:
                return self.detect_statistical_anomalies(features.tolist())
            else:
                # Use mean of features
                mean_features = np.mean(features, axis=0)
                return self.detect_statistical_anomalies(mean_features.tolist())
        except Exception as e:
            logger.error(f"Error in Isolation Forest anomaly detection: {e}")
            return {
                'is_anomaly': False,
                'anomaly_score': 0.0,
                'anomalies': [],
            }
    
    def detect_pattern_anomalies(
        self,
        time_series: pd.Series,
        window_size: int = 7,
        threshold: float = 3.0
    ) -> Dict[str, Any]:
        """
        Detect anomalies in time series patterns
        
        Args:
            time_series: Time series data
            window_size: Window size for pattern detection
            threshold: Threshold for anomaly detection
        
        Returns:
            Dictionary with anomaly information
        """
        try:
            if len(time_series) < window_size * 2:
                return {
                    'is_anomaly': False,
                    'anomaly_score': 0.0,
                    'anomalies': [],
                }
            
            # Calculate moving average and std
            ma = time_series.rolling(window=window_size).mean()
            std = time_series.rolling(window=window_size).std()
            
            # Calculate deviations
            deviations = np.abs(time_series - ma)
            z_scores = deviations / (std + 1e-8)  # Avoid division by zero
            
            # Find anomalies
            anomalies = []
            for i, z_score in enumerate(z_scores):
                if pd.notna(z_score) and z_score > threshold:
                    anomalies.append({
                        'index': i,
                        'value': float(time_series.iloc[i]),
                        'z_score': float(z_score),
                        'deviation': float(deviations.iloc[i]) if pd.notna(deviations.iloc[i]) else 0.0,
                    })
            
            is_anomaly = len(anomalies) > 0
            anomaly_score = float(np.mean(z_scores[z_scores > threshold])) if len(anomalies) > 0 else 0.0
            
            return {
                'is_anomaly': is_anomaly,
                'anomaly_score': float(anomaly_score),
                'anomalies': anomalies,
                'method': 'pattern_detection',
            }
        except Exception as e:
            logger.error(f"Error detecting pattern anomalies: {e}")
            return {
                'is_anomaly': False,
                'anomaly_score': 0.0,
                'anomalies': [],
            }


# Singleton instance
anomaly_detector = AnomalyDetector()

