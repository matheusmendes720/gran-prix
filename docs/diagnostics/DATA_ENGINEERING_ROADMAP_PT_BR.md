# 🗺️ ROADMAP DE ENGENHARIA DE DADOS - NOVA CORRENTE
## Status Atual vs. Plano de Implementação (16 Semanas)

**Versão:** 3.0  
**Data:** Novembro 2025  
**Status:** 📋 Roadmap Atualizado - Com Status Real de Implementação  
**Progresso Atual:** 15% Implementado (Fase 0 parcial)  
**Última Atualização Diagnóstico:** Novembro 2025

---

## 📊 EXECUTIVE SUMMARY

### Visão Geral
Este roadmap define a implementação completa da arquitetura de engenharia de dados para o projeto Nova Corrente, transformando o sistema atual (baseado em CSV e scripts Python) em uma plataforma moderna de Data Lakehouse com orquestração profissional.

**🔍 IMPORTANTE:** Este documento foi atualizado com base no [diagnóstico completo](./COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md) que identificou exatamente o que foi implementado e o que está faltando.

### Objetivos Estratégicos
1. **Escalabilidade:** Suportar crescimento de dados de GB → TB
2. **Confiabilidade:** Garantir qualidade de dados (99.9% accuracy)
3. **Performance:** Reduzir tempo de processamento em 80%
4. **Governança:** Implementar data catalog e lineage tracking
5. **Self-Service:** Permitir análises sem dependência de engenharia

### Métricas de Sucesso
| Métrica | Atual | Meta (16 semanas) | Status |
|---------|-------|-------------------|---------|
| **Data Quality Score** | 60% (validação manual) | 95% (Great Expectations) | 🔴 35% gap |
| **Pipeline Latency** | 4h (batch scripts) | 30min (Airflow otimizado) | 🔴 88% gap |
| **Storage Efficiency** | CSV (27MB não escalável) | Delta Lake (compressão 70%) | 🔴 100% gap |
| **Query Performance** | 30s (CSV full scan) | <3s (Delta Lake indexed) | 🔴 90% gap |
| **Data Governance** | 0% (sem catalog) | 90% (DataHub + lineage) | 🔴 100% gap |

### O Que Já Existe ✅
1. **ETL Básico Python** - `orchestrator_service.py` com scheduler básico (schedule library)
2. **Feature Engineering** - 73 features implementadas em `backend/pipelines/feature_calculation_etl.py`
3. **Database PostgreSQL** - Schema inicial em `backend/data/Nova_Corrente_ML_Ready_DB.sql`
4. **Pipelines ETL** - Scripts Python para Anatel 5G, Weather, Economic, Brazilian Calendar
5. **Data Processing** - 19 scripts de processamento em `backend/pipelines/data_processing/`
6. **Validação Básica** - Scripts manuais em `backend/pipelines/monitoring/`
7. **API FastAPI** - Endpoints básicos em `backend/api/enhanced_api.py`

### O Que NÃO Existe ❌
1. **Data Lakehouse (Bronze/Silver/Gold)** - 0% implementado
2. **Delta Lake** - 0% implementado
3. **dbt (data build tool)** - 0% implementado
4. **Apache Airflow** - 0% implementado (apenas scheduler Python básico)
5. **Great Expectations** - 0% implementado
6. **MLflow** - 0% implementado
7. **Star Schema (Gold Layer)** - 0% implementado
8. **Metabase/Superset** - 0% implementado
9. **DataHub Catalog** - 0% implementado
10. **Cloud Storage (S3/MinIO)** - 0% implementado

---

## 📋 RESUMO EXECUTIVO: O QUE JÁ FOI FEITO vs. O QUE FALTA

### 🟢 IMPLEMENTADO (15%)

| Componente | Status | Localização | Qualidade |
|------------|--------|---------------|----------|
| **ETL Pipelines** | ✅ 70% | `backend/pipelines/*.py` | Funcional, mas sem Airflow |
| **Feature Engineering** | ✅ 100% | `backend/pipelines/feature_calculation_etl.py` | 73 features completas |
| **Data Collectors** | ✅ 80% | `backend/data/collectors/` | Weather, Economic, 5G |
| **PostgreSQL Schema** | ✅ 60% | `backend/data/Nova_Corrente_ML_Ready_DB.sql` | Schema inicial, não star schema |
| **Orchestrator Básico** | ⚠️ 20% | `backend/pipelines/orchestrator_service.py` | Scheduler Python, sem UI |
| **ML Models** | ✅ 90% | `backend/ml/models/` | Prophet, ARIMA, LSTM |
| **Model Registry Básico** | ⚠️ 10% | `backend/services/ml_models/` | Pickle local, sem MLflow |
| **API FastAPI** | ✅ 80% | `backend/api/enhanced_api.py` | Endpoints básicos |
| **Documentação** | ✅ 100% | `docs/` | Completa e detalhada |

### 🔴 FALTANDO (85%)

| Componente | Status | Impacto | Prioridade |
|------------|--------|---------|------------|
| **Cloud Storage (MinIO/S3)** | ❌ 0% | Bloqueando TUDO | 🔴🔴🔴 CRÍTICA |
| **Delta Lake** | ❌ 0% | Sem ACID, sem scala | 🔴🔴🔴 CRÍTICA |
| **dbt** | ❌ 0% | Transform sem testes | 🔴🔴🔴 CRÍTICA |
| **Apache Airflow** | ❌ 0% | Orq. sem UI/retry | 🔴🔴🔴 CRÍTICA |
| **Bronze/Silver/Gold Layers** | ❌ 0% | Arquitetura incompleta | 🔴🔴 ALTA |
| **Great Expectations** | ❌ 0% | Qualidade não validada | 🔴🔴 ALTA |
| **Star Schema (Gold)** | ❌ 0% | Analytics não otimizado | 🟡 MÉDIA |
| **MLflow** | ❌ 0% | ML sem tracking | 🟡 MÉDIA |
| **Metabase/BI** | ❌ 0% | Sem self-service | 🟡 MÉDIA |
| **DataHub Catalog** | ❌ 0% | Sem governança | 🟢 BAIXA |
| **Streaming (Kafka)** | ❌ 0% | Sem real-time | 🟢 BAIXA |

---

## 🎯 PRÓXIMOS PASSOS PRIORITÁRIOS

### 🔥 SPRINT 1: FUNDAÇÃO CRÍTICA (Semana 1-2)
**Objetivo:** Estabelecer infraestrutura base que está bloqueando tudo

**Tasks em Ordem de Execução:**

