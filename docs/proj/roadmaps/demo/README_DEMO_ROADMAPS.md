# DEMO Path Roadmaps Index
## Nova Corrente - 4-Day Sprint, Mock Data, Local ML, Roadshow-Ready

**Version:** 1.0  
**Date:** November 2025  
**Status:** Complete Index

---

## Overview

The DEMO path focuses on rapid deployment for roadshow demonstrations, MVP development, and cost-sensitive deployments. This path uses a simplified, lightweight stack that can be deployed in 4 days.

### Key Characteristics
- **Timeline:** 4 days (D0-D4)
- **Stack:** Parquet + MinIO + DuckDB + Pandas + Simple Scheduler
- **Use Case:** Roadshow, MVP, rapid deployment
- **Complexity:** Low
- **Cost:** Minimal

---

## Quick Start

1. **Read First:** [`docs/diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md`](../../../diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md)
2. **Global Constraints:** [`docs/diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md`](../../../diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)
3. **Choose Your Cluster:** See cluster documents below

---

## Core Documents

### 4-Day Sprint Overview
- **[00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md](../../../diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md)**
  - Complete 4-day sprint execution guide
  - Cluster structure and milestones
  - Quick orientation

### Global Constraints
- **[GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md](../../../diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)**
  - "NO ML OPS IN DEPLOYMENT" policy
  - Enforcement rules
  - Validation procedures

---

## Cluster Documents

### Data Cluster
- **[01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md](../../../diagnostics/clusters/01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md)**
  - Storage: MinIO + Parquet
  - Ingestion and transformations
  - Gold layer (Star Schema)

### Backend Cluster
- **[02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md](../../../diagnostics/clusters/02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md)**
  - FastAPI (read-only)
  - DuckDB + Parquet data access
  - No ML dependencies

### Frontend Cluster
- **[03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md](../../../diagnostics/clusters/03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md)**
  - React + Vite dashboard
  - Recharts visualizations
  - No ML processing UI

### Deploy Cluster
- **[04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md](../../../diagnostics/clusters/04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md)**
  - Docker Compose deployment
  - Offline deployable
  - Image size < 600 MB

---

## Simplified Roadmaps

### Analytics Engineering (4-Day Version)
- **[ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md](../ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md)**
  - Updated for 4-day sprint scope
  - Simplified stack (Parquet + MinIO + DuckDB)
  - Original 16-week plan preserved for reference

### Current Architecture to Analytics
- **[CURRENT_ARCHITECTURE_TO_ANALYTICS_ROADMAP_PT_BR.md](../CURRENT_ARCHITECTURE_TO_ANALYTICS_ROADMAP_PT_BR.md)**
  - Migration plan for 4-day sprint
  - Simplified architecture diagrams
  - Parquet layers (Bronze/Silver/Gold)

### Complete Roadmap Summary
- **[COMPLETE_ROADMAP_SUMMARY_PT_BR.md](../COMPLETE_ROADMAP_SUMMARY_PT_BR.md)**
  - Updated for 4-day sprint
  - Progress tracking
  - Next steps

---

## Technical Documentation

### Scope Update Summary
- **[SCOPE_UPDATE_4DAY_SPRINT_SUMMARY_PT_BR.md](../../../diagnostics/SCOPE_UPDATE_4DAY_SPRINT_SUMMARY_PT_BR.md)**
  - Complete scope reduction analysis
  - Before/after comparison
  - Document update status

### Implementation Summary
- **[IMPLEMENTATION_SUMMARY.md](../../../IMPLEMENTATION_SUMMARY.md)**
  - ML Ops constraint enforcement
  - Code separation
  - Docker infrastructure

---

## Stack Technology Overview

### Storage
- **Parquet:** Columnar file format
- **MinIO:** S3-compatible storage (local/Docker)
- **Layers:** Bronze (raw) → Silver (cleaned) → Gold (curated)

### Compute
- **DuckDB:** In-process SQL engine
- **Pandas:** Python data processing
- **No Spark/Databricks:** Removed for simplification

### Orchestration
- **Simple Scheduler:** Python scripts + cron
- **Docker Compose:** Service orchestration
- **No Airflow:** Removed for simplification

### Transformations
- **Python Scripts:** Custom transformation logic
- **SQL (DuckDB):** Queries over Parquet files
- **No dbt:** Removed for simplification

---

## Migration Path to PROD

See [`docs/MIGRATION_DEMO_TO_PROD.md`](../../../MIGRATION_DEMO_TO_PROD.md) for step-by-step migration guide.

**Key Migration Steps:**
1. Database: Parquet → PostgreSQL
2. Storage: MinIO → S3 + Delta Lake
3. Compute: DuckDB → Spark + Databricks
4. Orchestration: Simple scheduler → Airflow
5. Transformations: Python scripts → dbt models

---

## References

- [DEMO Path Changelog](../../../CHANGELOG_DEMO.md)
- [PROD Path Changelog](../../../CHANGELOG_PROD.md)
- [Stack Comparison](../../../STACK_COMPARISON_DEMO_VS_PROD.md)
- [Architecture Bifurcation Analysis](../../../ARCHITECTURE_BIFURCATION_ANALYSIS.md)
- [PROD Roadmaps](../prod/README_PROD_ROADMAPS.md)

---

**Last Updated:** November 2025  
**Version:** 1.0  
**Status:** Complete Index

