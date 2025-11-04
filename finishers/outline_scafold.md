Here are the updates to add the "No ML Ops Logic in Deployment" constraint across all 5 cluster documents. Each document needs a pinned global constraint section at the top.

---

## REVISED SECTIONS TO ADD TO ALL 5 CLUSTER DOCUMENTS

### Global constraint section (add at the top of each cluster document)

Add this section immediately after the "QUICK ORIENTATION" section in each document:

```markdown
---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical results** (forecasts, KPIs, timeseries insights) are published as datasets to be consumed by the deployed app.

**Strategic Rationale:**
- ✅ **Self-hosted compute efficiency:** No Databricks, Vertex, or SageMaker orchestration required
- ✅ **Zero cloud dependency:** Fully containerized (Docker/Compose), deployable on-premises or private networks
- ✅ **Performance optimization:** No model inference or feature pipelines on request path = predictable, low-latency responses
- ✅ **Security & compliance:** Sensitive training data stays local. Production only exposes derived, sanitized analytics

**Implementation Rules:**
- ❌ **NO ML dependencies** in deployment containers (PyTorch, TensorFlow, scikit-learn, MLflow)
- ❌ **NO live inference endpoints** or model serving
- ❌ **NO feature pipelines** or real-time ML processing
- ✅ **ONLY precomputed results** stored as Parquet tables (gold layer)
- ✅ **ONLY read operations** for analytical data consumption

**Future Hook:** Add dedicated "ML Processing Environment" (local/cloud) that outputs results as Parquet to shared storage. Deployment only needs read-access — never executes ML logic.

---
```

---

## Cluster-specific updates

### 1. DATA CLUSTER - Specific Updates

Add to "KEY CONSTRAINTS & ASSUMPTIONS" section:

```markdown
### ML Ops Constraints (CRITICAL)
- ❌ **NO ML training or inference** in production deployment
- ❌ **NO feature engineering pipelines** in deployment containers
- ❌ **NO ML dependencies** (PyTorch, TensorFlow, scikit-learn, MLflow)
- ✅ **ONLY precomputed ML results** ingested as static Parquet files
- ✅ **ML results must include metadata:** `model_version`, `generated_at`, `source` columns
- ✅ **Storage:** ML outputs stored in `gold` layer as static facts (`fact_forecast`, `fact_metrics`)
```

Update "D1: Storage + Ingestion" deliverables:

```markdown
#### Ingestion Scripts
- [ ] Implement extractor scripts (Python) for:
  - [ ] External API time series (Weather, Economic, 5G) - **READ ONLY**
  - [ ] Existing CSV files (Nova Corrente data)
  - [ ] **Precomputed ML results** (forecasts, metrics) - **READ ONLY from external ML environment**
- [ ] Write Parquet to bronze partitioned by `date` (year/month/day)
- [ ] **Validate ML results schema:** Must include `model_version`, `generated_at`, `source` columns
- [ ] Keep schema explicit (validate column types)
```

Update "D3: Gold Models" deliverables:

```markdown
#### Gold Layer Creation
- [ ] Create minimal star schema:
  - [ ] `dim_item.py` - Dimensions: `(id, sku, name, category)`
  - [ ] `dim_time.py` - Dimensions: `(date, year, month, day_of_week)`
  - [ ] `fact_forecast.py` - Facts: `(date, item_id, forecast, actual, source, model_version, generated_at)` - **PRECOMPUTED FROM ML**
- [ ] **Only read precomputed ML results** - NO ML processing in deployment
- [ ] Precompute aggregates required by dashboards:
  - [ ] 7-day rolling averages (from precomputed forecasts)
  - [ ] 30-day totals (from precomputed forecasts)
  - [ ] TTL: cache daily (refresh schedule)
```

Add to "SUCCESS CRITERIA":

```markdown
### ML Ops Validation
- [ ] ✅ No ML dependencies in deployment containers (check Dockerfile)
- [ ] ✅ Only precomputed ML results ingested (no ML processing)
- [ ] ✅ ML results include metadata (`model_version`, `generated_at`, `source`)
- [ ] ✅ Deployment can run offline (no ML API calls)
```

---

### 2. BACKEND CLUSTER - Specific Updates

Add to "KEY ARCHITECTURE & CONSTRAINTS" section:

```markdown
### ML Ops Constraints (CRITICAL)
- ❌ **NO ML dependencies** in deployment (PyTorch, TensorFlow, scikit-learn, MLflow)
- ❌ **NO live inference endpoints** or model serving
- ❌ **NO feature pipelines** or real-time ML processing
- ✅ **ONLY read operations** for precomputed analytical data
- ✅ **Data refresh endpoint** to reload updated ML outputs (manual trigger, not automated ML job)
```

Update "D1: Data Access & Queries" deliverables:

