# 📊 Guia Completo dos Datasets de Treinamento

## Nova Corrente - Demand Forecasting System

---

## 🎯 Visão Geral

Este documento fornece uma análise completa de todos os datasets de treinamento preparados para ML, incluindo estrutura, estatísticas e guias de uso.

---

## 📁 Localização dos Datasets

### Estrutura Completa

```
data/
├── processed/                    ⭐ DADOS PROCESSADOS
│   ├── unified_dataset_with_factors.csv (27.25 MB | 118,082 rows)
│   ├── zenodo_milan_telecom_preprocessed.csv (9.87 MB | 116,257 rows)
│   └── test_dataset_preprocessed.csv (0.05 MB | 730 rows)
│
├── training/                     ⭐ DADOS DE TREINAMENTO (SPLITS)
│   ├── unknown_train.csv (11.61 MB | 93,881 rows) ⭐ MAIOR
│   ├── unknown_test.csv (2.90 MB | 23,471 rows)
│   ├── unknown_full.csv (14.51 MB | 117,352 rows)
│   ├── CONN-001_train.csv (0.06 MB | 584 rows)
│   ├── CONN-001_test.csv (0.02 MB | 146 rows)
│   ├── CONN-001_full.csv (0.08 MB | 730 rows)
│   ├── metadata.json
│   └── training_summary.json
│
└── raw/                          📥 DADOS BRUTOS
    ├── zenodo_milan_telecom/
    │   └── output-step-bsId_1-2023_9_28_12_50_10.csv (28.7 MB | 116,257 rows)
    └── test_dataset/
        └── test_data.csv (37 KB | 730 rows)
```

---

## 📊 Dataset 1: Zenodo Milan Telecom

### 1.1 Dataset Original (Raw)

**Localização:** `data/raw/zenodo_milan_telecom/output-step-bsId_1-2023_9_28_12_50_10.csv`

**Estatísticas:**
- **Tamanho:** 28.7 MB
- **Registros:** 116,257 linhas
- **Colunas:** 38 colunas

**Colunas Principais (Original):**
- `bsId` - Base Station ID (todos = 1)
- `episode` - Episódio do algoritmo (0-41)
- `step` - Passo temporal (0-116,256)
- `loadSMS`, `loadInt`, `loadCalls` - Traffic loads por serviço
- `totalSched` - Total Admitted Traffic Load ⭐ **USE COMO DEMANDA**
- `bsCap` - Base Station Capacity
- `rejectRate*`, `delayRate*` - Taxas de rejeição/delay
- `reward`, `episodeReward` - Rewards do algoritmo

**Características:**
- Dados de 5G network slice resource demand prediction
- 42 episódios do algoritmo de controle de admissão
- Dados simulados/processados (game-theoretic episodes)
- Período: Novembro 2013 - Janeiro 2014 (original MILANO dataset processado)

### 1.2 Dataset Preprocessado

**Localização:** `data/processed/zenodo_milan_telecom_preprocessed.csv`

**Estatísticas:**
- **Tamanho:** 9.87 MB
- **Registros:** 116,257 linhas
- **Colunas:** 9 colunas (schema unificado)

**Estrutura Após Preprocessing:**

| Coluna | Tipo | Valor Exemplo | Origem |
|--------|------|---------------|--------|
| `date` | DateTime | 1970-01-01 00:00:00 | `step` convertido |
| `item_id` | String | "unknown" | Default |
| `quantity` | Float | 0.0 | `totalSched` |
| `cost` | Float | 0.0 | Default |
| `lead_time` | Integer | 14 | Default |
| `item_name` | String | "unknown" | Default |
| `category` | String | "unknown" | Default |
| `site_id` | String | "1" | `bsId` |
| `dataset_source` | String | "zenodo_milan_telecom" | Source marker |

**Observações Importantes:**

⚠️ **Date Conversion:**
- `step` (0-116,256) foi convertido para DateTime usando 1970-01-01 como base
- Resultado: dates de 1970-01-01 a 2024-12-30 (range artificial)
- **Recomendação:** Para análise temporal, considerar usar `step` diretamente ou recalcular datas baseadas no período original (Nov 2013 - Jan 2014)

⚠️ **Quantity Values:**
- Muitos valores são 0.0 no início
- Valores reais começam após alguns steps
- **Recomendação:** Filtrar zeros ou usar apenas valores > 0 para treinamento

### 1.3 Uso do Dataset Zenodo

