# Nova Corrente - DEMO Path Changelog
## 4-Day Sprint, Mock Data, Local ML, Roadshow-Ready

> **🗺️ Master Navigation:** For complete navigation of all documentation, roadmaps, and changelogs, see **[docs/NAVIGATION_INDEX.md](docs/NAVIGATION_INDEX.md)**

> **Path:** DEMO - Simplified, lightweight, roadshow-ready deployment  
> **Stack:** Parquet + MinIO + DuckDB + Pandas + Simple Scheduler  
> **Timeline:** 4 days (D0-D4)  
> **Use Case:** Roadshow demonstrations, MVP, rapid deployment

---

## [2.3.0-demo] – 2025-11-05 – Roadshow Preparation

### Added
- **4-Day Sprint Cluster Documents**
  - [`docs/diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md`](docs/diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md) — complete 4-day sprint execution guide
  - [`docs/diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md`](docs/diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) — global constraint enforcement
  - [`docs/diagnostics/clusters/01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md`](docs/diagnostics/clusters/01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md) — data cluster plan
  - [`docs/diagnostics/clusters/02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md`](docs/diagnostics/clusters/02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md) — backend cluster plan
  - [`docs/diagnostics/clusters/03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md`](docs/diagnostics/clusters/03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md) — frontend cluster plan
  - [`docs/diagnostics/clusters/04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md`](docs/diagnostics/clusters/04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md) — deploy cluster plan
- **Mock Data Generation**
  - Local ML processing scripts for generating demo data
  - Precomputed forecast outputs for roadshow demonstrations
  - Sample datasets for quick setup

### Changed
- **Scope Reduction**
  - Timeline: 16 weeks → 4 days
  - Stack: Delta Lake + S3 + Spark → Parquet + MinIO + DuckDB
  - Orchestration: Airflow → Simple scheduler
  - Transformations: dbt → Python scripts + SQL

### Documentation
- Complete 4-day sprint execution guide
- Cluster-specific implementation plans
- Roadshow preparation checklist

---

## [2.2.0-demo] – 2025-11-04 – Mock Data and Local ML Processing

### Added
- **Local ML Processing Environment**
  - Separate ML environment for generating precomputed results
  - Scripts for offline ML training and inference
  - Export utilities for Parquet output generation
- **Mock Data Infrastructure**
  - Sample data generators for demonstrations
  - Precomputed forecast tables
  - Demo-ready datasets

### Changed
- **ML Processing**
  - Moved ML processing to separate environment
  - Deployment only consumes precomputed Parquet files
  - No ML dependencies in deployment containers

### Documentation
- ML environment setup guide: [`docs/ml/ML_ENVIRONMENT_SETUP.md`](docs/ml/ML_ENVIRONMENT_SETUP.md)
- Mock data generation procedures

---

## [2.1.0-demo] – 2025-11-04 – 4-Day Sprint Scope Reduction

### Added
- **Simplified Stack Documentation**
  - Updated roadmap documents for 4-day sprint scope
  - Simplified architecture diagrams
  - Lightweight technology stack guides
- **Scope Reduction Summary**
  - [`docs/diagnostics/SCOPE_UPDATE_4DAY_SPRINT_SUMMARY_PT_BR.md`](docs/diagnostics/SCOPE_UPDATE_4DAY_SPRINT_SUMMARY_PT_BR.md)

### Changed
- **Architecture Simplification**
  - Storage: S3 + Delta Lake → MinIO + Parquet
  - Compute: Spark + Databricks → DuckDB + Pandas
  - Orchestration: Airflow/Prefect → Simple scheduler
  - Transformations: dbt models → Python scripts + SQL (DuckDB)
- **Timeline Reduction**
  - 16 weeks → 4 days (D0-D4)
  - Focus on MVP functionality
  - Roadshow-ready deployment

### Removed
- Cloud service dependencies
- Complex orchestration requirements
- Heavy ML Ops infrastructure
- Enterprise-scale features (deferred to PROD path)

### Documentation
- Updated all roadmap documents with 4-day sprint scope
- Created scope reduction summary document

---

## [2.0.0] – 2025-11-04 – ML Ops Constraint Enforcement

> **Commit:** `4e62dda`  
> **Tag:** `v2.0.0`, `sprint-4day-ready`  
> **Status:** Shared with PROD path

