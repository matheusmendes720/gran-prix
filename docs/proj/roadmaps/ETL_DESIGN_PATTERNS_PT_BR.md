# 🔄 ETL DESIGN PATTERNS - PRODUÇÃO
## Nova Corrente - Data Engineering Patterns

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Patterns Completos

---

## 📋 ÍNDICE

1. [ELT vs ETL Pattern](#elt-vs-etl)
2. [Medallion Architecture Pattern](#medallion)
3. [Incremental Loading Pattern](#incremental)
4. [Change Data Capture (CDC)](#cdc)
5. [Idempotent Pipelines](#idempotent)
6. [Slowly Changing Dimensions (SCD)](#scd)
7. [Data Quality Gates](#quality-gates)
8. [Error Handling Patterns](#error-handling)

---

<a name="elt-vs-etl"></a>

## 1. 🔄 ELT vs ETL PATTERN

### 1.1 ELT Pattern (Recomendado)

**Extract → Load → Transform**

**Vantagens:**
- Flexibilidade (transformações podem mudar)
- Performance (processamento no warehouse)
- Escalabilidade (compute separado de storage)
- Velocidade (load rápido, transform depois)

**Implementação:**

```python
# Step 1: Extract & Load (raw to Bronze)
def extract_and_load():
    """Extract from source and load raw to Bronze"""
    # Extract from ERP
    data = extract_from_erp()
    
    # Load raw to S3 (Bronze)
    load_to_s3(data, path="bronze/erp/year=2025/month=11/day=01/data.parquet")
    
    # No transformation here - just raw data

# Step 2: Transform (Bronze → Silver → Gold)
def transform_with_dbt():
    """Transform using dbt in the warehouse"""
    # dbt transforms in-place (no ETL needed)
    # Bronze → Silver (cleaned)
    # Silver → Gold (curated)
    
    # Run dbt models
    subprocess.run(["dbt", "run", "--models", "staging.*"])
    subprocess.run(["dbt", "run", "--models", "marts.*"])
```

---

### 1.2 ETL Pattern (Legacy)

**Extract → Transform → Load**

**Quando usar:**
- Dados sensíveis (PII) - transformar antes de armazenar
- Storage limitado - transformar e filtrar antes
- APIs externas - precisa transformar antes de salvar

**Implementação:**

```python
# Step 1: Extract
data = extract_from_source()

# Step 2: Transform (before loading)
transformed_data = transform_data(data)
# - Clean data
# - Mask PII
# - Filter records
# - Aggregate

# Step 3: Load (transformed to Bronze)
load_to_s3(transformed_data)
```

---

<a name="medallion"></a>

## 2. 🥇 MEDALLION ARCHITECTURE PATTERN

### 2.1 Bronze Layer (Raw)

**Princípios:**
- Dados brutos como chegam
- Sem transformações
- Schema evolução permitida
- Particionamento por data

**Implementação:**

```python
# Load to Bronze
def load_to_bronze(df, source, date):
    """Load raw data to Bronze layer"""
    year = date.year
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"
    
    s3_path = f"s3://bronze/{source}/year={year}/month={month}/day={day}/data.parquet"
    
    df.to_parquet(
        s3_path,
        partition_cols=['year', 'month', 'day'],
        compression='snappy'
    )
```

---

### 2.2 Silver Layer (Cleaned)

**Princípios:**
- Dados limpos e validados
- Schema aplicado
- Duplicatas removidas
- Tipos corrigidos

**Implementação:**

```sql
-- dbt model: Bronze → Silver
-- models/staging/stg_items.sql
{{ config(materialized='view', schema='staging') }}

WITH source AS (
    SELECT * FROM {{ source('bronze', 'raw_items') }}
    WHERE _partition_date = CURRENT_DATE - 1
),

cleaned AS (
    SELECT
        CAST(item_id AS STRING) AS item_id,
        TRIM(item_name) AS item_name,
        CAST(cost AS DECIMAL(10, 2)) AS cost,
        -- Validation
        CASE WHEN cost > 0 THEN cost ELSE NULL END AS cost_validated
    FROM source
    WHERE item_id IS NOT NULL
),

deduplicated AS (
    SELECT *
    FROM cleaned
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY item_id, date
        ORDER BY loaded_at DESC
    ) = 1
)

SELECT * FROM deduplicated
```

---

### 2.3 Gold Layer (Curated)

**Princípios:**
- Modelos de negócio (star schema)
- Métricas pré-calculadas
- Performance otimizado
- Ready for BI

**Implementação:**

```sql
-- dbt model: Silver → Gold
-- models/marts/fact_forecasts.sql
{{ config(
    materialized='table',
    schema='marts',
    partition_by={'field': 'date', 'data_type': 'date'},
    cluster_by=['item_id']
) }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_forecasts') }}
),

dim_items AS (
    SELECT * FROM {{ ref('dim_items') }}
),

final AS (
    SELECT
        f.forecast_id,
        f.item_id,
        i.category,
        f.date,
        f.forecasted_demand,
        f.actual_demand,
        f.mape,
        -- Pre-calculated metrics
        f.forecasted_demand - f.actual_demand AS forecast_error,
        ABS(f.forecasted_demand - f.actual_demand) AS absolute_error
    FROM staging f
    INNER JOIN dim_items i ON f.item_id = i.item_id
)

SELECT * FROM final
```

---

<a name="incremental"></a>

## 3. ⬆️ INCREMENTAL LOADING PATTERN

### 3.1 Pattern: Incremental Load

**Objetivo:** Carregar apenas dados novos/modificados

**Implementação:**

```python
# Incremental load using merge
from delta.tables import DeltaTable

def incremental_load(source_df, target_path, key_column='id'):
    """Load data incrementally"""
    # Read target Delta table
    target_delta = DeltaTable.forPath(spark, target_path)
    
    # Merge new data
    target_delta.alias("target").merge(
        source_df.alias("source"),
        f"target.{key_column} = source.{key_column}"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

**dbt Incremental Model:**

```sql
-- models/marts/fact_forecasts.sql
{{ config(
    materialized='incremental',
    unique_key='forecast_id',
    on_schema_change='append_new_columns'
) }}

SELECT * FROM {{ ref('stg_forecasts') }}

{% if is_incremental() %}
    WHERE loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
{% endif %}
```

---

<a name="cdc"></a>

## 4. 🔄 CHANGE DATA CAPTURE (CDC)

### 4.1 CDC Pattern

**Objetivo:** Capturar mudanças em tempo real

**Implementação:**

```python
# CDC handler using Debezium + Kafka
from kafka import KafkaConsumer

class CDCHandler:
    """Handle CDC events"""
    
    def process_cdc_events(self):
        consumer = KafkaConsumer(
            'erp-cdc',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        for message in consumer:
            event = message.value
            
            if event['op'] == 'c':  # Create
                self.handle_insert(event['after'])
            elif event['op'] == 'u':  # Update
                self.handle_update(event['before'], event['after'])
            elif event['op'] == 'd':  # Delete
                self.handle_delete(event['before'])
    
    def handle_update(self, before, after):
        """Handle update event"""
        # Load updated record
        load_to_bronze(pd.DataFrame([after]))
```

---

<a name="idempotent"></a>

## 5. 🔁 IDEMPOTENT PIPELINES

### 5.1 Idempotent Pattern

**Objetivo:** Pipelines que podem ser re-executados com segurança

**Implementação:**

```python
def idempotent_pipeline(execution_date):
    """Pipeline that can be safely re-run"""
    # Check if already processed
    if is_already_processed(execution_date):
        print(f"Already processed for {execution_date}, skipping")
        return
    
    # Process
    extract(execution_date)
    transform(execution_date)
    load(execution_date)
    
    # Mark as processed
    mark_as_processed(execution_date)

def is_already_processed(date):
    """Check if date already processed"""
    query = f"""
        SELECT COUNT(*) as count
        FROM processing_log
        WHERE execution_date = '{date.date()}'
        AND status = 'SUCCESS'
    """
    result = execute_query(query)
    return result['count'] > 0
```

---

<a name="scd"></a>

## 6. 📅 SLOWLY CHANGING DIMENSIONS (SCD)

### 6.1 SCD Type 2 Pattern

**Objetivo:** Manter histórico completo de dimensões

**Implementação:**

```sql
-- dbt model: dim_items (SCD Type 2)
{{ config(
    materialized='table',
    unique_key='item_id',
    strategy='check',
    check_cols=['item_name', 'category', 'cost']
) }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_items') }}
),

current_records AS (
    SELECT *
    FROM {{ this }}
    WHERE valid_to IS NULL
),

merged AS (
    SELECT
        s.item_id,
        s.item_name,
        s.category,
        s.cost,
        CASE
            WHEN c.item_id IS NULL THEN CURRENT_TIMESTAMP()  -- New record
            WHEN s.item_name != c.item_name 
                 OR s.category != c.category 
                 OR s.cost != c.cost 
            THEN CURRENT_TIMESTAMP()  -- Changed record
            ELSE c.valid_from  -- No change
        END AS valid_from,
        NULL AS valid_to,
        TRUE AS is_current
    FROM staging s
    LEFT JOIN current_records c ON s.item_id = c.item_id
)

SELECT * FROM merged
```

---

<a name="quality-gates"></a>

## 7. ✅ DATA QUALITY GATES

### 7.1 Quality Gate Pattern

**Objetivo:** Validar qualidade antes de prosseguir

**Implementação:**

```python
def quality_gate(df, expectations):
    """Validate data quality before proceeding"""
    suite = ge.dataset.PandasDataset(df)
    
    for expectation in expectations:
        result = suite.validate_expectation(expectation)
        if not result.success:
            raise DataQualityError(f"Quality gate failed: {expectation}")
    
    return True

# Usage in pipeline
def pipeline_with_quality_gates():
    # Extract
    data = extract()
    
    # Quality gate 1
    quality_gate(data, [
        {'expectation_type': 'expect_column_to_exist', 'kwargs': {'column': 'item_id'}},
        {'expectation_type': 'expect_column_values_to_not_be_null', 'kwargs': {'column': 'item_id'}}
    ])
    
    # Transform
    transformed = transform(data)
    
    # Quality gate 2
    quality_gate(transformed, [
        {'expectation_type': 'expect_column_values_to_be_between', 
         'kwargs': {'column': 'cost', 'min_value': 0, 'max_value': 1000000}}
    ])
    
    # Load
    load(transformed)
```

---

<a name="error-handling"></a>

## 8. ⚠️ ERROR HANDLING PATTERNS

### 8.1 Retry Pattern

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def extract_with_retry():
    """Extract with automatic retry"""
    return extract_from_source()
```

### 8.2 Dead Letter Queue Pattern

```python
def pipeline_with_dlq():
    """Pipeline with dead letter queue for failures"""
    try:
        process_data()
    except Exception as e:
        # Send to dead letter queue
        send_to_dlq(data, error=str(e))
        # Continue processing other records
        pass
```

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ ETL Design Patterns Completos

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**







