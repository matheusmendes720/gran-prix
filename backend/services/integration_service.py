"""
Integration service for Nova Corrente
Orchestrates expanded Brazilian API integration with all services
"""
from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
import pandas as pd

from backend.services.database_service import db_service
from backend.services.material_service import material_service
from backend.services.feature_service import feature_service
from backend.services.external_data_service import external_data_service
from backend.services.expanded_api_integration import expanded_api_integration
from backend.services.feature_engineering.feature_pipeline import feature_pipeline
from backend.pipelines.feature_calculation_etl import feature_calculation_etl
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.services.integration')


class IntegrationService:
    """
    Service to orchestrate expanded Brazilian API integration
    """
    
    def run_daily_pipeline(self, date_ref: Optional[date] = None) -> Dict[str, Any]:
        """
        Run complete daily pipeline:
        1. Refresh external data (climate, economic, 5G, transport, trade, etc.)
        2. Calculate daily aggregations
        3. Calculate features for all materials
        4. Generate insights
        
        Args:
            date_ref: Reference date (default: today)
        
        Returns:
            Dictionary with pipeline execution results
        """
        if date_ref is None:
            date_ref = date.today()
        
        results = {
            'date': date_ref.isoformat(),
            'external_data': {},
            'aggregations': 0,
            'features_calculated': 0,
            'insights_generated': 0,
            'status': 'success',
            'errors': []
        }
        
        try:
            logger.info(f"Starting daily pipeline for {date_ref}")
            
            # 1. Refresh external data
            start_date = date_ref - timedelta(days=7)  # Get last 7 days
            end_date = date_ref
            
            try:
                results['external_data']['climate'] = external_data_service.refresh_climate_data(
                    start_date, end_date
                )
            except Exception as e:
                logger.error(f"Error refreshing climate data: {e}")
                results['errors'].append(f"Climate data: {str(e)}")
            
            try:
                results['external_data']['economic'] = external_data_service.refresh_economic_data(
                    start_date, end_date
                )
            except Exception as e:
                logger.error(f"Error refreshing economic data: {e}")
                results['errors'].append(f"Economic data: {str(e)}")
            
            try:
                results['external_data']['5g'] = external_data_service.refresh_5g_data(
                    start_date, end_date
                )
            except Exception as e:
                logger.error(f"Error refreshing 5G data: {e}")
                results['errors'].append(f"5G data: {str(e)}")
            
            # 2. Calculate daily aggregations
            try:
                feature_calculation_etl.calculate_daily_aggregations(date_ref)
                results['aggregations'] = 1
            except Exception as e:
                logger.error(f"Error calculating daily aggregations: {e}")
                results['errors'].append(f"Aggregations: {str(e)}")
            
            # 3. Calculate features for all materials
            try:
                materials = material_service.get_materials(limit=1000)
                material_ids = [m['material_id'] for m in materials]
                
                # Calculate features in batch
                feature_results = feature_pipeline.batch_calculate_features(
                    material_ids,
                    date_ref=date_ref,
                    batch_size=100,
                    parallel=False
                )
                
                results['features_calculated'] = len(feature_results)
            except Exception as e:
                logger.error(f"Error calculating features: {e}")
                results['errors'].append(f"Features: {str(e)}")
            
            # 4. Generate insights (placeholder)
            results['insights_generated'] = 0
            
            if results['errors']:
                results['status'] = 'partial_success'
            else:
                results['status'] = 'success'
            
            logger.info(
                f"Daily pipeline completed: "
                f"{results['features_calculated']} features calculated, "
                f"{len(results['errors'])} errors"
            )
            
            return results
        except Exception as e:
            logger.error(f"Error in daily pipeline: {e}")
            results['status'] = 'error'
            results['errors'].append(f"Pipeline: {str(e)}")
            return results
    
    def refresh_all_external_data(
        self,
        start_date: date,
        end_date: date,
        data_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Refresh all external data sources
        
        Args:
            start_date: Start date
            end_date: End date
            data_types: Optional list of data types to refresh (default: all)
        
        Returns:
            Dictionary with refresh results
        """
        if data_types is None:
            data_types = ['climate', 'economic', '5g', 'transport', 'trade', 'energy', 'employment']
        
        results = {}
        
        try:
            # Standard data sources
            if 'climate' in data_types:
                results['climate'] = external_data_service.refresh_climate_data(
                    start_date, end_date
                )
            
            if 'economic' in data_types:
                results['economic'] = external_data_service.refresh_economic_data(
                    start_date, end_date
                )
            
            if '5g' in data_types:
                results['5g'] = external_data_service.refresh_5g_data(
                    start_date, end_date
                )
            
            # Expanded data sources (25+ sources)
            try:
                expanded_data = expanded_api_integration.fetch_all_expanded_data(
                    start_date, end_date
                )
                results.update(expanded_data)
            except Exception as e:
                logger.warning(f"Error fetching expanded data: {e}")
            
            logger.info(f"Refreshed {len(results)} data sources")
            return results
        except Exception as e:
            logger.error(f"Error refreshing external data: {e}")
            raise
    
    def calculate_features_for_all_materials(
        self,
        date_ref: Optional[date] = None,
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Calculate features for all materials using expanded data sources
        
        Args:
            date_ref: Reference date (default: today)
            batch_size: Batch size for processing
        
        Returns:
            Dictionary with calculation results
        """
        if date_ref is None:
            date_ref = date.today()
        
        try:
            # Get all materials
            materials = material_service.get_materials(limit=10000)
            material_ids = [m['material_id'] for m in materials]
            
            # Calculate features in batch
            feature_results = feature_pipeline.batch_calculate_features(
                material_ids,
                date_ref=date_ref,
                batch_size=batch_size,
                parallel=False
            )
            
            return {
                'total_materials': len(material_ids),
                'features_calculated': len(feature_results),
                'date': date_ref.isoformat(),
                'status': 'success'
            }
        except Exception as e:
            logger.error(f"Error calculating features for all materials: {e}")
            raise
    
    def generate_expanded_features(
        self,
        material_id: int,
        date_ref: Optional[date] = None
    ) -> Dict[str, float]:
        """
        Generate expanded features using all data sources (125+ features)
        
        Args:
            material_id: Material ID
            date_ref: Reference date (default: today)
        
        Returns:
            Dictionary with all features (125+)
        """
        if date_ref is None:
            date_ref = date.today()
        
        try:
            # Extract all features using feature pipeline (includes expanded features)
            feature_vector = feature_pipeline.extract_all_features(
                material_id,
                date_ref=date_ref,
                include_temporal=True,
                include_statistical=True,
                include_external=True,
                include_hierarchical=True,
                include_expanded=True  # Includes 52+ expanded features
            )
            
            logger.info(
                f"Generated {len(feature_vector.features)} features (125+) "
                f"for material {material_id}"
            )
            
            return feature_vector.features
        except Exception as e:
            logger.error(f"Error generating expanded features: {e}")
            raise


# Singleton instance
integration_service = IntegrationService()
