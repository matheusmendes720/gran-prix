"""
Create combined ML-ready dataset with top 5 families
- Combine Nova Corrente enriched data with existing training data
- Focus on top 5 families for multi-item forecasting
- Create train/validation/test splits
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).parent.parent.parent
NOVA_CORRENTE_ENRICHED = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_enriched.csv"
TRAINING_DATA = PROJECT_ROOT / "data" / "training"
TOP_FAMILIES_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "top_5_families.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "nova_corrente"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_datasets():
    """Load all datasets"""
    print("=" * 80)
    print("CARREGANDO DATASETS PARA COMBINAÇÃO")
    print("=" * 80)
    
    # Load Nova Corrente enriched
    nova_corrente = pd.read_csv(NOVA_CORRENTE_ENRICHED, parse_dates=['date'])
    print(f"\n[INFO] Nova Corrente enriched: {len(nova_corrente):,} registros")
    print(f"[INFO] Features: {len(nova_corrente.columns)}")
    
    # Load top families
    top_families = pd.read_csv(TOP_FAMILIES_FILE, index_col=0)
    top_family_names = top_families.index.tolist()
    print(f"\n[INFO] Top 5 famílias: {', '.join(top_family_names)}")
    
    # Load existing training data (sample)
    training_file = TRAINING_DATA / "unknown_train.csv"
    if training_file.exists():
        training_data = pd.read_csv(training_file, nrows=5000, parse_dates=['date'])
        print(f"\n[INFO] Training data (sample): {len(training_data):,} registros")
    else:
        training_data = None
        print(f"\n[WARNING] Training data não encontrado")
    
    return nova_corrente, top_family_names, training_data

def filter_top_families(df, top_family_names):
    """Filter dataset to top 5 families"""
    print("\n" + "=" * 80)
    print("FILTRANDO TOP 5 FAMÍLIAS")
    print("=" * 80)
    
    # Filter to top families
    df_filtered = df[df['familia'].isin(top_family_names)].copy()
    
    print(f"\n[INFO] Registros após filtro: {len(df_filtered):,}/{len(df):,}")
    print(f"\n[INFO] Distribuição por família:")
    family_counts = df_filtered['familia'].value_counts()
    for familia, count in family_counts.items():
        print(f"  - {familia}: {count:,} registros ({count/len(df_filtered)*100:.1f}%)")
    
    return df_filtered

def prepare_features(df):
    """Prepare features for ML"""
    print("\n" + "=" * 80)
    print("PREPARANDO FEATURES PARA ML")
    print("=" * 80)
    
    # Ensure date column
    if 'date' not in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Create item_id consistent format
    if 'item_id' not in df.columns:
        df['item_id'] = df['familia'] + '_' + df['material'].str[:30]
    
    # Encode categorical features
    if 'familia' in df.columns:
        df['familia_encoded'] = df['familia'].astype('category').cat.codes
    if 'site_id' not in df.columns or df['site_id'].isna().any():
        df['site_id'] = df['deposito'].astype('category').cat.codes if 'deposito' in df.columns else 0
    
    # Create target variable (quantity)
    if 'target' not in df.columns:
        df['target'] = df['quantidade'].copy()
    
    # Ensure numeric columns
    numeric_cols = ['quantidade', 'lead_time_days']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"\n[INFO] Features preparadas:")
    print(f"  - Total features: {len(df.columns)}")
    print(f"  - Item IDs únicos: {df['item_id'].nunique()}")
    print(f"  - Famílias: {df['familia'].nunique() if 'familia' in df.columns else 0}")
    
    return df

def create_splits(df, test_size=0.2, val_size=0.2):
    """Create train/validation/test splits"""
    print("\n" + "=" * 80)
    print("CRIANDO SPLITS TRAIN/VALIDATION/TEST")
    print("=" * 80)
    
    # Sort by date
    df = df.sort_values('date').copy()
    
    # Split by date (time series split)
    total_len = len(df)
    test_start = int(total_len * (1 - test_size))
    val_start = int(test_start * (1 - val_size))
    
    train_df = df.iloc[:val_start].copy()
    val_df = df.iloc[val_start:test_start].copy()
    test_df = df.iloc[test_start:].copy()
    
    print(f"\n[INFO] Splits criados:")
    print(f"  - Train: {len(train_df):,} registros ({len(train_df)/total_len*100:.1f}%)")
    print(f"    Período: {train_df['date'].min()} a {train_df['date'].max()}")
    print(f"  - Validation: {len(val_df):,} registros ({len(val_df)/total_len*100:.1f}%)")
    print(f"    Período: {val_df['date'].min()} a {val_df['date'].max()}")
    print(f"  - Test: {len(test_df):,} registros ({len(test_df)/total_len*100:.1f}%)")
    print(f"    Período: {test_df['date'].min()} a {test_df['date'].max()}")
    
    # Family distribution in splits
    if 'familia' in df.columns:
        print(f"\n[INFO] Distribuição por família (train):")
        train_family_counts = train_df['familia'].value_counts()
        for familia, count in train_family_counts.head(5).items():
            print(f"  - {familia}: {count:,} registros")
    
    return train_df, val_df, test_df

def save_datasets(train_df, val_df, test_df, df_combined):
    """Save all datasets"""
    print("\n" + "=" * 80)
    print("SALVANDO DATASETS")
    print("=" * 80)
    
    # Save splits
    train_file = OUTPUT_DIR / "nova_corrente_top5_train.csv"
    train_df.to_csv(train_file, index=False, encoding='utf-8')
    print(f"\n[SUCCESS] Train: {train_file}")
    
    val_file = OUTPUT_DIR / "nova_corrente_top5_validation.csv"
    val_df.to_csv(val_file, index=False, encoding='utf-8')
    print(f"[SUCCESS] Validation: {val_file}")
    
    test_file = OUTPUT_DIR / "nova_corrente_top5_test.csv"
    test_df.to_csv(test_file, index=False, encoding='utf-8')
    print(f"[SUCCESS] Test: {test_file}")
    
    # Save combined
    combined_file = OUTPUT_DIR / "nova_corrente_top5_combined.csv"
    df_combined.to_csv(combined_file, index=False, encoding='utf-8')
    print(f"[SUCCESS] Combined: {combined_file}")
    
    # Save summary
    summary = {
        'creation_date': datetime.now().isoformat(),
        'total_records': len(df_combined),
        'total_features': len(df_combined.columns),
        'splits': {
            'train': {
                'records': len(train_df),
                'percentage': float(len(train_df) / len(df_combined) * 100),
                'date_range': {
                    'min': str(train_df['date'].min()),
                    'max': str(train_df['date'].max())
                }
            },
            'validation': {
                'records': len(val_df),
                'percentage': float(len(val_df) / len(df_combined) * 100),
                'date_range': {
                    'min': str(val_df['date'].min()),
                    'max': str(val_df['date'].max())
                }
            },
            'test': {
                'records': len(test_df),
                'percentage': float(len(test_df) / len(df_combined) * 100),
                'date_range': {
                    'min': str(test_df['date'].min()),
                    'max': str(test_df['date'].max())
                }
            }
        },
        'families': df_combined['familia'].value_counts().to_dict() if 'familia' in df_combined.columns else {},
        'items_count': int(df_combined['item_id'].nunique()),
        'date_range': {
            'min': str(df_combined['date'].min()),
            'max': str(df_combined['date'].max()),
            'span_days': (df_combined['date'].max() - df_combined['date'].min()).days
        },
        'features_list': list(df_combined.columns)
    }
    
    summary_file = OUTPUT_DIR / "combined_ml_dataset_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"[SUCCESS] Summary: {summary_file}")
    
    return summary

def main():
    """Main pipeline"""
    print("\n" + "=" * 80)
    print("PIPELINE: DATASET COMBINADO ML-READY")
    print("=" * 80 + "\n")
    
    # Step 1: Load datasets
    nova_corrente, top_family_names, training_data = load_datasets()
    
    # Step 2: Filter to top 5 families
    df_filtered = filter_top_families(nova_corrente, top_family_names)
    
    # Step 3: Prepare features
    df_combined = prepare_features(df_filtered)
    
    # Step 4: Create splits
    train_df, val_df, test_df = create_splits(df_combined)
    
    # Step 5: Save datasets
    summary = save_datasets(train_df, val_df, test_df, df_combined)
    
    print("\n" + "=" * 80)
    print("DATASET COMBINADO CRIADO!")
    print("=" * 80)
    print(f"\n[RESUMO]")
    print(f"  - Total registros: {summary['total_records']:,}")
    print(f"  - Total features: {summary['total_features']}")
    print(f"  - Items únicos: {summary['items_count']}")
    print(f"  - Famílias: {len(summary['families'])}")
    print(f"  - Train: {summary['splits']['train']['records']:,} ({summary['splits']['train']['percentage']:.1f}%)")
    print(f"  - Validation: {summary['splits']['validation']['records']:,} ({summary['splits']['validation']['percentage']:.1f}%)")
    print(f"  - Test: {summary['splits']['test']['records']:,} ({summary['splits']['test']['percentage']:.1f}%)")
    print(f"\n[PRÓXIMOS PASSOS]")
    print(f"  1. Validar qualidade dos dados")
    print(f"  2. Treinar modelos por família")
    print(f"  3. Avaliar MAPE < 15%")
    
    return train_df, val_df, test_df, summary

if __name__ == "__main__":
    main()

