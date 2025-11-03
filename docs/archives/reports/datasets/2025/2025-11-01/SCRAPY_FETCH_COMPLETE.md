# 🕷️ Sistema Completo de Busca e Download com Scrapy

## Nova Corrente - Demand Forecasting System

---

## 📋 Visão Geral

Sistema completo de descoberta, busca e download de datasets estruturados usando Scrapy e APIs de múltiplas fontes.

---

## 🚀 Funcionalidades Implementadas

### 1. **Integração Scrapy com Pipeline Principal**

**Arquivo:** `src/pipeline/scrapy_integration.py`

✅ Integração completa dos spiders Scrapy com o pipeline de download  
✅ Execução automática de spiders quando necessário  
✅ Fallback para métodos manuais se Scrapy falhar  
✅ Rastreamento de resultados de download

**Uso:**
```python
from src.pipeline.scrapy_integration import ScrapyIntegration

integration = ScrapyIntegration()
results = integration.run_all_scrapy_datasets()
```

---

### 2. **Busca Inteligente de Datasets**

**Arquivo:** `scripts/enhance_dataset_search.py`

✅ Busca em Zenodo por query  
✅ Busca em GitHub por repositórios  
✅ Busca no Kaggle (requer autenticação)  
✅ Descoberta automática de datasets Anatel  
✅ Validação de repositórios para arquivos de dados

**Funcionalidades:**
- `search_zenodo()` - Busca datasets no Zenodo
- `search_github()` - Busca repositórios GitHub
- `search_kaggle()` - Busca datasets Kaggle
- `discover_anatel_datasets()` - Descobre datasets Anatel
- `suggest_datasets()` - Busca em múltiplas fontes
- `save_discovered_datasets()` - Salva resultados

**Uso:**
```bash
# Buscar datasets
python scripts/enhance_dataset_search.py --keywords telecom demand forecast brazil

# Resultados salvos em: data/raw/discovered_datasets.json
```

---

### 3. **Pipeline Completo de Busca e Download**

**Arquivo:** `scripts/fetch_and_structure_all.py`

✅ Pipeline completo: descoberta → download → estruturação  
✅ Integração de todos os métodos de download  
✅ Relatórios detalhados de sucesso/falha  
✅ Verificação de arquivos baixados

**Execução:**
```bash
python scripts/fetch_and_structure_all.py
```

**Fluxo:**
1. **Descoberta** - Busca datasets em todas as fontes
2. **Download Scrapy** - Baixa datasets que requerem scraping
3. **Download Padrão** - Baixa datasets via APIs/URLs diretas
4. **Verificação** - Confirma arquivos baixados

---

## 📦 Scripts Disponíveis

### Script 1: `scripts/fetch_all_datasets_scrapy.py`

**Propósito:** Executar todos os spiders Scrapy configurados

**Uso:**
```bash
python scripts/fetch_all_datasets_scrapy.py
```

**Funcionalidades:**
- Identifica datasets que requerem scraping
- Executa spiders apropriados
- Salva metadados de downloads
- Gera relatório de sucesso/falha

---

### Script 2: `scripts/enhance_dataset_search.py`

**Propósito:** Buscar e descobrir novos datasets estruturados

**Uso:**
```bash
# Busca padrão (telecom, demand, forecast)
python scripts/enhance_dataset_search.py

# Busca customizada
python scripts/enhance_dataset_search.py --keywords mobile broadband network

# Salvar em arquivo específico
python scripts/enhance_dataset_search.py --output data/raw/my_discoveries.json
```

**Fontes de Busca:**
- Zenodo (API)
- GitHub (API search)
- Kaggle (API, requer token)
- Anatel/Data Basis (web scraping)

---

### Script 3: `scripts/fetch_and_structure_all.py`

**Propósito:** Pipeline completo de descoberta e download

**Uso:**
```bash
python scripts/fetch_and_structure_all.py
```

**Executa:**
1. Descoberta de datasets
2. Download via Scrapy
3. Download via métodos padrão
4. Verificação e relatório

---

## 🔧 Integração com Pipeline Principal

### Modificação em `download_datasets.py`

O método `download_all_datasets()` agora usa automaticamente Scrapy quando `download_method == 'scrape'`:

```python
elif download_method == 'scrape':
    # Use Scrapy integration for scraping
    from src.pipeline.scrapy_integration import ScrapyIntegration
    scrapy_integration = ScrapyIntegration(config_path=self.config_path)
    success = scrapy_integration.run_scrapy_spider(dataset_id, dataset_info)
    
    if not success:
        # Fallback to manual scraping methods
        ...
```

