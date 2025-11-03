"""
Static Analysis: Business Requirements vs Feature Engineering
Compare Nova Corrente dadosSuprimentos.xlsx with requirements and training data
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
NOVA_CORRENTE_FILE = PROJECT_ROOT / "docs" / "proj" / "dadosSuprimentos.xlsx"
TRAINING_DATA = PROJECT_ROOT / "data" / "training"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

def analyze_nova_corrente_excel():
    """Analyze the Nova Corrente Excel file"""
    print("=" * 80)
    print("ANÁLISE DO ARQUIVO NOVA CORRENTE: dadosSuprimentos.xlsx")
    print("=" * 80)
    
    try:
        # Read Excel file
        df = pd.read_excel(NOVA_CORRENTE_FILE, sheet_name=None)
        
        analysis = {
            'file_exists': True,
            'sheets': list(df.keys()),
            'analysis': {}
        }
        
        for sheet_name, sheet_df in df.items():
            print(f"\n[Sheet] {sheet_name}")
            print(f"   Shape: {sheet_df.shape}")
            print(f"   Columns: {list(sheet_df.columns)}")
            print(f"   Data types:\n{sheet_df.dtypes}")
            print(f"\n   First 5 rows:")
            print(sheet_df.head().to_string())
            print(f"\n   Summary statistics:")
            print(sheet_df.describe().to_string())
            print(f"\n   Missing values:")
            print(sheet_df.isnull().sum().to_string())
            print(f"\n   Unique values per column:")
            for col in sheet_df.columns:
                unique_count = sheet_df[col].nunique()
                print(f"      {col}: {unique_count} unique")
                if unique_count <= 20:
                    print(f"         Values: {list(sheet_df[col].unique()[:20])}")
            
            analysis['analysis'][sheet_name] = {
                'shape': sheet_df.shape,
                'columns': list(sheet_df.columns),
                'dtypes': {col: str(dtype) for col, dtype in sheet_df.dtypes.items()},
                'missing_values': sheet_df.isnull().sum().to_dict(),
                'unique_counts': {col: int(sheet_df[col].nunique()) for col in sheet_df.columns},
                'summary_stats': sheet_df.describe().to_dict(),
                'sample_data': sheet_df.head(10).to_dict('records')
            }
        
        return analysis, df
        
    except Exception as e:
        print(f"[ERROR] Error reading Excel file: {e}")
        return {'file_exists': False, 'error': str(e)}, None

def load_training_data_summary():
    """Load summary of training data"""
    training_summary_file = TRAINING_DATA / "training_summary.json"
    
    if training_summary_file.exists():
        with open(training_summary_file, 'r') as f:
            return json.load(f)
    return None

def load_processed_datasets():
    """Analyze processed datasets"""
    datasets = {}
    
    key_files = [
        "unified_dataset_with_factors.csv",
        "unified_brazilian_telecom_nova_corrente_enriched.csv",
        "unified_comprehensive_ml_ready.csv"
    ]
    
    for filename in key_files:
        filepath = PROCESSED_DATA / filename
        if filepath.exists():
            try:
                df = pd.read_csv(filepath, nrows=1000)  # Sample for analysis
                datasets[filename] = {
                    'shape_sample': df.shape,
                    'columns': list(df.columns),
                    'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                    'sample': df.head(5).to_dict('records')
                }
            except Exception as e:
                datasets[filename] = {'error': str(e)}
    
    return datasets

def compare_requirements_vs_data(business_reqs, nova_corrente_data, training_data, processed_datasets):
    """Compare business requirements with available data"""
    
    comparison = {
        'business_requirements': {
            'needed_features': [
                'Histórico de consumo semanal/mensal por item',
                'Datas/feriados',
                'Tempo médio de entrega (lead time)',
                'Sazonalidades',
                'Fatores climáticos',
                'Fatores econômicos',
                'Fatores tecnológicos (5G)'
            ],
            'outputs_required': [
                'Projeção para próximos 30 dias por item',
                'Erro médio da previsão (MAPE)',
                'Recomendação de compra',
                'Alertas de ruptura'
            ],
            'minimum_items': 5
        },
        'data_availability': {},
        'gaps': [],
        'opportunities': []
    }
    
    # Analyze Nova Corrente data
    if nova_corrente_data:
        for sheet_name, sheet_df in nova_corrente_data.items():
            columns = list(sheet_df.columns)
            
            # Check for key features
            has_date = any('data' in col.lower() or 'date' in col.lower() for col in columns)
            has_item = any('item' in col.lower() or 'produto' in col.lower() or 'suprimento' in col.lower() for col in columns)
            has_quantity = any('quantidade' in col.lower() or 'qtd' in col.lower() or 'quantity' in col.lower() for col in columns)
            has_leadtime = any('lead' in col.lower() or 'prazo' in col.lower() or 'entrega' in col.lower() for col in columns)
            
            comparison['data_availability'][f'nova_corrente_{sheet_name}'] = {
                'has_date': has_date,
                'has_item': has_item,
                'has_quantity': has_quantity,
                'has_leadtime': has_leadtime,
                'columns': columns,
                'rows': len(sheet_df),
                'date_range': None
            }
            
            # Check for date column
            if has_date:
                date_col = [col for col in columns if 'data' in col.lower() or 'date' in col.lower()][0]
                try:
                    dates = pd.to_datetime(sheet_df[date_col], errors='coerce')
                    valid_dates = dates.dropna()
                    if len(valid_dates) > 0:
                        comparison['data_availability'][f'nova_corrente_{sheet_name}']['date_range'] = {
                            'min': str(valid_dates.min()),
                            'max': str(valid_dates.max()),
                            'span_days': (valid_dates.max() - valid_dates.min()).days
                        }
                except:
                    pass
    
    # Analyze training data
    if training_data:
        comparison['data_availability']['training_data'] = {
            'total_items': training_data.get('total_items', 0),
            'items_statistics': training_data.get('items_statistics', {})
        }
    
    # Analyze processed datasets
    comparison['data_availability']['processed_datasets'] = {}
    for name, info in processed_datasets.items():
        if 'columns' in info:
            comparison['data_availability']['processed_datasets'][name] = {
                'columns_count': len(info['columns']),
                'columns_sample': info['columns'][:20],
                'has_external_factors': any(
                    'weather' in col.lower() or 'climate' in col.lower() or 
                    'economic' in col.lower() or '5g' in col.lower()
                    for col in info['columns']
                )
            }
    
    # Identify gaps
    gaps = []
    if not comparison['data_availability'].get('nova_corrente_data'):
        gaps.append("Nova Corrente dadosSuprimentos.xlsx não encontrado ou não pode ser lido")
    
    # Identify opportunities
    opportunities = []
    if comparison['data_availability'].get('processed_datasets'):
        opportunities.append("Datasets processados já contêm features externas (clima, economia, 5G)")
        opportunities.append("Pode combinar dados Nova Corrente com datasets enriquecidos existentes")
    
    comparison['gaps'] = gaps
    comparison['opportunities'] = opportunities
    
    return comparison

def main():
    """Main analysis function"""
    print("\n" + "="*80)
    print("ANÁLISE ESTÁTICA: BUSINESS REQUIREMENTS vs FEATURE ENGINEERING")
    print("Nova Corrente Grand Prix SENAI - Demand Forecasting System")
    print("="*80 + "\n")
    
    # 1. Analyze Nova Corrente Excel
    nova_corrente_analysis, nova_corrente_data = analyze_nova_corrente_excel()
    
    # 2. Load training data summary
    training_summary = load_training_data_summary()
    if training_summary:
        print("\n" + "="*80)
        print("TRAINING DATA SUMMARY")
        print("="*80)
        print(json.dumps(training_summary, indent=2, default=str))
    
    # 3. Load processed datasets
    processed_datasets = load_processed_datasets()
    
    # 4. Compare requirements vs data
    business_reqs = {
        'needed_features': [
            'Histórico de consumo semanal/mensal por item',
            'Datas/feriados',
            'Tempo médio de entrega (lead time)',
            'Sazonalidades'
        ]
    }
    
    comparison = compare_requirements_vs_data(
        business_reqs,
        nova_corrente_data,
        training_summary,
        processed_datasets
    )
    
    # 5. Save results
    output_file = PROJECT_ROOT / "docs" / "proj" / "strategy" / "STATIC_ANALYSIS_REQUIREMENTS_VS_DATA.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    results = {
        'analysis_date': datetime.now().isoformat(),
        'nova_corrente_analysis': nova_corrente_analysis,
        'training_data_summary': training_summary,
        'processed_datasets': processed_datasets,
        'comparison': comparison
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("COMPARAÇÃO: REQUIREMENTS vs DATA")
    print("="*80)
    print(json.dumps(comparison, indent=2, default=str, ensure_ascii=False))
    
    print(f"\n[SUCCESS] Analysis saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    main()