```python
import pandas as pd
import numpy as np

# Carregar dataset Zenodo preprocessado
df_zenodo = pd.read_csv('data/processed/zenodo_milan_telecom_preprocessed.csv')

# Filtrar zeros (opcional)
df_zenodo = df_zenodo[df_zenodo['quantity'] > 0]

# Preparar para time series
df_zenodo['date'] = pd.to_datetime(df_zenodo['date'])
df_zenodo = df_zenodo.set_index('date').sort_index()

# Extrair série temporal
series = df_zenodo['quantity']

# Estatísticas
print(f"Total: {len(series):,} registros")
print(f"Mean: {series.mean():.2f}")
print(f"Std: {series.std():.2f}")
print(f"Min: {series.min():.2f}")
print(f"Max: {series.max():.2f}")
```

---

## 📊 Dataset 2: Test Dataset

### 2.1 Dataset Original (Raw)

**Localização:** `data/raw/test_dataset/test_data.csv`

**Estatísticas:**
- **Tamanho:** 37 KB
- **Registros:** 730 linhas (2 anos de dados diários)
- **Colunas:** 7 colunas

**Estrutura Original:**

| Coluna | Tipo | Exemplo | Descrição |
|--------|------|---------|-----------|
| `Date` | Date | 2023-01-01 | Data (diária) |
| `Product` | String | "CONN-001" | ID do produto |
| `Order_Demand` | Integer | 7 | Demanda diária (4-10) |
| `Site` | String | "TORRE001" | ID da torre/site |
| `Category` | String | "Conectores" | Categoria |
| `Cost` | Float | 300.0 | Custo unitário |
| `Lead_Time` | Integer | 14 | Tempo de entrega (dias) |

**Características:**
- ✅ **Dados Sintéticos/Guiados:** Criados para teste do pipeline
- ✅ **Período Completo:** 2 anos (730 dias) de 2023-01-01 a 2024-12-30
- ✅ **Sem Gaps:** Dados contínuos para todos os dias
- ✅ **Demanda Realística:** Varia de 4 a 10 unidades/dia
- ✅ **Estrutura Limpa:** Pronto para uso direto

**Estatísticas do Test Dataset:**
- **Mean Demand:** 6.93 unidades/dia
- **Std Demand:** 2.51 unidades
- **Min Demand:** 3 unidades
- **Max Demand:** 11 unidades
- **Lead Time:** 14 dias (fixo)
- **Cost:** 300.0 (fixo)

### 2.2 Dataset Preprocessado

**Localização:** `data/processed/test_dataset_preprocessed.csv`

**Estrutura Após Preprocessing:**

| Coluna | Tipo | Origem |
|--------|------|--------|
| `date` | DateTime | `Date` |
| `item_id` | String | `Product` |
| `quantity` | Float | `Order_Demand` |
| `site_id` | String | `Site` |
| `category` | String | `Category` |
| `cost` | Float | `Cost` |
| `lead_time` | Integer | `Lead_Time` |
| `item_name` | String | Default |
| `dataset_source` | String | "test_dataset" |

**Características:**
- ✅ Mantém todas as informações originais
- ✅ Schema unificado aplicado
- ✅ Time-based features adicionados (year, month, weekday, etc.)

### 2.3 Uso do Test Dataset

```python
# Carregar test dataset
df_test = pd.read_csv('data/raw/test_dataset/test_data.csv')

# Análise básica
print(f"Period: {df_test['Date'].min()} to {df_test['Date'].max()}")
print(f"Days: {len(df_test)}")
print(f"Mean Demand: {df_test['Order_Demand'].mean():.2f}")
print(f"Std Demand: {df_test['Order_Demand'].std():.2f}")

# Preparar para ML
df_test['Date'] = pd.to_datetime(df_test['Date'])
df_test = df_test.set_index('Date').sort_index()
series = df_test['Order_Demand']

# Ideal para:
# - Testes de algoritmos
# - Validação rápida
# - Prototipagem
# - Baseline comparisons
```

---

## 📊 Dataset 3: Unknown (Training Split)

### 3.1 Unknown Train Dataset ⭐ MAIOR

**Localização:** `data/training/unknown_train.csv`

**Estatísticas:**
- **Tamanho:** 11.61 MB
- **Registros:** 93,881 linhas (80% de treino)
- **Colunas:** 31 colunas (9 base + 22 external factors)

**Composição:**
- **98.5%** do Zenodo Milan Telecom (~92,500 registros)
- **0.6%** do Kaggle Retail Inventory (~560 registros)
- **0.6%** do Test Dataset (~560 registros)
- **0.3%** do Kaggle Supply Chain (~260 registros)

