# PostgreSQL Migration - Implementation Checklist

## Phase 1: Database Setup (Week 1)

### PostgreSQL Installation
- [ ] Install PostgreSQL 14+ via Docker or native
  ```bash
  docker run --name postgres-nova-corrente \
    -e POSTGRES_USER=nova_corrente \
    -e POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD \
    -e POSTGRES_DB=nova_corrente \
    -p 5432:5432 \
    -v pgdata:/var/lib/postgresql/data \
    -d postgres:14
  ```
- [ ] Verify PostgreSQL is running: `docker ps`
- [ ] Test connection: `psql -U nova_corrente -h localhost -d nova_corrente`

### Alembic Migration Setup
- [ ] Install Alembic: `pip install alembic psycopg2-binary`
- [ ] Initialize Alembic: `alembic init alembic`
- [ ] Configure `alembic.ini` with DATABASE_URL
- [ ] Create initial migration: `alembic revision -m "initial_schema"`
- [ ] Copy DDL from `docs/proj/diagrams/Project.md` Section 3 into migration
- [ ] Apply migration: `alembic upgrade head`

### Schema Verification
- [ ] Check schemas created: `\dn` in psql
- [ ] List core tables: `\dt core.*`
- [ ] List analytics tables: `\dt analytics.*`
- [ ] Verify partitions: `\d+ core.fact_demand_daily`
- [ ] Check indexes: `\di core.*`

### Demo Data Generation (Optional)
- [ ] Run `scripts/generate_demo_data.py`
- [ ] Verify data loaded: `SELECT COUNT(*) FROM core.dim_calendar;`
- [ ] Check fact data: `SELECT COUNT(*) FROM core.fact_demand_daily;`

---

## Phase 2: Backend Refactor (Week 2)

### Configuration Updates
- [x] Update `backend/config/database_config.py` (PostgreSQL port 5432)
- [x] Update `backend/app/config.py` (DATABASE_URL, production flags)
- [x] Update `backend/.env` (PostgreSQL credentials)
- [ ] Update `backend/requirements_deployment.txt` to include:
  - `flask>=2.3.0`
  - `sqlalchemy>=2.0.0`
  - `psycopg2-binary>=2.9.0`
  - `alembic>=1.12.0`
  - `flask-cors>=4.0.0`
  - `flask-caching>=2.1.0`
  - `python-jose[cryptography]>=3.3.0`
  - `passlib[bcrypt]>=1.7.4`
  - `gunicorn>=21.0.0`

### API Endpoints Implementation
- [ ] Create `backend/api/v1/routes.py`
- [ ] Implement `/health` endpoint
- [ ] Implement `/api/v1/items` (GET with pagination)
- [ ] Implement `/api/v1/analytics/kpis` (GET with date filters)
- [ ] Implement `/api/v1/demand/timeseries` (GET)
- [ ] Implement `/api/v1/inventory/timeseries` (GET)
- [ ] Implement `/api/v1/forecasts` (GET)
- [ ] Implement `/api/v1/features` (GET)
- [ ] Implement `/api/v1/recommendations` (GET, PATCH)
- [ ] Implement `/api/v1/alerts` (GET, PATCH)
- [ ] Register blueprint in `backend/api/enhanced_api.py`

### Authentication & Security
- [ ] Create `backend/auth.py` with JWT functions
- [ ] Implement `create_token()` function
- [ ] Implement `@token_required` decorator
- [ ] Add RBAC checks (ADMIN, ANALYST, VIEWER)
- [ ] Create `support.users` seed data (admin user)

### Testing
- [ ] Test `/health`: `curl http://localhost:5000/health`
- [ ] Test `/api/v1/items`: `curl http://localhost:5000/api/v1/items?limit=10`
- [ ] Test authentication flow
- [ ] Create Postman collection for all endpoints
- [ ] Run integration tests

---

## Phase 3: Frontend Integration (Week 3)

### Configuration
- [x] Update `frontend/.env.local` (NEXT_PUBLIC_API_URL)
- [ ] Install dependencies:
  ```bash
  npm install swr recharts d3 date-fns @tremor/react framer-motion react-select react-csv react-hot-toast
  ```

### Dashboard Page
- [ ] Create `app/dashboard/page.tsx`
- [ ] Implement KPI cards component
- [ ] Implement demand trend chart (Recharts)
- [ ] Implement alerts list component
- [ ] Implement recommendations list component
- [ ] Test with real API data

### Material Pages
- [ ] Create `app/materials/page.tsx` (catalog with filters)
- [ ] Create `app/materials/[itemId]/page.tsx` (detail page)
- [ ] Implement tabs: Demand, Inventory, Forecasts, Features
- [ ] Create DemandChart component
- [ ] Create InventoryChart component
- [ ] Create ForecastChart component (with confidence intervals)
- [ ] Implement CSV export button

