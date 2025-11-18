# Migration Guide: DEMO → PROD
## Step-by-Step Migration from DEMO to PROD Path

**Version:** 1.0  
**Date:** November 2025  
**Status:** Complete Guide

---

## Overview

This guide provides step-by-step instructions for migrating from the DEMO path (4-day sprint, simplified stack) to the PROD path (production-ready, enterprise-scale).

### Migration Scope
- Database: Parquet files → PostgreSQL
- Storage: MinIO → (Future: S3 + Delta Lake)
- Compute: DuckDB → PostgreSQL + (Future: Spark)
- Orchestration: Simple scheduler → (Future: Airflow)
- Transformations: Python scripts → (Future: dbt models)
- Infrastructure: Local → Production + (Future: AWS)

---

## Prerequisites

- [ ] DEMO path fully functional
- [ ] PostgreSQL 14+ installed and configured
- [ ] Redis installed (for caching)
- [ ] Docker and Docker Compose installed
- [ ] Backup of all DEMO data
- [ ] Review of [PROD Path Changelog](../CHANGELOG_PROD.md)

---

## Phase 1: Database Migration

### Step 1.1: Set Up PostgreSQL

1. **Install PostgreSQL 14+**
   ```bash
   # Using Docker
   docker run --name postgres-nova-corrente \
     -e POSTGRES_USER=nova_corrente \
     -e POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD \
     -e POSTGRES_DB=nova_corrente \
     -p 5432:5432 \
     -v pgdata:/var/lib/postgresql/data \
     -d postgres:14
   ```

2. **Verify Installation**
   ```bash
   psql -U nova_corrente -h localhost -d nova_corrente
   ```

### Step 1.2: Set Up Alembic

1. **Install Alembic**
   ```bash
   pip install alembic psycopg2-binary
   ```

2. **Initialize Alembic**
   ```bash
   cd backend
   alembic init alembic
   ```

3. **Configure `alembic.ini`**
   ```ini
   sqlalchemy.url = postgresql://nova_corrente:YOUR_PASSWORD@localhost/nova_corrente
   ```

4. **Create Initial Migration**
   ```bash
   alembic revision -m "initial_schema"
   ```

5. **Copy Schema from Project.md**
   - Reference: [`docs/proj/diagrams/Project.md`](../proj/diagrams/Project.md)
   - Copy DDL into migration file

6. **Apply Migration**
   ```bash
   alembic upgrade head
   ```

### Step 1.3: Migrate Data from Parquet to PostgreSQL

1. **Export Parquet Data**
   ```python
   import pandas as pd
   import duckdb
   
   # Read from Parquet using DuckDB
   conn = duckdb.connect()
   df = conn.execute("SELECT * FROM read_parquet('data/gold/*.parquet')").df()
   ```

2. **Load into PostgreSQL**
   ```python
   from sqlalchemy import create_engine
   
   engine = create_engine('postgresql://nova_corrente:password@localhost/nova_corrente')
   df.to_sql('fact_demand_daily', engine, if_exists='append', index=False)
   ```

3. **Verify Data**
   ```sql
   SELECT COUNT(*) FROM core.fact_demand_daily;
   ```

---

## Phase 2: Backend Migration

### Step 2.1: Update Configuration

1. **Update `backend/config/database_config.py`**
   - Change from DuckDB/Parquet to PostgreSQL
   - Update connection string

2. **Update `backend/app/config.py`**
   - Set `DATABASE_URL` to PostgreSQL
   - Configure connection pooling

3. **Update `.env`**
   ```env
   DATABASE_URL=postgresql://nova_corrente:password@localhost/nova_corrente
   REDIS_URL=redis://localhost:6379/0
   ```

### Step 2.2: Update Data Access Layer

1. **Replace DuckDB Queries with SQLAlchemy**
   - Convert DuckDB SQL to SQLAlchemy ORM
   - Update all data access functions

2. **Implement Connection Pooling**
   - Configure SQLAlchemy connection pool
   - Set appropriate pool size

### Step 2.3: Add Redis Caching

1. **Install Redis**
   ```bash
   docker run -d -p 6379:6379 redis:alpine
   ```

