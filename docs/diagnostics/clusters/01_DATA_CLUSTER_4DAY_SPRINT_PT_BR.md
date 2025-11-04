****# 📊 DATA CLUSTER - 4-DAY SPRINT PLAN
## Nova Corrente - Analytics Data Foundation

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** 🚀 Execution-Ready  
**Sprint:** 4 Days (D0-D4)  
**Cluster Lead:** Data Engineer  
**Team Size:** 1-2 Engineers

---

## 📋 QUICK ORIENTATION

**Goal:** Create a reproducible, queryable analytics store (time series focused) that supports the dashboard and API reads with simple schema and ingestion — **deploy in 4 days**.

**Key Constraint:** No heavy cloud/Databricks/ML production runs this sprint. Use local or lightweight managed infra (MinIO or S3 if account exists). Keep formats Parquet. Use Delta only as optional upgrade if trivial to add.

**Reference Documents:**
- [Diagnóstico Completo](../COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md) - Gap analysis completo
- [Lista de Tarefas Críticas](../CRITICAL_TASKS_PRIORITY_LIST_PT_BR.md) - TASK 1.1-1.4, 2.1-2.3
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy document

---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Reference:** [Global Constraints Document](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical results** are ingested as static Parquet files.

**Data Cluster Specific Rules:**
- ✅ Only ingest and transform **pre-aggregated or model-output data**, not raw training features
- ✅ Store ML results (predictions, forecasts, metrics) as static Parquet tables (`gold` layer)
- ✅ Label each ML-generated file with version metadata: `model_version`, `generated_at`, `source`, `dataset_id`
- ❌ **NO feature engineering** in ingestion scripts
- ❌ **NO ML processing** in transformation scripts
- ❌ **NO ML dependencies** in deployment containers

**Validation:**
- [ ] Check ingestion scripts have NO ML dependencies
- [ ] Check transformation scripts have NO ML processing
- [ ] Verify all ML results include required metadata columns
- [ ] Verify schema registry documents ML result metadata

---

## 🎯 KEY CONSTRAINTS & ASSUMPTIONS

### Technical Constraints
- ✅ **Storage:** MinIO (Docker) or S3 (if AWS account exists)
- ✅ **Format:** Parquet (snappy compression)
- ✅ **Schema:** Minimal star schema (only columns needed by dashboards)
- ✅ **Processing:** Lightweight (Pandas/Spark job, no full dbt)
- ❌ **Deferred:** Delta Lake, full dbt, Databricks, Great Expectations
- ❌ **NO ML dependencies:** No PyTorch, TensorFlow, scikit-learn, MLflow

### Business Constraints
- **Data Sources:** Existing CSVs + External APIs (time series only)
- **ML Processing:** Local only, results exported to `gold` as facts
- **Analytics Focus:** Forecast accuracy, inventory levels, demand trends
- **Scale:** Small-medium datasets (< 10GB total)

### Scope Reduction Triggers
- If external APIs unavailable → Use existing CSVs only
- If MinIO provisioning fails → Use PostgreSQL for small datasets
- If Parquet processing stalls → Use CSV + PostgreSQL (worse scale, faster setup)

---

## 📅 DELIVERABLES (DAY-BY-DAY)

### **D0 (TODAY): Freeze Inputs & Sample Data** ⏱️ 2-4 hours
**Owner:** Data Lead  
**Deliverables:**
- [ ] Freeze list of external APIs and CSVs to use
- [ ] Sample extract for each source (max 1-2 days history for speed)
- [ ] Export sample CSVs to `data/raw/`
- [ ] Document schema for each source
- [ ] Create `data/schema_registry.json` with column definitions
- [ ] **Verify NO ML dependencies** in sample data extraction scripts

**Acceptance Criteria:**
- ✅ All sample files in `data/raw/` with documented schema
- ✅ Schema registry JSON validates
- ✅ NO ML dependencies in extraction scripts

**Output Files:**
- `data/raw/samples/` - Sample data files
- `data/schema_registry.json` - Schema definitions

---

### **D1: Storage + Ingestion** ⏱️ 6-8 hours
**Owner:** 1-2 Data Engineers  
**Deliverables:**

#### Storage Setup
- [ ] Provision MinIO (docker-compose) or configure S3 buckets
- [ ] Create buckets: `nova-bronze` (raw), `nova-silver` (cleaned), `nova-gold` (analytics)
- [ ] Test upload/download via Python client
- [ ] Configure IAM roles/policies (if S3)

#### Ingestion Scripts
- [ ] Implement extractor scripts (Python) for:
  - [ ] External API time series (Weather, Economic, 5G) - **READ ONLY**
  - [ ] Existing CSV files (Nova Corrente data)
  - [ ] **Precomputed ML results** (forecasts, metrics) - **READ ONLY from external ML environment**
- [ ] Write Parquet to bronze partitioned by `date` (year/month/day)
- [ ] **Validate ML results schema:** Must include `model_version`, `generated_at`, `source`, `dataset_id` columns
- [ ] Keep schema explicit (validate column types)
- [ ] Add logging and error handling
- [ ] **Verify NO ML dependencies** in extractor scripts

**Acceptance Criteria:**
- ✅ MinIO/S3 buckets accessible
- ✅ Extractor scripts write Parquet to bronze
- ✅ Partitioning works (year=YYYY/month=MM/day=DD)
- ✅ Sample data ingestion successful
- ✅ ML results include required metadata columns
- ✅ NO ML dependencies in extractor scripts

**Output Files:**
- `backend/pipelines/extractors/` - Extractor scripts
- `backend/pipelines/extractors/api_extractor.py`
- `backend/pipelines/extractors/csv_extractor.py`
- `backend/pipelines/extractors/ml_results_extractor.py` - Precomputed ML results
- `docker-compose.yml` (MinIO service if using)

**Technical Specs:**
```python
# Example ML results schema validation
required_columns = ['model_version', 'generated_at', 'source', 'dataset_id']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"ML results must include {col} column")
```

---

### **D2: Lightweight Transformations** ⏱️ 6-8 hours
**Owner:** 1 Data Engineer  
**Deliverables:**

#### Transformation Scripts
- [ ] Implement SQL-like transformation scripts (Pandas/Spark job):
  - [ ] `stg_items.sql` or `stg_items.py` - Clean items data
  - [ ] `stg_forecasts.sql` or `stg_forecasts.py` - Clean forecasts data (from precomputed ML results)
  - [ ] `stg_inventory.sql` or `stg_inventory.py` - Clean inventory data
- [ ] Materialize outputs to silver Parquet
- [ ] Add basic validation (null checks, type casts, duplicates removal)
- [ ] **Preserve ML metadata:** Keep `model_version`, `generated_at`, `source`, `dataset_id` columns
- [ ] **Verify NO ML processing** in transformation scripts

**If dbt available (optional):**
- [ ] Install `dbt-core` + `dbt-spark` (or `dbt-duckdb`)
- [ ] Create `dbt_project.yml` with basic config
- [ ] Create `models/staging/` with SQL models
- [ ] Test `dbt run --models staging.*`
- [ ] **Verify NO ML dependencies** in dbt project

**Acceptance Criteria:**
- ✅ Silver Parquet files created from bronze
- ✅ Data cleaned (no nulls in key columns, types correct)
- ✅ Duplicates removed
- ✅ Schema validated
- ✅ ML metadata preserved
- ✅ NO ML processing in transformation scripts

**Output Files:**
- `backend/pipelines/transformations/` - Transformation scripts
- `backend/pipelines/transformations/stg_items.py`
- `backend/pipelines/transformations/stg_forecasts.py`
- `backend/pipelines/transformations/stg_inventory.py`
- OR `dbt/models/staging/` if using dbt

**Technical Specs:**
```python
# Example transformation - preserve ML metadata
def transform_forecasts(bronze_path, silver_path):
    df = pd.read_parquet(bronze_path)
    # Clean: trim, lowercase, type cast
    df['forecast'] = pd.to_numeric(df['forecast'], errors='coerce')
    df['actual'] = pd.to_numeric(df['actual'], errors='coerce')
    # Preserve ML metadata
    ml_metadata = ['model_version', 'generated_at', 'source', 'dataset_id']
    for col in ml_metadata:
        if col not in df.columns:
            raise ValueError(f"ML metadata column {col} missing")
    # Write to silver
    df.to_parquet(silver_path, partition_cols=['date'])
```

---

### **D3: Gold Models (Star Schema)** ⏱️ 6-8 hours
**Owner:** 1 Data Engineer  
**Deliverables:**

#### Gold Layer Creation
- [ ] Create minimal star schema:
  - [ ] `dim_item.sql` or `.py` - Dimensions: `(id, sku, name, category)`
  - [ ] `dim_time.sql` or `.py` - Dimensions: `(date, year, month, day_of_week)`
  - [ ] `fact_forecast.sql` or `.py` - Facts: `(date, item_id, forecast, actual, source, model_version, generated_at, dataset_id)` - **PRECOMPUTED FROM ML**
- [ ] Only columns needed by dashboards (see Backend section for requirements)
- [ ] Precompute aggregates required by dashboards:
  - [ ] 7-day rolling averages (from precomputed forecasts)
  - [ ] 30-day totals (from precomputed forecasts)
  - [ ] TTL: cache daily (refresh schedule)
- [ ] **Preserve ML metadata** in fact tables

**Acceptance Criteria:**
- ✅ Gold Parquet files created (dim_item, dim_time, fact_forecast)
- ✅ Aggregates precomputed
- ✅ Schema matches dashboard requirements
- ✅ ML metadata included in fact_forecast
- ✅ Query test: `SELECT * FROM fact_forecast WHERE date >= '2025-10-01'` returns < 2s

**Output Files:**
- `backend/pipelines/models/` - Gold models
- `backend/pipelines/models/dim_item.py`
- `backend/pipelines/models/dim_time.py`
- `backend/pipelines/models/fact_forecast.py`
- OR `dbt/models/marts/` if using dbt

**Technical Specs:**
```python
# Example fact table with ML metadata
fact_forecast = {
    'date': 'date',
    'item_id': 'string',
    'forecast': 'float',
    'actual': 'float',
    'source': 'string',  # 'prophet', 'arima', 'lstm', 'ensemble'
    'model_version': 'string',  # ML metadata
    'generated_at': 'timestamp',  # ML metadata
    'dataset_id': 'string',  # ML metadata
    'mape': 'float',
    'created_at': 'timestamp'
}
```

---

### **D4: Test & Deliver** ⏱️ 4-6 hours
**Owner:** 1 Data Engineer  
**Deliverables:**

#### End-to-End Testing
- [ ] Run complete pipeline: pull → bronze → silver → gold
- [ ] Validate Parquet queries via SQL (DuckDB or Spark SQL)
- [ ] Provide example SQL queries for backend endpoints:
  - [ ] `get_timeseries(item_id, start, end)` query
  - [ ] `get_aggregate(item_ids, window)` query
  - [ ] `get_inventory(item_id, date)` query
- [ ] Document data locations and access patterns
- [ ] Create `README_DATA.md` with usage examples
- [ ] **Verify NO ML dependencies** in entire pipeline

**Acceptance Criteria:**
- ✅ End-to-end pipeline runs without error
- ✅ All queries return expected results
- ✅ Documentation complete
- ✅ Backend can read Parquet files successfully
- ✅ NO ML dependencies in pipeline

**Output Files:**
- `docs/data/README_DATA.md` - Data documentation
- `docs/data/example_queries.sql` - SQL examples
- `data/gold/` - Final gold layer Parquet files

---

## 🔧 SUB-TASKS & TECHNICAL SPECS

### Storage Specifications

#### MinIO Setup (Docker)
```yaml
# docker-compose.yml excerpt
services:
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
```

#### S3 Setup (AWS)
```python
# Requirements
- AWS account
- IAM user with S3 access
- Buckets: nova-corrente-bronze, nova-corrente-silver, nova-corrente-gold
- Lifecycle policy: 90 days retention for bronze
```

#### Partitioning Strategy
```
Bronze: year=YYYY/month=MM/day=DD
Silver: date=YYYY-MM-DD (minimal partitioning)
Gold: date=YYYY-MM-DD (for query performance)
```

#### File Format
- **Format:** Parquet (snappy compression)
- **Schema:** Explicit column types (date/datetime, int/float, string/varchar)
- **Validation:** Schema registry JSON

---

### Schema Registry

**File:** `data/schema_registry.json`

```json
{
  "bronze": {
    "erp_items": {
      "item_id": "string",
      "item_name": "string",
      "cost": "float",
      "date": "date"
    },
    "forecasts": {
      "item_id": "string",
      "date": "date",
      "forecast": "float",
      "actual": "float",
      "source": "string",
      "model_version": "string",
      "generated_at": "timestamp",
      "dataset_id": "string"
    }
  },
  "silver": {
    "stg_items": {
      "item_id": "string (PK)",
      "item_name": "string (trimmed, lowercase)",
      "cost": "float",
      "date": "date"
    },
    "stg_forecasts": {
      "item_id": "string",
      "date": "date",
      "forecast": "float",
      "actual": "float",
      "source": "string",
      "model_version": "string",
      "generated_at": "timestamp",
      "dataset_id": "string"
    }
  },
  "gold": {
    "dim_item": {
      "item_id": "string (PK)",
      "sku": "string",
      "name": "string",
      "category": "string"
    },
    "fact_forecast": {
      "date": "date",
      "item_id": "string (FK)",
      "forecast": "float",
      "actual": "float",
      "source": "string",
      "model_version": "string",
      "generated_at": "timestamp",
      "dataset_id": "string",
      "mape": "float"
    }
  }
}
```

---

### Validation Specifications

#### Minimal Validation (No Great Expectations)
```python
# Basic validation checks
1. Not null: item_id, date, forecast, actual
2. Type validation: float columns are numeric
3. Range validation: forecast >= 0, actual >= 0
4. Uniqueness: (item_id, date, source) combination unique
5. Row count: Sample row counts match expected
6. ML metadata: model_version, generated_at, source, dataset_id present
```

#### Error Handling
- Log errors to `logs/data_ingestion.log`
- Retry failed API calls (3 attempts)
- Skip invalid rows (log and continue)
- Alert on critical failures (email/Slack)

---

## ✅ SUCCESS CRITERIA (ACCEPTANCE TESTS)

### Functional Requirements
- [ ] ✅ End-to-end job runs without error for sample day set
- [ ] ✅ `fact_forecast` query of last 30 days aggregates returns < 2s on local/dev machine
- [ ] ✅ All dashboard endpoints (see Backend section) return required fields (no missing keys)
- [ ] ✅ Data quality: < 1% null values in key columns
- [ ] ✅ Schema validation: All columns match schema registry

### Performance Requirements
- [ ] ✅ Bronze ingestion: < 5 min for 1 day of data
- [ ] ✅ Silver transformation: < 10 min for 1 day of data
- [ ] ✅ Gold aggregation: < 15 min for 1 day of data
- [ ] ✅ Query performance: < 2s for 30-day time series

### ML Ops Validation (MANDATORY)
- [ ] ✅ No ML dependencies in ingestion scripts
- [ ] ✅ No ML dependencies in transformation scripts
- [ ] ✅ Only precomputed ML results ingested (no ML processing)
- [ ] ✅ ML results include metadata (`model_version`, `generated_at`, `source`, `dataset_id`)
- [ ] ✅ Deployment can run offline (no ML API calls)

### Documentation Requirements
- [ ] ✅ Schema registry documented
- [ ] ✅ Data locations documented
- [ ] ✅ Example queries provided
- [ ] ✅ Access patterns documented

---

## 🚨 SCOPE-REDUCTION OPTIONS (IF BLOCKERS)

### Option 1: Absolute Minimal (No External APIs)
**Trigger:** External APIs unavailable or rate-limited

**Changes:**
- Use existing CSVs only (from `data/processed/`)
- Map CSVs to schema directly
- Skip real-time ingestion
- Update documentation to reflect static data

**Impact:** ⚠️ No real-time updates, but functional for demo

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 2: Minimal Analytics (No Dimensions)
**Trigger:** Time pressure or complex joins failing

**Changes:**
- Materialize only `fact_forecast` (no dims)
- Compute labels on backend (join in API layer)
- Simpler schema, faster to build

**Impact:** ⚠️ More complex queries in backend, but faster to deploy

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 3: No Parquet (PostgreSQL Only)
**Trigger:** MinIO/Parquet provisioning stalls

**Changes:**
- Use PostgreSQL for small datasets (< 1GB)
- Store data in PostgreSQL tables
- Backend queries PostgreSQL directly
- Worse scale but faster to stand up

**Impact:** ⚠️ Doesn't scale well, but functional for MVP

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

## 🔗 KEY RECOMMENDATIONS

### Technical Decisions
1. **Use DuckDB for Parquet queries** - Fastest path to SQL over Parquet without Spark
2. **Partition by date** - Enables efficient time series queries
3. **Precompute aggregates** - Reduces query time in dashboard
4. **Schema registry JSON** - Single source of truth for schema
5. **Preserve ML metadata** - Traceability for precomputed results

### Follow-Up Questions (Answer Quickly)
1. **Storage:** Do you have AWS account and prefer S3, or default to MinIO docker-compose?
2. **Transformation:** Prefer Python scripts or dbt SQL? (dbt recommended if time allows)
3. **Data Sources:** Which external APIs are critical? (Weather, Economic, 5G - prioritize)
4. **Schema:** What exact columns are needed by dashboard? (See Backend section)
5. **ML Results:** Where will precomputed ML results be stored? (shared storage path)

---

## 📚 REFERENCE LINKS

- [Diagnóstico Completo](../COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md#storage-layer) - Storage gaps analysis
- [Tarefas Críticas](../CRITICAL_TASKS_PRIORITY_LIST_PT_BR.md#task-11-setup-cloud-storage-s3minio) - TASK 1.1-1.4
- [Backend Cluster](./02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - API requirements
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy
- [Roadmap Analytics](../../proj/roadmaps/ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md#arquitetura-dados) - Full architecture vision

---

## 📝 NEXT STEPS

1. **Assign Cluster Lead:** Data Engineer
2. **Assign Team:** 1-2 Engineers
3. **Kickoff Meeting:** Review this document, assign tasks
4. **Daily Standup:** 9 AM - Review progress, blockers
5. **End of Day:** Acceptance test for each day's deliverables

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Execution-Ready - 4-Day Sprint Plan

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