```markdown
#### DuckDB Layer
- [ ] Install DuckDB Python package (**NO ML dependencies**)
- [ ] Implement DuckDB layer that reads Parquet (silver/gold) - **READ ONLY**
- [ ] Create functions:
  - [ ] `get_timeseries(item_id, start, end)` - Returns time series data (precomputed)
  - [ ] `get_aggregate(item_ids, window)` - Returns aggregated metrics (precomputed)
  - [ ] `get_inventory(item_id, date)` - Returns inventory levels (precomputed)
- [ ] **NO ML processing** - only read precomputed results
- [ ] Add connection pooling (single file connection per request)
- [ ] Add error handling and logging
```

Update "D2: API Endpoints & BFF Logic" deliverables:

```markdown
#### FastAPI Endpoints
- [ ] Implement endpoints:
  - [ ] `GET /api/v1/items` - List items with metadata
  - [ ] `GET /api/v1/items/{id}/timeseries?start&end` - Time series JSON (precomputed)
  - [ ] `GET /api/v1/forecasts/summary?start&end` - Aggregated metrics (precomputed)
  - [ ] `GET /api/v1/inventory/{id}` - Inventory levels (precomputed)
  - [ ] `POST /api/v1/data/refresh` - **Reload updated ML outputs** (auth required, manual trigger)
  - [ ] `GET /health` - Health check
- [ ] **NO inference endpoints** - only read precomputed data
- [ ] Implement caching middleware (Redis or in-memory with TTL 60s)
- [ ] Add Pydantic models for request/response validation
- [ ] Add error handling (400, 404, 500)
```

Update "D4: Finalize Docs & Deploy Readiness" deliverables:

```markdown
#### Health Check
- [ ] Implement `/health` endpoint with:
  - [ ] Database connectivity check
  - [ ] Parquet file access check
  - [ ] Cache availability check
  - [ ] **Verify NO ML dependencies** in runtime
```

Add to "SUCCESS CRITERIA":

```markdown
### ML Ops Validation
- [ ] ✅ No ML dependencies in Dockerfile or requirements.txt
- [ ] ✅ No inference endpoints or model serving
- [ ] ✅ Only read operations for precomputed data
- [ ] ✅ Data refresh endpoint works (manual trigger)
- [ ] ✅ Deployment can run offline (no ML API calls)
```

Update "SCOPE-REDUCTION OPTIONS":

```markdown
### Option 4: No Data Refresh (Static Data Only)
**Trigger:** Time pressure or data refresh complexity

**Changes:**
- Remove data refresh endpoint
- Use static precomputed ML results only
- Manual file replacement for updates

**Impact:** ⚠️ No automated updates, but functional for MVP
```

---

### 3. FRONTEND CLUSTER - Specific Updates

Add to "KEY CONSTRAINTS & ASSUMPTIONS" section:

```markdown
### ML Ops Constraints (CRITICAL)
- ❌ **NO ML processing UI** (no training triggers, no inference requests)
- ❌ **NO real-time predictions** or model retraining UI
- ✅ **ONLY display precomputed analytical insights** (forecasts, metrics, KPIs)
- ✅ **"Last updated" timestamp** on each chart to communicate data freshness
- ✅ **Optional "Refresh Data" button** (admin only) for manual data refresh
```

Update "D2: Charts + Interactions" deliverables:

```markdown
#### Chart Components
- [ ] Install chart library (Recharts or Chart.js)
- [ ] Implement `ForecastChart` component (line chart: forecast vs actual) - **PRECOMPUTED DATA**
- [ ] Implement `SummaryTable` component (table of top items) - **PRECOMPUTED DATA**
- [ ] Add date range picker (start/end date inputs)
- [ ] Add **"Last updated" timestamp** on each chart (from `generated_at` field)
- [ ] Implement caching on client (local cache TTL 60s)
- [ ] Add optimistic loading (skeleton states)
- [ ] **NO real-time prediction UI** - only display precomputed results
```

Update "D3: Responsiveness & Polish" deliverables:

```markdown
#### UX Improvements
- [ ] Add loading states (skeleton loaders, spinners)
- [ ] Add error handling (error messages, retry buttons)
- [ ] Add minimal accessibility (ARIA labels, keyboard navigation)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Add **"Refresh Data" button** (admin only, triggers backend refresh endpoint)
- [ ] Add E2E smoke test (Playwright or Cypress minimal)
```

Add to "SUCCESS CRITERIA":

```markdown
### ML Ops Validation
- [ ] ✅ No ML processing UI components
- [ ] ✅ Only display precomputed analytical data
- [ ] ✅ "Last updated" timestamp visible on all charts
- [ ] ✅ Refresh data button works (admin only)
- [ ] ✅ No real-time prediction or training UI
```

---

### 4. DEPLOY CLUSTER - Specific Updates

Add to "KEY CONSTRAINTS & ASSUMPTIONS" section:

