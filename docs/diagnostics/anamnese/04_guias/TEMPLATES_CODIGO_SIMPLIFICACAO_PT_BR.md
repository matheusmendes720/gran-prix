# 📝 TEMPLATES DE CÓDIGO PARA SIMPLIFICAÇÃO
## Nova Corrente - Templates de Código para Aplicar Mudanças

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Templates Prontos - Pronto para Uso  
**Objetivo:** Fornecer templates de código para aplicar simplificações necessárias

---

## 📋 ÍNDICE

1. [Template: Integration Manager Simplificado](#template-integration-manager)
2. [Template: Orchestrator Simplificado](#template-orchestrator)
3. [Template: ETL Pipeline com Desabilitação](#template-etl)
4. [Template: Health Check Simplificado](#template-health-check)
5. [Template: Environment Variables](#template-env-vars)

---

<a name="template-integration-manager"></a>

## 1. 🔧 TEMPLATE: INTEGRATION MANAGER SIMPLIFICADO

### 1.1 Código Antes (Com ML e APIs Externas)

```python
# backend/app/core/integration_manager.py
# ❌ ANTES - Com ML e APIs externas

from backend.services.external_data_service import external_data_service
from backend.services.prediction_service import prediction_service

# External Data Service
self.services['external_data'] = external_data_service

# Prediction Service
self.services['prediction'] = prediction_service

# External API Clients
from backend.config.external_apis_config import INMET_CONFIG, BACEN_CONFIG, ANATEL_CONFIG
self.external_clients['inmet'] = {...}
self.external_clients['bacen'] = {...}
self.external_clients['anatel'] = {...}
```

---

### 1.2 Código Depois (Simplificado)

```python
# backend/app/core/integration_manager.py
# ✅ DEPOIS - Simplificado (sem ML e sem APIs externas)

# ❌ REMOVIDO: External Data Service
# ❌ REMOVIDO: Prediction Service
# ❌ REMOVIDO: External API Clients

# ✅ MANTER apenas services essenciais:
from backend.services.database_service import database_service
from backend.services.material_service import material_service
from backend.services.feature_service import feature_service
from backend.services.analytics_service import analytics_service
from backend.services.integration_service import integration_service

# Initialize services (SIMPLIFICADO)
self.services = {}
self.services['database'] = database_service
self.services['material'] = material_service
self.services['feature'] = feature_service
self.services['analytics'] = analytics_service
self.services['integration'] = integration_service

# ❌ REMOVIDO: external_clients (não mais necessário)
```

---

<a name="template-orchestrator"></a>

## 2. 🔧 TEMPLATE: ORCHESTRATOR SIMPLIFICADO

### 2.1 Código Antes (Com Chamadas a APIs Externas)

```python
# backend/pipelines/orchestrator_service.py
# ❌ ANTES - Com chamadas a APIs externas

def run_complete_pipeline(self, start_date, end_date):
    # Extract external data
    if 'climate' in sources or 'all' in sources:
        rows = climate_etl.run(start_date, end_date)  # ❌ Chamada API
    
    if 'economic' in sources or 'all' in sources:
        rows = economic_etl.run(start_date, end_date)  # ❌ Chamada API
    
    if 'anatel' in sources or 'all' in sources:
        rows = anatel_5g_etl.run(start_date, end_date)  # ❌ Chamada API
```

---

### 2.2 Código Depois (Simplificado)

```python
# backend/pipelines/orchestrator_service.py
# ✅ DEPOIS - Simplificado (sem chamadas a APIs externas)

def run_complete_pipeline(self, start_date, end_date):
    # ❌ APIs externas desabilitadas em produção
    # ✅ Usar apenas dados pré-computados
    
    if 'climate' in sources or 'all' in sources:
        logger.info("⚠️ Climate ETL disabled in production - using precomputed data")
        # rows = climate_etl.run(start_date, end_date)  # ❌ DESABILITADO
        # ✅ Carregar dados pré-computados se necessário
        pass
    
    if 'economic' in sources or 'all' in sources:
        logger.info("⚠️ Economic ETL disabled in production - using precomputed data")
        # rows = economic_etl.run(start_date, end_date)  # ❌ DESABILITADO
        pass
    
    if 'anatel' in sources or 'all' in sources:
        logger.info("⚠️ Anatel 5G ETL disabled in production - using precomputed data")
        # rows = anatel_5g_etl.run(start_date, end_date)  # ❌ DESABILITADO
        pass
    
    # ✅ MANTER: Processamento de dados pré-computados
    # ✅ MANTER: Transformações locais
    # ✅ MANTER: Feature engineering
```

---

<a name="template-etl"></a>

## 3. 🔧 TEMPLATE: ETL PIPELINE COM DESABILITAÇÃO

### 3.1 Código Antes (Sempre Chama API)

```python
# backend/pipelines/climate_etl.py
# ❌ ANTES - Sempre chama API

def run(self, start_date, end_date):
    # Chamadas API em tempo real
    data = self.fetch_from_api(start_date, end_date)
    processed_data = self.process(data)
    return processed_data
```

---

### 3.2 Código Depois (Com Desabilitação)

```python
# backend/pipelines/climate_etl.py
# ✅ DEPOIS - Com desabilitação de APIs em produção

import os
from pathlib import Path

def run(self, start_date, end_date):
    # Verificar se APIs externas estão habilitadas
    enable_external_apis = os.getenv('ENABLE_EXTERNAL_APIS', 'false').lower() == 'true'
    
    if not enable_external_apis:
        # 🟡 Em produção: usar apenas dados pré-computados
        logger.info("⚠️ External APIs disabled - using precomputed data")
        return self.load_from_precomputed(start_date, end_date)
    
    # ✅ Apenas para processamento local (ML environment)
    data = self.fetch_from_api(start_date, end_date)
    processed_data = self.process(data)
    return processed_data

def load_from_precomputed(self, start_date, end_date):
    """Load precomputed data from storage"""
    ml_results_path = Path(os.getenv('ML_RESULTS_PATH', './data/ml_results'))
    data_file = ml_results_path / 'climate' / f'climate_{start_date}_{end_date}.parquet'
    
    if data_file.exists():
        import pandas as pd
        return pd.read_parquet(data_file)
    else:
        logger.warning(f"Precomputed data not found: {data_file}")
        return None
```

---

<a name="template-health-check"></a>

## 4. 🔧 TEMPLATE: HEALTH CHECK SIMPLIFICADO

### 4.1 Código Antes (Verifica ML e APIs Externas)

```python
# backend/app/api/v1/routes/health.py
# ❌ ANTES - Verifica ML e APIs externas

async def health_check():
    # Check ML services
    ml_status = check_ml_services()
    
    # Check external APIs
    api_status = check_external_apis()
    
    return {
        'status': 'healthy',
        'ml_services': ml_status,
        'external_apis': api_status
    }
```

---

### 4.2 Código Depois (Simplificado)

```python
# backend/app/api/v1/routes/health.py
# ✅ DEPOIS - Simplificado (sem ML e sem APIs externas)

async def health_check():
    # ✅ MANTER apenas services essenciais
    database_status = check_database()
    storage_status = check_storage()
    cache_status = check_cache()
    
    return {
        'status': 'healthy',
        'database': database_status,
        'storage': storage_status,
        'cache': cache_status,
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    }
    
    # ❌ REMOVIDO: ML services check
    # ❌ REMOVIDO: External APIs check
```

---

<a name="template-env-vars"></a>

## 5. 🔧 TEMPLATE: ENVIRONMENT VARIABLES

### 5.1 Arquivo .env (Deployment)

```bash
# .env - Deployment Environment
# ✅ Configurações para deployment simplificado

# External APIs
ENABLE_EXTERNAL_APIS=false
ENABLE_ML_PROCESSING=false

# Data Paths
ML_RESULTS_PATH=./data/ml_results
DATA_DIR=./data
LOG_DIR=./logs

# MinIO Configuration
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Redis Configuration
REDIS_URL=redis://redis:6379

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:5000

# ❌ REMOVIDO: ML-related variables
# ❌ REMOVIDO: External API keys
```

---

### 5.2 Arquivo .env.ml (ML Environment Local)

```bash
# .env.ml - ML Processing Environment (Local)
# ✅ Configurações para processamento ML local

# External APIs (habilitado para coleta local)
ENABLE_EXTERNAL_APIS=true
ENABLE_ML_PROCESSING=true

# ML Configuration
MODELS_DIR=./models
ML_RESULTS_PATH=./data/ml_results

# Data Paths
DATA_DIR=./data
LOG_DIR=./logs

# ML Processing
ML_BATCH_SIZE=1000
ML_NUM_WORKERS=4

# External API Keys (para coleta local)
INMET_API_KEY=your_key_here
BACEN_API_KEY=your_key_here
ANATEL_API_KEY=your_key_here
```

---

## 6. 📝 TEMPLATES ADICIONAIS

### 6.1 Template: Endpoint Simplificado

**Antes:**
```python
@router.get("/forecasts")
async def get_forecasts():
    # ❌ Usa ML service para gerar previsões em tempo real
    predictions = prediction_service.predict(...)
    return predictions
```

**Depois:**
```python
@router.get("/forecasts")
async def get_forecasts():
    # ✅ Lê apenas dados pré-computados
    ml_results_path = Path(os.getenv('ML_RESULTS_PATH', './data/ml_results'))
    forecasts_file = ml_results_path / 'forecasts' / 'latest.parquet'
    
    if forecasts_file.exists():
        import pandas as pd
        df = pd.read_parquet(forecasts_file)
        return df.to_dict('records')
    else:
        return {"error": "Precomputed forecasts not available"}
```

---

### 6.2 Template: Docker Compose Simplificado

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build:
      dockerfile: infrastructure/docker/Dockerfile.backend.deployment
    environment:
      - ENABLE_EXTERNAL_APIS=false
      - ENABLE_ML_PROCESSING=false
      - ML_RESULTS_PATH=/app/data/ml_results
    volumes:
      - ./data/ml_results:/app/data/ml_results:ro  # Read-only
    # ❌ REMOVIDO: ML-related volumes
    # ❌ REMOVIDO: External API configurations

  # ❌ REMOVIDO: ML processing service
  # ❌ REMOVIDO: External API collectors
```

---

## 7. ✅ CHECKLIST DE APLICAÇÃO

### Antes de Aplicar Templates:

- [ ] ✅ Backup do código atual
- [ ] ✅ Branch de trabalho criada
- [ ] ✅ Ambiente de testes configurado

### Aplicando Templates:

- [ ] ✅ Template 1: Integration Manager aplicado
- [ ] ✅ Template 2: Orchestrator aplicado
- [ ] ✅ Template 3: ETL Pipelines aplicado
- [ ] ✅ Template 4: Health Check aplicado
- [ ] ✅ Template 5: Environment Variables aplicado

### Após Aplicar Templates:

- [ ] ✅ Código compila sem erros
- [ ] ✅ Testes passando
- [ ] ✅ Validação executada
- [ ] ✅ Health checks funcionando

---

## 8. 📝 CONCLUSÃO

Estes templates fornecem:

1. **Código Pronto:** Templates de código para aplicar mudanças
2. **Comparação:** Antes vs. Depois para cada componente
3. **Exemplos Práticos:** Código específico para cada mudança
4. **Checklist:** Validação de aplicação

**Próximos Passos:**
1. Revisar templates
2. Aplicar templates no código
3. Validar mudanças
4. Testar aplicação

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Templates Prontos - Pronto para Uso

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

