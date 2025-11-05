# 🔍 DIAGNÓSTICO PROFUNDO: DADOS & STORAGE - NOVA CORRENTE
## Status Atual vs. Arquitetura Alvo (Novembro 2025)

**Versão:** 2.0  
**Data:** Novembro 2025  
**Status:** 🔴 CRÍTICO - 85% de Gap Arquitetural  
**Referência:** [Roadmap de Engenharia de Dados](./DATA_ENGINEERING_ROADMAP_PT_BR.md)

---

## 📊 EXECUTIVE SUMMARY

### Situação Crítica
O sistema atual opera com **arquitetura de dados básica (CSV + SQLite)** inadequada para produção. Faltam **85% dos componentes** da arquitetura moderna de Data Lakehouse planejada no roadmap.

### Impacto no Negócio
- ❌ **Não escala:** CSV files limitados a ~27MB, não suportam TB de dados
- ❌ **Sem ACID:** Impossível garantir consistência transacional
- ❌ **Sem qualidade:** Validação manual, risco alto de dados incorretos
- ❌ **Sem governança:** Zero rastreabilidade, lineage ou catalog
- ❌ **Performance ruim:** Queries de 30s+ (meta: <3s)

### Gap Arquitetural
| Componente | Planejado | Atual | Gap |
|------------|-----------|-------|-----|
| **Storage Layer** | MinIO/S3 + Delta Lake | CSV files | 100% |
| **Data Quality** | Great Expectations | Scripts manuais | 85% |
| **Orchestration** | Apache Airflow | Python scheduler básico | 80% |
| **Transformation** | dbt | Scripts Python ad-hoc | 100% |
| **Governance** | DataHub + Lineage | Nenhum | 100% |

---

## 🗂️ INVENTÁRIO TÉCNICO ATUAL (REALIDADE)

### 1. Storage & Persistência

#### ✅ O Que EXISTE
```
data/
├── raw/ (37 items)                    # Dados brutos CSV
│   ├── anatel_5g/
│   ├── weather/
│   ├── economic/
│   └── ... (33+ subdiretorios)
├── processed/ (37 items)              # Dados processados CSV
│   ├── unified_dataset_with_factors.csv (27MB, 118K rows)
│   ├── feature_engineered_data.csv
│   └── ...
├── training/ (8 items)                # Datasets ML
│   ├── unknown_train.csv (93,881 rows)
│   └── unknown_test.csv (23,471 rows)
└── registry/ (2 items)                # Metadata básico
```

**Problemas Identificados:**
- ❌ **CSV como storage primário** - não escala, sem ACID
- ❌ **Sem particionamento** - queries sempre full scan
- ❌ **Sem compressão eficiente** - desperdiça storage
- ❌ **Sem versionamento** - impossível rollback
- ❌ **Sem schema enforcement** - dados inconsistentes

#### ❌ O Que FALTA (Arquitetura Alvo)
```
MinIO/S3 + Delta Lake:
├── bronze/                            # Raw data (Parquet + Delta)
│   ├── year=2025/month=11/day=05/
│   │   ├── anatel_5g.parquet
│   │   ├── weather.parquet
│   │   └── economic.parquet
├── silver/                            # Cleaned data (Delta Lake)
│   ├── stg_items/
│   ├── stg_towers/
│   └── stg_forecasts/
└── gold/                              # Analytics (Star Schema)
    ├── dim_items/
    ├── dim_towers/
    ├── dim_time/
    ├── fact_forecasts/
    └── fact_inventory/
```

**Status:** 🔴 **0% implementado**

---

### 2. Database & Schema

#### ✅ O Que EXISTE
```python
# backend/app/config.py
DATABASE_URL = "sqlite:///./data/nova_corrente.db"  # SQLite local

# backend/data/Nova_Corrente_ML_Ready_DB.sql (34.8KB)
# Schema inicial PostgreSQL (NÃO em uso)
CREATE TABLE Material (
    material_id INT PRIMARY KEY,
    descricao VARCHAR(255),
    familia VARCHAR(100),
    fornecedor_id INT
);
-- + outras 10+ tabelas
```

**Problemas:**
- ⚠️ **SQLite em produção** - sem suporte adequado a concorrência
- ❌ **Schema SQL não aplicado** - sem migrações (Alembic)
- ❌ **Sem ORM (SQLAlchemy)** - queries SQL manuais dispersas
- ❌ **Não é Star Schema** - schema transacional, não analítico
- ❌ **PostgreSQL config existe mas não está em uso**

