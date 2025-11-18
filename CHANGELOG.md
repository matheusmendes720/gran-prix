# Nova Corrente – Complete Changelog

> **Tip:** All file/folder references below are clickable in most editors for quick navigation.

> **🗺️ Master Navigation:** For complete navigation of all documentation, roadmaps, and changelogs, see **[docs/NAVIGATION_INDEX.md](docs/NAVIGATION_INDEX.md)**

> **Note:** This project has evolved into two distinct paths: **DEMO** (4-day sprint, simplified) and **PROD** (production-ready, enterprise-scale). See separate changelogs for path-specific history:
> - **[CHANGELOG_DEMO.md](CHANGELOG_DEMO.md)** - Complete DEMO path history
> - **[CHANGELOG_PROD.md](CHANGELOG_PROD.md)** - Complete PROD path history
> - **[docs/ARCHITECTURE_BIFURCATION_ANALYSIS.md](docs/ARCHITECTURE_BIFURCATION_ANALYSIS.md)** - Analysis of path divergence

---

## [3.1.0-docs] – 2025-11-14

### Added
- **Implementation roadmap and deployment checklists**
  - [`IMPLEMENTATION_CHECKLIST.md`](IMPLEMENTATION_CHECKLIST.md) — phased plan for PostgreSQL migration, backend refactor, frontend integration, ML pipeline, production deployment, monitoring, and rollback.
  - [`docs/proj/roadmaps/SESSION_REPORT_COMPLETE_CHANGES_PT_BR.md`](docs/proj/roadmaps/SESSION_REPORT_COMPLETE_CHANGES_PT_BR.md) — consolidated report of analytics engineering + fullstack documentation and roadmap coverage.
- **Executive and strategy reports**
  - [`docs/pitch/relatorio_final/Relatorio-Executivo-Conciso-Imparcial.md`](docs/pitch/relatorio_final/Relatorio-Executivo-Conciso-Imparcial.md) — neutral, evidence-based executive report comparing SCM platforms (SAP IBP, Blue Yonder, Kinaxis, NetSuite, TOTVS, Proteus, MaxPro) and recommending Kinaxis RapidResponse.
  - Other competitive analysis and pitch material under [`docs/pitch/relatorio_final/`](docs/pitch/relatorio_final/) and [`docs/pitch/`](docs/pitch/).
- **Frontend feature-engineering documentation**
  - [`docs/development/FRONTEND_UX_TECHNICAL_DIAGNOSIS.md`](docs/development/FRONTEND_UX_TECHNICAL_DIAGNOSIS.md) — deep analysis of the current dashboard UX, data wiring, and gaps between components and backend contracts.
  - [`docs/development/frontend_feature_engineering/INDEX.md`](docs/development/frontend_feature_engineering/INDEX.md) — index for the “Intent to Feature Engineering” series, including:
    - [`legacy-dashboard-restoration.md`](docs/development/frontend_feature_engineering/legacy-dashboard-restoration.md)
    - [`scenario-simulator-integration.md`](docs/development/frontend_feature_engineering/scenario-simulator-integration.md)
    - [`bff-data-pipeline.md`](docs/development/frontend_feature_engineering/bff-data-pipeline.md)
    - [`climate-storytelling.md`](docs/development/frontend_feature_engineering/climate-storytelling.md)
    - [`demo-snapshot-mode.md`](docs/development/frontend_feature_engineering/demo-snapshot-mode.md)
    - [`geo-heatmap-insights.md`](docs/development/frontend_feature_engineering/geo-heatmap-insights.md)
    - [`safe-restore-roadmap.md`](docs/development/frontend_feature_engineering/safe-restore-roadmap.md)
- **Startup and integration guides**
  - [`docs/development/STARTUP_GUIDE.md`](docs/development/STARTUP_GUIDE.md) — end-to-end startup instructions for backend and frontend.
  - [`docs/development/QUICK_START_BACKEND.md`](docs/development/QUICK_START_BACKEND.md) and [`docs/development/BACKEND_INTEGRATION_GUIDE.md`](docs/development/BACKEND_INTEGRATION_GUIDE.md) — focused guides for backend API and integration.

### Changed
- **Architecture & narrative alignment**
  - Documentation now explicitly positions the PostgreSQL + offline-ML stack as the reference architecture for Nova Corrente.
  - Frontend feature-engineering docs align dashboard UX scenarios with the new read-only API and BFF patterns.
- **Roadmap clarity**
  - [`docs/proj/roadmaps/`](docs/proj/roadmaps/) updated to classify documents by category (production focus, migration, templates, indices) and link to new implementation-focused guides.

