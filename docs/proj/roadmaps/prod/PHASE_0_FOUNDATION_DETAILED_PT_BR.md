# 🏗️ FASE 0: FOUNDATION - GUIA DETALHADO
## Nova Corrente - Analytics Engineering Roadmap

**Versão:** 1.0  
**Data:** Novembro 2025  
**Duração:** 2 semanas  
**Status:** 📋 Plano de Implementação

---

## 📋 OBJETIVOS DA FASE 0

**Meta Principal:**
Estabelecer a base de infraestrutura e configuração inicial para suportar todo o pipeline de Analytics Engineering.

**Objetivos Específicos:**
1. ✅ Setup infraestrutura cloud (AWS/GCP)
2. ✅ Configurar repositório de dados Bronze layer
3. ✅ Criar estrutura do projeto dbt
4. ✅ Setup inicial do Airflow
5. ✅ Documentação inicial e onboarding

---

## 🎯 ENTREGAS PRINCIPAIS

### 1. Infraestrutura Cloud (Terraform)

**Objetivo:** Criar toda infraestrutura como código

**Arquivos a Criar:**
```
infrastructure/terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── modules/
│   ├── s3/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── databricks/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── networking/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── dev/
    │   └── terraform.tfvars
    ├── staging/
    │   └── terraform.tfvars
    └── prod/
        └── terraform.tfvars
```

**Exemplo: main.tf**

```hcl
# infrastructure/terraform/main.tf
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }
  
  backend "s3" {
    bucket         = "nova-corrente-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Provider configuration
provider "aws" {
  region = var.aws_region
}

provider "databricks" {
  host = var.databricks_host
}

# S3 Bucket for Bronze Layer
module "data_lake_bronze" {
  source = "./modules/s3"
  
  bucket_name = "nova-corrente-data-lake-bronze-${var.environment}"
  versioning  = true
  
  lifecycle_rules = [
    {
      id      = "delete-old-versions"
      enabled = true
      expiration = {
        days = 90
      }
    }
  ]
  
  tags = {
    Environment = var.environment
    Layer       = "bronze"
    Project     = "analytics-engineering"
  }
}

# S3 Bucket for Silver Layer
module "data_lake_silver" {
  source = "./modules/s3"
  
  bucket_name = "nova-corrente-data-lake-silver-${var.environment}"
  versioning  = true
  
  tags = {
    Environment = var.environment
    Layer       = "silver"
    Project     = "analytics-engineering"
  }
}

# S3 Bucket for Gold Layer
module "data_lake_gold" {
  source = "./modules/s3"
  
  bucket_name = "nova-corrente-data-lake-gold-${var.environment}"
  versioning  = true
  
  tags = {
    Environment = var.environment
    Layer       = "gold"
    Project     = "analytics-engineering"
  }
}

# Databricks Workspace
module "databricks_workspace" {
  source = "./modules/databricks"
  
  workspace_name    = "nova-corrente-${var.environment}"
  deployment_name    = "nova-corrente-${var.environment}"
  account_id         = var.databricks_account_id
  
  tags = {
    Environment = var.environment
    Project     = "analytics-engineering"
  }
}
```

**Exemplo: variables.tf**

```hcl
# infrastructure/terraform/variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}

variable "databricks_account_id" {
  description = "Databricks account ID"
  type        = string
  sensitive   = true
}

variable "databricks_host" {
  description = "Databricks workspace host"
  type        = string
}
```

**Checklist:**
- [ ] Terraform instalado (>= 1.5.0)
- [ ] Backend S3 configurado
- [ ] Módulos criados (S3, Databricks, Networking)
- [ ] Variáveis definidas
- [ ] Terraform init executado
- [ ] Terraform plan revisado
- [ ] Terraform apply executado (dev primeiro)
- [ ] Outputs validados

---

### 2. Estrutura do Projeto dbt

**Objetivo:** Criar estrutura completa do projeto dbt