---

## 📊 Estrutura de Dados Descobertos

### Formato JSON (`discovered_datasets.json`)

```json
{
  "zenodo": [
    {
      "id": "12345",
      "title": "Dataset Title",
      "doi": "10.1234/example",
      "url": "https://zenodo.org/record/12345",
      "csv_file": "https://zenodo.org/record/12345/files/data.csv",
      "creators": ["Author Name"],
      "description": "...",
      "keywords": ["telecom", "demand"],
      "publication_date": "2024-01-01"
    }
  ],
  "github": [
    {
      "id": 12345,
      "name": "repo-name",
      "full_name": "user/repo-name",
      "url": "https://github.com/user/repo-name",
      "description": "...",
      "stars": 42,
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "kaggle": [
    {
      "ref": "user/dataset-name",
      "title": "Dataset Title",
      "url": "https://www.kaggle.com/datasets/user/dataset-name",
      "size": "123MB",
      "download_count": 1000
    }
  ],
  "anatel": [
    {
      "title": "Dataset Title",
      "url": "https://data-basis.org/dataset/...",
      "source": "anatel"
    }
  ]
}
```

---

## 🎯 Casos de Uso

### Caso 1: Buscar Novos Datasets

```bash
# Buscar datasets relacionados a telecom no Brasil
python scripts/enhance_dataset_search.py --keywords telecom brazil mobile

# Resultados em: data/raw/discovered_datasets.json
```

### Caso 2: Download Automático via Scrapy

```bash
# Executar todos os spiders Scrapy
python scripts/fetch_all_datasets_scrapy.py

# Ou usar integração direta
python -c "from src.pipeline.scrapy_integration import ScrapyIntegration; ScrapyIntegration().run_all_scrapy_datasets()"
```

### Caso 3: Pipeline Completo

```bash
# Descoberta + Download + Estruturação
python scripts/fetch_and_structure_all.py
```

---

## 🔍 Detalhes Técnicos

### Zenodo Search

- **API:** `https://zenodo.org/api/records`
- **Parâmetros:** query, type=dataset, size, sort
- **Campos extraídos:** id, title, doi, url, files, creators, description

### GitHub Search

- **API:** `https://api.github.com/search/repositories`
- **Query:** `{keywords} dataset`
- **Validação:** Verifica se repositório contém arquivos CSV/JSON
- **Limitação:** Rate limit (requer token para mais resultados)

### Kaggle Search

- **API:** Kaggle API (requer autenticação)
- **Biblioteca:** `kaggle` Python package
- **Configuração:** `~/.kaggle/kaggle.json`

### Anatel Discovery

- **Método:** Web scraping do Data Basis
- **URL:** `https://data-basis.org/datasets`
- **Limitação:** 20 datasets por busca

---

## 📝 Metadados e Logging

### Metadados de Download

**Arquivo:** `data/raw/download_metadata.json`

Armazenado automaticamente pelos pipelines Scrapy.

### Logs

Todos os scripts geram logs detalhados:
- Informações de busca
- Status de downloads
- Erros e warnings
- Resumos finais

---

## 🚀 Próximos Passos

### Melhorias Planejadas

1. **Auto-configuração de Novos Datasets**
   - Detectar automaticamente estrutura de datasets descobertos
   - Gerar configurações para `datasets_config.json`

2. **Validação Automática**
   - Validar datasets baixados antes de processar
   - Verificar schema e qualidade

3. **Notificações**
   - Alertas para novos datasets encontrados
   - Notificações de atualizações

4. **Dashboard**
   - Interface visual para descoberta
   - Monitoramento de downloads
   - Estatísticas de uso

---

## ✅ Checklist de Implementação

- [x] Integração Scrapy com pipeline principal
- [x] Busca em Zenodo implementada
- [x] Busca em GitHub implementada
- [x] Busca no Kaggle implementada
- [x] Descoberta Anatel implementada
- [x] Pipeline completo de busca e download
- [x] Scripts de execução criados
- [x] Documentação completa

---

## 📊 Estatísticas

### Datasets Configurados: 18
### Spiders Scrapy: 5
### Fontes de Busca: 4 (Zenodo, GitHub, Kaggle, Anatel)

---

**Status:** ✅ **SISTEMA COMPLETO DE BUSCA E DOWNLOAD IMPLEMENTADO**

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**