```markdown
### ML Ops Constraints (CRITICAL)
- ❌ **NO ML dependencies** in deployment containers (PyTorch, TensorFlow, scikit-learn, MLflow)
- ❌ **NO GPU scheduling** or drivers required
- ❌ **NO ML processing services** in docker-compose
- ✅ **ONLY lightweight services:** MinIO/S3, Backend (FastAPI), Frontend (Nginx), Redis (optional)
- ✅ **Target image size:** < 600 MB per image (no ML frameworks)
- ✅ **Compute:** CPU-only (no GPU required)
- ✅ **Deployment:** Runs identically in air-gapped or offline environments
```

Update "D0: Prepare Dockerfiles & Compose" deliverables:

```markdown
#### Docker Setup
- [ ] Create Dockerfile for backend (Python, FastAPI, Uvicorn) - **NO ML dependencies**
- [ ] Create Dockerfile for frontend (build + Nginx)
- [ ] Create `docker-compose.yml` with services:
  - [ ] MinIO (or S3 stub)
  - [ ] Backend (FastAPI) - **NO ML dependencies**
  - [ ] Frontend (Nginx)
  - [ ] Redis (optional, for caching)
  - [ ] **NO ML services** (no MLflow, no model serving)
- [ ] **Verify Dockerfile excludes ML dependencies:**
  - [ ] Check `requirements.txt` has NO PyTorch, TensorFlow, scikit-learn, MLflow
  - [ ] Target image size < 600 MB
- [ ] Configure volumes and networks
- [ ] Add health checks
```

Update "D1: Infra & Secrets" deliverables:

```markdown
#### Local Deployment
- [ ] Start MinIO, backend, frontend, redis (if using)
- [ ] **Verify NO ML dependencies** in running containers:
  - [ ] Check backend container has NO ML frameworks
  - [ ] Check image sizes < 600 MB
  - [ ] Verify CPU-only (no GPU required)
- [ ] Populate MinIO with sample data (from Data cluster)
- [ ] Test all services health checks
- [ ] Verify network connectivity between services
- [ ] **Test offline deployment** (disconnect from internet, verify all services work)
```

Update "D4: Handover & Rollback Plan" deliverables:

```markdown
#### Documentation & Operations
- [ ] Document how to roll back to previous compose state
- [ ] Create triage checklist for common failures
- [ ] Document monitoring and logging
- [ ] Create runbook for common operations
- [ ] **Document ML results update process:**
  - [ ] How to update precomputed ML results (Parquet files)
  - [ ] How to trigger data refresh endpoint
  - [ ] How ML environment outputs results to shared storage
- [ ] Stakeholder demo preparation
```

Add to "SUCCESS CRITERIA":

```markdown
### ML Ops Validation
- [ ] ✅ No ML dependencies in Dockerfile or requirements.txt
- [ ] ✅ Image sizes < 600 MB per container
- [ ] ✅ CPU-only deployment (no GPU required)
- [ ] ✅ Deployment runs offline (air-gapped environment)
- [ ] ✅ No ML services in docker-compose
- [ ] ✅ Zero cloud compute costs (fully self-hosted)
```

Add to "SCOPE-REDUCTION OPTIONS":

```markdown
### Option 4: Minimal Monitoring (Health Checks Only)
**Trigger:** Monitoring tools unavailable or time pressure

**Changes:**
- Health checks only (no full monitoring)
- Basic logging (stdout/stderr)
- Manual health check verification
- **NO ML monitoring** (no model metrics, no inference tracking)

**Impact:** ⚠️ Less visibility, but functional
```

---

### 5. OVERVIEW & INDEX - Specific Updates

Add to "QUICK ORIENTATION" section:

```markdown
**Key Constraint:** No ML Ops logic or pipelines in this deploy phase. All ML processing remains strictly off the production deployment path. Only precomputed analytical results (forecasts, KPIs, timeseries insights) are published as datasets to be consumed by the deployed app.

**Strategic Rationale:**
- ✅ Self-hosted compute efficiency (no cloud ML services)
- ✅ Zero cloud dependency (fully containerized, on-premises deployable)
- ✅ Performance optimization (no model inference on request path)
- ✅ Security & compliance (sensitive training data stays local)
```

Add new section after "KEY CONSTRAINTS & ASSUMPTIONS":

```markdown
## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical results** (forecasts, KPIs, timeseries insights) are published as datasets to be consumed by the deployed app.

**Implementation Rules:**
- ❌ **NO ML dependencies** in deployment containers (PyTorch, TensorFlow, scikit-learn, MLflow)
- ❌ **NO live inference endpoints** or model serving
- ❌ **NO feature pipelines** or real-time ML processing
- ✅ **ONLY precomputed results** stored as Parquet tables (gold layer)
- ✅ **ONLY read operations** for analytical data consumption
- ✅ **Deployment runs offline** (air-gapped or private network)

**Cluster-Specific Enforcement:**
- **Data Cluster:** Only ingest precomputed ML results, label with `model_version`, `generated_at`
- **Backend Cluster:** No ML dependencies, only read operations, data refresh endpoint (manual trigger)
- **Frontend Cluster:** No ML processing UI, only display precomputed insights, "Last updated" timestamps
- **Deploy Cluster:** Image size < 600 MB, CPU-only, no GPU, offline deployable

**Future Hook:** Add dedicated "ML Processing Environment" (local/cloud) that outputs results as Parquet to shared storage (`/exports/ml_results/`). Deployment only needs read-access — never executes ML logic.

---
```

