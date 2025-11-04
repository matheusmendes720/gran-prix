# 🎯 LISTA DE TAREFAS CRÍTICAS - PRIORIZADA
## Nova Corrente - Tarefas Fundamentais (Bottom-Up)

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ⚠️ Ação Imediata Necessária

---

## 🔴 TIER 1: FUNDAÇÃO CRÍTICA (Semanas 1-2)

### TASK 1.1: Setup Cloud Storage (S3/MinIO) 🔴🔴🔴
**Prioridade:** MÁXIMA  
**Tempo:** 3-5 dias  
**Blocos:** TASK 1.2, 1.3, 1.4

**Checklist:**
- [ ] Criar conta AWS (ou setup MinIO local para dev)
- [ ] Criar S3 buckets:
  - [ ] `nova-corrente-data-lake-bronze`
  - [ ] `nova-corrente-data-lake-silver`
  - [ ] `nova-corrente-data-lake-gold`
- [ ] Configurar IAM roles e policies
- [ ] Testar upload/download de arquivos
- [ ] Configurar lifecycle policies (retenção 90 dias Bronze)

**Dependências:** Nenhuma  
**Impacto:** Bloqueia TODO o resto do roadmap

---

### TASK 1.2: Implementar Delta Lake 🔴🔴🔴
**Prioridade:** MÁXIMA  
**Tempo:** 5-7 dias  
**Blocos:** TASK 1.3, 1.4, 2.1

**Checklist:**
- [ ] Instalar Delta Lake (PySpark ou standalone)
- [ ] Configurar Spark session com Delta extensions
- [ ] Criar Bronze layer (Parquet → Delta)
- [ ] Migrar dados CSV existentes → Parquet → Delta
- [ ] Testar ACID transactions
- [ ] Testar time travel (versionamento)
- [ ] Configurar Z-ordering e clustering

**Dependências:** TASK 1.1 (S3)  
**Impacto:** Fundação para todo storage

---

### TASK 1.3: Setup dbt Project 🔴🔴🔴
**Prioridade:** MÁXIMA  
**Tempo:** 4-6 dias  
**Blocos:** TASK 2.1, 2.2, 2.3

**Checklist:**
- [ ] Instalar `dbt-core` + `dbt-databricks` (ou `dbt-spark`)
- [ ] Criar `dbt_project.yml` com configuração básica
- [ ] Criar `profiles.yml` (conexão Delta Lake)
- [ ] Criar estrutura de diretórios:
  - [ ] `models/staging/`
  - [ ] `models/intermediate/`
  - [ ] `models/marts/`
  - [ ] `tests/`
  - [ ] `macros/`
- [ ] Criar primeiro modelo staging (`stg_items.sql`)
- [ ] Testar conexão e execução (`dbt run`, `dbt test`)
- [ ] Configurar CI/CD (GitHub Actions)

**Dependências:** TASK 1.2 (Delta Lake)  
**Impacto:** Transformações versionadas e testadas

---

### TASK 1.4: Setup Airflow 🔴🔴🔴
**Prioridade:** MÁXIMA  
**Tempo:** 4-6 dias  
**Blocos:** TASK 2.1, 2.2, 2.3

**Checklist:**
- [ ] Setup Airflow (Docker Compose ou managed service)
- [ ] Configurar conexões:
  - [ ] S3 connection
  - [ ] Delta Lake connection
  - [ ] Database connection
- [ ] Criar primeiro DAG (extract → bronze → silver)
- [ ] Migrar `orchestrator_service.py` → Airflow DAG
- [ ] Configurar retry policies (3 tentativas)
- [ ] Configurar alerting (Slack/Email)
- [ ] Testar execução e monitoramento

**Dependências:** TASK 1.1 (S3), TASK 1.2 (Delta Lake)  
**Impacto:** Orquestração profissional

---

## 🟡 TIER 2: DATA FOUNDATION (Semanas 3-4)

