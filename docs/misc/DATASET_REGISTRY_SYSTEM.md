# 📋 Sistema de Registro Unificado de Datasets

## Nova Corrente - Demand Forecasting System

---

## 🎯 Visão Geral

Sistema completo de registro, validação e configuração automática de datasets descobertos e baixados.

---

## 🚀 Funcionalidades

### 1. **Registro Centralizado de Datasets**

**Arquivo:** `src/utils/dataset_registry.py`

✅ Registro unificado de todos os datasets  
✅ Rastreamento de status (discovered, downloaded, validated, etc.)  
✅ Metadados completos de cada dataset  
✅ Histórico de atualizações

**Estrutura do Registry:**
```json
{
  "datasets": {
    "zenodo_12345": {
      "id": "zenodo_12345",
      "registered_at": "2024-01-01T00:00:00",
      "last_updated": "2024-01-02T00:00:00",
      "status": "validated",
      "source": "zenodo",
      "title": "Dataset Title",
      "url": "https://zenodo.org/record/12345",
      "description": "...",
      "keywords": ["telecom", "demand"],
      "doi": "10.1234/example"
    }
  },
  "metadata": {
    "version": "1.0",
    "created": "2024-01-01T00:00:00",
    "last_updated": "2024-01-02T00:00:00"
  }
}
```

---

### 2. **Descoberta e Registro Automático**

**Arquivo:** `scripts/auto_register_discovered_datasets.py`

✅ Registra datasets descobertos automaticamente  
✅ Gera IDs únicos baseados na fonte  
✅ Extrai metadados de múltiplas fontes  
✅ Gera configurações automáticas opcionais

**Uso:**
```bash
# Registrar datasets descobertos
python scripts/auto_register_discovered_datasets.py

# Com geração automática de configs
python scripts/auto_register_discovered_datasets.py --auto-config

# Buscar e registrar em um passo
python scripts/auto_register_discovered_datasets.py --keywords telecom demand brazil --auto-config
```

---

### 3. **Validação Automática de Datasets**

**Arquivo:** `scripts/validate_all_datasets.py`

✅ Valida arquivos CSV baixados  
✅ Verifica estrutura e schema  
✅ Detecta valores nulos e problemas  
✅ Gera relatório detalhado

**Validações:**
- ✅ Arquivo existe
- ✅ Arquivo não está vazio
- ✅ Possui colunas
- ✅ Possui linhas
- ✅ Colunas esperadas presentes (date, item_id, quantity)
- ✅ Percentual aceitável de valores nulos
- ✅ Tipos de dados corretos

**Uso:**
```bash
# Validar todos os datasets
python scripts/validate_all_datasets.py

# Validar e atualizar registry
python scripts/validate_all_datasets.py --update-registry

# Salvar relatório customizado
python scripts/validate_all_datasets.py --output data/registry/my_validation.json
```

---

### 4. **Pipeline Inteligente de Busca e Download**

**Arquivo:** `scripts/smart_dataset_fetch.py`

✅ Pipeline completo: descobrir → registrar → baixar → validar → configurar  
✅ Processamento automático inteligente  
✅ Limite de datasets configurável  
✅ Integração com Scrapy e métodos padrão

**Fluxo:**
1. **Descoberta** - Busca datasets em todas as fontes
2. **Registro** - Registra datasets descobertos
3. **Download** - Baixa datasets automaticamente
4. **Validação** - Valida datasets baixados
5. **Configuração** - Gera configs automaticamente

**Uso:**
```bash
# Pipeline completo com todas as etapas
python scripts/smart_dataset_fetch.py --auto-download --auto-validate --auto-config

# Pipeline parcial
python scripts/smart_dataset_fetch.py --auto-download

# Limitar quantidade de datasets
python scripts/smart_dataset_fetch.py --max-datasets 5 --auto-download
```

---

## 📊 APIs e Classes

### `DatasetRegistry`

**Métodos principais:**

```python
# Registrar dataset
registry.register_dataset(dataset_id, dataset_info, source='zenodo')

# Atualizar status
registry.update_dataset_status(dataset_id, status='downloaded')

# Obter dataset
dataset = registry.get_dataset(dataset_id)

# Listar datasets
datasets = registry.list_datasets(status='discovered', source='zenodo')

# Registrar datasets descobertos
registry.discover_and_register(discovered_datasets)

# Validar arquivo
validation = registry.validate_dataset_file(dataset_id, file_path)

# Gerar configuração automática
config = registry.auto_generate_config(dataset_id)

# Exportar configurações
configs = registry.export_configs()
```

---

## 🔍 Validação de Datasets

### Critérios de Validação

1. **Arquivo existe**
   - ❌ Erro se arquivo não encontrado

2. **Estrutura básica**
   - ✅ Arquivo não vazio
   - ✅ Possui colunas
   - ✅ Possui linhas

3. **Colunas esperadas**
   - ⚠️  Aviso se colunas esperadas ausentes:
     - `date` (ou variações: Date, Time, Timestamp, Step)
     - `item_id` (ou variações: Item, Product, SKU, ID)
     - `quantity` (ou variações: Quantity, Demand, Order, Count)

4. **Qualidade de dados**
   - ⚠️  Aviso se >10% de datas nulas
   - ⚠️  Aviso se colunas críticas com muitos nulos

### Resultado de Validação

