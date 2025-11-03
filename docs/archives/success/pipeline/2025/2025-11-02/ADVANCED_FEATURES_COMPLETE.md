# 🚀 Funcionalidades Avançadas - Sistema Completo

## Nova Corrente - Demand Forecasting System

---

## 📋 Visão Geral

Sistema completo de funcionalidades avançadas para processamento inteligente de datasets, incluindo indexação temporal, parsing avançado de PDFs, dashboard de status e sistema de retry.

---

## 🎯 Funcionalidades Implementadas

### 1. **Indexação Temporal para Datasets sem Data**

**Arquivo:** `src/utils/temporal_indexing.py`

✅ Cria timestamps sintéticos para datasets sem coluna de data  
✅ Múltiplas estratégias de indexação (order, pattern, external)  
✅ Features temporais automáticas (year, month, weekday, etc.)  
✅ Encoding cíclico para ML (sin/cos transformations)

**Estratégias:**
- **Order-based**: Baseado na ordem das linhas
- **Pattern-based**: Baseado em padrões detectados
- **External**: Merge com dados externos que têm timestamps

**Uso:**
```python
from src.utils.temporal_indexing import TemporalIndexer

indexer = TemporalIndexer(base_date='2022-01-01', frequency='D')
df_with_dates = indexer.create_index_from_order(df)

# Com features temporais
df_enhanced = indexer.enhance_with_temporal_features(df_with_dates)
```

---

### 2. **Parser Avançado de PDFs**

**Arquivo:** `src/utils/advanced_pdf_parser.py`

✅ Suporte para múltiplas bibliotecas (pdfplumber, tabula, camelot, PyPDF2)  
✅ Auto-detecção do melhor parser  
✅ Estratégia combinada para máxima extração  
✅ Limpeza automática de dados extraídos

**Parsers Suportados:**
- **pdfplumber**: Extração precisa de tabelas
- **tabula-py**: Extração de tabelas em PDFs complexos
- **camelot**: Extração de tabelas com bordas
- **PyPDF2**: Fallback para extração de texto

**Uso:**
```python
from src.utils.advanced_pdf_parser import AdvancedPDFParser

parser = AdvancedPDFParser()

# Parsear com estratégia automática
df = parser.parse_pdf(pdf_path, strategy='auto')

# Parsear com parser específico
df = parser.parse_pdf(pdf_path, strategy='pdfplumber')

# Extrair todas as tabelas
csv_files = parser.extract_tables_from_pdf(pdf_path, output_dir)
```

---

### 3. **Dashboard de Status do Sistema**

**Arquivo:** `src/utils/system_status_dashboard.py`

✅ Status completo de datasets (registrados, baixados, validados)  
✅ Status do pipeline (download, preprocess, merge, external factors)  
✅ Status de armazenamento (tamanhos, contagens)  
✅ Health check do sistema

**Status Incluídos:**
- **Datasets**: Total, por status, por fonte, download/validation status
- **Pipeline**: Prontidão de cada etapa, progresso
- **Storage**: Tamanhos de dados brutos/processados
- **Health**: Estado geral e componentes

**Uso:**
```bash
# Exibir dashboard
python scripts/show_system_status.py

# Salvar relatório
python scripts/show_system_status.py --save --output data/registry/system_status.json
```

**Dashboard Exemplo:**
```
================================================================================
SYSTEM STATUS DASHBOARD
================================================================================
Timestamp: 2024-01-01T00:00:00

--------------------------------------------------------------------------------
DATASETS STATUS
--------------------------------------------------------------------------------
Total Registered: 18
By Status:
  discovered: 5
  downloaded: 10
  validated: 8
By Source:
  kaggle: 8
  zenodo: 4
  anatel: 3
  github: 3

Download Status:
  Downloaded: 10
  Not Downloaded: 5
  Failed: 3

--------------------------------------------------------------------------------
PIPELINE STATUS
--------------------------------------------------------------------------------
Download: ✓ (13 datasets)
Preprocess: ✓ (10 preprocessed, 3 pending)
Merge: ✓ (Unified dataset exists)
External Factors: ✓ (Enriched dataset exists)

--------------------------------------------------------------------------------
STORAGE STATUS
--------------------------------------------------------------------------------
Raw Data: 1250.50 MB (13 datasets)
Processed Data: 850.25 MB (10 datasets)
Total: 2100.75 MB

--------------------------------------------------------------------------------
SYSTEM HEALTH
--------------------------------------------------------------------------------
Overall: HEALTHY

Components:
  registry: ✓
  raw_data_dir: ✓
  processed_data_dir: ✓
  config_file: ✓
================================================================================
```

---

### 4. **Sistema de Retry e Recuperação**

**Arquivo:** `src/utils/retry_handler.py`

✅ Retry automático com backoff exponencial  
✅ Jitter aleatório para evitar thundering herd  
✅ Estratégias de recuperação customizáveis  
✅ Handlers especializados (download, file operations)

**Características:**
- **Backoff Exponencial**: Delay cresce exponencialmente
- **Jitter**: Adiciona aleatoriedade para evitar sincronização
- **Max Delay**: Limita delay máximo
- **Callbacks**: Funções chamadas após cada falha