1. **TASK 1.1: Setup MinIO** (Dia 1-2)
   - 🎯 Bloqueia tudo
   - 📍 Criar buckets Bronze/Silver/Gold
   - 📍 Migrar CSV existentes para MinIO
   - ✅ Critério: MinIO rodando + dados migrados

2. **TASK 1.2: Implementar Delta Lake** (Dia 3-7)
   - 🎯 Depende de MinIO
   - 📍 Setup PySpark + Delta Lake
   - 📍 Migrar dados para Delta format
   - ✅ Critério: ACID transactions funcionando

3. **TASK 1.3: Setup dbt** (Dia 8-12)
   - 🎯 Depende de Delta Lake
   - 📍 Criar projeto dbt
   - 📍 Migrar transformações Python → SQL
   - ✅ Critério: 5 staging models rodando

4. **TASK 1.4: Setup Airflow** (Dia 8-12, paralelo com dbt)
   - 🎯 Depende de MinIO + Delta Lake
   - 📍 Substituir orchestrator_service.py
   - 📍 Criar DAGs
   - ✅ Critério: Airflow UI + DAGs rodando

**Resultado Esperado Após Sprint 1:**
- ✅ Infraestrutura base funcionando
- ✅ Dados em Delta Lake (não mais CSV)
- ✅ Transformações versionadas (dbt)
- ✅ Orquestração profissional (Airflow)
- 📈 Progresso: 15% → 40%

---

### 🟡 SPRINT 2: CAMADA DE DADOS (Semana 3-4)
**Objetivo:** Implementar Bronze/Silver com qualidade

**Tasks:**

5. **TASK 2.1: Bronze Layer** (Dia 13-16)
   - Refatorar extractors existentes
   - Salvar em MinIO/Bronze (Parquet)
   - Particionamento year/month/day

6. **TASK 2.2: Silver Layer** (Dia 17-21)
   - Criar dbt staging models
   - Limpeza e validação
   - Testes dbt

7. **TASK 2.3: Great Expectations** (Dia 22-26)
   - Expectation suites
   - Data quality reports
   - Alertas automáticos

**Resultado Esperado Após Sprint 2:**
- ✅ Bronze layer ingerindo dados daily
- ✅ Silver layer com dados limpos
- ✅ Qualidade >95% validada
- 📈 Progresso: 40% → 65%

---

### 🟢 SPRINT 3-4: ANALYTICS + ML OPS (Semana 5-12)
**Objetivo:** Gold layer + MLflow (menor prioridade, pode ser adiado)

**Tasks (em ordem):**

8. **TASK 3.1: Gold Layer (Star Schema)** - Semana 5-6
9. **TASK 3.2: Metabase** - Semana 7
10. **TASK 3.3: dbt Metrics** - Semana 7
11. **TASK 4.1: MLflow** - Semana 9-10
12. **TASK 4.2: Feature Store (Opcional)** - Semana 11-12

**Resultado Esperado Após Sprint 3-4:**
- ✅ Analytics layer completo
- ✅ BI self-service funcionando
- ✅ ML tracking profissional
- 📈 Progresso: 65% → 90%

---

## 🚨 BLOQUEADORES CRÍTICOS IDENTIFICADOS

### 1️⃣ Falta de Cloud Storage
**Problema:** CSV files não escalam, sem backup, sem ACID  
**Solução:** TASK 1.1 (MinIO) - **URGENTE**  
**Impacto:** Bloqueando 100% do roadmap

### 2️⃣ Falta de Delta Lake
**Problema:** Sem transações ACID, sem time travel, sem schema evolution  
**Solução:** TASK 1.2 (Delta Lake) - **URGENTE**  
**Impacto:** Bloqueando Silver/Gold layers

### 3️⃣ Falta de dbt
**Problema:** Transformações não versionadas, sem testes, código duplicado  
**Solução:** TASK 1.3 (dbt) - **URGENTE**  
**Impacto:** Qualidade não garantida

### 4️⃣ Falta de Airflow
**Problema:** Orchestrator básico sem UI, retry, alerting  
**Solução:** TASK 1.4 (Airflow) - **URGENTE**  
**Impacto:** Operações difíceis, debugging complexo

---

## 📊 MÉTRICAS DE PROGRESSO ATUALIZADAS

### Por Fase

| Fase | Planejado | Real Atual | Gap | Próxima Meta |
|------|-----------|------------|-----|---------------|
| **Fase 0: Foundation** | 100% | **15%** | 85% | 40% (após Sprint 1) |
| **Fase 1: Data Foundation** | 100% | **40%** | 60% | 65% (após Sprint 2) |
| **Fase 2: Analytics Layer** | 100% | **0%** | 100% | 25% (após Sprint 3) |
| **Fase 3: ML Ops** | 100% | **10%** | 90% | 50% (após Sprint 4) |
| **Fase 4: Advanced** | 100% | **0%** | 100% | Adiado (post-MVP) |
| **TOTAL** | 100% | **15%** | 85% | **40%** (meta 4 semanas) |

### Por Componente

| Componente | Atual | Meta 4 Sem | Meta 8 Sem | Meta 16 Sem |
|------------|-------|------------|------------|-------------|
| **Storage (MinIO/S3)** | 0% | **100%** | 100% | 100% |
| **Delta Lake** | 0% | **100%** | 100% | 100% |
| **dbt** | 0% | **80%** | 100% | 100% |
| **Airflow** | 20% | **100%** | 100% | 100% |
| **Bronze Layer** | 50% | 80% | **100%** | 100% |
| **Silver Layer** | 0% | 60% | **100%** | 100% |
| **Great Expectations** | 0% | 50% | **100%** | 100% |
| **Gold Layer** | 0% | 0% | 50% | **100%** |
| **Metabase** | 0% | 0% | 50% | **100%** |
| **MLflow** | 0% | 0% | 30% | **100%** |
| **DataHub** | 0% | 0% | 0% | 80% |

---

### FASE 0: FOUNDATION (Semanas 1-2) - **FUNDAÇÃO CRÍTICA**
**Objetivo:** Estabelecer infraestrutura base  
**Progresso Real:** 🔴 **15%** (somente documentação e scripts básicos)  
**Status:** ⚠️ CRÍTICO - Bloqueando todas as outras fases

#### ✅ O Que JÁ FOI FEITO
- ✅ Documentação completa do projeto
- ✅ Scripts Python ETL básicos (clima, economia, 5G)
- ✅ Orchestrator Python com scheduler básico (`schedule` library)
- ✅ PostgreSQL schema inicial
- ⚠️ Docker Compose básico (backend, frontend, scheduler)

