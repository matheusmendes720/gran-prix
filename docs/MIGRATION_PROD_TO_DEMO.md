# Migration Guide: PROD → DEMO
## Step-by-Step Simplification from PROD to DEMO Path

**Version:** 1.0  
**Date:** November 2025  
**Status:** Complete Guide

---

## Overview

This guide provides step-by-step instructions for simplifying from the PROD path (production-ready, enterprise-scale) to the DEMO path (4-day sprint, simplified stack).

### Simplification Scope
- Database: PostgreSQL → Parquet files
- Storage: PostgreSQL → MinIO + Parquet
- Compute: PostgreSQL → DuckDB
- Orchestration: (Future: Airflow) → Simple scheduler
- Transformations: (Future: dbt) → Python scripts
- Infrastructure: Production → Local

---

## Prerequisites

- [ ] PROD path fully functional
- [ ] MinIO installed and configured
- [ ] DuckDB available
- [ ] Backup of all PROD data
- [ ] Review of [DEMO Path Changelog](../CHANGELOG_DEMO.md)

---

## Phase 1: Data Export

### Step 1.1: Export PostgreSQL Data to Parquet

1. **Export Core Tables**
   ```python
   import pandas as pd
   from sqlalchemy import create_engine
   
   engine = create_engine('postgresql://nova_corrente:password@localhost/nova_corrente')
   
   # Export fact tables
   df = pd.read_sql('SELECT * FROM core.fact_demand_daily', engine)
   df.to_parquet('data/gold/fact_demand_daily.parquet', index=False)
   
   # Export dimension tables
   df = pd.read_sql('SELECT * FROM core.dim_item', engine)
   df.to_parquet('data/gold/dim_item.parquet', index=False)
   ```

2. **Export Analytics Tables**
   ```python
   # Export forecasts
   df = pd.read_sql('SELECT * FROM analytics.fact_forecasts', engine)
   df.to_parquet('data/gold/fact_forecasts.parquet', index=False)
   ```

3. **Verify Exports**
   ```python
   import duckdb
   conn = duckdb.connect()
   df = conn.execute("SELECT * FROM read_parquet('data/gold/fact_demand_daily.parquet')").df()
   print(df.head())
   ```

---

## Phase 2: Storage Migration

### Step 2.1: Set Up MinIO

1. **Install MinIO**
   ```bash
   docker run -d -p 9000:9000 -p 9001:9001 \
     -e MINIO_ROOT_USER=minioadmin \
     -e MINIO_ROOT_PASSWORD=minioadmin \
     minio/minio server /data --console-address ":9001"
   ```

2. **Create Buckets**
   - Bronze bucket (raw data)
   - Silver bucket (cleaned data)
   - Gold bucket (curated data)

3. **Upload Parquet Files**
   ```python
   from minio import Minio
   
   client = Minio('localhost:9000',
                  access_key='minioadmin',
                  secret_key='minioadmin',
                  secure=False)
   
   client.fput_object('gold', 'fact_demand_daily.parquet', 
                      'data/gold/fact_demand_daily.parquet')
   ```

---

## Phase 3: Backend Simplification

### Step 3.1: Update Configuration

1. **Update `backend/config/database_config.py`**
   - Change from PostgreSQL to DuckDB/Parquet
   - Update data access methods

2. **Update `backend/app/config.py`**
   - Remove PostgreSQL connection
   - Configure DuckDB connection
   - Remove Redis if not needed

3. **Update `.env`**
   ```env
   # Remove PostgreSQL
   # DATABASE_URL=postgresql://...
   
   # Add MinIO
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   ```

### Step 3.2: Replace SQLAlchemy with DuckDB

1. **Update Data Access Functions**
   ```python
   import duckdb
   
   # Replace SQLAlchemy queries with DuckDB
   conn = duckdb.connect()
   df = conn.execute("""
       SELECT * FROM read_parquet('data/gold/fact_demand_daily.parquet')
       WHERE date >= '2025-01-01'
   """).df()
   ```