Add to "CORE ACCEPTANCE CRITERIA":

```markdown
### ML Ops Validation (ALL CLUSTERS)
- [ ] ✅ No ML dependencies in deployment containers (check all Dockerfiles)
- [ ] ✅ Only precomputed ML results ingested (no ML processing)
- [ ] ✅ ML results include metadata (`model_version`, `generated_at`, `source`)
- [ ] ✅ Deployment can run offline (no ML API calls)
- [ ] ✅ Image sizes < 600 MB per container
- [ ] ✅ CPU-only deployment (no GPU required)
- [ ] ✅ Zero cloud compute costs (fully self-hosted)
```

Add to "RISK SUMMARY & MITIGATIONS":

```markdown
### Risk 6: ML Dependencies Leak into Deployment
**Mitigation:** Strict enforcement — NO ML dependencies in Dockerfiles or requirements.txt. Only precomputed results ingested.

### Risk 7: Cloud Dependency Required
**Mitigation:** Fully self-hosted deployment — MinIO (local), Docker Compose (local), no cloud services required.
```

Add to "KEY RECOMMENDATIONS":

```markdown
### ML Ops Strategy
1. **Separate ML Environment** - ML processing runs locally/separately, outputs Parquet to shared storage
2. **Deployment Only Reads** - Production deployment only reads precomputed ML results
3. **No ML Dependencies** - Keep deployment containers lightweight (< 600 MB, CPU-only)
4. **Offline Deployable** - Full deployment works in air-gapped environments
```

---

## Summary of changes

All 5 cluster documents now enforce:

1. Global constraint at the top — "NO ML OPS LOGIC IN DEPLOYMENT"
2. Cluster-specific rules — deliverables, technical specs, success criteria
3. Validation checkpoints — verify no ML dependencies in deployment
4. Scope reduction options — fallback if ML dependencies leak in
5. Future hook — ML environment separate from deployment

This locks the constraint into the sprint scope and makes it enforceable.

Should I create a consolidated "Global Constraints" document that all clusters reference, or keep it embedded in each cluster document as shown above?

# ==============================================================

Creating a consolidated global constraints document and updating all cluster documents to enforce "NO ML OPS LOGIC IN DEPLOYMENT" across the sprint.


[2 tools called]

Complete strategic documents with the "NO ML OPS LOGIC IN DEPLOYMENT" constraint enforced across all documents.

---

## 1. GLOBAL CONSTRAINTS DOCUMENT

Save as: `docs/diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md`