#### ❌ O Que FALTA FAZER
- ❌ Cloud Storage (S3/MinIO) - 0% implementado
- ❌ Delta Lake - 0% implementado
- ❌ dbt project - 0% implementado
- ❌ Apache Airflow - 0% implementado
- ❌ Terraform IaC - 0% implementado

#### Stack Tecnológico
```yaml
Storage:
  - Cloud: AWS S3 / Azure Blob / MinIO (self-hosted)
  - Format: Delta Lake (ACID transactions)
  - Partitioning: year/month/day

Transformation:
  - Framework: dbt (data build tool)
  - Language: SQL + Jinja2
  - Testing: dbt tests + Great Expectations

Orchestration:
  - Engine: Apache Airflow 2.x
  - Deployment: Docker Compose / Kubernetes
  - Scheduler: Cron + Event-based

Infrastructure:
  - IaC: Terraform
  - Containers: Docker + Docker Compose
  - CI/CD: GitHub Actions
```

#### Tasks Críticas

##### 🔴 TASK 1.1: Setup Cloud Storage (3-5 dias)
**Prioridade:** CRÍTICA  
**Owner:** Data Engineering Lead  
**Status Atual:** ❌ **NÃO INICIADO** (0%)  
**Impacto:** Bloqueando TUDO - sem storage escalável, nada funciona

**Situação Atual:**
- ❌ Dados armazenados em CSV files (`data/processed/*.csv`, `data/raw/*.csv`)
- ❌ Total: ~27MB de dados (NÃO ESCALA para TB)
- ❌ Sem particionamento, sem ACID, sem versionamento
- ❌ Sem backup automático, sem disaster recovery

**Subtarefas:**
- [ ] **CRÍTICO:** Provisionar MinIO local (alternativa gratuita ao S3)
  - [ ] `nova-corrente-bronze` (raw data) - Parquet files
  - [ ] `nova-corrente-silver` (cleaned data) - Delta Lake
  - [ ] `nova-corrente-gold` (analytics-ready) - Star Schema
- [ ] Configurar MinIO access keys e policies
- [ ] Setup lifecycle policies (Bronze: 90d retention)
- [ ] Migrar dados CSV existentes → MinIO/Parquet
- [ ] Testar upload/download de arquivos
- [ ] Documentar acesso e credenciais

**Dependências:** Nenhuma  
**Bloqueia:** TASK 1.2, 1.3, 1.4, 2.1

**Critérios de Aceite:**
- ✅ MinIO rodando via Docker Compose
- ✅ Buckets criados e acessíveis
- ✅ Dados CSV migrados para Parquet
- ✅ Scripts de teste executados com sucesso
- ✅ Documentação completa

**Alternativa AWS:** Se orçamento permitir, usar AWS S3 ($100-300/mês para ~1TB)

---

##### 🔴 TASK 1.2: Implementar Delta Lake (5-7 dias)
**Prioridade:** CRÍTICA  
**Owner:** Data Engineering Lead  
**Status Atual:** ❌ **NÃO INICIADO** (0%)  
**Impacto:** Sem ACID, sem time travel, sem schema evolution

**Situação Atual:**
- ❌ CSV files sem transações ACID
- ❌ Sem versionamento de dados (não consegue rollback)
- ❌ Sem schema evolution (mudanças quebram sistema)
- ❌ Sem otimização de queries (full scan sempre)
- ❌ Sem compactação eficiente

**Dados Existentes para Migrar:**
```
data/processed/
├── unified_dataset_with_factors.csv (27MB, 118K rows, 31 features)
├── feature_engineered_data.csv
data/training/
├── unknown_train.csv (93,881 rows)
├── unknown_test.csv (23,471 rows)
data/raw/
├── anatel_5g/ (dados brutos 5G)
├── weather/ (dados climáticos)
├── economic/ (dados econômicos)
└── ... (33 subdiretorios)
```

**Subtarefas:**
- [ ] Setup PySpark local (ou Databricks Community Edition)
- [ ] Instalar Delta Lake libraries (`pip install delta-spark`)
- [ ] Criar Bronze layer (raw data)
  - [ ] Migrar `data/raw/**/*.csv` → Parquet → Delta
  - [ ] Implementar particionamento `year/month/day`
  - [ ] Adicionar metadata (source, extraction_time)
- [ ] Criar Silver layer (cleaned data)
  - [ ] Migrar `data/processed/*.csv` → Delta
- [ ] Testar ACID transactions (insert, update, delete)
- [ ] Testar time travel (versioning, rollback)
- [ ] Configurar Z-ordering para queries otimizadas
- [ ] Setup Delta Lake metadata catalog

**Dependências:** TASK 1.1 (MinIO/S3)  
**Bloqueia:** TASK 1.3, 2.1, 2.2

**Critérios de Aceite:**
- ✅ Bronze layer com todos os dados migrados
- ✅ ACID transactions testadas e funcionando
- ✅ Time travel funcionando (rollback para versão anterior)
- ✅ Particionamento por data otimizado
- ✅ Performance: queries 10x mais rápidas que CSV
- ✅ Compressão: 70% redução em storage vs CSV

---

##### 🔴 TASK 1.3: Setup dbt Project (4-6 dias)
**Prioridade:** CRÍTICA  
**Owner:** Analytics Engineer  
**Status Atual:** ❌ **NÃO IMPLEMENTADO** (0%)  
**Impacto:** Transformações não versionadas, sem testes, sem documentação

**Situação Atual:**
- ❌ Transformações em scripts Python (`backend/pipelines/data_processing/*.py`)
- ❌ 19 scripts de processamento SEM versionamento adequado
- ❌ Sem testes automáticos de qualidade
- ❌ Sem documentação automática
- ❌ Código duplicado entre scripts
- ❌ Difícil manutenção e debugging

**Scripts Existentes para Migrar:**
```
backend/pipelines/data_processing/
├── data_aggregation.py
├── data_cleaning.py
├── feature_engineering.py
├── time_series_preparation.py
└── ... (15+ scripts de transformação)
```

**Subtarefas:**
- [ ] Instalar `dbt-core` + `dbt-spark` (para Delta Lake)
- [ ] Criar estrutura do projeto dbt:
  ```
  dbt_nova_corrente/
  ├── dbt_project.yml
  ├── profiles.yml (conexão Delta Lake)
  ├── models/
  │   ├── staging/ (camada Silver)
  │   │   ├── stg_items.sql
  │   │   ├── stg_towers.sql
  │   │   ├── stg_weather.sql
  │   │   ├── stg_economic.sql
  │   │   └── stg_5g.sql
  │   ├── intermediate/
  │   └── marts/ (camada Gold)
  ├── tests/ (validações automáticas)
  ├── macros/ (reorder_point, safety_stock)
  └── docs/
  ```