#### ❌ O Que FALTA
- ❌ PostgreSQL/MySQL em produção com pooling
- ❌ SQLAlchemy ORM com models declarativos
- ❌ Alembic para migrações versionadas
- ❌ Star Schema (dim_items, dim_towers, fact_forecasts)
- ❌ Índices otimizados para queries analíticas

**Status:** 🔴 **40% implementado** (schema existe, não aplicado)

---

### 3. ETL Pipelines & Orchestration

#### ✅ O Que EXISTE
```python
# backend/pipelines/orchestrator_service.py (7.9KB)
class OrchestratorService:
    def start_scheduler(self, time_str="02:00"):
        schedule.every().day.at(time_str).do(
            self.run_complete_pipeline
        )
        # Threading básico Python

# Pipelines implementados:
backend/pipelines/
├── anatel_5g_etl.py          # ✅ 5G data extractor
├── climate_etl.py            # ✅ Weather API
├── economic_etl.py           # ✅ Economic API
├── brazilian_calendar_etl.py # ✅ Calendar
├── feature_calculation_etl.py # ✅ 73 features
└── data_processing/ (19 scripts)
```

**Pontos Positivos:**
- ✅ Extractors funcionais para fontes externas
- ✅ Feature engineering implementado (73 features)
- ✅ Scheduler básico funciona para MVP

**Problemas Críticos:**
- ❌ **Sem Apache Airflow** - orchestração sem UI, retry, monitoring
- ❌ **Sem DAGs visuais** - impossível debugar dependências
- ❌ **Sem retry automático** - falhas não tratadas
- ❌ **Sem alerting** - falhas silenciosas
- ❌ **Logging básico** - sem agregação/busca
- ❌ **Salvam em CSV** - não em Bronze/Silver layers

#### ❌ O Que FALTA (Airflow)
```python
# dags/extract_bronze_dag.py (NÃO EXISTE)
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('extract_bronze', schedule='@daily') as dag:
    extract_weather = PythonOperator(...)
    extract_economic = PythonOperator(...)
    extract_5g = PythonOperator(...)
    
    [extract_weather, extract_economic, extract_5g] >> validate_bronze
```

**Status:** 🟡 **20% implementado** (scheduler existe, Airflow não)

---

### 4. Data Transformation (dbt)

#### ❌ Status Atual: **0% implementado**

**Transformações Atuais (Python ad-hoc):**
```python
# backend/pipelines/data_processing/
├── data_aggregation.py
├── data_cleaning.py
├── feature_engineering.py
├── time_series_preparation.py
└── ... (15+ scripts duplicados)
```

**Problemas:**
- ❌ **Código duplicado** - mesmas transformações em múltiplos arquivos
- ❌ **Sem versionamento** - mudanças não rastreadas
- ❌ **Sem testes** - qualidade não validada
- ❌ **Sem documentação automática** - tribal knowledge
- ❌ **Difícil manutenção** - refatorar = quebrar tudo

#### ❌ O Que FALTA (dbt)
```yaml
# dbt_nova_corrente/models/staging/stg_items.sql (NÃO EXISTE)
SELECT
  item_id,
  TRIM(LOWER(item_name)) as item_name,
  CAST(price AS DECIMAL(10,2)) as price,
  -- Validações automáticas via dbt tests
FROM {{ source('bronze', 'raw_items') }}
WHERE item_id IS NOT NULL
```

**Benefícios Perdidos:**
- ❌ SQL versionado como código
- ❌ Testes automáticos (not_null, unique, relationships)
- ❌ Documentação HTML gerada automaticamente
- ❌ Lineage visual de transformações
- ❌ CI/CD integrado

---

### 5. Data Quality & Validation

#### ⚠️ O Que EXISTE (Básico)
```python
# backend/pipelines/monitoring/data_quality_report.py
# Scripts manuais de validação
def check_nulls(df):
    return df.isnull().sum()

def check_duplicates(df):
    return df.duplicated().sum()
```

**Problemas:**
- ⚠️ **Validação manual** - precisa executar script manualmente
- ❌ **Sem expectation suites** - regras não documentadas
- ❌ **Sem alertas automáticos** - falhas passam despercebidas
- ❌ **Sem histórico** - não rastreia degradação ao longo do tempo
- ❌ **Sem data docs** - qualidade não reportada

