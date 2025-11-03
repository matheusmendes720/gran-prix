"""
Feature service for Nova Corrente
Handles feature extraction, aggregation, and caching
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import pandas as pd

from backend.services.database_service import db_service
from backend.services.material_service import material_service
from backend.data_structures.feature_vector import FeatureVector
from backend.utils.cache_manager import cache_manager
from backend.config.feature_config import FEATURE_CATEGORIES, FEATURE_PIPELINE
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.services.feature')


class FeatureService:
    """
    Service for feature operations
    """
    
    def get_features(
        self,
        material_id: int,
        feature_names: Optional[List[str]] = None,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, float]:
        """
        Get features for material
        
        Args:
            material_id: Material ID
            feature_names: Optional list of specific feature names
            category: Optional feature category filter
            start_date: Optional start date for temporal features
            end_date: Optional end date for temporal features
        
        Returns:
            Dictionary of feature name -> value
        """
        try:
            query = """
                SELECT feature_name, feature_value, feature_category, data_coleta
                FROM MaterialFeatures
                WHERE material_id = :material_id
            """
            
            params = {'material_id': material_id}
            
            if feature_names:
                placeholders = ', '.join([f"'{name}'" for name in feature_names])
                query += f" AND feature_name IN ({placeholders})"
            
            if category:
                query += " AND feature_category = :category"
                params['category'] = category
            
            if start_date:
                query += " AND DATE(data_coleta) >= :start_date"
                params['start_date'] = start_date
            
            if end_date:
                query += " AND DATE(data_coleta) <= :end_date"
                params['end_date'] = end_date
            
            query += " ORDER BY data_coleta DESC"
            
            results = db_service.execute_query(query, params=params)
            
            # Get latest value for each feature
            features = {}
            seen_features = set()
            
            for row in results:
                feature_name = row['feature_name']
                if feature_name not in seen_features:
                    features[feature_name] = float(row['feature_value'])
                    seen_features.add(feature_name)
            
            logger.info(f"Retrieved {len(features)} features for material {material_id}")
            return features
        except Exception as e:
            logger.error(f"Error getting features for material {material_id}: {e}")
            raise
    
    def get_feature_vector(
        self,
        material_id: int,
        include_categories: bool = True
    ) -> FeatureVector:
        """
        Get feature vector for material
        
        Args:
            material_id: Material ID
            include_categories: Include feature categories in result
        
        Returns:
            FeatureVector object
        """
        try:
            # Check cache first
            cache_key = f"feature_vector_{material_id}"
            cached = cache_manager.get(cache_key)
            
            if cached and FEATURE_PIPELINE['enable_caching']:
                logger.debug(f"Retrieved cached feature vector for material {material_id}")
                return cached
            
            # Get features from database
            features_dict = self.get_features(material_id)
            
            # Get categories if requested
            categories = {}
            if include_categories:
                query = """
                    SELECT DISTINCT feature_name, feature_category
                    FROM MaterialFeatures
                    WHERE material_id = :material_id
                """
                results = db_service.execute_query(
                    query,
                    params={'material_id': material_id}
                )
                categories = {r['feature_name']: r['feature_category'] for r in results}
            
            feature_vector = FeatureVector(
                material_id=material_id,
                features=features_dict,
                feature_categories=categories
            )
            
            # Cache result
            if FEATURE_PIPELINE['enable_caching']:
                cache_manager.set(
                    cache_key,
                    feature_vector,
                    ttl=FEATURE_PIPELINE['cache_duration']
                )
            
            logger.info(f"Created feature vector for material {material_id}")
            return feature_vector
        except Exception as e:
            logger.error(f"Error getting feature vector for material {material_id}: {e}")
            raise
    
    def store_features(
        self,
        material_id: int,
        features: Dict[str, float],
        categories: Optional[Dict[str, str]] = None,
        valid_until: Optional[datetime] = None
    ) -> bool:
        """
        Store features for material
        
        Args:
            material_id: Material ID
            features: Dictionary of feature name -> value
            categories: Optional dictionary of feature name -> category
            valid_until: Optional expiration timestamp
        
        Returns:
            True if successful
        """
        try:
            # Prepare data for insertion
            feature_rows = []
            for feature_name, feature_value in features.items():
                category = (categories or {}).get(feature_name, 'UNKNOWN')
                feature_rows.append({
                    'material_id': material_id,
                    'feature_name': feature_name,
                    'feature_value': float(feature_value),
                    'feature_category': category,
                    'data_coleta': datetime.now(),
                    'valido_ate': valid_until
                })
            
            if not feature_rows:
                return True
            
            # Insert features using DataFrame
            df = pd.DataFrame(feature_rows)
            db_service.insert_dataframe(
                'MaterialFeatures',
                df,
                if_exists='append'
            )
            
            # Invalidate cache
            cache_key = f"feature_vector_{material_id}"
            cache_manager.delete(cache_key)
            
            logger.info(
                f"Stored {len(feature_rows)} features for material {material_id}"
            )
            return True
        except Exception as e:
            logger.error(f"Error storing features for material {material_id}: {e}")
            raise
    
    def get_features_by_category(
        self,
        category: str,
        material_id: Optional[int] = None
    ) -> Dict[str, float]:
        """
        Get features by category
        
        Args:
            category: Feature category
            material_id: Optional material ID filter
        
        Returns:
            Dictionary of feature name -> value
        """
        try:
            return self.get_features(
                material_id=material_id or 0,  # Will be filtered in query
                category=category
            )
        except Exception as e:
            logger.error(f"Error getting features by category {category}: {e}")
            raise
    
    def aggregate_features(
        self,
        material_ids: List[int],
        aggregation: str = 'mean'
    ) -> Dict[str, float]:
        """
        Aggregate features across multiple materials
        
        Args:
            material_ids: List of material IDs
            aggregation: Aggregation method ('mean', 'sum', 'max', 'min', 'median')
        
        Returns:
            Dictionary of aggregated feature name -> value
        """
        try:
            if not material_ids:
                return {}
            
            placeholders = ', '.join([str(mid) for mid in material_ids])
            query = f"""
                SELECT feature_name, feature_value
                FROM MaterialFeatures
                WHERE material_id IN ({placeholders})
                AND data_coleta >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            """
            
            results = db_service.execute_query(query)
            
            if not results:
                return {}
            
            # Group by feature name
            feature_data = {}
            for row in results:
                feature_name = row['feature_name']
                if feature_name not in feature_data:
                    feature_data[feature_name] = []
                feature_data[feature_name].append(float(row['feature_value']))
            
            # Aggregate
            aggregated = {}
            import numpy as np
            
            for feature_name, values in feature_data.items():
                if aggregation == 'mean':
                    aggregated[feature_name] = float(np.mean(values))
                elif aggregation == 'sum':
                    aggregated[feature_name] = float(np.sum(values))
                elif aggregation == 'max':
                    aggregated[feature_name] = float(np.max(values))
                elif aggregation == 'min':
                    aggregated[feature_name] = float(np.min(values))
                elif aggregation == 'median':
                    aggregated[feature_name] = float(np.median(values))
            
            logger.info(
                f"Aggregated {len(aggregated)} features for {len(material_ids)} materials"
            )
            return aggregated
        except Exception as e:
            logger.error(f"Error aggregating features: {e}")
            raise
    
    def get_feature_statistics(
        self,
        material_id: int,
        feature_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get statistics for features
        
        Args:
            material_id: Material ID
            feature_name: Optional specific feature name
        
        Returns:
            Dictionary with statistics
        """
        try:
            query = """
                SELECT feature_name, feature_value, data_coleta
                FROM MaterialFeatures
                WHERE material_id = :material_id
            """
            
            params = {'material_id': material_id}
            
            if feature_name:
                query += " AND feature_name = :feature_name"
                params['feature_name'] = feature_name
            
            query += " ORDER BY data_coleta DESC LIMIT 1000"
            
            results = db_service.execute_query(query, params=params)
            
            if not results:
                return {}
            
            import numpy as np
            
            # Group by feature
            feature_stats = {}
            for row in results:
                name = row['feature_name']
                if name not in feature_stats:
                    feature_stats[name] = []
                feature_stats[name].append(float(row['feature_value']))
            
            # Calculate statistics
            statistics = {}
            for name, values in feature_stats.items():
                statistics[name] = {
                    'count': len(values),
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values)),
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'median': float(np.median(values)),
                }
            
            return statistics
        except Exception as e:
            logger.error(f"Error getting feature statistics for material {material_id}: {e}")
            raise


# Singleton instance
feature_service = FeatureService()