### TASK 2.1: Criar Bronze Layer 🟡🟡
**Prioridade:** ALTA  
**Tempo:** 3-4 dias  
**Blocos:** TASK 2.2

**Checklist:**
- [ ] Criar extractors para cada fonte:
  - [ ] ERP extractor
  - [ ] Weather API extractor
  - [ ] Economic API extractor
  - [ ] 5G API extractor
- [ ] Implementar particionamento `year/month/day`
- [ ] Salvar em Parquet no Bronze (S3)
- [ ] Validar schema e tipos
- [ ] Testar ingestão diária

**Dependências:** TASK 1.1 (S3), TASK 1.4 (Airflow)  
**Impacto:** Dados brutos organizados

---

### TASK 2.2: Criar Silver Layer (dbt Staging) 🟡🟡
**Prioridade:** ALTA  
**Tempo:** 5-7 dias  
**Blocos:** TASK 2.3, 3.1

**Checklist:**
- [ ] Criar dbt staging models:
  - [ ] `stg_items.sql`
  - [ ] `stg_towers.sql`
  - [ ] `stg_forecasts.sql`
- [ ] Implementar limpeza de dados:
  - [ ] Trim strings
  - [ ] Lowercase categoricals
  - [ ] Type casting
  - [ ] Remove duplicates
- [ ] Validar schema
- [ ] Materializar como Delta tables (Silver layer)
- [ ] Criar testes dbt:
  - [ ] `not_null` tests
  - [ ] `unique` tests
  - [ ] `relationships` tests

**Dependências:** TASK 1.3 (dbt), TASK 2.1 (Bronze)  
**Impacto:** Dados limpos e validados

---

### TASK 2.3: Setup Great Expectations 🟡🟡
**Prioridade:** ALTA  
**Tempo:** 4-6 dias  
**Blocos:** TASK 3.1

**Checklist:**
- [ ] Instalar Great Expectations
- [ ] Criar expectation suites:
  - [ ] `items_expectations.json`
  - [ ] `towers_expectations.json`
  - [ ] `forecasts_expectations.json`
- [ ] Configurar checkpoints
- [ ] Integrar com Airflow (validation task)
- [ ] Gerar data docs (relatórios HTML)
- [ ] Configurar alertas (Slack/Email)

**Dependências:** TASK 2.2 (Silver Layer)  
**Impacto:** Qualidade garantida automaticamente

---

## 🟢 TIER 3: ANALYTICS LAYER (Semanas 5-8)

### TASK 3.1: Criar Gold Layer (Star Schema) 🟢
**Prioridade:** MÉDIA  
**Tempo:** 7-10 dias  
**Blocos:** TASK 3.2, 3.3

**Checklist:**
- [ ] Criar dimensões (dbt marts):
  - [ ] `dim_items.sql`
  - [ ] `dim_towers.sql`
  - [ ] `dim_time.sql`
- [ ] Criar fatos:
  - [ ] `fact_forecasts.sql`
  - [ ] `fact_inventory.sql`
- [ ] Configurar particionamento e clustering
- [ ] Materializar como Delta tables (Gold layer)
- [ ] Criar testes dbt

**Dependências:** TASK 2.2 (Silver Layer)  
**Impacto:** Dados prontos para analytics

---

### TASK 3.2: Setup Metabase 🟢
**Prioridade:** MÉDIA  
**Tempo:** 2-3 dias  
**Blocos:** Nenhuma

**Checklist:**
- [ ] Setup Metabase (Docker Compose)
- [ ] Conectar com Gold layer (Delta Lake via Spark)
- [ ] Criar dashboards básicos:
  - [ ] Forecast accuracy dashboard
  - [ ] Inventory levels dashboard
- [ ] Configurar usuários e permissões

**Dependências:** TASK 3.1 (Gold Layer)  
**Impacto:** Self-service BI para usuários

---

### TASK 3.3: Criar dbt Metrics 🟢
**Prioridade:** MÉDIA  
**Tempo:** 3-4 dias  
**Blocos:** Nenhuma