**Colunas Disponíveis:**

**Base (9):**
- `date`, `item_id`, `item_name`, `quantity`, `site_id`, `category`, `cost`, `lead_time`, `dataset_source`

**External Factors (22):**
- **Climáticos:** `temperature`, `precipitation`, `humidity`, `extreme_heat`, `heavy_rain`, `high_humidity`
- **Econômicos:** `exchange_rate_brl_usd`, `inflation_rate`, `gdp_growth`, `high_inflation`, `currency_devaluation`
- **Regulatórios:** `5g_coverage`, `regulatory_compliance_date`, `5g_expansion_rate`
- **Operacionais:** `is_holiday`, `is_vacation_period`, `sla_renewal_period`, `weekend`
- **Scores:** `climate_impact`, `economic_impact`, `operational_impact`, `demand_adjustment_factor`

**Características:**
- ✅ **Maior Dataset:** 93,881 registros de treino
- ✅ **Com External Factors:** 22 fatores externos integrados
- ✅ **Schema Unificado:** Pronto para ML direto
- ✅ **Time Series Ready:** Indexado por data

**⚠️ Observação sobre Quantity:**
- Média: 0.0 (devido aos zeros do Zenodo)
- **Recomendação:** Filtrar valores > 0 ou usar apenas dados do test_dataset/corrigir preprocessing

### 3.2 Unknown Test Dataset

**Localização:** `data/training/unknown_test.csv`

**Estatísticas:**
- **Tamanho:** 2.90 MB
- **Registros:** 23,471 linhas (20% de teste)
- **Colunas:** 31 colunas

**Uso:** Para avaliação de modelos ML (validação)

---

## 📊 Dataset 4: CONN-001 (Training Split)

### 4.1 CONN-001 Train Dataset

**Localização:** `data/training/CONN-001_train.csv`

**Estatísticas:**
- **Tamanho:** 0.06 MB
- **Registros:** 584 linhas (80% de treino)
- **Colunas:** 31 colunas
- **Origem:** 100% do test_dataset

**Estatísticas (do metadata.json):**
- **Period:** 2023-01-01 to 2024-12-30
- **Mean Quantity:** 6.93 unidades/dia
- **Std Quantity:** 2.51 unidades
- **Min Quantity:** 3.0 unidades
- **Max Quantity:** 11.0 unidades

**Características:**
- ✅ **Dataset Limpo:** Sem zeros, dados realísticos
- ✅ **Período Completo:** 2 anos de dados diários
- ✅ **Estrutura Limpa:** Pronto para uso direto
- ✅ **Ideal para:** Testes rápidos, prototipagem, baseline

### 4.2 CONN-001 Test Dataset

**Localização:** `data/training/CONN-001_test.csv`

**Estatísticas:**
- **Tamanho:** 0.02 MB
- **Registros:** 146 linhas (20% de teste)
- **Colunas:** 31 colunas

---

## 📊 Dataset 5: Unified Dataset (Completo)

### `data/processed/unified_dataset_with_factors.csv` ⭐ PRINCIPAL

**Estatísticas:**
- **Tamanho:** 27.25 MB
- **Registros:** 118,082 linhas
- **Colunas:** 31 colunas (9 base + 22 external factors)

**Composição Final:**

| Fonte | Registros | Percentual |
|-------|-----------|------------|
| **zenodo_milan_telecom** | 116,257 | 98.5% |
| **test_dataset** | 730 | 0.6% |
| **kaggle_retail_inventory** | 731 | 0.6% |
| **kaggle_supply_chain** | 364 | 0.3% |
| **Total** | **118,082** | **100%** |

**Características:**
- ✅ **Dataset Completo:** Todos os dados mesclados
- ✅ **External Factors:** 22 fatores integrados
- ✅ **Schema Unificado:** Pronto para análise completa
- ✅ **Ideal para:** Análise exploratória, visualizações, análise completa

---

## 🎯 Recomendações de Uso

### Para Treinar Modelos ML (ARIMA, Prophet, LSTM):

**✅ RECOMENDADO:** `data/training/unknown_train.csv`

**Razões:**
- ✅ Maior dataset (93,881 registros)
- ✅ Já dividido train/test
- ✅ Com external factors
- ✅ Pronto para uso direto

**Código:**

