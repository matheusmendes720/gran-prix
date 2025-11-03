"""
Pipeline robusto para validação de qualidade de dados
Inclui checagens de integridade, completude, consistência e outliers
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class DataQualityValidator:
    """Validador completo de qualidade de dados"""
    
    def __init__(self, output_dir: str = 'data/processed/quality_reports'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_dataset(self, df: pd.DataFrame, dataset_id: str, 
                        config: Optional[Dict] = None) -> Dict:
        """
        Validar dataset completo e gerar relatório de qualidade
        
        Returns:
            Dict com resultados da validação e métricas de qualidade
        """
        logger.info(f"Validating dataset: {dataset_id}")
        
        validation_results = {
            'dataset_id': dataset_id,
            'validation_date': datetime.now().isoformat(),
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'checks': {}
        }
        
        # 1. Completude
        completeness = self._check_completeness(df)
        validation_results['checks']['completeness'] = completeness
        
        # 2. Integridade de tipos
        type_integrity = self._check_type_integrity(df, config)
        validation_results['checks']['type_integrity'] = type_integrity
        
        # 3. Consistência de valores
        value_consistency = self._check_value_consistency(df, config)
        validation_results['checks']['value_consistency'] = value_consistency
        
        # 4. Outliers
        outliers = self._check_outliers(df)
        validation_results['checks']['outliers'] = outliers
        
        # 5. Duplicatas
        duplicates = self._check_duplicates(df)
        validation_results['checks']['duplicates'] = duplicates
        
        # 6. Data range validation
        date_validation = self._check_date_range(df)
        validation_results['checks']['date_validation'] = date_validation
        
        # 7. Business rules
        business_rules = self._check_business_rules(df, config)
        validation_results['checks']['business_rules'] = business_rules
        
        # Calcular score geral de qualidade
        quality_score = self._calculate_quality_score(validation_results['checks'])
        validation_results['quality_score'] = quality_score
        
        # Gerar relatório
        self._save_quality_report(validation_results, dataset_id)
        
        logger.info(f"✓ Validation complete - Quality Score: {quality_score:.2%}")
        
        return validation_results
    
    def _check_completeness(self, df: pd.DataFrame) -> Dict:
        """Verificar completude dos dados"""
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        missing_percentage = (missing_cells / total_cells * 100) if total_cells > 0 else 0
        
        missing_by_column = df.isnull().sum().to_dict()
        missing_percentage_by_column = (df.isnull().sum() / len(df) * 100).to_dict()
        
        # Classificar severidade
        severity = 'low' if missing_percentage < 5 else 'medium' if missing_percentage < 20 else 'high'
        
        return {
            'total_cells': int(total_cells),
            'missing_cells': int(missing_cells),
            'missing_percentage': round(missing_percentage, 2),
            'missing_by_column': {k: int(v) for k, v in missing_by_column.items()},
            'missing_percentage_by_column': {k: round(v, 2) for k, v in missing_percentage_by_column.items()},
            'severity': severity,
            'status': 'pass' if missing_percentage < 10 else 'warning' if missing_percentage < 30 else 'fail'
        }
    
    def _check_type_integrity(self, df: pd.DataFrame, config: Optional[Dict] = None) -> Dict:
        """Verificar integridade de tipos de dados"""
        issues = []
        
        # Verificar colunas esperadas
        expected_columns = config.get('columns_mapping', {}).keys() if config else []
        
        for col in df.columns:
            col_type = str(df[col].dtype)
            
            # Verificar valores não numéricos em colunas numéricas
            if 'int' in col_type or 'float' in col_type:
                non_numeric = pd.to_numeric(df[col], errors='coerce').isna().sum()
                if non_numeric > 0:
                    issues.append({
                        'column': col,
                        'issue': f'{non_numeric} non-numeric values in numeric column',
                        'severity': 'high' if non_numeric > len(df) * 0.1 else 'medium'
                    })
            
            # Verificar datas inválidas em colunas de data
            if 'date' in col.lower() or 'time' in col.lower():
                if df[col].dtype == 'object':
                    try:
                        pd.to_datetime(df[col], errors='raise')
                    except:
                        invalid_dates = sum(pd.to_datetime(df[col], errors='coerce').isna())
                        if invalid_dates > 0:
                            issues.append({
                                'column': col,
                                'issue': f'{invalid_dates} invalid date values',
                                'severity': 'high' if invalid_dates > len(df) * 0.1 else 'medium'
                            })
        
        return {
            'issues': issues,
            'issue_count': len(issues),
            'status': 'pass' if len(issues) == 0 else 'warning' if len(issues) < 5 else 'fail'
        }
    
    def _check_value_consistency(self, df: pd.DataFrame, config: Optional[Dict] = None) -> Dict:
        """Verificar consistência de valores"""
        issues = []
        
        # Verificar valores negativos em colunas que não devem ter negativos
        positive_columns = ['quantity', 'cost', 'price', 'demand', 'temperature', 'precipitation', 'humidity']
        for col in df.columns:
            if any(pos in col.lower() for pos in positive_columns):
                negatives = (df[col] < 0).sum()
                if negatives > 0:
                    issues.append({
                        'column': col,
                        'issue': f'{negatives} negative values found',
                        'severity': 'medium'
                    })
        
        # Verificar valores zero excessivos
        zero_columns = ['quantity', 'demand']
        for col in df.columns:
            if any(zero in col.lower() for zero in zero_columns):
                zeros = (df[col] == 0).sum()
                zero_percentage = zeros / len(df) * 100
                if zero_percentage > 50:
                    issues.append({
                        'column': col,
                        'issue': f'{zero_percentage:.1f}% zero values (high percentage)',
                        'severity': 'low'
                    })
        
        return {
            'issues': issues,
            'issue_count': len(issues),
            'status': 'pass' if len(issues) == 0 else 'warning'
        }
    
    def _check_outliers(self, df: pd.DataFrame) -> Dict:
        """Verificar outliers usando IQR method"""
        outliers_by_column = {}
        total_outliers = 0
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            if IQR > 0:
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                outlier_count = len(outliers)
                
                if outlier_count > 0:
                    outliers_by_column[col] = {
                        'count': outlier_count,
                        'percentage': round(outlier_count / len(df) * 100, 2),
                        'lower_bound': round(lower_bound, 2),
                        'upper_bound': round(upper_bound, 2)
                    }
                    total_outliers += outlier_count
        
        severity = 'low' if total_outliers < len(df) * 0.05 else 'medium' if total_outliers < len(df) * 0.15 else 'high'
        
        return {
            'outliers_by_column': outliers_by_column,
            'total_outliers': total_outliers,
            'total_outlier_percentage': round(total_outliers / (len(df) * len(numeric_columns)) * 100, 2) if numeric_columns.size > 0 else 0,
            'severity': severity,
            'status': 'pass' if total_outliers < len(df) * 0.1 else 'warning' if total_outliers < len(df) * 0.2 else 'fail'
        }
    
    def _check_duplicates(self, df: pd.DataFrame) -> Dict:
        """Verificar duplicatas"""
        duplicate_rows = df.duplicated().sum()
        duplicate_percentage = duplicate_rows / len(df) * 100 if len(df) > 0 else 0
        
        # Verificar duplicatas em chaves primárias esperadas
        key_columns = ['date', 'item_id']
        present_key_columns = [col for col in key_columns if col in df.columns]
        
        key_duplicates = 0
        if present_key_columns:
            key_duplicates = df.duplicated(subset=present_key_columns).sum()
        
        severity = 'high' if key_duplicates > 0 else 'low' if duplicate_rows < len(df) * 0.05 else 'medium'
        
        return {
            'total_duplicates': int(duplicate_rows),
            'duplicate_percentage': round(duplicate_percentage, 2),
            'key_duplicates': int(key_duplicates),
            'severity': severity,
            'status': 'pass' if duplicate_rows == 0 and key_duplicates == 0 else 'warning' if duplicate_rows < len(df) * 0.05 else 'fail'
        }
    
    def _check_date_range(self, df: pd.DataFrame) -> Dict:
        """Verificar range de datas"""
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        
        if not date_columns:
            return {
                'status': 'warning',
                'message': 'No date columns found'
            }
        
        issues = []
        date_ranges = {}
        
        for col in date_columns:
            try:
                dates = pd.to_datetime(df[col], errors='coerce')
                valid_dates = dates.dropna()
                
                if len(valid_dates) > 0:
                    min_date = valid_dates.min()
                    max_date = valid_dates.max()
                    date_range_days = (max_date - min_date).days
                    
                    date_ranges[col] = {
                        'min': min_date.isoformat(),
                        'max': max_date.isoformat(),
                        'range_days': date_range_days,
                        'valid_dates': len(valid_dates),
                        'total_rows': len(df)
                    }
                    
                    # Verificar datas futuras (provavelmente inválidas)
                    today = pd.Timestamp.now()
                    future_dates = (valid_dates > today).sum()
                    if future_dates > 0:
                        issues.append({
                            'column': col,
                            'issue': f'{future_dates} future dates found',
                            'severity': 'medium'
                        })
                    
                    # Verificar datas muito antigas (antes de 1900)
                    old_dates = (valid_dates < pd.Timestamp('1900-01-01')).sum()
                    if old_dates > 0:
                        issues.append({
                            'column': col,
                            'issue': f'{old_dates} dates before 1900',
                            'severity': 'low'
                        })
            except Exception as e:
                issues.append({
                    'column': col,
                    'issue': f'Error processing dates: {str(e)}',
                    'severity': 'high'
                })
        
        return {
            'date_ranges': date_ranges,
            'issues': issues,
            'issue_count': len(issues),
            'status': 'pass' if len(issues) == 0 else 'warning' if len(issues) < 3 else 'fail'
        }
    
    def _check_business_rules(self, df: pd.DataFrame, config: Optional[Dict] = None) -> Dict:
        """Verificar regras de negócio"""
        issues = []
        
        # Regra: Quantidade deve ser positiva
        if 'quantity' in df.columns:
            negative_quantity = (df['quantity'] < 0).sum()
            if negative_quantity > 0:
                issues.append({
                    'rule': 'quantity_positive',
                    'issue': f'{negative_quantity} negative quantities',
                    'severity': 'high'
                })
        
        # Regra: Temperatura em range razoável (-50 a 60°C)
        if 'temperature' in df.columns:
            extreme_temp = ((df['temperature'] < -50) | (df['temperature'] > 60)).sum()
            if extreme_temp > 0:
                issues.append({
                    'rule': 'temperature_range',
                    'issue': f'{extreme_temp} temperatures outside reasonable range (-50 to 60°C)',
                    'severity': 'medium'
                })
        
        # Regra: Precipitação não pode ser negativa
        if 'precipitation' in df.columns:
            negative_precip = (df['precipitation'] < 0).sum()
            if negative_precip > 0:
                issues.append({
                    'rule': 'precipitation_positive',
                    'issue': f'{negative_precip} negative precipitation values',
                    'severity': 'high'
                })
        
        return {
            'issues': issues,
            'issue_count': len(issues),
            'status': 'pass' if len(issues) == 0 else 'warning' if len(issues) < 3 else 'fail'
        }
    
    def _calculate_quality_score(self, checks: Dict) -> float:
        """Calcular score geral de qualidade (0-1)"""
        weights = {
            'completeness': 0.25,
            'type_integrity': 0.20,
            'value_consistency': 0.15,
            'outliers': 0.15,
            'duplicates': 0.15,
            'date_validation': 0.05,
            'business_rules': 0.05
        }
        
        scores = {}
        for check_name, check_data in checks.items():
            if check_name in weights:
                status = check_data.get('status', 'fail')
                if status == 'pass':
                    scores[check_name] = 1.0
                elif status == 'warning':
                    scores[check_name] = 0.7
                else:  # fail
                    scores[check_name] = 0.3
        
        # Calcular weighted average
        total_score = sum(scores.get(name, 0.5) * weights[name] for name in weights.keys())
        
        return total_score
    
    def _save_quality_report(self, results: Dict, dataset_id: str) -> Path:
        """Salvar relatório de qualidade"""
        report_path = self.output_dir / f"{dataset_id}_quality_report.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✓ Quality report saved: {report_path}")
        
        return report_path

