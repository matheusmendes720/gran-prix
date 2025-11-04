# 🎯 OVERVIEW & INDEX - 4-DAY SPRINT PLAN
## Nova Corrente - Complete Execution Guide

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** 🚀 Execution-Ready  
**Sprint:** 4 Days (D0-D4)  
**Total Teams:** 4 Clusters (Data, Backend, Frontend, Deploy)

---

## 📋 QUICK ORIENTATION

**Goal:** Deploy a minimal, functional analytics dashboard with time series data, forecast insights, and supply chain inventory management in **4 days**.

**Key Constraint:** No heavy ML processing in production. ML runs locally, results exported to analytics layer. Focus on BI dashboard and supply chain management.

**Scope Reduction:** This plan deliberately reduces cyclomatic complexity by using lightweight alternatives (Parquet+DuckDB instead of Delta+Spark, MinIO instead of S3, simple orchestrator instead of Airflow).

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

## 🔗 CLUSTER DOCUMENTS

### 1. DATA CLUSTER
**Document:** [01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md)  
**Lead:** Data Engineer  
**Team:** 1-2 Engineers  
**Focus:** Storage (MinIO/S3), Ingestion, Transformations (Parquet), Gold Layer (Star Schema)

**Key Deliverables:**
- D0: Freeze inputs & sample data
- D1: Storage + Ingestion (MinIO/S3, extractors)
- D2: Lightweight Transformations (Pandas/Spark, silver layer)
- D3: Gold Models (Star Schema: dim_item, dim_time, fact_forecast)
- D4: Test & Deliver (end-to-end pipeline, documentation)

**ML Constraint:** Only ingest precomputed ML results, NO ML processing in ingestion/transformation scripts

---

### 2. BACKEND CLUSTER
**Document:** [02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md](./02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md)  
**Lead:** Backend Lead  
**Team:** 1-2 Engineers  
**Focus:** API (FastAPI), Data Access (DuckDB + Parquet), Caching, Auth

**Key Deliverables:**
- D0: Freeze endpoints & contract (OpenAPI spec)
- D1: Data Access & Queries (DuckDB layer)
- D2: API Endpoints & BFF Logic (FastAPI routes)
- D3: Auth, Tests & Integration (JWT/API key, pytest)
- D4: Finalize Docs & Deploy Readiness (documentation, health check)

**ML Constraint:** NO ML dependencies in requirements, NO inference endpoints, only read operations

---

### 3. FRONTEND CLUSTER
**Document:** [03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md](./03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md)  
**Lead:** Frontend Lead  
**Team:** 1-2 Engineers  
**Focus:** Dashboard (React + Vite), Charts (Recharts), Interactions, Responsiveness

**Key Deliverables:**
- D0: Freeze UX & Component List (mockups, component list)
- D1: Project Scaffold + Components (React + Vite, Tailwind CSS)
- D2: Charts + Interactions (Recharts, date range picker, caching)
- D3: Responsiveness & Polish (loading states, error handling, accessibility)
- D4: Bundle & Integration Test (production build, deployment)

**ML Constraint:** NO ML processing UI, only display precomputed insights, "Last updated" timestamps

---

### 4. DEPLOY CLUSTER
**Document:** [04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md](./04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md)  
**Lead:** DevOps/Backend Lead  
**Team:** 1 Engineer  
**Focus:** Docker Compose, CI/CD, Health Checks, Secrets Management

**Key Deliverables:**
- D0: Prepare Dockerfiles & Compose (Dockerfiles, docker-compose.yml)
- D1: Infra & Secrets (local deployment, environment variables)
- D2: CI Pipeline + Automated Builds (GitHub Actions)
- D3: Smoke Tests + Domain (E2E tests, Cloudflare Tunnel/ngrok)
- D4: Handover & Rollback Plan (documentation, runbook)

**ML Constraint:** NO ML dependencies in Dockerfiles, image size < 600 MB, CPU-only, offline deployable

---

## 📅 SPRINT MILESTONE MAP (4 DAYS)

### **D0 (TODAY): Freeze & Planning** ⏱️ 4-6 hours
**All Clusters:**
- [ ] **Data:** Freeze inputs & sample data
- [ ] **Backend:** Freeze endpoints & contract
- [ ] **Frontend:** Freeze UX & component list
- [ ] **Deploy:** Prepare Dockerfiles & compose

**Checkpoint:** All teams aligned, contracts defined, ready to build

---