- [ ] Migrar transformações Python → SQL dbt models
- [ ] Criar testes dbt (not_null, unique, relationships)
- [ ] Configurar CI/CD (GitHub Actions para dbt test/run)
- [ ] Gerar dbt docs (documentação HTML automática)

**Dependências:** TASK 1.2 (Delta Lake)  
**Bloqueia:** TASK 2.2, 2.3, 3.1

**Critérios de Aceite:**
- ✅ dbt project inicializado e funcionando
- ✅ Conexão com Delta Lake testada
- ✅ Pelo menos 5 staging models rodando (stg_items, stg_towers, etc.)
- ✅ Testes dbt passando (100% coverage)
- ✅ CI/CD configurado (GitHub Actions)
- ✅ Documentação HTML gerada (dbt docs generate)

---

##### 🔴 TASK 1.4: Setup Apache Airflow (4-6 dias)
**Prioridade:** CRÍTICA  
**Owner:** Data Engineering Lead  
**Status Atual:** ⚠️ **20% PARCIAL** (apenas Python scheduler básico)  
**Impacto:** Sem orquestração visual, sem retry automático, difícil monitoramento

**Situação Atual:**
- ⚠️ **JÁ EXISTE:** `orchestrator_service.py` com scheduler básico
  - Usa biblioteca `schedule` (Python puro)
  - Threading básico para execução
  - Sem UI, sem visualização de DAGs
  - Sem retry automático
  - Sem alerting integrado
  - Difícil debugging

**Código Existente:**
```python
# backend/pipelines/orchestrator_service.py
class OrchestratorService:
    def start_scheduler(self, time_str: str = "02:00"):
        schedule.every().day.at(time_str).do(self.run_complete_pipeline)
        # Threading básico - sem Airflow
```

**O Que FALTA:**
- ❌ Apache Airflow Web UI (visualização de DAGs)
- ❌ Retry policies automáticas
- ❌ Dependências entre tasks visuais
- ❌ Alerting integrado (Slack/Email)
- ❌ Logs centralizados e searchable
- ❌ Backfill automático

**Subtarefas:**
- [ ] Setup Airflow via Docker Compose
  - [ ] Web server (port 8080)
  - [ ] Scheduler
  - [ ] Worker (Celery executor)
  - [ ] PostgreSQL metadata DB
  - [ ] Redis (message broker)
- [ ] Configurar conexões Airflow:
  - [ ] MinIO/S3 connection
  - [ ] Delta Lake/Spark connection
  - [ ] PostgreSQL connection
- [ ] Criar DAGs (migrar de orchestrator_service.py):
  - [ ] `extract_bronze_dag.py` (ingestão daily)
  - [ ] `bronze_to_silver_dag.py` (limpeza + validação)
  - [ ] `silver_to_gold_dag.py` (analytics layer)
- [ ] Migrar lógica de `orchestrator_service.py` → Airflow DAGs
- [ ] Configurar retry policies (3 tentativas, exponential backoff)
- [ ] Setup alerting (Slack webhook ou Email SMTP)
- [ ] Configurar monitoring dashboard

**Dependências:** TASK 1.1 (MinIO), TASK 1.2 (Delta Lake)  
**Bloqueia:** TASK 2.1, 2.2, 2.3

**Critérios de Aceite:**
- ✅ Airflow rodando (web UI acessível em localhost:8080)
- ✅ Pelo menos 3 DAGs criados e executando
- ✅ Retry funcionando (testar com falha proposital)
- ✅ Alertas configurados (Slack ou Email)
- ✅ Logs centralizados e searchable
- ✅ `orchestrator_service.py` depreciado (substituído por Airflow)

---

### FASE 1: DATA FOUNDATION (Semanas 3-4) - **CAMADA DE DADOS**
**Objetivo:** Implementar Bronze/Silver layers  
**Progresso Real:** 🟡 **40%** (pipelines ETL existem, mas sem Medallion architecture)  
**Status:** ⚠️ PARCIAL - Precisa refatorar para Bronze/Silver

#### ✅ O Que JÁ FOI FEITO
- ✅ **Pipelines ETL implementados:**
  - `anatel_5g_etl.py` - Extração dados 5G da Anatel
  - `climate_etl.py` - Extração dados climáticos
  - `economic_etl.py` - Extração dados econômicos
  - `brazilian_calendar_etl.py` - Calendário brasileiro (feriados)
  - `feature_calculation_etl.py` - Cálculo de 73 features
- ✅ Data collectors em `backend/data/collectors/`
- ✅ Data loaders em `backend/data/loaders/`
- ✅ Feature engineering básico implementado

#### ❌ O Que FALTA FAZER
- ❌ Bronze Layer (raw data em Delta Lake) - 0%
- ❌ Silver Layer (cleaned data em Delta Lake) - 0%
- ❌ Particionamento year/month/day - 0%
- ❌ Great Expectations (validação automática) - 0%
- ❌ dbt staging models - 0%
- ❌ Data quality reports automáticos - 0%

#### Arquitetura Medallion

```
┌─────────────────────────────────────────────────────────────┐
│                        SOURCES                               │
│  ERP | Weather API | Economic API | 5G API | Manual Uploads │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    BRONZE LAYER (Raw)                        │
│  - Formato: Parquet + Delta Lake                            │
│  - Particionamento: year/month/day                          │
│  - Retenção: 90 dias                                        │
│  - Schema: Exactly as source                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   SILVER LAYER (Cleaned)                     │
│  - Transformação: dbt staging models                        │
│  - Validação: Great Expectations                            │
│  - Deduplicação, limpeza, type casting                      │
│  - Schema validado e documentado                            │
└─────────────────────────────────────────────────────────────┘
```

#### Tasks Principais

##### 🟡 TASK 2.1: Criar Bronze Layer (3-4 dias)
**Prioridade:** ALTA  
**Owner:** Data Engineer  
**Status Atual:** ⚠️ **50% PARCIAL** (extractors existem, falta Bronze layer)  
**Impacto:** Dados brutos não organizados, sem particionamento

