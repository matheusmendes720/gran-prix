"""
ABC classification algorithm for Nova Corrente
Classifies materials into A, B, C categories based on importance
"""
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.algorithms.abc')


class ABCClassifier:
    """
    Classify materials using ABC analysis
    """
    
    def classify_by_value(
        self,
        items: List[Dict[str, Any]],
        value_key: str = 'value',
        item_key: str = 'item_id'
    ) -> Dict[str, Any]:
        """
        Classify items by total value (Pareto analysis)
        
        Args:
            items: List of items with values
            value_key: Key for value in item dictionary
            item_key: Key for item identifier
        
        Returns:
            Dictionary with classifications and statistics
        """
        try:
            if not items:
                return {'classifications': {}, 'statistics': {}}
            
            # Create DataFrame
            df = pd.DataFrame(items)
            
            if value_key not in df.columns:
                raise ValueError(f"Value key '{value_key}' not found in items")
            
            # Calculate total value
            df['cumulative_value'] = df[value_key].cumsum()
            df['cumulative_percent'] = (df['cumulative_value'] / df[value_key].sum()) * 100
            
            # Classify
            df['category'] = 'C'
            df.loc[df['cumulative_percent'] <= 80, 'category'] = 'A'
            df.loc[(df['cumulative_percent'] > 80) & (df['cumulative_percent'] <= 95), 'category'] = 'B'
            
            # Create classification dictionary
            classifications = {}
            for _, row in df.iterrows():
                item_id = row[item_key]
                classifications[item_id] = {
                    'category': row['category'],
                    'value': float(row[value_key]),
                    'cumulative_percent': float(row['cumulative_percent']),
                }
            
            # Statistics
            statistics = {
                'total_items': len(df),
                'total_value': float(df[value_key].sum()),
                'category_counts': df['category'].value_counts().to_dict(),
                'category_values': df.groupby('category')[value_key].sum().to_dict(),
            }
            
            logger.info(f"Classified {len(df)} items: {statistics['category_counts']}")
            
            return {
                'classifications': classifications,
                'statistics': statistics,
            }
        except Exception as e:
            logger.error(f"Error in ABC classification: {e}")
            raise
    
    def classify_by_volume(
        self,
        items: List[Dict[str, Any]],
        volume_key: str = 'volume',
        item_key: str = 'item_id'
    ) -> Dict[str, Any]:
        """
        Classify items by volume/movement
        
        Args:
            items: List of items with volumes
            volume_key: Key for volume in item dictionary
            item_key: Key for item identifier
        
        Returns:
            Dictionary with classifications and statistics
        """
        return self.classify_by_value(items, value_key=volume_key, item_key=item_key)
    
    def classify_by_frequency(
        self,
        items: List[Dict[str, Any]],
        frequency_key: str = 'frequency',
        item_key: str = 'item_id'
    ) -> Dict[str, Any]:
        """
        Classify items by movement frequency
        
        Args:
            items: List of items with frequencies
            frequency_key: Key for frequency in item dictionary
            item_key: Key for item identifier
        
        Returns:
            Dictionary with classifications and statistics
        """
        return self.classify_by_value(items, value_key=frequency_key, item_key=item_key)
    
    def classify_by_criticality(
        self,
        items: List[Dict[str, Any]],
        criticality_key: str = 'criticality_score',
        item_key: str = 'item_id',
        thresholds: Tuple[float, float] = (0.8, 0.95)
    ) -> Dict[str, Any]:
        """
        Classify items by criticality score
        
        Args:
            items: List of items with criticality scores
            criticality_key: Key for criticality score in item dictionary
            item_key: Key for item identifier
            thresholds: Tuple of (A threshold, B threshold) for cumulative percent
        
        Returns:
            Dictionary with classifications and statistics
        """
        try:
            if not items:
                return {'classifications': {}, 'statistics': {}}
            
            # Create DataFrame
            df = pd.DataFrame(items)
            
            if criticality_key not in df.columns:
                raise ValueError(f"Criticality key '{criticality_key}' not found in items")
            
            # Sort by criticality (descending)
            df = df.sort_values(criticality_key, ascending=False).reset_index(drop=True)
            
            # Calculate cumulative percent
            df['cumulative_score'] = df[criticality_key].cumsum()
            df['cumulative_percent'] = (df['cumulative_score'] / df[criticality_key].sum()) * 100
            
            # Classify using thresholds
            df['category'] = 'C'
            df.loc[df['cumulative_percent'] <= thresholds[0] * 100, 'category'] = 'A'
            df.loc[
                (df['cumulative_percent'] > thresholds[0] * 100) & 
                (df['cumulative_percent'] <= thresholds[1] * 100),
                'category'
            ] = 'B'
            
            # Create classification dictionary
            classifications = {}
            for _, row in df.iterrows():
                item_id = row[item_key]
                classifications[item_id] = {
                    'category': row['category'],
                    'criticality_score': float(row[criticality_key]),
                    'cumulative_percent': float(row['cumulative_percent']),
                }
            
            # Statistics
            statistics = {
                'total_items': len(df),
                'total_criticality': float(df[criticality_key].sum()),
                'category_counts': df['category'].value_counts().to_dict(),
            }
            
            logger.info(f"Classified {len(df)} items by criticality: {statistics['category_counts']}")
            
            return {
                'classifications': classifications,
                'statistics': statistics,
            }
        except Exception as e:
            logger.error(f"Error in ABC classification by criticality: {e}")
            raise


# Singleton instance
abc_classifier = ABCClassifier()