#### ❌ O Que FALTA (Great Expectations)
```python
# great_expectations/expectations/items_suite.json (NÃO EXISTE)
{
  "expectations": [
    {
      "expectation_type": "expect_column_values_to_not_be_null",
      "kwargs": {"column": "item_id"}
    },
    {
      "expectation_type": "expect_column_values_to_be_unique",
      "kwargs": {"column": "item_id"}
    },
    {
      "expectation_type": "expect_column_values_to_be_between",
      "kwargs": {"column": "price", "min_value": 0, "max_value": 1000000}
    }
  ]
}
```

**Status:** 🟡 **15% implementado** (validação básica existe)

---

### 6. ML Ops & Model Management

#### ⚠️ O Que EXISTE
```python
# backend/ml/models/ (implementado)
├── prophet/
├── arima/
└── lstm/

# backend/services/ml_models/model_registry.py (básico)
class ModelRegistry:
    def save_model(self, model, path):
        with open(path, 'wb') as f:
            pickle.dump(model, f)  # Pickle local
```

**Pontos Positivos:**
- ✅ Modelos ML implementados (Prophet, ARIMA, LSTM)
- ✅ Model registry básico funciona

**Problemas:**
- ❌ **Sem MLflow** - sem tracking de experimentos
- ❌ **Pickle files** - versionamento manual, sem metadata
- ❌ **Sem experiment tracking** - impossível comparar modelos
- ❌ **Sem model serving** - inferência não padronizada
- ❌ **Sem monitoring** - drift não detectado

#### ❌ O Que FALTA (MLflow)
```python
# NÃO EXISTE
import mlflow

with mlflow.start_run():
    mlflow.log_params({"horizon": 30, "seasonality": "weekly"})
    mlflow.log_metrics({"mape": 0.12, "rmse": 45.3})
    mlflow.sklearn.log_model(model, "prophet_model")
```

**Status:** 🟡 **10% implementado** (models existem, MLflow não)

---

### 7. Observability & Monitoring

#### ⚠️ O Que EXISTE
```python
# backend/config/logging_config.py
import logging
from logging.handlers import RotatingFileHandler

# Logging básico para arquivos
logger = logging.getLogger('nova_corrente')
handler = RotatingFileHandler('logs/app.log', maxBytes=10MB)
```

**Problemas:**
- ⚠️ **Logs em arquivos** - difícil agregar/buscar
- ❌ **Sem Prometheus/Grafana** - sem métricas de sistema
- ❌ **Sem alerting** - problemas não notificados
- ❌ **Sem tracing distribuído** - debugging difícil
- ❌ **Sem dashboards** - visibilidade zero

#### ❌ O Que FALTA
- ❌ Prometheus + Grafana para métricas
- ❌ ELK/Loki para logs agregados
- ❌ OpenTelemetry para tracing
- ❌ Alertmanager para notificações
- ❌ Dashboards de observabilidade

**Status:** 🟡 **20% implementado** (logging básico)

---

### 8. Data Governance & Catalog

#### ❌ Status Atual: **0% implementado**

**O Que NÃO EXISTE:**
- ❌ Data Catalog (DataHub) - datasets não descobríveis
- ❌ Lineage tracking - origem dos dados desconhecida
- ❌ Metadata management - sem documentação centralizada
- ❌ Data ownership - responsáveis não definidos
- ❌ Access policies - sem RBAC para dados
- ❌ Data versioning - mudanças não rastreadas

**Impacto:**
- 🔴 **Descoberta impossível** - usuários não encontram dados
- 🔴 **Conformidade em risco** - não atende LGPD/GDPR
- 🔴 **Debugging difícil** - não sabe de onde vem o dado
- 🔴 **Colaboração prejudicada** - conhecimento tribal

---

## 🔴 GAPS CRÍTICOS IDENTIFICADOS

### GAP #1: Storage Layer (100% faltando)
**Atual:** CSV files (27MB, não escalável)  
**Alvo:** MinIO/S3 + Delta Lake (TB-scale, ACID)  
**Impacto:** 🔴 BLOQUEADOR - nada escala sem isso

### GAP #2: Data Quality (85% faltando)
**Atual:** Scripts manuais de validação  
**Alvo:** Great Expectations automático  
**Impacto:** 🔴 ALTO - dados ruins em produção

### GAP #3: Orchestration (80% faltando)
**Atual:** Python scheduler básico  
**Alvo:** Apache Airflow com DAGs  
**Impacto:** 🔴 ALTO - operações não confiáveis

### GAP #4: Transformation (100% faltando)
**Atual:** Scripts Python ad-hoc  
**Alvo:** dbt com testes e docs  
**Impacto:** 🟡 MÉDIO - manutenção difícil

