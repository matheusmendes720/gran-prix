"""Daily feature calculation ETL for Nova Corrente"""
from typing import List, Optional
from datetime import date, datetime
import pandas as pd

from backend.services.database_service import db_service
from backend.services.feature_engineering.feature_pipeline import feature_pipeline
from backend.services.material_service import material_service
from backend.config.feature_config import FEATURE_PIPELINE
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.etl.features')


class FeatureCalculationETL:
    """ETL for daily feature calculation"""
    
    def calculate_features_for_material(
        self,
        material_id: int,
        date_ref: date
    ) -> bool:
        """Calculate and store features for a material"""
        try:
            feature_vector = feature_pipeline.calculate_and_store_features(
                material_id,
                date_ref=date_ref,
                store_in_db=True
            )
            
            logger.info(f"Calculated features for material {material_id}")
            return True
        except Exception as e:
            logger.error(f"Error calculating features for material {material_id}: {e}")
            return False
    
    def calculate_daily_aggregations(self, date_ref: date) -> int:
        """Calculate daily aggregations for all materials"""
        try:
            # Call stored procedure
            db_service.execute_procedure(
                'sp_calcular_historico_diario',
                params={'p_data_referencia': date_ref, 'p_material_id': None}
            )
            
            logger.info(f"Calculated daily aggregations for {date_ref}")
            return 1
        except Exception as e:
            logger.error(f"Error calculating daily aggregations: {e}")
            raise
    
    def run(self, date_ref: Optional[date] = None, material_ids: Optional[List[int]] = None) -> int:
        """Run complete feature calculation ETL"""
        try:
            if date_ref is None:
                date_ref = date.today()
            
            # Calculate daily aggregations
            self.calculate_daily_aggregations(date_ref)
            
            # Calculate features for materials
            if material_ids:
                count = 0
                for material_id in material_ids:
                    if self.calculate_features_for_material(material_id, date_ref):
                        count += 1
                
                logger.info(f"Calculated features for {count}/{len(material_ids)} materials")
                return count
            else:
                # Get all active materials
                materials = material_service.get_materials(limit=1000)
                material_ids = [m['material_id'] for m in materials]
                
                count = 0
                for material_id in material_ids:
                    if self.calculate_features_for_material(material_id, date_ref):
                        count += 1
                
                logger.info(f"Calculated features for {count}/{len(material_ids)} materials")
                return count
        except Exception as e:
            logger.error(f"Error running feature calculation ETL: {e}")
            raise


feature_calculation_etl = FeatureCalculationETL()

