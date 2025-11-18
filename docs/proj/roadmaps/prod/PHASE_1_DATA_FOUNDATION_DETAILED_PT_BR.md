# 🏗️ FASE 1: DATA FOUNDATION - GUIA DETALHADO
## Nova Corrente - Analytics Engineering Roadmap

**Versão:** 1.0  
**Data:** Novembro 2025  
**Duração:** 2 semanas  
**Status:** 📋 Plano de Implementação (60% já completo via pré-processamento)

---

## 📋 OBJETIVOS DA FASE 1

**Meta Principal:**
Implementar completamente a Silver layer com dados limpos, validados e prontos para analytics.

**Objetivos Específicos:**
1. ✅ Completar limpeza de dados (já 60% feito)
2. ⏳ Implementar staging models no dbt
3. ⏳ Setup Great Expectations suite completo
4. ⏳ Data profiling automatizado
5. ⏳ Documentação completa da Silver layer

---

## 🎯 ENTREGAS PRINCIPAIS

### 1. Staging Models dbt (Silver Layer)

**Objetivo:** Criar modelos staging para todos os datasets processados

**Estrutura:**
```
dbt/models/staging/
├── _staging.yml
├── stg_items.sql
├── stg_towers.sql
├── stg_forecasts.sql
├── stg_inventory.sql
├── stg_weather.sql
├── stg_economic.sql
└── stg_5g_expansion.sql
```

**Exemplo: stg_items.sql**

```sql
-- models/staging/stg_items.sql
{{ config(
    materialized='view',
    schema='staging',
    tags=['staging', 'items', 'nova-corrente']
) }}

WITH source AS (
    SELECT * FROM {{ source('bronze', 'raw_items') }}
    WHERE _partition_date = CURRENT_DATE - 1
),

cleaned AS (
    SELECT
        -- Primary keys
        CAST(item_id AS STRING) AS item_id,
        CAST(family AS STRING) AS family,
        
        -- Attributes
        TRIM(item_name) AS item_name,
        LOWER(category) AS category,
        CAST(supplier_id AS STRING) AS supplier_id,
        
        -- Metrics
        CAST(cost AS DECIMAL(10, 2)) AS cost,
        CAST(quantity AS INTEGER) AS quantity,
        CAST(current_stock AS INTEGER) AS current_stock,
        
        -- Lead time
        CAST(lead_time_days AS INTEGER) AS lead_time_days,
        
        -- Timestamps
        CAST(date AS DATE) AS date,
        CAST(created_at AS TIMESTAMP) AS created_at,
        CURRENT_TIMESTAMP() AS loaded_at
        
    FROM source
    WHERE item_id IS NOT NULL
        AND item_name IS NOT NULL
        AND cost > 0
        AND date >= '2024-01-01'  -- Valid date range
),

deduplicated AS (
    SELECT *
    FROM cleaned
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY item_id, date
        ORDER BY loaded_at DESC
    ) = 1
),

enriched AS (
    SELECT
        *,
        -- Business logic
        CASE 
            WHEN current_stock <= 0 THEN 'OUT_OF_STOCK'
            WHEN current_stock <= 10 THEN 'LOW_STOCK'
            ELSE 'OK'
        END AS stock_status,
        
        -- Calculated metrics
        cost * quantity AS total_value,
        cost / NULLIF(quantity, 0) AS unit_cost
        
    FROM deduplicated
)

SELECT * FROM enriched
```

**Exemplo: stg_forecasts.sql**