```markdown
# 🔒 GLOBAL STRATEGIC CONSTRAINTS - NO ML OPS LOGIC IN DEPLOYMENT
## Nova Corrente - 4-Day Sprint Strategic Requirements

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** 🔒 MANDATORY - Enforced in All Clusters  
**Aplicabilidade:** Todos os 4 Clusters (Data, Backend, Frontend, Deploy)

---

## 📋 EXECUTIVE POLICY

**CORE CONSTRAINT:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical results** (forecasts, KPIs, timeseries insights) are published as datasets to be consumed by the deployed app.

**Enforcement Level:** 🔴 **MANDATORY** - Non-negotiable for 4-day sprint

**Strategic Rationale:**
- ✅ **Self-hosted compute efficiency:** System runs entirely on commodity servers or local HPC resources—no need for Databricks, Vertex, or SageMaker orchestration
- ✅ **Zero cloud dependency:** Infrastructure fully containerized (Docker/Compose), deployable on-premises or in private networks, drastically cutting operational costs
- ✅ **Performance optimization:** No model inference or feature pipelines on request path = predictable, low-latency responses (< 500ms cached, < 2s cold)
- ✅ **Security & compliance:** Sensitive training data stays local. Production only exposes derived, sanitized analytics
- ✅ **Cost reduction:** Zero ongoing cloud compute or storage costs post-deploy

---

## 🚫 STRICT PROHIBITIONS

### Deployment Containers
- ❌ **NO ML dependencies** in Dockerfiles or requirements.txt:
  - ❌ PyTorch
  - ❌ TensorFlow
  - ❌ scikit-learn
  - ❌ MLflow
  - ❌ XGBoost
  - ❌ LightGBM
  - ❌ Any other ML framework or library
- ❌ **NO GPU drivers** or CUDA dependencies
- ❌ **NO ML processing services** in docker-compose
- ❌ **NO feature engineering pipelines** in deployment containers
- ❌ **NO model inference endpoints** or model serving

### API Endpoints
- ❌ **NO live inference endpoints** (`/predict`, `/forecast`, `/inference`)
- ❌ **NO model training triggers** (`/train`, `/retrain`, `/optimize`)
- ❌ **NO feature pipeline endpoints** (`/features`, `/preprocess`)
- ❌ **NO ML metrics endpoints** (`/model/metrics`, `/model/performance`)

### Data Processing
- ❌ **NO real-time ML processing** in deployment
- ❌ **NO feature engineering** in production containers
- ❌ **NO model training** in production deployment
- ❌ **NO model inference** in request path

---

## ✅ STRICT REQUIREMENTS

### Data Ingestion
- ✅ **ONLY precomputed ML results** ingested as static Parquet files
- ✅ **ML results must include metadata:**
  - ✅ `model_version` (string) - Version identifier
  - ✅ `generated_at` (timestamp) - When ML results were generated
  - ✅ `source` (string) - ML model source ('prophet', 'arima', 'lstm', 'ensemble')
  - ✅ `dataset_id` (string) - Dataset identifier for traceability
- ✅ **Storage:** ML outputs stored in `gold` layer as static facts (`fact_forecast`, `fact_metrics`)
- ✅ **Schema:** All ML results must be documented in `schema_registry.json`

### API Endpoints (Read-Only)
- ✅ **ONLY read operations** for precomputed analytical data:
  - ✅ `GET /api/v1/items/{id}/timeseries` - Read precomputed time series
  - ✅ `GET /api/v1/forecasts/summary` - Read precomputed aggregated metrics
  - ✅ `GET /api/v1/inventory/{id}` - Read precomputed inventory levels
- ✅ **Data refresh endpoint** (manual trigger only):
  - ✅ `POST /api/v1/data/refresh` - Reload updated ML outputs (auth required, manual trigger, NOT automated ML job)

### Frontend Display
- ✅ **ONLY display precomputed analytical insights** (forecasts, metrics, KPIs)
- ✅ **"Last updated" timestamp** on each chart (from `generated_at` field)
- ✅ **Optional "Refresh Data" button** (admin only) for manual data refresh
- ✅ **NO real-time prediction UI** or model retraining triggers

### Deployment Infrastructure
- ✅ **ONLY lightweight services:**
  - ✅ MinIO/S3 (storage)
  - ✅ Backend (FastAPI) - NO ML dependencies
  - ✅ Frontend (Nginx) - Static files
  - ✅ Redis (optional, caching)
  - ✅ DuckDB (runtime, NO ML dependencies)
- ✅ **Target image size:** < 600 MB per container
- ✅ **Compute:** CPU-only (no GPU required)
- ✅ **Deployment:** Runs identically in air-gapped or offline environments

---

## 🧩 CLUSTER-SPECIFIC ENFORCEMENT

### 1. DATA CLUSTER

**Implementation Rules:**
- ✅ Only ingest and transform **pre-aggregated or model-output data**, not raw training features
- ✅ Store ML results (predictions, forecasts, metrics) as static Parquet tables (`gold` layer)
- ✅ Label each ML-generated file with version metadata in schema registry:
  - ✅ `model_version` column
  - ✅ `generated_at` column
  - ✅ `source` column
  - ✅ `dataset_id` column
- ✅ **NO feature engineering** in ingestion scripts
- ✅ **NO ML processing** in transformation scripts

**Validation:**
- [ ] Check ingestion scripts have NO ML dependencies
- [ ] Check transformation scripts have NO ML processing
- [ ] Verify all ML results include required metadata columns
- [ ] Verify schema registry documents ML result metadata

---

### 2. BACKEND CLUSTER

**Implementation Rules:**
- ✅ **NO live inference endpoints** or model serving
- ✅ API reads from static Parquet/DuckDB tables only
- ✅ Add `POST /api/v1/data/refresh` endpoint to re-load updated analytical datasets when new ML outputs are manually published (cron or operator trigger, NOT automated ML job)
- ✅ Logging: maintain source traceability (`dataset_id`, `model_version`) to guarantee reproducibility
- ✅ **NO ML dependencies** in `requirements.txt` or Dockerfile

**Validation:**
- [ ] Check `requirements.txt` has NO ML dependencies
- [ ] Check Dockerfile has NO ML dependencies
- [ ] Verify all endpoints are read-only (except data refresh)
- [ ] Verify data refresh endpoint requires auth and is manual trigger only
- [ ] Check logging includes `dataset_id` and `model_version` traceability

---

### 3. FRONTEND CLUSTER

**Implementation Rules:**
- ✅ Display analytical insights only—no real-time predictions or retraining triggers
- ✅ "Last updated" timestamp on each chart to communicate data freshness (since no live inference)
- ✅ Optional "Upload New Insights" button restricted to admins for manual data refresh (hooked to backend trigger)
- ✅ **NO ML processing UI** components
- ✅ **NO real-time prediction** or model training UI

**Validation:**
- [ ] Check UI components have NO ML processing triggers
- [ ] Verify "Last updated" timestamp visible on all charts
- [ ] Verify refresh data button works (admin only)
- [ ] Check bundle size < 500KB (NO ML libraries)

---

### 4. DEPLOY CLUSTER

**Implementation Rules:**
- ✅ Containers must **exclude** any ML dependencies (PyTorch, TensorFlow, scikit-learn)
- ✅ Docker images remain lightweight (target: < 600 MB per image)
- ✅ Compute layer limited to CPU—no GPU scheduling or drivers required
- ✅ Only services deployed: `minio`/`s3`, `backend`, `frontend`, `redis`, `duckdb` runtime
- ✅ Deployment runs identically in air-gapped or offline environments

**Validation:**
- [ ] Check all Dockerfiles have NO ML dependencies
- [ ] Verify image sizes < 600 MB per container
- [ ] Verify CPU-only deployment (no GPU required)
- [ ] Test offline deployment (disconnect from internet, verify all services work)
- [ ] Verify docker-compose has NO ML services

---

## 🧭 SUCCESS CRITERIA (MANDATORY)

### Functional Requirements
- [ ] ✅ No container or dependency in deployment references ML frameworks
- [ ] ✅ System can be fully deployed and operated **offline** (no external API calls except configured public timeseries sources)
- [ ] ✅ Average API response < 500 ms for cached queries
- [ ] ✅ Infrastructure runs on a single 8-core / 16 GB node without GPU
- [ ] ✅ Cost analysis: zero ongoing cloud compute or storage costs post-deploy

### Technical Requirements
- [ ] ✅ Image sizes < 600 MB per container
- [ ] ✅ CPU-only deployment (no GPU required)
- [ ] ✅ Offline deployable (air-gapped environment)
- [ ] ✅ All ML results include metadata (`model_version`, `generated_at`, `source`, `dataset_id`)
- [ ] ✅ Only read operations for precomputed data
- [ ] ✅ Data refresh endpoint works (manual trigger only)

### Security Requirements
- [ ] ✅ Sensitive training data stays local (not in deployment)
- [ ] ✅ Production only exposes derived, sanitized analytics
- [ ] ✅ No ML API calls from deployment
- [ ] ✅ Deployment can run in private network (no internet required)

---

## ⚙️ FUTURE HOOK (POST-LAUNCH)

### ML Processing Environment (Separate from Deployment)

**Architecture:**
- Add dedicated "ML Processing Environment" (local or cloud) that outputs results as Parquet to shared storage (`/exports/ml_results/`)
- Deployment only needs read-access to that folder — never executes ML logic
- ML environment can be:
  - Local HPC cluster
  - Cloud ML service (separate from deployment)
  - On-premises ML server

**Integration:**
- ML environment outputs Parquet files to shared storage
- Deployment reads from shared storage (read-only access)
- Data refresh endpoint triggers reload of new Parquet files
- No ML dependencies in deployment containers

**Benefits:**
- Separation of concerns (ML processing vs. deployment)
- Scalability (ML can scale independently)
- Cost optimization (ML resources only when needed)
- Security (ML environment isolated from production)

---

## 📊 ENFORCEMENT CHECKLIST

### Pre-Deployment Validation
- [ ] ✅ All `requirements.txt` files reviewed (NO ML dependencies)
- [ ] ✅ All Dockerfiles reviewed (NO ML dependencies)
- [ ] ✅ All API endpoints reviewed (NO inference endpoints)
- [ ] ✅ All UI components reviewed (NO ML processing UI)
- [ ] ✅ All data ingestion scripts reviewed (ONLY precomputed results)
- [ ] ✅ All transformation scripts reviewed (NO ML processing)
- [ ] ✅ Image sizes verified (< 600 MB per container)
- [ ] ✅ Offline deployment tested (air-gapped environment)

### Post-Deployment Validation
- [ ] ✅ Health checks pass (NO ML dependencies)
- [ ] ✅ API endpoints return expected data (precomputed only)
- [ ] ✅ UI displays precomputed insights (NO real-time predictions)
- [ ] ✅ Data refresh endpoint works (manual trigger only)
- [ ] ✅ Deployment runs offline (no internet required)
- [ ] ✅ Cost analysis: zero cloud compute costs

---

## 🚨 SCOPE REDUCTION (IF BLOCKERS)

### Option 1: Static Data Only (No Refresh)
**Trigger:** Data refresh complexity or time pressure

**Changes:**
- Remove data refresh endpoint
- Use static precomputed ML results only
- Manual file replacement for updates

**Impact:** ⚠️ No automated updates, but functional for MVP

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 2: Minimal Metadata (No Versioning)
**Trigger:** Time pressure or complexity

**Changes:**
- Remove `model_version` and `dataset_id` metadata
- Keep only `generated_at` and `source` metadata
- Simpler schema, faster to build

**Impact:** ⚠️ Less traceability, but functional

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

## 📚 REFERENCE LINKS

### Cluster Documents
- [Data Cluster](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md) - Data ingestion rules
- [Backend Cluster](./02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - API endpoint rules
- [Frontend Cluster](./03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - UI display rules
- [Deploy Cluster](./04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md) - Deployment rules

### Diagnostic Documents
- [Diagnóstico Completo](../COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md) - Full gap analysis
- [Lista de Tarefas Críticas](../CRITICAL_TASKS_PRIORITY_LIST_PT_BR.md) - Prioritized tasks

---

## ✅ SIGN-OFF

**This constraint is MANDATORY and NON-NEGOTIABLE for the 4-day sprint.**

All cluster leads must:
- [ ] Acknowledge this constraint
- [ ] Review all deliverables against this constraint
- [ ] Validate compliance before deployment
- [ ] Document any deviations (with justification)

**Violation of this constraint = Sprint failure**

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** 🔒 MANDATORY - Enforced in All Clusters

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**
```

