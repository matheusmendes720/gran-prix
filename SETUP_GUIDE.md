# Nova Corrente - Complete Setup Guide

## PostgreSQL Refactoring & Full-Stack Analytics Platform

This guide covers the complete setup for the **Nova Corrente** supply-chain analytics platform after the PostgreSQL refactoring.

---

## 📋 Architecture Overview

### Technology Stack
- **Backend**: Flask 2.3+ (Python) - Read-only REST API
- **Database**: PostgreSQL 14+ with partitioning
- **Frontend**: Next.js 14 (React, TypeScript, Tailwind CSS)
- **Caching**: Redis (optional for production)
- **Migration**: Alembic for database versioning

### Database Schema
- **4 Schemas**: `core`, `analytics`, `support`, `staging`
- **Star Schema Design**: 5 dimension tables + 2 partitioned fact tables
- **Partitioning**: Monthly range partitions for scalability
- **Indexes**: B-tree + GIN (for JSONB columns)

---

## 🚀 Quick Start (Windows)

### Option 1: Automated Setup (Recommended)

1. **Install PostgreSQL**
   - Download: https://www.postgresql.org/download/windows/
   - Install with default settings (port 5432)
   - Set password for `postgres` user

2. **Create Database & User**
   ```sql
   -- Run in pgAdmin or psql
   CREATE USER nova_corrente WITH PASSWORD 'password';
   CREATE DATABASE nova_corrente OWNER nova_corrente;
   GRANT ALL PRIVILEGES ON DATABASE nova_corrente TO nova_corrente;
   ```

3. **Update `.env` File**
   - Open `backend/.env`
   - Update `DB_PASSWORD=` with your actual password
   - Save the file

4. **Run Automated Setup**
   ```cmd
   SETUP_AND_RUN.bat
   ```

   This script will:
   - Install Python dependencies
   - Run database migrations
   - Generate demo data
   - Start the Flask API server

### Option 2: Manual Setup

#### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements_deployment.txt
```

#### Step 2: Configure Database

Edit `backend/.env`:
```env
DATABASE_URL=postgresql://nova_corrente:YOUR_PASSWORD@localhost:5432/nova_corrente
```

#### Step 3: Run Migrations

```bash
cd backend
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial_postgres_schema, Initial PostgreSQL schema with partitioning
```

#### Step 4: Generate Demo Data

```bash
cd backend
python scripts/generate_demo_data.py
```

Expected output:
```
✅ Inserted 1096 calendar records
✅ Inserted 5 regions
✅ Inserted 10 sites
✅ Inserted 50 suppliers
✅ Inserted 500 items
✅ Inserted ~27,000 demand records
✅ Inserted ~27,000 inventory records
...
```

#### Step 5: Start Backend API

```bash
cd backend
python run_flask_api.py
```

API will be available at: http://localhost:5000

#### Step 6: Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## 🐳 Docker Setup

### Development with Docker Compose

```bash
docker-compose up --build
```

Services:
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`
- **Backend API**: `localhost:5000`
- **Frontend**: `localhost:3000`

### Production Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📊 Database Schema Details

### Core Schema (Operational Data)

#### Dimension Tables
1. **dim_calendar** - Date dimension (3 years)
2. **dim_item** - Materials/SKUs catalog (500+ items)
3. **dim_site** - Distribution centers/warehouses
4. **dim_supplier** - Supplier master data
5. **dim_region** - Geographic regions

#### Fact Tables (Partitioned by Month)
1. **fact_demand_daily** - Daily demand transactions
2. **fact_inventory_daily** - Daily inventory snapshots

### Analytics Schema (Precomputed ML Results)

1. **forecasts** - ML forecast predictions with confidence intervals
2. **features_store** - Feature vectors for ML models (JSONB)
3. **kpis_daily** - Daily aggregated KPIs
4. **recommendations** - System-generated recommendations
5. **alerts** - Automated alerts (stockouts, delays, etc.)

### Support Schema

1. **users** - Application users (RBAC: ADMIN, ANALYST, VIEWER)
2. **audit_logs** - Comprehensive audit trail

---

## 🔌 API Endpoints

### Health Check
```
GET /health
```

### Items/Materials
```
GET /api/v1/items?family=ELECTRICAL&abc_class=A&limit=20&offset=0
GET /api/v1/items/{item_id}
```

### Analytics KPIs
```
GET /api/v1/analytics/kpis?start_date=2025-01-01&end_date=2025-01-31
```

### Time Series
```
GET /api/v1/demand/timeseries?item_id=123&start_date=2025-01-01
GET /api/v1/inventory/timeseries?item_id=123&start_date=2025-01-01
```

### Forecasts
```
GET /api/v1/forecasts?item_id=123&horizon_days=30
```

### Recommendations
```
GET /api/v1/recommendations?status=PENDING&priority=CRITICAL
PATCH /api/v1/recommendations/{id}
```

### Alerts
```
GET /api/v1/alerts?status=NEW&severity=CRITICAL
PATCH /api/v1/alerts/{id}
```

---

## 🎨 Frontend Components

### Created Components

1. **KPIDashboard** (`src/components/KPIDashboard.tsx`)
   - Real-time KPI cards with trends
   - Auto-refreshes every 5 minutes

2. **MaterialsTable** (`src/components/MaterialsTable.tsx`)
   - Filterable materials catalog
   - ABC class filtering
   - Pagination support

3. **DemandChart** (`src/components/DemandChart.tsx`)
   - Time series visualization with Recharts
   - Actual vs. Forecast comparison
   - Confidence intervals

### API Client (`src/lib/api-client.ts`)
- Type-safe TypeScript API client
- All endpoints covered

### SWR Hooks (`src/hooks/use-api.ts`)
- Real-time data fetching
- Auto-revalidation
- Caching strategy