2. **Update Backend to Use Redis**
   - Add Redis client configuration
   - Implement caching strategies
   - Update API endpoints to use cache

---

## Phase 3: Frontend Updates

### Step 3.1: Update API Client

1. **Update `frontend/src/lib/api.ts`**
   - Verify API endpoints match new backend
   - Update data types if needed

2. **Test All Endpoints**
   - Verify all API calls work
   - Check error handling

### Step 3.2: Update Environment Variables

1. **Update `frontend/.env.local`**
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```

---

## Phase 4: ML Pipeline Migration

### Step 4.1: Update ML Pipeline

1. **Update `backend/ml_pipeline/main.py`**
   - Ensure outputs are compatible with PostgreSQL
   - Update export format if needed

2. **Update ETL Scripts**
   - Modify `backend/etl/load_ml_outputs.py` for PostgreSQL
   - Update data loading procedures

### Step 4.2: Verify ML Outputs

1. **Run ML Pipeline**
   ```bash
   python backend/ml_pipeline/main.py
   ```

2. **Load Results into PostgreSQL**
   ```bash
   python backend/etl/load_ml_outputs.py
   ```

3. **Verify Data**
   ```sql
   SELECT COUNT(*) FROM analytics.fact_forecasts;
   ```

---

## Phase 5: Deployment Migration

### Step 5.1: Update Docker Compose

1. **Update `docker-compose.prod.yml`**
   - Add PostgreSQL service
   - Add Redis service
   - Update service dependencies

2. **Update Dockerfiles**
   - Ensure PostgreSQL client libraries are included
   - Update requirements files

### Step 5.2: Deploy

1. **Build Images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Start Services**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Verify Deployment**
   ```bash
   curl http://localhost:5000/health
   ```

---

## Phase 6: Testing and Validation

### Step 6.1: Functional Testing

- [ ] All API endpoints respond correctly
- [ ] Frontend displays data correctly
- [ ] ML outputs load successfully
- [ ] Caching works as expected
- [ ] Authentication works

### Step 6.2: Performance Testing

- [ ] Database queries perform well
- [ ] Caching improves response times
- [ ] Connection pooling works correctly
- [ ] No memory leaks

### Step 6.3: Data Validation

- [ ] All data migrated correctly
- [ ] No data loss
- [ ] Data integrity maintained
- [ ] Relationships preserved

---

## Future Migration Steps (Optional)

### Phase 7: Cloud Infrastructure (Future)

1. **Set Up AWS S3**
   - Create S3 buckets
   - Configure access policies
   - Migrate data to S3

2. **Set Up Delta Lake**
   - Install Delta Lake
   - Convert Parquet to Delta format
   - Set up Delta tables

3. **Set Up Spark/Databricks**
   - Configure Spark cluster
   - Migrate processing logic
   - Update data pipelines

### Phase 8: Orchestration (Future)

1. **Set Up Airflow**
   - Install Airflow
   - Create DAGs
   - Migrate scheduler logic

2. **Set Up dbt**
   - Install dbt
   - Convert Python scripts to dbt models
   - Set up dbt project

---

## Rollback Plan

If migration fails, rollback steps:

1. **Stop PROD Services**
   ```bash
   docker-compose -f docker-compose.prod.yml down
   ```

2. **Restore DEMO Environment**
   - Restore Parquet files from backup
   - Restore MinIO data
   - Restart DEMO services

3. **Verify DEMO Works**
   ```bash
   curl http://localhost:5000/health
   ```

---

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check PostgreSQL is running
   - Verify connection string
   - Check firewall rules

2. **Data Migration Errors**
   - Verify Parquet file formats
   - Check data types match schema
   - Review error logs

3. **Performance Issues**
   - Check connection pool settings
   - Verify indexes are created
   - Review query performance

---

## References

- [PROD Path Changelog](../CHANGELOG_PROD.md)
- [DEMO Path Changelog](../CHANGELOG_DEMO.md)
- [Stack Comparison](STACK_COMPARISON_DEMO_VS_PROD.md)
- [Implementation Checklist](../IMPLEMENTATION_CHECKLIST.md)
- [PostgreSQL Specification](../proj/diagrams/Project.md)

---

**Document Created:** November 2025  
**Version:** 1.0  
**Status:** Complete Guide

