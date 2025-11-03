"""
Temporal feature engineering for Nova Corrente
Cyclical encoding, Brazilian calendar features
"""
from typing import Dict, Any, List
from datetime import datetime, date
import pandas as pd
import numpy as np

from backend.services.database_service import db_service
from backend.config.feature_config import TEMPORAL_FEATURES
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.features.temporal')


class TemporalFeatureExtractor:
    """
    Extract temporal features from dates
    """
    
    def extract_cyclical_features(self, date_obj: date) -> Dict[str, float]:
        """
        Extract cyclical temporal features using sin/cos encoding
        
        Args:
            date_obj: Date object
        
        Returns:
            Dictionary of cyclical feature name -> value
        """
        features = {}
        
        # Day of year (1-365)
        day_of_year = date_obj.timetuple().tm_yday
        features['day_of_year_sin'] = np.sin(2 * np.pi * day_of_year / 365.25)
        features['day_of_year_cos'] = np.cos(2 * np.pi * day_of_year / 365.25)
        
        # Week of year (1-52)
        week_of_year = date_obj.isocalendar()[1]
        features['week_of_year_sin'] = np.sin(2 * np.pi * week_of_year / 52)
        features['week_of_year_cos'] = np.cos(2 * np.pi * week_of_year / 52)
        
        # Day of week (1=Monday, 7=Sunday)
        day_of_week = date_obj.weekday() + 1
        features['day_of_week_sin'] = np.sin(2 * np.pi * day_of_week / 7)
        features['day_of_week_cos'] = np.cos(2 * np.pi * day_of_week / 7)
        
        # Month (1-12)
        month = date_obj.month
        features['month_sin'] = np.sin(2 * np.pi * month / 12)
        features['month_cos'] = np.cos(2 * np.pi * month / 12)
        
        # Quarter (1-4)
        quarter = (month - 1) // 3 + 1
        features['quarter_sin'] = np.sin(2 * np.pi * quarter / 4)
        features['quarter_cos'] = np.cos(2 * np.pi * quarter / 4)
        
        return features
    
    def extract_categorical_features(self, date_obj: date) -> Dict[str, int]:
        """
        Extract categorical temporal features
        
        Args:
            date_obj: Date object
        
        Returns:
            Dictionary of categorical feature name -> value
        """
        features = {}
        
        # Basic categorical
        features['year'] = date_obj.year
        features['month'] = date_obj.month
        features['day'] = date_obj.day
        features['weekday'] = date_obj.weekday() + 1  # 1=Monday, 7=Sunday
        features['quarter'] = (date_obj.month - 1) // 3 + 1
        
        # Weekday encoding
        features['is_weekend'] = 1 if date_obj.weekday() >= 5 else 0
        features['is_month_start'] = 1 if date_obj.day <= 7 else 0
        features['is_month_end'] = 1 if date_obj.day >= 25 else 0
        
        return features
    
    def extract_brazilian_calendar_features(
        self,
        date_obj: date
    ) -> Dict[str, int]:
        """
        Extract Brazilian calendar features (holidays, seasons, etc.)
        
        Args:
            date_obj: Date object
        
        Returns:
            Dictionary of Brazilian calendar feature name -> value
        """
        features = {}
        
        try:
            # Get Brazilian calendar data
            query = """
                SELECT is_feriado, is_carnaval, is_natal, is_verao, is_chuva_sazonal,
                       impact_demanda, nome_feriado
                FROM CalendarioBrasil
                WHERE data_referencia = :date_ref
            """
            
            result = db_service.execute_query(
                query,
                params={'date_ref': date_obj},
                fetch_one=True
            )
            
            if result:
                features['is_feriado'] = 1 if result.get('is_feriado') else 0
                features['is_carnaval'] = 1 if result.get('is_carnaval') else 0
                features['is_natal'] = 1 if result.get('is_natal') else 0
                features['is_verao'] = 1 if result.get('is_verao') else 0
                features['is_chuva_sazonal'] = 1 if result.get('is_chuva_sazonal') else 0
                features['impact_demanda'] = float(result.get('impact_demanda', 1.0))
            else:
                # Default values if not in calendar
                features['is_feriado'] = 0
                features['is_carnaval'] = 0
                features['is_natal'] = 0
                features['is_verao'] = 0
                features['is_chuva_sazonal'] = 0
                features['impact_demanda'] = 1.0
        except Exception as e:
            logger.warning(f"Error extracting Brazilian calendar features: {e}")
            # Default values on error
            features['is_feriado'] = 0
            features['is_carnaval'] = 0
            features['is_natal'] = 0
            features['is_verao'] = 0
            features['is_chuva_sazonal'] = 0
            features['impact_demanda'] = 1.0
        
        return features
    
    def extract_all_temporal_features(
        self,
        date_obj: date,
        include_cyclical: bool = True,
        include_categorical: bool = True,
        include_brazilian: bool = True
    ) -> Dict[str, float]:
        """
        Extract all temporal features
        
        Args:
            date_obj: Date object
            include_cyclical: Include cyclical features (sin/cos)
            include_categorical: Include categorical features
            include_brazilian: Include Brazilian calendar features
        
        Returns:
            Dictionary of all temporal feature name -> value
        """
        features = {}
        
        if include_cyclical:
            features.update(self.extract_cyclical_features(date_obj))
        
        if include_categorical:
            cat_features = self.extract_categorical_features(date_obj)
            features.update({k: float(v) for k, v in cat_features.items()})
        
        if include_brazilian:
            features.update(self.extract_brazilian_calendar_features(date_obj))
        
        return features
    
    def extract_for_date_range(
        self,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """
        Extract temporal features for a date range
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            DataFrame with date and temporal features
        """
        try:
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            rows = []
            for date_obj in date_range:
                row = {'data_referencia': date_obj.date()}
                row.update(self.extract_all_temporal_features(date_obj.date()))
                rows.append(row)
            
            df = pd.DataFrame(rows)
            logger.info(f"Extracted temporal features for {len(df)} dates")
            return df
        except Exception as e:
            logger.error(f"Error extracting temporal features for range: {e}")
            raise


# Singleton instance
temporal_feature_extractor = TemporalFeatureExtractor()

