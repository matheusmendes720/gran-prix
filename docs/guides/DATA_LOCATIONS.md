# 📍 Localização dos Dados - Guia Rápido

## 🎯 DATASET PRINCIPAL - USE ESTE!

### ✅ `data/processed/unified_dataset_with_factors.csv`

**Este é o arquivo principal com TODOS os dados processados!**

```
Localização: data/processed/unified_dataset_with_factors.csv
Tamanho: 27.25 MB
Registros: 118,082 linhas
Colunas: 31 colunas (9 base + 22 external factors)
Status: ✅ PRONTO PARA ML TRAINING
```

**Contém:**
- ✅ Todos os datasets mesclados
- ✅ Fatores externos integrados
- ✅ Schema unificado
- ✅ Pronto para ARIMA, Prophet, LSTM

---

## 📊 Dados de Treinamento (Train/Test Splits)

### ✅ `data/training/`

**Datasets divididos por item e prontos para treinamento:**

#### Dataset Maior (unknown - 117K registros)
- **`unknown_train.csv`** - 93,881 registros (80%) - **11.61 MB** ⭐ MAIOR
- **`unknown_test.csv`** - 23,471 registros (20%) - 2.90 MB
- **`unknown_full.csv`** - 117,352 registros (100%) - 14.51 MB

#### Dataset Menor (CONN-001 - 730 registros)
- **`CONN-001_train.csv`** - 584 registros (80%) - 0.06 MB
- **`CONN-001_test.csv`** - 146 registros (20%) - 0.02 MB
- **`CONN-001_full.csv`** - 730 registros (100%) - 0.08 MB

#### Metadados
- **`metadata.json`** - Metadados do treinamento
- **`training_summary.json`** - Resumo estatístico

---

## 📂 Estrutura Completa

```
data/
│
├── processed/                    ⭐ DADOS PROCESSADOS
│   ├── unified_dataset_with_factors.csv  (27.25 MB) ⭐ PRINCIPAL
│   ├── unified_dataset.csv              (10.04 MB)
│   └── *_preprocessed.csv               (vários)
│
├── training/                     ⭐ DADOS DE TREINAMENTO
│   ├── unknown_train.csv         (11.61 MB) ⭐ MAIOR DATASET
│   ├── unknown_test.csv          (2.90 MB)
│   ├── unknown_full.csv          (14.51 MB)
│   ├── CONN-001_train.csv        (0.06 MB)
│   ├── CONN-001_test.csv         (0.02 MB)
│   └── CONN-001_full.csv         (0.08 MB)
│
└── raw/                          📥 DADOS BRUTOS
    ├── kaggle_*/                 (vários datasets)
    ├── zenodo_milan_telecom/     (28.7 MB)
    └── test_dataset/             (37 KB)
```

---

## 🚀 Como Usar

### 1. Dataset Principal Completo

```python
import pandas as pd

# Carregar TODOS os dados com fatores externos
df = pd.read_csv('data/processed/unified_dataset_with_factors.csv')
print(f"Total: {len(df):,} registros")
print(f"Colunas: {len(df.columns)}")
```

### 2. Dataset de Treinamento (Maior)

```python
# Dataset maior (117K registros)
train = pd.read_csv('data/training/unknown_train.csv')
test = pd.read_csv('data/training/unknown_test.csv')
print(f"Train: {len(train):,} | Test: {len(test):,}")
```

### 3. Dataset de Treinamento (Menor)

```python
# Dataset menor (730 registros) - para testes rápidos
train = pd.read_csv('data/training/CONN-001_train.csv')
test = pd.read_csv('data/training/CONN-001_test.csv')
print(f"Train: {len(train):,} | Test: {len(test):,}")
```

---

## ✅ Resumo

**PRINCIPAIS ARQUIVOS:**

1. **`data/processed/unified_dataset_with_factors.csv`** 
   - 118,082 registros | 31 colunas | 27.25 MB
   - ✅ **USE ESTE PARA ANÁLISE GERAL**

2. **`data/training/unknown_train.csv`**
   - 93,881 registros | 11.61 MB
   - ✅ **USE ESTE PARA TREINAR MODELOS ML**

3. **`data/training/CONN-001_train.csv`**
   - 584 registros | 0.06 MB
   - ✅ **USE ESTE PARA TESTES RÁPIDOS**

---

**Todos os dados estão prontos e localizados em `data/`!** 🎉