**Situação Atual:**
- ✅ **JÁ EXISTEM extractors:**
  - `climate_etl.py` - Weather API (OpenWeather implementado)
  - `economic_etl.py` - Economic API (Banco Central implementado)
  - `anatel_5g_etl.py` - 5G API (Anatel implementado)
  - `brazilian_calendar_etl.py` - Calendário brasileiro
- ⚠️ **MAS:** Salvam em CSV (`data/raw/`), não em Bronze Layer
- ❌ Sem particionamento year/month/day
- ❌ Sem metadata padronizada (extraction_time, source)
- ❌ Sem Airflow DAG (apenas `orchestrator_service.py`)

**O Que FALTA:**
- ❌ Refatorar extractors para salvar em MinIO/Bronze (Parquet)
- ❌ Implementar particionamento automático
- ❌ Adicionar metadata padronizada
- ❌ Migrar de orchestrator_service.py → Airflow DAG

**Subtarefas:**
- [ ] **Refatorar extractors existentes:**
  - [ ] Modificar `climate_etl.py` → salvar em MinIO/Bronze/Parquet
  - [ ] Modificar `economic_etl.py` → salvar em MinIO/Bronze/Parquet
  - [ ] Modificar `anatel_5g_etl.py` → salvar em MinIO/Bronze/Parquet
  - [ ] Modificar `brazilian_calendar_etl.py` → salvar em MinIO/Bronze/Parquet
- [ ] Implementar particionamento year/month/day em cada extractor
- [ ] Adicionar metadata padrão:
  ```python
  metadata = {
      'extraction_time': datetime.now(),
      'source': 'anatel_api',
      'dataset_id': 'bronze_5g_towers',
      'version': '1.0'
  }
  ```
- [ ] Criar Airflow DAG `extract_bronze_dag.py`:
  ```python
  extract_climate >> extract_economic >> extract_5g >> extract_calendar
  ```
- [ ] Setup monitoring de ingestão (alertas se falhar)

**Dependências:** TASK 1.1 (MinIO), TASK 1.4 (Airflow)  
**Bloqueia:** TASK 2.2

**Critérios de Aceite:**
- ✅ Dados brutos salvos em MinIO/Bronze (Parquet + Delta)
- ✅ Particionamento year/month/day funcionando
- ✅ Metadata padronizada em todos os datasets
- ✅ Airflow DAG executando diariamente
- ✅ Monitoring configurado (alertas em caso de falha)

---

##### 🟡 TASK 2.2: Criar Silver Layer - dbt Staging (5-7 dias)
**Prioridade:** ALTA  
**Owner:** Analytics Engineer

**Subtarefas:**
- [ ] Criar dbt staging models:
  - [ ] `stg_items.sql` (limpeza de itens)
  - [ ] `stg_towers.sql` (limpeza de torres)
  - [ ] `stg_forecasts.sql` (limpeza de previsões)
  - [ ] `stg_weather.sql`
  - [ ] `stg_economic.sql`
  - [ ] `stg_5g.sql`
- [ ] Implementar transformações:
  - Trim strings
  - Lowercase/normalize categoricals
  - Type casting (int, float, date)
  - Remove duplicates
  - Handle nulls
- [ ] Criar testes dbt:
  - `not_null` tests
  - `unique` tests
  - `relationships` tests (FK validation)
  - Custom tests (business logic)
- [ ] Materializar como Delta tables (Silver layer)
- [ ] Documentar modelos (schema.yml)

**Dependências:** TASK 1.3 (dbt), TASK 2.1 (Bronze)  
**Bloqueia:** TASK 2.3, 3.1

**Critérios de Aceite:**
- ✅ Staging models criados e testados
- ✅ Dados limpos em Silver layer
- ✅ Testes dbt passando
- ✅ Documentação completa

---

##### 🟡 TASK 2.3: Setup Great Expectations (4-6 dias)
**Prioridade:** ALTA  
**Owner:** Data Quality Engineer

**Subtarefas:**
- [ ] Instalar Great Expectations
- [ ] Criar expectation suites:
  - [ ] `items_expectations.json`
    - expect_column_values_to_not_be_null
    - expect_column_values_to_be_unique
    - expect_column_values_to_be_in_set
  - [ ] `towers_expectations.json`
  - [ ] `forecasts_expectations.json`
- [ ] Configurar checkpoints (validation points)
- [ ] Integrar com Airflow (validation task)
- [ ] Gerar data docs (HTML reports)
- [ ] Configurar alertas (Slack/Email)
- [ ] Setup historical validation tracking

**Dependências:** TASK 2.2 (Silver Layer)  
**Bloqueia:** TASK 3.1

**Critérios de Aceite:**
- ✅ Expectation suites criadas
- ✅ Checkpoints configurados
- ✅ Validação automática funcionando
- ✅ Data docs gerados
- ✅ Alertas configurados

---

### FASE 2: ANALYTICS LAYER (Semanas 5-8) - **CAMADA ANALÍTICA**
**Objetivo:** Implementar Gold layer (Star Schema)  
**Progresso Real:** ❌ **0%** (nada implementado)  
**Status:** 🔴 CRÍTICO - Bloqueado por Fase 0 e 1

#### ✅ O Que JÁ FOI FEITO
- ⚠️ PostgreSQL schema inicial existe (`backend/data/Nova_Corrente_ML_Ready_DB.sql`)
- ⚠️ Mas NÃO é modelagem dimensional (star schema)

#### ❌ O Que FALTA FAZER
- ❌ Gold Layer (Star Schema) - 0%
- ❌ Dimensões (dim_items, dim_towers, dim_time) - 0%
- ❌ Fatos (fact_forecasts, fact_inventory) - 0%
- ❌ dbt marts - 0%
- ❌ Metabase - 0%
- ❌ dbt Metrics - 0%
- ❌ BI Dashboards - 0%

**Bloqueador:** Fase 0 (Delta Lake, dbt) e Fase 1 (Silver layer) precisam estar completos primeiro

#### Modelagem Dimensional