### GAP #5: ML Ops (90% faltando)
**Atual:** Pickle files manuais  
**Alvo:** MLflow tracking + registry  
**Impacto:** 🟡 MÉDIO - reprodutibilidade baixa

### GAP #6: Governance (100% faltando)
**Atual:** Nenhum catalog ou lineage  
**Alvo:** DataHub + metadata management  
**Impacto:** 🟢 BAIXO - nice to have

---

## 🚨 RISCOS CRÍTICOS

### Risco #1: Perda de Dados (ALTO)
**Causa:** CSV sem backup, versionamento ou ACID  
**Probabilidade:** Alta (80%)  
**Impacto:** Crítico - perda de dados históricos  
**Mitigação:** TASK 1.1 (MinIO) + TASK 1.2 (Delta Lake) URGENTE

### Risco #2: Dados Incorretos em Produção (ALTO)
**Causa:** Sem validação automática (Great Expectations)  
**Probabilidade:** Alta (70%)  
**Impacto:** Alto - decisões de negócio erradas  
**Mitigação:** TASK 2.3 (Great Expectations) necessário

### Risco #3: Falhas Silenciosas de Pipeline (MÉDIO)
**Causa:** Orchestrator sem retry, monitoring, alerting  
**Probabilidade:** Média (50%)  
**Impacto:** Médio - dados desatualizados  
**Mitigação:** TASK 1.4 (Airflow) resolve

### Risco #4: Impossibilidade de Escalar (ALTO)
**Causa:** SQLite + CSV não suportam concorrência/volume  
**Probabilidade:** Certa (100%) quando crescer  
**Impacto:** Crítico - sistema para  
**Mitigação:** Migração para PostgreSQL + Delta Lake

### Risco #5: Reprodutibilidade de ML Baixa (MÉDIO)
**Causa:** Modelos em Pickle sem tracking (MLflow)  
**Probabilidade:** Média (60%)  
**Impacto:** Médio - não consegue replicar resultados  
**Mitigação:** TASK 4.1 (MLflow) recomendado

---

## 🎯 PLANO DE AÇÃO PRIORITÁRIO

### 🔥 SPRINT 1: FUNDAÇÃO CRÍTICA (Semana 1-2)
**Objetivo:** Resolver bloqueadores críticos de storage e orchestração

#### TASK 1.1: Setup MinIO (Dia 1-2) 🔴 URGENTE
**Status Atual:** ❌ 0%  
**Bloqueador:** CSV files (~27MB) não escalam

**Ações:**
1. Provisionar MinIO via Docker Compose
   ```yaml
   # docker-compose.yml (ADICIONAR)
   minio:
     image: minio/minio:latest
     ports:
       - "9000:9000"
       - "9001:9001"
     volumes:
       - ./data/minio:/data
     environment:
       MINIO_ROOT_USER: admin
       MINIO_ROOT_PASSWORD: minio123
     command: server /data --console-address ":9001"
   ```

2. Criar buckets Bronze/Silver/Gold
   ```python
   # scripts/setup_minio.py (CRIAR)
   from minio import Minio
   
   client = Minio("localhost:9000", 
                  access_key="admin",
                  secret_key="minio123",
                  secure=False)
   
   for bucket in ["bronze", "silver", "gold"]:
       if not client.bucket_exists(bucket):
           client.make_bucket(bucket)
   ```

3. Migrar dados CSV existentes → MinIO
   ```python
   # scripts/migrate_csv_to_minio.py (CRIAR)
   import pandas as pd
   from minio import Minio
   
   # Migrar data/processed/*.csv → bronze/
   for csv_file in Path("data/processed").glob("*.csv"):
       df = pd.read_csv(csv_file)
       parquet_buffer = df.to_parquet()
       client.put_object(
           "bronze",
           f"raw/{csv_file.stem}.parquet",
           parquet_buffer
       )
   ```

**Critérios de Aceite:**
- ✅ MinIO rodando em localhost:9000
- ✅ Buckets bronze/silver/gold criados
- ✅ Dados CSV migrados para Parquet em MinIO/bronze
- ✅ Script de teste upload/download funcionando

---

#### TASK 1.2: Implementar Delta Lake (Dia 3-7) 🔴 URGENTE
**Status Atual:** ❌ 0%  
**Bloqueador:** Sem ACID, sem time travel, sem schema evolution

**Ações:**
1. Instalar Delta Lake
   ```bash
   # requirements_delta.txt (CRIAR)
   delta-spark==2.4.0
   pyspark==3.4.1
   ```

