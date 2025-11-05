# 🔍 RELATÓRIO DE ANÁLISE DE CODEBASE
## Nova Corrente - Mapeamento Completo de Componentes e Dependências

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Análise Completa - Mapeamento Detalhado  
**Objetivo:** Identificar todos os componentes que devem ser removidos/simplificados para deploy simplificado

---

## 📋 ÍNDICE

1. [Mapeamento de Arquivos e Componentes](#mapeamento)
2. [Análise de Dependências ML](#dependencias-ml)
3. [Análise de Dependências APIs Externas](#dependencias-apis)
4. [Identificação de Código para Remoção](#codigo-remocao)
5. [Identificação de Código para Simplificação](#codigo-simplificacao)
6. [Estratégia de Refatoração](#estrategia-refatoracao)
7. [Impacto de Mudanças](#impacto-mudancas)

---

<a name="mapeamento"></a>

## 1. 📁 MAPEAMENTO DE ARQUIVOS E COMPONENTES

### 1.1 Estrutura de Diretórios Atual

```
gran_prix/
├── backend/
│   ├── api/                          # API Legacy (Flask)
│   │   └── enhanced_api.py           # ❌ REMOVER ou DEPRECATED
│   │
│   ├── app/                          # API Principal (FastAPI)
│   │   ├── main.py                   # ✅ MANTER
│   │   ├── api/v1/routes/            # ✅ MANTER (verificar endpoints ML)
│   │   └── core/
│   │       ├── integration_manager.py # 🟡 SIMPLIFICAR (remover ML/APIs)
│   │       └── startup.py            # ✅ MANTER
│   │
│   ├── data/collectors/              # ❌ REMOVER do deployment
│   │   ├── brazilian_apis_expanded.py # ❌ REMOVER do deployment
│   │   ├── web_scrapers.py           # ❌ REMOVER do deployment
│   │   └── README_EXPANDED_APIS.md   # ❌ REMOVER do deployment
│   │
│   ├── ml/                           # ❌ REMOVER do deployment
│   │   ├── models/                   # ❌ REMOVER do deployment
│   │   └── ... (32 arquivos)         # ❌ REMOVER do deployment
│   │
│   ├── pipelines/                    # 🟡 SIMPLIFICAR
│   │   ├── climate_etl.py           # 🟡 DESABILITAR chamadas em tempo real
│   │   ├── economic_etl.py          # 🟡 DESABILITAR chamadas em tempo real
│   │   ├── anatel_5g_etl.py         # 🟡 DESABILITAR chamadas em tempo real
│   │   ├── orchestrator_service.py  # 🟡 SIMPLIFICAR (sem APIs externas)
│   │   └── ... (82 arquivos)         # ✅ MANTER para processamento local
│   │
│   ├── services/                     # 🟡 SIMPLIFICAR
│   │   ├── prediction_service.py    # ❌ REMOVER do deployment
│   │   ├── external_data_service.py # ❌ REMOVER do deployment
│   │   ├── ml_models/                # ❌ REMOVER do deployment
│   │   │   └── model_registry.py    # ❌ REMOVER do deployment
│   │   └── ... (outros services)     # ✅ MANTER
│   │
│   ├── config/
│   │   └── external_apis_config.py  # 🟡 DESABILITAR em produção
│   │
│   └── requirements*.txt
│       ├── requirements.txt          # ✅ OK (dev local)
│       ├── requirements_deployment.txt # ✅ OK (NO ML)
│       └── requirements_ml.txt      # ✅ OK (ML environment)
│
├── data/
│   ├── raw/                          # ✅ MANTER (dados históricos)
│   ├── processed/                    # 🟡 MIGRAR para Parquet
│   └── training/                     # ✅ MANTER (dados ML)
│
├── frontend/                         # ✅ MANTER (verificar ML UI)
│   └── src/
│
└── infrastructure/
    └── docker/
        ├── Dockerfile.backend.deployment # ✅ OK (NO ML)
        └── Dockerfile.backend.ml      # ✅ OK (ML environment)
```

---

### 1.2 Componentes por Categoria

#### ✅ Componentes que DEVEM ser MANTIDOS

**Backend API (FastAPI):**
- `backend/app/main.py` - FastAPI app principal
- `backend/app/api/v1/routes/` - Endpoints REST (exceto ML/APIs externas)
- `backend/app/core/startup.py` - Startup handlers

**Services Essenciais:**
- `backend/services/database_service.py` - Database service
- `backend/services/material_service.py` - Material management
- `backend/services/feature_service.py` - Feature engineering (dados pré-computados)
- `backend/services/analytics_service.py` - Analytics
- `backend/services/integration_service.py` - Integration (sem APIs externas)

**Infrastructure:**
- `docker-compose.yml` - Docker Compose
- `infrastructure/docker/Dockerfile.backend.deployment` - Deployment container
- MinIO, Redis configurados

**Frontend:**
- `frontend/` - React + Next.js dashboard

---

#### 🟡 Componentes que DEVEM ser SIMPLIFICADOS

**Integration Manager:**
- `backend/app/core/integration_manager.py` - Remover inicialização de:
  - `prediction_service`
  - `external_data_service`
  - External API clients (INMET, BACEN, ANATEL, OpenWeather, Expanded)

**Orchestrator:**
- `backend/pipelines/orchestrator_service.py` - Desabilitar chamadas a:
  - `climate_etl.run()` (em produção)
  - `economic_etl.run()` (em produção)
  - `anatel_5g_etl.run()` (em produção)

**ETL Pipelines:**
- `backend/pipelines/climate_etl.py` - Desabilitar chamadas API em tempo real
- `backend/pipelines/economic_etl.py` - Desabilitar chamadas API em tempo real
- `backend/pipelines/anatel_5g_etl.py` - Desabilitar chamadas API em tempo real

**Config:**
- `backend/config/external_apis_config.py` - Desabilitar em produção

---

#### ❌ Componentes que DEVEM ser REMOVIDOS do Deployment

**API Legacy:**
- `backend/api/enhanced_api.py` - Flask API legacy

**ML Services:**
- `backend/services/prediction_service.py` - ML predictions
- `backend/services/ml_models/model_registry.py` - Model registry
- `backend/ml/` - Todo diretório ML

**External Data Services:**
- `backend/services/external_data_service.py` - Service para APIs externas

**Collectors:**
- `backend/data/collectors/brazilian_apis_expanded.py` - 25+ APIs
- `backend/data/collectors/web_scrapers.py` - Web scraping

---

<a name="dependencias-ml"></a>

## 2. 🔍 ANÁLISE DE DEPENDÊNCIAS ML

### 2.1 Arquivos com Imports ML

#### Arquivos que DEVEM ser modificados:

**1. `backend/api/enhanced_api.py`**
```python
# ❌ REMOVER estas linhas:
from backend.services.ml_models.model_registry import model_registry
```

**2. `backend/app/core/integration_manager.py`**
```python
# ❌ REMOVER estas linhas (linhas 109-117):
try:
    from backend.services.prediction_service import prediction_service
    self.services['prediction'] = prediction_service
    results['services']['prediction'] = {'status': 'healthy'}
    logger.info("✅ Prediction service initialized")
except Exception as e:
    logger.error(f"❌ Prediction service error: {e}")
    results['services']['prediction'] = {'status': 'error', 'error': str(e)}
```

**3. Verificar `backend/app/api/v1/routes/`**
- Verificar se há endpoints ML que precisam ser removidos
- Endpoints que devem ser mantidos: analytics, forecasts (dados pré-computados)

---

### 2.2 Dependências em Requirements

**Status Atual:**
- ✅ `backend/requirements_deployment.txt` - **Já está correto** (NO ML dependencies)
- ✅ `backend/requirements_ml.txt` - Para ML environment separado (OK)
- ✅ `backend/requirements.txt` - Para dev local (OK)

**Validação:**
- ✅ Dockerfile verifica ausência de ML dependencies
- ✅ Requirements de deployment não contém ML

**Ação Necessária:**
- ❌ Remover imports ML do código
- ❌ Remover inicializações de ML services

---

<a name="dependencias-apis"></a>

## 3. 🔍 ANÁLISE DE DEPENDÊNCIAS APIs EXTERNAS

### 3.1 Arquivos que Fazem Chamadas a APIs Externas

#### Arquivos que DEVEM ser modificados:

**1. `backend/app/core/integration_manager.py`**
```python
# ❌ REMOVER estas seções (linhas 61-62, 119-186):
# External Data Service
from backend.services.external_data_service import external_data_service
self.services['external_data'] = external_data_service

# External API Clients
# INMET (Climate) - linhas 122-134
# BACEN (Economic) - linhas 136-148
# ANATEL (5G) - linhas 150-162
# OpenWeatherMap - linhas 164-176
# Expanded API Integration - linhas 178-186
```

**2. `backend/pipelines/orchestrator_service.py`**
```python
# 🟡 DESABILITAR estas chamadas (linhas 19-22, 84-102):
from backend.pipelines.climate_etl import climate_etl
from backend.pipelines.economic_etl import economic_etl
from backend.pipelines.anatel_5g_etl import anatel_5g_etl

# No método run_complete_pipeline():
# ❌ DESABILITAR:
rows = climate_etl.run(start_date, end_date)
rows = economic_etl.run(start_date, end_date)
rows = anatel_5g_etl.run(start_date, end_date)
```

**3. `backend/pipelines/climate_etl.py`**
```python
# 🟡 DESABILITAR chamadas API em tempo real
# Manter apenas para processamento local de dados pré-coletados
```

**4. `backend/pipelines/economic_etl.py`**
```python
# 🟡 DESABILITAR chamadas API em tempo real
# Manter apenas para processamento local de dados pré-coletados
```

**5. `backend/pipelines/anatel_5g_etl.py`**
```python
# 🟡 DESABILITAR chamadas API em tempo real
# Manter apenas para processamento local de dados pré-coletados
```

**6. `backend/app/api/v1/routes/integration.py`**
```python
# 🟡 DESABILITAR endpoints de refresh de APIs externas
# Verificar endpoints que fazem chamadas em tempo real
```

---

### 3.2 Collectors de APIs Externas

#### Arquivos que DEVEM ser removidos do deployment:

**1. `backend/data/collectors/brazilian_apis_expanded.py`**
- 25+ APIs externas
- **Ação:** ❌ Remover do deployment (manter localmente para ML processing)

**2. `backend/data/collectors/web_scrapers.py`**
- Web scraping de sites governamentais
- **Ação:** ❌ Remover do deployment (manter localmente para ML processing)

**3. `backend/data/collectors/README_EXPANDED_APIS.md`**
- Documentação de APIs
- **Ação:** ❌ Remover do deployment (manter localmente para referência)

---

<a name="codigo-remocao"></a>

## 4. 🗑️ IDENTIFICAÇÃO DE CÓDIGO PARA REMOÇÃO

### 4.1 Código ML que deve ser removido

#### Remover de `backend/api/enhanced_api.py`:
```python
# ❌ REMOVER:
from backend.services.ml_models.model_registry import model_registry
```

#### Remover de `backend/app/core/integration_manager.py`:
```python
# ❌ REMOVER seção completa (linhas 109-117):
# Prediction Service
try:
    from backend.services.prediction_service import prediction_service
    self.services['prediction'] = prediction_service
    results['services']['prediction'] = {'status': 'healthy'}
    logger.info("✅ Prediction service initialized")
except Exception as e:
    logger.error(f"❌ Prediction service error: {e}")
    results['services']['prediction'] = {'status': 'error', 'error': str(e)}
```

---

### 4.2 Código APIs Externas que deve ser removido

#### Remover de `backend/app/core/integration_manager.py`:
```python
# ❌ REMOVER (linha 61-62):
from backend.services.external_data_service import external_data_service
self.services['external_data'] = external_data_service

# ❌ REMOVER seção completa (linhas 119-186):
# Initialize Outer API Clients
logger.info("Initializing external API clients...")

# INMET (Climate) - REMOVER
# BACEN (Economic) - REMOVER
# ANATEL (5G) - REMOVER
# OpenWeatherMap - REMOVER
# Expanded API Integration - REMOVER
```

#### Desabilitar de `backend/pipelines/orchestrator_service.py`:
```python
# 🟡 DESABILITAR (linhas 84-102):
# No método run_complete_pipeline():
if 'climate' in sources or 'all' in sources:
    rows = climate_etl.run(start_date, end_date)  # ❌ DESABILITAR

if 'economic' in sources or 'all' in sources:
    rows = economic_etl.run(start_date, end_date)  # ❌ DESABILITAR

if 'anatel' in sources or 'all' in sources:
    rows = anatel_5g_etl.run(start_date, end_date)  # ❌ DESABILITAR
```

---

### 4.3 API Legacy que deve ser removida

#### Remover ou marcar como deprecated:
- `backend/api/enhanced_api.py` - Flask API legacy
- **Ação:** ❌ Remover completamente ou marcar como DEPRECATED

---

<a name="codigo-simplificacao"></a>

## 5. 🔧 IDENTIFICAÇÃO DE CÓDIGO PARA SIMPLIFICAÇÃO

### 5.1 Integration Manager - Simplificação

#### Mudanças necessárias em `backend/app/core/integration_manager.py`:

**Antes:**
```python
# Initialize services
self.services = {}
self.external_clients = {}

# External Data Service
from backend.services.external_data_service import external_data_service
self.services['external_data'] = external_data_service

# Prediction Service
from backend.services.prediction_service import prediction_service
self.services['prediction'] = prediction_service

# External API Clients
# INMET, BACEN, ANATEL, OpenWeather, Expanded...
```

**Depois:**
```python
# Initialize services (SIMPLIFICADO)
self.services = {}
# ❌ REMOVIDO: external_clients (não mais necessário)

# ✅ MANTER apenas services essenciais:
# - database_service
# - material_service
# - feature_service
# - analytics_service
# - integration_service (sem APIs externas)

# ❌ REMOVIDO: external_data_service
# ❌ REMOVIDO: prediction_service
# ❌ REMOVIDO: external_clients (INMET, BACEN, ANATEL, etc.)
```

---

### 5.2 Orchestrator Service - Simplificação

#### Mudanças necessárias em `backend/pipelines/orchestrator_service.py`:

**Antes:**
```python
def run_complete_pipeline(self, start_date, end_date):
    # Extract external data
    rows = climate_etl.run(start_date, end_date)
    rows = economic_etl.run(start_date, end_date)
    rows = anatel_5g_etl.run(start_date, end_date)
    
    # Process data
    # ...
```

**Depois:**
```python
def run_complete_pipeline(self, start_date, end_date):
    # ❌ REMOVIDO: Chamadas a APIs externas
    # ✅ MANTER: Processamento de dados pré-computados
    # ✅ MANTER: Transformações locais
    # ✅ MANTER: Feature engineering
    pass
```

---

### 5.3 ETL Pipelines - Desabilitar Chamadas API

#### Mudanças necessárias em ETL pipelines:

**Antes (`climate_etl.py`, `economic_etl.py`, `anatel_5g_etl.py`):**
```python
def run(self, start_date, end_date):
    # Chamadas API em tempo real
    data = self.fetch_from_api(start_date, end_date)
    # Processamento
    return processed_data
```

**Depois:**
```python
def run(self, start_date, end_date):
    # 🟡 DESABILITAR chamadas API em produção
    if os.getenv('ENABLE_EXTERNAL_APIS', 'false').lower() == 'true':
        # Apenas para processamento local
        data = self.fetch_from_api(start_date, end_date)
    else:
        # Em produção: usar apenas dados pré-computados
        data = self.load_from_precomputed(start_date, end_date)
    
    # Processamento
    return processed_data
```

---

<a name="estrategia-refatoracao"></a>

## 6. 🎯 ESTRATÉGIA DE REFATORAÇÃO

### 6.1 Fase 1: Remover ML Services (Prioridade MÁXIMA)

**Arquivos a modificar:**
1. `backend/app/core/integration_manager.py` - Remover inicialização de `prediction_service`
2. `backend/api/enhanced_api.py` - Remover import de `model_registry`
3. `backend/app/api/v1/routes/` - Verificar e remover endpoints ML

**Tempo estimado:** 1-2 horas  
**Prioridade:** 🔴 **MÁXIMA**

---

### 6.2 Fase 2: Desabilitar APIs Externas (Prioridade MÁXIMA)

**Arquivos a modificar:**
1. `backend/app/core/integration_manager.py` - Remover inicialização de external API clients
2. `backend/pipelines/orchestrator_service.py` - Desabilitar chamadas ETL
3. `backend/app/api/v1/routes/integration.py` - Desabilitar endpoints de refresh
4. `backend/pipelines/climate_etl.py` - Desabilitar chamadas API
5. `backend/pipelines/economic_etl.py` - Desabilitar chamadas API
6. `backend/pipelines/anatel_5g_etl.py` - Desabilitar chamadas API

**Tempo estimado:** 2-3 horas  
**Prioridade:** 🔴 **MÁXIMA**

---

### 6.3 Fase 3: Remover API Legacy (Prioridade BAIXA)

**Arquivo a modificar:**
1. `backend/api/enhanced_api.py` - Remover ou marcar como deprecated

**Tempo estimado:** 30 minutos  
**Prioridade:** 🟢 **BAIXA** (pode ser feito após deploy)

---

### 6.4 Fase 4: Simplificar Integration Manager (Prioridade ALTA)

**Arquivo a modificar:**
1. `backend/app/core/integration_manager.py` - Limpar código removido

**Tempo estimado:** 1 hora  
**Prioridade:** 🟡 **ALTA**

---

<a name="impacto-mudancas"></a>

## 7. 📊 IMPACTO DE MUDANÇAS

### 7.1 Impacto em Funcionalidades

#### Funcionalidades que NÃO serão mais disponíveis em produção:

**ML Services:**
- ❌ Predições ML em tempo real
- ❌ Model registry em produção
- ✅ **Mantido:** Resultados pré-computados (read-only)

**APIs Externas:**
- ❌ Refresh de dados em tempo real
- ❌ Chamadas a APIs externas (INMET, BACEN, ANATEL)
- ✅ **Mantido:** Dados pré-coletados (processamento offline)

**API Legacy:**
- ❌ Flask API legacy
- ✅ **Mantido:** FastAPI (principal)

---

### 7.2 Impacto em Performance

**Melhorias Esperadas:**
- ✅ Redução de latência (sem chamadas API externas)
- ✅ Redução de tamanho de containers (sem ML dependencies)
- ✅ Redução de complexidade (menos componentes)

**Degradações Esperadas:**
- 🟡 Dados podem estar desatualizados (sem refresh automático)
- ✅ **Mitigação:** Processamento offline regular

---

### 7.3 Impacto em Manutenibilidade

**Melhorias Esperadas:**
- ✅ Código mais simples (menos componentes)
- ✅ Menos dependências externas
- ✅ Deployment mais simples

---

## 8. ✅ CHECKLIST DE REFATORAÇÃO

### Fase 1: Remover ML Services
- [ ] Remover import de `model_registry` de `enhanced_api.py`
- [ ] Remover inicialização de `prediction_service` de `integration_manager.py`
- [ ] Verificar e remover endpoints ML de `backend/app/api/v1/routes/`
- [ ] Testar aplicação sem ML services

### Fase 2: Desabilitar APIs Externas
- [ ] Remover inicialização de external API clients de `integration_manager.py`
- [ ] Remover inicialização de `external_data_service` de `integration_manager.py`
- [ ] Desabilitar chamadas ETL em `orchestrator_service.py`
- [ ] Desabilitar chamadas API em `climate_etl.py`, `economic_etl.py`, `anatel_5g_etl.py`
- [ ] Desabilitar endpoints de refresh em `integration.py`
- [ ] Testar aplicação offline (sem APIs externas)

### Fase 3: Remover API Legacy
- [ ] Remover ou marcar como deprecated `enhanced_api.py`
- [ ] Atualizar documentação

### Fase 4: Limpeza Final
- [ ] Limpar código removido de `integration_manager.py`
- [ ] Atualizar documentação
- [ ] Testes finais

---

## 9. 📝 CONCLUSÃO

Este relatório mapeou:

1. **Estrutura Completa:** Todos os arquivos e componentes
2. **Dependências ML:** Arquivos que importam/usam ML services
3. **Dependências APIs:** Arquivos que fazem chamadas a APIs externas
4. **Código para Remoção:** Código específico que deve ser removido
5. **Código para Simplificação:** Código que deve ser simplificado
6. **Estratégia de Refatoração:** Plano passo a passo
7. **Impacto:** Análise de impacto das mudanças

**Próximos Passos:**
1. Executar Fase 1 (Remover ML Services)
2. Executar Fase 2 (Desabilitar APIs Externas)
3. Executar Fase 3 (Remover API Legacy)
4. Executar Fase 4 (Limpeza Final)

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Análise Completa - Pronto para Refatoração

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