### Documentation
- **Centralized indexes**
  - Roadmaps and implementation docs indexed under [`docs/proj/roadmaps/`](docs/proj/roadmaps/).
  - Frontend feature-engineering docs indexed under [`docs/development/frontend_feature_engineering/INDEX.md`](docs/development/frontend_feature_engineering/INDEX.md).
- **Business/strategy layer**
  - SCM platform evaluation and recommendation captured under [`docs/pitch/relatorio_final/`](docs/pitch/relatorio_final/), complementing the technical architecture documentation.

---

## [3.0.0-postgres] – 2025-11-05

### Added
- **PostgreSQL core architecture**
  - Multi-schema database design (`core`, `analytics`, `support`, `staging`) with advanced features (partitioning, JSONB, materialized views).
  - Alembic configuration and initial migration for the PostgreSQL schema.
  - Planned demo data utilities and verification queries (see [`IMPLEMENTATION_CHECKLIST.md`](IMPLEMENTATION_CHECKLIST.md) for commands).
- **Backend API (read-only, offline-first)**
  - Flask-based API exposing:
    - Health checks (`/health`).
    - Read-only endpoints for items, demand, inventory, forecasts, features, alerts, and recommendations under `/api/v1/…`.
  - Central configuration and connection management:
    - [`backend/config/database_config.py`](backend/config/database_config.py)
    - [`backend/app/config.py`](backend/app/config.py)
    - `.env` templates under [`backend/`](backend/).
- **Next.js 14 frontend**
  - Next.js 14 + TypeScript dashboard implementation under [`frontend/app/`](frontend/app/) and [`frontend/src/components/`](frontend/src/components/).
  - KPI cards, trend charts, alerts/recommendations panels, and materials drill-down pages (see `app/dashboard/page.tsx`, `app/materials/page.tsx`, `app/materials/[itemId]/page.tsx` when present).
- **Offline ML and ETL pipeline**
  - Offline forecasting pipeline entrypoint: [`ml_pipeline/main.py`](ml_pipeline/main.py) (Prophet + feature engineering loop, as per ML docs).
  - ETL scripts for loading precomputed ML outputs into PostgreSQL:
    - [`etl/load_ml_outputs.py`](etl/load_ml_outputs.py) (forecasts + features).
    - [`etl/calculate_kpis.sql`](etl/calculate_kpis.sql) (stockout rate, ABC-A share, delayed orders, etc.).
  - Output artifacts stored as Parquet for forecasts and features.
- **Security, caching, and auditing**
  - JWT-based authentication and role-based access control (RBAC) with roles: `ADMIN`, `ANALYST`, `VIEWER`.
  - Redis-based caching layer with endpoint-specific strategies.
  - Dedicated audit logging pipeline and retrieval/cleanup endpoints.
- **Containerization and deployment**
  - Dockerfiles for backend and frontend (e.g. [`backend/Dockerfile.flask`](backend/Dockerfile.flask), [`frontend/Dockerfile.nextjs`](frontend/Dockerfile.nextjs)).
  - [`docker-compose.prod.yml`](docker-compose.prod.yml) for production orchestration, plus dev configuration.

### Changed
- Migrated storage from MySQL/SQLite to PostgreSQL, leveraging partitioning, JSONB columns, and materialized views for analytics.
- Enforced **offline-first** ML architecture: production reads only from precomputed tables; training/inference runs are executed out-of-band.
- Replaced the previous API implementation with a read-only Flask API surface optimized for dashboards and analytics.
- Updated the frontend from the legacy implementation to a modern stack (Next.js 14, TypeScript, Tailwind CSS, Recharts).
- Applied Redis caching and database indexing to reduce response times on high-traffic endpoints.
- Strengthened security boundaries with JWT+RBAC and stricter environment configuration.

### Fixed
- Database connection pooling and stability issues when serving concurrent dashboard traffic.
- Performance bottlenecks in complex analytics queries via materialized views and targeted indexes.
- Security vulnerabilities related to unauthenticated access paths and weak secrets.
- Cross-origin resource sharing (CORS) misconfigurations between backend and frontend.
- Inconsistent API response formats and error handling across endpoints.
- Frontend state management and data fetching edge cases under error or empty-data scenarios.
- Type safety gaps in the new TypeScript-based frontend.

### Security
- Implemented JWT-based authentication and RBAC (admin/analyst/viewer) across protected endpoints.
- Adopted bcrypt-based password hashing and improved password strength validation utilities.
- Hardened environment configuration (secrets, DB credentials, JWT keys).
- Protected API endpoints with token validation and basic input validation/sanitization.
- Ensured audit logging is explicit and avoids leaking sensitive information.

