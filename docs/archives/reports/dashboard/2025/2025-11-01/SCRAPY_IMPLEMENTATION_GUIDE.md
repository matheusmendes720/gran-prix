# 🕷️ Guia Completo de Implementação Scrapy

## Nova Corrente - Demand Forecasting System

---

## 📋 Visão Geral

Este documento detalha a implementação completa de spiders Scrapy para scraping de datasets de múltiplas fontes, especialmente focada em dados brasileiros de telecomunicações.

---

## 🕷️ Spiders Implementados

### 1. **AnatelSpider** - Dados Regulatórios Anatel

**Arquivo:** `src/scrapy/scrapy_spiders/anatel_spider.py`

**Funcionalidades:**
- ✅ Scraping da página Data Basis (Base dos Dados)
- ✅ Extração de links CSV via parsing HTML
- ✅ Parsing de scripts JavaScript (React/Next.js)
- ✅ Fallback para API Data Basis
- ✅ Download direto de arquivos CSV

**Uso:**
```bash
python scripts/run_scrapy_spider.py anatel \
  --dataset-id anatel_mobile_brazil \
  --url "https://data-basis.org/dataset/d3c86a88-d9a4-4c0-bdec-08ab61e8f63c"
```

**Estrutura:**
- `parse_dataset_page()` - Parse da página do dataset
- `download_csv()` - Download do arquivo CSV
- Suporte para React/Next.js (extração de JSON embutido)
- Fallback para API Data Basis

---

### 2. **InternetAbertaSpider** - Relatórios e Forecasts

**Arquivo:** `src/scrapy/scrapy_spiders/internet_aberta_spider.py`

**Funcionalidades:**
- ✅ Download direto de PDFs
- ✅ Busca de links PDF em páginas web
- ✅ Suporte para URLs diretas de PDF
- ✅ Validação de arquivos baixados

**Uso:**
```bash
python scripts/run_scrapy_spider.py internet_aberta \
  --dataset-id internet_aberta_forecast \
  --url "https://internetaberta.com.br/wp-content/uploads/2024/05/Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf"
```

**Estrutura:**
- `parse_page()` - Parse de páginas web para encontrar PDFs
- `download_pdf()` - Download direto de PDFs
- Suporte para forecasts e relatórios

---

### 3. **SpringerSpider** - Artigos Científicos

**Arquivo:** `src/scrapy/scrapy_spiders/springer_spider.py`

**Funcionalidades:**
- ✅ Parse de artigos científicos Springer
- ✅ Extração de links para datasets suplementares
- ✅ Busca em seções "Materials and Methods" e "Data Availability"
- ✅ Detecção de links para repositórios externos (Zenodo, GitHub, Figshare)
- ✅ Download automático de arquivos de dados (CSV, ZIP, JSON)

**Uso:**
```bash
python scripts/run_scrapy_spider.py springer \
  --dataset-id springer_digital_divide \
  --url "https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-024-00508-8"
```

**Estrutura:**
- `parse_article()` - Parse do artigo científico
- `download_data()` - Download de arquivos de dados
- Detecção inteligente de links de dados
- Suporte para múltiplos formatos (CSV, ZIP, JSON)

---

### 4. **GitHubSpider** - Repositórios GitHub

**Arquivo:** `src/scrapy/scrapy_spiders/github_spider.py`

**Funcionalidades:**
- ✅ Parse de repositórios GitHub
- ✅ Conversão automática de URLs blob → raw
- ✅ Busca recursiva em diretórios de dados
- ✅ Download de múltiplos formatos (CSV, JSON, ZIP, Parquet, TSV, XLSX)

**Uso:**
```bash
python scripts/run_scrapy_spider.py github \
  --dataset-id github_5g3e \
  --url "https://github.com/cedric-cnam/5G3E-dataset"
```

**Estrutura:**
- `parse_repository()` - Parse do repositório GitHub
- `download_file()` - Download de arquivos
- Conversão automática blob → raw
- Busca recursiva em subdiretórios

---

## 📦 Items e Estrutura de Dados

### Items Definidos

**Arquivo:** `src/scrapy/scrapy_spiders/items.py`

#### 1. **DatasetItem** (Base)
```python
class DatasetItem(scrapy.Item):
    dataset_id = scrapy.Field()
    file_path = scrapy.Field()
    url = scrapy.Field()
    size = scrapy.Field()
    filename = scrapy.Field()
    file_type = scrapy.Field()
    download_date = scrapy.Field()
```

#### 2. **AnatelItem** (Específico Anatel)
```python
class AnatelItem(DatasetItem):
    region = scrapy.Field()
    technology = scrapy.Field()
    subscribers = scrapy.Field()
    period = scrapy.Field()
```

#### 3. **ZenodoItem** (Específico Zenodo)
```python
class ZenodoItem(DatasetItem):
    record_id = scrapy.Field()
    record_title = scrapy.Field()
    authors = scrapy.Field()
    description = scrapy.Field()
```