### Added
- **Deployment Constraint Enforcement**
  - Global constraint: "NO ML OPS IN DEPLOYMENT"
  - Validation scripts to enforce constraint
  - Separate ML requirements file
- **Simplified Deployment Requirements**
  - [`backend/requirements_deployment.txt`](backend/requirements_deployment.txt) — no ML dependencies
  - [`backend/requirements_ml.txt`](backend/requirements_ml.txt) — ML dependencies for separate environment

### Changed
- **Backend Integration Manager**
  - Removed external data service initialization
  - Removed external API clients (INMET, BACEN, ANATEL, OpenWeatherMap)
  - Removed prediction/ML services from runtime path
- **Pipelines Orchestrator**
  - Disabled external ETL pipeline calls
  - System now relies on precomputed, internal data only
- **Legacy Flask API**
  - Marked as DEPRECATED
  - Removed ML endpoints
  - Disabled external data refresh endpoints
- **Health Checks**
  - Simplified to track only database and local dependencies
  - Removed external API client checks

### Fixed
- Eliminated runtime failures from missing external services
- Reduced deployment complexity
- Enabled offline deployment capability

### Documentation
- [`docs/diagnostics/anamnese/03_implementacao/CHANGELOG_SIMPLIFICACAO_IMPLEMENTACAO.md`](docs/diagnostics/anamnese/03_implementacao/CHANGELOG_SIMPLIFICACAO_IMPLEMENTACAO.md)
- [`docs/IMPLEMENTATION_SUMMARY.md`](docs/IMPLEMENTATION_SUMMARY.md)

---

## [1.0.0] – 2025-11-03 – Initial Release (Shared Baseline)

> **Commit:** `457b704` / `1798c80`  
> **Tag:** `v1.0.0`  
> **Status:** Shared baseline with PROD path

### Added
- **Initial Fullstack App**
  - Backend API (FastAPI/Flask) with ML services
  - Next.js frontend dashboard
  - ML experimentation stack
- **Data and ML Infrastructure**
  - Data ingestion and preprocessing scripts
  - ML models (ARIMA, Prophet, LSTM, Ensemble)
  - External API integrations (INMET, BACEN, ANATEL)
- **Documentation**
  - Project structure documentation
  - Git workflow guidelines
  - Initial architecture documentation

### Notes
- This version established the baseline for both DEMO and PROD paths
- Full ML Ops vision with cloud services and real-time processing
- Subsequent versions diverged into DEMO (simplified) and PROD (enterprise) paths

---

## DEMO Path Characteristics

### Technology Stack
- **Storage:** Parquet files + MinIO (S3-compatible, local/Docker)
- **Compute:** DuckDB (in-process SQL) + Pandas (Python processing)
- **Orchestration:** Simple scheduler (Python scripts + cron)
- **Transformations:** Python scripts + SQL queries (DuckDB)
- **Frontend:** React + Vite + Recharts
- **Backend:** FastAPI (read-only, no ML dependencies)
- **ML Processing:** Separate environment, outputs Parquet files

### Key Features
- ✅ 4-day sprint deployment
- ✅ Offline deployable (air-gapped networks)
- ✅ No cloud dependencies
- ✅ Minimal infrastructure requirements
- ✅ Roadshow-ready demonstrations
- ✅ Mock data generation
- ✅ Local ML processing

### Use Cases
- Roadshow demonstrations
- MVP deployment
- Rapid prototyping
- Offline/air-gapped deployments
- Cost-sensitive deployments
- Local development and testing

---

## Migration to PROD Path

See [`docs/MIGRATION_DEMO_TO_PROD.md`](docs/MIGRATION_DEMO_TO_PROD.md) for step-by-step migration guide from DEMO to PROD path.

---

## References

- [PROD Path Changelog](CHANGELOG_PROD.md)
- [Architecture Bifurcation Analysis](docs/ARCHITECTURE_BIFURCATION_ANALYSIS.md)
- [Stack Comparison](docs/STACK_COMPARISON_DEMO_VS_PROD.md)
- [DEMO Roadmaps](docs/proj/roadmaps/demo/README_DEMO_ROADMAPS.md)

---

**Last Updated:** November 2025  
**Version:** 2.3.0-demo  
**Status:** Active Development