### Charts & Visualizations
- [ ] Configure Recharts responsive containers
- [ ] Add tooltips with date formatting (date-fns)
- [ ] Implement Framer Motion animations
- [ ] Test chart performance with 90-day datasets

### Data Fetching
- [ ] Update `frontend/src/lib/api.ts` hooks
- [ ] Implement `useKPIs()` hook with SWR
- [ ] Implement `useForecasts()` hook
- [ ] Implement `useDemandTimeSeries()` hook
- [ ] Test caching behavior

---

## Phase 4: ML Pipeline (Week 4)

### Offline ML Pipeline
- [ ] Create `ml_pipeline/main.py`
- [ ] Implement data extraction from PostgreSQL
- [ ] Implement feature engineering:
  - [ ] Lag features (7d, 14d, 30d)
  - [ ] Rolling statistics (mean, std)
  - [ ] Calendar features (holidays, weekday)
  - [ ] Economic indicators (optional)
- [ ] Implement Prophet forecasting loop
- [ ] Export forecasts to `output/forecasts.parquet`
- [ ] Export features to `output/features.parquet`

### ETL Load Scripts
- [ ] Create `etl/load_ml_outputs.py`
- [ ] Implement Parquet → PostgreSQL loader for forecasts
- [ ] Implement JSONB transformation for features
- [ ] Add materialized view refresh logic
- [ ] Test with sample Parquet files

### KPI Calculation
- [ ] Create `etl/calculate_kpis.sql`
- [ ] Implement stockout rate calculation
- [ ] Implement ABC-A share calculation
- [ ] Implement delayed orders percentage
- [ ] Schedule as cron job: `0 2 * * * psql -f calculate_kpis.sql`

---

## Phase 5: Production Deployment (Week 5)

### Docker Setup
- [ ] Create `backend/Dockerfile.flask`
- [ ] Create `frontend/Dockerfile.nextjs`
- [ ] Create `docker-compose.prod.yml`
- [ ] Configure environment variables for production
- [ ] Set strong `SECRET_KEY` and `DB_PASSWORD`

### Build & Deploy
- [ ] Build images: `docker-compose -f docker-compose.prod.yml build`
- [ ] Start services: `docker-compose -f docker-compose.prod.yml up -d`
- [ ] Verify PostgreSQL: `docker logs nova-corrente-db`
- [ ] Verify Flask API: `curl http://localhost:5000/health`
- [ ] Verify Next.js: `curl http://localhost:3000`

### Health Checks & Monitoring
- [ ] Configure PostgreSQL health check in docker-compose
- [ ] Add Flask `/health` endpoint monitoring
- [ ] Set up log aggregation (optional: ELK stack)
- [ ] Configure backup script: `pg_dump` daily to S3

### Testing & Validation
- [ ] Run end-to-end test suite
- [ ] Test dashboard page loads in < 2s
- [ ] Test forecast chart renders correctly
- [ ] Test CSV export functionality
- [ ] Test authentication & RBAC
- [ ] Verify audit logs are populated
- [ ] Load test with 100 concurrent requests (optional: k6, Locust)

---

## Post-Deployment (Week 6+)

### Monitoring
- [ ] Set up PostgreSQL monitoring: `pg_stat_statements`, `pg_stat_activity`
- [ ] Monitor API response times (Flask logging + APM)
- [ ] Monitor cache hit rates (Flask-Caching metrics)
- [ ] Set up alerts for slow queries (> 100ms)

### Optimization
- [ ] Analyze slow queries with `EXPLAIN ANALYZE`
- [ ] Add missing indexes based on query patterns
- [ ] Optimize materialized view refresh schedule
- [ ] Tune PostgreSQL config: `shared_buffers`, `work_mem`

### Documentation
- [ ] Update README with setup instructions
- [ ] Create API documentation (Swagger/OpenAPI)
- [ ] Document dashboard usage for end-users
- [ ] Create runbook for common operations

---

## Rollback Plan (If Needed)

### Revert to Legacy System
- [ ] Keep legacy MySQL/SQLite database accessible
- [ ] Maintain feature flag: `ENABLE_LEGACY_MYSQL=true`
- [ ] Document rollback steps in `docs/ROLLBACK.md`
- [ ] Test rollback procedure in staging environment

---

**Status**: Implementation in progress  
**Current Phase**: Phase 1 (Database Setup)  
**Next Milestone**: Alembic migration applied, schema verified  
**Last Updated**: 2025-11-05
