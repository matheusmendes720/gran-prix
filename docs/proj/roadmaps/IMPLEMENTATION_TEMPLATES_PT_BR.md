# 📋 TEMPLATES DE IMPLEMENTAÇÃO
## Nova Corrente - Analytics Engineering

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Templates Prontos para Uso

---

## 📋 ÍNDICE

1. [Templates dbt](#templates-dbt)
2. [Templates Airflow](#templates-airflow)
3. [Templates Terraform](#templates-terraform)
4. [Templates Python](#templates-python)
5. [Templates SQL](#templates-sql)
6. [Checklists](#checklists)

---

<a name="templates-dbt"></a>

## 1. 📊 TEMPLATES DBT

### 1.1 Model Staging Template

```sql
-- models/staging/stg_items.sql
{{ config(
    materialized='view',
    schema='staging',
    tags=['staging', 'items']
) }}

WITH source AS (
    SELECT * FROM {{ source('bronze', 'raw_items') }}
    WHERE date = CURRENT_DATE - 1  -- Process yesterday's data
),

cleaned AS (
    SELECT
        -- Primary keys
        CAST(item_id AS STRING) AS item_id,
        
        -- Attributes
        TRIM(item_name) AS item_name,
        LOWER(category) AS category,
        CAST(supplier_id AS STRING) AS supplier_id,
        
        -- Metrics
        CAST(cost AS DECIMAL(10, 2)) AS cost,
        CAST(quantity AS INTEGER) AS quantity,
        
        -- Timestamps
        CAST(created_at AS TIMESTAMP) AS created_at,
        CURRENT_TIMESTAMP() AS loaded_at
        
    FROM source
    WHERE item_id IS NOT NULL
        AND item_name IS NOT NULL
        AND cost > 0
),

deduplicated AS (
    SELECT *
    FROM cleaned
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY item_id, created_at
        ORDER BY loaded_at DESC
    ) = 1
)

SELECT * FROM deduplicated
```

### 1.2 Model Dimension Template

```sql
-- models/marts/dim_items.sql
{{ config(
    materialized='table',
    schema='marts',
    tags=['marts', 'dimensions', 'items'],
    cluster_by=['category']
) }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_items') }}
),

final AS (
    SELECT
        item_id,
        item_name,
        category,
        supplier_id,
        cost,
        CURRENT_TIMESTAMP() AS valid_from,
        NULL AS valid_to,
        TRUE AS is_current
    FROM staging
)

SELECT * FROM final
```

### 1.3 Model Fact Template

```sql
-- models/marts/fact_forecasts.sql
{{ config(
    materialized='table',
    schema='marts',
    tags=['marts', 'facts', 'forecasts'],
    cluster_by=['date'],
    partition_by={'field': 'date', 'data_type': 'date'}
) }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_forecasts') }}
),

items AS (
    SELECT * FROM {{ ref('dim_items') }}
),

final AS (
    SELECT
        f.forecast_id,
        f.item_id,
        i.item_name,
        i.category,
        f.date,
        f.forecasted_demand,
        f.actual_demand,
        f.model_type,
        f.mape,
        f.confidence_interval_lower,
        f.confidence_interval_upper,
        f.created_at
    FROM staging f
    INNER JOIN items i ON f.item_id = i.item_id
    WHERE f.date >= CURRENT_DATE - 90  -- Last 90 days
)

SELECT * FROM final
```

### 1.4 Schema YAML Template

```yaml
# models/staging/_staging.yml
version: 2

models:
  - name: stg_items
    description: "Staging layer for items from ERP system"
    
    columns:
      - name: item_id
        description: "Unique identifier for item"
        tests:
          - unique
          - not_null
      
      - name: item_name
        description: "Item name"
        tests:
          - not_null
      
      - name: category
        description: "Item category"
        tests:
          - not_null
          - accepted_values:
              values: ['connectors', 'cables', 'structures', 'other']
      
      - name: cost
        description: "Item cost in BRL"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```

---

<a name="templates-airflow"></a>

## 2. 🔄 TEMPLATES AIRFLOW

### 2.1 DAG Template Base

```python
# dags/nova_corrente/template_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

default_args = {
    'owner': 'nova-corrente',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email': ['data-team@novacorrente.com'],
}

dag = DAG(
    'nova_corrente_template',
    default_args=default_args,
    description='Template DAG for Nova Corrente pipelines',
    schedule_interval='@daily',
    start_date=datetime(2025, 11, 1),
    catchup=False,
    tags=['nova-corrente', 'template'],
    max_active_runs=1,
    max_active_tasks=10,
)

# Task 1: Extract
extract_task = BashOperator(
    task_id='extract_data',
    bash_command='python /opt/airflow/scripts/extract.py',
    dag=dag,
)

# Task 2: Wait for file
wait_for_file = FileSensor(
    task_id='wait_for_data',
    filepath='/data/raw/data.csv',
    poke_interval=30,
    timeout=300,
    dag=dag,
)

# Task 3: Transform (dbt)
run_dbt = BashOperator(
    task_id='run_dbt',
    bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir .',
    env={'DBT_PROFILES_DIR': '/opt/airflow/dbt'},
    dag=dag,
)

# Task 4: Test
test_dbt = BashOperator(
    task_id='test_dbt',
    bash_command='cd /opt/airflow/dbt && dbt test --profiles-dir .',
    env={'DBT_PROFILES_DIR': '/opt/airflow/dbt'},
    dag=dag,
)

# Task 5: Databricks job
databricks_job = DatabricksRunNowOperator(
    task_id='run_databricks_job',
    job_id=12345,
    dag=dag,
)

# Define dependencies
extract_task >> wait_for_file >> run_dbt >> test_dbt >> databricks_job
```

### 2.2 Python Operator Template

```python
# dags/nova_corrente/python_task_template.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract_and_load(**context):
    """
    Extract data and load to Bronze layer
    """
    import boto3
    import pandas as pd
    
    # Get execution date
    execution_date = context['execution_date']
    
    # Extract data
    data = extract_from_source(execution_date)
    
    # Load to S3
    load_to_bronze(data, execution_date)
    
    return f"Processed {len(data)} rows"

def extract_from_source(date):
    """Extract data from source"""
    # Implementation here
    return pd.DataFrame()

def load_to_bronze(data, date):
    """Load data to Bronze layer"""
    s3_client = boto3.client('s3')
    # Implementation here
    pass

dag = DAG(
    'nova_corrente_python_template',
    default_args=default_args,
    description='Python operator template',
    schedule_interval='@daily',
    start_date=datetime(2025, 11, 1),
    catchup=False,
)

python_task = PythonOperator(
    task_id='extract_and_load',
    python_callable=extract_and_load,
    provide_context=True,
    dag=dag,
)
```

---

<a name="templates-terraform"></a>

## 3. 🏗️ TEMPLATES TERRAFORM

### 3.1 S3 Module Template

```hcl
# modules/s3/main.tf
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  
  tags = merge(
    var.tags,
    {
      Name = var.bucket_name
    }
  )
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = var.versioning ? "Enabled" : "Disabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  dynamic "rule" {
    for_each = var.lifecycle_rules
    content {
      id     = rule.value.id
      status = rule.value.enabled ? "Enabled" : "Disabled"
      
      expiration {
        days = rule.value.expiration.days
      }
    }
  }

  depends_on = [aws_s3_bucket_versioning.this]
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets  = true
}
```

### 3.2 Variables Template

```hcl
# modules/s3/variables.tf
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "versioning" {
  description = "Enable versioning"
  type        = bool
  default     = true
}

variable "lifecycle_rules" {
  description = "Lifecycle rules for the bucket"
  type = list(object({
    id      = string
    enabled = bool
    expiration = object({
      days = number
    })
  }))
  default = []
}

variable "tags" {
  description = "Tags for the bucket"
  type        = map(string)
  default     = {}
}
```

---

<a name="templates-python"></a>

## 4. 🐍 TEMPLATES PYTHON

### 4.1 Data Extraction Template

```python
# scripts/extract_template.py
"""
Template for data extraction from sources
"""
import pandas as pd
import boto3
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExtractor:
    """Base class for data extraction"""
    
    def __init__(self, source_name: str, bronze_bucket: str):
        self.source_name = source_name
        self.bronze_bucket = bronze_bucket
        self.s3_client = boto3.client('s3')
    
    def extract(self, date: datetime = None) -> pd.DataFrame:
        """
        Extract data from source
        
        Args:
            date: Date to extract (defaults to yesterday)
        
        Returns:
            DataFrame with extracted data
        """
        if date is None:
            date = datetime.now()
        
        logger.info(f"Extracting data from {self.source_name} for {date}")
        
        # Implementation here
        data = self._fetch_data(date)
        
        logger.info(f"Extracted {len(data)} rows")
        return data
    
    def load_to_bronze(self, data: pd.DataFrame, date: datetime = None):
        """
        Load data to Bronze layer in S3
        
        Args:
            data: DataFrame to load
            date: Partition date
        """
        if date is None:
            date = datetime.now()
        
        # Build S3 key
        year = date.year
        month = f"{date.month:02d}"
        day = f"{date.day:02d}"
        
        s3_key = f"{self.source_name}/year={year}/month={month}/day={day}/data.parquet"
        
        # Convert to Parquet
        parquet_buffer = data.to_parquet(index=False)
        
        # Upload to S3
        self.s3_client.put_object(
            Bucket=self.bronze_bucket,
            Key=s3_key,
            Body=parquet_buffer,
            ContentType='application/parquet'
        )
        
        logger.info(f"✅ Loaded to s3://{self.bronze_bucket}/{s3_key}")
    
    def _fetch_data(self, date: datetime) -> pd.DataFrame:
        """Fetch data from source - to be implemented by subclasses"""
        raise NotImplementedError

# Usage example
if __name__ == "__main__":
    extractor = DataExtractor("erp", "nova-corrente-data-lake-bronze")
    data = extractor.extract()
    extractor.load_to_bronze(data)
```

### 4.2 Data Quality Template

```python
# scripts/data_quality_template.py
"""
Template for data quality checks using Great Expectations
"""
import great_expectations as ge
from great_expectations.dataset import SparkDFDataset
import pandas as pd

def validate_data_quality(df: pd.DataFrame, expectation_suite: dict) -> dict:
    """
    Validate data quality using Great Expectations
    
    Args:
        df: DataFrame to validate
        expectation_suite: Expectation suite dictionary
    
    Returns:
        Validation result dictionary
    """
    # Create GE dataset
    dataset = ge.dataset.PandasDataset(df)
    
    # Load expectations
    dataset.set_default_expectation_argument("result_format", "COMPLETE")
    
    # Run validations
    results = []
    for expectation in expectation_suite['expectations']:
        result = dataset.validate_expectation(expectation)
        results.append(result)
    
    # Calculate pass rate
    passed = sum(1 for r in results if r.success)
    total = len(results)
    pass_rate = (passed / total) * 100 if total > 0 else 0
    
    return {
        'pass_rate': pass_rate,
        'passed': passed,
        'total': total,
        'results': results
    }

# Example expectations
example_expectations = {
    'expectations': [
        {
            'expectation_type': 'expect_column_to_exist',
            'kwargs': {'column': 'item_id'}
        },
        {
            'expectation_type': 'expect_column_values_to_be_between',
            'kwargs': {
                'column': 'cost',
                'min_value': 0,
                'max_value': 1000000
            }
        },
        {
            'expectation_type': 'expect_column_values_to_be_unique',
            'kwargs': {'column': 'item_id'}
        }
    ]
}
```

---

<a name="templates-sql"></a>

## 5. 💾 TEMPLATES SQL

### 5.1 Reorder Point Macro

```sql
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
```

### 5.2 Safety Stock Macro

```sql
-- macros/safety_stock.sql
{% macro calculate_safety_stock(
    std_demand,
    lead_time,
    service_level=0.95
) %}
    {%- set z_score = 1.96 -%}  {# 95% service level #}
    {{ z_score * std_demand * sqrt(lead_time) }}
{% endmacro %}
```

### 5.3 MAPE Calculation

```sql
-- models/intermediate/int_forecast_accuracy.sql
{{ config(materialized='view') }}

WITH forecasts AS (
    SELECT * FROM {{ ref('stg_forecasts') }}
),

mape_calc AS (
    SELECT
        item_id,
        date,
        forecasted_demand,
        actual_demand,
        ABS(forecasted_demand - actual_demand) / NULLIF(actual_demand, 0) AS absolute_percentage_error
    FROM forecasts
    WHERE actual_demand > 0
)

SELECT
    item_id,
    AVG(absolute_percentage_error) * 100 AS mape,
    COUNT(*) AS observations
FROM mape_calc
GROUP BY item_id
```

---

<a name="checklists"></a>

## 6. ✅ CHECKLISTS

### 6.1 Checklist de Implementação dbt

```markdown
## dbt Implementation Checklist

### Setup
- [ ] dbt instalado (>= 1.6.0)
- [ ] Estrutura de pastas criada
- [ ] dbt_project.yml configurado
- [ ] profiles.yml configurado
- [ ] packages.yml definido
- [ ] dbt deps executado

### Models
- [ ] Staging models criados
- [ ] Intermediate models criados
- [ ] Marts models criados (dim/fact)
- [ ] Schema YAMLs preenchidos
- [ ] Tests definidos

### Testing
- [ ] dbt test executado (100% pass)
- [ ] Custom tests criados
- [ ] Data quality validada

### Documentation
- [ ] dbt docs generate executado
- [ ] dbt docs serve funcionando
- [ ] Lineage visualizado
```

### 6.2 Checklist de Implementação Airflow

```markdown
## Airflow Implementation Checklist

### Setup
- [ ] Docker instalado
- [ ] docker-compose.yml configurado
- [ ] Airflow UI acessível
- [ ] Admin user criado

### DAGs
- [ ] DAGs básicos criados
- [ ] Conexões configuradas
- [ ] Variáveis definidas
- [ ] Testes de execução passando

### Monitoring
- [ ] Logs configurados
- [ ] Alerts configurados
- [ ] Dashboards criados
```

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Templates Prontos para Uso

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

