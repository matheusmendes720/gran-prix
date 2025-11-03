"""
Pipeline para análise estatística e geração de insights automáticos
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional, List
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Analisador de dados com estatísticas e insights automáticos"""
    
    def __init__(self, output_dir: str = 'data/processed/analysis_reports'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_dataset(self, df: pd.DataFrame, dataset_id: str, 
                       target_column: Optional[str] = None) -> Dict:
        """
        Análise completa do dataset com estatísticas e insights
        
        Args:
            df: DataFrame para análise
            dataset_id: ID do dataset
            target_column: Coluna alvo (se houver)
        
        Returns:
            Dict com análises completas
        """
        logger.info(f"Analyzing dataset: {dataset_id}")
        
        analysis = {
            'dataset_id': dataset_id,
            'analysis_date': datetime.now().isoformat(),
            'basic_stats': self._basic_statistics(df),
            'temporal_analysis': self._temporal_analysis(df) if 'date' in df.columns else None,
            'target_analysis': self._target_analysis(df, target_column) if target_column else None,
            'correlation_analysis': self._correlation_analysis(df),
            'distribution_analysis': self._distribution_analysis(df),
            'insights': []
        }
        
        # Gerar insights automáticos
        analysis['insights'] = self._generate_insights(analysis)
        
        # Salvar análise
        self._save_analysis(analysis, dataset_id)
        
        logger.info(f"✓ Analysis complete - {len(analysis['insights'])} insights generated")
        
        return analysis
    
    def _basic_statistics(self, df: pd.DataFrame) -> Dict:
        """Estatísticas básicas"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        stats = {
            'shape': {
                'rows': len(df),
                'columns': len(df.columns)
            },
            'numeric_columns': {},
            'categorical_columns': {}
        }
        
        # Estatísticas numéricas
        for col in numeric_cols:
            stats['numeric_columns'][col] = {
                'mean': float(df[col].mean()) if not df[col].empty else None,
                'median': float(df[col].median()) if not df[col].empty else None,
                'std': float(df[col].std()) if not df[col].empty else None,
                'min': float(df[col].min()) if not df[col].empty else None,
                'max': float(df[col].max()) if not df[col].empty else None,
                'q25': float(df[col].quantile(0.25)) if not df[col].empty else None,
                'q75': float(df[col].quantile(0.75)) if not df[col].empty else None,
                'missing': int(df[col].isna().sum()),
                'missing_pct': float(df[col].isna().sum() / len(df) * 100)
            }
        
        # Estatísticas categóricas
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols[:10]:  # Limitar a 10 para não ficar muito grande
            value_counts = df[col].value_counts()
            stats['categorical_columns'][col] = {
                'unique_values': int(df[col].nunique()),
                'most_frequent': value_counts.index[0] if len(value_counts) > 0 else None,
                'most_frequent_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else None,
                'missing': int(df[col].isna().sum()),
                'missing_pct': float(df[col].isna().sum() / len(df) * 100)
            }
        
        return stats
    
    def _temporal_analysis(self, df: pd.DataFrame) -> Optional[Dict]:
        """Análise temporal se houver coluna de data"""
        if 'date' not in df.columns:
            return None
        
        try:
            dates = pd.to_datetime(df['date'], errors='coerce')
            valid_dates = dates.dropna()
            
            if len(valid_dates) == 0:
                return None
            
            temporal = {
                'date_range': {
                    'start': valid_dates.min().isoformat(),
                    'end': valid_dates.max().isoformat(),
                    'days': int((valid_dates.max() - valid_dates.min()).days)
                },
                'temporal_coverage': {
                    'years': round((valid_dates.max() - valid_dates.min()).days / 365.25, 2),
                    'months': round((valid_dates.max() - valid_dates.min()).days / 30, 2)
                },
                'granularity': self._detect_granularity(dates),
                'seasonality_detected': self._detect_seasonality(df, dates) if len(valid_dates) > 30 else False
            }
            
            return temporal
        except Exception as e:
            logger.warning(f"Failed temporal analysis: {e}")
            return None
    
    def _detect_granularity(self, dates: pd.Series) -> str:
        """Detectar granularidade temporal"""
        valid_dates = dates.dropna()
        if len(valid_dates) < 2:
            return 'unknown'
        
        # Calcular diferenças médias
        diffs = valid_dates.sort_values().diff().dropna()
        mean_diff = diffs.mean()
        
        if mean_diff < pd.Timedelta(hours=2):
            return 'hourly'
        elif mean_diff < pd.Timedelta(days=2):
            return 'daily'
        elif mean_diff < pd.Timedelta(days=8):
            return 'weekly'
        elif mean_diff < pd.Timedelta(days=35):
            return 'monthly'
        else:
            return 'yearly'
    
    def _detect_seasonality(self, df: pd.DataFrame, dates: pd.Series) -> bool:
        """Detectar sazonalidade básica"""
        # Implementação simples - verificar se há padrão mensal
        try:
            df_with_dates = df.copy()
            df_with_dates['date'] = dates
            df_with_dates['month'] = df_with_dates['date'].dt.month
            
            if 'quantity' in df_with_dates.columns:
                monthly_mean = df_with_dates.groupby('month')['quantity'].mean()
                # Sazonalidade se variância entre meses > 10%
                if monthly_mean.std() / monthly_mean.mean() > 0.1:
                    return True
        except:
            pass
        
        return False
    
    def _target_analysis(self, df: pd.DataFrame, target_column: str) -> Optional[Dict]:
        """Análise da variável alvo"""
        if target_column not in df.columns:
            return None
        
        target = df[target_column]
        
        analysis = {
            'column': target_column,
            'type': 'numeric' if pd.api.types.is_numeric_dtype(target) else 'categorical',
            'missing': int(target.isna().sum()),
            'missing_pct': float(target.isna().sum() / len(df) * 100)
        }
        
        if pd.api.types.is_numeric_dtype(target):
            analysis['statistics'] = {
                'mean': float(target.mean()) if not target.empty else None,
                'median': float(target.median()) if not target.empty else None,
                'std': float(target.std()) if not target.empty else None,
                'min': float(target.min()) if not target.empty else None,
                'max': float(target.max()) if not target.empty else None,
                'cv': float(target.std() / target.mean()) if target.mean() != 0 else None  # Coefficient of variation
            }
            
            # Classificar variabilidade
            cv = analysis['statistics']['cv']
            if cv:
                if cv < 0.2:
                    analysis['variability'] = 'low'
                elif cv < 0.5:
                    analysis['variability'] = 'medium'
                else:
                    analysis['variability'] = 'high'
        
        return analysis
    
    def _correlation_analysis(self, df: pd.DataFrame) -> Dict:
        """Análise de correlação"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return {'message': 'Not enough numeric columns for correlation'}
        
        corr_matrix = numeric_df.corr()
        
        # Encontrar correlações fortes (>0.7 ou <-0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'column1': corr_matrix.columns[i],
                        'column2': corr_matrix.columns[j],
                        'correlation': float(corr_value)
                    })
        
        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'strong_correlations': strong_correlations[:10],  # Limitar a 10
            'high_correlation_count': len(strong_correlations)
        }
    
    def _distribution_analysis(self, df: pd.DataFrame) -> Dict:
        """Análise de distribuições"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        distributions = {}
        
        for col in numeric_cols[:10]:  # Limitar a 10 colunas
            values = df[col].dropna()
            if len(values) > 0:
                # Teste básico de normalidade (skewness)
                skewness = float(values.skew())
                
                distributions[col] = {
                    'skewness': skewness,
                    'distribution_type': 'normal' if abs(skewness) < 0.5 else 'skewed_right' if skewness > 0.5 else 'skewed_left',
                    'has_outliers': (abs(skewness) > 2)
                }
        
        return distributions
    
    def _generate_insights(self, analysis: Dict) -> List[str]:
        """Gerar insights automáticos baseados na análise"""
        insights = []
        
        # Insight 1: Tamanho do dataset
        shape = analysis['basic_stats']['shape']
        if shape['rows'] < 1000:
            insights.append(f"⚠️ Small dataset: {shape['rows']} rows - may limit model generalization")
        elif shape['rows'] > 100000:
            insights.append(f"✅ Large dataset: {shape['rows']} rows - excellent for training robust models")
        
        # Insight 2: Dados faltantes
        for col, stats in analysis['basic_stats'].get('numeric_columns', {}).items():
            missing_pct = stats.get('missing_pct', 0)
            if missing_pct > 20:
                insights.append(f"⚠️ High missing data in {col}: {missing_pct:.1f}% - consider imputation")
        
        # Insight 3: Sazonalidade
        if analysis.get('temporal_analysis') and analysis['temporal_analysis'].get('seasonality_detected'):
            insights.append("✅ Seasonality detected - time-series models (SARIMA, Prophet) recommended")
        
        # Insight 4: Correlações fortes
        strong_corr_count = analysis['correlation_analysis'].get('high_correlation_count', 0)
        if strong_corr_count > 5:
            insights.append(f"⚠️ {strong_corr_count} strong correlations detected - check for multicollinearity")
        
        # Insight 5: Variabilidade do target
        if analysis.get('target_analysis'):
            target_var = analysis['target_analysis'].get('variability')
            if target_var == 'high':
                insights.append("⚠️ High target variability - consider log transformation or robust models")
        
        return insights
    
    def _save_analysis(self, analysis: Dict, dataset_id: str) -> Path:
        """Salvar análise"""
        report_path = self.output_dir / f"{dataset_id}_analysis.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✓ Analysis report saved: {report_path}")
        
        return report_path