### **D1: Storage + Data Access** ⏱️ 6-8 hours
**Parallel Work:**
- [ ] **Data:** Storage + Ingestion (MinIO/S3, extractors)
- [ ] **Backend:** Data Access & Queries (DuckDB layer)
- [ ] **Frontend:** Project Scaffold + Components
- [ ] **Deploy:** Infra & Secrets (local deployment)

**Checkpoint:** Data flowing into storage, backend can query, frontend scaffolded

---

### **D2: API + Frontend Minimal** ⏱️ 6-8 hours
**Parallel Work:**
- [ ] **Data:** Lightweight Transformations (silver layer)
- [ ] **Backend:** API Endpoints & BFF Logic (FastAPI routes)
- [ ] **Frontend:** Charts + Interactions (Recharts, date picker)
- [ ] **Deploy:** CI Pipeline + Automated Builds

**Checkpoint:** API endpoints working, frontend charts rendering, CI pipeline running

---

### **D3: Integration** ⏱️ 6-8 hours
**Parallel Work:**
- [ ] **Data:** Gold Models (Star Schema)
- [ ] **Backend:** Auth, Tests & Integration (JWT/API key, pytest)
- [ ] **Frontend:** Responsiveness & Polish (loading states, error handling)
- [ ] **Deploy:** Smoke Tests + Domain (E2E tests, public access)

**Checkpoint:** End-to-end integration working, tests passing, ready for deployment

---

### **D4: Deploy & Demo** ⏱️ 4-6 hours
**Final Work:**
- [ ] **Data:** Test & Deliver (end-to-end pipeline, documentation)
- [ ] **Backend:** Finalize Docs & Deploy Readiness (documentation, health check)
- [ ] **Frontend:** Bundle & Integration Test (production build)
- [ ] **Deploy:** Handover & Rollback Plan (documentation, runbook)

**Checkpoint:** All services deployed, stakeholder demo ready, documentation complete

---

## ✅ CORE ACCEPTANCE CRITERIA (ALL CLUSTERS)

### End-to-End Path
- [ ] ✅ Data ingestion → bronze → silver → gold → Parquet queries validated
- [ ] ✅ Backend API endpoints return expected JSON
- [ ] ✅ Frontend dashboard renders with correct data
- [ ] ✅ All services deployed and accessible

### Performance Requirements
- [ ] ✅ Data queries: < 2s for 30-day time series
- [ ] ✅ API endpoints: < 500ms cached, < 2s cold
- [ ] ✅ Frontend load: < 2.5s on reasonable dev VM
- [ ] ✅ Services start: < 2 minutes

### Quality Requirements
- [ ] ✅ Backend: 80%+ unit test coverage
- [ ] ✅ Frontend: E2E smoke tests passing
- [ ] ✅ Data: < 1% null values in key columns
- [ ] ✅ Deploy: Health checks passing

### ML Ops Validation (MANDATORY)
- [ ] ✅ No ML dependencies in deployment containers (check all Dockerfiles)
- [ ] ✅ Only precomputed ML results ingested (no ML processing)
- [ ] ✅ ML results include metadata (`model_version`, `generated_at`, `source`, `dataset_id`)
- [ ] ✅ Deployment can run offline (no ML API calls)
- [ ] ✅ Image sizes < 600 MB per container
- [ ] ✅ CPU-only deployment (no GPU required)
- [ ] ✅ Zero cloud compute costs (fully self-hosted)

---

## 🚨 RISK SUMMARY & MITIGATIONS

### Risk 1: Delta/Databricks Not Available
**Mitigation:** Use Parquet + DuckDB (already planned)

### Risk 2: External API Rate Limits
**Mitigation:** Use cached historical sample and poll once

### Risk 3: Too Many Features
**Mitigation:** Apply scope reduction list per cluster immediately

### Risk 4: Docker Compose Issues
**Mitigation:** Provide local dev runbook (no Docker)

### Risk 5: Time Pressure
**Mitigation:** Prioritize core functionality, defer non-essential features

### Risk 6: ML Dependencies Leak into Deployment
**Mitigation:** Strict enforcement — NO ML dependencies in Dockerfiles or requirements.txt. Only precomputed results ingested.

### Risk 7: Cloud Dependency Required
**Mitigation:** Fully self-hosted deployment — MinIO (local), Docker Compose (local), no cloud services required.

---

## 📊 REFERENCE DOCUMENTS

### Diagnostic Documents
- [Diagnóstico Completo](../COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md) - Full gap analysis
- [Lista de Tarefas Críticas](../CRITICAL_TASKS_PRIORITY_LIST_PT_BR.md) - Prioritized tasks