```
┌─────────────────────────────────────────────────────────────┐
│                     GOLD LAYER (Analytics)                   │
│                                                              │
│  ┌──────────────┐     ┌──────────────────┐                 │
│  │  dim_items   │     │ fact_forecasts   │                 │
│  ├──────────────┤     ├──────────────────┤                 │
│  │ item_id (PK) │◄────┤ item_id (FK)     │                 │
│  │ item_name    │     │ tower_id (FK)    │                 │
│  │ category     │     │ date_id (FK)     │                 │
│  │ supplier     │     │ forecasted_qty   │                 │
│  └──────────────┘     │ actual_qty       │                 │
│                       │ mape             │                 │
│  ┌──────────────┐     └──────────────────┘                 │
│  │ dim_towers   │                                           │
│  ├──────────────┤     ┌──────────────────┐                 │
│  │ tower_id(PK) │◄────┤ fact_inventory   │                 │
│  │ tower_name   │     ├──────────────────┤                 │
│  │ region       │     │ item_id (FK)     │                 │
│  │ 5g_status    │     │ tower_id (FK)    │                 │
│  └──────────────┘     │ date_id (FK)     │                 │
│                       │ stock_level      │                 │
│  ┌──────────────┐     │ reorder_point    │                 │
│  │  dim_time    │     │ safety_stock     │                 │
│  ├──────────────┤     └──────────────────┘                 │
│  │ date_id (PK) │                                           │
│  │ date         │◄────────────────────────┘                 │
│  │ year         │                                           │
│  │ month        │                                           │
│  │ day_of_week  │                                           │
│  │ is_holiday   │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

#### Tasks Principais

##### 🟢 TASK 3.1: Criar Gold Layer - Star Schema (7-10 dias)
**Prioridade:** MÉDIA  
**Owner:** Analytics Engineer

**Subtarefas:**
- [ ] Criar dimensões (dbt marts):
  - [ ] `dim_items.sql`
    ```sql
    -- SCD Type 2 para histórico de mudanças
    SELECT
      item_id,
      item_name,
      category,
      supplier,
      valid_from,
      valid_to,
      is_current
    FROM {{ ref('stg_items') }}
    ```
  - [ ] `dim_towers.sql`
  - [ ] `dim_time.sql` (calendar dimension)
- [ ] Criar fatos:
  - [ ] `fact_forecasts.sql`
    ```sql
    -- Grain: item x tower x date
    SELECT
      i.item_id,
      t.tower_id,
      d.date_id,
      f.forecasted_qty,
      f.actual_qty,
      ABS(f.forecasted_qty - f.actual_qty) / f.actual_qty AS mape
    FROM {{ ref('stg_forecasts') }} f
    LEFT JOIN {{ ref('dim_items') }} i ON f.item = i.item_name
    LEFT JOIN {{ ref('dim_towers') }} t ON f.tower = t.tower_name
    LEFT JOIN {{ ref('dim_time') }} d ON f.date = d.date
    ```
  - [ ] `fact_inventory.sql`
- [ ] Configurar particionamento e clustering
- [ ] Materializar como Delta tables (Gold layer)
- [ ] Criar testes dbt (referential integrity)
- [ ] Documentar modelos (ER diagram)

**Dependências:** TASK 2.2 (Silver Layer)  
**Bloqueia:** TASK 3.2, 3.3

**Critérios de Aceite:**
- ✅ Star schema implementado
- ✅ Dimensões e fatos materializados
- ✅ Testes de integridade passando
- ✅ Performance otimizada (< 3s queries)
- ✅ Documentação completa

---

##### 🟢 TASK 3.2: Setup Metabase (2-3 dias)
**Prioridade:** MÉDIA  
**Owner:** BI Engineer

**Subtarefas:**
- [ ] Setup Metabase via Docker Compose
- [ ] Conectar com Gold layer (via Spark JDBC)
- [ ] Criar dashboards básicos:
  - [ ] **Forecast Accuracy Dashboard**
    - MAPE por item
    - MAPE por torre
    - MAPE trend (temporal)
  - [ ] **Inventory Levels Dashboard**
    - Stock atual por item
    - Items abaixo do reorder point
    - Safety stock coverage
  - [ ] **Demand Forecast Dashboard**
    - Previsões próximos 30 dias
    - Comparação com histórico
- [ ] Configurar usuários e permissões
- [ ] Setup scheduled email reports

**Dependências:** TASK 3.1 (Gold Layer)  
**Bloqueia:** Nenhuma

**Critérios de Aceite:**
- ✅ Metabase rodando e acessível
- ✅ Dashboards criados e funcionais
- ✅ Usuários configurados
- ✅ Reports agendados

---

##### 🟢 TASK 3.3: Criar dbt Metrics (3-4 dias)
**Prioridade:** MÉDIA  
**Owner:** Analytics Engineer

**Subtarefas:**
- [ ] Criar `metrics.yml` com métricas de negócio:
  ```yaml
  metrics:
    - name: forecast_accuracy
      label: Forecast Accuracy (MAPE)
      type: average
      sql: mape
      timestamp: date
      time_grains: [day, week, month]
      dimensions: [item_id, tower_id]
  
    - name: total_forecasted_demand
      label: Total Forecasted Demand
      type: sum
      sql: forecasted_qty
      timestamp: date
  
    - name: inventory_turnover
      label: Inventory Turnover
      type: derived
      sql: total_demand / avg_inventory
  ```
- [ ] Testar métricas (dbt run-metrics)
- [ ] Expor via dbt Semantic Layer API
- [ ] Integrar com Metabase

**Dependências:** TASK 3.1 (Gold Layer)  
**Bloqueia:** Nenhuma

**Critérios de Aceite:**
- ✅ Métricas definidas e testadas
- ✅ Semantic Layer API funcionando
- ✅ Metabase consumindo métricas

---

### FASE 3: ML OPS (Semanas 9-12) - **MACHINE LEARNING OPS**
**Objetivo:** Implementar MLflow e Feature Store  
**Progresso Real:** ⚠️ **10%** (model registry básico existe)  
**Status:** 🟡 PARCIAL - ML existe, mas sem MLflow

⚠️ **IMPORTANTE:** Seguindo a política [GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md](./clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md), o ML Ops NÃO estará no deployment de produção. Apenas resultados pré-computados serão expostos.

#### ✅ O Que JÁ FOI FEITO
- ✅ **Modelos ML implementados:**
  - `backend/ml/models/` - Prophet, ARIMA, LSTM implementados
  - `backend/ml/training/` - Scripts de treinamento
  - `backend/ml/inference/` - Scripts de inferência
- ✅ Model registry básico: `backend/services/ml_models/model_registry.py`
- ✅ Feature engineering: 73 features calculadas
- ⚠️ **MAS:** Modelos salvos em Pickle local, sem versionamento adequado

#### ❌ O Que FALTA FAZER
- ❌ MLflow (experiment tracking, model registry, serving) - 0%
- ❌ Feature Store (Feast/Tecton) - 0%
- ❌ Model monitoring (drift detection) - 0%
- ❌ A/B testing setup - 0%
- ❌ Precomputed results pipeline (para deployment) - 0%

#### Tasks Principais

##### 🟢 TASK 4.1: Setup MLflow (4-6 dias)
**Prioridade:** MÉDIA  
**Owner:** ML Engineer

**Subtarefas:**
- [ ] Setup MLflow via Docker Compose
  - Tracking Server
  - Model Registry
  - Artifact Store (S3)
  - Backend Store (PostgreSQL)
- [ ] Integrar MLflow tracking nos modelos:
  - [ ] Prophet model
  - [ ] ARIMA model
  - [ ] LSTM model
- [ ] Configurar experiment tracking:
  ```python
  import mlflow
  
  with mlflow.start_run():
      mlflow.log_params({"horizon": 30, "seasonality": "weekly"})
      mlflow.log_metrics({"mape": 0.12, "rmse": 45.3})
      mlflow.log_model(model, "prophet_model")
  ```
- [ ] Criar model registry (staging, production)
- [ ] Configurar model serving (REST API)
- [ ] Setup monitoring de modelos (drift detection)

**Dependências:** Nenhuma (pode ser paralelo)  
**Bloqueia:** Nenhuma

**Critérios de Aceite:**
- ✅ MLflow rodando (web UI acessível)
- ✅ Experiment tracking funcionando
- ✅ Model registry criado
- ✅ Model serving testado

---

##### 🟢 TASK 4.2: Feature Store (Opcional) (7-10 dias)
**Prioridade:** BAIXA  
**Owner:** ML Engineer

**Subtarefas:**
- [ ] Avaliar Feast vs Tecton
- [ ] Setup feature store escolhido
- [ ] Migrar features existentes (73 features):
  - Temporal features (lags, rolling windows)
  - Weather features
  - Economic features
  - 5G features
- [ ] Criar feature views
- [ ] Integrar com ML training
- [ ] Setup feature monitoring

**Dependências:** TASK 4.1 (MLflow)  
**Bloqueia:** Nenhuma

**Critérios de Aceite:**
- ✅ Feature store rodando
- ✅ Features migradas
- ✅ Feature serving funcionando

---

### FASE 4: ADVANCED FEATURES (Semanas 13-16) - **RECURSOS AVANÇADOS**
**Objetivo:** Implementar Data Catalog e otimizações  
**Progresso Real:** ❌ **0%** (nada implementado)  
**Status:** 🔴 NÃO INICIADO - Menor prioridade

#### ❌ O Que FALTA FAZER
- ❌ DataHub (data catalog) - 0%
- ❌ Lineage tracking - 0%
- ❌ Performance optimization (Z-ordering, clustering) - 0%
- ❌ Streaming pipeline (Kafka, Flink) - 0%
- ❌ Self-service analytics - 0%

**Nota:** Fase 4 é opcional para MVP, pode ser adiada se houver restrição de tempo/orçamento

#### Tasks Principais

##### 🟡 TASK 5.1: Setup DataHub (4-6 dias)
**Prioridade:** BAIXA  
**Owner:** Data Engineer

**Subtarefas:**
- [ ] Setup DataHub via Docker Compose
- [ ] Ingestar metadata de datasets:
  - Delta Lake tables
  - dbt models
  - Airflow DAGs
- [ ] Configurar lineage tracking
- [ ] Adicionar ownership e tags
- [ ] Configurar search e discovery
- [ ] Integrar com autenticação (SSO)

**Dependências:** Nenhuma (pode ser paralelo)  
**Bloqueia:** Nenhuma

**Critérios de Aceite:**
- ✅ DataHub rodando (web UI acessível)
- ✅ Metadata ingestado
- ✅ Lineage visualizado
- ✅ Search funcionando

---

##### 🟡 TASK 5.2: Performance Optimization (5-7 dias)
**Prioridade:** BAIXA  
**Owner:** Data Engineer

**Subtarefas:**
- [ ] Implementar Z-ordering em Delta tables
- [ ] Configurar liquid clustering
- [ ] Otimizar particionamento
- [ ] Setup caching (Redis/Memcached)
- [ ] Implementar query pushdown
- [ ] Benchmark performance (before/after)

**Dependências:** TASK 3.1 (Gold Layer)  
**Bloqueia:** Nenhuma

**Critérios de Aceite:**
- ✅ Query performance < 3s
- ✅ Storage efficiency > 70%
- ✅ Benchmark completo

---

##### 🟡 TASK 5.3: Streaming Pipeline (Opcional) (10-14 dias)
**Prioridade:** BAIXA  
**Owner:** Data Engineer

**Subtarefas:**
- [ ] Setup Kafka cluster
- [ ] Criar topics (items, forecasts, alerts)
- [ ] Implementar Kafka producers
- [ ] Setup Flink/Spark Streaming
- [ ] Criar streaming jobs
- [ ] Integrar com batch pipelines (Lambda architecture)
- [ ] Setup monitoring (Prometheus + Grafana)

**Dependências:** TASK 1.4 (Airflow)  
**Bloqueia:** Nenhuma

**Critérios de Aceite:**
- ✅ Kafka rodando
- ✅ Streaming jobs processando dados
- ✅ Alertas em tempo real funcionando

---

## 📈 TRACKING & MONITORING

### KPIs por Fase

| Fase | KPI | Meta | Como Medir |
|------|-----|------|------------|
| **Fase 0** | Infrastructure Up | 100% | Todos os serviços rodando |
| **Fase 1** | Data Quality Score | >95% | Great Expectations reports |
| **Fase 2** | Query Performance | <3s | Benchmark queries |
| **Fase 3** | Model Accuracy | MAPE <15% | MLflow metrics |
| **Fase 4** | Data Discovery | >90% | DataHub usage metrics |

### Monitoring Dashboard

```yaml
Metrics to Track:
  - Pipeline Success Rate (target: >99%)
  - Data Freshness (target: <1h delay)
  - Storage Growth (monitor monthly)
  - Query Performance (P95 <3s)
  - Data Quality Score (>95%)
  - Model Performance (MAPE <15%)