**Uso:**
```python
from src.utils.retry_handler import RetryHandler, retry_with_recovery

# Retry básico
handler = RetryHandler(max_retries=3, base_delay=1.0)
result = handler.retry(exceptions=(ConnectionError,))(download_func)(url)

# Com decorator
@handler.retry(exceptions=(Exception,))
def risky_operation():
    # ...
    pass

# Com recuperação
@retry_with_recovery(
    max_retries=3,
    recovery_strategies=[fallback_strategy1, fallback_strategy2]
)
def critical_operation():
    # ...
    pass

# Handlers especializados
from src.utils.retry_handler import DownloadRetryHandler, FileOperationRetryHandler

download_handler = DownloadRetryHandler(max_retries=3)
file_handler = FileOperationRetryHandler(max_retries=3)

# Download com retry
result = download_handler.download_with_retry(download_func, url)

# Operações de arquivo com retry
data = file_handler.read_with_retry(file_path, pd.read_csv)
file_handler.write_with_retry(file_path, data, pd.DataFrame.to_csv)
```

---

## 🔧 Integrações

### 1. **Integração com Preprocessing**

O sistema de indexação temporal pode ser usado no preprocessing:

```python
from src.utils.temporal_indexing import process_dataset_without_date

# No preprocess_datasets.py
if 'date' not in df.columns:
    config = {
        'temporal_indexing': {
            'strategy': 'order',
            'base_date': '2022-01-01',
            'frequency': 'D',
            'add_temporal_features': True
        }
    }
    df = process_dataset_without_date(dataset_id, df, config, output_path)
```

### 2. **Integração com Download**

O sistema de retry pode ser usado em downloads:

```python
from src.utils.retry_handler import DownloadRetryHandler

handler = DownloadRetryHandler(max_retries=3)

# No download_datasets.py
success = handler.download_with_retry(
    self.download_direct_url,
    url,
    output_path
)
```

### 3. **Integração com PDF Parsing**

O parser avançado pode ser usado em preprocessing:

```python
from src.utils.advanced_pdf_parser import AdvancedPDFParser

parser = AdvancedPDFParser()

# No download ou preprocessing
if file_path.suffix.lower() == '.pdf':
    df = parser.parse_pdf(file_path, strategy='auto')
    df.to_csv(output_csv_path, index=False)
```

---

## 📊 Scripts Disponíveis

### Script 1: `scripts/show_system_status.py`

**Propósito:** Exibir dashboard de status do sistema

**Uso:**
```bash
# Exibir no terminal
python scripts/show_system_status.py

# Salvar em JSON
python scripts/show_system_status.py --save
```

---

## 🎯 Casos de Uso

### Caso 1: Processar Dataset sem Data

```python
from src.utils.temporal_indexing import TemporalIndexer

indexer = TemporalIndexer(base_date='2022-01-01')
df = indexer.create_index_from_order(df, sort_by=['item_id'])
df = indexer.enhance_with_temporal_features(df)
```

### Caso 2: Extrair Dados de PDF

```python
from src.utils.advanced_pdf_parser import AdvancedPDFParser

parser = AdvancedPDFParser()
df = parser.parse_pdf('data/raw/internet_aberta_forecast/forecast.pdf')
df.to_csv('data/raw/internet_aberta_forecast/forecast.csv', index=False)
```

### Caso 3: Download com Retry

```python
from src.utils.retry_handler import DownloadRetryHandler

handler = DownloadRetryHandler(max_retries=5)
success = handler.download_with_retry(download_func, url, path)
```

### Caso 4: Verificar Status do Sistema

```bash
python scripts/show_system_status.py
```

---

## 📁 Estrutura de Arquivos

```
src/utils/
├── temporal_indexing.py           ⭐ NOVO
├── advanced_pdf_parser.py         ⭐ NOVO
├── system_status_dashboard.py     ⭐ NOVO
└── retry_handler.py               ⭐ NOVO

scripts/
└── show_system_status.py           ⭐ NOVO

docs/
└── ADVANCED_FEATURES_COMPLETE.md   ⭐ NOVO
```

---

## ✅ Checklist de Implementação

- [x] Sistema de indexação temporal
- [x] Parser avançado de PDFs
- [x] Dashboard de status
- [x] Sistema de retry e recuperação
- [x] Integrações com pipeline principal
- [x] Scripts de execução
- [x] Documentação completa

---

## 📊 Benefícios

### Indexação Temporal
- ✅ Processa datasets sem timestamps
- ✅ Cria features temporais automaticamente
- ✅ Suporta múltiplas estratégias

### Parser de PDFs
- ✅ Extrai dados de PDFs complexos
- ✅ Múltiplas bibliotecas para máxima compatibilidade
- ✅ Limpeza automática de dados

### Dashboard
- ✅ Visão completa do sistema
- ✅ Identificação rápida de problemas
- ✅ Monitoramento de progresso

### Retry Handler
- ✅ Maior resiliência a falhas
- ✅ Recuperação automática
- ✅ Reduz necessidade de intervenção manual

---

**Status:** ✅ **FUNCIONALIDADES AVANÇADAS COMPLETAS**

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

