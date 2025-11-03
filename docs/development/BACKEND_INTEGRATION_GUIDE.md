# 🔌 Backend Integration Guide

## Overview

This guide explains how all backend services and external API clients are integrated and initialized in the Nova Corrente API.

## Architecture

```
┌─────────────────────────────────────────────────┐
│           FastAPI Application                   │
│            (app/main.py)                        │
└─────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                        │
┌───────▼────────┐      ┌───────▼────────┐
│  Inner Services│      │ External APIs │
│                 │      │                │
│ - Database      │      │ - INMET        │
│ - Features     │      │ - BACEN        │
│ - Analytics    │      │ - ANATEL       │
│ - Materials    │      │ - OpenWeather  │
│ - Predictions  │      │ - Expanded (25+)│
│ - Integration  │      │                │
└────────────────┘      └────────────────┘
```

## Startup Sequence

1. **Path Setup** - Backend directory added to Python path
2. **Environment Variables** - `.env` file loaded
3. **FastAPI App Creation** - App instance created with metadata
4. **Startup Event** - Integration Manager initializes all services
5. **Router Registration** - All API routes registered
6. **CORS Middleware** - Cross-origin requests configured
7. **Server Start** - Uvicorn starts listening on configured port

## Inner Data Services

### 1. Database Service (`database_service.py`)

**Purpose:** Connection pooling, query builder, transaction management

**Initialization:**
```python
from backend.services.database_service import db_service

# Test connection
db_healthy = db_service.test_connection()
```

**Configuration:** `backend/config/database_config.py`

**Environment Variables:**
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 3306)
- `DB_USER` - Database user (default: root)
- `DB_PASSWORD` - Database password
- `DB_NAME` - Database name (default: STOCK)

### 2. External Data Service (`external_data_service.py`)

**Purpose:** Manage external data refresh (Climate, Economic, 5G)

**Methods:**
- `refresh_climate_data(start_date, end_date)` - Refresh INMET climate data
- `refresh_economic_data(start_date, end_date)` - Refresh BACEN economic data
- `refresh_5g_data(start_date, end_date)` - Refresh ANATEL 5G data

### 3. Integration Service (`integration_service.py`)

**Purpose:** Orchestrate expanded Brazilian API integration

**Methods:**
- `run_daily_pipeline(date_ref)` - Run complete daily pipeline
- `refresh_all_external_data(start_date, end_date, data_types)` - Refresh all external data
- `calculate_features_for_all_materials(date_ref, batch_size)` - Calculate features
- `generate_expanded_features(material_id, date_ref)` - Generate 125+ features

### 4. Feature Service (`feature_service.py`)

**Purpose:** Feature extraction and engineering

### 5. Material Service (`material_service.py`)

**Purpose:** Material management and operations

### 6. Analytics Service (`analytics_service.py`)

**Purpose:** Analytics and reporting

### 7. Prediction Service (`prediction_service.py`)

**Purpose:** ML model predictions and forecasts

## External API Clients

### 1. INMET (Climate Data)

**Configuration:** `backend/config/external_apis_config.py`

**Base URL:** `https://apitempo.inmet.gov.br/`

**Environment Variables:**
- `INMET_API_KEY` - API key (optional)

**Features:**
- Temperature data
- Precipitation data
- Humidity data
- Climate risk analysis

### 2. BACEN (Economic Data)

**Configuration:** `backend/config/external_apis_config.py`

**Base URL:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.`

**Environment Variables:**
- `BACEN_API_KEY` - API key (optional)

**Series Codes:**
- IPCA: 433 (Inflation index)
- SELIC: 11 (Interest rate)
- Exchange Rate: 1 (USD/BRL)
- GDP: 4380 (GDP index)

### 3. ANATEL (5G Expansion)

**Configuration:** `backend/config/external_apis_config.py`

**Base URL:** `https://www.gov.br/anatel/`

**Environment Variables:**
- `ANATEL_API_KEY` - API key (optional)

**Features:**
- 5G tower expansion data
- Coverage percentages
- Milestone tracking
- Demand impact analysis