```sql
-- models/staging/stg_forecasts.sql
{{ config(
    materialized='view',
    schema='staging',
    tags=['staging', 'forecasts', 'ml']
) }}

WITH source AS (
    SELECT * FROM {{ source('bronze', 'raw_forecasts') }}
    WHERE _partition_date = CURRENT_DATE - 1
),

cleaned AS (
    SELECT
        CAST(forecast_id AS BIGINT) AS forecast_id,
        CAST(item_id AS STRING) AS item_id,
        CAST(date AS DATE) AS forecast_date,
        
        -- Forecast values
        CAST(forecasted_demand AS DECIMAL(10, 2)) AS forecasted_demand,
        CAST(actual_demand AS DECIMAL(10, 2)) AS actual_demand,
        
        -- Model info
        CAST(model_type AS STRING) AS model_type,
        CAST(confidence_interval_lower AS DECIMAL(10, 2)) AS ci_lower,
        CAST(confidence_interval_upper AS DECIMAL(10, 2)) AS ci_upper,
        
        -- Metrics
        CAST(mape AS DECIMAL(5, 2)) AS mape,
        
        -- Timestamps
        CAST(created_at AS TIMESTAMP) AS created_at,
        CURRENT_TIMESTAMP() AS loaded_at
        
    FROM source
    WHERE forecast_id IS NOT NULL
        AND item_id IS NOT NULL
        AND forecast_date >= CURRENT_DATE - 90
),

with_calculations AS (
    SELECT
        *,
        -- Calculate MAPE if missing
        CASE 
            WHEN mape IS NULL AND actual_demand > 0 
            THEN ABS(forecasted_demand - actual_demand) / actual_demand * 100
            ELSE mape
        END AS calculated_mape,
        
        -- Forecast accuracy
        CASE 
            WHEN calculated_mape < 10 THEN 'EXCELLENT'
            WHEN calculated_mape < 15 THEN 'GOOD'
            WHEN calculated_mape < 20 THEN 'ACCEPTABLE'
            ELSE 'POOR'
        END AS accuracy_level
        
    FROM cleaned
)

SELECT * FROM with_calculations
```

**Checklist:**
- [ ] Todos os datasets transformados em staging models
- [ ] Schema YAMLs preenchidos com testes
- [ ] Validações básicas implementadas
- [ ] dbt test passando (100%)

---

### 2. Great Expectations Suite Completa

**Objetivo:** Implementar validações robustas de qualidade de dados

**Estrutura:**
```
great_expectations/
├── great_expectations.yml
├── expectations/
│   ├── items_expectations.json
│   ├── forecasts_expectations.json
│   └── inventory_expectations.json
├── checkpoints/
│   ├── items_checkpoint.yml
│   └── forecasts_checkpoint.yml
└── data_docs/
```

**Exemplo: expectations/items_expectations.json**

```json
{
  "expectation_suite_name": "items_expectations",
  "expectations": [
    {
      "expectation_type": "expect_table_row_count_to_be_between",
      "kwargs": {
        "min_value": 100,
        "max_value": 10000
      }
    },
    {
      "expectation_type": "expect_column_to_exist",
      "kwargs": {
        "column": "item_id"
      }
    },
    {
      "expectation_type": "expect_column_values_to_be_unique",
      "kwargs": {
        "column": "item_id"
      }
    },
    {
      "expectation_type": "expect_column_values_to_not_be_null",
      "kwargs": {
        "column": "item_id",
        "mostly": 1.0
      }
    },
    {
      "expectation_type": "expect_column_values_to_be_between",
      "kwargs": {
        "column": "cost",
        "min_value": 0,
        "max_value": 1000000
      }
    },
    {
      "expectation_type": "expect_column_values_to_be_in_set",
      "kwargs": {
        "column": "category",
        "value_set": ["connectors", "cables", "structures", "other"]
      }
    },
    {
      "expectation_type": "expect_column_mean_to_be_between",
      "kwargs": {
        "column": "lead_time_days",
        "min_value": 5,
        "max_value": 30
      }
    },
    {
      "expectation_type": "expect_column_values_to_match_regex",
      "kwargs": {
        "column": "item_id",
        "regex": "^[A-Z]{3,5}-[0-9]{3,5}$"
      }
    }
  ]
}
```

**Integração com Airflow:**

```python
# dags/nova_corrente/data_quality_check.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from great_expectations.checkpoint import Checkpoint
from great_expectations.data_context import DataContext

def validate_data_quality(**context):
    """Run Great Expectations validation"""
    context = DataContext()
    
    checkpoint = Checkpoint(
        name="items_checkpoint",
        data_context=context,
        expectation_suite_name="items_expectations"
    )
    
    result = checkpoint.run()
    
    if result.success:
        print("✅ Data quality validation passed")
    else:
        print("❌ Data quality validation failed")
        print(result.statistics)
        raise ValueError("Data quality check failed")
    
    return result

dag = DAG(
    'nova_corrente_data_quality',
    default_args=default_args,
    description='Data quality validation',
    schedule_interval='@daily',
    start_date=datetime(2025, 11, 1),
    catchup=False,
)

validate_task = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_data_quality,
    provide_context=True,
    dag=dag,
)
```