```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Missing expected columns: ['item_id']"],
  "info": {
    "rows_checked": 1000,
    "columns": ["Date", "Product", "Quantity"],
    "column_count": 3,
    "dtypes": {"Date": "object", "Product": "object", "Quantity": "int64"},
    "missing_values": {"Date": 0, "Product": 5, "Quantity": 2},
    "file_size_mb": 2.5
  }
}
```

---

## 🎯 Status de Datasets

### Status Possíveis

- `discovered` - Dataset descoberto, ainda não baixado
- `downloaded` - Dataset baixado com sucesso
- `download_failed` - Falha no download
- `validated` - Dataset validado e pronto para uso
- `validation_failed` - Falha na validação
- `processed` - Dataset processado e pronto para ML

---

## 📝 Geração Automática de Configurações

### Inferência de Colunas

O sistema tenta inferir automaticamente o mapeamento de colunas:

**Coluna de Data:**
- Busca por: `date`, `time`, `timestamp`, `step`

**Coluna de Item:**
- Busca por: `item`, `product`, `sku`, `id`

**Coluna de Quantidade:**
- Busca por: `quantity`, `demand`, `order`, `count`, `total`, `value`

### Configuração Gerada

```json
{
  "zenodo_12345": {
    "name": "Dataset Title",
    "source": "zenodo",
    "url": "https://zenodo.org/record/12345",
    "description": "...",
    "columns_mapping": {
      "date": "Date",
      "item_id": "Product_ID",
      "quantity": "Demand"
    },
    "preprocessing_notes": "Auto-generated from discovery. Validation: {...}"
  }
}
```

---

## 🔧 Integração com Pipeline Principal

### 1. Descoberta → Registro

```bash
# Descobrir e registrar
python scripts/enhance_dataset_search.py --keywords telecom brazil
python scripts/auto_register_discovered_datasets.py --discovered-file data/raw/discovered_datasets.json
```

### 2. Download → Validação

```bash
# Baixar e validar
python scripts/fetch_and_structure_all.py
python scripts/validate_all_datasets.py --update-registry
```

### 3. Pipeline Completo

```bash
# Tudo em um comando
python scripts/smart_dataset_fetch.py --auto-download --auto-validate --auto-config
```

---

## 📊 Relatórios e Estatísticas

### Relatório de Validação

**Arquivo:** `data/registry/validation_report.json`

```json
{
  "valid": [
    {
      "dataset_id": "zenodo_12345",
      "file": "data/raw/zenodo_12345/data.csv",
      "info": {...}
    }
  ],
  "invalid": [
    {
      "dataset_id": "anatel_123",
      "file": "data/raw/anatel_123/data.csv",
      "errors": ["File is empty"],
      "warnings": []
    }
  ],
  "warnings": [...],
  "statistics": {
    "valid": 15,
    "invalid": 2,
    "with_warnings": 3,
    "no_files": 1
  }
}
```

---

## 🎯 Casos de Uso

### Caso 1: Descobrir Novos Datasets

```bash
# Buscar e registrar
python scripts/auto_register_discovered_datasets.py --keywords telecom demand forecast brazil

# Revisar registry
python -c "from src.utils.dataset_registry import DatasetRegistry; r = DatasetRegistry(); print(r.list_datasets())"
```

### Caso 2: Validar Datasets Baixados

```bash
# Validar todos
python scripts/validate_all_datasets.py --update-registry

# Verificar resultados
cat data/registry/validation_report.json
```

### Caso 3: Pipeline Completo Automático

```bash
# Descobrir, baixar, validar e configurar
python scripts/smart_dataset_fetch.py \
  --keywords telecom demand brazil \
  --auto-download \
  --auto-validate \
  --auto-config \
  --max-datasets 10
```

---

## 📁 Estrutura de Arquivos

```
data/
├── registry/
│   ├── datasets_registry.json          # Registry principal
│   └── validation_report.json          # Relatório de validação
├── raw/
│   ├── discovered_datasets.json        # Datasets descobertos
│   └── {dataset_id}/                   # Datasets baixados
│       └── *.csv

config/
└── auto_generated_configs.json        # Configs gerados automaticamente

src/
└── utils/
    └── dataset_registry.py            # Classe principal

scripts/
├── auto_register_discovered_datasets.py
├── validate_all_datasets.py
└── smart_dataset_fetch.py
```

---

## ✅ Checklist de Implementação

- [x] Sistema de registro centralizado
- [x] Descoberta e registro automático
- [x] Validação automática de datasets
- [x] Geração automática de configurações
- [x] Pipeline inteligente completo
- [x] Relatórios e estatísticas
- [x] Integração com pipeline principal
- [x] Documentação completa

---

## 📊 Estatísticas do Sistema

### Métricas

- **Datasets registrados:** Consultar registry
- **Taxa de validação:** Ver validation_report
- **Configs gerados:** Ver auto_generated_configs.json

### Comandos Úteis

```bash
# Contar datasets por status
python -c "from src.utils.dataset_registry import DatasetRegistry; r = DatasetRegistry(); datasets = r.list_datasets(); print({s: sum(1 for d in datasets if d.get('status') == s) for s in set(d.get('status') for d in datasets)})"

# Listar datasets por fonte
python -c "from src.utils.dataset_registry import DatasetRegistry; r = DatasetRegistry(); datasets = r.list_datasets(); print({s: sum(1 for d in datasets if d.get('source') == s) for s in set(d.get('source') for d in datasets)})"
```

---

**Status:** ✅ **SISTEMA DE REGISTRO E VALIDAÇÃO COMPLETO**

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