2. Configurar Spark + Delta
   ```python
   # backend/config/delta_config.py (CRIAR)
   from pyspark.sql import SparkSession
   from delta import configure_spark_with_delta_pip
   
   def get_spark_session():
       builder = SparkSession.builder \
           .appName("nova_corrente") \
           .config("spark.sql.extensions", 
                   "io.delta.sql.DeltaSparkSessionExtension") \
           .config("spark.sql.catalog.spark_catalog", 
                   "org.apache.spark.sql.delta.catalog.DeltaCatalog")
       
       return configure_spark_with_delta_pip(builder).getOrCreate()
   ```

3. Migrar Parquet → Delta Lake
   ```python
   # scripts/migrate_parquet_to_delta.py (CRIAR)
   from delta.tables import DeltaTable
   
   spark = get_spark_session()
   
   # Ler Parquet do Bronze
   df = spark.read.parquet("s3a://bronze/raw/unified_dataset.parquet")
   
   # Escrever como Delta com particionamento
   df.write \
       .format("delta") \
       .mode("overwrite") \
       .partitionBy("year", "month", "day") \
       .save("s3a://bronze/delta/unified_dataset")
   ```

4. Testar ACID transactions
   ```python
   # tests/test_delta_acid.py (CRIAR)
   def test_delta_time_travel():
       df_v0 = spark.read.format("delta").load("s3a://bronze/delta/...")
       df_v0.write.format("delta").mode("append").save(...)
       
       # Rollback para versão anterior
       df_v1 = spark.read.format("delta") \
           .option("versionAsOf", 0) \
           .load("s3a://bronze/delta/...")
       
       assert df_v0.count() != df_v1.count()
   ```

**Critérios de Aceite:**
- ✅ PySpark + Delta Lake instalados
- ✅ Bronze layer em Delta format
- ✅ Particionamento year/month/day funcionando
- ✅ ACID transactions testadas
- ✅ Time travel (versioning) testado

---

#### TASK 1.3: Setup dbt (Dia 8-12) 🔴 CRÍTICO
**Status Atual:** ❌ 0%  
**Bloqueador:** Transformações não versionadas, sem testes

**Ações:**
1. Criar projeto dbt
   ```bash
   cd backend/
   pip install dbt-spark
   dbt init dbt_nova_corrente
   ```

2. Configurar conexão Delta Lake
   ```yaml
   # dbt_nova_corrente/profiles.yml (CRIAR)
   nova_corrente:
     target: dev
     outputs:
       dev:
         type: spark
         method: thrift
         host: localhost
         port: 10000
         schema: silver
   ```

3. Migrar transformações Python → SQL
   ```sql
   -- dbt_nova_corrente/models/staging/stg_items.sql (CRIAR)
   WITH source AS (
     SELECT * FROM {{ source('bronze', 'raw_items') }}
   )
   
   SELECT
     item_id,
     TRIM(LOWER(item_name)) as item_name,
     TRIM(category) as category,
     CAST(price AS DECIMAL(10,2)) as price,
     CURRENT_TIMESTAMP() as _dbt_loaded_at
   FROM source
   WHERE item_id IS NOT NULL
   ```

4. Adicionar testes dbt
   ```yaml
   # dbt_nova_corrente/models/staging/schema.yml (CRIAR)
   version: 2
   
   models:
     - name: stg_items
       description: "Staging layer for items"
       columns:
         - name: item_id
           tests:
             - not_null
             - unique
         - name: price
           tests:
             - dbt_utils.accepted_range:
                 min_value: 0
                 max_value: 1000000
   ```

**Critérios de Aceite:**
- ✅ dbt project inicializado
- ✅ 5 staging models criados (stg_items, stg_towers, stg_weather, stg_economic, stg_5g)
- ✅ Testes dbt passando (not_null, unique, relationships)
- ✅ Documentação gerada (dbt docs generate)

---

#### TASK 1.4: Setup Airflow (Dia 8-12) 🔴 CRÍTICO
**Status Atual:** ⚠️ 20% (apenas Python scheduler)  
**Bloqueador:** Sem UI, retry, monitoring, alerting