---

## 🗂️ File Structure

```
gran-prix/
├── backend/
│   ├── alembic/
│   │   └── versions/
│   │       └── 001_initial_postgres_schema.py  ← Migration file
│   ├── api/
│   │   ├── enhanced_api.py                     ← Flask app (main)
│   │   └── v1/
│   │       └── routes.py                       ← API v1 routes
│   ├── scripts/
│   │   ├── setup_database.py                   ← Setup automation
│   │   └── generate_demo_data.py               ← Demo data generator
│   ├── .env                                     ← Environment config
│   ├── alembic.ini                              ← Alembic config
│   ├── Dockerfile                               ← Backend container
│   ├── run_flask_api.py                         ← Flask runner
│   └── requirements_deployment.txt              ← Python deps
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── page.tsx                         ← Main dashboard
│   │   ├── components/
│   │   │   ├── KPIDashboard.tsx                 ← KPI cards
│   │   │   ├── MaterialsTable.tsx               ← Items table
│   │   │   └── DemandChart.tsx                  ← Time series chart
│   │   ├── hooks/
│   │   │   └── use-api.ts                       ← SWR hooks
│   │   └── lib/
│   │       └── api-client.ts                    ← API client
│   ├── .env.local                               ← Frontend config
│   ├── Dockerfile                               ← Frontend container
│   └── package.json                             ← Node deps
│
├── docker-compose.yml                           ← Dev environment
├── SETUP_AND_RUN.bat                            ← Windows quick start
└── SETUP_GUIDE.md                               ← This file
```

---

## ✅ Verification Checklist

After setup, verify everything is working:

### Backend Verification

1. **Database Connection**
   ```bash
   curl http://localhost:5000/health
   ```
   Expected: `{"status": "healthy", "database": "connected"}`

2. **Check Items**
   ```bash
   curl http://localhost:5000/api/v1/items?limit=5
   ```
   Expected: JSON array with 5 items

3. **Check KPIs**
   ```bash
   curl http://localhost:5000/api/v1/analytics/kpis
   ```
   Expected: JSON array with daily KPIs

### Frontend Verification

1. Open http://localhost:3000
2. Verify KPI cards load with data
3. Verify materials table displays items
4. Click on an item to see demand chart

### Database Verification

```sql
-- Connect to PostgreSQL
psql -U nova_corrente -d nova_corrente

-- Check schemas
\dn

-- Check tables
\dt core.*
\dt analytics.*

-- Check data counts
SELECT COUNT(*) FROM core.dim_item;          -- Should be 500
SELECT COUNT(*) FROM core.fact_demand_daily; -- Should be ~27,000

-- Check partitions
SELECT tablename FROM pg_tables 
WHERE schemaname = 'core' 
AND tablename LIKE 'fact_demand_daily_%';
```

---

## 🐛 Troubleshooting

### Issue: "Could not connect to PostgreSQL"

**Solution**:
1. Check PostgreSQL is running: `pg_isready -U nova_corrente`
2. Verify `.env` has correct `DATABASE_URL`
3. Ensure database and user exist

### Issue: "Alembic migration failed"

**Solution**:
1. Check if database exists: `psql -U nova_corrente -l`
2. Reset migration: `alembic downgrade base` then `alembic upgrade head`
3. Check `alembic.ini` has correct connection string

### Issue: "Frontend can't connect to API"

**Solution**:
1. Verify backend is running on port 5000
2. Check `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:5000`
3. Check CORS settings in `backend/.env`

### Issue: "No data showing in dashboard"

**Solution**:
1. Run demo data generator: `python backend/scripts/generate_demo_data.py`
2. Check API responses directly: `curl http://localhost:5000/api/v1/items`
3. Check browser console for errors

---

## 📝 Production Deployment Notes

### Environment Variables

Update these for production:

```env
# Security
SECRET_KEY=<generate-64-char-random-string>
DB_PASSWORD=<strong-password>

# Database
DATABASE_URL=postgresql://nova_corrente:<password>@<host>:5432/nova_corrente

# Redis (optional, for caching)
REDIS_URL=redis://<host>:6379/0
USE_REDIS_CACHE=true

# API Settings
API_RELOAD=false
EXTERNAL_APIS_ENABLED=false
ENABLE_ML_PROCESSING=false
```

### Performance Tuning

1. **PostgreSQL**: Tune `work_mem`, `shared_buffers` for large datasets
2. **Connection Pooling**: Already configured (pool_size=10)
3. **Indexes**: All critical indexes created by migration
4. **Partitioning**: Add more monthly partitions as needed

### Security

1. **Authentication**: JWT tokens configured (change SECRET_KEY)
2. **RBAC**: Three roles (ADMIN, ANALYST, VIEWER)
3. **CORS**: Update `CORS_ORIGINS` for production domains
4. **Audit Logs**: All user actions logged to `support.audit_logs`

---

## 📚 Additional Resources

- **Alembic Documentation**: https://alembic.sqlalchemy.org/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **PostgreSQL Partitioning**: https://www.postgresql.org/docs/14/ddl-partitioning.html

---

## 🎯 Next Steps

1. ✅ Database migrations complete
2. ✅ Demo data generated
3. ✅ API endpoints working
4. ✅ Frontend dashboard created
5. ⏭️ Connect to real data sources (ETL pipelines)
6. ⏭️ Train ML models and populate forecasts
7. ⏭️ Set up monitoring and alerting
8. ⏭️ Deploy to production environment

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs in `backend/logs/`
3. Check PostgreSQL logs for database issues
4. Verify all environment variables are set correctly

---

**Status**: ✅ PostgreSQL refactoring complete and ready for use!

Last updated: November 5, 2025