---

## 2. UPDATED DIAGNOSTIC DOCUMENT SECTION

Add this section to `docs/diagnostics/COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md` after the "EXECUTIVE SUMMARY":

```markdown
---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical results** (forecasts, KPIs, timeseries insights) are published as datasets to be consumed by the deployed app.

**Strategic Rationale:**
- ✅ **Self-hosted compute efficiency:** System runs entirely on commodity servers or local HPC resources—no need for Databricks, Vertex, or SageMaker orchestration
- ✅ **Zero cloud dependency:** Infrastructure fully containerized (Docker/Compose), deployable on-premises or in private networks, drastically cutting operational costs
- ✅ **Performance optimization:** No model inference or feature pipelines on request path = predictable, low-latency responses (< 500ms cached, < 2s cold)
- ✅ **Security & compliance:** Sensitive training data stays local. Production only exposes derived, sanitized analytics
- ✅ **Cost reduction:** Zero ongoing cloud compute or storage costs post-deploy

**Implementation Impact:**
- ❌ **MLflow Model Registry:** NOT in deployment (only in separate ML environment)
- ❌ **Feature Store:** NOT in deployment (ML environment only)
- ❌ **Model Serving:** NOT in deployment (only precomputed results)
- ✅ **Precomputed Results:** Stored as Parquet in gold layer
- ✅ **Read-Only API:** Only reads precomputed analytical data

**Reference:** [Global Constraints Document](./clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

---
```