#### 4. **RepositoryItem** (Links de Repositórios)
```python
class RepositoryItem(scrapy.Item):
    repository_url = scrapy.Field()
    article_url = scrapy.Field()
    dataset_id = scrapy.Field()
    type = scrapy.Field()
```

---

## 🔧 Pipelines

### 1. **DatasetMetadataPipeline**

**Arquivo:** `src/scrapy/scrapy_spiders/pipelines.py`

**Funcionalidades:**
- ✅ Salva metadados de todos os downloads
- ✅ Rastreia URLs, tamanhos, datas
- ✅ Armazena em `data/raw/download_metadata.json`

**Estrutura de Metadados:**
```json
{
  "dataset_id": [
    {
      "file_path": "data/raw/dataset/file.csv",
      "url": "https://...",
      "filename": "file.csv",
      "size": 12345,
      "file_type": "csv",
      "download_date": "2025-10-31T...",
      "spider": "anatel"
    }
  ]
}
```

---

### 2. **ValidateFilePipeline**

**Funcionalidades:**
- ✅ Valida arquivos baixados
- ✅ Verifica existência e tamanho
- ✅ Valida tipos de arquivo
- ✅ Remove items inválidos

---

## ⚙️ Configurações

### Settings do Scrapy

**Arquivo:** `src/scrapy/scrapy_spiders/settings.py`

**Configurações Principais:**
- ✅ `ROBOTSTXT_OBEY = False` (para scraping permitido)
- ✅ `DOWNLOAD_DELAY = 1` (respeito aos sites)
- ✅ `AUTOTHROTTLE_ENABLED = True` (controle automático de taxa)
- ✅ `USER_AGENT` customizado
- ✅ Pipelines ativados
- ✅ Feed exports em JSON

---

## 🚀 Execução dos Spiders

### Método 1: Script Individual

```bash
# Executar spider Anatel
python scripts/run_scrapy_spider.py anatel \
  --dataset-id anatel_mobile_brazil \
  --url "https://data-basis.org/dataset/d3c86a88-d9a4-4c0-bdec-08ab61e8f63c"

# Executar spider Internet Aberta
python scripts/run_scrapy_spider.py internet_aberta \
  --dataset-id internet_aberta_forecast \
  --url "https://internetaberta.com.br/wp-content/uploads/2024/05/Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf"

# Executar spider Springer
python scripts/run_scrapy_spider.py springer \
  --dataset-id springer_digital_divide \
  --url "https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-024-00508-8"

# Executar spider GitHub
python scripts/run_scrapy_spider.py github \
  --dataset-id github_5g3e \
  --url "https://github.com/cedric-cnam/5G3E-dataset"
```

### Método 2: Executar Todos os Spiders

```bash
# Executar todos os spiders configurados
python src/scrapy/run_all_spiders.py
```

**Este script:**
1. Carrega configuração de datasets
2. Identifica datasets que requerem scraping
3. Executa spiders apropriados
4. Salva metadados de todos os downloads

---

## 📊 Estrutura do Projeto Scrapy

```
src/scrapy/
├── __init__.py
└── scrapy_spiders/
    ├── __init__.py
    ├── items.py                    # Definições de Items
    ├── pipelines.py               # Pipelines de processamento
    ├── settings.py                # Configurações Scrapy
    ├── anatel_spider.py           # Spider Anatel
    ├── internet_aberta_spider.py   # Spider Internet Aberta
    ├── springer_spider.py         # Spider Springer
    ├── github_spider.py           # Spider GitHub
    └── mit_spider.py              # Spider MIT (existente)
```

---

## 🎯 Casos de Uso

### Caso 1: Scraping Anatel (Data Basis)

**Problema:** Data Basis usa React/Next.js, tornando difícil extrair links diretamente.

**Solução:**
1. Parse de HTML para encontrar links CSV
2. Extração de JSON embutido em scripts JavaScript
3. Fallback para API Data Basis se disponível
4. Download direto de arquivos CSV

**Exemplo:**
```python
# Spider automaticamente:
# 1. Parse da página React
# 2. Busca links CSV
# 3. Tenta API Data Basis
# 4. Download do arquivo
```

---

### Caso 2: Download de PDFs (Internet Aberta)

**Problema:** PDFs podem estar em links diretos ou em páginas intermediárias.

**Solução:**
1. Download direto se URL é PDF
2. Parse de página para encontrar links PDF
3. Validação de arquivos baixados

**Exemplo:**
```python
# Spider automaticamente:
# 1. Detecta se URL é PDF direto
# 2. Ou parse página para encontrar PDF
# 3. Download e validação
```

---

### Caso 3: Artigos Científicos (Springer)

**Problema:** Dados podem estar em múltiplos lugares (artigo, repositórios externos).

**Solução:**
1. Parse do artigo para encontrar links de dados
2. Detecção de repositórios externos (Zenodo, GitHub)
3. Download automático de arquivos suplementares
4. Registro de links de repositórios para processamento posterior