```python
# Carregar dados de treino
train_df = pd.read_csv('data/training/unknown_train.csv')
test_df = pd.read_csv('data/training/unknown_test.csv')

# Filtrar zeros (se necessário)
train_df = train_df[train_df['quantity'] > 0]
test_df = test_df[test_df['quantity'] > 0]

# Preparar para time series
train_df['date'] = pd.to_datetime(train_df['date'])
train_df = train_df.set_index('date').sort_index()

# Extrair série temporal
series_train = train_df['quantity']

# Treinar modelos...
```

### Para Testes Rápidos e Prototipagem:

**✅ RECOMENDADO:** `data/training/CONN-001_train.csv`

**Razões:**
- ✅ Dataset menor (584 registros)
- ✅ Dados limpos (sem zeros)
- ✅ Período completo (2 anos)
- ✅ Rápido para iterar

**Código:**

```python
# Dataset menor para testes rápidos
train_small = pd.read_csv('data/training/CONN-001_train.csv')
test_small = pd.read_csv('data/training/CONN-001_test.csv')

# Ideal para:
# - Testes de algoritmos
# - Validação rápida
# - Prototipagem
```

### Para Análise Completa:

**✅ RECOMENDADO:** `data/processed/unified_dataset_with_factors.csv`

**Razões:**
- ✅ Todos os dados unificados
- ✅ Com external factors
- ✅ Análise exploratória completa

---

## 📐 Análise Matemática

### Distribuição de Quantidade

**Para unknown dataset:**
- **Mean:** 0.0 (devido aos zeros do Zenodo)
- **Std:** 0.0
- **Recomendação:** Filtrar zeros ou corrigir preprocessing

**Para CONN-001 dataset:**
- **Mean:** 6.93 unidades/dia
- **Std:** 2.51 unidades
- **Min:** 3.0 unidades
- **Max:** 11.0 unidades
- **Distribuição:** Normalizada e realística

### Análise Temporal

**Unknown Dataset:**
- **Date Range:** 1970-01-01 to 2024-12-30 (artificial devido à conversão de step)
- **Total Days:** ~54 anos (range artificial)
- **Real Period:** Nov 2013 - Jan 2014 (original)

**CONN-001 Dataset:**
- **Date Range:** 2023-01-01 to 2024-12-30
- **Total Days:** 730 dias (2 anos)
- **Realistic:** Dados contínuos sem gaps

---

## 🔍 Problemas Identificados e Soluções

### Problema 1: Zeros no Zenodo Dataset

**Problema:** Muitos valores de `quantity` são 0.0 no dataset unknown.

**Solução:**
```python
# Filtrar zeros
df = df[df['quantity'] > 0]

# Ou usar apenas CONN-001 que não tem zeros
df = pd.read_csv('data/training/CONN-001_train.csv')
```

### Problema 2: Date Range Artificial

**Problema:** Datas do Zenodo começam em 1970 (conversão de step).

**Solução:**
```python
# Opção 1: Recalcular datas baseadas no período original
# Nov 2013 - Jan 2014 = ~60 dias
start_date = pd.to_datetime('2013-11-01')
df['date'] = start_date + pd.to_timedelta(df['step'], unit='D')

# Opção 2: Usar step diretamente como índice temporal
df['time_index'] = df['step']
df = df.set_index('time_index')
```

### Problema 3: Item ID = "unknown"

**Problema:** Todos os registros do Zenodo têm item_id = "unknown".

**Solução:**
```python
# Criar item_id baseado em site_id + episode
df['item_id'] = df['site_id'].astype(str) + '_ep' + df['episode'].astype(str)
```

---

## ✅ Resumo Final

### Datasets Recomendados para ML Training:

1. **`unknown_train.csv`** ⭐ **PRINCIPAL**
   - 93,881 registros
   - 31 colunas com external factors
   - 11.61 MB
   - **USE ESTE PARA TREINAR MODELOS ML COMPLETOS**

2. **`CONN-001_train.csv`** ⭐ **PARA TESTES**
   - 584 registros
   - 31 colunas
   - 0.06 MB
   - **USE ESTE PARA TESTES RÁPIDOS E PROTOPIPAGEM**

3. **`unified_dataset_with_factors.csv`** ⭐ **PARA ANÁLISE**
   - 118,082 registros
   - 31 colunas
   - 27.25 MB
   - **USE ESTE PARA ANÁLISE EXPLORATÓRIA COMPLETA**

---

**Status:** ✅ **Todos os datasets prontos e documentados!**

**Próximo:** Treinar modelos ML usando os datasets de treinamento!

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

