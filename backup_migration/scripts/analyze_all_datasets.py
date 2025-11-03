"""Análise profunda de todos os datasets - colunas, variáveis e contexto."""
import pandas as pd
import json
from pathlib import Path
from collections import Counter
import numpy as np

project_root = Path(__file__).parent.parent

def analyze_dataset_file(file_path: Path, dataset_id: str):
    """Analisar um arquivo de dataset em profundidade"""
    print(f"\n{'='*80}")
    print(f"ANÁLISE PROFUNDA: {dataset_id}")
    print(f"{'='*80}")
    print(f"Arquivo: {file_path.name}")
    print(f"Caminho: {file_path}")
    
    if not file_path.exists():
        print(f"❌ Arquivo não encontrado")
        return None
    
    # Detectar tipo de arquivo
    ext = file_path.suffix.lower()
    
    try:
        if ext == '.csv':
            # Ler CSV com diferentes encodings
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            df = None
            for enc in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=enc, low_memory=False)
                    break
                except:
                    continue
            if df is None:
                print(f"❌ Não foi possível ler o CSV com nenhum encoding testado")
                return None
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            print(f"⚠️  Formato não suportado: {ext}")
            return None
        
        # Informações básicas
        print(f"\n📊 INFORMAÇÕES BÁSICAS:")
        print(f"  Total de registros: {len(df):,}")
        print(f"  Total de colunas: {len(df.columns)}")
        print(f"  Tamanho do arquivo: {file_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Análise de colunas
        print(f"\n📋 COLUNAS E VARIÁVEIS:")
        print(f"{'Coluna':<30} {'Tipo':<15} {'Não-Nulos':<15} {'% Não-Nulos':<15} {'Valores Únicos':<15}")
        print("-" * 90)
        
        column_analysis = {}
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            non_null = df[col].notna().sum()
            pct_non_null = (non_null / len(df) * 100) if len(df) > 0 else 0
            unique = df[col].nunique()
            
            print(f"{col[:28]:<30} {dtype[:13]:<15} {non_null:<15,} {pct_non_null:>13.2f}% {unique:<15,}")
            
            # Análise detalhada por tipo
            col_analysis = {
                'dtype': dtype,
                'non_null': int(non_null),
                'pct_non_null': float(pct_non_null),
                'unique': int(unique),
                'null_count': int(df[col].isna().sum()),
                'null_pct': float((df[col].isna().sum() / len(df) * 100) if len(df) > 0 else 0)
            }
            
            # Estatísticas para numéricas
            if pd.api.types.is_numeric_dtype(df[col]):
                col_analysis.update({
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                    'std': float(df[col].std()) if not df[col].isna().all() else None,
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None,
                    'median': float(df[col].median()) if not df[col].isna().all() else None,
                    'q25': float(df[col].quantile(0.25)) if not df[col].isna().all() else None,
                    'q75': float(df[col].quantile(0.75)) if not df[col].isna().all() else None,
                })
            
            # Valores únicos para categóricas
            if pd.api.types.is_object_dtype(df[col]) or unique < 50:
                unique_vals = df[col].value_counts().head(10).to_dict()
                col_analysis['top_values'] = {str(k): int(v) for k, v in unique_vals.items()}
            
            column_analysis[col] = col_analysis
        
        # Análise de tipos de dados
        print(f"\n🔢 DISTRIBUIÇÃO DE TIPOS:")
        dtype_counts = Counter(df.dtypes.astype(str))
        for dtype, count in dtype_counts.items():
            print(f"  {dtype}: {count} coluna(s)")
        
        # Análise de valores faltantes
        print(f"\n⚠️  VALORES FALTANTES:")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100)
        missing_df = pd.DataFrame({
            'Coluna': missing.index,
            'Faltantes': missing.values,
            '%': missing_pct.values
        })
        missing_df = missing_df[missing_df['Faltantes'] > 0].sort_values('Faltantes', ascending=False)
        
        if len(missing_df) > 0:
            for _, row in missing_df.iterrows():
                print(f"  {row['Coluna']:<30} {int(row['Faltantes']):<15,} ({row['%']:.2f}%)")
        else:
            print(f"  ✅ Nenhum valor faltante encontrado")
        
        # Primeiras linhas de exemplo
        print(f"\n📄 EXEMPLOS (Primeiras 3 linhas):")
        print(df.head(3).to_string())
        
        # Análise de duplicatas
        print(f"\n🔄 DUPLICATAS:")
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"  ⚠️  {duplicates:,} linha(s) duplicada(s) encontrada(s) ({duplicates/len(df)*100:.2f}%)")
        else:
            print(f"  ✅ Nenhuma linha duplicada")
        
        # Análise temporal (se houver coluna de data)
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower() or 'timestamp' in col.lower()]
        if date_cols:
            print(f"\n📅 ANÁLISE TEMPORAL:")
            for col in date_cols:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    valid_dates = df[col].notna().sum()
                    if valid_dates > 0:
                        date_range = df[col].min(), df[col].max()
                        print(f"  {col}:")
                        print(f"    Período: {date_range[0]} até {date_range[1]}")
                        print(f"    Total de dias: {(date_range[1] - date_range[0]).days}")
                        print(f"    Registros com data válida: {valid_dates:,} ({valid_dates/len(df)*100:.2f}%)")
                except:
                    pass
        
        return {
            'dataset_id': dataset_id,
            'file_path': str(file_path),
            'shape': {'rows': len(df), 'cols': len(df.columns)},
            'columns': column_analysis,
            'dtypes': dtype_counts,
            'missing': missing_df.to_dict('records') if len(missing_df) > 0 else [],
            'duplicates': int(duplicates),
            'sample_data': df.head(5).to_dict('records')
        }
        
    except Exception as e:
        print(f"❌ Erro ao analisar arquivo: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Analisar todos os datasets"""
    raw_dir = project_root / 'data/raw'
    
    print("=" * 80)
    print("ANÁLISE PROFUNDA DE TODOS OS DATASETS")
    print("=" * 80)
    
    all_analyses = {}
    
    # Iterar sobre todas as pastas de datasets
    for dataset_dir in sorted(raw_dir.iterdir()):
        if not dataset_dir.is_dir():
            continue
        
        dataset_id = dataset_dir.name
        
        # Encontrar arquivos de dados
        data_files = []
        for ext in ['.csv', '.xlsx', '.xls', '.parquet', '.json']:
            data_files.extend(dataset_dir.glob(f'*{ext}'))
        
        if not data_files:
            print(f"\n⚠️  {dataset_id}: Nenhum arquivo de dados encontrado")
            continue
        
        # Analisar o primeiro arquivo principal (ou todos)
        main_file = data_files[0]  # Pode ser mais inteligente depois
        analysis = analyze_dataset_file(main_file, dataset_id)
        
        if analysis:
            all_analyses[dataset_id] = analysis
    
    # Salvar análise completa
    output_file = project_root / 'docs/DEEP_DATASETS_ANALYSIS.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_analyses, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"\n\n{'='*80}")
    print(f"RESUMO DA ANÁLISE")
    print(f"{'='*80}")
    print(f"\n✅ {len(all_analyses)} dataset(s) analisado(s)")
    print(f"📄 Análise completa salva em: {output_file}")
    
    # Resumo estatístico
    total_rows = sum(a['shape']['rows'] for a in all_analyses.values())
    total_cols = sum(a['shape']['cols'] for a in all_analyses.values())
    total_missing = sum(len(a.get('missing', [])) for a in all_analyses.values())
    
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"  Total de registros (todos os datasets): {total_rows:,}")
    print(f"  Total de colunas (todos os datasets): {total_cols}")
    print(f"  Datasets com valores faltantes: {total_missing}")

if __name__ == "__main__":
    main()