2. **Update All API Endpoints**
   - Replace PostgreSQL queries with DuckDB
   - Update data access patterns

### Step 3.3: Remove Production Features

1. **Remove Redis Caching** (optional, can keep for performance)
   - Remove Redis client
   - Remove caching decorators
   - Update endpoints

2. **Simplify Authentication** (optional)
   - Keep JWT if needed
   - Or remove for demo simplicity

---

## Phase 4: Frontend Updates

### Step 4.1: Update API Client

1. **Update `frontend/src/lib/api.ts`**
   - Verify API endpoints still work
   - Update data types if needed

2. **Test All Endpoints**
   - Verify all API calls work
   - Check error handling

---

## Phase 5: ML Pipeline Simplification

### Step 5.1: Update ML Pipeline

1. **Update `backend/ml_pipeline/main.py`**
   - Ensure outputs are Parquet format
   - Update export paths to MinIO

2. **Update ETL Scripts**
   - Modify to work with Parquet files
   - Update data loading procedures

---

## Phase 6: Deployment Simplification

### Step 6.1: Update Docker Compose

1. **Update `docker-compose.yml`**
   - Remove PostgreSQL service
   - Add MinIO service
   - Remove Redis if not needed
   - Simplify service dependencies

2. **Update Dockerfiles**
   - Remove PostgreSQL client libraries
   - Update requirements files

### Step 6.2: Deploy

1. **Build Images**
   ```bash
   docker-compose build
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Verify Deployment**
   ```bash
   curl http://localhost:5000/health
   ```

---

## Phase 7: Remove Complex Components

### Step 7.1: Remove Future Components (if any)

1. **Remove Airflow** (if installed)
   - Stop Airflow services
   - Remove Airflow configuration
   - Convert DAGs to simple scheduler

2. **Remove dbt** (if installed)
   - Remove dbt project
   - Convert dbt models to Python scripts
   - Update transformation logic

3. **Remove Cloud Services** (if any)
   - Remove AWS configurations
   - Remove cloud-specific code
   - Update to local alternatives

---

## Phase 8: Testing and Validation

### Step 8.1: Functional Testing

- [ ] All API endpoints respond correctly
- [ ] Frontend displays data correctly
- [ ] ML outputs work correctly
- [ ] Data access works with DuckDB
- [ ] MinIO storage works

### Step 8.2: Performance Testing

- [ ] DuckDB queries perform well
- [ ] Parquet file access is fast
- [ ] No performance regressions

### Step 8.3: Data Validation

- [ ] All data accessible from Parquet
- [ ] No data loss
- [ ] Data integrity maintained

---

## Rollback Plan

If simplification fails, rollback steps:

1. **Stop DEMO Services**
   ```bash
   docker-compose down
   ```

2. **Restore PROD Environment**
   - Restore PostgreSQL from backup
   - Restore Redis if needed
   - Restart PROD services

3. **Verify PROD Works**
   ```bash
   curl http://localhost:5000/health
   ```

---

## Troubleshooting

### Common Issues

1. **DuckDB Query Errors**
   - Check Parquet file paths
   - Verify file formats
   - Review error messages

2. **MinIO Connection Errors**
   - Check MinIO is running
   - Verify credentials
   - Check network connectivity

3. **Performance Issues**
   - Check Parquet file sizes
   - Verify DuckDB configuration
   - Review query patterns

---

## References

- [DEMO Path Changelog](../CHANGELOG_DEMO.md)
- [PROD Path Changelog](../CHANGELOG_PROD.md)
- [Stack Comparison](STACK_COMPARISON_DEMO_VS_PROD.md)
- [DEMO Roadmaps](../proj/roadmaps/demo/README_DEMO_ROADMAPS.md)

---

**Document Created:** November 2025  
**Version:** 1.0  
**Status:** Complete Guide