### 4. OpenWeatherMap (Alternative Climate)

**Configuration:** `backend/config/external_apis_config.py`

**Base URL:** `https://api.openweathermap.org/data/2.5/`

**Environment Variables:**
- `OPENWEATHER_API_KEY` - API key (required)

**Features:**
- Current weather
- Forecast data
- Historical weather

### 5. Expanded API Integration (25+ Sources)

**Service:** `backend/services/expanded_api_integration.py`

**Sources:**
- Transport (ANTT/DNIT)
- Trade (MDIC/SECEX)
- Energy (EPE/ANEEL)
- Employment (CAGED/IBGE)
- Construction (CBIC/IBGE)
- Industrial (ABDI/IBGE)
- Logistics (Port authorities)
- Regional (State APIs)

## Integration Manager

**Location:** `backend/app/core/integration_manager.py`

**Purpose:** Central coordinator for all integrations

**Key Methods:**
- `initialize_all()` - Initialize all services and clients
- `get_service(name)` - Get inner service by name
- `get_external_client(name)` - Get external client by name
- `refresh_all_external_data(start_date, end_date)` - Refresh all external data

**Usage:**
```python
from app.core.integration_manager import integration_manager

# Initialize all
await integration_manager.initialize_all()

# Get service
db_service = integration_manager.get_service('database')

# Refresh external data
results = await integration_manager.refresh_all_external_data()
```

## Health Check Endpoint

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T...",
  "version": "1.0.0",
  "service": "nova-corrente-api",
  "services": {
    "database": {
      "status": "healthy",
      "connected": true
    },
    "external_data": {
      "status": "healthy"
    }
  },
  "external_apis": {
    "inmet": {
      "status": "configured",
      "configured": true
    },
    "bacen": {
      "status": "configured",
      "configured": true
    }
  }
}
```

## Integration Endpoints

**Base Path:** `/api/v1/integration`

### GET `/api/v1/integration/status`
Get comprehensive integration status

### POST `/api/v1/integration/refresh`
Refresh all external data sources

### GET `/api/v1/integration/services`
List all available inner services

### GET `/api/v1/integration/external-clients`
List all available external API clients

## Starting the Backend

### Option 1: Using the Startup Script

```bash
scripts\start_backend.bat
```

### Option 2: Using Python Directly

```bash
cd backend
python run_server.py
```

### Option 3: Using Uvicorn Directly

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

## Environment Configuration

Create `backend/.env`:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=STOCK

# API
API_HOST=127.0.0.1
API_PORT=5000
API_RELOAD=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# External APIs (Optional)
INMET_API_KEY=
BACEN_API_KEY=
ANATEL_API_KEY=
OPENWEATHER_API_KEY=
```

## Troubleshooting

### Service Not Initializing

1. Check Python path - backend directory must be in `sys.path`
2. Check database connection - verify credentials in `.env`
3. Check logs - see startup logs for specific errors

### External API Not Working

1. Check API keys - verify in `.env` (optional for most)
2. Check network connectivity - ensure internet access
3. Check rate limits - APIs may have rate limiting
4. Use fallback data - some APIs have database fallbacks

### Import Errors

1. Verify backend directory structure
2. Check `__init__.py` files exist
3. Use absolute imports: `from backend.services...`

## Monitoring

### Startup Logs

When the server starts, you'll see:
```
🚀 Starting Nova Corrente API...
Initializing all services and external API clients...
✅ Database service initialized
✅ External data service initialized
...
✅ Startup complete - Status: healthy
📊 Services: 7/7 healthy
🌐 External APIs: 5/5 configured
```

### Health Check

Visit `http://localhost:5000/health` to see full status

### Integration Status

Visit `http://localhost:5000/api/v1/integration/status` for detailed integration status

## Next Steps

1. ✅ All services initialized
2. ✅ All external APIs configured
3. ✅ Health checks working
4. ✅ Integration endpoints available
5. ⚠️ Test with frontend
6. ⚠️ Monitor startup logs

---

**Status**: ✅ Backend Integration Complete
**Last Updated**: November 2025