### Performance
- PostgreSQL partitioning for large fact tables (e.g. daily demand).
- Materialized views for frequently accessed KPI and trend queries.
- Redis caching for high-traffic endpoints and expensive analytics queries.
- Connection pooling and tuned SQL queries with appropriate indexing.
- Improved frontend rendering using Next.js SSR/CSR hybrid patterns and lightweight data-fetching hooks.

### Documentation
- Deployment guides, environment variable examples, and Docker Compose usage documented under:
  - [`docs/proj/roadmaps/`](docs/proj/roadmaps/)
  - [`docs/development/STARTUP_GUIDE.md`](docs/development/STARTUP_GUIDE.md)
  - [`docs/development/QUICK_START_BACKEND.md`](docs/development/QUICK_START_BACKEND.md)
- Data pipeline workflow and architecture captured in analytics engineering and ML documentation (see `docs/mathematics/` and `docs/proj/roadmaps/`).

---

## [2.0.0] – 2025-11-04 – ML Ops Constraint Enforcement

> **Commit:** `7c440c5`  
> **Scope:** Remove external ML/ETL/third-party dependencies from the deployment path and enforce an offline, self-contained runtime.

### Added
- **Simplified deployment changelog**
  - [`docs/diagnostics/anamnese/03_implementacao/CHANGELOG_SIMPLIFICACAO_IMPLEMENTACAO.md`](docs/diagnostics/anamnese/03_implementacao/CHANGELOG_SIMPLIFICACAO_IMPLEMENTACAO.md) — detailed record of all code changes made to simplify deployment and remove ML/external dependencies.
- **Validation scripts**
  - [`scripts/validation/check_no_ml_imports.py`](scripts/validation/check_no_ml_imports.py)
  - [`scripts/validation/check_no_external_apis.py`](scripts/validation/check_no_external_apis.py)
  - [`scripts/validation/validate_deployment_simplified.py`](scripts/validation/validate_deployment_simplified.py) (planned final validation before deploy).

### Changed
- **Backend integration manager**
  - File: [`backend/app/core/integration_manager.py`](backend/app/core/integration_manager.py)
  - Removed:
    - `external_data_service` initialization and wiring.
    - External API clients (INMET, BACEN, ANATEL, OpenWeatherMap, and other expanded integrations).
    - Prediction/ML services from the runtime path.
  - Cleaned up imports, unused members, and improved logging around disabled integrations.
- **Pipelines orchestrator**
  - File: [`backend/pipelines/orchestrator_service.py`](backend/pipelines/orchestrator_service.py)
  - Disabled calls to external ETL pipelines:
    - Climate ETL
    - Economic ETL
    - ANATEL 5G ETL
  - Left clear logs indicating the system now relies on precomputed, internal data only.
- **Legacy Flask API**
  - File: [`backend/api/enhanced_api.py`](backend/api/enhanced_api.py)
  - Marked as **DEPRECATED** and removed all dependencies on prediction services and external data services.
  - Disabled endpoints:
    - `/api/materials/<int:material_id>/forecast`
    - `/api/models/<int:model_id>/predict`
    - `/api/external-data/refresh`
  - Replaced with `410 Gone` responses and informative error messages.
- **Health checks**
  - File: [`backend/app/api/v1/routes/health.py`](backend/app/api/v1/routes/health.py)
  - Removed checks for external API clients and configs (INMET, BACEN, ANATEL, OpenWeather, etc.).
  - Simplified health and readiness probes to track only database and local ML dependencies.

### Fixed
- Eliminated risk of runtime failures caused by missing external ML models or third-party APIs.
- Reduced deployment complexity (no need for real-time ML services or external data calls in production).
- Ensured health checks accurately reflect the simplified, offline architecture.

### Documentation
- Detailed, file-level change log for simplification:
  - [`docs/diagnostics/anamnese/03_implementacao/CHANGELOG_SIMPLIFICACAO_IMPLEMENTACAO.md`](docs/diagnostics/anamnese/03_implementacao/CHANGELOG_SIMPLIFICACAO_IMPLEMENTACAO.md)
- Updated high-level documentation to reflect that:
  - External APIs are no longer part of the mandatory deployment scope.
  - ML services are strictly offline and not part of the production request path.

---

## [1.0.0] – 2025-11-03 – Initial Release

> **Commit:** `457b704`  
> **Scope:** Initial fullstack analytics dashboard, ML experimentation stack, and baseline documentation.

### Added
- **Initial fullstack app**
  - Backend API (FastAPI/Flask depending on branch) exposing endpoints for demand, inventory, and basic analytics.
  - Next.js-based frontend dashboard with core pages under `frontend/` (main dashboard, basic materials view, and exploratory analytics).