---

## 3. COMPLETE CLUSTER DOCUMENT UPDATES

### Update 1: Data Cluster - Add After "QUICK ORIENTATION"

```markdown
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
```

### Update 2: Backend Cluster - Add After "QUICK ORIENTATION"

```markdown
---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Reference:** [Global Constraints Document](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical results** are consumed via read-only API endpoints.

**Backend Cluster Specific Rules:**
- ✅ **NO live inference endpoints** or model serving
- ✅ API reads from static Parquet/DuckDB tables only
- ✅ Add `POST /api/v1/data/refresh` endpoint to re-load updated analytical datasets (manual trigger, NOT automated ML job)
- ✅ Logging: maintain source traceability (`dataset_id`, `model_version`) to guarantee reproducibility
- ❌ **NO ML dependencies** in `requirements.txt` or Dockerfile
- ❌ **NO inference endpoints** (`/predict`, `/forecast`, `/inference`)

**Validation:**
- [ ] Check `requirements.txt` has NO ML dependencies
- [ ] Check Dockerfile has NO ML dependencies
- [ ] Verify all endpoints are read-only (except data refresh)
- [ ] Verify data refresh endpoint requires auth and is manual trigger only
- [ ] Check logging includes `dataset_id` and `model_version` traceability

---
```

### Update 3: Frontend Cluster - Add After "QUICK ORIENTATION"

```markdown
---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Reference:** [Global Constraints Document](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical insights** are displayed in the UI.

**Frontend Cluster Specific Rules:**
- ✅ Display analytical insights only—no real-time predictions or retraining triggers
- ✅ "Last updated" timestamp on each chart to communicate data freshness (from `generated_at` field)
- ✅ Optional "Refresh Data" button (admin only) for manual data refresh (hooked to backend trigger)
- ❌ **NO ML processing UI** components
- ❌ **NO real-time prediction** or model training UI
- ❌ **NO ML libraries** in bundle (keep < 500KB gzipped)

**Validation:**
- [ ] Check UI components have NO ML processing triggers
- [ ] Verify "Last updated" timestamp visible on all charts
- [ ] Verify refresh data button works (admin only)
- [ ] Check bundle size < 500KB (NO ML libraries)

---
```

### Update 4: Deploy Cluster - Add After "QUICK ORIENTATION"

