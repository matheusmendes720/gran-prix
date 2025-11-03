# 🔧 GUIA DE TROUBLESHOOTING
## Nova Corrente - Analytics Engineering

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Guia Completo

---

## 📋 ÍNDICE DE PROBLEMAS COMUNS

1. [Problemas de Infraestrutura](#infraestrutura)
2. [Problemas de Dados](#dados)
3. [Problemas de dbt](#dbt)
4. [Problemas de Airflow](#airflow)
5. [Problemas de ML](#ml)
6. [Problemas de BI Tools](#bi)

---

<a name="infraestrutura"></a>

## 1. 🏗️ PROBLEMAS DE INFRAESTRUTURA

### Problema: Terraform apply falha

**Sintomas:**
```
Error: Error creating S3 bucket: BucketAlreadyExists
```

**Solução:**
```bash
# Verificar buckets existentes
aws s3 ls | grep nova-corrente

# Se bucket existe, usar data source ou importar
terraform import aws_s3_bucket.this nova-corrente-data-lake-bronze-dev

# Ou mudar nome do bucket
terraform apply -var="bucket_name=nova-corrente-data-lake-bronze-dev-v2"
```

---

### Problema: Databricks workspace não acessível

**Sintomas:**
```
Error: Cannot connect to Databricks workspace
```

**Solução:**
1. Verificar token:
```bash
echo $DATABRICKS_TOKEN
```

2. Verificar host:
```bash
echo $DATABRICKS_HOST
# Deve ser: https://<workspace>.cloud.databricks.com
```

3. Testar conexão:
```python
from databricks import sql
connection = sql.connect(
    server_hostname="<workspace>.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/<warehouse-id>",
    access_token="<token>"
)
```

---

<a name="dados"></a>

## 2. 📊 PROBLEMAS DE DADOS

### Problema: Missing values em features externas

**Sintomas:**
```
Quality score: 70% (esperado: 90%+)
Missing values: 30% em clima/economia
```

**Solução:**
```python
# scripts/impute_missing.py
import pandas as pd

def impute_climate_features(df):
    """Forward fill from previous year same date"""
    df = df.sort_values('date')
    
    # Forward fill within same year
    df['temperature'] = df.groupby(df['date'].dt.dayofyear)['temperature'].fillna(method='ffill')
    
    # If still missing, use previous year same date
    df['temperature'] = df['temperature'].fillna(
        df.groupby(df['date'].dt.dayofyear)['temperature'].transform('median')
    )
    
    return df
```

---

### Problema: Schema evolution quebrando pipelines

**Sintomas:**
```
Error: Column 'new_column' not found in source
```

**Solução:**
```sql
-- dbt: Use dbt_utils.star() para handle schema changes
SELECT 
    {{ dbt_utils.star(from=ref('stg_items'), except=['deprecated_column']) }}
FROM {{ ref('stg_items') }}
```

**Ou Delta Lake schema evolution:**
```python
# Automático no Delta Lake
df.write.format("delta").mode("overwrite").option("mergeSchema", "true").save(path)
```

---

<a name="dbt"></a>

## 3. 📐 PROBLEMAS DE DBT

### Problema: dbt test falha

**Sintomas:**
```
Fail: 5 tests failed
  - stg_items: unique test on item_id failed
```

**Solução:**
1. **Identificar duplicatas:**
```sql
SELECT item_id, date, COUNT(*) as count
FROM {{ ref('stg_items') }}
GROUP BY item_id, date
HAVING COUNT(*) > 1
```

2. **Corrigir deduplicação:**
```sql
-- Usar QUALIFY para deduplicar
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY item_id, date
    ORDER BY loaded_at DESC
) = 1
```

---

### Problema: dbt run lento

**Sintomas:**
```
dbt run takes > 30 minutes
```

**Soluções:**

1. **Usar incremental models:**
```sql
{{ config(materialized='incremental') }}

SELECT * FROM {{ ref('stg_items') }}
{% if is_incremental() %}
    WHERE loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
{% endif %}
```

2. **Otimizar queries:**
```sql
-- Adicionar WHERE clause early
WHERE date >= CURRENT_DATE - 90

-- Usar LIMIT em desenvolvimento
{% if target.name == 'dev' %}
    LIMIT 1000
{% endif %}
```

---

### Problema: dbt connection timeout

**Sintomas:**
```
Error: Connection timeout to Databricks
```

**Solução:**
```yaml
# profiles.yml
nova_corrente:
  target: prod
  outputs:
    prod:
      type: databricks
      threads: 4  # Reduzir threads
      connect_timeout: 60  # Aumentar timeout
      connection_parameters:
        http_path: "{{ env_var('DATABRICKS_HTTP_PATH') }}"
        server_hostname: "{{ env_var('DATABRICKS_HOST') }}"
        access_token: "{{ env_var('DATABRICKS_TOKEN') }}"
```

---

<a name="airflow"></a>

## 4. 🔄 PROBLEMAS DE AIRFLOW

### Problema: DAG não aparece na UI

**Sintomas:**
```
DAG file existe mas não aparece no Airflow UI
```

**Solução:**
1. **Verificar syntax:**
```bash
python -m py_compile dags/nova_corrente/my_dag.py
```

2. **Verificar imports:**
```python
# Verificar se todos imports estão disponíveis
python -c "from airflow import DAG"
```

3. **Verificar permissões:**
```bash
chmod 644 dags/nova_corrente/*.py
```

4. **Restart scheduler:**
```bash
docker-compose restart airflow-scheduler
```

---

### Problema: Task falha intermitentemente

**Sintomas:**
```
Task fails sometimes but not always
```

**Solução:**
1. **Aumentar retries:**
```python
default_args = {
    'retries': 5,
    'retry_delay': timedelta(minutes=10),
    'retry_exponential_backoff': True,
}
```

2. **Adicionar timeout:**
```python
task = BashOperator(
    task_id='my_task',
    bash_command='python script.py',
    execution_timeout=timedelta(minutes=30),
    dag=dag,
)
```

---

<a name="ml"></a>

## 5. 🤖 PROBLEMAS DE ML

### Problema: MAPE > 15%

**Sintomas:**
```
MAPE: 25% (esperado: < 15%)
```

**Soluções:**

1. **Feature engineering:**
```python
# Adicionar mais features temporais
df['lag_7'] = df['demand'].shift(7)
df['rolling_mean_30'] = df['demand'].rolling(30).mean()
```

2. **Hyperparameter tuning:**
```python
# Prophet
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='multiplicative',  # Tentar multiplicative
    changepoint_prior_scale=0.05  # Ajustar changepoints
)
```

3. **Ensemble:**
```python
# Combinar modelos
ensemble = 0.4 * prophet_pred + 0.3 * arima_pred + 0.3 * lstm_pred
```

---

### Problema: Modelo não treina

**Sintomas:**
```
Error: Not enough data for training
```

**Solução:**
```python
# Verificar quantidade de dados
print(f"Train samples: {len(X_train)}")
print(f"Min required: {min_samples_required}")

# Se insuficiente, reduzir features ou aumentar dados históricos
if len(X_train) < min_samples_required:
    # Reduzir features ou usar dados mais antigos
    pass
```

---

<a name="bi"></a>

## 6. 📊 PROBLEMAS DE BI TOOLS

### Problema: Metabase query lenta

**Sintomas:**
```
Query takes > 30 seconds in Metabase
```

**Soluções:**

1. **Criar materialized view:**
```sql
CREATE MATERIALIZED VIEW forecast_summary AS
SELECT 
    category,
    date,
    AVG(mape) as avg_mape
FROM fact_forecasts
GROUP BY category, date;
```

2. **Otimizar query:**
```sql
-- Adicionar WHERE early
WHERE date >= CURRENT_DATE - 30

-- Usar LIMIT
LIMIT 10000
```

3. **Configurar caching:**
```yaml
# Metabase settings
query_caching_min_ttl: 3600  # 1 hour
```

---

### Problema: Conexão Metabase → Databricks falha

**Sintomas:**
```
Error: Cannot connect to Databricks
```

**Solução:**
1. **Verificar credentials:**
   - Host correto
   - HTTP Path correto
   - Token válido

2. **Testar conexão:**
```bash
curl -X GET \
  "https://<workspace>.cloud.databricks.com/api/2.0/sql/warehouses" \
  -H "Authorization: Bearer <token>"
```

3. **Verificar firewall:**
   - Metabase IP whitelisted no Databricks

---

## 🔍 DEBUGGING GERAL

### Logs Importantes

**dbt:**
```bash
dbt run --debug  # Verbose logging
tail -f logs/dbt.log
```

**Airflow:**
```bash
# Ver logs de task
airflow tasks logs dag_id task_id execution_date

# Ou via UI: Admin → Logs
```

**Databricks:**
```python
# Spark logs
spark.sparkContext.setLogLevel("DEBUG")
```

---

### Performance Profiling

**dbt:**
```bash
dbt run --profile  # Performance profiling
```

**Python:**
```python
import cProfile
cProfile.run('my_function()')
```

---

## 📞 SUPORTE

**Documentação:**
- dbt: https://docs.getdbt.com
- Airflow: https://airflow.apache.org/docs
- Databricks: https://docs.databricks.com

**Comunidade:**
- dbt Slack: #nova-corrente
- Airflow Slack: #help

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia de Troubleshooting Completo

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

