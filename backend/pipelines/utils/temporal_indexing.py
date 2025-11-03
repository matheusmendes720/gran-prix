"""
Sistema de Indexação Temporal para Datasets sem Coluna de Data
Cria timestamps sintéticos baseados em ordem, padrões temporais e características dos dados
"""
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TemporalIndexer:
    """Cria índices temporais para datasets sem coluna de data explícita"""
    
    def __init__(self, base_date: Optional[str] = None, frequency: str = 'D'):
        """
        Args:
            base_date: Data base para início da série (default: hoje - 2 anos)
            frequency: Frequência temporal ('D' para diário, 'H' para horário, etc.)
        """
        if base_date:
            self.base_date = pd.to_datetime(base_date)
        else:
            # Default: 2 anos atrás
            self.base_date = pd.to_datetime(datetime.now()) - pd.Timedelta(days=730)
        
        self.frequency = frequency
    
    def create_index_from_order(self, df: pd.DataFrame, 
                                 date_col: str = 'date',
                                 sort_by: Optional[list] = None) -> pd.DataFrame:
        """
        Cria índice temporal baseado na ordem das linhas
        
        Args:
            df: DataFrame sem coluna de data
            date_col: Nome da coluna de data a ser criada
            sort_by: Colunas para ordenar antes de criar índice (ex: ['item_id', 'quantity'])
        
        Returns:
            DataFrame com coluna de data criada
        """
        df = df.copy()
        
        # Ordenar se especificado
        if sort_by:
            df = df.sort_values(sort_by).reset_index(drop=True)
        
        # Criar índice temporal sequencial
        date_range = pd.date_range(
            start=self.base_date,
            periods=len(df),
            freq=self.frequency
        )
        
        df[date_col] = date_range[:len(df)]
        
        logger.info(f"Created temporal index from order: {len(df)} records")
        logger.info(f"  Date range: {df[date_col].min()} to {df[date_col].max()}")
        
        return df
    
    def create_index_from_patterns(self, df: pd.DataFrame,
                                    group_by: Optional[str] = None,
                                    date_col: str = 'date',
                                    pattern_hint: Optional[str] = None) -> pd.DataFrame:
        """
        Cria índice temporal baseado em padrões detectados nos dados
        
        Args:
            df: DataFrame sem coluna de data
            group_by: Coluna para agrupar (cada grupo tem sua própria série temporal)
            date_col: Nome da coluna de data a ser criada
            pattern_hint: Dica de padrão ('daily', 'weekly', 'monthly', 'hourly')
        
        Returns:
            DataFrame com coluna de data criada
        """
        df = df.copy()
        
        # Detectar padrão se não especificado
        if not pattern_hint:
            pattern_hint = self._detect_temporal_pattern(df)
        
        # Determinar frequência baseada no padrão
        freq_map = {
            'hourly': 'H',
            'daily': 'D',
            'weekly': 'W',
            'monthly': 'M',
        }
        freq = freq_map.get(pattern_hint.lower(), 'D')
        
        if group_by and group_by in df.columns:
            # Criar série temporal por grupo
            df = df.sort_values(group_by).reset_index(drop=True)
            
            date_list = []
            current_date = self.base_date
            
            last_group = None
            for idx, row in df.iterrows():
                current_group = row[group_by]
                
                # Se mudou de grupo, resetar data
                if last_group is not None and current_group != last_group:
                    current_date = self.base_date
                
                date_list.append(current_date)
                current_date += pd.Timedelta(1, freq)
                last_group = current_group
        else:
            # Criar série temporal simples
            date_range = pd.date_range(
                start=self.base_date,
                periods=len(df),
                freq=freq
            )
            date_list = date_range[:len(df)]
        
        df[date_col] = pd.Series(date_list)
        
        logger.info(f"Created temporal index from patterns: {pattern_hint}")
        logger.info(f"  Date range: {df[date_col].min()} to {df[date_col].max()}")
        
        return df
    
    def create_index_from_external(self, df: pd.DataFrame,
                                   external_data: pd.DataFrame,
                                   join_cols: list,
                                   date_col_external: str,
                                   date_col: str = 'date') -> pd.DataFrame:
        """
        Cria índice temporal a partir de dados externos que têm timestamps
        
        Args:
            df: DataFrame sem coluna de data
            external_data: DataFrame externo com timestamps
            join_cols: Colunas para fazer join
            date_col_external: Nome da coluna de data no DataFrame externo
            date_col: Nome da coluna de data a ser criada
        
        Returns:
            DataFrame com coluna de data criada
        """
        df = df.copy()
        
        # Fazer merge com dados externos
        merge_df = external_data[[date_col_external] + join_cols].copy()
        
        df = df.merge(
            merge_df,
            on=join_cols,
            how='left',
            suffixes=('', '_external')
        )
        
        # Renomear coluna
        df[date_col] = df[date_col_external]
        df = df.drop(columns=[date_col_external])
        
        # Preencher datas faltantes com interpolação ou forward fill
        if df[date_col].isnull().sum() > 0:
            df = df.sort_values([date_col] + join_cols)
            df[date_col] = df[date_col].fillna(method='ffill')
            
            if df[date_col].isnull().sum() > 0:
                # Se ainda houver nulos, usar índice sequencial
                null_mask = df[date_col].isnull()
                n_nulls = null_mask.sum()
                if n_nulls > 0:
                    logger.warning(f"Filling {n_nulls} null dates with sequential index")
                    date_range = pd.date_range(
                        start=self.base_date,
                        periods=n_nulls,
                        freq=self.frequency
                    )
                    df.loc[null_mask, date_col] = date_range[:n_nulls]
        
        logger.info(f"Created temporal index from external data")
        logger.info(f"  Date range: {df[date_col].min()} to {df[date_col].max()}")
        logger.info(f"  Matched: {(df[date_col].notna()).sum()}/{len(df)} records")
        
        return df
    
    def _detect_temporal_pattern(self, df: pd.DataFrame) -> str:
        """
        Tenta detectar padrão temporal nos dados
        
        Returns:
            Padrão detectado ('hourly', 'daily', 'weekly', 'monthly')
        """
        # Heurísticas simples
        n_records = len(df)
        
        if n_records < 100:
            return 'daily'
        elif n_records < 1000:
            # Possivelmente diário ou semanal
            return 'daily'
        elif n_records < 10000:
            # Possivelmente horário ou diário
            return 'daily'
        else:
            # Datasets grandes podem ser horários
            return 'daily'
    
    def enhance_with_temporal_features(self, df: pd.DataFrame,
                                       date_col: str = 'date') -> pd.DataFrame:
        """
        Adiciona features temporais após criar índice
        
        Args:
            df: DataFrame com coluna de data
            date_col: Nome da coluna de data
        
        Returns:
            DataFrame com features temporais adicionadas
        """
        if date_col not in df.columns:
            logger.warning(f"Date column '{date_col}' not found, skipping temporal features")
            return df
        
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        
        # Features básicas
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        df['weekday'] = df[date_col].dt.weekday
        df['week'] = df[date_col].dt.isocalendar().week
        df['quarter'] = df[date_col].dt.quarter
        df['day_of_year'] = df[date_col].dt.dayofyear
        
        # Features cíclicas (para ML)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['weekday_sin'] = np.sin(2 * np.pi * df['weekday'] / 7)
        df['weekday_cos'] = np.cos(2 * np.pi * df['weekday'] / 7)
        df['day_of_year_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
        df['day_of_year_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
        
        # Features booleanas
        df['is_weekend'] = (df['weekday'] >= 5).astype(int)
        df['is_month_start'] = (df['day'] <= 3).astype(int)
        df['is_month_end'] = (df['day'] >= 28).astype(int)
        
        logger.info(f"Added temporal features to dataset")
        
        return df

def process_dataset_without_date(dataset_id: str,
                                 df: pd.DataFrame,
                                 config: Dict,
                                 output_path: Path) -> pd.DataFrame:
    """
    Processar dataset sem coluna de data usando indexação temporal
    
    Args:
        dataset_id: ID do dataset
        df: DataFrame sem coluna de data
        config: Configuração do dataset
        output_path: Caminho para salvar resultado
    
    Returns:
        DataFrame processado com coluna de data
    """
    logger.info(f"Processing dataset without date: {dataset_id}")
    
    # Criar indexador temporal
    base_date = config.get('temporal_indexing', {}).get('base_date')
    frequency = config.get('temporal_indexing', {}).get('frequency', 'D')
    
    indexer = TemporalIndexer(base_date=base_date, frequency=frequency)
    
    # Estratégia baseada na configuração
    strategy = config.get('temporal_indexing', {}).get('strategy', 'order')
    
    if strategy == 'order':
        sort_by = config.get('temporal_indexing', {}).get('sort_by')
        df = indexer.create_index_from_order(df, sort_by=sort_by)
    
    elif strategy == 'pattern':
        group_by = config.get('temporal_indexing', {}).get('group_by')
        pattern_hint = config.get('temporal_indexing', {}).get('pattern_hint')
        df = indexer.create_index_from_patterns(df, group_by=group_by, pattern_hint=pattern_hint)
    
    elif strategy == 'external':
        external_path = config.get('temporal_indexing', {}).get('external_data_path')
        if external_path and Path(external_path).exists():
            external_data = pd.read_csv(external_path)
            join_cols = config.get('temporal_indexing', {}).get('join_cols', [])
            date_col_external = config.get('temporal_indexing', {}).get('date_col_external', 'date')
            df = indexer.create_index_from_external(df, external_data, join_cols, date_col_external)
        else:
            logger.warning("External data path not found, falling back to order strategy")
            df = indexer.create_index_from_order(df)
    
    # Adicionar features temporais
    add_features = config.get('temporal_indexing', {}).get('add_temporal_features', True)
    if add_features:
        df = indexer.enhance_with_temporal_features(df)
    
    # Salvar
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    logger.info(f"Processed dataset saved to: {output_path}")
    
    return df

