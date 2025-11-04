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
  - ❌ PyTorch (`torch`, `torchvision`, `torchaudio`)
  - ❌ TensorFlow (`tensorflow`, `tensorflow-gpu`, `keras`)
  - ❌ scikit-learn (`scikit-learn`, `sklearn`)
  - ❌ MLflow (`mlflow`)
  - ❌ XGBoost (`xgboost`)z
  - ❌ LightGBM (`lightgbm`)
  - ❌ Prophet (`prophet`)
  - ❌ pmdarima (`pmdarima`)
  - ❌ Statsmodels (for ML, not for basic stats)
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
- [ ] Check `requirements_deployment.txt` has NO ML dependencies
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
- [ ] ✅ All `requirements_deployment.txt` files reviewed (NO ML dependencies)
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

