"""
External feature engineering for Nova Corrente
Climate, economic, 5G feature extraction
"""
from typing import Dict, Any, Optional
from datetime import date, datetime
import pandas as pd

from backend.services.database_service import db_service
from backend.config.external_apis_config import EXTERNAL_FEATURES
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.features.external')


class ExternalFeatureExtractor:
    """
    Extract external features (climate, economic, 5G)
    """
    
    def extract_climate_features(
        self,
        date_ref: date,
        location: str = 'Salvador'
    ) -> Dict[str, float]:
        """
        Extract climate features from ClimaSalvador table
        
        Args:
            date_ref: Reference date
            location: Location (default Salvador)
        
        Returns:
            Dictionary of climate feature name -> value
        """
        features = {}
        
        try:
            query = """
                SELECT temperatura_media, temperatura_maxima, temperatura_minima,
                       precipitacao_mm, umidade_percentual, velocidade_vento_kmh,
                       is_extreme_heat, is_heavy_rain, corrosion_risk,
                       field_work_disruption
                FROM ClimaSalvador
                WHERE data_referencia = :date_ref
            """
            
            result = db_service.execute_query(
                query,
                params={'date_ref': date_ref},
                fetch_one=True
            )
            
            if result:
                features['temperature_avg'] = float(result.get('temperatura_media', 0.0) or 0.0)
                features['temperature_max'] = float(result.get('temperatura_maxima', 0.0) or 0.0)
                features['temperature_min'] = float(result.get('temperatura_minima', 0.0) or 0.0)
                features['precipitation_mm'] = float(result.get('precipitacao_mm', 0.0) or 0.0)
                features['humidity_percent'] = float(result.get('umidade_percentual', 0.0) or 0.0)
                features['wind_speed_kmh'] = float(result.get('velocidade_vento_kmh', 0.0) or 0.0)
                features['is_extreme_heat'] = 1.0 if result.get('is_extreme_heat') else 0.0
                features['is_heavy_rain'] = 1.0 if result.get('is_heavy_rain') else 0.0
                features['corrosion_risk'] = float(result.get('corrosion_risk', 0.0) or 0.0)
                features['field_work_disruption'] = float(result.get('field_work_disruption', 0.0) or 0.0)
            else:
                # Default values if not found
                logger.warning(f"No climate data found for {date_ref}")
                features = {key: 0.0 for key in EXTERNAL_FEATURES.get('climate_features', [])}
        except Exception as e:
            logger.warning(f"Error extracting climate features: {e}")
            features = {key: 0.0 for key in EXTERNAL_FEATURES.get('climate_features', [])}
        
        return features
    
    def extract_economic_features(self, date_ref: date) -> Dict[str, float]:
        """
        Extract economic features from IndicadoresEconomicos table
        
        Args:
            date_ref: Reference date
        
        Returns:
            Dictionary of economic feature name -> value
        """
        features = {}
        
        try:
            # Get most recent economic data (may not be daily)
            query = """
                SELECT taxa_inflacao, taxa_inflacao_anual, taxa_cambio_brl_usd,
                       pib_crescimento, taxa_selic, is_high_inflation,
                       is_currency_devaluation
                FROM IndicadoresEconomicos
                WHERE data_referencia <= :date_ref
                ORDER BY data_referencia DESC
                LIMIT 1
            """
            
            result = db_service.execute_query(
                query,
                params={'date_ref': date_ref},
                fetch_one=True
            )
            
            if result:
                features['taxa_inflacao'] = float(result.get('taxa_inflacao', 0.0) or 0.0)
                features['taxa_inflacao_anual'] = float(result.get('taxa_inflacao_anual', 0.0) or 0.0)
                features['taxa_cambio_brl_usd'] = float(result.get('taxa_cambio_brl_usd', 0.0) or 0.0)
                features['pib_crescimento'] = float(result.get('pib_crescimento', 0.0) or 0.0)
                features['taxa_selic'] = float(result.get('taxa_selic', 0.0) or 0.0)
                features['is_high_inflation'] = 1.0 if result.get('is_high_inflation') else 0.0
                features['is_currency_devaluation'] = 1.0 if result.get('is_currency_devaluation') else 0.0
            else:
                logger.warning(f"No economic data found for {date_ref}")
                features = {key: 0.0 for key in EXTERNAL_FEATURES.get('economic_features', [])}
        except Exception as e:
            logger.warning(f"Error extracting economic features: {e}")
            features = {key: 0.0 for key in EXTERNAL_FEATURES.get('economic_features', [])}
        
        return features
    
    def extract_5g_features(self, date_ref: date) -> Dict[str, float]:
        """
        Extract 5G expansion features from Expansao5G table
        
        Args:
            date_ref: Reference date
        
        Returns:
            Dictionary of 5G feature name -> value
        """
        features = {}
        
        try:
            # Get most recent 5G data
            query = """
                SELECT cobertura_5g_percentual, investimento_5g_brl_billions,
                       torres_5g_ativas, is_5g_milestone, taxa_expansao_5g
                FROM Expansao5G
                WHERE data_referencia <= :date_ref
                ORDER BY data_referencia DESC
                LIMIT 1
            """
            
            result = db_service.execute_query(
                query,
                params={'date_ref': date_ref},
                fetch_one=True
            )
            
            if result:
                features['cobertura_5g_percentual'] = float(result.get('cobertura_5g_percentual', 0.0) or 0.0)
                features['investimento_5g_brl_billions'] = float(result.get('investimento_5g_brl_billions', 0.0) or 0.0)
                features['torres_5g_ativas'] = float(result.get('torres_5g_ativas', 0.0) or 0.0)
                features['is_5g_milestone'] = 1.0 if result.get('is_5g_milestone') else 0.0
                features['taxa_expansao_5g'] = float(result.get('taxa_expansao_5g', 0.0) or 0.0)
            else:
                logger.warning(f"No 5G data found for {date_ref}")
                features = {key: 0.0 for key in EXTERNAL_FEATURES.get('5g_features', [])}
        except Exception as e:
            logger.warning(f"Error extracting 5G features: {e}")
            features = {key: 0.0 for key in EXTERNAL_FEATURES.get('5g_features', [])}
        
        return features
    
    def extract_all_external_features(
        self,
        date_ref: date,
        include_climate: bool = True,
        include_economic: bool = True,
        include_5g: bool = True
    ) -> Dict[str, float]:
        """
        Extract all external features
        
        Args:
            date_ref: Reference date
            include_climate: Include climate features
            include_economic: Include economic features
            include_5g: Include 5G features
        
        Returns:
            Dictionary of all external feature name -> value
        """
        features = {}
        
        if include_climate:
            features.update(self.extract_climate_features(date_ref))
        
        if include_economic:
            features.update(self.extract_economic_features(date_ref))
        
        if include_5g:
            features.update(self.extract_5g_features(date_ref))
        
        return features


# Singleton instance
external_feature_extractor = ExternalFeatureExtractor()

