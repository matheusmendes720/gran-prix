"""
Pipeline para estruturar dados brutos em formato ML-ready
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class MLDataStructuringPipeline:
    """Pipeline para estruturar dados para ML"""
    
    def __init__(self, output_dir: str = 'data/processed/ml_ready'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def structure_dataset(self, dataset_id: str, raw_file_path: str, 
                         config: Dict) -> pd.DataFrame:
        """Estruturar dataset individual"""
        raw_path = Path(raw_file_path)
        
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw file not found: {raw_file_path}")
        
        # Carregar dados brutos
        logger.info(f"Loading raw data from: {raw_path}")
        try:
            if raw_path.suffix == '.csv':
                # Tentar diferentes encodings
                for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                    try:
                        df = pd.read_csv(raw_path, encoding=encoding, low_memory=False)
                        break
                    except UnicodeDecodeError:
                        continue
            elif raw_path.suffix == '.json':
                df = pd.read_json(raw_path)
            elif raw_path.suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(raw_path)
            else:
                raise ValueError(f"Unsupported file format: {raw_path.suffix}")
        except Exception as e:
            logger.error(f"Failed to load file {raw_path}: {e}")
            raise
        
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Aplicar mapeamento de colunas
        column_mapping = config.get('columns_mapping', {})
        structured_df = self._apply_column_mapping(df, column_mapping, dataset_id)
        
        # Adicionar features de tempo
        structured_df = self._add_temporal_features(structured_df)
        
        # Adicionar dataset_source
        structured_df['dataset_source'] = dataset_id
        
        # Validar estrutura
        structured_df = self._validate_structure(structured_df, config)
        
        # Salvar dataset estruturado
        output_path = self.output_dir / f"{dataset_id}_structured.csv"
        structured_df.to_csv(output_path, index=False)
        
        logger.info(f"Structured dataset {dataset_id}: {len(structured_df)} rows, {len(structured_df.columns)} columns")
        logger.info(f"Saved to: {output_path}")
        
        return structured_df
    
    def _apply_column_mapping(self, df: pd.DataFrame, mapping: Dict, dataset_id: str) -> pd.DataFrame:
        """Aplicar mapeamento de colunas"""
        structured_df = df.copy()
        
        # Renomear colunas
        rename_map = {v: k for k, v in mapping.items() if v is not None and v in df.columns}
        structured_df = structured_df.rename(columns=rename_map)
        
        # Adicionar colunas obrigatórias ausentes
        required_cols = {
            'date': None,
            'item_id': None,
            'quantity': None
        }
        
        for col in required_cols:
            if col not in structured_df.columns:
                if col == 'date':
                    # Tentar gerar data a partir do índice
                    if isinstance(df.index, pd.DatetimeIndex):
                        structured_df[col] = df.index
                    else:
                        # Gerar datas sintéticas
                        structured_df[col] = pd.date_range(
                            start='2020-01-01', 
                            periods=len(df), 
                            freq='D'
                        )
                elif col == 'item_id':
                    # Gerar IDs sequenciais
                    structured_df[col] = [f"{dataset_id}_{i}" for i in range(len(df))]
                elif col == 'quantity':
                    # Tentar encontrar coluna numérica semelhante
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        structured_df[col] = df[numeric_cols[0]].fillna(0)
                    else:
                        structured_df[col] = 0
        
        return structured_df
    
    def _add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adicionar features temporais"""
        if 'date' not in df.columns:
            logger.warning("No 'date' column found, skipping temporal features")
            return df
        
        # Converter para datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Remover linhas com data inválida
        df = df.dropna(subset=['date'])
        
        if len(df) == 0:
            logger.warning("All dates invalid after conversion")
            return df
        
        # Features cíclicas (sin/cos para capturar periodicidade)
        df['day_of_year'] = df['date'].dt.dayofyear
        df['day_of_year_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365.25)
        df['day_of_year_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365.25)
        
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['week_of_year_sin'] = np.sin(2 * np.pi * df['week_of_year'] / 52.14)
        df['week_of_year_cos'] = np.cos(2 * np.pi * df['week_of_year'] / 52.14)
        
        df['day_of_month'] = df['date'].dt.day
        df['day_of_month_sin'] = np.sin(2 * np.pi * df['day_of_month'] / 30.44)
        df['day_of_month_cos'] = np.cos(2 * np.pi * df['day_of_month'] / 30.44)
        
        # Features categóricas
        df['month'] = df['date'].dt.month
        df['weekday'] = df['date'].dt.weekday
        df['quarter'] = df['date'].dt.quarter
        df['year'] = df['date'].dt.year
        
        # Features booleanas
        df['is_weekend'] = (df['date'].dt.weekday >= 5).astype(int)
        df['is_month_start'] = (df['date'].dt.day <= 7).astype(int)
        df['is_month_end'] = (df['date'].dt.day >= 25).astype(int)
        
        # Features brasileiras
        df['is_holiday'] = self._get_brazilian_holidays(df['date']).astype(int)
        df['is_carnival'] = self._get_carnival_dates(df['date']).astype(int)
        
        # Remover colunas auxiliares
        df = df.drop(columns=['day_of_year', 'week_of_year', 'day_of_month'], errors='ignore')
        
        return df
    
    def _get_brazilian_holidays(self, dates: pd.Series) -> pd.Series:
        """Identificar feriados brasileiros fixos"""
        # Feriados fixos (mês, dia)
        fixed_holidays = [
            (1, 1),   # Ano Novo
            (4, 21),  # Tiradentes
            (5, 1),   # Dia do Trabalhador
            (9, 7),   # Independência
            (10, 12), # Nossa Senhora Aparecida
            (11, 2),  # Finados
            (11, 15), # Proclamação da República
            (12, 25)  # Natal
        ]
        
        is_holiday = pd.Series(False, index=dates.index)
        for month, day in fixed_holidays:
            is_holiday |= (dates.dt.month == month) & (dates.dt.day == day)
        
        return is_holiday
    
    def _get_carnival_dates(self, dates: pd.Series) -> pd.Series:
        """Identificar datas de carnaval (aproximado - segunda-feira anterior à quarta-feira de cinzas)"""
        # Carnaval varia por ano, mas geralmente em fevereiro/março
        # Aproximação: segunda-feira de fevereiro ou início de março
        is_carnival = pd.Series(False, index=dates.index)
        
        # Para simplificar, marcar período de carnaval (fevereiro/março)
        is_carnival |= (dates.dt.month == 2) & (dates.dt.day >= 10) & (dates.dt.day <= 17)
        is_carnival |= (dates.dt.month == 3) & (dates.dt.day <= 5)
        
        return is_carnival
    
    def _validate_structure(self, df: pd.DataFrame, config: Dict) -> pd.DataFrame:
        """Validar estrutura do dataset"""
        # Verificar colunas obrigatórias
        required = ['date', 'item_id', 'quantity']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Remover outliers em quantity (IQR method)
        if 'quantity' in df.columns:
            Q1 = df['quantity'].quantile(0.25)
            Q3 = df['quantity'].quantile(0.75)
            IQR = Q3 - Q1
            if IQR > 0:
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                initial_count = len(df)
                df = df[(df['quantity'] >= lower_bound) & (df['quantity'] <= upper_bound)]
                removed = initial_count - len(df)
                if removed > 0:
                    logger.info(f"Removed {removed} outliers using IQR method")
        
        # Preencher valores ausentes
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isna().any():
                df[col] = df[col].fillna(method='ffill').fillna(method='bfill').fillna(0)
        
        # Preencher strings com 'unknown'
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            if col != 'date':  # Não preencher date
                df[col] = df[col].fillna('unknown')
        
        return df
    
    def merge_with_external_factors(self, structured_df: pd.DataFrame, 
                                   external_factors_dir: str = 'data/raw') -> pd.DataFrame:
        """Mesclar com fatores externos"""
        external_dir = Path(external_factors_dir)
        
        if not external_dir.exists():
            logger.warning(f"External factors directory not found: {external_dir}")
            return structured_df
        
        # Carregar fatores climáticos (INMET)
        climate_files = list(external_dir.glob('**/inmet_*.csv'))
        if climate_files:
            logger.info(f"Found {len(climate_files)} climate files")
            climate_dfs = []
            for f in climate_files:
                try:
                    df = pd.read_csv(f, encoding='latin-1', low_memory=False)
                    # Tentar identificar coluna de data
                    date_cols = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower()]
                    if date_cols:
                        df['date'] = pd.to_datetime(df[date_cols[0]], errors='coerce')
                        df = df.dropna(subset=['date'])
                        # Extrair temperatura, precipitação, umidade
                        temp_cols = [col for col in df.columns if 'temp' in col.lower() and 'umid' not in col.lower()]
                        prec_cols = [col for col in df.columns if 'prec' in col.lower() or 'chuva' in col.lower()]
                        umid_cols = [col for col in df.columns if 'umid' in col.lower() or 'humid' in col.lower()]
                        
                        if temp_cols:
                            df['temperature'] = pd.to_numeric(df[temp_cols[0]], errors='coerce')
                        if prec_cols:
                            df['precipitation'] = pd.to_numeric(df[prec_cols[0]], errors='coerce')
                        if umid_cols:
                            df['humidity'] = pd.to_numeric(df[umid_cols[0]], errors='coerce')
                        
                        climate_dfs.append(df[['date', 'temperature', 'precipitation', 'humidity']].dropna(subset=['date']))
                except Exception as e:
                    logger.warning(f"Failed to process climate file {f}: {e}")
            
            if climate_dfs:
                climate_df = pd.concat(climate_dfs, ignore_index=True)
                climate_df = climate_df.groupby('date').agg({
                    'temperature': 'mean',
                    'precipitation': 'sum',
                    'humidity': 'mean'
                }).reset_index()
                structured_df = structured_df.merge(
                    climate_df,
                    on='date',
                    how='left'
                )
                logger.info(f"Merged climate data: {len(climate_df)} records")
        
        # Carregar fatores econômicos (BACEN)
        economic_files = list(external_dir.glob('**/bacen_*.json'))
        if economic_files:
            logger.info(f"Found {len(economic_files)} economic files")
            economic_data = []
            for f in economic_files:
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        if isinstance(data, list):
                            economic_data.extend(data)
                except Exception as e:
                    logger.warning(f"Failed to process economic file {f}: {e}")
            
            if economic_data:
                economic_df = pd.DataFrame(economic_data)
                # BACEN retorna {'data': '01/01/2020', 'valor': 4.5}
                if 'data' in economic_df.columns:
                    economic_df['date'] = pd.to_datetime(economic_df['data'], format='%d/%m/%Y', errors='coerce')
                    if 'valor' in economic_df.columns:
                        economic_df['exchange_rate'] = pd.to_numeric(economic_df['valor'], errors='coerce')
                        economic_df = economic_df[['date', 'exchange_rate']].dropna()
                        # Mesclar com structured_df
                        # Se houver múltiplos datasets econômicos, pode ser necessário fazer merge mais complexo
                        structured_df = structured_df.merge(
                            economic_df,
                            on='date',
                            how='left'
                        )
                        logger.info(f"Merged economic data: {len(economic_df)} records")
        
        return structured_df
    
    def combine_all_datasets(self, structured_datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Combinar múltiplos datasets estruturados"""
        if not structured_datasets:
            logger.warning("No structured datasets to combine")
            return pd.DataFrame()
        
        logger.info(f"Combining {len(structured_datasets)} datasets")
        
        # Combinar todos os datasets
        combined_df = pd.concat(structured_datasets.values(), ignore_index=True)
        
        # Ordenar por data
        if 'date' in combined_df.columns:
            combined_df = combined_df.sort_values('date').reset_index(drop=True)
        
        # Salvar dataset combinado
        output_path = self.output_dir / "all_datasets_combined.csv"
        combined_df.to_csv(output_path, index=False)
        
        logger.info(f"Combined dataset: {len(combined_df)} rows, {len(combined_df.columns)} columns")
        logger.info(f"Saved to: {output_path}")
        
        return combined_df

