"""
Comprehensive Data Quality Validation
- Missing values analysis
- Outliers detection
- Data distribution analysis
- Feature importance analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).parent.parent.parent
TRAIN_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_train.csv"
VAL_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_validation.csv"
TEST_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_test.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "nova_corrente"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_datasets():
    """Load train/validation/test datasets"""
    print("=" * 80)
    print("CARREGANDO DATASETS PARA VALIDAÇÃO")
    print("=" * 80)
    
    train_df = pd.read_csv(TRAIN_FILE, parse_dates=['date'])
    val_df = pd.read_csv(VAL_FILE, parse_dates=['date'])
    test_df = pd.read_csv(TEST_FILE, parse_dates=['date'])
    
    print(f"\n[INFO] Train: {len(train_df):,} registros")
    print(f"[INFO] Validation: {len(val_df):,} registros")
    print(f"[INFO] Test: {len(test_df):,} registros")
    
    return train_df, val_df, test_df

def analyze_missing_values(df, dataset_name):
    """Analyze missing values"""
    print(f"\n[ANALYSIS] Missing Values - {dataset_name}")
    
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    
    missing_df = pd.DataFrame({
        'column': missing.index,
        'missing_count': missing.values,
        'missing_pct': missing_pct.values
    }).sort_values('missing_pct', ascending=False)
    
    missing_df = missing_df[missing_df['missing_count'] > 0]
    
    if len(missing_df) > 0:
        print(f"\n  Colunas com missing values: {len(missing_df)}")
        print(missing_df.head(10).to_string(index=False))
    else:
        print("\n  ✅ Nenhum missing value encontrado!")
    
    return missing_df.to_dict('records')

def detect_outliers(df, numeric_cols):
    """Detect outliers using IQR method"""
    print(f"\n[ANALYSIS] Outliers Detection")
    
    outliers_summary = {}
    
    for col in numeric_cols:
        if col not in df.columns:
            continue
        
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_count = len(outliers)
        outlier_pct = (outlier_count / len(df) * 100) if len(df) > 0 else 0
        
        outliers_summary[col] = {
            'count': int(outlier_count),
            'percentage': float(outlier_pct),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound)
        }
        
        if outlier_count > 0:
            print(f"\n  {col}:")
            print(f"    Outliers: {outlier_count:,} ({outlier_pct:.2f}%)")
            print(f"    Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    return outliers_summary

def analyze_distributions(df, numeric_cols):
    """Analyze data distributions"""
    print(f"\n[ANALYSIS] Data Distributions")
    
    distributions = {}
    
    for col in numeric_cols:
        if col not in df.columns:
            continue
        
        distributions[col] = {
            'mean': float(df[col].mean()) if not df[col].isna().all() else None,
            'median': float(df[col].median()) if not df[col].isna().all() else None,
            'std': float(df[col].std()) if not df[col].isna().all() else None,
            'min': float(df[col].min()) if not df[col].isna().all() else None,
            'max': float(df[col].max()) if not df[col].isna().all() else None,
            'skewness': float(df[col].skew()) if not df[col].isna().all() else None,
            'kurtosis': float(df[col].kurtosis()) if not df[col].isna().all() else None
        }
    
    print(f"\n  Estatísticas calculadas para {len(distributions)} colunas numéricas")
    
    return distributions

def analyze_by_family(df):
    """Analyze data by family"""
    print(f"\n[ANALYSIS] Analysis by Family")
    
    if 'familia' not in df.columns:
        return {}
    
    family_stats = df.groupby('familia').agg({
        'quantidade': ['count', 'mean', 'std', 'min', 'max'],
        'lead_time_days': ['mean', 'std', 'min', 'max'],
        'item_id': 'nunique',
        'site_id': 'nunique'
    }).round(2)
    
    family_stats.columns = ['records', 'qty_mean', 'qty_std', 'qty_min', 'qty_max',
                           'lt_mean', 'lt_std', 'lt_min', 'lt_max',
                           'items_unique', 'sites_unique']
    
    print(f"\n  Estatísticas por família:")
    print(family_stats.to_string())
    
    return family_stats.to_dict('index')

def validate_data_quality(df, dataset_name):
    """Comprehensive data quality validation"""
    print("\n" + "=" * 80)
    print(f"VALIDAÇÃO DE QUALIDADE: {dataset_name}")
    print("=" * 80)
    
    # Basic info
    info = {
        'dataset_name': dataset_name,
        'total_records': len(df),
        'total_features': len(df.columns),
        'date_range': {
            'min': str(df['date'].min()) if 'date' in df.columns else None,
            'max': str(df['date'].max()) if 'date' in df.columns else None
        }
    }
    
    # Missing values
    missing = analyze_missing_values(df, dataset_name)
    
    # Numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'target' in numeric_cols:
        numeric_cols.remove('target')
    
    # Outliers
    outliers = detect_outliers(df, numeric_cols[:10])  # Top 10 numeric columns
    
    # Distributions
    distributions = analyze_distributions(df, numeric_cols[:10])
    
    # Family analysis
    family_stats = analyze_by_family(df) if 'familia' in df.columns else {}
    
    return {
        'info': info,
        'missing_values': missing,
        'outliers': outliers,
        'distributions': distributions,
        'family_stats': family_stats
    }

def save_validation_report(train_validation, val_validation, test_validation):
    """Save comprehensive validation report"""
    print("\n" + "=" * 80)
    print("SALVANDO RELATÓRIO DE VALIDAÇÃO")
    print("=" * 80)
    
    report = {
        'validation_date': datetime.now().isoformat(),
        'train': train_validation,
        'validation': val_validation,
        'test': test_validation,
        'summary': {
            'total_datasets': 3,
            'total_records': (
                train_validation['info']['total_records'] +
                val_validation['info']['total_records'] +
                test_validation['info']['total_records']
            ),
            'data_quality_score': calculate_quality_score(train_validation, val_validation, test_validation)
        }
    }
    
    report_file = OUTPUT_DIR / "data_quality_validation_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n[SUCCESS] Relatório salvo: {report_file}")
    
    # Create summary text report
    summary_file = OUTPUT_DIR / "data_quality_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO DE VALIDAÇÃO DE QUALIDADE DOS DADOS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("RESUMO GERAL\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total de registros: {report['summary']['total_records']:,}\n")
        f.write(f"Score de qualidade: {report['summary']['data_quality_score']:.1f}%\n\n")
        
        f.write("TRAIN SET\n")
        f.write("-" * 80 + "\n")
        f.write(f"Registros: {train_validation['info']['total_records']:,}\n")
        f.write(f"Features: {train_validation['info']['total_features']}\n")
        f.write(f"Missing values: {len(train_validation['missing_values'])} colunas\n")
        f.write(f"Outliers: {len(train_validation['outliers'])} colunas\n\n")
        
        f.write("VALIDATION SET\n")
        f.write("-" * 80 + "\n")
        f.write(f"Registros: {val_validation['info']['total_records']:,}\n")
        f.write(f"Features: {val_validation['info']['total_features']}\n\n")
        
        f.write("TEST SET\n")
        f.write("-" * 80 + "\n")
        f.write(f"Registros: {test_validation['info']['total_records']:,}\n")
        f.write(f"Features: {test_validation['info']['total_features']}\n")
    
    print(f"[SUCCESS] Resumo texto: {summary_file}")
    
    return report

def calculate_quality_score(train_val, val_val, test_val):
    """Calculate overall data quality score"""
    score = 100.0
    
    # Penalize for missing values
    total_missing_cols = len(train_val['missing_values']) + len(val_val['missing_values']) + len(test_val['missing_values'])
    score -= min(total_missing_cols * 2, 20)  # Max 20 points penalty
    
    # Penalize for outliers
    total_outlier_cols = len(train_val['outliers']) + len(val_val['outliers']) + len(test_val['outliers'])
    score -= min(total_outlier_cols * 1, 10)  # Max 10 points penalty
    
    return max(score, 0)

def main():
    """Main validation pipeline"""
    print("\n" + "=" * 80)
    print("PIPELINE DE VALIDAÇÃO DE QUALIDADE")
    print("=" * 80 + "\n")
    
    # Step 1: Load datasets
    train_df, val_df, test_df = load_datasets()
    
    # Step 2: Validate train set
    train_validation = validate_data_quality(train_df, "TRAIN")
    
    # Step 3: Validate validation set
    val_validation = validate_data_quality(val_df, "VALIDATION")
    
    # Step 4: Validate test set
    test_validation = validate_data_quality(test_df, "TEST")
    
    # Step 5: Save report
    report = save_validation_report(train_validation, val_validation, test_validation)
    
    print("\n" + "=" * 80)
    print("VALIDAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"\n[RESUMO]")
    print(f"  - Total registros validados: {report['summary']['total_records']:,}")
    print(f"  - Score de qualidade: {report['summary']['data_quality_score']:.1f}%")
    print(f"\n[PRÓXIMOS PASSOS]")
    print(f"  1. Treinar modelos baseline")
    print(f"  2. Avaliar performance")
    print(f"  3. Otimizar features")
    
    return report

if __name__ == "__main__":
    main()