**Arquivos a Criar:**
```
dbt/
├── dbt_project.yml
├── profiles.yml
├── packages.yml
├── README.md
├── models/
│   ├── _sources/
│   │   └── sources.yml
│   ├── staging/
│   │   ├── _staging.yml
│   │   └── stg_*.sql (placeholder files)
│   ├── intermediate/
│   │   ├── _intermediate.yml
│   │   └── int_*.sql (placeholder files)
│   └── marts/
│       ├── _marts.yml
│       ├── dim_*.sql (placeholder files)
│       └── fact_*.sql (placeholder files)
├── macros/
│   ├── reorder_point.sql
│   ├── safety_stock.sql
│   └── date_utils.sql
├── tests/
│   ├── assertions/
│   └── custom_tests/
├── snapshots/
│   └── snp_*.sql (placeholder files)
└── seeds/
    └── *.csv (reference data)
```

**Exemplo: dbt_project.yml**

```yaml
# dbt/dbt_project.yml
name: 'nova_corrente_dbt'
version: '1.0.0'
config-version: 2

profile: 'nova_corrente'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

vars:
  project_name: "Nova Corrente"
  environment: "{{ env_var('ENVIRONMENT', 'dev') }}"
  
  # Reorder Point Configuration
  default_service_level: 0.95
  default_lead_time_days: 14
  
  # Data Quality Thresholds
  mape_threshold: 15.0
  data_freshness_hours: 24

models:
  nova_corrente_dbt:
    staging:
      +materialized: view
      +schema: staging
      +tags: ["staging"]
    
    intermediate:
      +materialized: view
      +schema: intermediate
      +tags: ["intermediate"]
    
    marts:
      +materialized: table
      +schema: marts
      +tags: ["marts"]
      dim_*:
        +materialized: table
        +tags: ["dimensions"]
      fact_*:
        +materialized: table
        +tags: ["facts"]
        +cluster_by: ["date"]

tests:
  nova_corrente_dbt:
    +store_failures: true
    +limit: 100

seeds:
  nova_corrente_dbt:
    +quote_columns: true
```

**Exemplo: profiles.yml**

```yaml
# dbt/profiles.yml
nova_corrente:
  target: dev
  outputs:
    dev:
      type: databricks
      schema: nova_corrente_dev
      host: "{{ env_var('DATABRICKS_HOST') }}"
      http_path: "{{ env_var('DATABRICKS_HTTP_PATH') }}"
      token: "{{ env_var('DATABRICKS_TOKEN') }}"
      catalog: hive_metastore
      
    staging:
      type: databricks
      schema: nova_corrente_staging
      host: "{{ env_var('DATABRICKS_HOST') }}"
      http_path: "{{ env_var('DATABRICKS_HTTP_PATH') }}"
      token: "{{ env_var('DATABRICKS_TOKEN') }}"
      catalog: hive_metastore
      
    prod:
      type: databricks
      schema: nova_corrente_prod
      host: "{{ env_var('DATABRICKS_HOST') }}"
      http_path: "{{ env_var('DATABRICKS_HTTP_PATH') }}"
      token: "{{ env_var('DATABRICKS_TOKEN') }}"
      catalog: hive_metastore
```

**Exemplo: packages.yml**

```yaml
# dbt/packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: dbt-labs/codegen
    version: 0.12.1
  - package: calogica/dbt_expectations
    version: 0.10.0
  - package: dbt-labs/audit_helper
    version: 0.11.0
```

**Checklist:**
- [ ] dbt instalado (>= 1.6.0)
- [ ] Estrutura de pastas criada
- [ ] dbt_project.yml configurado
- [ ] profiles.yml configurado (dev/staging/prod)
- [ ] packages.yml definido
- [ ] dbt deps executado
- [ ] Conexão com Databricks testada
- [ ] dbt debug executado (sucesso)

---

### 3. Setup Airflow Básico

**Objetivo:** Configurar Airflow para orquestração de pipelines

**Arquivos a Criar:**
```
infrastructure/airflow/
├── docker-compose.yml
├── .env.example
├── dags/
│   ├── __init__.py
│   └── nova_corrente/
│       ├── __init__.py
│       ├── extract_dag.py
│       ├── bronze_to_silver_dag.py
│       └── dbt_dag.py
├── plugins/
│   └── __init__.py
├── config/
│   └── airflow.cfg
└── requirements.txt
```

**Exemplo: docker-compose.yml**

