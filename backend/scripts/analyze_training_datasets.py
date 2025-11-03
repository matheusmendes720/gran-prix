"""Análise detalhada dos datasets de treinamento."""
import pandas as pd
import os
from pathlib import Path

project_root = Path(__file__).parent.parent

print("=== ANÁLISE DETALHADA DOS DATASETS DE TREINAMENTO ===\n")

# 1. Unknown Train
if os.path.exists(project_root / 'data/training/unknown_train.csv'):
    train = pd.read_csv(project_root / 'data/training/unknown_train.csv', low_memory=False)
    print("1. UNKNOWN TRAIN:")
    print(f"   Registros: {len(train):,}")
    print(f"   Colunas: {len(train.columns)}")
    print(f"   Quantity Mean: {train['quantity'].mean():.4f}")
    print(f"   Quantity Std: {train['quantity'].std():.4f}")
    print(f"   Quantity Min: {train['quantity'].min():.4f}")
    print(f"   Quantity Max: {train['quantity'].max():.4f}")
    zeros = (train['quantity'] == 0).sum()
    print(f"   Zeros: {zeros:,} ({zeros/len(train)*100:.1f}%)")
    if 'dataset_source' in train.columns:
        print(f"   Dataset sources: {train['dataset_source'].value_counts().to_dict()}")
    print(f"   Primeiras colunas: {list(train.columns[:5])}")
    print()

# 2. CONN-001 Train
if os.path.exists(project_root / 'data/training/CONN-001_train.csv'):
    conn = pd.read_csv(project_root / 'data/training/CONN-001_train.csv', low_memory=False)
    print("2. CONN-001 TRAIN:")
    print(f"   Registros: {len(conn):,}")
    print(f"   Colunas: {len(conn.columns)}")
    print(f"   Quantity Mean: {conn['quantity'].mean():.2f}")
    print(f"   Quantity Std: {conn['quantity'].std():.2f}")
    print(f"   Quantity Min: {conn['quantity'].min():.0f}")
    print(f"   Quantity Max: {conn['quantity'].max():.0f}")
    zeros = (conn['quantity'] == 0).sum()
    print(f"   Zeros: {zeros} (0%)")
    print()

# 3. Zenodo Preprocessed
if os.path.exists(project_root / 'data/processed/zenodo_milan_telecom_preprocessed.csv'):
    zenodo = pd.read_csv(project_root / 'data/processed/zenodo_milan_telecom_preprocessed.csv', low_memory=False)
    print("3. ZENODO PREPROCESSED:")
    print(f"   Registros: {len(zenodo):,}")
    print(f"   Colunas: {len(zenodo.columns)}")
    print(f"   Quantity Mean: {zenodo['quantity'].mean():.4f}")
    print(f"   Quantity Std: {zenodo['quantity'].std():.4f}")
    print(f"   Quantity Min: {zenodo['quantity'].min():.4f}")
    print(f"   Quantity Max: {zenodo['quantity'].max():.4f}")
    zeros = (zenodo['quantity'] == 0).sum()
    print(f"   Zeros: {zeros:,} ({zeros/len(zenodo)*100:.1f}%)")
    print()

# 4. Unified Dataset
if os.path.exists(project_root / 'data/processed/unified_dataset_with_factors.csv'):
    unified = pd.read_csv(project_root / 'data/processed/unified_dataset_with_factors.csv', low_memory=False)
    print("4. UNIFIED DATASET:")
    print(f"   Registros: {len(unified):,}")
    print(f"   Colunas: {len(unified.columns)}")
    if 'dataset_source' in unified.columns:
        print(f"   Dataset sources: {unified['dataset_source'].value_counts().to_dict()}")
    print(f"   Primeiras colunas: {list(unified.columns[:5])}")
    print()

print("=== RECOMENDAÇÕES ===")
print("✅ USE 'unknown_train.csv' PARA TREINAR MODELOS ML COMPLETOS")
print("✅ USE 'CONN-001_train.csv' PARA TESTES RÁPIDOS E PROTOPIPAGEM")
print("✅ USE 'unified_dataset_with_factors.csv' PARA ANÁLISE EXPLORATÓRIA")

