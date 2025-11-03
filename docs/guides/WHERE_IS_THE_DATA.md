# 📁 Onde Estão os Dados?

## 🎯 Dataset Principal Final

### ✅ `data/processed/unified_dataset_with_factors.csv`

**Este é o dataset principal com TODOS os dados processados e prontos para ML!**

- **Localização:** `data/processed/unified_dataset_with_factors.csv`
- **Tamanho:** ~27.25 MB
- **Registros:** 118,082 linhas
- **Colunas:** 31 colunas (9 base + 22 external factors)
- **Status:** ✅ **PRONTO PARA ML TRAINING**

**Conteúdo:**
- ✅ Dados de todos os datasets baixados
- ✅ Fatores externos integrados (clima, econômico, regulatório, operacional)
- ✅ Schema unificado
- ✅ Pronto para ARIMA, Prophet, LSTM

---

## 📊 Datasets de Treinamento (Train/Test Splits)

### ✅ `data/training/`

**Datasets divididos por item e prontos para treinamento:**

| Arquivo | Tamanho | Registros | Descrição |
|---------|---------|-----------|-----------|
| `CONN-001_train.csv` | ~62 KB | 584 | Dataset de treino (80%) |
| `CONN-001_test.csv` | ~16 KB | 146 | Dataset de teste (20%) |
| `CONN-001_full.csv` | ~78 KB | 730 | Dataset completo |
| `unknown_train.csv` | ~9.4 MB | 93,881 | Dataset de treino (80%) |
| `unknown_test.csv` | ~2.3 MB | 23,471 | Dataset de teste (20%) |
| `unknown_full.csv` | ~11.8 MB | 117,352 | Dataset completo |
| `metadata.json` | ~0.1 KB | - | Metadados do treinamento |
| `training_summary.json` | ~0.3 KB | - | Resumo estatístico |

**Total:** ~23 MB de dados de treinamento prontos!

---

## 📂 Estrutura Completa de Dados

```
data/
├── raw/                          # Dados brutos baixados
│   ├── kaggle_daily_demand/
│   │   └── Daily Demand Forecasting Orders.csv (6 KB)
│   ├── kaggle_logistics_warehouse/
│   │   └── logistics_dataset.csv (365 KB)
│   ├── kaggle_retail_inventory/
│   │   └── retail_store_inventory.csv (6 MB)
│   ├── kaggle_supply_chain/
│   │   └── supply_chain_dataset1.csv (6.4 MB)
│   ├── zenodo_milan_telecom/
│   │   └── output-step-bsId_1-2023_9_28_12_50_10.csv (28.7 MB) ⭐
│   └── test_dataset/
│       └── test_data.csv (37 KB)
│
├── processed/                    # Dados processados
│   ├── unified_dataset.csv (27 MB)           # Dataset mesclado
│   ├── unified_dataset_with_factors.csv (27.25 MB) ⭐ PRINCIPAL
│   ├── kaggle_*_preprocessed.csv (vários)
│   ├── zenodo_milan_telecom_preprocessed.csv (vários MB)
│   └── test_dataset_preprocessed.csv
│
└── training/                     # Dados prontos para ML
    ├── CONN-001_train.csv (62 KB)
    ├── CONN-001_test.csv (16 KB)
    ├── CONN-001_full.csv (78 KB)
    ├── unknown_train.csv (9.4 MB) ⭐ MAIOR
    ├── unknown_test.csv (2.3 MB)
    ├── unknown_full.csv (11.8 MB)
    ├── metadata.json
    └── training_summary.json
```

---

## 🎯 Como Usar os Dados

### 1. Dataset Principal (Todos os Dados)

```python
import pandas as pd

# Carregar dataset principal com TODOS os dados e fatores externos
df = pd.read_csv('data/processed/unified_dataset_with_factors.csv')

print(f"Total: {len(df):,} registros")
print(f"Colunas: {len(df.columns)}")
print(df.head())
```

### 2. Datasets de Treinamento (por Item)

```python
# Carregar dados de treino/teste para um item específico
train_df = pd.read_csv('data/training/CONN-001_train.csv')
test_df = pd.read_csv('data/training/CONN-001_test.csv')

print(f"Train: {len(train_df):,} registros")
print(f"Test: {len(test_df):,} registros")
```

### 3. Dataset Maior (unknown - 117K registros)

```python
# Dataset maior (maioria dos dados do Zenodo)
train_df = pd.read_csv('data/training/unknown_train.csv')
test_df = pd.read_csv('data/training/unknown_test.csv')

print(f"Train: {len(train_df):,} registros")  # 93,881
print(f"Test: {len(test_df):,} registros")    # 23,471
```

---

## 📈 Estatísticas dos Dados

### Dataset Principal
- **118,082 registros** unificados
- **31 colunas** (9 base + 22 external factors)
- **27.25 MB** de dados processados
- **Date range:** 1970-01-01 to 2024-12-30

### Composição por Fonte
- **zenodo_milan_telecom:** 116,257 (98.5%)
- **kaggle_retail_inventory:** 731 (0.6%)
- **test_dataset:** 730 (0.6%)
- **kaggle_supply_chain:** 364 (0.3%)

### Datasets de Treinamento
- **2 itens preparados:**
  - `CONN-001`: 730 registros (584 train + 146 test)
  - `unknown`: 117,352 registros (93,881 train + 23,471 test)

---

## 🚀 Próximos Passos com os Dados

### 1. Treinar Modelos ML

```python
# Usar dados de treinamento
train_df = pd.read_csv('data/training/unknown_train.csv')

# Preparar para ARIMA/Prophet
train_df['date'] = pd.to_datetime(train_df['date'])
train_df = train_df.set_index('date')
series = train_df['quantity']

# Treinar modelos...
```

### 2. Calcular Reorder Points (PP)

```python
# Usar forecast + lead time
forecast = model.forecast(steps=30)
avg_demand = forecast.mean()
pp = (avg_demand * lead_time) + safety_stock
```

### 3. Gerar Alertas

```python
# Verificar se estoque <= PP
if current_stock <= pp:
    print(f"ALERTA: Reordenar {int(pp - current_stock)} unidades")
```

---

## ✅ Resumo

### Dados Principais
- **`data/processed/unified_dataset_with_factors.csv`** ⭐ **USE ESTE!**
  - 118,082 registros
  - 31 colunas
  - 27.25 MB
  - **PRONTO PARA ML**

### Dados de Treinamento
- **`data/training/unknown_train.csv`** ⭐ **MAIOR DATASET**
  - 93,881 registros de treino
  - Pronto para ARIMA, Prophet, LSTM

- **`data/training/CONN-001_train.csv`**
  - 584 registros de treino
  - Dataset menor para testes rápidos

---

**Status:** ✅ **Dados prontos e localizados!**

**Próximo:** Treinar modelos ML usando esses dados!

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

