# Nova Corrente - Quick Start Guide ⚡

## Get Running in 5 Minutes!

---

## Prerequisites

✅ **Python 3.10+** installed  
✅ **Node.js 18+** & npm installed  
✅ **PostgreSQL 14+** installed and running  
✅ **Git** (to clone if needed)

---

## 🚀 Quick Start Steps

### Step 1: Setup PostgreSQL Database (2 minutes)

```sql
-- Open pgAdmin or psql and run:
CREATE USER nova_corrente WITH PASSWORD 'password';
CREATE DATABASE nova_corrente OWNER nova_corrente;
GRANT ALL PRIVILEGES ON DATABASE nova_corrente TO nova_corrente;
```

### Step 2: Configure Environment (30 seconds)

Edit `backend/.env` file:
```env
DATABASE_URL=postgresql://nova_corrente:password@localhost:5432/nova_corrente
```
*Replace `password` with your actual PostgreSQL password*

### Step 3A: Automated Setup (Windows) - **RECOMMENDED**

```cmd
SETUP_AND_RUN.bat
```

This will:
1. Install all Python dependencies
2. Run database migrations
3. Generate demo data
4. Start the Flask API server

**That's it!** API will be running at http://localhost:5000

### Step 3B: Manual Setup (All Platforms)

#### Install Backend Dependencies
```bash
cd backend
pip install -r requirements_deployment.txt
```

#### Run Database Migrations
```bash
cd backend
alembic upgrade head
```

Expected output:
```
INFO [alembic.runtime.migration] Running upgrade  -> 001, Initial PostgreSQL schema
```

#### Generate Demo Data
```bash
cd backend
python scripts/generate_demo_data.py
```

Expected output:
```
✅ Inserted 1096 calendar records
✅ Inserted 500 items
✅ Inserted ~27,000 demand records
...
✅ Demo data generation complete!
```

#### Start Backend API
```bash
cd backend
python run_flask_api.py
```

API will start at: http://localhost:5000

### Step 4: Start Frontend (2 minutes)

Open a **new terminal**:

```bash
cd frontend
npm install
npm run dev
```

Frontend will start at: http://localhost:3000

---

## ✅ Verify Everything Works

### 1. Check Backend Health
Open browser: http://localhost:5000/health

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-05T...",
  "version": "3.0.0"
}
```

### 2. Check API Endpoints
- Items: http://localhost:5000/api/v1/items?limit=5
- KPIs: http://localhost:5000/api/v1/analytics/kpis

### 3. Check Frontend Dashboard
Open browser: http://localhost:3000

You should see:
- ✅ KPI cards with real data
- ✅ Materials table with 500 items
- ✅ Filters working (Family, ABC Class)
- ✅ Click an item to see demand chart

---

## 🐳 Docker Quick Start (Alternative)

If you prefer Docker:

```bash
docker-compose up --build
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend API (port 5000)
- Frontend (port 3000)

**Note**: First startup takes 3-5 minutes for database initialization.

---

## 🎯 What You Get

### Dashboard Features
1. **KPI Cards**: Real-time metrics with trends
   - Total Demand
   - Stockout Rate
   - Forecast MAPE
   - Delayed Orders %
   - ABC A-Share
   - Total Records

2. **Materials Catalog**: 500 items with filtering
   - Filter by Family (ELECTRICAL, TELECOM, etc.)
   - Filter by ABC Class (A, B, C)
   - Pagination (20 items/page)
   - Click for details

3. **Demand Chart**: Time series visualization
   - Last 90 days of demand data
   - Actual vs. Forecast comparison
   - Confidence intervals
   - Summary statistics

4. **Alerts & Recommendations**
   - Real-time system alerts
   - Critical recommendations
   - Color-coded priorities

### Database Content
- **1,096** calendar dates (3 years)
- **500** items/materials
- **~27,000** demand records
- **~27,000** inventory records
- **30** daily KPIs
- **50** recommendations
- **30** alerts
- **1** admin user (username: `admin`, password: `admin123`)

---

## 🔧 Troubleshooting

### "Can't connect to PostgreSQL"
1. Check PostgreSQL is running:
   ```bash
   pg_isready -U nova_corrente
   ```
2. Verify password in `backend/.env`
3. Check database exists:
   ```bash
   psql -U nova_corrente -l
   ```

### "Alembic command not found"
```bash
pip install alembic
```

### "Module not found" errors
```bash
cd backend
pip install -r requirements_deployment.txt
```

### "Frontend can't connect to API"
1. Verify backend is running: http://localhost:5000/health
2. Check `frontend/.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```
3. Clear browser cache and reload

### "No data in dashboard"
1. Re-run demo data generator:
   ```bash
   python backend/scripts/generate_demo_data.py
   ```
2. Check API directly: http://localhost:5000/api/v1/items
3. Check browser console for errors (F12)

---

## 📱 Access URLs

| Service | URL | Notes |
|---------|-----|-------|
| **Frontend Dashboard** | http://localhost:3000 | Main UI |
| **Backend API** | http://localhost:5000 | REST API |
| **Health Check** | http://localhost:5000/health | System status |
| **Items API** | http://localhost:5000/api/v1/items | Materials catalog |
| **KPIs API** | http://localhost:5000/api/v1/analytics/kpis | Daily metrics |
| **PostgreSQL** | localhost:5432 | Database: `nova_corrente` |

---

## 🎓 Learn More

- **Complete Setup Guide**: `SETUP_GUIDE.md`
- **Implementation Details**: `REFACTORING_COMPLETE.md`
- **Project Specification**: `docs/proj/diagrams/Project.md`

---

## 🚦 System Status

After successful setup, you should see:

**Terminal 1 (Backend)**:
```
🚀 Nova Corrente Flask API Server
====================================
📡 Host: 127.0.0.1
🔌 Port: 5000
📚 Health: http://127.0.0.1:5000/health
====================================
 * Running on http://127.0.0.1:5000
```

**Terminal 2 (Frontend)**:
```
▲ Next.js 14.2.0
- Local:        http://localhost:3000
- Ready in 2.1s
```

---

## 💡 Tips

1. **Auto-refresh**: Frontend auto-refreshes data every 30s-5min depending on component
2. **Filters**: Try different families and ABC classes in materials table
3. **Charts**: Click any item in the table to see its demand time series
4. **API Explorer**: Visit http://localhost:5000/api/v1/items to see raw JSON

---

## ✅ Success!

If you see the dashboard with:
- ✅ KPI cards showing numbers
- ✅ Materials table with 500 items
- ✅ Alerts and recommendations panels

**Congratulations!** 🎉 Nova Corrente is running successfully!

---

*Quick Start Guide - Nova Corrente Analytics Platform*  
*Last Updated: November 5, 2025*
