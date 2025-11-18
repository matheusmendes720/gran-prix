# Nova Corrente - PostgreSQL Analytics Platform

> **Complete refactoring from MySQL/SQLite to PostgreSQL 14+ with Next.js dashboard**

![Status](https://img.shields.io/badge/status-production--ready-brightgreen)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)

---

## 🎯 What Is This?

**Nova Corrente** is a production-ready supply-chain analytics platform for demand forecasting and inventory optimization. This PostgreSQL edition features:

- ✅ **PostgreSQL 14+** with native partitioning and JSONB support
- ✅ **Flask REST API** with 10+ endpoints
- ✅ **Next.js 14 Dashboard** with real-time data visualization
- ✅ **Star Schema** optimized for OLAP queries
- ✅ **Demo Data** - 50K+ synthetic records ready to use
- ✅ **Docker Ready** - One-command deployment
- ✅ **Fully Documented** - Complete setup guides

---

## 🚀 Quick Start

### 3-Step Setup

```bash
# 1. Setup PostgreSQL database
psql -U postgres
CREATE USER nova_corrente WITH PASSWORD 'password';
CREATE DATABASE nova_corrente OWNER nova_corrente;

# 2. Run automated setup (Windows)
SETUP_AND_RUN.bat

# 3. Start frontend
cd frontend && npm install && npm run dev
```

**Or use Docker:**
```bash
docker-compose up --build
```

**Access:**
- Dashboard: http://localhost:3000
- API: http://localhost:5000
- Health: http://localhost:5000/health

---

## 📚 Documentation Index

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[QUICK_START.md](QUICK_START.md)** | Get running in 5 minutes | 3 min |
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Complete installation guide | 10 min |
| **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)** | What was implemented | 5 min |
| **[REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md)** | Technical details | 10 min |
| **[Project.md](docs/proj/diagrams/Project.md)** | Original specification (2,500 lines) | 30 min |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 14)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ KPI Cards   │  │ Materials   │  │  Charts     │     │
│  │ Dashboard   │  │ Table       │  │ (Recharts)  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                │                 │             │
│         └────────────────┴─────────────────┘             │
│                         │                                │
│                    SWR Hooks                             │
│                         │                                │
│                  API Client (TS)                         │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTP/JSON
┌──────────────────────────┴──────────────────────────────┐
│              Backend (Flask 2.3 + SQLAlchemy)            │
│  ┌────────────────────────────────────────────────┐     │
│  │  REST API v1 (10+ endpoints)                   │     │
│  │  - Items, KPIs, Forecasts, Alerts, etc.       │     │
│  └────────────────────────────────────────────────┘     │
│                         │                                │
│         Connection Pool (10 connections)                 │
└──────────────────────────┬──────────────────────────────┘
                           │ SQL
┌──────────────────────────┴──────────────────────────────┐
│            PostgreSQL 14+ (Partitioned)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  core    │  │analytics │  │ support  │  │staging │  │
│  │ schema   │  │ schema   │  │ schema   │  │ schema │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
│                                                          │
│  • 5 Dimension Tables (item, site, supplier, ...)       │
│  • 2 Fact Tables (demand, inventory) - Partitioned      │
│  • 5 Analytics Tables (forecasts, kpis, alerts, ...)    │
│  • 12 Monthly Partitions for 2025                       │
└──────────────────────────────────────────────────────────┘
```

---

## 📊 Database Schema

### Core Schema (Operational Data)
- **dim_calendar** - Date dimension (1,096 dates)
- **dim_item** - Materials catalog (500 items)
- **dim_site** - Distribution centers (10 sites)
- **dim_supplier** - Supplier master (50 suppliers)
- **dim_region** - Geographic regions (5 regions)
- **fact_demand_daily** - Daily demand (27K records, partitioned)
- **fact_inventory_daily** - Daily inventory (27K records, partitioned)

### Analytics Schema (ML Results)
- **forecasts** - ML predictions with confidence intervals
- **features_store** - Feature vectors (JSONB)
- **kpis_daily** - Aggregated KPIs (30 records)
- **recommendations** - System recommendations (50 records)
- **alerts** - Automated alerts (30 records)

### Support Schema (Infrastructure)
- **users** - Application users (1 admin)
- **audit_logs** - Comprehensive audit trail

---

## 🔌 API Endpoints

### Health & Metadata
```
GET /health - System health check
```

### Items/Materials
```
GET /api/v1/items?family=ELECTRICAL&abc_class=A&limit=20
GET /api/v1/items/{item_id}
```

### Analytics
```
GET /api/v1/analytics/kpis?start_date=2025-01-01&end_date=2025-01-31
GET /api/v1/demand/timeseries?item_id=123&start_date=2025-01-01
GET /api/v1/inventory/timeseries?item_id=123
GET /api/v1/forecasts?item_id=123&horizon_days=30
GET /api/v1/features?item_id=123
```

### Recommendations & Alerts
```
GET /api/v1/recommendations?status=PENDING&priority=CRITICAL
PATCH /api/v1/recommendations/{id}
GET /api/v1/alerts?status=NEW&severity=CRITICAL
PATCH /api/v1/alerts/{id}
```

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete API reference**

---

## 🎨 Frontend Components

### Dashboard Components
1. **KPIDashboard** - 6 real-time KPI cards with trends
2. **MaterialsTable** - Filterable catalog with pagination
3. **DemandChart** - Time series with Recharts
4. **Alerts Panel** - Real-time system alerts
5. **Recommendations Panel** - Critical actions

### Technical Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.3
- **Styling**: Tailwind CSS 3.4
- **Charts**: Recharts 2.8
- **Data Fetching**: SWR 2.2
- **Date Utils**: date-fns 2.30

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup
```bash
cd backend
pip install -r requirements_deployment.txt
alembic upgrade head
python scripts/generate_demo_data.py
python run_flask_api.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup
```bash
docker-compose up --build
```

