# PROD Path Technical Stack
## Nova Corrente - Complete Stack Breakdown

**Version:** 1.0  
**Date:** November 2025  
**Status:** Complete Documentation

---

## Overview

The PROD path uses a production-ready, enterprise-scale technology stack optimized for long-term production deployment and scalability.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                         │
│  ERP | External APIs | Precomputed ML Results          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                        │
│              Multi-Schema Architecture                  │
│              - core: Business data                      │
│              - analytics: ML outputs                    │
│              - support: Auth, audit                     │
│              - staging: ETL staging                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              ML PROCESSING (Offline)                    │
│              Separate Environment                       │
│              - Prophet/ARIMA/LSTM training              │
│              - Output: PostgreSQL tables                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼ (Read-only)
┌─────────────────────────────────────────────────────────┐
│              BACKEND API (Flask)                        │
│              - Read-only endpoints                      │
│              - PostgreSQL queries                       │
│              - Redis caching                            │
│              - JWT authentication                       │
│              - NO ML dependencies                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (Next.js 14)                      │
│              - Dashboard with Recharts                  │
│              - TypeScript                               │
│              - Display precomputed insights             │
│              - NO ML processing UI                      │
└─────────────────────────────────────────────────────────┘
```

---

## Database Layer

### PostgreSQL 14+
- **Version:** PostgreSQL 14 or higher
- **Architecture:** Multi-schema design
- **Schemas:**
  - `core`: Business data (items, demand, inventory)
  - `analytics`: ML outputs (forecasts, features, metrics)
  - `support`: System data (users, audit logs)
  - `staging`: ETL staging area

### Key Features
- **Partitioning:** Large fact tables partitioned by date
- **JSONB:** Flexible schema for ML outputs
- **Materialized Views:** Precomputed analytics
- **Indexing:** Optimized indexes for query performance

### Schema Example
```sql
-- Core schema
CREATE SCHEMA core;

CREATE TABLE core.dim_item (
    item_id VARCHAR(50) PRIMARY KEY,
    item_name VARCHAR(255),
    category VARCHAR(100),
    -- ... other columns
);

CREATE TABLE core.fact_demand_daily (
    item_id VARCHAR(50),
    date DATE,
    demand INTEGER,
    -- ... other columns
) PARTITION BY RANGE (date);

-- Analytics schema
CREATE SCHEMA analytics;

CREATE TABLE analytics.fact_forecasts (
    forecast_id SERIAL PRIMARY KEY,
    item_id VARCHAR(50),
    forecast_date DATE,
    forecast_value NUMERIC,
    confidence_interval JSONB,
    model_version VARCHAR(50),
    generated_at TIMESTAMP
);
```

---

## Caching Layer

### Redis
- **Purpose:** High-traffic endpoint caching
- **Configuration:**
  ```python
  import redis
   
  redis_client = redis.Redis(
      host='localhost',
      port=6379,
      db=0,
      decode_responses=True
  )
  ```

### Caching Strategy
- **TTL:** 30 seconds to 1 hour (endpoint-specific)
- **Keys:** Pattern-based (e.g., `api:v1:items:{item_id}`)
- **Invalidation:** Manual or TTL-based

---

## Backend API

### Flask
- **Framework:** Flask 2.3+
- **Endpoints:** Read-only REST API
- **Data Access:** SQLAlchemy ORM over PostgreSQL
- **Dependencies:** NO ML libraries

**Example Endpoint:**
```python
from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)
engine = create_engine('postgresql://user:pass@localhost/db')

@app.route('/api/v1/items/<item_id>/timeseries')
def get_timeseries(item_id):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT date, demand
            FROM core.fact_demand_daily
            WHERE item_id = :item_id
            ORDER BY date
        """), {"item_id": item_id})
        return jsonify([dict(row) for row in result])
```

---

## Frontend

### Next.js 14
- **Framework:** Next.js 14+ with TypeScript
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **State Management:** React hooks + SWR

### Key Pages
- Dashboard: `/dashboard`
- Materials: `/materials`
- Material Detail: `/materials/[itemId]`
- Forecasts: `/forecasts`
- Recommendations: `/recommendations`

---

## ML Processing (Offline)

### Offline ML Pipeline
- **Location:** Separate environment
- **Entry Point:** `backend/ml_pipeline/main.py`
- **Models:** Prophet, ARIMA, LSTM, Ensemble
- **Output:** PostgreSQL tables (via ETL)

### ML Pipeline Flow
```python
# ml_pipeline/main.py
import pandas as pd
from prophet import Prophet
from sqlalchemy import create_engine

# Load data from PostgreSQL
engine = create_engine('postgresql://...')
df = pd.read_sql('SELECT * FROM core.fact_demand_daily', engine)

# Train model
model = Prophet()
model.fit(df)

# Generate forecast
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Load into PostgreSQL via ETL
# (See etl/load_ml_outputs.py)
```

---

## ETL Pipeline

### Load ML Outputs
- **Script:** `backend/etl/load_ml_outputs.py`
- **Purpose:** Load precomputed ML results into PostgreSQL
- **Input:** Parquet files from ML pipeline
- **Output:** PostgreSQL tables

### KPI Calculations
- **Script:** `backend/etl/calculate_kpis.sql`
- **Purpose:** Calculate business KPIs
- **Output:** Materialized views

---

## Authentication & Security

### JWT Authentication
- **Library:** python-jose
- **Token Type:** Bearer tokens
- **Expiration:** Configurable (default: 24 hours)

### Role-Based Access Control (RBAC)
- **Roles:**
  - `ADMIN`: Full access
  - `ANALYST`: Read/write analytics
  - `VIEWER`: Read-only access

### Audit Logging
- **Service:** `backend/services/audit_service.py`
- **Storage:** PostgreSQL `support.audit_logs` table
- **Events:** API calls, data changes, authentication

---

## Deployment

### Docker Compose (Production)
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: nova_corrente
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: nova_corrente
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://nova_corrente:${DB_PASSWORD}@postgres/nova_corrente
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

---

## Future Stack (Planned)

### Cloud Infrastructure
- **Storage:** AWS S3 + Delta Lake
- **Compute:** AWS ECS/EKS
- **Database:** AWS RDS PostgreSQL (managed)
- **Monitoring:** CloudWatch

### Data Engineering
- **Processing:** Spark + Databricks
- **Orchestration:** Airflow
- **Transformations:** dbt (data build tool)

### Analytics
- **BI Tools:** Metabase/Superset
- **Semantic Layer:** dbt Semantic Layer
- **Embed Analytics:** Integration in apps

---

## Performance Characteristics

- **Query Speed:** < 50ms for cached queries, < 200ms for database queries
- **Data Volume:** Handles millions of rows
- **Concurrency:** High (database-based)
- **Scalability:** Horizontal scaling with load balancer

---

## References

- [PROD Path Changelog](../../../CHANGELOG_PROD.md)
- [PROD Roadmaps](README_PROD_ROADMAPS.md)
- [Implementation Checklist](../../../IMPLEMENTATION_CHECKLIST.md)
- [PostgreSQL Specification](../../../proj/diagrams/Project.md)

---

**Document Created:** November 2025  
**Version:** 1.0  
**Status:** Complete Documentation

