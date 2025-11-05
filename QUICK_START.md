# Quick Start Guide - PostgreSQL Migration

## 🚀 Get Started in 5 Minutes

### Prerequisites

- Docker Desktop installed
- Python 3.11+
- Node.js 18+
- Git

---

## Step 1: PostgreSQL Setup (2 minutes)

```bash
# Start PostgreSQL via Docker
docker run --name postgres-nova-corrente \
  -e POSTGRES_USER=nova_corrente \
  -e POSTGRES_PASSWORD=devpassword123 \
  -e POSTGRES_DB=nova_corrente \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:14-alpine

# Verify it's running
docker ps | grep postgres-nova-corrente
```

---

## Step 2: Backend Setup (2 minutes)

```bash
cd backend

# Update .env with PostgreSQL credentials
# (already configured with defaults)

# Install dependencies
pip install -r requirements_deployment.txt

# Initialize Alembic (if not already done)
alembic init alembic

# Apply migrations (when migration files are created)
# alembic upgrade head

# Start Flask API
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

**Test API**:
```bash
curl http://localhost:5000/health
# Expected: {"status": "healthy", "database": "connected", ...}
```

---

## Step 3: Frontend Setup (1 minute)

```bash
cd frontend

# Install dependencies (if not already done)
npm install

# Start Next.js dev server
npm run dev
```

**Open browser**: http://localhost:3000

---

## Step 4: Load Demo Data (Optional)

```bash
# Generate synthetic demo data
python scripts/generate_demo_data.py

# Verify data loaded
docker exec -it postgres-nova-corrente psql -U nova_corrente -d nova_corrente \
  -c "SELECT COUNT(*) FROM core.dim_calendar;"
```

---

## Architecture Summary

```
┌─────────────────────────────────────────────┐
│         NEXT.JS (http://localhost:3000)      │
│  Dashboard | Materials | Forecasts | Alerts │
└─────────────────────┬───────────────────────┘
                      │ REST API
┌─────────────────────▼───────────────────────┐
│         FLASK (http://localhost:5000)        │
│  /health | /api/v1/items | /api/v1/kpis    │
└─────────────────────┬───────────────────────┘
                      │ SQL Queries
┌─────────────────────▼───────────────────────┐
│   POSTGRESQL (localhost:5432)               │
│  core.dim_item | analytics.forecasts        │
└─────────────────────────────────────────────┘
```

---

## Key Files & Locations

### Documentation
- **Complete Spec**: `docs/proj/diagrams/Project.md` (2,500+ lines)
- **Migration Summary**: `POSTGRES_MIGRATION_SUMMARY.md`
- **This Guide**: `QUICK_START.md`
- **Checklist**: `IMPLEMENTATION_CHECKLIST.md`

### Backend
- **Config**: `backend/app/config.py`, `backend/config/database_config.py`
- **Environment**: `backend/.env`
- **API**: `backend/api/enhanced_api.py`
- **Migrations**: `backend/alembic/versions/` (to be created)

### Frontend
- **Config**: `frontend/.env.local`
- **API Client**: `frontend/src/lib/api.ts`
- **Pages**: `frontend/src/app/` (dashboard, materials, etc.)

---

## Common Commands

### Database

```bash
# Connect to PostgreSQL
docker exec -it postgres-nova-corrente psql -U nova_corrente -d nova_corrente

# List schemas
\dn

# List tables in core schema
\dt core.*

# Describe table
\d+ core.dim_item

# Run query
SELECT COUNT(*) FROM core.fact_demand_daily;

# Exit psql
\q
```

### Backend

```bash
# Install dependencies
pip install -r requirements_deployment.txt

# Run Flask API (development)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000

# Run Flask API (production)
gunicorn -b 0.0.0.0:5000 -w 4 backend.api.enhanced_api:app

# Apply migrations
alembic upgrade head

# Create new migration
alembic revision -m "description"
```

### Frontend

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run tests
npm test

# Type check
npm run type-check
```

### Docker

```bash
# Start all services (production)
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild images
docker-compose build --no-cache
```

---

## Troubleshooting

### PostgreSQL Connection Error

**Error**: `FATAL: password authentication failed`

**Fix**:
```bash
# Update backend/.env with correct password
DATABASE_URL=postgresql://nova_corrente:devpassword123@localhost:5432/nova_corrente
```

### Flask API Not Starting

**Error**: `ModuleNotFoundError: No module named 'pydantic_settings'`

**Fix**:
```bash
pip install pydantic-settings
```

### Frontend API 404

**Error**: `Failed to fetch http://localhost:5000/api/v1/items`

**Fix**:
1. Ensure Flask is running: `curl http://localhost:5000/health`
2. Check `frontend/.env.local` has correct API URL
3. Restart Next.js dev server

### Database Schema Missing

**Error**: `relation "core.dim_item" does not exist`

**Fix**:
```bash
# Apply migrations
cd backend
alembic upgrade head
```

---

## Next Steps

1. ✅ Read **`docs/proj/diagrams/Project.md`** for complete specification
2. ✅ Follow **`IMPLEMENTATION_CHECKLIST.md`** for step-by-step tasks
3. ✅ Create Alembic migration with DDL from Project.md Section 3
4. ✅ Implement Flask API endpoints from Project.md Section 4
5. ✅ Build Next.js dashboard pages from Project.md Section 5
6. ✅ Set up ML pipeline from Project.md Section 6
7. ✅ Deploy via Docker Compose from Project.md Section 9

---

## Resources

- **PostgreSQL Docs**: https://www.postgresql.org/docs/14/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Next.js Docs**: https://nextjs.org/docs
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Recharts Examples**: https://recharts.org/en-US/examples

---

## Support

- **GitHub Issues**: https://github.com/novacorrente/gran-prix/issues
- **Documentation**: `docs/proj/diagrams/Project.md`
- **Email**: tech@novacorrente.com (replace with actual)

---

**Status**: ✅ Ready to Start  
**Estimated Time**: 5 weeks (full implementation)  
**Quick Demo Setup**: 5 minutes (this guide)  
**Last Updated**: 2025-11-05