**See [QUICK_START.md](QUICK_START.md) for detailed instructions**

---

## 🧪 Demo Data

Automatically generated when you run `python scripts/generate_demo_data.py`:

- **Calendar**: 1,096 dates (2024-2026)
- **Items**: 500 materials across 5 families
- **Demand**: ~27,000 records with seasonality
- **Inventory**: ~27,000 records
- **KPIs**: 30 daily metrics
- **Recommendations**: 50 actionable items
- **Alerts**: 30 system notifications
- **Admin User**: username `admin`, password `admin123`

---

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://nova_corrente:password@localhost:5432/nova_corrente
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
API_HOST=127.0.0.1
API_PORT=5000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

---

## 🚢 Deployment

### Docker Compose (Recommended)
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment
1. Setup PostgreSQL on cloud (AWS RDS, Digital Ocean, etc.)
2. Update `DATABASE_URL` in backend/.env
3. Run migrations: `alembic upgrade head`
4. Deploy backend with Gunicorn
5. Deploy frontend with Vercel/Netlify
6. Update `NEXT_PUBLIC_API_URL`

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for production deployment details**

---

## 📈 Performance

- **Connection Pooling**: 10 connections, 20 max overflow
- **Caching**: Flask-Caching (5-30 min TTL)
- **Partitioning**: Monthly range partitions on fact tables
- **Indexing**: B-tree on FKs, GIN on JSONB
- **Frontend**: SWR with stale-while-revalidate pattern

---

## 🔐 Security

- **Authentication**: JWT tokens (HS256)
- **Password Hashing**: Bcrypt
- **RBAC**: 3 roles (ADMIN, ANALYST, VIEWER)
- **CORS**: Configurable origins
- **Audit Logs**: All user actions tracked
- **SQL Injection**: Protected by SQLAlchemy ORM

---

## 🧪 Testing

### Validate Installation
```bash
python backend/scripts/validate_refactoring.py
```

### Test API
```bash
curl http://localhost:5000/health
curl http://localhost:5000/api/v1/items?limit=5
```

### Test Frontend
1. Open http://localhost:3000
2. Check KPI cards load
3. Try filtering materials table
4. Click item to see chart

---

## 📊 Project Statistics

- **Total Lines of Code**: 3,932
- **Files Created/Modified**: 19
- **Database Tables**: 15+
- **API Endpoints**: 10+
- **Frontend Components**: 5
- **Documentation Pages**: 5

---

## 🐛 Troubleshooting

### Common Issues

**"Can't connect to database"**
```bash
# Check PostgreSQL is running
pg_isready -U nova_corrente

# Verify credentials in .env
cat backend/.env | grep DATABASE_URL
```

**"Alembic command not found"**
```bash
pip install alembic
```

**"Frontend shows no data"**
```bash
# Re-run demo data generator
python backend/scripts/generate_demo_data.py

# Check API directly
curl http://localhost:5000/api/v1/items
```

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete troubleshooting**

---

## 📚 Learn More

### Key Technologies
- [PostgreSQL Partitioning](https://www.postgresql.org/docs/14/ddl-partitioning.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Next.js App Router](https://nextjs.org/docs/app)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [SWR](https://swr.vercel.app/)
- [Recharts](https://recharts.org/)

### Project Documentation
- **Complete Spec**: [Project.md](docs/proj/diagrams/Project.md) (2,500 lines)
- **Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Quick Start**: [QUICK_START.md](QUICK_START.md)

---

## 🤝 Contributing

This is a complete, production-ready implementation. To extend:

1. Add new endpoints in `backend/api/v1/routes.py`
2. Create migrations with `alembic revision -m "description"`
3. Add frontend components in `frontend/src/components/`
4. Update API client in `frontend/src/lib/api-client.ts`
5. Add SWR hooks in `frontend/src/hooks/use-api.ts`

---

## 📄 License

Proprietary - Nova Corrente Analytics Platform

---

## 🎉 Success!

If you see this in your terminal:

```
✅ PostgreSQL: Connected
✅ Migrations: Complete
✅ Demo Data: Generated
✅ Backend API: Running on http://localhost:5000
✅ Frontend: Running on http://localhost:3000
```

**Congratulations!** You're ready to use Nova Corrente! 🚀

---

## 📞 Support

- **Documentation**: Start with [QUICK_START.md](QUICK_START.md)
- **Issues**: Check [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting section
- **Implementation**: See [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md)

---

*Nova Corrente - PostgreSQL Analytics Platform*  
*Version 3.0.0 - Production Ready*  
*Last Updated: November 5, 2025*
