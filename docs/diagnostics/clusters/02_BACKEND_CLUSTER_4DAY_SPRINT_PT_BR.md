# 🔧 BACKEND CLUSTER - 4-DAY SPRINT PLAN
## Nova Corrente - API & Data Access Layer

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** 🚀 Execution-Ready  
**Sprint:** 4 Days (D0-D4)  
**Cluster Lead:** Backend Lead  
**Team Size:** 1-2 Engineers

---

## 📋 QUICK ORIENTATION

**Goal:** Provide stable API / BFF endpoints for the dashboard to query aggregated analytics and expose a minimal ingestion trigger.

**Key Constraint:** Use FastAPI (already exists), DuckDB for fast SQL over Parquet (no Spark), no heavy ML serving (ML runs locally, results exported to gold).

**Reference Documents:**
- [Diagnóstico Completo](../COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md#analytics-layer) - API gaps analysis
- [Data Cluster](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md) - Data layer requirements
- [Frontend Cluster](./03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - Frontend requirements
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy

---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Reference:** [Global Constraints Document](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical results** are consumed via read-only API endpoints.

**Backend Cluster Specific Rules:**
- ✅ **NO live inference endpoints** or model serving
- ✅ API reads from static Parquet/DuckDB tables only
- ✅ Add `POST /api/v1/data/refresh` endpoint to re-load updated analytical datasets (manual trigger, NOT automated ML job)
- ✅ Logging: maintain source traceability (`dataset_id`, `model_version`) to guarantee reproducibility
- ❌ **NO ML dependencies** in `requirements_deployment.txt` or Dockerfile
- ❌ **NO inference endpoints** (`/predict`, `/forecast`, `/inference`)
- ❌ **NO training endpoints** (`/train`, `/retrain`, `/optimize`)

**Validation:**
- [ ] Check `requirements_deployment.txt` has NO ML dependencies
- [ ] Check Dockerfile has NO ML dependencies
- [ ] Verify all endpoints are read-only (except data refresh)
- [ ] Verify data refresh endpoint requires auth and is manual trigger only
- [ ] Check logging includes `dataset_id` and `model_version` traceability

---

## 🎯 KEY ARCHITECTURE & CONSTRAINTS

### Technical Stack
- ✅ **API Framework:** FastAPI (Python) - already exists
- ✅ **Data Access:** DuckDB + Parquet (fast SQL over Parquet, no Spark)
- ✅ **Caching:** Redis or in-memory (TTL 60s)
- ✅ **Auth:** API key or JWT (simple)
- ❌ **Deferred:** MLflow serving, Seldon Core, feature store
- ❌ **NO ML dependencies:** PyTorch, TensorFlow, scikit-learn, MLflow

### API Requirements
- **Read Operations:** Time series, aggregates, inventory (precomputed only)
- **Write Operations:** Data refresh trigger (auth required, manual only)
- **Performance:** < 500ms cached, < 2s cold queries
- **Scale:** Small-medium datasets (< 10GB)

### Scope Reduction Triggers
- If DuckDB unavailable → Use Pandas reads (slower but workable)
- If caching infra unavailable → Aggressive rate limits + in-process memoization

---

## 📅 DELIVERABLES (DAY-BY-DAY)

### **D0 (TODAY): Freeze Endpoints & Contract** ⏱️ 2-4 hours
**Owner:** Backend Lead  
**Deliverables:**
- [ ] Define API endpoints and payloads (see below)
- [ ] Create `openapi.yaml` (minimal OpenAPI spec)
- [ ] Document request/response schemas
- [ ] Review with Frontend team for alignment
- [ ] **Verify NO ML endpoints** in API contract

**Acceptance Criteria:**
- ✅ OpenAPI spec validates
- ✅ Frontend team confirms endpoints meet requirements
- ✅ All payloads documented
- ✅ NO inference or training endpoints defined

**Output Files:**
- `backend/api/openapi.yaml` - API contract
- `backend/api/schemas/` - Pydantic models

**API Endpoints (Read-Only):**
```yaml
# Endpoints to implement - READ ONLY (except data refresh)
GET  /api/v1/items                          # List items + metadata
GET  /api/v1/items/{id}/timeseries          # Time series for item (precomputed)
GET  /api/v1/forecasts/summary              # Aggregated metrics (precomputed)
GET  /api/v1/inventory/{id}                 # Inventory levels (precomputed)
POST /api/v1/data/refresh                   # Trigger data refresh (auth, manual)
GET  /health                                # Health check (includes ML dependency check)
```

---

### **D1: Data Access & Queries** ⏱️ 6-8 hours
**Owner:** 1 Backend Engineer  
**Deliverables:**

#### DuckDB Layer
- [ ] Install DuckDB Python package (**NO ML dependencies**)
- [ ] Implement DuckDB layer that reads Parquet (silver/gold) - **READ ONLY**
- [ ] Create functions:
  - [ ] `get_timeseries(item_id, start, end)` - Returns time series data (precomputed)
  - [ ] `get_aggregate(item_ids, window)` - Returns aggregated metrics (precomputed)
  - [ ] `get_inventory(item_id, date)` - Returns inventory levels (precomputed)
- [ ] **NO ML processing** - only read precomputed results
- [ ] Add connection pooling (single file connection per request)
- [ ] Add error handling and logging
- [ ] **Verify NO ML dependencies** in data access code

**Acceptance Criteria:**
- ✅ DuckDB reads Parquet files successfully
- ✅ All query functions return expected data
- ✅ Query performance < 2s for 30-day time series
- ✅ Error handling works (file not found, invalid params)
- ✅ NO ML dependencies in code

**Output Files:**
- `backend/services/data_access.py` - DuckDB data access layer
- `backend/services/queries.py` - Query functions

**Technical Specs:**
```python
# Example DuckDB query - READ ONLY
import duckdb

def get_timeseries(item_id: str, start: date, end: date):
    conn = duckdb.connect()
    query = f"""
    SELECT date, forecast, actual, source, model_version, generated_at
    FROM read_parquet('data/gold/fact_forecast.parquet')
    WHERE item_id = '{item_id}'
      AND date >= '{start}'
      AND date <= '{end}'
    ORDER BY date
    """
    result = conn.execute(query).fetchdf()
    conn.close()
    return result
```

---

### **D2: API Endpoints & BFF Logic** ⏱️ 6-8 hours
**Owner:** 1-2 Backend Engineers  
**Deliverables:**

#### FastAPI Endpoints
- [ ] Implement endpoints:
  - [ ] `GET /api/v1/items` - List items with metadata
  - [ ] `GET /api/v1/items/{id}/timeseries?start&end` - Time series JSON (precomputed)
  - [ ] `GET /api/v1/forecasts/summary?start&end` - Aggregated metrics (precomputed)
  - [ ] `GET /api/v1/inventory/{id}` - Inventory levels (precomputed)
  - [ ] `POST /api/v1/data/refresh` - Kicks data refresh (auth token, manual trigger)
  - [ ] `GET /health` - Health check (includes ML dependency validation)
- [ ] **NO inference endpoints** - only read precomputed data
- [ ] Implement caching middleware (Redis or in-memory with TTL 60s)
- [ ] Add Pydantic models for request/response validation
- [ ] Add error handling (400, 404, 500)
- [ ] Add source traceability logging (`dataset_id`, `model_version`)

**Acceptance Criteria:**
- ✅ All endpoints return expected JSON
- ✅ Caching works (60s TTL)
- ✅ Error handling works (invalid params, missing data)
- ✅ Response times < 500ms cached, < 2s cold
- ✅ NO ML endpoints exist

**Output Files:**
- `backend/api/routes/items.py` - Items endpoints
- `backend/api/routes/forecasts.py` - Forecasts endpoints
- `backend/api/routes/inventory.py` - Inventory endpoints
- `backend/api/routes/data_refresh.py` - Data refresh endpoint
- `backend/api/middleware/cache.py` - Caching middleware

**Technical Specs:**
```python
# Example FastAPI endpoint - READ ONLY
from fastapi import FastAPI, Query
from datetime import date
from backend.services.data_access import get_timeseries

app = FastAPI()

@app.get("/api/v1/items/{id}/timeseries")
async def get_timeseries_endpoint(
    id: str,
    start: date = Query(...),
    end: date = Query(...)
):
    # Read precomputed data only
    data = get_timeseries(id, start, end)
    
    # Log source traceability
    if not data.empty:
        model_version = data['model_version'].iloc[0] if 'model_version' in data.columns else None
        dataset_id = data['dataset_id'].iloc[0] if 'dataset_id' in data.columns else None
        logger.info(f"Timeseries query: item={id}, model_version={model_version}, dataset_id={dataset_id}")
    
    return {"item_id": id, "timeseries": data.to_dict("records")}
```

---

### **D3: Auth, Tests & Integration** ⏱️ 6-8 hours
**Owner:** 1 Backend Engineer  
**Deliverables:**

#### Authentication
- [ ] Add basic API key auth or JWT for BFF
- [ ] Protect `/api/v1/data/refresh` endpoint (auth required, admin only)
- [ ] Add rate limiting (optional, if caching unavailable)

#### Testing
- [ ] Add unit tests for API handlers (pytest)
- [ ] Add integration tests for data access layer
- [ ] Test caching behavior
- [ ] Test error handling
- [ ] **Test NO ML dependencies** in deployment code

#### CI/CD
- [ ] Add GitHub Action to run tests on push
- [ ] Configure test coverage reporting (target 80%+)
- [ ] Add ML dependency validation to CI pipeline

**Acceptance Criteria:**
- ✅ Auth works (API key or JWT)
- ✅ Protected endpoints require auth
- ✅ Unit tests pass (80%+ coverage)
- ✅ CI pipeline runs successfully
- ✅ ML dependency validation passes

**Output Files:**
- `backend/api/auth.py` - Authentication logic
- `backend/tests/test_api.py` - API tests
- `backend/tests/test_data_access.py` - Data access tests
- `backend/tests/test_deployment_constraints.py` - ML constraint tests
- `.github/workflows/backend-tests.yml` - CI pipeline

---

### **D4: Finalize Docs & Deploy Readiness** ⏱️ 4-6 hours
**Owner:** 1 Backend Engineer  
**Deliverables:**

#### Documentation
- [ ] Produce `README_API.md` with:
  - [ ] API endpoints documentation
  - [ ] Authentication guide
  - [ ] Example requests/responses
  - [ ] Error codes reference
  - [ ] **ML constraint documentation** (no ML endpoints, read-only)
- [ ] Create examples for frontend consumption
- [ ] Document deployment process

#### Health Check
- [ ] Implement `/health` endpoint with:
  - [ ] Database connectivity check
  - [ ] Parquet file access check
  - [ ] Cache availability check
  - [ ] **ML dependency validation** (verify NO ML frameworks loaded)

**Acceptance Criteria:**
- ✅ Documentation complete
- ✅ Health check works (includes ML validation)
- ✅ Frontend can consume API successfully
- ✅ Deploy-ready (Dockerfile, requirements_deployment.txt updated)

**Output Files:**
- `docs/backend/README_API.md` - API documentation
- `docs/backend/examples/` - Example requests/responses
- `backend/Dockerfile` - Dockerfile for deployment

---

## 🔧 TECHNICAL GUIDELINES & PATTERNS

### Data Access Patterns

#### DuckDB + Parquet (Read-Only)
```python
# Single file connection per request (avoid open file contention)
import duckdb

def query_parquet(file_path: str, query: str):
    conn = duckdb.connect()
    try:
        result = conn.execute(f"SELECT * FROM read_parquet('{file_path}') WHERE {query}").fetchdf()
        return result
    finally:
        conn.close()
```

#### Caching Strategy
```python
# Redis or in-memory cache
from functools import lru_cache
from datetime import timedelta

@lru_cache(maxsize=100)
def get_cached_timeseries(item_id: str, start: str, end: str):
    # Cache for 60 seconds
    return get_timeseries(item_id, start, end)
```

### API Patterns

#### Pydantic Models
```python
from pydantic import BaseModel
from datetime import date

class TimeseriesRequest(BaseModel):
    item_id: str
    start: date
    end: date

class TimeseriesResponse(BaseModel):
    item_id: str
    timeseries: list[dict]
    model_version: str | None = None  # ML metadata
    dataset_id: str | None = None  # ML metadata
```

#### Error Handling
```python
from fastapi import HTTPException

@app.get("/api/v1/items/{id}/timeseries")
async def get_timeseries(id: str, start: date, end: date):
    try:
        data = get_timeseries(id, start, end)
        if data.empty:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Include ML metadata in response
        metadata = {
            "model_version": data['model_version'].iloc[0] if 'model_version' in data.columns else None,
            "dataset_id": data['dataset_id'].iloc[0] if 'dataset_id' in data.columns else None,
            "generated_at": data['generated_at'].iloc[0] if 'generated_at' in data.columns else None
        }
        
        return {"item_id": id, "timeseries": data.to_dict("records"), "metadata": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📊 API ENDPOINT SPECIFICATIONS

### GET /api/v1/items
**Description:** List all items with metadata

**Response:**
```json
{
  "items": [
    {
      "id": "item_001",
      "name": "Item Name",
      "category": "CONN-001",
      "sku": "SKU-001"
    }
  ],
  "total": 100
}
```

---

### GET /api/v1/items/{id}/timeseries
**Description:** Get time series data for an item (precomputed)

**Query Parameters:**
- `start` (date): Start date (required)
- `end` (date): End date (required)

**Response:**
```json
{
  "item_id": "item_001",
  "timeseries": [
    {
      "date": "2025-11-01",
      "forecast": 100.5,
      "actual": 95.0,
      "source": "prophet",
      "model_version": "v1.2.3",
      "generated_at": "2025-11-01T10:00:00Z"
    }
  ],
  "metadata": {
    "model_version": "v1.2.3",
    "dataset_id": "dataset_001",
    "generated_at": "2025-11-01T10:00:00Z"
  }
}
```

---

### GET /api/v1/forecasts/summary
**Description:** Get aggregated forecast metrics (precomputed)

**Query Parameters:**
- `start` (date): Start date (required)
- `end` (date): End date (required)
- `item_ids` (string, optional): Comma-separated item IDs

**Response:**
```json
{
  "summary": {
    "total_forecast": 10000.5,
    "total_actual": 9500.0,
    "mape": 5.26,
    "items_count": 100
  },
  "period": {
    "start": "2025-11-01",
    "end": "2025-11-30"
  },
  "metadata": {
    "model_version": "v1.2.3",
    "dataset_id": "dataset_001"
  }
}
```

---

### GET /api/v1/inventory/{id}
**Description:** Get inventory levels for an item (precomputed)

**Response:**
```json
{
  "item_id": "item_001",
  "current_stock": 150,
  "reorder_point": 100,
  "safety_stock": 50,
  "last_updated": "2025-11-01T10:00:00Z"
}
```

---

### POST /api/v1/data/refresh
**Description:** Trigger data refresh to reload updated ML results (auth required, manual trigger only)

**Headers:**
- `Authorization: Bearer <token>` or `X-API-Key: <key>`

**Request Body:**
```json
{
  "source": "ml_results",
  "force": false
}
```

**Response:**
```json
{
  "status": "triggered",
  "job_id": "job_123",
  "estimated_completion": "2025-11-01T10:30:00Z",
  "message": "Data refresh triggered manually"
}
```

**Note:** This endpoint triggers reload of precomputed ML results from storage. It does NOT trigger ML processing.

---

### GET /health
**Description:** Health check with ML dependency validation

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "parquet_access": "ok",
  "cache": "ok",
  "ml_dependencies": {
    "status": "compliant",
    "message": "No ML dependencies detected",
    "checked_packages": ["torch", "tensorflow", "sklearn", "mlflow"],
    "violations": []
  },
  "timestamp": "2025-11-01T10:00:00Z"
}
```

---

## ✅ SUCCESS CRITERIA (ACCEPTANCE TESTS)

### Functional Requirements
- [ ] ✅ All endpoints respond as contract in < 500ms for cached queries, < 2s for cold queries on sample dataset
- [ ] ✅ Data refresh trigger runs successfully and reloads Parquet from storage (NO ML processing)
- [ ] ✅ 80%+ unit test coverage on newly added API code (or at least tests for critical routes)
- [ ] ✅ All endpoints return expected JSON structure
- [ ] ✅ Error handling works (400, 404, 500)

### Performance Requirements
- [ ] ✅ Cached queries: < 500ms
- [ ] ✅ Cold queries: < 2s
- [ ] ✅ Health check: < 100ms

### ML Ops Validation (MANDATORY)
- [ ] ✅ No ML dependencies in requirements_deployment.txt
- [ ] ✅ No ML dependencies in Dockerfile
- [ ] ✅ No inference endpoints exist
- [ ] ✅ Only read operations for precomputed data
- [ ] ✅ Data refresh endpoint works (manual trigger only)
- [ ] ✅ Health check validates NO ML dependencies

### Security Requirements
- [ ] ✅ Protected endpoints require auth
- [ ] ✅ API keys stored securely (env vars)
- [ ] ✅ Rate limiting works (if implemented)

---

## 🚨 SCOPE-REDUCTION OPTIONS (IF BLOCKERS)

### Option 1: Replace DuckDB with Pandas
**Trigger:** DuckDB unavailable or installation issues

**Changes:**
- Use Pandas `read_parquet()` directly
- Slower but workable for small datasets
- No SQL queries, Python-only

**Impact:** ⚠️ Slower queries, but functional

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 2: No Caching (Aggressive Rate Limits)
**Trigger:** Redis/caching infra unavailable

**Changes:**
- Add aggressive server-side rate limits
- Use in-process memoization (lru_cache)
- Add request throttling

**Impact:** ⚠️ Higher latency, but functional

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 3: Minimal Auth (API Key Only)
**Trigger:** JWT/OAuth too complex

**Changes:**
- Use simple API key in header
- No refresh tokens
- Basic rate limiting

**Impact:** ⚠️ Less secure, but functional for MVP

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 4: No Data Refresh (Static Data Only)
**Trigger:** Time pressure or data refresh complexity

**Changes:**
- Remove data refresh endpoint
- Use static precomputed ML results only
- Manual file replacement for updates

**Impact:** ⚠️ No automated updates, but functional

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

## 🔗 KEY RECOMMENDATIONS

### Technical Decisions
1. **Use DuckDB** - Fastest path to SQL over Parquet without Spark
2. **Cache aggressively** - 60s TTL for heavy queries
3. **Pydantic models** - Type safety and validation
4. **Health check** - Essential for deployment monitoring (includes ML validation)
5. **Source traceability** - Log dataset_id and model_version for reproducibility

### Follow-Up Questions (Answer Quickly)
1. **Data Access:** DuckDB + Parquet acceptable? Or must use Spark?
2. **Caching:** Redis available, or use in-memory cache?
3. **Auth:** Simple API key or JWT/OAuth?
4. **Performance:** What's acceptable query latency? (Target: < 2s)
5. **ML Results Path:** Where are precomputed ML results stored? (shared storage path)

---

## 📚 REFERENCE LINKS

- [Data Cluster](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md) - Data layer requirements
- [Frontend Cluster](./03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - Frontend requirements
- [Deploy Cluster](./04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md) - Deployment requirements
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy
- [Diagnóstico Completo](../COMPREHENSIVE_DATA_ENGINEERING_DIAGNOSTIC_PT_BR.md#analytics-layer) - API gaps

---

## 📝 NEXT STEPS

1. **Assign Cluster Lead:** Backend Lead
2. **Assign Team:** 1-2 Engineers
3. **Kickoff Meeting:** Review endpoints, align with Frontend
4. **Daily Standup:** 9 AM - Review progress, blockers
5. **End of Day:** Acceptance test for each day's deliverables

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Execution-Ready - 4-Day Sprint Plan

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