```

---

## 🚨 RISK MANAGEMENT

### Riscos Identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| **Cloud costs exceeding budget** | Alta | Alto | Start with MinIO (self-hosted), migrate later |
| **Team lacks dbt experience** | Média | Médio | Training + pair programming |
| **Data sources unstable** | Alta | Alto | Implement retry logic + alerting |
| **Performance issues** | Média | Alto | Early benchmarking + optimization |
| **Scope creep** | Alta | Médio | Strict phase gates + sign-offs |

### Contingency Plans

1. **Budget Overrun:** Usar MinIO ao invés de S3
2. **Timeline Delay:** Priorizar Fase 0-1, adiar Fase 4
3. **Technical Blocker:** Escalar para arquiteto sênior

---

## ✅ DEFINITION OF DONE

### Por Fase

#### Fase 0: Foundation
- [ ] S3 buckets provisionados e acessíveis
- [ ] Delta Lake com dados migrados
- [ ] dbt project com pelo menos 1 modelo funcionando
- [ ] Airflow com pelo menos 1 DAG executando
- [ ] CI/CD configurado (GitHub Actions)
- [ ] Documentação técnica completa

#### Fase 1: Data Foundation
- [ ] Bronze layer ingerindo dados diariamente
- [ ] Silver layer com staging models materializados
- [ ] Great Expectations validando qualidade (>95% score)
- [ ] Testes dbt passando (100% coverage)
- [ ] Data profiling reports gerados

#### Fase 2: Analytics Layer
- [ ] Gold layer com star schema implementado
- [ ] Metabase com dashboards criados
- [ ] dbt metrics funcionando
- [ ] Query performance <3s (P95)
- [ ] BI users treinados

#### Fase 3: ML Ops
- [ ] MLflow tracking funcionando
- [ ] Model registry com modelos versionados
- [ ] Feature store implementado (opcional)
- [ ] Model serving testado
- [ ] Monitoring de modelos configurado

#### Fase 4: Advanced
- [ ] DataHub catalog populado
- [ ] Performance otimizado (70% storage savings)
- [ ] Streaming pipeline funcionando (opcional)
- [ ] Governança completa (lineage, ownership)

---

## 📚 DOCUMENTATION & TRAINING

### Documentação Necessária

1. **Architecture Diagrams**
   - Data flow diagrams
   - Infrastructure diagrams
   - Network diagrams

2. **Technical Docs**
   - dbt model documentation
   - Airflow DAG documentation
   - API documentation

3. **Runbooks**
   - Incident response
   - Deployment procedures
   - Backup/restore procedures

4. **User Guides**
   - Metabase user guide
   - DataHub search guide
   - Self-service analytics guide

### Training Plan

| Audience | Training | Duration |
|----------|----------|----------|
| **Data Engineers** | dbt + Airflow workshop | 2 dias |
| **Analytics Engineers** | dbt advanced patterns | 1 dia |
| **BI Users** | Metabase self-service | 4 horas |
| **Developers** | Data catalog usage | 2 horas |

---

## 🎯 NEXT STEPS

### Immediate Actions (This Week)

1. **Setup Project Kickoff Meeting**
   - Align on roadmap
   - Assign owners
   - Set up communication channels

2. **Provision Infrastructure**
   - Create AWS/GCP accounts (ou setup MinIO)
   - Setup GitHub repository
   - Configure CI/CD

3. **Start TASK 1.1: Cloud Storage**
   - Create S3 buckets
   - Configure IAM
   - Test connectivity

### Week 2-4 Focus

- Complete Fase 0 (Foundation)
- Start Fase 1 (Data Foundation)
- Weekly sync meetings
- Risk monitoring

---

## 📞 STAKEHOLDER COMMUNICATION

### Weekly Status Report Template

```markdown
# Data Engineering Weekly Status - Week X