### Cluster Documents
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy document
- [Data Cluster](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md)
- [Backend Cluster](./02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md)
- [Frontend Cluster](./03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md)
- [Deploy Cluster](./04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md)

### Roadmap Documents
- [Roadmap Analytics Engineering](../../proj/roadmaps/ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md) - Full roadmap vision
- [Estado Atual Pré-Processamento](../../proj/roadmaps/CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md) - Current state

---

## 🔗 KEY RECOMMENDATIONS

### Technical Decisions
1. **Parquet + DuckDB** - Fastest path to SQL over Parquet without Spark
2. **MinIO Docker** - Fastest storage setup (or S3 if AWS account exists)
3. **Docker Compose** - Fastest reproducible deployment
4. **Recharts** - Simple, lightweight charting for React

### ML Ops Strategy
1. **Separate ML Environment** - ML processing runs locally/separately, outputs Parquet to shared storage
2. **Deployment Only Reads** - Production deployment only reads precomputed ML results
3. **No ML Dependencies** - Keep deployment containers lightweight (< 600 MB, CPU-only)
4. **Offline Deployable** - Full deployment works in air-gapped environments

### Scope Reduction Strategy
- **Absolute Minimal:** No external APIs, use existing CSVs only
- **Minimal Analytics:** Only fact_forecast, no dimensions
- **No Parquet:** PostgreSQL for small datasets
- **No Docker:** Local dev runbook

---

## 📝 FOLLOW-UP QUESTIONS (ANSWER QUICKLY)

### Storage & Infrastructure
1. **Storage:** Do you have AWS account and prefer S3, or default to MinIO docker-compose?
2. **Transformation:** Prefer Python scripts or dbt SQL? (dbt recommended if time allows)

### Backend & API
3. **Data Access:** DuckDB + Parquet acceptable? Or must use Spark?
4. **Caching:** Redis available, or use in-memory cache?
5. **Auth:** Simple API key or JWT/OAuth?

### Frontend & UX
6. **Chart Library:** Recharts or Chart.js? (Recharts recommended)
7. **Bundle Size:** Target < 500KB gzipped acceptable?
8. **Responsive:** Desktop-only OK for MVP, or need mobile?

### Deployment
9. **Deployment:** Local Docker Compose OK, or need cloud VM?
10. **Public Access:** Need public URL, or local-only OK?
11. **Monitoring:** Health checks only OK, or need full monitoring?

### Business Requirements
12. **Dashboards:** Which exact KPIs must be visible on Day 4? (List top 3)
13. **Data Sources:** Which external APIs are critical? (Weather, Economic, 5G - prioritize)
14. **Schema:** What exact columns are needed by dashboard? (See Backend section)

---

## ✅ QUICK CHECKLIST FOR ASSIGNMENT

### Assign Cluster Leads
- [ ] **Data Lead:** Data Engineer (1-2 engineers)
- [ ] **Backend Lead:** Backend Lead (1-2 engineers)
- [ ] **Frontend Lead:** Frontend Lead (1-2 engineers)
- [ ] **Deploy Lead:** DevOps/Backend Lead (1 engineer)

### Daily Standup (9 AM)
- [ ] Review progress from previous day
- [ ] Identify blockers
- [ ] Assign tasks for current day
- [ ] Update status in shared doc

### End of Day Acceptance
- [ ] Test each day's deliverables
- [ ] Document any blockers
- [ ] Update status for next day

---

## 🎯 SUCCESS METRICS

### Functional Metrics
- ✅ All services deployed and accessible
- ✅ Dashboard renders with correct data
- ✅ API endpoints return expected JSON
- ✅ Data pipeline runs end-to-end

### Performance Metrics
- ✅ Data queries < 2s
- ✅ API endpoints < 500ms cached, < 2s cold
- ✅ Frontend load < 2.5s
- ✅ Services start < 2 minutes

### Quality Metrics
- ✅ Backend 80%+ test coverage
- ✅ Frontend E2E tests passing
- ✅ Data quality < 1% nulls
- ✅ Health checks passing

---

## 📚 NEXT STEPS

1. **Review All Cluster Documents** - Read each cluster doc thoroughly
2. **Answer Follow-Up Questions** - Decide on technical choices quickly
3. **Assign Cluster Leads** - Assign leads and team members
4. **Kickoff Meeting** - Review all documents, align on approach
5. **Start Sprint** - Begin D0 deliverables today

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Execution-Ready - 4-Day Sprint Overview

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