**Exemplo:**
```python
# Spider automaticamente:
# 1. Parse artigo Springer
# 2. Busca seções "Data Availability"
# 3. Encontra links CSV/ZIP
# 4. Detecta links Zenodo/GitHub
# 5. Download de arquivos diretos
```

---

### Caso 4: Repositórios GitHub

**Problema:** Arquivos podem estar em múltiplos diretórios, URLs blob precisam ser convertidas.

**Solução:**
1. Conversão automática blob → raw
2. Busca recursiva em diretórios de dados
3. Download de múltiplos formatos

**Exemplo:**
```python
# Spider automaticamente:
# 1. Converte URLs blob para raw
# 2. Busca em diretórios "data", "dataset"
# 3. Download de todos os arquivos encontrados
```

---

## 🔍 Detalhes Técnicos

### AnatelSpider - Parsing React/Next.js

**Desafio:** Data Basis usa React, então HTML renderizado não contém todos os dados.

**Abordagem:**
1. Parse de scripts JavaScript que contêm `__NEXT_DATA__`
2. Extração de JSON com informações do dataset
3. Fallback para API Data Basis

**Código:**
```python
# Buscar JSON embutido em scripts
scripts = response.css('script::text').getall()
for script in scripts:
    if '__NEXT_DATA__' in script:
        json_match = re.search(r'__NEXT_DATA__.*?({.+?})', script)
        if json_match:
            data = json.loads(json_match.group(1))
            # Processar dados do dataset
```

---

### SpringerSpider - Detecção de Links de Dados

**Abordagem:**
1. Parse de texto completo do artigo
2. Busca por padrões de URLs (regex)
3. Filtragem por extensões relevantes (.csv, .zip, .json)

**Código:**
```python
# Buscar padrões de URLs de dados
text_content = response.css('body').get()
data_urls = re.findall(
    r'https?://[^\s<>"\'{}|\\^`\[\]]+\.(?:csv|zip|json|parquet)',
    text_content
)
```

---

## 📝 Metadados e Logging

### Arquivo de Metadados

**Localização:** `data/raw/download_metadata.json`

**Estrutura:**
```json
{
  "anatel_mobile_brazil": [
    {
      "file_path": "data/raw/anatel_mobile_brazil/mobile_data.csv",
      "url": "https://data-basis.org/...",
      "filename": "mobile_data.csv",
      "size": 58234,
      "file_type": "csv",
      "download_date": "2025-10-31T21:30:00",
      "spider": "anatel"
    }
  ]
}
```

### Logs

**Localização:** `data/raw/scrapy.log`

**Informações:**
- Requests feitos
- Downloads bem-sucedidos
- Erros e warnings
- Estatísticas de scraping

---

## 🧪 Testes

### Testar Spider Individual

```bash
# Testar Anatel
python scripts/run_scrapy_spider.py anatel \
  --dataset-id test_anatel \
  --url "https://data-basis.org/dataset/d3c86a88-d9a4-4c0-bdec-08ab61e8f63c"

# Verificar arquivo baixado
ls -lh data/raw/test_anatel/

# Verificar metadados
cat data/raw/download_metadata.json | jq '.test_anatel'
```

### Testar Todos os Spiders

```bash
# Executar todos
python src/scrapy/run_all_spiders.py

# Verificar resultados
cat data/raw/download_metadata.json
```

---

## 🔧 Troubleshooting

### Problema 1: Spider não encontra arquivos

**Solução:**
- Verificar se o site mudou estrutura HTML
- Ajustar seletores CSS/XPath
- Adicionar fallbacks adicionais

### Problema 2: Rate Limiting

**Solução:**
- Aumentar `DOWNLOAD_DELAY`
- Habilitar `AUTOTHROTTLE`
- Reduzir `CONCURRENT_REQUESTS`

### Problema 3: Encoding Issues

**Solução:**
- Especificar encoding no spider
- Usar `response.encoding` para detecção automática
- Configurar `FEED_EXPORT_ENCODING` nas settings

---

## 🚀 Próximos Passos

### Melhorias Planejadas

1. **Scrapy Middleware Personalizado**
   - Rotação de User-Agents
   - Proxy support
   - Retry inteligente

2. **Spider Universal**
   - Spider genérico que detecta tipo de site
   - Auto-configuração baseada em URL

3. **Integração com Pipeline Principal**
   - Chamar spiders do pipeline de download
   - Processamento automático após download

4. **Monitoramento**
   - Dashboard de status dos spiders
   - Alertas para falhas
   - Estatísticas de sucesso

---

## ✅ Checklist de Implementação

- [x] AnatelSpider implementado
- [x] InternetAbertaSpider implementado
- [x] SpringerSpider implementado
- [x] GitHubSpider implementado
- [x] Items definidos
- [x] Pipelines implementados
- [x] Settings configurados
- [x] Scripts de execução criados
- [x] Documentação completa

---

**Status:** ✅ **SCRAPY COMPLETO E PRONTO PARA USO**

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**


