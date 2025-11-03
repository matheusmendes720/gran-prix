"""
End-to-end feature engineering pipeline for Nova Corrente
Orchestrates all feature extractors
"""
from typing import Dict, Any, List, Optional
from datetime import date, datetime
import pandas as pd

from backend.services.material_service import material_service
from backend.services.feature_service import feature_service
from backend.data_structures.feature_vector import FeatureVector
from backend.data_structures.time_series import TimeSeries
from backend.services.feature_engineering.temporal_features import temporal_feature_extractor
from backend.services.feature_engineering.statistical_features import statistical_feature_extractor
from backend.services.feature_engineering.external_features import external_feature_extractor
from backend.services.feature_engineering.hierarchical_features import hierarchical_feature_extractor
from backend.services.feature_engineering.expanded_features import expanded_feature_extractor
from backend.config.feature_config import FEATURE_PIPELINE, FEATURE_CATEGORIES
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.features.pipeline')


class FeaturePipeline:
    """
    End-to-end feature engineering pipeline
    """
    
    def extract_all_features(
        self,
        material_id: int,
        date_ref: Optional[date] = None,
        include_temporal: bool = True,
        include_statistical: bool = True,
        include_external: bool = True,
        include_hierarchical: bool = True,
        include_expanded: bool = True
    ) -> FeatureVector:
        """
        Extract all features for a material
        
        Args:
            material_id: Material ID
            date_ref: Reference date (default: today)
            include_temporal: Include temporal features
            include_statistical: Include statistical features
            include_external: Include external features
            include_hierarchical: Include hierarchical features
        
        Returns:
            FeatureVector with all features
        """
        if date_ref is None:
            date_ref = date.today()
        
        try:
            logger.info(f"Starting feature extraction for material {material_id}")
            
            all_features = {}
            all_categories = {}
            
            # 1. Temporal features
            if include_temporal:
                temporal_features = temporal_feature_extractor.extract_all_temporal_features(
                    date_ref
                )
                all_features.update(temporal_features)
                all_categories.update({
                    k: 'TEMPORAL' for k in temporal_features.keys()
                })
            
            # 2. Statistical features (from time series)
            if include_statistical:
                try:
                    # Get historical time series
                    time_series = material_service.get_material_historical(
                        material_id,
                        start_date=None,
                        end_date=date_ref,
                        aggregation='daily'
                    )
                    
                    if time_series and time_series.length > 0:
                        # Get quantity series
                        ts_df = time_series.to_dataframe()
                        if 'quantidade_final' in ts_df.columns:
                            quantity_series = pd.Series(
                                ts_df['quantidade_final'].values,
                                index=ts_df['data_referencia']
                            )
                            
                            statistical_features = (
                                statistical_feature_extractor.extract_all_statistical_features(
                                    quantity_series
                                )
                            )
                            all_features.update(statistical_features)
                            all_categories.update({
                                k: 'STATISTICAL' for k in statistical_features.keys()
                            })
                except Exception as e:
                    logger.warning(f"Error extracting statistical features: {e}")
            
            # 3. External features
            if include_external:
                external_features = external_feature_extractor.extract_all_external_features(
                    date_ref
                )
                all_features.update(external_features)
                # Categorize external features
                for key in external_features.keys():
                    if 'temperature' in key or 'precipitation' in key or 'humidity' in key or 'wind' in key or 'corrosion' in key or 'disruption' in key:
                        all_categories[key] = 'CLIMATE'
                    elif 'inflacao' in key or 'cambio' in key or 'pib' in key or 'selic' in key or 'inflation' in key or 'currency' in key:
                        all_categories[key] = 'ECONOMIC'
                    elif '5g' in key or 'cobertura' in key or 'investimento' in key or 'torres' in key:
                        all_categories[key] = '5G'
            
            # 4. Hierarchical features
            if include_hierarchical:
                hierarchical_features = (
                    hierarchical_feature_extractor.extract_all_hierarchical_features(
                        material_id
                    )
                )
                all_features.update(hierarchical_features)
                all_categories.update({
                    k: 'HIERARCHICAL' for k in hierarchical_features.keys()
                })
            
            # 5. Expanded features (52+ features from 25+ data sources)
            if include_expanded:
                expanded_features = expanded_feature_extractor.extract_all_expanded_features(
                    date_ref
                )
                all_features.update(expanded_features)
                # Categorize expanded features
                for key in expanded_features.keys():
                    if 'transport' in key:
                        all_categories[key] = 'TRANSPORT'
                    elif 'trade' in key:
                        all_categories[key] = 'TRADE'
                    elif 'energy' in key:
                        all_categories[key] = 'ENERGY'
                    elif 'employment' in key:
                        all_categories[key] = 'EMPLOYMENT'
                    elif 'construction' in key:
                        all_categories[key] = 'CONSTRUCTION'
                    elif 'industrial' in key:
                        all_categories[key] = 'INDUSTRIAL'
                    elif 'logistics' in key:
                        all_categories[key] = 'LOGISTICS'
                    elif 'regional' in key:
                        all_categories[key] = 'REGIONAL'
                    else:
                        all_categories[key] = 'EXPANDED'
            
            # Create feature vector
            feature_vector = FeatureVector(
                material_id=material_id,
                features=all_features,
                feature_categories=all_categories,
                timestamp=datetime.now()
            )
            
            # Validate
            feature_vector.fill_missing()
            
            logger.info(
                f"Extracted {len(all_features)} features for material {material_id}"
            )
            
            return feature_vector
        except Exception as e:
            logger.error(f"Error in feature extraction pipeline for material {material_id}: {e}")
            raise
    
    def calculate_and_store_features(
        self,
        material_id: int,
        date_ref: Optional[date] = None,
        store_in_db: bool = True
    ) -> FeatureVector:
        """
        Calculate and store features for material
        
        Args:
            material_id: Material ID
            date_ref: Reference date (default: today)
            store_in_db: Store features in database
        
        Returns:
            FeatureVector object
        """
        if date_ref is None:
            date_ref = date.today()
        
        try:
            # Extract all features
            feature_vector = self.extract_all_features(
                material_id,
                date_ref=date_ref
            )
            
            # Store in database if requested
            if store_in_db:
                feature_service.store_features(
                    material_id=material_id,
                    features=feature_vector.features,
                    categories=feature_vector.feature_categories
                )
            
            return feature_vector
        except Exception as e:
            logger.error(f"Error calculating and storing features for material {material_id}: {e}")
            raise
    
    def batch_calculate_features(
        self,
        material_ids: List[int],
        date_ref: Optional[date] = None,
        batch_size: int = 100,
        parallel: bool = False
    ) -> Dict[int, FeatureVector]:
        """
        Calculate features for multiple materials in batch
        
        Args:
            material_ids: List of material IDs
            date_ref: Reference date (default: today)
            batch_size: Batch size for processing
            parallel: Use parallel processing (if enabled)
        
        Returns:
            Dictionary of material_id -> FeatureVector
        """
        if date_ref is None:
            date_ref = date.today()
        
        results = {}
        
        try:
            if FEATURE_PIPELINE.get('parallel_processing', False) and parallel:
                # Parallel processing (simplified - would use multiprocessing or threading)
                import concurrent.futures
                
                def extract_for_material(mid):
                    try:
                        return mid, self.extract_all_features(mid, date_ref=date_ref)
                    except Exception as e:
                        logger.error(f"Error extracting features for material {mid}: {e}")
                        return mid, None
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    futures = [executor.submit(extract_for_material, mid) for mid in material_ids]
                    
                    for future in concurrent.futures.as_completed(futures):
                        mid, feature_vector = future.result()
                        if feature_vector:
                            results[mid] = feature_vector
            else:
                # Sequential processing
                for i, material_id in enumerate(material_ids):
                    try:
                        feature_vector = self.extract_all_features(
                            material_id,
                            date_ref=date_ref
                        )
                        results[material_id] = feature_vector
                        
                        if (i + 1) % batch_size == 0:
                            logger.info(f"Processed {i + 1}/{len(material_ids)} materials")
                    except Exception as e:
                        logger.error(f"Error processing material {material_id}: {e}")
            
            logger.info(f"Batch feature extraction completed: {len(results)}/{len(material_ids)} successful")
            return results
        except Exception as e:
            logger.error(f"Error in batch feature calculation: {e}")
            raise


# Singleton instance
feature_pipeline = FeaturePipeline()