## Progress
- ✅ Completed: [Task list]
- 🚧 In Progress: [Task list]
- 🔴 Blocked: [Task list with blockers]

## Metrics
- Data Quality Score: XX%
- Pipeline Success Rate: XX%
- Storage Used: XX GB

## Risks & Issues
- [List of active risks]
- [Mitigation actions]

## Next Week Plan
- [Task list]
```

### Monthly Steering Committee Review

- Phase completion status
- Budget vs actual
- Risk register update
- Go/No-Go decision for next phase

---

## 📊 APPENDIX

### A. Technology Stack Details

```yaml
Storage:
  - Delta Lake 2.x
  - AWS S3 / Azure Blob / MinIO

Transformation:
  - dbt-core 1.7+
  - dbt-databricks / dbt-spark

Orchestration:
  - Apache Airflow 2.8+
  - Celery executor

Data Quality:
  - Great Expectations 0.18+

ML Ops:
  - MLflow 2.10+
  - Feast 0.35+ (optional)

BI:
  - Metabase 0.48+
  - Apache Superset (optional)

Data Catalog:
  - DataHub 0.12+

Streaming (Optional):
  - Apache Kafka 3.6+
  - Apache Flink 1.18+
```

### B. Cost Estimation

| Component | Monthly Cost (USD) | Notes |
|-----------|-------------------|-------|
| **S3 Storage** | $100-300 | ~1TB data |
| **Compute (Airflow)** | $200-400 | t3.large EC2 |
| **Delta Lake (Databricks)** | $500-1000 | Community edition free |
| **Monitoring** | $50-100 | CloudWatch/Datadog |
| **Total** | **$850-1800** | Or $0 with self-hosted MinIO |

**Self-Hosted Alternative:** ~$200/month (bare metal servers)

### C. Team Structure

```
Data Engineering Team (4-6 pessoas)
├── Data Engineering Lead (1)
│   └── Responsável por Fase 0-1
├── Analytics Engineer (1-2)
│   └── Responsável por dbt + Fase 2
├── ML Engineer (1)
│   └── Responsável por Fase 3
└── Data Quality Engineer (1)
    └── Responsável por Great Expectations
```

---

**Documento criado:** Novembro 2025  
**Versão:** 3.0  
**Status:** ✅ Roadmap Atualizado - Status Real Baseado em Diagnóstico Completo

**Referências:**
- [Diagnóstico Completo](./COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md) - Gap analysis detalhado
- [Lista de Tarefas Críticas](./CRITICAL_TASKS_PRIORITY_LIST_PT_BR.md) - Tasks priorizadas
- [Constraints Globais](./clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Política de ML Ops

**Resumo de Mudanças (v3.0):**
- ✅ Adicionado status real de implementação baseado em código existente
- ✅ Identificado o que JÁ FOI FEITO (15%) vs. o que FALTA (85%)
- ✅ Atualizado progresso por fase e componente
- ✅ Adicionado bloqueadores críticos identificados
- ✅ Criado plano de sprints prioritário (Sprint 1-2 críticos)
- ✅ Detalhado situação atual de cada task com arquivos existentes
- ✅ Adicionado métricas de progresso realistas (0% → 40% → 65% → 90%)

**Próxima Ação Imediata:**
🔴 **TASK 1.1: Setup MinIO** - Bloqueando TUDO, começar HOJE!