```yaml
# infrastructure/airflow/docker-compose.yml
version: '3.8'

x-airflow-common:
  &airflow-common
  build:
    context: .
    dockerfile: Dockerfile
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: LocalExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    AIRFLOW__API__AUTH_BACKEND: 'airflow.api.auth.backend.basic_auth'
    AIRFLOW__WEBSERVER__EXPOSE_CONFIG: 'true'
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
  user: "${AIRFLOW_UID:-50000}:0"
  depends_on:
    &airflow-common-depends-on
    postgres:
      condition: service_healthy

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

  airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler
    healthcheck:
      test: ["CMD-SHELL", 'airflow jobs check --job-type SchedulerJob --hostname "$${HOSTNAME}"']
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-init:
    <<: *airflow-common
    entrypoint: /bin/bash
    command:
      - -c
      - |
        function ver() {
          printf "%04d%04d%04d%04d" $${1//./ }
        }
        airflow_version=$$(AIRFLOW__LOGGING__LOGGING_LEVEL=INFO && airflow version)
        airflow_version_comparable=$$(ver $${airflow_version})
        min_airflow_version=2.7.0
        min_airflow_version_comparable=$$(ver $${min_airflow_version})
        if (( airflow_version_comparable < min_airflow_version_comparable )); then
          echo
          echo -e "\033[1;31mERROR!!!: Too old Airflow version $${airflow_version}!\e[0m"
          echo "The minimum Airflow version supported: $${min_airflow_version}. Only use this or higher!"
          exit 1
        fi
        if [[ -z "$${AIRFLOW_UID}" ]]; then
          echo
          echo -e "\033[1;33mWARNING!!!: AIRFLOW_UID not set!\e[0m"
          echo "If you are on Linux, you SHOULD run the following command:"
          echo "  export AIRFLOW_UID=$(id -u)"
          echo
        fi
        one_meg=1048576
        mem_available=$$(($$(getconf _PHYS_PAGES) * $$(getconf PAGE_SIZE) / one_meg))
        cpus_available=$$(grep -cE 'cpu[0-9]+' /proc/stat)
        disk_available=$$(df / | tail -1 | awk '{print $$4}')
        warning_resources="false"
        if (( mem_available < 4000 )) ; then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough memory available for Docker.\e[0m"
          echo "At least 4GB of memory required. You have $$(numfmt --to iec $$((mem_available * one_meg)))"
          echo
          warning_resources="true"
        fi
        if (( cpus_available < 2 )); then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough CPUS available for Docker.\e[0m"
          echo "At least 2 CPUs recommended. You have $${cpus_available}"
          echo
          warning_resources="true"
        fi
        if (( disk_available < one_meg * 10 )); then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough Disk Space available for Docker.\e[0m"
          echo "At least 10 GBs recommended. You have $$(numfmt --to iec $$((disk_available * 1024 )))"
          echo
          warning_resources="true"
        fi
        if [[ $${warning_resources} == "true" ]]; then
          echo
          echo -e "\033[1;33mWARNING!!!: You have not enough resources to run Airflow!\e[0m"
          echo "Please follow the instructions to increase amount of resources available:"
          echo "   https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#before-you-begin"
          exit 1
        fi
        mkdir -p /sources/logs /sources/dags /sources/plugins
        chown -R "$${AIRFLOW_UID}:0" /sources/{logs,dags,plugins}
        exec /entrypoint airflow version
    environment:
      <<: *airflow-common-env
      _AIRFLOW_DB_MIGRATE: 'true'
      _AIRFLOW_WWW_USER_CREATE: 'true'
      _AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow}
      _AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow}
    user: "0:0"
    volumes:
      - ${AIRFLOW_PROJ_DIR:-.}:/sources

volumes:
  postgres-db-volume:
```

**Exemplo: DAG Básico**

```python
# infrastructure/airflow/dags/nova_corrente/extract_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'nova-corrente',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'nova_corrente_extract',
    default_args=default_args,
    description='Extract data from sources to Bronze layer',
    schedule_interval='@daily',
    start_date=datetime(2025, 11, 1),
    catchup=False,
    tags=['nova-corrente', 'extract', 'bronze'],
)

extract_erp = BashOperator(
    task_id='extract_erp',
    bash_command='python scripts/extract_erp.py',
    dag=dag,
)

extract_weather = BashOperator(
    task_id='extract_weather',
    bash_command='python scripts/extract_weather.py',
    dag=dag,
)

extract_anatel = BashOperator(
    task_id='extract_anatel',
    bash_command='python scripts/extract_anatel.py',
    dag=dag,
)

[extract_erp, extract_weather, extract_anatel]
```

