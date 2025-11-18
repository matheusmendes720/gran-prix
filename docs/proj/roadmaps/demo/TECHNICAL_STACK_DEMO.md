# DEMO Path Technical Stack
## Nova Corrente - Complete Stack Breakdown

**Version:** 1.0  
**Date:** November 2025  
**Status:** Complete Documentation

---

## Overview

The DEMO path uses a simplified, lightweight technology stack optimized for rapid deployment (4 days) and roadshow demonstrations.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                         │
│  ERP | Mock Data | Precomputed ML Results (Parquet)    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              BRONZE LAYER (Raw)                         │
│              Parquet Files in MinIO                     │
│              - Raw data as received                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SILVER LAYER (Cleaned)                     │
│              Parquet Files in MinIO                     │
│              - Cleaned and validated data               │
│              Processing: DuckDB + Pandas                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              GOLD LAYER (Curated)                       │
│              Parquet Files in MinIO                     │
│              - Star Schema: dim_item, dim_time,         │
│                fact_forecast, fact_metrics              │
│              Processing: DuckDB + Pandas                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              ML PROCESSING (Separate)                   │
│              Local Environment                          │
│              - Prophet/ARIMA/LSTM training              │
│              - Output: Precomputed Parquet files        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼ (Read-only)
┌─────────────────────────────────────────────────────────┐
│              BACKEND API (FastAPI)                      │
│              - Read-only endpoints                      │
│              - DuckDB queries over Parquet              │
│              - NO ML dependencies                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (React + Vite)                    │
│              - Dashboard with Recharts                  │
│              - Display precomputed insights             │
│              - NO ML processing UI                      │
└─────────────────────────────────────────────────────────┘
```

---

## Storage Layer

### Parquet Files
- **Format:** Columnar Parquet files
- **Advantages:**
  - Efficient compression
  - Fast analytical queries
  - Schema evolution support
  - Cross-platform compatibility

### MinIO
- **Type:** S3-compatible object storage
- **Deployment:** Local/Docker
- **Configuration:**
  ```yaml
  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
  ```

### Storage Structure
```
minio/
├── bronze/
│   ├── raw_data/
│   └── ingested/
├── silver/
│   ├── cleaned/
│   └── validated/
└── gold/
    ├── dim_item.parquet
    ├── dim_time.parquet
    ├── fact_demand_daily.parquet
    ├── fact_forecasts.parquet
    └── fact_metrics.parquet
```

---

## Compute Layer

### DuckDB
- **Type:** In-process SQL engine
- **Use Case:** Analytical queries over Parquet files
- **Advantages:**
  - Fast analytical queries
  - No separate server required
  - Direct Parquet file access
  - SQL interface

**Example Query:**
```python
import duckdb

conn = duckdb.connect()
result = conn.execute("""
    SELECT 
        item_id,
        SUM(demand) as total_demand
    FROM read_parquet('data/gold/fact_demand_daily.parquet')
    WHERE date >= '2025-01-01'
    GROUP BY item_id
    ORDER BY total_demand DESC
    LIMIT 10
""").df()
```

### Pandas
- **Type:** Python data processing library
- **Use Case:** Data transformations, cleaning, feature engineering
- **Advantages:**
  - Flexible data manipulation
  - Rich functionality
  - Easy integration with DuckDB

---

## Orchestration

### Simple Scheduler
- **Type:** Python scripts + cron/schedule
- **Configuration:**
  ```python
  import schedule
  import time
   
  def run_daily_pipeline():
      # Data ingestion
      # Transformations
      # Export to gold layer
      pass
   
  schedule.every().day.at("02:00").do(run_daily_pipeline)
   
  while True:
      schedule.run_pending()
      time.sleep(60)
  ```

### Docker Compose
- **Purpose:** Service orchestration
- **Services:**
  - MinIO (storage)
  - Backend API (FastAPI)
  - Frontend (React)

---

## Backend API

### FastAPI
- **Framework:** FastAPI (Python)
- **Endpoints:** Read-only
- **Data Access:** DuckDB queries over Parquet
- **Dependencies:** NO ML libraries

**Example Endpoint:**
```python
from fastapi import FastAPI
import duckdb

app = FastAPI()

@app.get("/api/v1/items/{item_id}/timeseries")
def get_timeseries(item_id: str):
    conn = duckdb.connect()
    df = conn.execute(f"""
        SELECT date, demand
        FROM read_parquet('data/gold/fact_demand_daily.parquet')
        WHERE item_id = '{item_id}'
        ORDER BY date
    """).df()
    return df.to_dict('records')
```

---

## Frontend

### React + Vite
- **Framework:** React 18+
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Charts:** Recharts

### Key Components
- Dashboard with KPI cards
- Time series charts
- Data tables
- No ML processing UI

---

## ML Processing (Separate Environment)

### Local ML Environment
- **Location:** Separate from deployment
- **Models:** Prophet, ARIMA, LSTM
- **Output:** Precomputed Parquet files
- **Metadata:** model_version, generated_at, source

### ML Pipeline
```python
# ml_pipeline/main.py
import pandas as pd
from prophet import Prophet

# Load data
df = pd.read_parquet('data/gold/fact_demand_daily.parquet')

# Train model
model = Prophet()
model.fit(df)

# Generate forecast
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Export to Parquet
forecast.to_parquet('output/forecasts.parquet')
```

---

## Deployment

### Docker Compose
```yaml
version: '3.8'

services:
  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    depends_on:
      - minio

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  minio_data:
```

---

## Mock Data Generation

### Sample Data Script
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate mock demand data
dates = pd.date_range(start='2024-01-01', end='2025-01-01', freq='D')
items = ['ITEM-001', 'ITEM-002', 'ITEM-003']

data = []
for item in items:
    for date in dates:
        data.append({
            'item_id': item,
            'date': date,
            'demand': np.random.poisson(100)
        })

df = pd.DataFrame(data)
df.to_parquet('data/gold/fact_demand_daily.parquet', index=False)
```

---

## Performance Characteristics

- **Query Speed:** < 100ms for typical queries
- **Data Volume:** Up to 10GB Parquet files
- **Concurrency:** Limited (file-based)
- **Scalability:** Single-node

---

## References

- [DEMO Path Changelog](../../../CHANGELOG_DEMO.md)
- [DEMO Roadmaps](README_DEMO_ROADMAPS.md)
- [4-Day Sprint Overview](../../../diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md)

---

**Document Created:** November 2025  
**Version:** 1.0  
**Status:** Complete Documentation

