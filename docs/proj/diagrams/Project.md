# Nova Corrente - Complete PostgreSQL Refactoring Specification
## Production-Ready Full-Stack Predictive Analytics Platform

**Version:** 3.0.0-postgres  
**Stack:** Next.js 14 + Flask 2.3+ + PostgreSQL 14+  
**Architecture:** Offline-first, Analytics-driven, Zero ML in Production  
**Last Updated:** 2025-11-05

---

## Executive Summary

This document specifies the complete refactoring of Nova Corrente from MySQL/SQLite to **PostgreSQL**, establishing a production-grade full-stack analytics platform for predictive supply-chain and inventory optimization.

**Core Principles:**
- ✅ **Offline-first**: All ML/predictive analytics precomputed offline; production only reads
- ✅ **PostgreSQL-native**: Leverage partitioning, JSONB, materialized views, and advanced indexing
- ✅ **API read-only**: Flask serves precomputed forecasts, features, KPIs, recommendations
- ✅ **Time-series focused**: Dashboard presents discrete, static time-series data (no streaming)
- ✅ **Future-proof**: JSONB + flexible schema accommodate evolving ML outputs
- ✅ **Cost-optimized**: Minimal infra, no external APIs in prod, no real-time training

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Strategic Data Modeling](#2-strategic-data-modeling)
3. [PostgreSQL Schema Design](#3-postgresql-schema-design)
4. [Flask API Specification](#4-flask-api-specification)
5. [Next.js Dashboard Design](#5-nextjs-dashboard-design)
6. [Data Pipeline & Integration](#6-data-pipeline--integration)
7. [Performance & Scalability](#7-performance--scalability)
8. [Security & Governance](#8-security--governance)
9. [Migration Strategy](#9-migration-strategy)
10. [Modern Libraries & Frameworks](#10-modern-libraries--frameworks)
11. [Implementation Roadmap](#11-implementation-roadmap)

---

## 1. Architecture Overview

---

## 1. Architecture Overview

### 1.1 Three-Tier Stack

```
┌─────────────────────────────────────────────┐
│         NEXT.JS FRONTEND (SSR/SPA)         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │Dashboard │ │Materials │ │Analytics │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       └────────────┼────────────┘          │
│                    │ HTTPS REST API        │
└────────────────────┼───────────────────────┘
                     │
┌────────────────────▼───────────────────────┐
│         FLASK API (Read-Only)              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  KPIs    │ │Forecasts │ │ Alerts   │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       └────────────┼────────────┘          │
│              SQLAlchemy + psycopg2         │
└────────────────────┼───────────────────────┘
                     │
┌────────────────────▼───────────────────────┐
│         POSTGRESQL 14+ (ACID)              │
│  ┌──────────────┐ ┌──────────────┐        │
│  │ Core Schema  │ │Analytics Sch.│        │
│  │ (Dimensions) │ │ (Precomputed)│        │
│  │ (Facts)      │ │ (Forecasts)  │        │
│  └──────────────┘ └──────────────┘        │
│  Partitioned | Indexed | Materialized     │
└────────────────────────────────────────────┘
```

### 1.2 Data Flow (Offline-First)

```
┌──────────────────────────────────────┐
│    ML ENVIRONMENT (Offline)          │
│  ┌────────────────────────────────┐  │
│  │  Training & Feature Eng.       │  │
│  │  - Prophet, ARIMA, LSTM        │  │
│  │  - Feature extraction          │  │
│  │  - Backtesting, validation     │  │
│  └───────────┬────────────────────┘  │
│              │ Export                │
│              ▼                        │
│  ┌────────────────────────────────┐  │
│  │  CSV/Parquet/JSON Outputs      │  │
│  │  - forecasts.parquet           │  │
│  │  - features.parquet            │  │
│  │  - kpis.csv                    │  │
│  └───────────┬────────────────────┘  │
└──────────────┼───────────────────────┘
               │ Load (COPY/INSERT)
               ▼
┌──────────────────────────────────────┐
│   POSTGRESQL (Production)            │
│   analytics.forecasts                │
│   analytics.features_store           │
│   analytics.kpis_daily               │
└──────────────┬───────────────────────┘
               │ Read-Only Queries
               ▼
┌──────────────────────────────────────┐
│   FLASK API → NEXT.JS DASHBOARD      │
└──────────────────────────────────────┘
```

### 1.3 Key Design Decisions

| **Aspect** | **Decision** | **Rationale** |
|------------|-------------|---------------|
| **Database** | PostgreSQL 14+ | Native partitioning, JSONB, materialized views, superior indexing |
| **Backend** | Flask 2.3+ (read-only) | Lightweight, mature, no need for async complexity; SQLAlchemy ORM |
| **Frontend** | Next.js 14 (SSR/CSR hybrid) | SEO-friendly, fast initial load, React ecosystem, built-in routing |
| **ML Strategy** | Offline precomputation | Zero prod complexity, cost savings, easier debugging, deterministic outputs |
| **API Pattern** | REST (JSON) | Simple, cacheable, wide client support, no WebSocket overhead |
| **Auth** | JWT + RBAC | Stateless, scalable, role-based access (admin/analyst/viewer) |
| **Caching** | Flask-Caching (simple) | Short TTL for KPIs/forecasts; invalidate on data refresh |
| **Deployment** | Docker Compose | Single-node prod initially; Kubernetes-ready if scaling needed |

---

## 2. Strategic Data Modeling

### 2.1 Business Context & Assumptions

**Supply Chain Dynamics (Industry Standards):**
- **ABC Classification**: A-items (20% SKUs, 80% revenue) require tightest control
- **Safety Stock**: `SS = Z × σ_LT × √LT` where Z=service level, σ=demand std, LT=lead time
- **Reorder Point**: `ROP = (Avg_Demand × LT) + SS`
- **Stockout Cost**: Revenue loss + expedite shipping + customer dissatisfaction
- **Inventory Turnover**: `COGS / Avg_Inventory` (target: 8-12× annually for electrical parts)

**Market Dynamics (Brazilian Context):**
- **Macroeconomic Volatility**: IPCA inflation, SELIC rates, USD/BRL exchange affect costs
- **Seasonality**: Carnival, holidays, construction cycles drive demand patterns
- **5G Expansion**: Telecommunications infrastructure growth impacts telecom parts demand
- **Regional Variation**: Northeast vs Southeast demand patterns differ significantly
- **Lead Time Variability**: Supplier reliability varies; imports face customs delays

**Business Problem Setup:**

**Primary Goal**: Minimize stockouts while optimizing inventory holding costs  
**Key Constraints**:
- No real-time ML in production (cost, complexity)
- No external API dependencies (reliability, rate limits)
- Dashboard must be **demonstrable** with static datasets initially

**Success Metrics (KPIs)**:
1. **Stockout Rate**: % of demand unfulfilled due to zero inventory
2. **Forecast Accuracy (MAPE)**: Mean Absolute Percentage Error < 15%
3. **Inventory Carrying Cost**: Reduction target 20-30%
4. **Delayed Orders**: % orders exceeding promised lead time
5. **ABC Coverage**: A-items stockout rate < 2%, B < 5%, C < 10%

### 2.2 Strategic Data Model Assumptions

**Before Full Dataset Availability**:

Since predictive/prescriptive datasets are pending teammate delivery, the schema **must be flexible**:

1. **JSONB for Unknown Features**:
   - `features_store.features` column holds arbitrary JSON
   - Allows ML team to add/remove features without schema migrations
   - Example: `{"lag_7d": 120.5, "rolling_mean_30d": 98.3, "holiday_effect": 1.2}`

2. **Partitioning for Scale**:
   - Fact tables partitioned by `full_date` (monthly partitions)
   - Enables fast time-range queries and partition pruning
   - Easy to drop old partitions for archival

3. **Nullable Foreign Keys Initially**:
   - `fact_demand_daily.supplier_id` nullable (not all orders have supplier yet)
   - Reconcile via nightly jobs when data quality improves

4. **Audit Trail for Data Lineage**:
   - `support.audit_logs` tracks all data loads, transformations, manual corrections
   - Critical for debugging forecast accuracy issues

5. **Materialized Views for Performance**:
   - `analytics.mv_kpis_latest` refreshed nightly
   - Dashboard queries hit MV, not raw facts (10-100× faster)

### 2.3 Relational Scaffolding (Star Schema)

**Why Star Schema?**
- Optimized for **OLAP** (analytical queries, not transactional)
- Denormalized dimensions enable fast joins
- Intuitive for business users ("slice by site, dice by ABC class")
- Compatible with BI tools (Metabase, Superset, Tableau)

**Scaffold Design**:

```
         ┌──────────────┐
         │ dim_calendar │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼───┐   ┌──▼────┐  ┌───▼──────┐
│dim_   │   │fact_  │  │fact_     │
│item   ├───┤demand │  │inventory │
└───────┘   │_daily │  │_daily    │
            └───┬───┘  └──────────┘
                │
    ┌───────────┼───────────┐
┌───▼──────┐ ┌─▼────────┐ ┌▼────────┐
│dim_site  │ │dim_      │ │dim_     │
│          │ │supplier  │ │region   │
└──────────┘ └──────────┘ └─────────┘
```

**Dimension Cardinality Estimates**:
- `dim_calendar`: ~1,100 rows (3 years of daily dates)
- `dim_item`: ~5,000-50,000 SKUs
- `dim_site`: ~10-100 locations
- `dim_supplier`: ~200-1,000 suppliers
- `dim_region`: ~30 (Brazilian states + economic zones)

**Fact Cardinality Estimates**:
- `fact_demand_daily`: ~500K-5M rows/month (items × sites × days)
- `fact_inventory_daily`: similar magnitude
- `analytics.forecasts`: ~100K-1M rows (items × horizons × dates)

---

## 3. PostgreSQL Schema Design

---

## 3. PostgreSQL Schema Design

### 3.1 Schema Organization

**Four Logical Schemas:**

1. **`core`** – Operational data (dimensions + facts)
2. **`analytics`** – Precomputed outputs (forecasts, features, KPIs)
3. **`support`** – Infrastructure (audit logs, notifications, user management)
4. **`staging`** – Temporary ETL workspace (truncated after loads)

### 3.2 Core Schema DDL

#### Dimensions

```sql
-- Schema creation
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS support;
CREATE SCHEMA IF NOT EXISTS staging;

-- Calendar Dimension (pre-populated)
CREATE TABLE core.dim_calendar (
  date_id SERIAL PRIMARY KEY,
  full_date DATE UNIQUE NOT NULL,
  year SMALLINT NOT NULL,
  month SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
  quarter SMALLINT NOT NULL CHECK (quarter BETWEEN 1 AND 4),
  weekday SMALLINT NOT NULL CHECK (weekday BETWEEN 0 AND 6),
  day_of_month SMALLINT NOT NULL,
  week_of_year SMALLINT NOT NULL,
  is_weekend BOOLEAN NOT NULL DEFAULT false,
  is_holiday BOOLEAN NOT NULL DEFAULT false,
  holiday_name TEXT,
  fiscal_year SMALLINT,
  fiscal_quarter SMALLINT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_dim_calendar_date ON core.dim_calendar(full_date);
CREATE INDEX ix_dim_calendar_year_month ON core.dim_calendar(year, month);

-- Item/Material Dimension
CREATE TABLE core.dim_item (
  item_id SERIAL PRIMARY KEY,
  sku TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  family TEXT,
  category TEXT,
  subcategory TEXT,
  unit_measure TEXT NOT NULL DEFAULT 'UN',
  abc_class CHAR(1) CHECK (abc_class IN ('A', 'B', 'C')),
  criticality SMALLINT CHECK (criticality BETWEEN 0 AND 10),
  active BOOLEAN NOT NULL DEFAULT true,
  min_order_qty NUMERIC(18,4),
  max_order_qty NUMERIC(18,4),
  extra_attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_dim_item_sku ON core.dim_item(sku);
CREATE INDEX ix_dim_item_family ON core.dim_item(family);
CREATE INDEX ix_dim_item_abc ON core.dim_item(abc_class);
CREATE INDEX gin_dim_item_attrs ON core.dim_item USING GIN (extra_attributes);

-- Site/Location Dimension
CREATE TABLE core.dim_region (
  region_id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  state_code CHAR(2),
  economic_zone TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE core.dim_site (
  site_id SERIAL PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  region_id INT REFERENCES core.dim_region(region_id),
  latitude NUMERIC(9,6),
  longitude NUMERIC(9,6),
  site_type TEXT CHECK (site_type IN ('WAREHOUSE', 'STORE', 'DISTRIBUTION_CENTER')),
  active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_dim_site_region ON core.dim_site(region_id);

-- Supplier Dimension
CREATE TABLE core.dim_supplier (
  supplier_id SERIAL PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  supplier_type TEXT CHECK (supplier_type IN ('DOMESTIC', 'IMPORT', 'HYBRID')),
  reliability_score NUMERIC(5,2) CHECK (reliability_score BETWEEN 0 AND 100),
  avg_lead_time_days INTEGER,
  on_time_delivery_rate NUMERIC(5,2),
  active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_dim_supplier_type ON core.dim_supplier(supplier_type);
```

#### Facts (Partitioned)

```sql
-- Demand Fact (partitioned by month)
CREATE TABLE core.fact_demand_daily (
  demand_id BIGSERIAL,
  full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
  item_id INT NOT NULL REFERENCES core.dim_item(item_id),
  site_id INT NOT NULL REFERENCES core.dim_site(site_id),
  supplier_id INT REFERENCES core.dim_supplier(supplier_id),
  quantity NUMERIC(18,4) NOT NULL CHECK (quantity >= 0),
  unit_cost NUMERIC(18,4),
  total_cost NUMERIC(18,4) GENERATED ALWAYS AS (quantity * unit_cost) STORED,
  lead_time_days INTEGER,
  extra_attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (demand_id, full_date)
) PARTITION BY RANGE (full_date);

-- Create monthly partitions (example: 2025)
CREATE TABLE core.fact_demand_daily_2025_01 PARTITION OF core.fact_demand_daily
  FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE core.fact_demand_daily_2025_02 PARTITION OF core.fact_demand_daily
  FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- ... (automate partition creation via cron/script)

CREATE INDEX ix_fact_demand_date ON core.fact_demand_daily(full_date);
CREATE INDEX ix_fact_demand_item ON core.fact_demand_daily(item_id);
CREATE INDEX ix_fact_demand_site ON core.fact_demand_daily(site_id);
CREATE INDEX ix_fact_demand_composite ON core.fact_demand_daily(item_id, site_id, full_date);

-- Inventory Fact (partitioned)
CREATE TABLE core.fact_inventory_daily (
  inventory_id BIGSERIAL,
  full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
  item_id INT NOT NULL REFERENCES core.dim_item(item_id),
  site_id INT NOT NULL REFERENCES core.dim_site(site_id),
  current_stock NUMERIC(18,4) NOT NULL,
  safety_stock NUMERIC(18,4),
  reorder_point NUMERIC(18,4),
  days_to_rupture INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (inventory_id, full_date)
) PARTITION BY RANGE (full_date);

-- Partitions similar to demand fact...

CREATE INDEX ix_fact_inventory_date ON core.fact_inventory_daily(full_date);
CREATE INDEX ix_fact_inventory_item_site ON core.fact_inventory_daily(item_id, site_id);

-- Orders Fact
CREATE TABLE core.fact_orders (
  order_id BIGSERIAL,
  order_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
  item_id INT NOT NULL REFERENCES core.dim_item(item_id),
  supplier_id INT NOT NULL REFERENCES core.dim_supplier(supplier_id),
  site_id INT NOT NULL REFERENCES core.dim_site(site_id),
  quantity NUMERIC(18,4) NOT NULL,
  unit_price NUMERIC(18,4),
  status TEXT NOT NULL CHECK (status IN ('PLACED', 'RECEIVED', 'CANCELLED', 'DELAYED')),
  expected_delivery_date DATE,
  actual_delivery_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (order_id, order_date)
) PARTITION BY RANGE (order_date);

CREATE INDEX ix_fact_orders_date ON core.fact_orders(order_date);
CREATE INDEX ix_fact_orders_status ON core.fact_orders(status);
```

### 3.3 Analytics Schema (Precomputed)

```sql
-- Forecasts Table
CREATE TABLE analytics.forecasts (
  forecast_id BIGSERIAL PRIMARY KEY,
  full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
  item_id INT NOT NULL REFERENCES core.dim_item(item_id),
  site_id INT NOT NULL REFERENCES core.dim_site(site_id),
  horizon_days SMALLINT NOT NULL CHECK (horizon_days > 0),
  yhat NUMERIC(18,4) NOT NULL,
  yhat_lower NUMERIC(18,4),
  yhat_upper NUMERIC(18,4),
  model_tag TEXT NOT NULL,
  confidence_level NUMERIC(5,2),
  computed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_forecasts_item_site_date ON analytics.forecasts(item_id, site_id, full_date);
CREATE INDEX ix_forecasts_horizon ON analytics.forecasts(horizon_days);
CREATE INDEX ix_forecasts_computed ON analytics.forecasts(computed_at);

-- Features Store (flexible JSONB)
CREATE TABLE analytics.features_store (
  feature_id BIGSERIAL PRIMARY KEY,
  full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
  item_id INT NOT NULL REFERENCES core.dim_item(item_id),
  site_id INT REFERENCES core.dim_site(site_id),
  features JSONB NOT NULL,
  schema_version TEXT NOT NULL DEFAULT 'v1.0',
  computed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_features_item_date ON analytics.features_store(item_id, full_date);
CREATE INDEX gin_features_jsonb ON analytics.features_store USING GIN (features);

-- KPIs Daily (aggregated metrics)
CREATE TABLE analytics.kpis_daily (
  kpi_id BIGSERIAL PRIMARY KEY,
  full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
  total_demand NUMERIC(18,4),
  stockout_rate NUMERIC(10,4),
  abc_a_share NUMERIC(10,4),
  delayed_orders_pct NUMERIC(10,4),
  forecast_mape NUMERIC(10,4),
  avg_inventory_value NUMERIC(18,2),
  computed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (full_date, computed_at)
);

CREATE INDEX ix_kpis_date ON analytics.kpis_daily(full_date DESC);

-- Recommendations Table
CREATE TABLE analytics.recommendations (
  recommendation_id BIGSERIAL PRIMARY KEY,
  item_id INT REFERENCES core.dim_item(item_id),
  site_id INT REFERENCES core.dim_site(site_id),
  type TEXT NOT NULL CHECK (type IN ('REORDER', 'PROMO', 'REALLOCATE', 'HOLD', 'EXPEDITE')),
  priority TEXT NOT NULL CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
  message TEXT NOT NULL,
  action_date DATE,
  quantity_recommended NUMERIC(18,4),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  acknowledged_at TIMESTAMP,
  acknowledged_by TEXT
);

CREATE INDEX ix_recommendations_priority ON analytics.recommendations(priority, created_at DESC);
CREATE INDEX ix_recommendations_item ON analytics.recommendations(item_id);

-- Alerts Table
CREATE TABLE analytics.alerts (
  alert_id BIGSERIAL PRIMARY KEY,
  item_id INT REFERENCES core.dim_item(item_id),
  site_id INT REFERENCES core.dim_site(site_id),
  level TEXT NOT NULL CHECK (level IN ('NORMAL', 'WARNING', 'CRITICAL')),
  category TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  read_at TIMESTAMP,
  resolved_at TIMESTAMP
);

CREATE INDEX ix_alerts_level_date ON analytics.alerts(level, created_at DESC);
CREATE INDEX ix_alerts_unread ON analytics.alerts(read_at) WHERE read_at IS NULL;
```

### 3.4 Support Schema

```sql
-- Audit Logs
CREATE TABLE support.audit_logs (
  audit_id BIGSERIAL PRIMARY KEY,
  actor TEXT NOT NULL,
  action TEXT NOT NULL,
  entity_type TEXT,
  entity_id BIGINT,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  ip_address INET,
  user_agent TEXT,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_audit_actor ON support.audit_logs(actor);
CREATE INDEX ix_audit_timestamp ON support.audit_logs(timestamp DESC);
CREATE INDEX gin_audit_details ON support.audit_logs USING GIN (details);

-- User Management (simple RBAC)
CREATE TABLE support.users (
  user_id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('ADMIN', 'ANALYST', 'VIEWER')),
  active BOOLEAN NOT NULL DEFAULT true,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_users_username ON support.users(username);
```

### 3.5 Materialized Views

```sql
-- Latest KPIs (for dashboard)
CREATE MATERIALIZED VIEW analytics.mv_kpis_latest AS
SELECT DISTINCT ON (full_date)
  full_date,
  total_demand,
  stockout_rate,
  abc_a_share,
  delayed_orders_pct,
  forecast_mape,
  avg_inventory_value,
  computed_at
FROM analytics.kpis_daily
ORDER BY full_date DESC, computed_at DESC
LIMIT 90; -- Last 90 days

CREATE UNIQUE INDEX ix_mv_kpis_date ON analytics.mv_kpis_latest(full_date DESC);

-- Latest Forecasts (per item/site/horizon)
CREATE MATERIALIZED VIEW analytics.mv_forecasts_latest AS
SELECT DISTINCT ON (item_id, site_id, horizon_days, full_date)
  forecast_id,
  full_date,
  item_id,
  site_id,
  horizon_days,
  yhat,
  yhat_lower,
  yhat_upper,
  model_tag,
  computed_at
FROM analytics.forecasts
ORDER BY item_id, site_id, horizon_days, full_date DESC, computed_at DESC;

CREATE INDEX ix_mv_forecasts_item_site ON analytics.mv_forecasts_latest(item_id, site_id);

-- Refresh strategy (via cron or manual):
-- REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.mv_kpis_latest;
-- REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.mv_forecasts_latest;
```

---

## 4. Flask API Specification

---

## 4. Flask API Specification

### 4.1 API Design Principles

- **Read-Only in Production**: Zero writes; all mutations happen offline
- **RESTful JSON**: Standard HTTP verbs, predictable URLs
- **Pagination**: `limit`/`offset` query params; return total_count in metadata
- **Filtering**: Query params for common filters (date ranges, IDs, priorities)
- **Caching**: Flask-Caching with 5-minute TTL for KPIs, 1-hour for forecasts
- **Error Handling**: Consistent JSON error format `{"error": "...", "detail": "..."}`
- **Versioning**: `/api/v1/` prefix; future v2 isolated

### 4.2 Endpoint Catalog

#### Health & Metadata

```python
GET /health
Response: {
  "status": "healthy" | "degraded",
  "database": "connected" | "disconnected",
  "timestamp": "2025-11-05T10:30:00Z",
  "version": "3.0.0"
}
```

#### KPIs

```python
GET /api/v1/analytics/kpis?start_date=2025-01-01&end_date=2025-01-31
Response: {
  "status": "success",
  "data": [
    {
      "full_date": "2025-01-15",
      "total_demand": 12500.5,
      "stockout_rate": 0.03,
      "abc_a_share": 0.82,
      "delayed_orders_pct": 0.05,
      "forecast_mape": 0.12,
      "computed_at": "2025-01-15T02:00:00Z"
    }
  ],
  "metadata": {
    "total_count": 31,
    "page": 1,
    "limit": 100
  }
}
```

#### Items/Materials

```python
GET /api/v1/items?family=ELECTRICAL&abc_class=A&limit=50&offset=0
Response: {
  "status": "success",
  "data": [
    {
      "item_id": 123,
      "sku": "ELE-12345",
      "name": "Conector 10mm",
      "family": "ELECTRICAL",
      "abc_class": "A",
      "criticality": 9
    }
  ],
  "metadata": {"total_count": 450}
}

GET /api/v1/items/{item_id}
Response: {
  "item_id": 123,
  "sku": "ELE-12345",
  "name": "Conector 10mm",
  "family": "ELECTRICAL",
  "category": "CONNECTORS",
  "abc_class": "A",
  "criticality": 9,
  "unit_measure": "UN",
  "extra_attributes": {"voltage_rating": "220V"}
}
```

#### Demand Time Series

```python
GET /api/v1/demand/timeseries?item_id=123&site_id=5&start_date=2024-01-01&end_date=2024-12-31
Response: {
  "status": "success",
  "data": [
    {"full_date": "2024-01-01", "quantity": 120.5},
    {"full_date": "2024-01-02", "quantity": 98.3}
  ],
  "metadata": {"item_id": 123, "site_id": 5}
}
```

#### Inventory Time Series

```python
GET /api/v1/inventory/timeseries?item_id=123&site_id=5&start_date=2024-01-01
Response: {
  "status": "success",
  "data": [
    {
      "full_date": "2024-01-01",
      "current_stock": 500.0,
      "safety_stock": 150.0,
      "reorder_point": 200.0,
      "days_to_rupture": 12
    }
  ]
}
```

#### Forecasts

```python
GET /api/v1/forecasts?item_id=123&site_id=5&horizon=30&start_date=2025-02-01
Response: {
  "status": "success",
  "data": [
    {
      "full_date": "2025-02-01",
      "yhat": 105.2,
      "yhat_lower": 92.1,
      "yhat_upper": 118.3,
      "model_tag": "prophet_v2.1",
      "horizon_days": 30
    }
  ],
  "metadata": {"computed_at": "2025-01-15T02:00:00Z"}
}
```

#### Features

```python
GET /api/v1/features?item_id=123&start_date=2024-01-01&end_date=2024-01-31
Response: {
  "status": "success",
  "data": [
    {
      "full_date": "2024-01-01",
      "features": {
        "lag_7d": 120.5,
        "rolling_mean_30d": 98.3,
        "holiday_effect": 1.2,
        "ipca_rate": 0.04,
        "selic_rate": 0.11
      },
      "schema_version": "v1.0"
    }
  ]
}
```

#### Recommendations

```python
GET /api/v1/recommendations?priority=CRITICAL&site_id=5&limit=20
Response: {
  "status": "success",
  "data": [
    {
      "recommendation_id": 456,
      "item_id": 123,
      "site_id": 5,
      "type": "REORDER",
      "priority": "CRITICAL",
      "message": "Stock below safety level. Reorder 500 units immediately.",
      "quantity_recommended": 500.0,
      "created_at": "2025-01-15T08:00:00Z"
    }
  ]
}

PATCH /api/v1/recommendations/{id}/acknowledge
Payload: {"acknowledged_by": "user@example.com"}
Response: {"status": "success"}
```

#### Alerts

```python
GET /api/v1/alerts?level=CRITICAL&unread=true
Response: {
  "status": "success",
  "data": [
    {
      "alert_id": 789,
      "item_id": 123,
      "site_id": 5,
      "level": "CRITICAL",
      "category": "STOCKOUT_IMMINENT",
      "message": "Item ELE-12345 will stock out in 2 days",
      "created_at": "2025-01-15T10:00:00Z",
      "read_at": null
    }
  ]
}

PATCH /api/v1/alerts/{id}/mark-read
Response: {"status": "success"}
```

### 4.3 Flask Implementation Pattern

```python
# backend/api/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))

# Cache configuration
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300})

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/nova_corrente')
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine)

@app.route('/health', methods=['GET'])
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'version': '3.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'degraded',
            'database': 'disconnected',
            'error': str(e)
        }), 503

@app.route('/api/v1/analytics/kpis', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_kpis():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = text("""
        SELECT full_date, total_demand, stockout_rate, abc_a_share, 
               delayed_orders_pct, forecast_mape, computed_at
        FROM analytics.kpis_daily
        WHERE full_date BETWEEN :start_date AND :end_date
        ORDER BY full_date DESC
    """)
    
    with SessionLocal() as session:
        result = session.execute(query, {'start_date': start_date, 'end_date': end_date})
        data = [dict(row._mapping) for row in result]
    
    return jsonify({
        'status': 'success',
        'data': data,
        'metadata': {'total_count': len(data)}
    })

# ... (similar patterns for other endpoints)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

---

## 5. Next.js Dashboard Design

---

## 5. Next.js Dashboard Design

### 5.1 Page Structure

```
/
├── /dashboard          → Executive KPIs + trends
├── /materials          → Item catalog with filters
│   └── /[itemId]       → Item detail (demand, inventory, forecasts)
├── /forecasts          → Forecast explorer (multi-item comparison)
├── /inventory          → Inventory health dashboard
├── /recommendations    → Prescriptive actions queue
├── /alerts             → Alert inbox
└── /admin              → Audit logs, user management
```

### 5.2 Dashboard Page (`/dashboard`)

**Layout:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     Nova Corrente - Supply Chain Analytics     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Stockout Rate   │ │ Forecast MAPE   │ │ Delayed Orders  │
│                 │ │                 │ │                 │
│   3.2% ▼ 0.5%  │ │   12.1% ▲ 1.2% │ │   4.8% ▼ 0.8% │
└────────────────┘ └────────────────┘ └────────────────┘

┌───────────────────────────────────────────────────────────┐
│  Demand Trend (Last 90 Days)                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │        Line Chart (Recharts)                   │  │
│  │  Actual vs Forecast                            │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘

┌────────────────────────────┐ ┌────────────────────────────┐
│ Top Alerts               │ │ Critical Recommendations │
│  • ELE-123: 2 days left  │ │  • Reorder 500 units    │
│  • TEL-456: Low stock    │ │  • Expedite TEL-789     │
└────────────────────────────┘ └────────────────────────────┘
```

**Components:**

```typescript
// app/dashboard/page.tsx
import { KPICard } from '@/components/KPICard';
import { DemandTrendChart } from '@/components/charts/DemandTrendChart';
import { AlertList } from '@/components/AlertList';
import { apiClient } from '@/lib/api';

export default async function DashboardPage() {
  const kpis = await apiClient.getKpis();
  const alerts = await apiClient.getAlerts({ level: 'CRITICAL', limit: 5 });
  
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      {/* KPI Cards */}
      <div className="grid grid-cols-3 gap-4">
        <KPICard 
          title="Stockout Rate"
          value={kpis.stockout_rate}
          change={-0.5}
          format="percentage"
        />
        <KPICard 
          title="Forecast MAPE"
          value={kpis.forecast_mape}
          change={1.2}
          format="percentage"
        />
        <KPICard 
          title="Delayed Orders"
          value={kpis.delayed_orders_pct}
          change={-0.8}
          format="percentage"
        />
      </div>
      
      {/* Demand Trend Chart */}
      <DemandTrendChart data={kpis.trend_data} />
      
      {/* Alerts & Recommendations */}
      <div className="grid grid-cols-2 gap-4">
        <AlertList alerts={alerts} />
        <RecommendationsList />
      </div>
    </div>
  );
}
```

### 5.3 Material Detail Page (`/materials/[itemId]`)

**Tabs:**

1. **Overview**: ABC class, criticality, description
2. **Demand History**: Time series line chart (actual vs forecast)
3. **Inventory Levels**: Stock, safety stock, reorder point over time
4. **Forecasts**: 30/60/90-day horizons with confidence intervals
5. **Features**: JSONB feature vector (collapsible table)

```typescript
// app/materials/[itemId]/page.tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { DemandChart } from '@/components/charts/DemandChart';
import { InventoryChart } from '@/components/charts/InventoryChart';
import { ForecastChart } from '@/components/charts/ForecastChart';

export default async function MaterialDetailPage({ params }: { params: { itemId: string } }) {
  const item = await apiClient.getItem(params.itemId);
  const demandData = await apiClient.getDemandTimeSeries(params.itemId);
  const forecastData = await apiClient.getForecasts(params.itemId, { horizon: 30 });
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">{item.name} ({item.sku})</h1>
      <p className="text-gray-600">ABC: {item.abc_class} | Criticality: {item.criticality}/10</p>
      
      <Tabs defaultValue="demand" className="mt-6">
        <TabsList>
          <TabsTrigger value="demand">Demand</TabsTrigger>
          <TabsTrigger value="inventory">Inventory</TabsTrigger>
          <TabsTrigger value="forecasts">Forecasts</TabsTrigger>
          <TabsTrigger value="features">Features</TabsTrigger>
        </TabsList>
        
        <TabsContent value="demand">
          <DemandChart data={demandData} />
        </TabsContent>
        
        <TabsContent value="forecasts">
          <ForecastChart data={forecastData} />
        </TabsContent>
        
        {/* ... other tabs */}
      </Tabs>
    </div>
  );
}
```

### 5.4 Chart Components (Recharts)

```typescript
// components/charts/DemandChart.tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DemandChartProps {
  data: { full_date: string; quantity: number }[];
}

export function DemandChart({ data }: DemandChartProps) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="full_date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="quantity" stroke="#8884d8" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

```typescript
// components/charts/ForecastChart.tsx (with confidence intervals)
import { LineChart, Line, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ForecastChartProps {
  data: { full_date: string; yhat: number; yhat_lower: number; yhat_upper: number }[];
}

export function ForecastChart({ data }: ForecastChartProps) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="full_date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Area 
          type="monotone" 
          dataKey="yhat_upper" 
          fill="#8884d8" 
          fillOpacity={0.2} 
          stroke="none" 
        />
        <Area 
          type="monotone" 
          dataKey="yhat_lower" 
          fill="#8884d8" 
          fillOpacity={0.2} 
          stroke="none" 
        />
        <Line 
          type="monotone" 
          dataKey="yhat" 
          stroke="#8884d8" 
          strokeWidth={2} 
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### 5.5 Data Fetching Strategy

**Hybrid Approach:**

- **Server Components** (getServerSideProps): Initial page load for SEO, fast FCP
- **Client Components** (SWR/TanStack Query): Interactive filters, real-time updates

```typescript
// lib/api.ts (enhanced with SWR)
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(res => res.json());

export function useKPIs(startDate?: string, endDate?: string) {
  const params = new URLSearchParams();
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  
  const { data, error, isLoading } = useSWR(
    `/api/v1/analytics/kpis?${params.toString()}`,
    fetcher,
    { refreshInterval: 60000 } // Refresh every 60s
  );
  
  return { kpis: data, error, isLoading };
}

export function useForecasts(itemId: number, horizon: number) {
  const { data, error, isLoading } = useSWR(
    `/api/v1/forecasts?item_id=${itemId}&horizon=${horizon}`,
    fetcher,
    { revalidateOnFocus: false } // Don't refetch on focus
  );
  
  return { forecasts: data, error, isLoading };
}
```

---

## 6. Data Pipeline & Integration

---

## 6. Data Pipeline & Integration

### 6.1 Offline ML Pipeline (Development Environment)

```python
# ml_pipeline/main.py (runs locally, not in production)
import pandas as pd
import numpy as np
from prophet import Prophet
from sqlalchemy import create_engine
import json

# 1. Extract: Read historical demand from PostgreSQL
engine = create_engine('postgresql://user:pass@localhost:5432/nova_corrente')
df = pd.read_sql("""
    SELECT 
        d.full_date,
        i.item_id,
        i.sku,
        s.site_id,
        SUM(f.quantity) AS quantity
    FROM core.fact_demand_daily f
    JOIN core.dim_item i ON f.item_id = i.item_id
    JOIN core.dim_site s ON f.site_id = s.site_id
    JOIN core.dim_calendar d ON f.full_date = d.full_date
    WHERE d.full_date >= '2024-01-01'
    GROUP BY d.full_date, i.item_id, i.sku, s.site_id
    ORDER BY d.full_date
""", engine)

# 2. Feature Engineering
features = []
for (item_id, site_id), group in df.groupby(['item_id', 'site_id']):
    group = group.sort_values('full_date')
    group['lag_7d'] = group['quantity'].shift(7)
    group['rolling_mean_30d'] = group['quantity'].rolling(30).mean()
    # Add IPCA, SELIC, etc. from dim_market_indicator joins...
    
    features.append(group)

features_df = pd.concat(features)

# 3. Training: Forecast with Prophet (per item/site)
forecasts = []
for (item_id, site_id), group in df.groupby(['item_id', 'site_id']):
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    train_df = group.rename(columns={'full_date': 'ds', 'quantity': 'y'})
    model.fit(train_df)
    
    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)
    
    # Save forecasts for horizons 7, 30, 60, 90 days
    for horizon in [7, 30, 60, 90]:
        horizon_forecast = forecast[forecast['ds'] <= pd.Timestamp.now() + pd.Timedelta(days=horizon)]
        for _, row in horizon_forecast.iterrows():
            forecasts.append({
                'full_date': row['ds'].date(),
                'item_id': item_id,
                'site_id': site_id,
                'horizon_days': horizon,
                'yhat': row['yhat'],
                'yhat_lower': row['yhat_lower'],
                'yhat_upper': row['yhat_upper'],
                'model_tag': 'prophet_v2.1',
                'computed_at': pd.Timestamp.now()
            })

forecast_df = pd.DataFrame(forecasts)

# 4. Export: Save to Parquet
forecast_df.to_parquet('./output/forecasts.parquet', index=False)
features_df.to_parquet('./output/features.parquet', index=False)

print(f"Exported {len(forecast_df)} forecast rows, {len(features_df)} feature rows")
```

### 6.2 Loading Precomputed Data into PostgreSQL

```python
# etl/load_ml_outputs.py (runs on-demand or via cron)
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine('postgresql://user:pass@localhost:5432/nova_corrente')

# 1. Load forecasts from Parquet
forecasts = pd.read_parquet('./output/forecasts.parquet')

# Truncate old forecasts (optional: keep history)
with engine.connect() as conn:
    conn.execute("TRUNCATE TABLE analytics.forecasts;")
    conn.commit()

# Bulk insert via COPY (fastest method)
forecasts.to_sql('forecasts', engine, schema='analytics', if_exists='append', index=False, method='multi', chunksize=10000)

print(f"Loaded {len(forecasts)} forecasts into PostgreSQL")

# 2. Load features (JSONB transformation)
features_raw = pd.read_parquet('./output/features.parquet')

features_json = []
for _, row in features_raw.iterrows():
    features_json.append({
        'full_date': row['full_date'],
        'item_id': row['item_id'],
        'site_id': row['site_id'],
        'features': json.dumps({
            'lag_7d': row['lag_7d'],
            'rolling_mean_30d': row['rolling_mean_30d'],
            # ... other features
        }),
        'schema_version': 'v1.0',
        'computed_at': datetime.now()
    })

features_df = pd.DataFrame(features_json)
features_df.to_sql('features_store', engine, schema='analytics', if_exists='append', index=False)

print(f"Loaded {len(features_df)} feature rows")

# 3. Refresh materialized views
with engine.connect() as conn:
    conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.mv_forecasts_latest;")
    conn.commit()

print("Materialized views refreshed")
```

### 6.3 KPI Calculation (Nightly Job)

```sql
-- etl/calculate_kpis.sql (scheduled via cron or Airflow)
INSERT INTO analytics.kpis_daily (
  full_date,
  total_demand,
  stockout_rate,
  abc_a_share,
  delayed_orders_pct,
  forecast_mape,
  avg_inventory_value,
  computed_at
)
SELECT
  d.full_date,
  COALESCE(SUM(f.quantity), 0) AS total_demand,
  
  -- Stockout rate: % of items with zero inventory
  (SELECT COUNT(DISTINCT item_id)::NUMERIC / NULLIF((SELECT COUNT(*) FROM core.dim_item WHERE active = true), 0)
   FROM core.fact_inventory_daily
   WHERE full_date = d.full_date AND current_stock = 0) AS stockout_rate,
  
  -- ABC A-class share of total demand
  (SELECT SUM(f2.quantity) FROM core.fact_demand_daily f2
   JOIN core.dim_item i2 ON f2.item_id = i2.item_id
   WHERE f2.full_date = d.full_date AND i2.abc_class = 'A') / NULLIF(SUM(f.quantity), 0) AS abc_a_share,
  
  -- Delayed orders: % orders past expected delivery
  (SELECT COUNT(*)::NUMERIC / NULLIF(COUNT(*), 0)
   FROM core.fact_orders
   WHERE order_date = d.full_date 
     AND status = 'DELAYED') AS delayed_orders_pct,
  
  -- Forecast MAPE (placeholder: calculate from actuals vs forecasts)
  NULL AS forecast_mape,
  
  -- Avg inventory value
  (SELECT AVG(current_stock * i.unit_cost)
   FROM core.fact_inventory_daily inv
   JOIN core.dim_item i ON inv.item_id = i.item_id
   WHERE inv.full_date = d.full_date) AS avg_inventory_value,
  
  CURRENT_TIMESTAMP AS computed_at
  
FROM core.dim_calendar d
LEFT JOIN core.fact_demand_daily f ON d.full_date = f.full_date
WHERE d.full_date = CURRENT_DATE - INTERVAL '1 day' -- Yesterday's KPIs
GROUP BY d.full_date
ON CONFLICT (full_date, computed_at) DO NOTHING;
```

### 6.4 Data Flow Diagram

```
[ML Environment]             [PostgreSQL Production]
       |                              |
   Training → Forecasts.parquet  →  COPY INTO analytics.forecasts
       |                              |
  Feature Eng → Features.parquet →  INSERT INTO analytics.features_store
       |                              |
   Validation                    REFRESH MV
                                     |
                              [Flask API] → [Next.js]
```

---

## 7. Performance & Scalability

### 7.1 Indexing Strategy

**Fact Tables:**

- **Partition Pruning**: Monthly partitions enable PostgreSQL to skip irrelevant partitions
- **B-Tree Indexes**: On FKs (item_id, site_id, supplier_id), date columns
- **Composite Indexes**: `(item_id, site_id, full_date)` for typical query patterns

**Analytics Tables:**

- **GIN Indexes**: On JSONB columns (`features_store.features`) for fast JSON key lookups
- **Partial Indexes**: `CREATE INDEX ... WHERE read_at IS NULL` for unread alerts (faster)
- **Covering Indexes**: Include commonly selected columns to avoid heap lookups

**Example Queries with Index Usage:**

```sql
-- Query: Get demand for item 123 at site 5 in Jan 2025
EXPLAIN ANALYZE
SELECT full_date, quantity
FROM core.fact_demand_daily
WHERE item_id = 123 
  AND site_id = 5 
  AND full_date BETWEEN '2025-01-01' AND '2025-01-31';

-- Uses: ix_fact_demand_composite (item_id, site_id, full_date)
-- Partition pruning: Only scans fact_demand_daily_2025_01
```

### 7.2 Caching Layers

**1. Flask-Caching (Application Layer)**

```python
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300})

@app.route('/api/v1/analytics/kpis')
@cache.cached(timeout=300, query_string=True) # 5min TTL
def get_kpis():
    # Cached per unique query string
    pass
```

**2. PostgreSQL Query Cache (Connection Pooling)**

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # Max concurrent connections
    max_overflow=20,       # Burst capacity
    pool_recycle=3600      # Recycle connections hourly
)
```

**3. Materialized Views (Database Layer)**

- Refresh nightly via cron:
  ```bash
  0 2 * * * psql -d nova_corrente -c "REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.mv_kpis_latest;"
  ```

### 7.3 Query Optimization Examples

**Slow Query (N+1):**

```sql
-- BAD: Fetches items one-by-one
FOR item IN (SELECT item_id FROM dim_item WHERE abc_class = 'A') LOOP
  SELECT AVG(quantity) FROM fact_demand_daily WHERE item_id = item.item_id;
END LOOP;
```

**Optimized (Single Query):**

```sql
-- GOOD: Single query with JOIN and GROUP BY
SELECT 
  i.item_id,
  i.sku,
  AVG(f.quantity) AS avg_demand
FROM core.dim_item i
JOIN core.fact_demand_daily f ON i.item_id = f.item_id
WHERE i.abc_class = 'A'
GROUP BY i.item_id, i.sku;
```

### 7.4 Scaling Strategy

**Phase 1: Single-Node (Current)**

- Docker Compose: Postgres + Flask + Next.js on one VM
- Suitable for: 10K-100K items, 1M-10M fact rows/month

**Phase 2: Vertical Scaling**

- Upgrade PostgreSQL instance (more CPU, RAM, faster SSD)
- Enable PostgreSQL read replicas for Flask read queries

**Phase 3: Horizontal Scaling (If Needed)**

- **Database**: Citus extension for sharding by `item_id`
- **API**: Multiple Flask instances behind Nginx load balancer
- **Frontend**: Next.js on Vercel/Netlify (CDN)

---

## 8. Security & Governance

### 8.1 Authentication & Authorization

**JWT Flow:**

```
User → POST /api/v1/auth/login {username, password}
      ← {access_token, expires_in}

User → GET /api/v1/items (Header: Authorization: Bearer <token>)
      ← {data: [...]}
```

**Implementation:**

```python
# backend/auth.py
from flask import request, jsonify
from functools import wraps
import jwt
import datetime

SECRET_KEY = os.getenv('SECRET_KEY', 'change-in-prod')

def create_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(roles=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                if roles and payload['role'] not in roles:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                return f(payload, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
        return wrapper
    return decorator

@app.route('/api/v1/items', methods=['GET'])
@token_required(roles=['ADMIN', 'ANALYST', 'VIEWER'])
def get_items(payload):
    # payload contains user_id, role
    pass
```

### 8.2 RBAC Matrix

| **Endpoint** | **ADMIN** | **ANALYST** | **VIEWER** |
|--------------|-----------|-------------|------------|
| GET /items   | ✓         | ✓           | ✓          |
| GET /forecasts | ✓       | ✓           | ✓          |
| PATCH /recommendations/:id/acknowledge | ✓ | ✓ | ✗ |
| POST /admin/users | ✓      | ✗           | ✗          |
| GET /admin/audit-logs | ✓    | ✗           | ✗          |

### 8.3 Audit Logging

```python
def log_audit(actor, action, entity_type, entity_id, details):
    with SessionLocal() as session:
        session.execute(text("""
            INSERT INTO support.audit_logs (actor, action, entity_type, entity_id, details, ip_address, timestamp)
            VALUES (:actor, :action, :entity_type, :entity_id, :details, :ip, NOW())
        """), {
            'actor': actor,
            'action': action,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'details': json.dumps(details),
            'ip': request.remote_addr
        })
        session.commit()

@app.route('/api/v1/recommendations/<int:id>/acknowledge', methods=['PATCH'])
@token_required(roles=['ADMIN', 'ANALYST'])
def acknowledge_recommendation(payload, id):
    # ... update recommendation ...
    log_audit(
        actor=payload['user_id'],
        action='ACKNOWLEDGE_RECOMMENDATION',
        entity_type='recommendation',
        entity_id=id,
        details={'acknowledged_at': datetime.utcnow().isoformat()}
    )
    return jsonify({'status': 'success'})
```

---

## 9. Migration Strategy

---

## 9. Migration Strategy

### 9.1 Phase 1: PostgreSQL Setup (Week 1)

**Tasks:**

1. **Install PostgreSQL 14+**
   ```bash
   # Docker (recommended for dev)
   docker run --name postgres-nova-corrente \
     -e POSTGRES_USER=nova_corrente \
     -e POSTGRES_PASSWORD=strong_password \
     -e POSTGRES_DB=nova_corrente \
     -p 5432:5432 \
     -v pgdata:/var/lib/postgresql/data \
     -d postgres:14
   ```

2. **Initialize Alembic**
   ```bash
   cd backend
   pip install alembic psycopg2-binary
   alembic init alembic
   ```

3. **Configure Database Connection**
   - Update `backend/.env`:
     ```ini
     DATABASE_URL=postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente
     DB_HOST=localhost
     DB_PORT=5432
     DB_USER=nova_corrente
     DB_PASSWORD=strong_password
     DB_NAME=nova_corrente
     ```

4. **Create Initial Migration (Schema Creation)**
   ```bash
   alembic revision -m "initial_schema_core_analytics_support"
   ```
   
   Edit migration file:
   ```python
   # alembic/versions/001_initial_schema.py
   def upgrade():
       # Create schemas
       op.execute('CREATE SCHEMA IF NOT EXISTS core')
       op.execute('CREATE SCHEMA IF NOT EXISTS analytics')
       op.execute('CREATE SCHEMA IF NOT EXISTS support')
       op.execute('CREATE SCHEMA IF NOT EXISTS staging')
       
       # Create dimensions (dim_calendar, dim_item, dim_site, etc.)
       # ... (use DDL from Section 3.2)
       
       # Create facts with partitions
       # ... (use DDL from Section 3.2)
       
       # Create analytics tables
       # ... (use DDL from Section 3.3)
       
       # Create support tables
       # ... (use DDL from Section 3.4)
       
       # Create indexes
       # ... (all CREATE INDEX statements)
   
   def downgrade():
       op.execute('DROP SCHEMA core CASCADE')
       op.execute('DROP SCHEMA analytics CASCADE')
       op.execute('DROP SCHEMA support CASCADE')
       op.execute('DROP SCHEMA staging CASCADE')
   ```

5. **Apply Migration**
   ```bash
   alembic upgrade head
   ```

6. **Verify Schema**
   ```sql
   \dt core.*
   \dt analytics.*
   \d+ core.fact_demand_daily
   ```

### 9.2 Phase 2: Backend Refactor (Week 2)

**Tasks:**

1. **Update Database Config**
   
   `backend/config/database_config.py`:
   ```python
   DATABASE_CONFIG: Dict[str, Any] = {
       'host': os.getenv('DB_HOST', 'localhost'),
       'port': int(os.getenv('DB_PORT', 5432)),  # Changed from 3306
       'user': os.getenv('DB_USER', 'nova_corrente'),
       'password': os.getenv('DB_PASSWORD', ''),
       'database': os.getenv('DB_NAME', 'nova_corrente'),
       'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
       'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20)),
       'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30)),
       'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
       'echo': os.getenv('DB_ECHO', 'False').lower() == 'true',
   }
   
   # PostgreSQL connection string
   SQLALCHEMY_DATABASE_URI = (
       f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
       f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
   )
   ```

2. **Update Main Config**
   
   `backend/app/config.py`:
   ```python
   class Settings(BaseSettings):
       # ...
       DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://nova_corrente:pass@localhost:5432/nova_corrente")
       # ...
   ```

3. **Create Flask API Endpoints**
   
   Create new file: `backend/api/v1/routes.py`
   ```python
   from flask import Blueprint, jsonify, request
   from backend.services.database_service import DatabaseService
   
   api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
   db = DatabaseService()
   
   @api_v1.route('/items', methods=['GET'])
   def get_items():
       limit = request.args.get('limit', 100, type=int)
       offset = request.args.get('offset', 0, type=int)
       
       query = """
           SELECT item_id, sku, name, family, category, abc_class, criticality
           FROM core.dim_item
           WHERE active = true
           ORDER BY item_id
           LIMIT :limit OFFSET :offset
       """
       
       items = db.execute_query(query, {'limit': limit, 'offset': offset})
       return jsonify({'status': 'success', 'data': items})
   
   # ... (implement all endpoints from Section 4.2)
   ```

4. **Register Blueprint in Main App**
   ```python
   # backend/api/enhanced_api.py
   from backend.api.v1.routes import api_v1
   
   app.register_blueprint(api_v1)
   ```

5. **Add Feature Flags**
   ```python
   # Disable external APIs and ML in production
   EXTERNAL_APIS_ENABLED = os.getenv('EXTERNAL_APIS_ENABLED', 'false').lower() == 'true'
   ENABLE_ML_PROCESSING = os.getenv('ENABLE_ML_PROCESSING', 'false').lower() == 'true'
   ```

### 9.3 Phase 3: Data Migration (Week 3)

**Option A: If MySQL data exists**

```python
# scripts/migrate_mysql_to_postgres.py
import pandas as pd
from sqlalchemy import create_engine

mysql_engine = create_engine('mysql+pymysql://root@localhost:3306/STOCK')
postgres_engine = create_engine('postgresql://nova_corrente:pass@localhost:5432/nova_corrente')

# Migrate dimensions
for table in ['dim_item', 'dim_site', 'dim_supplier', 'dim_region']:
    df = pd.read_sql(f"SELECT * FROM {table}", mysql_engine)
    df.to_sql(table, postgres_engine, schema='core', if_exists='append', index=False)
    print(f"Migrated {len(df)} rows from {table}")

# Migrate facts (with partitioning)
for year in [2024, 2025]:
    for month in range(1, 13):
        df = pd.read_sql(f"""
            SELECT * FROM fact_demand_daily
            WHERE YEAR(full_date) = {year} AND MONTH(full_date) = {month}
        """, mysql_engine)
        
        if not df.empty:
            df.to_sql('fact_demand_daily', postgres_engine, schema='core', if_exists='append', index=False)
            print(f"Migrated {len(df)} rows for {year}-{month:02d}")
```

**Option B: If starting fresh (synthetic data for demo)**

```python
# scripts/generate_demo_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine

engine = create_engine('postgresql://nova_corrente:pass@localhost:5432/nova_corrente')

# 1. Generate calendar dimension (3 years)
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
dates = pd.date_range(start_date, end_date, freq='D')

calendar = pd.DataFrame({
    'full_date': dates,
    'year': dates.year,
    'month': dates.month,
    'quarter': dates.quarter,
    'weekday': dates.weekday,
    'day_of_month': dates.day,
    'week_of_year': dates.isocalendar().week,
    'is_weekend': dates.weekday >= 5,
    'is_holiday': False  # Can enhance with holidays library
})

calendar.to_sql('dim_calendar', engine, schema='core', if_exists='append', index=False)
print(f"Generated {len(calendar)} calendar dates")

# 2. Generate items (500 SKUs)
items = pd.DataFrame({
    'sku': [f"ITEM-{i:05d}" for i in range(1, 501)],
    'name': [f"Product {i}" for i in range(1, 501)],
    'family': np.random.choice(['ELECTRICAL', 'TELECOM', 'HARDWARE'], 500),
    'abc_class': np.random.choice(['A', 'B', 'C'], 500, p=[0.2, 0.3, 0.5]),
    'criticality': np.random.randint(1, 11, 500),
    'unit_measure': 'UN',
    'active': True
})

items.to_sql('dim_item', engine, schema='core', if_exists='append', index=False)
print(f"Generated {len(items)} items")

# 3. Generate demand facts (last 90 days, 500 items × 5 sites = 225K rows)
site_ids = [1, 2, 3, 4, 5]  # Assume sites already exist
item_ids = range(1, 501)
last_90_days = pd.date_range(datetime.now() - timedelta(days=90), datetime.now(), freq='D')

demand_rows = []
for date in last_90_days:
    for item_id in item_ids:
        for site_id in site_ids:
            # Simulate demand with seasonality + noise
            base_demand = 50 + 20 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365)
            demand = max(0, base_demand + np.random.normal(0, 10))
            
            demand_rows.append({
                'full_date': date.date(),
                'item_id': item_id,
                'site_id': site_id,
                'quantity': round(demand, 2),
                'unit_cost': round(np.random.uniform(5, 50), 2)
            })

demand_df = pd.DataFrame(demand_rows)
demand_df.to_sql('fact_demand_daily', engine, schema='core', if_exists='append', index=False)
print(f"Generated {len(demand_df)} demand records")
```

### 9.4 Phase 4: Frontend Integration (Week 4)

1. **Update Frontend Environment**
   
   `frontend/.env.local`:
   ```ini
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```

2. **Test API Integration**
   ```bash
   curl http://localhost:5000/health
   curl http://localhost:5000/api/v1/items?limit=10
   ```

3. **Update Frontend API Client**
   
   Already configured in `frontend/src/lib/api.ts` (uses `NEXT_PUBLIC_API_URL`)

4. **Build & Deploy Frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   npm run start  # or deploy to Vercel
   ```

### 9.5 Phase 5: Docker Compose Production (Week 5)

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    container_name: nova-corrente-db
    environment:
      POSTGRES_USER: nova_corrente
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: nova_corrente
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - nova-corrente-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nova_corrente"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.flask
    container_name: nova-corrente-api
    environment:
      DATABASE_URL: postgresql://nova_corrente:${DB_PASSWORD}@postgres:5432/nova_corrente
      EXTERNAL_APIS_ENABLED: "false"
      ENABLE_ML_PROCESSING: "false"
      CORS_ORIGINS: http://localhost:3000,https://app.novacorrente.com
    ports:
      - "5000:5000"
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - nova-corrente-net

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.nextjs
    container_name: nova-corrente-web
    environment:
      NEXT_PUBLIC_API_URL: http://backend:5000
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - nova-corrente-net

volumes:
  pgdata:

networks:
  nova-corrente-net:
    driver: bridge
```

**Dockerfiles:**

`backend/Dockerfile.flask`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_deployment.txt .
RUN pip install --no-cache-dir -r requirements_deployment.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "backend.api.enhanced_api:app"]
```

`frontend/Dockerfile.nextjs`:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["npm", "run", "start"]
```

---

## 10. Modern Libraries & Frameworks

### 10.1 Backend Stack

| **Library** | **Version** | **Purpose** |
|-------------|-------------|-------------|
| **Flask** | 2.3+ | Lightweight web framework |
| **SQLAlchemy** | 2.0+ | ORM + query builder |
| **psycopg2-binary** | 2.9+ | PostgreSQL driver |
| **Alembic** | 1.12+ | Database migrations |
| **Flask-CORS** | 4.0+ | Cross-origin resource sharing |
| **Flask-Caching** | 2.1+ | Simple in-memory cache |
| **marshmallow** | 3.20+ | Request/response validation |
| **python-jose** | 3.3+ | JWT encoding/decoding |
| **passlib** | 1.7+ | Password hashing (bcrypt) |
| **gunicorn** | 21.0+ | WSGI production server |

**Installation:**
```bash
pip install flask sqlalchemy psycopg2-binary alembic flask-cors flask-caching marshmallow python-jose[cryptography] passlib[bcrypt] gunicorn
```

### 10.2 Frontend Stack

| **Library** | **Version** | **Purpose** |
|-------------|-------------|-------------|
| **Next.js** | 14.2+ | React framework (SSR/SSG) |
| **React** | 18.2+ | UI library |
| **TypeScript** | 5.3+ | Type safety |
| **Tailwind CSS** | 3.4+ | Utility-first CSS |
| **Recharts** | 2.8+ | Charting library (built on D3) |
| **D3.js** | 7.8+ | Advanced custom visualizations |
| **SWR** | 2.2+ | Data fetching + caching |
| **TanStack Query** | 5.0+ (alternative to SWR) | Powerful async state management |
| **date-fns** | 2.30+ | Date manipulation |
| **zod** | 3.22+ | Schema validation |
| **Shadcn UI** | Latest | High-quality component library |
| **Framer Motion** | 10.0+ | Animations |
| **React Table** | 8.0+ | Advanced data tables |

**Installation:**
```bash
npm install next react react-dom typescript tailwindcss recharts d3 swr date-fns zod framer-motion @tanstack/react-table
```

### 10.3 Enhanced Interactive Features

**1. Interactive Dashboards with Tremor**

```bash
npm install @tremor/react
```

```typescript
import { Card, Metric, Text, AreaChart } from '@tremor/react';

export function KPIDashboard({ data }) {
  return (
    <Card>
      <Text>Stockout Rate</Text>
      <Metric>3.2%</Metric>
      <AreaChart
        data={data}
        index="date"
        categories={["stockout_rate"]}
        colors={["blue"]}
        yAxisWidth={40}
      />
    </Card>
  );
}
```

**2. Real-Time Notifications with React Hot Toast**

```bash
npm install react-hot-toast
```

```typescript
import toast, { Toaster } from 'react-hot-toast';

export function AlertNotification() {
  useEffect(() => {
    // Poll for new alerts every 30s
    const interval = setInterval(async () => {
      const alerts = await apiClient.getAlerts({ unread: true });
      if (alerts.length > 0) {
        toast.error(`${alerts.length} new critical alerts!`);
      }
    }, 30000);
    
    return () => clearInterval(interval);
  }, []);
  
  return <Toaster position="top-right" />;
}
```

**3. Data Export with React-CSV**

```bash
npm install react-csv
```

```typescript
import { CSVLink } from 'react-csv';

export function ExportButton({ data }) {
  return (
    <CSVLink 
      data={data} 
      filename="demand_forecast.csv"
      className="btn-primary"
    >
      Export to CSV
    </CSVLink>
  );
}
```

**4. Advanced Filtering with React-Select**

```bash
npm install react-select
```

```typescript
import Select from 'react-select';

export function MaterialFilter({ onChange }) {
  const options = [
    { value: 'ELECTRICAL', label: 'Electrical' },
    { value: 'TELECOM', label: 'Telecom' },
    { value: 'HARDWARE', label: 'Hardware' }
  ];
  
  return (
    <Select
      isMulti
      options={options}
      onChange={onChange}
      placeholder="Filter by family..."
    />
  );
}
```

**5. Animated Transitions with Framer Motion**

```typescript
import { motion } from 'framer-motion';

export function AnimatedCard({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
    >
      {children}
    </motion.div>
  );
}
```

---

## 11. Implementation Roadmap

### Timeline: 5-Week Sprint

```mermaid
gantt
    title Nova Corrente PostgreSQL Refactoring Roadmap
    dateFormat YYYY-MM-DD
    section Database
    PostgreSQL Setup           :done, db1, 2025-11-05, 3d
    Schema Migration (Alembic) :active, db2, after db1, 4d
    Demo Data Generation       :db3, after db2, 2d
    
    section Backend
    Config Update (Postgres)   :be1, after db1, 2d
    API Endpoints v1           :be2, after be1, 5d
    Authentication & RBAC      :be3, after be2, 3d
    Caching & Optimization     :be4, after be3, 2d
    
    section Frontend
    API Client Integration     :fe1, after be2, 2d
    Dashboard Page             :fe2, after fe1, 4d
    Material Detail Pages      :fe3, after fe2, 3d
    Charts & Visualizations    :fe4, after fe3, 3d
    
    section Data Pipeline
    Offline ML Pipeline        :ml1, after db3, 5d
    ETL Load Scripts           :ml2, after ml1, 3d
    KPI Calculation Jobs       :ml3, after ml2, 2d
    
    section Deployment
    Docker Compose Setup       :dep1, after be4, 2d
    Production Deploy          :dep2, after dep1, 2d
    Testing & Validation       :dep3, after dep2, 3d
```

### Week-by-Week Breakdown

**Week 1: Database Foundation**
- ☑ Install PostgreSQL
- ☑ Create schemas (core, analytics, support, staging)
- ☑ Initialize Alembic migrations
- ☑ Generate demo/synthetic data
- **Deliverable**: Populated PostgreSQL database

**Week 2: Backend API**
- ☑ Refactor database config to PostgreSQL
- ☑ Implement Flask API v1 endpoints (health, items, KPIs, forecasts)
- ☑ Add JWT authentication
- ☑ Implement Flask-Caching
- **Deliverable**: Working REST API with Postman collection

**Week 3: Frontend Dashboard**
- ☑ Update Next.js API client
- ☑ Build Dashboard page (KPI cards + charts)
- ☑ Build Material catalog + detail pages
- ☑ Integrate Recharts for time-series viz
- **Deliverable**: Interactive dashboard (localhost)

**Week 4: ML Pipeline Integration**
- ☑ Create offline ML training scripts (Prophet/ARIMA)
- ☑ Feature engineering pipeline
- ☑ Export forecasts/features to Parquet
- ☑ ETL scripts to load into PostgreSQL
- **Deliverable**: Precomputed forecasts in database

**Week 5: Production Deployment**
- ☑ Docker Compose setup (Postgres + Flask + Next.js)
- ☑ Production environment variables
- ☑ Health checks & monitoring
- ☑ End-to-end testing
- **Deliverable**: Production-ready deployment

---

## 12. Success Criteria & KPIs

### Technical Metrics

| **Metric** | **Target** | **How to Measure** |
|------------|------------|-

---

## 12. Success Criteria & KPIs

### Technical Metrics

| **Metric** | **Target** | **How to Measure** |
|------------|------------|--------------------|
| API Response Time (p95) | < 200ms | Flask logging + APM |
| Database Query Time (p95) | < 100ms | PostgreSQL `pg_stat_statements` |
| Frontend Page Load (FCP) | < 1.5s | Lighthouse score |
| Forecast Accuracy (MAPE) | < 15% | Backtest: `\|actual - forecast\| / actual` |
| System Uptime | > 99.5% | Health check endpoint monitoring |
| Cache Hit Rate | > 80% | Flask-Caching metrics |
| PostgreSQL Connection Pool Utilization | < 70% | `pg_stat_activity` |

### Business Metrics

| **KPI** | **Baseline** | **6-Month Target** |
|---------|--------------|--------------------|
| Stockout Rate | 5.2% | < 3.0% |
| Delayed Orders | 8.1% | < 5.0% |
| Inventory Carrying Cost | Baseline | -20% |
| ABC-A Coverage (stockout rate) | 3.5% | < 2.0% |
| Time to Decision (avg) | 2 hours | < 30 minutes |

### Demo Validation Checklist

- [ ] Dashboard loads with KPI cards in < 2 seconds
- [ ] Material detail page shows 90-day demand history chart
- [ ] Forecast chart displays 30/60/90-day horizons with confidence intervals
- [ ] Recommendations page shows actionable items sorted by priority
- [ ] Alerts inbox shows unread critical alerts with mark-as-read functionality
- [ ] CSV export works for demand/forecast time series
- [ ] Filters (family, ABC class, site) apply correctly and update charts
- [ ] Authentication: login/logout, JWT token refresh
- [ ] Audit logs track all user actions
- [ ] Mobile responsive (Tailwind breakpoints work)

---

## 13. Risk Mitigation

### Technical Risks

| **Risk** | **Impact** | **Mitigation** |
|----------|-----------|----------------|
| PostgreSQL performance degradation at scale | High | Partitioning, indexing, materialized views; load test with 10M rows |
| Forecast accuracy drift over time | Medium | Monitor MAPE weekly; retrain models quarterly; A/B test new models |
| Frontend API timeout (slow queries) | Medium | Implement caching, query optimization, connection pooling |
| Data quality issues (nulls, duplicates) | High | Schema constraints (NOT NULL, UNIQUE), staging validation, audit logs |
| Dependency on teammate for ML datasets | High | Generate synthetic data for initial demo; establish data schema contracts early |

### Operational Risks

| **Risk** | **Impact** | **Mitigation** |
|----------|-----------|----------------|
| Single-point-of-failure (one VM) | High | Phase 2: PostgreSQL read replicas, Flask horizontal scaling |
| Manual data refresh (no automation) | Medium | Cron jobs for nightly ETL; later: Airflow DAGs |
| No monitoring/alerting | Medium | Add Prometheus + Grafana; set up PagerDuty alerts |
| Lack of backup/disaster recovery | Critical | PostgreSQL WAL archiving, daily pg_dump backups to S3 |

---

## 14. Future Enhancements

### Phase 2 (Post-MVP)

1. **Advanced Analytics**
   - Demand clustering (K-Means by seasonality patterns)
   - Supplier reliability scoring (Bayesian updates)
   - Multi-echelon inventory optimization
   - What-if scenario simulator (adjust lead time, safety stock)

2. **Real-Time Features (Optional)**
   - WebSocket for live alert notifications
   - Streaming data ingestion (Kafka + Flink)
   - Real-time dashboard updates (Server-Sent Events)

3. **BI Tool Integration**
   - Metabase/Superset connected to PostgreSQL
   - Pre-built dashboards for executives
   - Scheduled email reports (PDF)

4. **Mobile App**
   - React Native app for warehouse managers
   - Push notifications for critical alerts
   - Barcode scanning for inventory counts

5. **AI/LLM Features**
   - Natural language queries ("Show me A-class items with stockout risk")
   - Automated report generation (Gemini API)
   - Chatbot for KPI explanations

---

## 15. Conclusion

### Summary

This specification delivers a **production-ready, cost-optimized, offline-first analytics platform** for Nova Corrente's supply-chain and inventory optimization needs. By leveraging:

- **PostgreSQL** for ACID compliance, partitioning, and JSONB flexibility
- **Flask** for lightweight, read-only REST API
- **Next.js** for SEO-friendly, interactive dashboards
- **Offline ML** for deterministic, debuggable forecasts

...we achieve a **simple, stable, and scalable** system that:

✅ **Minimizes infrastructure costs** (no real-time ML, no external APIs)  
✅ **Enables rapid iteration** (schema flexibility via JSONB)  
✅ **Provides demonstrable value** (static datasets sufficient for demo)  
✅ **Future-proofs architecture** (easy to add Kubernetes, Citus, streaming later)

### Next Steps

1. **Approve this specification** (stakeholder review)
2. **Provision PostgreSQL** (Docker or managed service)
3. **Initialize Alembic migrations** (create schemas/tables)
4. **Generate demo data** (synthetic or teammate-provided datasets)
5. **Implement Flask API v1** (core endpoints)
6. **Build Next.js dashboard** (KPIs, charts, material pages)
7. **Deploy via Docker Compose** (single-node MVP)
8. **Iterate based on feedback** (add features incrementally)

### Contact & Support

- **Technical Lead**: [Your Name]
- **Project Repository**: `https://github.com/novacorrente/gran-prix`
- **Documentation**: `docs/proj/diagrams/Project.md` (this file)
- **Issue Tracker**: GitHub Issues

---

**End of Specification**  
**Version**: 3.0.0-postgres  
**Status**: ✅ Ready for Implementation  
**Last Updated**: 2025-11-05

---