**Checklist:**
- [ ] Docker instalado
- [ ] docker-compose.yml configurado
- [ ] Airflow UI acessível (localhost:8080)
- [ ] DAGs básicos criados
- [ ] Conexões configuradas
- [ ] Variáveis de ambiente definidas
- [ ] Teste de execução bem-sucedido

---

### 4. Bronze Layer Setup

**Objetivo:** Configurar ingestão inicial de dados brutos

**Estrutura de Dados:**
```
s3://nova-corrente-data-lake-bronze/
├── erp/
│   ├── items/
│   │   └── year=2025/month=11/day=01/
│   │       └── items_2025-11-01.parquet
│   ├── towers/
│   └── inventory/
├── external/
│   ├── weather/
│   │   └── year=2025/month=11/day=01/
│   │       └── weather_2025-11-01.json
│   ├── anatel/
│   └── economic/
└── raw/
    └── (dados não processados)
```

**Script de Ingestão Exemplo:**

```python
# scripts/ingest_to_bronze.py
import boto3
import pandas as pd
from datetime import datetime
from pathlib import Path
import json

s3_client = boto3.client('s3')
BRONZE_BUCKET = 'nova-corrente-data-lake-bronze'

def ingest_to_bronze(source: str, data: pd.DataFrame, partition_date: datetime = None):
    """
    Ingest data to Bronze layer in S3
    
    Args:
        source: Source name (e.g., 'erp', 'weather')
        data: DataFrame to ingest
        partition_date: Partition date (defaults to today)
    """
    if partition_date is None:
        partition_date = datetime.now()
    
    # Build S3 key with partitioning
    year = partition_date.year
    month = f"{partition_date.month:02d}"
    day = f"{partition_date.day:02d}"
    
    s3_key = f"{source}/year={year}/month={month}/day={day}/data_{partition_date.strftime('%Y-%m-%d')}.parquet"
    
    # Convert to Parquet
    parquet_buffer = data.to_parquet(index=False)
    
    # Upload to S3
    s3_client.put_object(
        Bucket=BRONZE_BUCKET,
        Key=s3_key,
        Body=parquet_buffer,
        ContentType='application/parquet'
    )
    
    print(f"✅ Ingested {len(data)} rows to s3://{BRONZE_BUCKET}/{s3_key}")
    
    return s3_key
```

**Checklist:**
- [ ] Buckets S3 criados (bronze/silver/gold)
- [ ] Particionamento definido (year/month/day)
- [ ] Scripts de ingestão criados
- [ ] Formato Parquet configurado
- [ ] Teste de ingestão bem-sucedido
- [ ] Validação de dados ingeridos

---

### 5. Documentação Inicial

**Arquivos a Criar:**
```
docs/proj/roadmaps/phase_0/
├── README.md
├── SETUP_GUIDE.md
├── TROUBLESHOOTING.md
└── CHECKLIST.md
```

**Checklist Final da Fase 0:**

- [ ] ✅ Terraform configurado e aplicado
- [ ] ✅ Buckets S3 criados (bronze/silver/gold)
- [ ] ✅ Databricks workspace configurado
- [ ] ✅ dbt project criado e testado
- [ ] ✅ Airflow rodando localmente
- [ ] ✅ DAGs básicos funcionando
- [ ] ✅ Scripts de ingestão criados
- [ ] ✅ Documentação completa
- [ ] ✅ Equipe treinada no básico
- [ ] ✅ Pronto para Fase 1

---

## 📊 MÉTRICAS DE SUCESSO FASE 0

**Técnicas:**
- ✅ Infraestrutura 100% provisionada via Terraform
- ✅ dbt conecta ao Databricks (100% sucesso)
- ✅ Airflow UI acessível e DAGs executando
- ✅ Ingestão inicial de dados funcionando

**Processo:**
- ✅ Documentação completa e acessível
- ✅ Equipe treinada no básico
- ✅ Pipeline de desenvolvimento configurado

---

## 🚀 PRÓXIMOS PASSOS

Após conclusão da Fase 0:
1. Revisar todos entregáveis
2. Validar com stakeholders
3. Preparar para Fase 1 (Data Foundation)
4. Alocar recursos (1-2 engenheiros)

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia Detalhado Fase 0

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