**Checklist:**
- [ ] Expectation suites criadas para todos datasets
- [ ] Checkpoints configurados
- [ ] Integração com Airflow funcionando
- [ ] Data docs gerados e acessíveis
- [ ] Alerts configurados para falhas

---

### 3. Data Profiling Automatizado

**Objetivo:** Perfis de dados gerados automaticamente

**Script de Profiling:**

```python
# scripts/auto_data_profiling.py
import pandas as pd
import great_expectations as ge
from datetime import datetime

def generate_data_profile(df, dataset_name):
    """Generate comprehensive data profile"""
    
    # Basic statistics
    profile = {
        'dataset': dataset_name,
        'timestamp': datetime.now().isoformat(),
        'row_count': len(df),
        'column_count': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
    }
    
    # Column-level statistics
    columns = {}
    for col in df.columns:
        col_stats = {
            'dtype': str(df[col].dtype),
            'null_count': df[col].isnull().sum(),
            'null_percentage': (df[col].isnull().sum() / len(df)) * 100,
            'unique_count': df[col].nunique(),
        }
        
        # Numeric columns
        if df[col].dtype in ['int64', 'float64']:
            col_stats.update({
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'median': df[col].median(),
            })
        
        # Categorical columns
        if df[col].dtype == 'object':
            col_stats['top_values'] = df[col].value_counts().head(5).to_dict()
        
        columns[col] = col_stats
    
    profile['columns'] = columns
    
    return profile

# Usage
if __name__ == "__main__":
    df = pd.read_parquet("s3://bronze/items/data.parquet")
    profile = generate_data_profile(df, "items")
    
    # Save profile
    import json
    with open(f"data_profiles/{profile['dataset']}_profile.json", "w") as f:
        json.dump(profile, f, indent=2, default=str)
```

**Integração com dbt:**

```yaml
# dbt_project.yml
on-run-end:
  - "python scripts/auto_data_profiling.py"
```

**Checklist:**
- [ ] Script de profiling criado
- [ ] Integração com pipeline automatizada
- [ ] Profiles salvos em formato estruturado
- [ ] Dashboard de profiles (opcional)

---

### 4. Documentação Silver Layer

**Objetivo:** Documentação completa da Silver layer

**Arquivo: docs/silver_layer_documentation.md**

```markdown
# Silver Layer Documentation

## Overview
Silver layer contains cleaned, validated, and enriched data ready for analytics.

## Datasets

### stg_items
- **Source:** Bronze layer raw_items
- **Rows:** ~4,207 (daily)
- **Schema:** [document schema]
- **Business Rules:** [document rules]
- **Data Quality:** Score 90%+

### stg_forecasts
- **Source:** ML models predictions
- **Rows:** ~540 items × 30 days
- **Schema:** [document schema]
- **Retention:** 90 days
```

**Checklist:**
- [ ] Documentação criada para todos datasets
- [ ] Schemas documentados
- [ ] Business rules documentadas
- [ ] Data lineage mapeado
- [ ] Acessível via DataHub (quando implementado)

---

## 📊 MÉTRICAS DE SUCESSO FASE 1

**Técnicas:**
- ✅ Staging models: 100% dos datasets
- ✅ Data quality score: 90%+ (atual: 70% → meta: 90%)
- ✅ Great Expectations: 100% pass rate
- ✅ Data profiling: Automatizado e atualizado diariamente

**Processo:**
- ✅ Documentação completa Silver layer
- ✅ dbt docs gerados e acessíveis
- ✅ Pipeline de validação funcionando

---

## 🚀 PRÓXIMOS PASSOS

Após conclusão da Fase 1:
1. Validar Silver layer completa
2. Preparar para Fase 2 (Gold layer / Analytics)
3. Setup BI tools (Metabase/Superset)

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia Detalhado Fase 1

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

