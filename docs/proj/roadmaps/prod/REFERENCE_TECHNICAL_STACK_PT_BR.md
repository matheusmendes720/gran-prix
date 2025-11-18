# 📚 REFERÊNCIA TÉCNICA - STACK COMPLETO
## Nova Corrente - Analytics Engineering

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Referência Completa

---

## 📋 ÍNDICE

1. [Cloud Infrastructure](#cloud)
2. [Data Storage](#storage)
3. [Transformation Tools](#transformation)
4. [Orchestration](#orchestration)
5. [ML Tools](#ml)
6. [BI Tools](#bi)
7. [Governance](#governance)

---

<a name="cloud"></a>

## 1. ☁️ CLOUD INFRASTRUCTURE

### AWS Services

**S3 (Storage):**
- **Uso:** Bronze/Silver/Gold layers
- **Formato:** Parquet/Delta
- **Custo:** ~$0.023/GB storage
- **Docs:** https://docs.aws.amazon.com/s3/

**Databricks (Compute):**
- **Uso:** Spark processing, SQL queries
- **Plano:** Standard ou Premium
- **Custo:** ~$0.40/DBU (Standard)
- **Docs:** https://docs.databricks.com/

**Alternativas:**
- **GCP:** Cloud Storage + BigQuery
- **Azure:** ADLS + Synapse

---

<a name="storage"></a>

## 2. 🗄️ DATA STORAGE

### Delta Lake

**Características:**
- ACID transactions
- Schema evolution
- Time travel
- Upserts/deletes

**Version:**
- 2.4.0 (latest stable)

**Documentação:**
- https://docs.delta.io/

**Configuração:**
```python
spark.conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
spark.conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
```

---

### Unity Catalog

**Características:**
- Centralized metadata
- Access control
- Data lineage
- Data sharing

**Version:**
- 2.4.0+

**Documentação:**
- https://docs.databricks.com/data-governance/unity-catalog/

---

<a name="transformation"></a>

## 3. 🔄 TRANSFORMATION TOOLS

### dbt (data build tool)

**Version:**
- 1.7.0+ (latest)

**Installation:**
```bash
pip install dbt-databricks
```

**Packages:**
```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.0
```

**Documentação:**
- https://docs.getdbt.com/

**CLI Commands:**
```bash
dbt deps          # Install packages
dbt debug         # Test connection
dbt run           # Run models
dbt test          # Run tests
dbt docs generate # Generate docs
dbt docs serve    # Serve docs locally
```

---

### Spark

**Version:**
- 3.5.0 (latest)

**Language:** Python, Scala, SQL

**Documentação:**
- https://spark.apache.org/docs/

**Performance:**
- Cluster: 2-8 workers
- Memory: 16-64 GB per worker
- CPUs: 4-16 cores per worker

---

<a name="orchestration"></a>

## 4. 🎛️ ORCHESTRATION

### Apache Airflow

**Version:**
- 2.7.0+ (latest)

**Installation:**
```bash
# Docker Compose
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml'
```

**Documentação:**
- https://airflow.apache.org/docs/

**Providers:**
```bash
pip install apache-airflow-providers-databricks
pip install apache-airflow-providers-aws
```

---

### Prefect (Alternative)

**Version:**
- 2.14.0+

**Installation:**
```bash
pip install prefect
pip install prefect-databricks
```

**Documentação:**
- https://docs.prefect.io/

---

<a name="ml"></a>

## 5. 🤖 ML TOOLS

### MLflow

**Version:**
- 2.9.0+ (latest)

**Installation:**
```bash
pip install mlflow
pip install mlflow[databricks]
```

**Documentação:**
- https://mlflow.org/docs/

**Features:**
- Experiment tracking
- Model registry
- Model serving
- Model versioning

---

### Feature Stores

**Feast:**
- Version: 0.37.0+
- Docs: https://docs.feast.dev/

**Tecton:**
- Managed service
- Docs: https://docs.tecton.ai/

---

<a name="bi"></a>

## 6. 📊 BI TOOLS

### Metabase

**Version:**
- Latest (0.49.0+)

**Installation:**
```bash
docker pull metabase/metabase:latest
```

**Documentação:**
- https://www.metabase.com/docs/

**Features:**
- Self-service BI
- Query builder
- Embed analytics
- Scheduled reports

---

### Apache Superset

**Version:**
- 3.0.0+ (latest)

**Installation:**
```bash
docker pull apache/superset:latest
```

**Documentação:**
- https://superset.apache.org/docs/

**Features:**
- Advanced dashboards
- SQL Lab
- Alerts
- Custom visualizations

---

<a name="governance"></a>

## 7. 🛡️ GOVERNANCE

### Great Expectations

**Version:**
- 0.18.0+

**Installation:**
```bash
pip install great_expectations[spark]
```

**Documentação:**
- https://docs.greatexpectations.io/

**Features:**
- Data validation
- Data profiling
- Data docs
- Alerting

---

### DataHub

**Version:**
- 0.12.0+ (latest)

**Installation:**
```bash
docker-compose -f quickstart.yml pull
docker-compose -f quickstart.yml up
```

**Documentação:**
- https://datahubproject.io/docs/

**Features:**
- Data catalog
- Data lineage
- Metadata management
- Access control

---

## 🔗 LINKS ÚTEIS

### Documentação Oficial

**Core Tools:**
- dbt: https://docs.getdbt.com
- Airflow: https://airflow.apache.org/docs
- Databricks: https://docs.databricks.com
- MLflow: https://mlflow.org/docs

**BI Tools:**
- Metabase: https://www.metabase.com/docs
- Superset: https://superset.apache.org/docs

**Governance:**
- Great Expectations: https://docs.greatexpectations.io
- DataHub: https://datahubproject.io/docs

### Comunidades

**dbt:**
- Slack: https://getdbt.com/community/
- Discourse: https://discourse.getdbt.com

**Airflow:**
- Slack: https://apache-airflow.slack.com
- GitHub: https://github.com/apache/airflow

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Referência Técnica Completa

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