**Ações:**
1. Adicionar Airflow ao Docker Compose
   ```yaml
   # docker-compose.yml (ADICIONAR)
   airflow-webserver:
     image: apache/airflow:2.8.0
     ports:
       - "8080:8080"
     environment:
       AIRFLOW__CORE__EXECUTOR: CeleryExecutor
       AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
     volumes:
       - ./dags:/opt/airflow/dags
       - ./logs:/opt/airflow/logs
     command: webserver
   
   airflow-scheduler:
     image: apache/airflow:2.8.0
     environment:
       AIRFLOW__CORE__EXECUTOR: CeleryExecutor
     volumes:
       - ./dags:/opt/airflow/dags
     command: scheduler
   ```

2. Migrar orchestrator_service.py → Airflow DAG
   ```python
   # dags/extract_bronze_dag.py (CRIAR)
   from airflow import DAG
   from airflow.operators.python import PythonOperator
   from datetime import datetime, timedelta
   
   default_args = {
       'owner': 'data-engineering',
       'depends_on_past': False,
       'start_date': datetime(2025, 11, 1),
       'email_on_failure': True,
       'email': ['alerts@novacorrente.com'],
       'retries': 3,
       'retry_delay': timedelta(minutes=5),
   }
   
   with DAG(
       'extract_bronze',
       default_args=default_args,
       schedule_interval='@daily',
       catchup=False
   ) as dag:
       
       extract_weather = PythonOperator(
           task_id='extract_weather',
           python_callable=climate_etl.extract
       )
       
       extract_economic = PythonOperator(
           task_id='extract_economic',
           python_callable=economic_etl.extract
       )
       
       extract_5g = PythonOperator(
           task_id='extract_5g',
           python_callable=anatel_5g_etl.extract
       )
       
       validate_bronze = PythonOperator(
           task_id='validate_bronze',
           python_callable=validate_bronze_data
       )
       
       # Dependencies
       [extract_weather, extract_economic, extract_5g] >> validate_bronze
   ```

3. Configurar alerting (Slack)
   ```python
   # dags/config/airflow_config.py (CRIAR)
   from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
   
   def send_slack_alert(context):
       alert = SlackWebhookOperator(
           task_id='slack_alert',
           http_conn_id='slack_webhook',
           message=f"❌ DAG {context['dag'].dag_id} failed!",
           channel='#data-alerts'
       )
       return alert.execute(context=context)
   ```

**Critérios de Aceite:**
- ✅ Airflow UI acessível em localhost:8080
- ✅ 3 DAGs criados (extract_bronze, bronze_to_silver, silver_to_gold)
- ✅ Retry automático funcionando (testar com falha proposital)
- ✅ Alertas Slack configurados
- ✅ orchestrator_service.py depreciado

---

### 🟡 SPRINT 2: QUALIDADE & TRANSFORMAÇÃO (Semana 3-4)

#### TASK 2.1: Bronze Layer Refactoring (Dia 13-16)
**Refatorar extractors** para salvar em MinIO/Bronze (Parquet + Delta)

#### TASK 2.2: Silver Layer (Dia 17-21)
**Criar dbt staging models** com limpeza e validação

#### TASK 2.3: Great Expectations (Dia 22-26)
**Implementar expectation suites** para validação automática

---

## ✅ CRITÉRIOS DE ACEITE FINAIS

### Fase 0: Fundação (Semana 1-2)
- [ ] MinIO rodando com buckets Bronze/Silver/Gold
- [ ] Delta Lake implementado com ACID transactions
- [ ] dbt project com 5 staging models rodando
- [ ] Airflow com 3 DAGs executando daily
- [ ] Dados CSV migrados para Delta Lake
- [ ] orchestrator_service.py depreciado

### Fase 1: Qualidade (Semana 3-4)
- [ ] Bronze layer ingerindo dados com particionamento
- [ ] Silver layer com dbt staging models materializados
- [ ] Great Expectations validando >95% qualidade
- [ ] Testes dbt passando (100% coverage)
- [ ] Data quality reports automáticos

### Fase 2: Analytics (Semana 5-8)
- [ ] Gold layer com star schema (dim_items, dim_towers, fact_forecasts)
- [ ] Metabase conectado e dashboards criados
- [ ] dbt metrics funcionando
- [ ] Query performance <3s (P95)

---

**Documento atualizado:** Novembro 2025  
**Versão:** 2.0  
**Status:** 🔴 CRÍTICO - 85% Gap Arquitetural  
**Próxima Ação:** 🔥 TASK 1.1 (Setup MinIO) - COMEÇAR HOJE!

**Referências:**
- [Roadmap de Engenharia de Dados](./DATA_ENGINEERING_ROADMAP_PT_BR.md)
- [Diagnóstico Completo](./COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md)
- [Constraints Globais](./clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)
