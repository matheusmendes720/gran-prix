"""
Pipeline robusto para integração de fatores externos
Inclui clima (INMET), economia (BACEN, IBGE), regulatório (Anatel), tecnológico (GSMA)
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class ExternalFactorsIntegrationPipeline:
    """Pipeline completo para integração de fatores externos"""
    
    def __init__(self, raw_data_dir: str = 'data/raw', processed_dir: str = 'data/processed'):
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def load_climate_data(self, region: str = 'bahia_salvador') -> pd.DataFrame:
        """Carregar dados climáticos do INMET"""
        climate_files = list(self.raw_data_dir.glob(f'**/inmet_*{region}*.csv'))
        
        if not climate_files:
            logger.warning(f"No climate data found for region: {region}")
            return pd.DataFrame()
        
        climate_dfs = []
        for f in climate_files:
            try:
                df = pd.read_csv(f, encoding='latin-1', low_memory=False)
                
                # Padronizar colunas de data
                date_cols = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
                if date_cols:
                    # Tentar diferentes formatos de data
                    for date_col in date_cols:
                        try:
                            df['date'] = pd.to_datetime(df[date_col], errors='coerce', format='%Y-%m-%d %H:%M:%S')
                            if df['date'].notna().any():
                                break
                            else:
                                df['date'] = pd.to_datetime(df[date_col], errors='coerce')
                                if df['date'].notna().any():
                                    break
                        except Exception:
                            continue
                    
                    df = df.dropna(subset=['date'])
                    
                    if df.empty:
                        continue
                
                # Extrair métricas climáticas
                temp_cols = [col for col in df.columns if 'temp' in col.lower() and 'umid' not in col.lower()]
                prec_cols = [col for col in df.columns if 'prec' in col.lower() or 'chuva' in col.lower() or 'rain' in col.lower()]
                umid_cols = [col for col in df.columns if 'umid' in col.lower() or 'humid' in col.lower()]
                
                climate_df = pd.DataFrame()
                climate_df['date'] = df['date']
                
                if temp_cols:
                    climate_df['temperature'] = pd.to_numeric(df[temp_cols[0]], errors='coerce')
                if prec_cols:
                    climate_df['precipitation'] = pd.to_numeric(df[prec_cols[0]], errors='coerce')
                if umid_cols:
                    climate_df['humidity'] = pd.to_numeric(df[umid_cols[0]], errors='coerce')
                
                climate_dfs.append(climate_df.dropna(subset=['date']))
            except Exception as e:
                logger.warning(f"Failed to process climate file {f}: {e}")
        
        if climate_dfs:
            combined = pd.concat(climate_dfs, ignore_index=True)
            # Agregar por dia (média temperatura/umidade, soma precipitação)
            combined['date'] = pd.to_datetime(combined['date'])
            combined['date_only'] = combined['date'].dt.date
            
            daily = combined.groupby('date_only').agg({
                'temperature': 'mean',
                'precipitation': 'sum',
                'humidity': 'mean'
            }).reset_index()
            
            daily['date'] = pd.to_datetime(daily['date_only'])
            daily = daily.drop('date_only', axis=1)
            
            logger.info(f"Loaded climate data: {len(daily)} daily records for {region}")
            return daily
        
        return pd.DataFrame()
    
    def load_economic_data(self) -> pd.DataFrame:
        """Carregar dados econômicos do BACEN e IBGE"""
        economic_files = list(self.raw_data_dir.glob('**/bacen_*.csv')) + \
                        list(self.raw_data_dir.glob('**/ibge_*.csv'))
        
        if not economic_files:
            logger.warning("No economic data found")
            return pd.DataFrame()
        
        economic_dfs = []
        for f in economic_files:
            try:
                df = pd.read_csv(f, encoding='utf-8', low_memory=False)
                
                # Identificar coluna de data
                date_cols = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
                if not date_cols:
                    continue
                
                df['date'] = pd.to_datetime(df[date_cols[0]], errors='coerce')
                df = df.dropna(subset=['date'])
                
                if df.empty:
                    continue
                
                # Identificar tipo de dado econômico
                file_lower = str(f).lower()
                
                if 'exchange_rate' in file_lower or 'usd' in file_lower or 'dolar' in file_lower:
                    value_cols = [col for col in df.columns if 'valor' in col.lower() or 'value' in col.lower() or 'rate' in col.lower() or 'exchange' in col.lower()]
                    if value_cols:
                        economic_df = pd.DataFrame()
                        economic_df['date'] = df['date']
                        economic_df['exchange_rate_usd_brl'] = pd.to_numeric(df[value_cols[0]], errors='coerce')
                        economic_dfs.append(economic_df)
                
                elif 'selic' in file_lower or 'interest' in file_lower or 'juros' in file_lower:
                    value_cols = [col for col in df.columns if 'valor' in col.lower() or 'value' in col.lower() or 'rate' in col.lower() or 'selic' in col.lower()]
                    if value_cols:
                        economic_df = pd.DataFrame()
                        economic_df['date'] = df['date']
                        economic_df['selic_rate'] = pd.to_numeric(df[value_cols[0]], errors='coerce')
                        economic_dfs.append(economic_df)
                
                elif 'ipca' in file_lower or 'inflation' in file_lower or 'inflacao' in file_lower:
                    value_cols = [col for col in df.columns if 'valor' in col.lower() or 'value' in col.lower() or 'ipca' in col.lower() or 'inflation' in col.lower()]
                    if value_cols:
                        economic_df = pd.DataFrame()
                        economic_df['date'] = df['date']
                        economic_df['inflation_rate'] = pd.to_numeric(df[value_cols[0]], errors='coerce')
                        economic_dfs.append(economic_df)
                
                elif 'gdp' in file_lower or 'pib' in file_lower:
                    value_cols = [col for col in df.columns if 'valor' in col.lower() or 'value' in col.lower() or 'gdp' in col.lower() or 'pib' in col.lower()]
                    if value_cols:
                        economic_df = pd.DataFrame()
                        economic_df['date'] = df['date']
                        economic_df['gdp_growth'] = pd.to_numeric(df[value_cols[0]], errors='coerce')
                        economic_dfs.append(economic_df)
            except Exception as e:
                logger.warning(f"Failed to process economic file {f}: {e}")
        
        if economic_dfs:
            # Merge de todos os dados econômicos
            economic_combined = economic_dfs[0]
            for df in economic_dfs[1:]:
                economic_combined = economic_combined.merge(df, on='date', how='outer')
            
            economic_combined = economic_combined.sort_values('date')
            logger.info(f"Loaded economic data: {len(economic_combined)} records with {len(economic_combined.columns) - 1} metrics")
            return economic_combined
        
        return pd.DataFrame()
    
    def integrate_external_factors(self, main_dataset: pd.DataFrame, 
                                   region: str = 'bahia_salvador') -> pd.DataFrame:
        """Integrar todos os fatores externos ao dataset principal"""
        logger.info("Integrating external factors...")
        
        # Garantir que a coluna date existe e está no formato correto
        if 'date' not in main_dataset.columns:
            logger.error("Main dataset must have a 'date' column")
            return main_dataset
        
        main_dataset = main_dataset.copy()
        main_dataset['date'] = pd.to_datetime(main_dataset['date'], errors='coerce')
        main_dataset = main_dataset.dropna(subset=['date'])
        
        initial_rows = len(main_dataset)
        
        # Carregar dados climáticos
        climate_df = self.load_climate_data(region)
        if not climate_df.empty:
            main_dataset = main_dataset.merge(climate_df, on='date', how='left')
            logger.info(f"✓ Integrated climate data: {len(climate_df)} records")
        
        # Carregar dados econômicos
        economic_df = self.load_economic_data()
        if not economic_df.empty:
            main_dataset = main_dataset.merge(economic_df, on='date', how='left')
            logger.info(f"✓ Integrated economic data: {len(economic_df)} records")
        
        # Adicionar flags e scores de impacto
        main_dataset = self._add_impact_flags(main_dataset)
        main_dataset = self._calculate_impact_scores(main_dataset)
        
        logger.info(f"✓ Integration complete: {initial_rows} → {len(main_dataset)} rows, {len(main_dataset.columns)} columns")
        
        return main_dataset
    
    def _add_impact_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adicionar flags de impacto baseados em thresholds"""
        # Flags climáticas
        if 'temperature' in df.columns:
            df['extreme_heat'] = (df['temperature'] > 32).astype(int)
            df['extreme_cold'] = (df['temperature'] < 10).astype(int)
        
        if 'precipitation' in df.columns:
            df['heavy_rain'] = (df['precipitation'] > 50).astype(int)
            df['moderate_rain'] = ((df['precipitation'] > 10) & (df['precipitation'] <= 50)).astype(int)
            df['drought_risk'] = ((df['precipitation'] == 0) & (df['temperature'] > 30)).astype(int)
        
        if 'humidity' in df.columns:
            df['high_humidity'] = (df['humidity'] > 80).astype(int)
            df['low_humidity'] = (df['humidity'] < 30).astype(int)
        
        # Flags econômicas
        if 'inflation_rate' in df.columns:
            df['high_inflation'] = (df['inflation_rate'] > 5.0).astype(int)
            df['moderate_inflation'] = ((df['inflation_rate'] > 2.0) & (df['inflation_rate'] <= 5.0)).astype(int)
        
        if 'exchange_rate_usd_brl' in df.columns:
            df['currency_devaluation'] = (df['exchange_rate_usd_brl'] > 5.5).astype(int)
            df['currency_volatility'] = df['exchange_rate_usd_brl'].rolling(window=7).std() > 0.1
        
        if 'selic_rate' in df.columns:
            df['high_interest'] = (df['selic_rate'] > 10.0).astype(int)
        
        return df
    
    def _calculate_impact_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcular scores de impacto combinado"""
        # Climate impact score (0-1)
        climate_score = pd.Series(0.0, index=df.index)
        
        if 'extreme_heat' in df.columns:
            climate_score += df['extreme_heat'] * 0.3
        if 'heavy_rain' in df.columns:
            climate_score += df['heavy_rain'] * 0.4
        if 'high_humidity' in df.columns:
            climate_score += df['high_humidity'] * 0.2
        if 'drought_risk' in df.columns:
            climate_score += df['drought_risk'] * 0.1
        
        df['climate_impact'] = np.clip(climate_score, 0, 1)
        
        # Economic impact score (0-1)
        economic_score = pd.Series(0.0, index=df.index)
        
        if 'high_inflation' in df.columns:
            economic_score += df['high_inflation'] * 0.5
        if 'currency_devaluation' in df.columns:
            economic_score += df['currency_devaluation'] * 0.5
        if 'high_interest' in df.columns:
            economic_score += df['high_interest'] * 0.2
        
        df['economic_impact'] = np.clip(economic_score, 0, 1)
        
        # Combined demand adjustment factor
        df['demand_adjustment_factor'] = 1.0 + (
            df.get('climate_impact', pd.Series(0, index=df.index)) * 0.3 +
            df.get('economic_impact', pd.Series(0, index=df.index)) * 0.1
        )
        
        logger.info("  ✓ Calculated climate_impact score")
        logger.info("  ✓ Calculated economic_impact score")
        logger.info("  ✓ Calculated demand_adjustment_factor")
        
        return df
    
    def save_enriched_dataset(self, df: pd.DataFrame, dataset_id: str) -> Path:
        """Salvar dataset enriquecido"""
        output_path = self.processed_dir / 'ml_ready' / f"{dataset_id}_enriched.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False)
        logger.info(f"✓ Saved enriched dataset: {output_path}")
        
        return output_path

