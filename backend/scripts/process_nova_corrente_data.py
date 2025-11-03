"""
Process Nova Corrente dadosSuprimentos.xlsx
- Clean and structure data
- Calculate lead times
- Identify top families
- Prepare for feature engineering
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
NOVA_CORRENTE_FILE = PROJECT_ROOT / "docs" / "proj" / "dadosSuprimentos.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "nova_corrente"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_nova_corrente_data():
    """Load and clean Nova Corrente Excel file"""
    print("=" * 80)
    print("PROCESSANDO DADOS NOVA CORRENTE")
    print("=" * 80)
    
    # Read main sheet
    df = pd.read_excel(NOVA_CORRENTE_FILE, sheet_name="CUSTO DE MATERIAL E SERVIÇOS")
    
    print(f"\n[INFO] Dados carregados: {len(df)} registros")
    print(f"[INFO] Colunas: {list(df.columns)}")
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Rename for consistency
    rename_map = {
        'DEPÓSITO': 'deposito',
        'PRODUTO/SERVIÇO': 'produto_servico',
        'MATERIAL': 'material',
        'FAMÍLIA': 'familia',
        'NOME FORNEC.': 'fornecedor',
        'QUANTIDADE': 'quantidade',
        'U.M.': 'unidade_medida',
        'DATA REQUISITADA': 'data_requisitada',
        'SOLICITAÇÃO': 'solicitacao',
        'DATA SOLICITADO': 'data_solicitado',
        'DATA DE COMPRA': 'data_compra'
    }
    
    df = df.rename(columns=rename_map)
    
    # Ensure date columns are datetime
    for date_col in ['data_requisitada', 'data_solicitado', 'data_compra']:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    print(f"\n[INFO] Dados limpos: {len(df)} registros")
    print(f"[INFO] Datas válidas:")
    print(f"  - data_requisitada: {df['data_requisitada'].notna().sum()}/{len(df)}")
    print(f"  - data_solicitado: {df['data_solicitado'].notna().sum()}/{len(df)}")
    print(f"  - data_compra: {df['data_compra'].notna().sum()}/{len(df)}")
    
    return df

def calculate_lead_times(df):
    """Calculate lead times from dates"""
    print("\n" + "=" * 80)
    print("CALCULANDO LEAD TIMES")
    print("=" * 80)
    
    # Calculate lead time (data_compra - data_solicitado)
    mask = df['data_solicitado'].notna() & df['data_compra'].notna()
    df.loc[mask, 'lead_time_days'] = (
        df.loc[mask, 'data_compra'] - df.loc[mask, 'data_solicitado']
    ).dt.days
    
    # Only keep positive lead times (handle edge cases)
    df.loc[df['lead_time_days'] < 0, 'lead_time_days'] = np.nan
    
    # Statistics
    valid_lead_times = df['lead_time_days'].dropna()
    
    print(f"\n[INFO] Lead times calculados: {len(valid_lead_times)}/{len(df)}")
    if len(valid_lead_times) > 0:
        print(f"[INFO] Estatísticas:")
        print(f"  - Média: {valid_lead_times.mean():.2f} dias")
        print(f"  - Mediana: {valid_lead_times.median():.2f} dias")
        print(f"  - Min: {valid_lead_times.min():.0f} dias")
        print(f"  - Max: {valid_lead_times.max():.0f} dias")
        print(f"  - Desvio padrão: {valid_lead_times.std():.2f} dias")
    
    # Calculate lead time by supplier
    supplier_lead_times = df.groupby('fornecedor')['lead_time_days'].agg([
        ('mean', 'mean'),
        ('std', 'std'),
        ('count', 'count')
    ]).round(2)
    
    # Calculate lead time by family
    family_lead_times = df.groupby('familia')['lead_time_days'].agg([
        ('mean', 'mean'),
        ('std', 'std'),
        ('count', 'count')
    ]).round(2)
    
    print(f"\n[INFO] Lead times por fornecedor: {len(supplier_lead_times)} fornecedores")
    print(f"[INFO] Lead times por família: {len(family_lead_times)} famílias")
    
    return df, supplier_lead_times, family_lead_times

def identify_top_families(df, top_n=5):
    """Identify top N families by volume and frequency"""
    print("\n" + "=" * 80)
    print(f"IDENTIFICANDO TOP {top_n} FAMÍLIAS")
    print("=" * 80)
    
    # Family statistics
    family_stats = df.groupby('familia').agg({
        'quantidade': ['sum', 'mean', 'count'],
        'material': 'nunique',
        'deposito': 'nunique'
    }).round(2)
    
    family_stats.columns = ['quantidade_total', 'quantidade_media', 'frequencia', 
                           'materiais_unicos', 'depositos_unicos']
    
    # Calculate importance score
    family_stats['importance_score'] = (
        family_stats['frequencia'] / family_stats['frequencia'].max() * 0.4 +
        family_stats['quantidade_total'] / family_stats['quantidade_total'].max() * 0.3 +
        family_stats['materiais_unicos'] / family_stats['materiais_unicos'].max() * 0.2 +
        family_stats['depositos_unicos'] / family_stats['depositos_unicos'].max() * 0.1
    )
    
    # Sort by importance
    family_stats = family_stats.sort_values('importance_score', ascending=False)
    
    top_families = family_stats.head(top_n)
    
    print(f"\n[INFO] Top {top_n} famílias identificadas:")
    print(top_families.to_string())
    
    return top_families, family_stats

def create_processed_dataset(df):
    """Create processed dataset ready for feature engineering"""
    print("\n" + "=" * 80)
    print("CRIANDO DATASET PROCESSADO")
    print("=" * 80)
    
    # Use data_solicitado as primary date (most complete)
    df['date'] = df['data_solicitado']
    
    # Create item_id (combine material + familia for uniqueness)
    df['item_id'] = df['familia'] + '_' + df['material'].str[:50]
    
    # Create site_id from deposito
    df['site_id'] = df['deposito'].astype('category').cat.codes
    
    # Create category from familia
    df['category'] = df['familia']
    
    # Prepare final columns
    processed_cols = [
        'date', 'item_id', 'material', 'familia', 'category',
        'quantidade', 'unidade_medida', 'deposito', 'site_id',
        'fornecedor', 'solicitacao', 'lead_time_days',
        'data_requisitada', 'data_solicitado', 'data_compra'
    ]
    
    # Keep only available columns
    available_cols = [col for col in processed_cols if col in df.columns]
    df_processed = df[available_cols].copy()
    
    # Remove rows without date
    df_processed = df_processed[df_processed['date'].notna()].copy()
    
    print(f"\n[INFO] Dataset processado: {len(df_processed)} registros")
    print(f"[INFO] Período: {df_processed['date'].min()} a {df_processed['date'].max()}")
    print(f"[INFO] Items únicos: {df_processed['item_id'].nunique()}")
    print(f"[INFO] Famílias: {df_processed['familia'].nunique()}")
    print(f"[INFO] Sites: {df_processed['site_id'].nunique()}")
    
    return df_processed

def save_results(df_processed, supplier_lead_times, family_lead_times, top_families, family_stats):
    """Save all processed results"""
    print("\n" + "=" * 80)
    print("SALVANDO RESULTADOS")
    print("=" * 80)
    
    # Save processed dataset
    output_file = OUTPUT_DIR / "nova_corrente_processed.csv"
    df_processed.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n[SUCCESS] Dataset salvo: {output_file}")
    
    # Save lead times
    supplier_file = OUTPUT_DIR / "lead_time_by_supplier.csv"
    supplier_lead_times.to_csv(supplier_file, encoding='utf-8')
    print(f"[SUCCESS] Lead times por fornecedor: {supplier_file}")
    
    family_file = OUTPUT_DIR / "lead_time_by_family.csv"
    family_lead_times.to_csv(family_file, encoding='utf-8')
    print(f"[SUCCESS] Lead times por família: {family_file}")
    
    # Save top families
    top_families_file = OUTPUT_DIR / "top_5_families.csv"
    top_families.to_csv(top_families_file, encoding='utf-8')
    print(f"[SUCCESS] Top 5 famílias: {top_families_file}")
    
    # Save all family stats
    all_families_file = OUTPUT_DIR / "all_families_stats.csv"
    family_stats.to_csv(all_families_file, encoding='utf-8')
    print(f"[SUCCESS] Estatísticas todas famílias: {all_families_file}")
    
    # Save summary JSON
    summary = {
        'processing_date': datetime.now().isoformat(),
        'total_records': len(df_processed),
        'date_range': {
            'min': str(df_processed['date'].min()),
            'max': str(df_processed['date'].max()),
            'span_days': (df_processed['date'].max() - df_processed['date'].min()).days
        },
        'unique_items': int(df_processed['item_id'].nunique()),
        'unique_families': int(df_processed['familia'].nunique()),
        'unique_sites': int(df_processed['site_id'].nunique()),
        'unique_suppliers': int(df_processed['fornecedor'].nunique()),
        'lead_time_stats': {
            'mean': float(df_processed['lead_time_days'].mean()) if df_processed['lead_time_days'].notna().any() else None,
            'median': float(df_processed['lead_time_days'].median()) if df_processed['lead_time_days'].notna().any() else None,
            'std': float(df_processed['lead_time_days'].std()) if df_processed['lead_time_days'].notna().any() else None
        },
        'top_5_families': top_families.index.tolist(),
        'top_families_stats': top_families.to_dict('index')
    }
    
    summary_file = OUTPUT_DIR / "processing_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"[SUCCESS] Resumo: {summary_file}")
    
    return summary

def main():
    """Main processing pipeline"""
    print("\n" + "=" * 80)
    print("PIPELINE DE PROCESSAMENTO: NOVA CORRENTE")
    print("=" * 80 + "\n")
    
    # Step 1: Load data
    df = load_nova_corrente_data()
    
    # Step 2: Calculate lead times
    df, supplier_lead_times, family_lead_times = calculate_lead_times(df)
    
    # Step 3: Identify top families
    top_families, family_stats = identify_top_families(df, top_n=5)
    
    # Step 4: Create processed dataset
    df_processed = create_processed_dataset(df)
    
    # Step 5: Save results
    summary = save_results(df_processed, supplier_lead_times, family_lead_times, 
                          top_families, family_stats)
    
    print("\n" + "=" * 80)
    print("PROCESSAMENTO CONCLUÍDO!")
    print("=" * 80)
    print(f"\n[RESUMO]")
    print(f"  - Registros processados: {summary['total_records']:,}")
    print(f"  - Items únicos: {summary['unique_items']}")
    print(f"  - Famílias: {summary['unique_families']}")
    print(f"  - Top 5 famílias: {', '.join(summary['top_5_families'])}")
    print(f"\n[PRÓXIMOS PASSOS]")
    print(f"  1. Enriquecer com features externas")
    print(f"  2. Implementar feature engineering avançado")
    print(f"  3. Combinar com datasets existentes")
    
    return df_processed, summary

if __name__ == "__main__":
    main()