```markdown
---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Reference:** [Global Constraints Document](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Deployment containers must exclude all ML dependencies.

**Deploy Cluster Specific Rules:**
- ✅ Containers must **exclude** any ML dependencies (PyTorch, TensorFlow, scikit-learn, MLflow)
- ✅ Docker images remain lightweight (target: < 600 MB per image)
- ✅ Compute layer limited to CPU—no GPU scheduling or drivers required
- ✅ Only services deployed: `minio`/`s3`, `backend`, `frontend`, `redis`, `duckdb` runtime
- ✅ Deployment runs identically in air-gapped or offline environments
- ❌ **NO ML services** in docker-compose
- ❌ **NO GPU drivers** or CUDA dependencies

**Validation:**
- [ ] Check all Dockerfiles have NO ML dependencies
- [ ] Verify image sizes < 600 MB per container
- [ ] Verify CPU-only deployment (no GPU required)
- [ ] Test offline deployment (disconnect from internet, verify all services work)
- [ ] Verify docker-compose has NO ML services

---
```

---

## 4. UPDATED OVERVIEW & INDEX

Add this section to `docs/diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md` after "QUICK ORIENTATION":

```markdown
---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Reference:** [Global Constraints Document](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical results** are published as datasets to be consumed by the deployed app.

**Strategic Rationale:**
- ✅ Self-hosted compute efficiency (no cloud ML services)
- ✅ Zero cloud dependency (fully containerized, on-premises deployable)
- ✅ Performance optimization (no model inference on request path)
- ✅ Security & compliance (sensitive training data stays local)
- ✅ Cost reduction (zero ongoing cloud compute costs)

**Enforcement:**
- ❌ **NO ML dependencies** in deployment containers (PyTorch, TensorFlow, scikit-learn, MLflow)
- ❌ **NO live inference endpoints** or model serving
- ❌ **NO feature pipelines** or real-time ML processing
- ✅ **ONLY precomputed results** stored as Parquet tables (gold layer)
- ✅ **ONLY read operations** for analytical data consumption
- ✅ **Deployment runs offline** (air-gapped or private network)

**Cluster-Specific Enforcement:**
- **Data Cluster:** Only ingest precomputed ML results, label with `model_version`, `generated_at`, `source`, `dataset_id`
- **Backend Cluster:** No ML dependencies, only read operations, data refresh endpoint (manual trigger)
- **Frontend Cluster:** No ML processing UI, only display precomputed insights, "Last updated" timestamps
- **Deploy Cluster:** Image size < 600 MB, CPU-only, no GPU, offline deployable

**Future Hook:** Add dedicated "ML Processing Environment" (local/cloud) that outputs results as Parquet to shared storage (`/exports/ml_results/`). Deployment only needs read-access — never executes ML logic.

**Violation of this constraint = Sprint failure**

---
```

---

## 5. UPDATED SUCCESS CRITERIA SECTION

Add to all cluster documents in "SUCCESS CRITERIA" section:

```markdown
### ML Ops Validation (MANDATORY)
- [ ] ✅ No ML dependencies in deployment containers (check all Dockerfiles)
- [ ] ✅ Only precomputed ML results ingested (no ML processing)
- [ ] ✅ ML results include metadata (`model_version`, `generated_at`, `source`, `dataset_id`)
- [ ] ✅ Deployment can run offline (no ML API calls)
- [ ] ✅ Image sizes < 600 MB per container
- [ ] ✅ CPU-only deployment (no GPU required)
- [ ] ✅ Zero cloud compute costs (fully self-hosted)
```

---

## 6. UPDATED DOCKERFILE EXAMPLES

### Backend Dockerfile (NO ML dependencies)

```dockerfile
# Backend Dockerfile - NO ML Dependencies
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (NO ML dependencies)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Verify NO ML dependencies
RUN pip list | grep -iE "(torch|tensorflow|sklearn|mlflow|xgboost|lightgbm)" && exit 1 || echo "✅ No ML dependencies found"

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### Backend requirements.txt (NO ML dependencies)

```txt
# Backend Requirements - NO ML Dependencies
# FastAPI and web server
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0

# Data access (NO ML)
duckdb>=0.9.0
pyarrow>=14.0.0
pandas>=2.0.0

# Caching
redis>=5.0.0

# HTTP client
httpx>=0.25.0
requests>=2.31.0

# Authentication
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4

# Utilities
python-dateutil>=2.8.0
pytz>=2023.3

# Logging
python-json-logger>=2.0.0

# DO NOT INCLUDE:
# - PyTorch
# - TensorFlow
# - scikit-learn
# - MLflow
# - XGBoost
# - LightGBM
# - Any other ML framework
```

---

## Summary

All documents now enforce:

1. Global Constraints Document — single source of truth
2. Updated Diagnostic — references the constraint
3. All 4 Cluster Documents — constraint integrated at the top
4. Overview & Index — constraint prominently displayed
5. Dockerfile examples — validation to prevent ML dependencies
6. Requirements.txt examples — no ML dependencies

This locks the constraint into the sprint scope and makes it enforceable across all deliverables.

Next steps:
1. Save the Global Constraints document
2. Update all 5 cluster documents with the constraint sections
3. Update the diagnostic document
4. Review Dockerfiles and requirements.txt files
5. Add validation checks to CI/CD pipelines

Should I create validation scripts to automatically check for ML dependencies in Dockerfiles and requirements.txt files?