- **Data and ML experimentation**
  - Initial data ingestion and preprocessing scripts under `data/` and `scripts/`.
  - ML experimentation notebooks and technical notes under `docs/mathematics/` and `docs/reports/`.
- **Documentation and workflow**
  - Project-level documentation under `docs/` describing architecture, datasets, and experimentation results.
  - Git workflow documentation and collaboration guidelines (later expanded in the changelog session).

### Notes
- This version established the first working baseline for Nova Corrente's analytics dashboard and experimentation environment.
- Subsequent versions (`2.0.0`, `3.0.0-postgres`, `3.1.0-docs`) iteratively hardened deployment, simplified ML dependencies, migrated to PostgreSQL, and formalized documentation/roadmaps.
- **Path Split:** After version `3.1.0-docs`, the project split into two paths:
  - **DEMO Path:** 4-day sprint, simplified stack (Parquet + MinIO + DuckDB)
  - **PROD Path:** Production-ready, enterprise-scale (PostgreSQL + future: AWS + Airflow + dbt)
  - See [CHANGELOG_DEMO.md](CHANGELOG_DEMO.md) and [CHANGELOG_PROD.md](CHANGELOG_PROD.md) for path-specific history.

---

## [4.0.0-roadmap-split] – 2025-11-17 – Roadmap Bifurcation

### Added
- **Separate Changelogs**
  - [`CHANGELOG_DEMO.md`](CHANGELOG_DEMO.md) — complete DEMO path history (4-day sprint, mock data, local ML, roadshow)
  - [`CHANGELOG_PROD.md`](CHANGELOG_PROD.md) — complete PROD path history (PostgreSQL, AWS, Airflow, dbt, full stack)
- **Architecture Analysis Documents**
  - [`docs/ARCHITECTURE_BIFURCATION_ANALYSIS.md`](docs/ARCHITECTURE_BIFURCATION_ANALYSIS.md) — complete analysis of path divergence with inflection points
  - [`docs/STACK_COMPARISON_DEMO_VS_PROD.md`](docs/STACK_COMPARISON_DEMO_VS_PROD.md) — detailed technology stack comparison
  - [`docs/ROADMAP_BIFURCATION_TIMELINE.md`](docs/ROADMAP_BIFURCATION_TIMELINE.md) — visual timeline of path divergence
- **Migration Guides**
  - [`docs/MIGRATION_DEMO_TO_PROD.md`](docs/MIGRATION_DEMO_TO_PROD.md) — step-by-step migration from DEMO to PROD
  - [`docs/MIGRATION_PROD_TO_DEMO.md`](docs/MIGRATION_PROD_TO_DEMO.md) — step-by-step simplification from PROD to DEMO
- **Reorganized Roadmap Documents**
  - [`docs/proj/roadmaps/demo/`](docs/proj/roadmaps/demo/) — DEMO path roadmaps
  - [`docs/proj/roadmaps/prod/`](docs/proj/roadmaps/prod/) — PROD path roadmaps
  - [`docs/proj/roadmaps/shared/`](docs/proj/roadmaps/shared/) — shared documentation
- **Path-Specific Indexes**
  - [`docs/proj/roadmaps/demo/README_DEMO_ROADMAPS.md`](docs/proj/roadmaps/demo/README_DEMO_ROADMAPS.md) — DEMO path navigation
  - [`docs/proj/roadmaps/prod/README_PROD_ROADMAPS.md`](docs/proj/roadmaps/prod/README_PROD_ROADMAPS.md) — PROD path navigation
- **Technical Stack Documentation**
  - [`docs/proj/roadmaps/demo/TECHNICAL_STACK_DEMO.md`](docs/proj/roadmaps/demo/TECHNICAL_STACK_DEMO.md) — complete DEMO stack breakdown
  - [`docs/proj/roadmaps/prod/TECHNICAL_STACK_PROD.md`](docs/proj/roadmaps/prod/TECHNICAL_STACK_PROD.md) — complete PROD stack breakdown

### Changed
- **Roadmap Organization**
  - Reorganized all roadmap documents into DEMO, PROD, and shared folders
  - Updated [`docs/proj/roadmaps/README_ROADMAPS.md`](docs/proj/roadmaps/README_ROADMAPS.md) with path selector and comparison
  - Updated all internal links to reflect new folder structure
- **Documentation Structure**
  - Clear separation between DEMO and PROD paths
  - Shared documentation clearly identified
  - Path-specific documentation organized by use case

### Documentation
- **Complete Path Analysis**
  - All inflection points documented with commit hashes, dates, and rationale
  - Stack evolution charts for both paths
  - Decision rationale for each path
  - Future convergence possibilities documented

---
