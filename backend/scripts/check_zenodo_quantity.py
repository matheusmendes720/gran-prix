"""Verificar se o quantity do Zenodo foi corrigido."""
import pandas as pd
from pathlib import Path

project_root = Path(__file__).parent.parent

print("=== VERIFICAÇÃO DO ZENODO ===\n")

# Verificar preprocessado
df_proc = pd.read_csv(project_root / 'data/processed/zenodo_milan_telecom_preprocessed.csv', low_memory=False)
print(f"Zenodo Preprocessed:")
print(f"  Registros: {len(df_proc):,}")
print(f"  Quantity Mean: {df_proc['quantity'].mean():.4f}")
print(f"  Quantity Std: {df_proc['quantity'].std():.4f}")
print(f"  Quantity Min: {df_proc['quantity'].min():.4f}")
print(f"  Quantity Max: {df_proc['quantity'].max():.4f}")
zeros = (df_proc['quantity'] == 0).sum()
print(f"  Zeros: {zeros:,} ({zeros/len(df_proc)*100:.1f}%)")
print(f"\nPrimeiros 10 valores de quantity:")
print(df_proc['quantity'].head(10).values)
print(f"\nÚltimos 10 valores de quantity:")
print(df_proc['quantity'].tail(10).values)