**Checklist:**
- [ ] Criar `metrics.yml` com métricas de negócio:
  - [ ] `forecast_accuracy` (MAPE)
  - [ ] `total_forecasted_demand`
  - [ ] `inventory_turnover`
- [ ] Testar métricas
- [ ] Expor via dbt Semantic Layer API

**Dependências:** TASK 3.1 (Gold Layer)  
**Impacto:** Métricas de negócio centralizadas

---

## 🟢 TIER 4: ML OPS (Semanas 9-12)

### TASK 4.1: Setup MLflow 🟢
**Prioridade:** MÉDIA  
**Tempo:** 4-6 dias  
**Blocos:** Nenhuma

**Checklist:**
- [ ] Setup MLflow (Docker ou managed service)
- [ ] Integrar MLflow tracking nos modelos:
  - [ ] Prophet model
  - [ ] ARIMA model
  - [ ] LSTM model
- [ ] Configurar experiment tracking
- [ ] Criar model registry
- [ ] Configurar model serving (REST API)

**Dependências:** Nenhuma (pode ser paralelo)  
**Impacto:** ML Ops profissional

---

### TASK 4.2: Feature Store (Opcional) 🟢
**Prioridade:** BAIXA  
**Tempo:** 7-10 dias  
**Blocos:** Nenhuma

**Checklist:**
- [ ] Avaliar Feast vs Tecton
- [ ] Setup feature store escolhido
- [ ] Migrar features existentes
- [ ] Criar feature views
- [ ] Integrar com ML training

**Dependências:** TASK 4.1 (MLflow)  
**Impacto:** Features reutilizáveis

---

## 📊 RESUMO DE PRIORIDADES

### Crítico (Fazer Agora)
1. **TASK 1.1:** Setup Cloud Storage (S3/MinIO)
2. **TASK 1.2:** Implementar Delta Lake
3. **TASK 1.3:** Setup dbt Project
4. **TASK 1.4:** Setup Airflow

### Alta (Fazer em Seguida)
5. **TASK 2.1:** Criar Bronze Layer
6. **TASK 2.2:** Criar Silver Layer (dbt Staging)
7. **TASK 2.3:** Setup Great Expectations

### Média (Fazer Depois)
8. **TASK 3.1:** Criar Gold Layer (Star Schema)
9. **TASK 3.2:** Setup Metabase
10. **TASK 3.3:** Criar dbt Metrics
11. **TASK 4.1:** Setup MLflow

---

## 🚨 CRITICAL PATH

**Caminho Crítico (Bloqueia Tudo):**
```
TASK 1.1 (S3) 
  → TASK 1.2 (Delta Lake)
    → TASK 1.3 (dbt) + TASK 1.4 (Airflow)
      → TASK 2.1 (Bronze)
        → TASK 2.2 (Silver)
          → TASK 2.3 (Great Expectations)
            → TASK 3.1 (Gold)
              → TASK 3.2 (Metabase) + TASK 3.3 (Metrics)
```

**Tempo Estimado Total:** 16-20 semanas (4-5 meses)

**Sem TASK 1.1-1.4, NADA MAIS FUNCIONA.**

---

## ✅ VALIDAÇÃO DE CONCLUSÃO

### Fase 0 (Foundation)
- [ ] S3 buckets criados e testados
- [ ] Delta Lake funcionando com ACID transactions
- [ ] dbt project criado e primeiro modelo rodando
- [ ] Airflow setup e primeiro DAG executando

### Fase 1 (Data Foundation)
- [ ] Bronze layer ingerindo dados diariamente
- [ ] Silver layer (dbt staging) materializado
- [ ] Great Expectations validando qualidade

### Fase 2 (Analytics Layer)
- [ ] Gold layer (star schema) criado
- [ ] Metabase conectado e dashboards criados
- [ ] dbt metrics funcionando

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Lista de Tarefas Críticas - Priorizada

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

