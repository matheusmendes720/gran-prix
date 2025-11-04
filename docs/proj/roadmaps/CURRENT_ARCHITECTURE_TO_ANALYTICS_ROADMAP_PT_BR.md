# 🔄 MIGRAÇÃO: ARQUITETURA ATUAL → ANALYTICS ENGINEERING
## Nova Corrente - Evolução da Arquitetura

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Plano de Migração Completo

---

## 📋 ÍNDICE

1. [Arquitetura Atual vs Target](#comparacao)
2. [Gap Analysis](#gap-analysis)
3. [Plano de Migração](#migracao)
4. [Integração de Componentes](#integracao)
5. [Timeline de Evolução](#timeline)

---

<a name="comparacao"></a>

## 1. 📊 ARQUITETURA ATUAL VS TARGET

### 1.1 Arquitetura Atual (Sistema Legacy)

```
┌─────────────────────────────────────────────┐
│         DATA SOURCES LAYER                  │
│  INMET | BACEN | ANATEL | ERP | Kaggle     │
└─────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│         INGESTION LAYER                       │
│  Data Collector | Schema Validator           │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│         PROCESSING LAYER                       │
│  Preprocessor | Feature Engineer (1000+)      │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│         ML/DL LAYER                           │
│  ARIMA | Prophet | LSTM | XGBoost | Ensemble │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│         BUSINESS LOGIC LAYER                  │
│  Reorder Point | Alert System | Reports       │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│         OUTPUT LAYER                          │
│  Dashboard | API | Email | PDF | SLA Monitor  │
└───────────────────────────────────────────────┘
```

**Características:**
- Pipeline monolítico Python
- Storage: CSV/PostgreSQL
- Sem camadas de dados (Bronze/Silver/Gold)
- Sem orquestração profissional (Airflow)
- Sem transformações SQL (dbt)
- Sem data lakehouse

---

### 1.2 Arquitetura Target (Analytics Engineering)

```
┌─────────────────────────────────────────────┐
│         DATA SOURCES                         │
│  ERP | Weather | Anatel | Supplier APIs     │
└─────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│      INGESTION (Airbyte/Fivetran)            │
│      Extract & Load → Bronze (S3 Delta)     │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│      BRONZE LAYER (Raw Data)                  │
│      S3 Delta Lake | Partitioned by date     │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│      SILVER LAYER (Cleaned)                   │
│      dbt Staging Models | Great Expectations │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│      GOLD LAYER (Star Schema)                 │
│      dbt Marts | Dimensions & Facts           │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│      SERVING LAYER                             │
│      FastAPI | Redis Cache | Message Queue    │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│      APPLICATION LAYER                        │
│      Next.js Frontend | FastAPI Backend       │
└───────────────────────────────────────────────┘
```

**Características:**
- Arquitetura Medallion (Bronze/Silver/Gold)
- Data Lakehouse (Delta Lake)
- Orquestração (Airflow)
- Transformações SQL (dbt)
- Self-service BI (Metabase/Superset)
- Governança completa (DataHub)

---

<a name="gap-analysis"></a>

## 2. 🔍 GAP ANALYSIS

### 2.1 Componentes Existentes (Manter)

**✅ Para Manter:**
- Feature engineering (73 features)
- ML models (ARIMA, Prophet, LSTM, Ensemble)
- Business logic (Reorder Point Calculator)
- Alert system
- Output channels (Dashboard, API, Email)

**Status:** ✅ Funcionando, integrar ao novo sistema

---

### 2.2 Componentes a Adicionar

**⏳ Para Adicionar:**

**Infraestrutura:**
- [ ] Terraform para IaC
- [ ] S3 buckets (Bronze/Silver/Gold)
- [ ] Databricks workspace
- [ ] Delta Lake format

**Orquestração:**
- [ ] Airflow instalado
- [ ] DAGs criados
- [ ] Scheduling configurado

**Transformações:**
- [ ] dbt project
- [ ] Staging models
- [ ] Mart models (star schema)
- [ ] dbt metrics

**Data Quality:**
- [ ] Great Expectations suite
- [ ] Data profiling automatizado
- [ ] Quality gates

**Serving:**
- [ ] Redis cache layer
- [ ] Message queue (Kafka)
- [ ] API optimization

**BI & Analytics:**
- [ ] Metabase/Superset
- [ ] Dashboards
- [ ] Self-service analytics

**Governança:**
- [ ] DataHub catalog
- [ ] Data lineage
- [ ] Access control

---

### 2.3 Componentes a Evoluir

**🔄 Para Evoluir:**

**Pipeline:**
- **Atual:** Python monolítico
- **Target:** ELT (Airbyte → dbt → Gold)
- **Evolução:** Manter Python para ML, usar dbt para transformações

**Storage:**
- **Atual:** CSV/PostgreSQL
- **Target:** Delta Lake (S3)
- **Evolução:** Migrar dados para Delta Lake

**Orquestração:**
- **Atual:** Cron jobs/Python scripts
- **Target:** Airflow DAGs
- **Evolução:** Transformar scripts em DAGs

**ML Serving:**
- **Atual:** Modelos carregados em memória
- **Target:** MLflow serving
- **Evolução:** Registrar modelos no MLflow

---

<a name="migracao"></a>

## 3. 🔄 PLANO DE MIGRAÇÃO

### 3.1 Fase de Migração (Semana 1-2)

**Objetivo:** Estabelecer nova infraestrutura sem quebrar sistema atual

**Ações:**
1. **Setup infraestrutura paralela**
   - Terraform (dev/staging/prod)
   - S3 buckets (Bronze/Silver/Gold)
   - Databricks workspace
   - Airflow instalado

2. **Migrar dados históricos**
   - Exportar PostgreSQL → CSV
   - Load CSV → Bronze (S3 Delta)
   - Validar dados migrados

3. **Criar pipelines paralelos**
   - Pipeline atual continua rodando
   - Pipeline novo roda em paralelo
   - Comparar resultados

**Checkpoint:**
- ✅ Sistema novo rodando em paralelo
- ✅ Dados históricos migrados
- ✅ Validação cruzada funcionando

---

### 3.2 Fase de Transição (Semana 3-4)

**Objetivo:** Migrar transformações para dbt

**Ações:**
1. **Migrar feature engineering para dbt**
   - Criar staging models
   - Migrar lógica Python → SQL
   - Validar resultados

2. **Migrar transformações para dbt**
   - Criar marts models
   - Migrar agregações
   - Criar star schema

3. **Migrar orquestração para Airflow**
   - Converter scripts Python → DAGs
   - Configurar scheduling
   - Testar execução

**Checkpoint:**
- ✅ dbt models funcionando
- ✅ Airflow DAGs executando
- ✅ Resultados validados

---

### 3.3 Fase de Integração (Semana 5-6)

**Objetivo:** Integrar novo sistema com aplicação fullstack

**Ações:**
1. **API layer**
   - Migrar endpoints para usar Gold layer
   - Implementar Redis cache
   - Configurar message queue

2. **Frontend integration**
   - Conectar ao novo backend
   - Testar endpoints
   - Validar performance

3. **ML serving**
   - Registrar modelos no MLflow
   - Setup model serving
   - Migrar inferência para MLflow

**Checklist:**
- ✅ API usando Gold layer
- ✅ Frontend conectado
- ✅ ML models servidos via MLflow

---

### 3.4 Fase de Desligamento (Semana 7-8)

**Objetivo:** Desligar sistema legado

**Ações:**
1. **Validação final**
   - Comparar resultados finais
   - Validar métricas
   - Testes de regressão

2. **Migrar usuários**
   - Notificar mudanças
   - Treinar usuários
   - Documentação atualizada

3. **Desligar sistema legado**
   - Parar pipelines antigos
   - Descomissionar servidores
   - Arquivar código legado

**Checklist:**
- ✅ Sistema novo 100% funcional
- ✅ Usuários migrados
- ✅ Sistema legado desligado

---

<a name="integracao"></a>

## 4. 🔗 INTEGRAÇÃO DE COMPONENTES

### 4.1 Mantendo Componentes Existentes

**Feature Engineering (73 features):**

**Estratégia:** Migrar para dbt + manter Python para features complexas

```sql
-- dbt: Features temporais básicas
-- models/intermediate/int_temporal_features.sql
{{ config(materialized='view') }}

WITH base AS (
    SELECT * FROM {{ ref('stg_demand') }}
)

SELECT
    *,
    -- Temporal features (SQL)
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    SIN(2 * PI() * EXTRACT(MONTH FROM date) / 12) AS month_sin,
    COS(2 * PI() * EXTRACT(MONTH FROM date) / 12) AS month_cos,
    -- Lag features
    LAG(demand, 1) OVER (PARTITION BY item_id ORDER BY date) AS lag_1,
    LAG(demand, 7) OVER (PARTITION BY item_id ORDER BY date) AS lag_7
FROM base
```

```python
# Python: Features complexas (ML-specific)
# backend/pipelines/feature_engineering/complex_features.py
def create_complex_features(df):
    """Create complex features that require Python"""
    # Rolling statistics
    df['ma_7'] = df.groupby('item_id')['demand'].rolling(7).mean()
    df['std_7'] = df.groupby('item_id')['demand'].rolling(7).std()
    
    # Advanced aggregations
    # ... complex logic ...
    
    return df
```

---

**ML Models (ARIMA, Prophet, LSTM, Ensemble):**

**Estratégia:** Registrar no MLflow, manter inferência via Python

```python
# backend/ml/inference/ensemble_inference.py
import mlflow
import mlflow.prophet
from mlflow.tracking import MlflowClient

class EnsembleInference:
    """Inference using MLflow registered models"""
    
    def __init__(self):
        self.client = MlflowClient()
        self.model_registry = "NovaCorrenteForecast"
    
    def load_models(self):
        """Load models from MLflow registry"""
        # Get production model version
        prod_version = self.client.get_latest_versions(
            self.model_registry,
            stages=["Production"]
        )[0]
        
        # Load models
        self.prophet = mlflow.prophet.load_model(
            f"models:/{self.model_registry}/{prod_version.version}"
        )
        # ... load other models
    
    def predict(self, features):
        """Generate ensemble prediction"""
        # Predict with each model
        pred_prophet = self.prophet.predict(features)
        pred_arima = self.arima.predict(features)
        pred_lstm = self.lstm.predict(features)
        
        # Ensemble (weighted average)
        ensemble = (
            0.35 * pred_prophet +
            0.20 * pred_arima +
            0.25 * pred_lstm +
            0.20 * pred_xgboost
        )
        
        return ensemble
```

---

**Reorder Point Calculator:**

**Estratégia:** Migrar para dbt macro + manter lógica complexa em Python

```sql
-- dbt: Macro para reorder point
-- macros/reorder_point.sql
{% macro calculate_reorder_point(
    avg_demand,
    lead_time,
    std_demand,
    service_level=0.95
) %}
    {%- set z_score = 1.96 -%}  {# 95% service level #}
    {%- set safety_stock = z_score * std_demand * sqrt(lead_time) -%}
    {{ avg_demand * lead_time + safety_stock }}
{% endmacro %}

-- Usage in dbt model
SELECT
    item_id,
    {{ calculate_reorder_point(
        avg_daily_demand,
        lead_time_days,
        std_daily_demand,
        0.95
    ) }} AS reorder_point
FROM {{ ref('int_item_metrics') }}
```

```python
# Python: Reorder point com fatores externos (mantido)
# backend/app/core/reorder_point.py
def calculate_dynamic_pp(
    forecast,
    lead_time,
    weather_factor,
    holiday_factor,
    expansion_factor
):
    """Calculate PP with external factors (complex logic)"""
    base_pp = calculate_base_pp(forecast, lead_time)
    
    # Apply factors
    adjusted_pp = base_pp * weather_factor * holiday_factor * expansion_factor
    
    return adjusted_pp
```

---

**Alert System:**

**Estratégia:** Integrar com Airflow + manter lógica de negócio

```python
# backend/app/core/alerts.py
"""
Alert system integrado com Airflow e message queue
"""
from app.core.message_queue import MessageQueue

class AlertSystem:
    """Alert system for inventory management"""
    
    def __init__(self):
        self.mq = MessageQueue()
        self.email_service = EmailService()
        self.sms_service = SMSService()
    
    def generate_alert(self, item_id, current_stock, reorder_point):
        """Generate alert if stock <= reorder point"""
        days_until_stockout = (current_stock - reorder_point) / avg_demand
        
        if current_stock <= reorder_point:
            alert = {
                'item_id': item_id,
                'severity': 'CRITICAL' if days_until_stockout <= 7 else 'WARNING',
                'current_stock': current_stock,
                'reorder_point': reorder_point,
                'days_until_stockout': days_until_stockout,
                'recommendation': f"Purchase {reorder_point * 2} units"
            }
            
            # Send via message queue
            self.mq.publish_stock_alert(item_id, alert)
            
            # Send immediate notification
            if alert['severity'] == 'CRITICAL':
                self.email_service.send_urgent(alert)
                self.sms_service.send(alert)
            
            return alert
        
        return None
```

---

### 4.2 Novo Pipeline Integrado

**Pipeline Híbrido (Python + dbt):**

```python
# backend/pipelines/daily_pipeline_hybrid.py
"""
Pipeline híbrido: dbt para transformações, Python para ML
"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def daily_pipeline():
    """
    Pipeline diário integrado:
    1. Extract (Airbyte) → Bronze
    2. Transform (dbt) → Silver → Gold
    3. ML Inference (Python/MLflow)
    4. Business Logic (Python)
    5. Alerts (Python + Message Queue)
    6. Serve (FastAPI)
    """
    pass

dag = DAG(
    'nova_corrente_daily_hybrid',
    schedule_interval='@daily',
    start_date=datetime(2025, 11, 1),
    catchup=False,
)

# Step 1: Extract → Bronze (Airbyte)
extract_task = BashOperator(
    task_id='extract_to_bronze',
    bash_command='airbyte extract --source erp',
    dag=dag
)

# Step 2: Transform → Silver (dbt)
transform_silver = BashOperator(
    task_id='transform_silver',
    bash_command='cd dbt && dbt run --models staging.*',
    dag=dag
)

# Step 3: Transform → Gold (dbt)
transform_gold = BashOperator(
    task_id='transform_gold',
    bash_command='cd dbt && dbt run --models marts.*',
    dag=dag
)

# Step 4: ML Inference (Python)
ml_inference = PythonOperator(
    task_id='ml_inference',
    python_callable=run_ml_inference,
    dag=dag
)

# Step 5: Business Logic (Python)
business_logic = PythonOperator(
    task_id='business_logic',
    python_callable=calculate_reorder_points,
    dag=dag
)

# Step 6: Alerts (Python)
alerts = PythonOperator(
    task_id='generate_alerts',
    python_callable=generate_alerts,
    dag=dag
)

# Dependencies
extract_task >> transform_silver >> transform_gold
transform_gold >> ml_inference >> business_logic >> alerts
```

---

<a name="timeline"></a>

## 5. 📅 TIMELINE DE EVOLUÇÃO

### Semana 1-2: Setup Paralelo

**Ações:**
- [ ] Terraform aplicado (dev/staging)
- [ ] S3 buckets criados
- [ ] Databricks configurado
- [ ] Airflow instalado
- [ ] Dados históricos migrados

**Resultado:** Sistema novo rodando em paralelo

---

### Semana 3-4: Migração de Transformações

**Ações:**
- [ ] dbt project criado
- [ ] Staging models criados (migração de features)
- [ ] Mart models criados
- [ ] Airflow DAGs criados
- [ ] Validação cruzada

**Resultado:** Transformações migradas para dbt

---

### Semana 5-6: Integração Fullstack

**Ações:**
- [ ] API migrada para usar Gold layer
- [ ] Redis cache configurado
- [ ] Message queue configurado
- [ ] Frontend integrado
- [ ] ML models registrados no MLflow

**Resultado:** Sistema integrado funcionando

---

### Semana 7-8: Desligamento Legado

**Ações:**
- [ ] Validação final
- [ ] Migração de usuários
- [ ] Desligar sistema legado
- [ ] Documentação finalizada

**Resultado:** Sistema 100% migrado

---

## 📊 COMPARAÇÃO FINAL

### Antes (Sistema Legado)

**Características:**
- Pipeline monolítico Python
- Storage: CSV/PostgreSQL
- Sem camadas de dados
- Sem orquestração profissional
- Sem self-service BI
- Sem governança de dados

**Desafios:**
- Difícil escalar
- Manutenção complexa
- Sem versionamento de transformações
- Sem observabilidade completa

---

### Depois (Analytics Engineering)

**Características:**
- Arquitetura Medallion (Bronze/Silver/Gold)
- Data Lakehouse (Delta Lake)
- Orquestração (Airflow)
- Transformações SQL (dbt)
- Self-service BI (Metabase/Superset)
- Governança completa (DataHub)

**Benefícios:**
- Escalável horizontalmente
- Manutenção simplificada
- Versionamento Git de tudo
- Observabilidade completa
- Self-service para usuários
- Governança e compliance

---

## ✅ CHECKLIST DE MIGRAÇÃO

### Fase 1: Setup Paralelo
- [ ] Terraform aplicado
- [ ] S3 buckets criados
- [ ] Databricks configurado
- [ ] Airflow instalado
- [ ] Dados migrados
- [ ] Pipeline paralelo rodando

### Fase 2: Migração Transformações
- [ ] dbt project criado
- [ ] Staging models criados
- [ ] Mart models criados
- [ ] Airflow DAGs criados
- [ ] Validação cruzada OK

### Fase 3: Integração
- [ ] API usando Gold layer
- [ ] Frontend integrado
- [ ] ML models no MLflow
- [ ] Cache configurado
- [ ] Message queue funcionando

### Fase 4: Desligamento
- [ ] Validação final OK
- [ ] Usuários migrados
- [ ] Sistema legado desligado
- [ ] Documentação atualizada

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Plano de Migração Completo

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**






