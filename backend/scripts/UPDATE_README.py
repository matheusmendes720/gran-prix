"""
Script to update README.md with new project structure.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent

README_CONTENT = """# Nova Corrente - Demand Forecasting System

**Production-Ready Full-Stack Application**

A comprehensive demand forecasting system with ML/DL models, Next.js dashboard, and FastAPI backend.

---

## 🏗️ Project Structure

```
gran_prix/
├── frontend/              # Next.js Frontend (React + TypeScript)
│   ├── src/
│   │   ├── app/           # Next.js 13+ App Router
│   │   ├── components/     # React components
│   │   ├── lib/            # API client & utilities
│   │   └── hooks/          # Custom React hooks
│   └── public/             # Static assets
│
├── backend/                # Python Backend (FastAPI)
│   ├── app/               # FastAPI application
│   │   ├── api/v1/        # REST API routes
│   │   ├── core/          # Business logic
│   │   └── config.py      # Configuration
│   ├── ml/                # ML/DL module
│   │   ├── models/        # Model implementations
│   │   │   ├── arima/
│   │   │   ├── prophet/
│   │   │   ├── lstm/
│   │   │   └── ensemble/
│   │   ├── data/          # Data loading
│   │   ├── training/      # Training pipeline
│   │   ├── inference/     # Prediction service
│   │   └── evaluation/    # Model evaluation
│   ├── pipelines/         # Data processing
│   │   ├── data_ingestion/
│   │   ├── data_processing/
│   │   └── feature_engineering/
│   └── scripts/           # Utility scripts
│
├── shared/                 # Shared types/schemas
├── infrastructure/         # Docker, K8s configs
├── docs/                   # Documentation
│   ├── guides/            # User guides
│   └── archives/          # Topic-organized reports
├── config/                 # Configuration files
├── data/                   # Data storage
├── models/                 # Trained models
└── reports/                # Generated reports
```

---

## 🚀 Quick Start

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m app.main
# API available at http://localhost:5000
# Docs at http://localhost:5000/docs
```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
# Frontend at http://localhost:3000
```

### Docker (All Services)

```bash
docker-compose up -d
# Backend: http://localhost:5000
# Frontend: http://localhost:3000
```

---

## 📚 Documentation

- **Main README**: This file
- **Reorganization**: `README_REORGANIZATION.md`
- **Migration Status**: `MIGRATION_STATUS.md`
- **Complete Guide**: `PROJECT_REORGANIZATION_COMPLETE.md`
- **Archive Index**: `docs/archives/ARCHIVE_INDEX.md`

---

## 🎯 Features

- ✅ **Multiple ML Models**: ARIMA, Prophet, LSTM, Ensemble
- ✅ **REST API**: FastAPI with automatic documentation
- ✅ **Next.js Dashboard**: Modern React dashboard
- ✅ **Data Pipelines**: Automated data processing
- ✅ **Archive System**: Topic-organized reports
- ✅ **Docker Ready**: Multi-container deployment

---

## 📊 Key Components

### ML Models
- **ARIMA/SARIMA**: Statistical time series forecasting
- **Prophet**: Facebook's forecasting tool
- **LSTM**: Deep learning for complex patterns
- **Ensemble**: Weighted combination of all models

### API Endpoints
- `/health` - Health check
- `/api/v1/forecasts` - Forecast generation
- `/api/v1/inventory` - Inventory management
- `/api/v1/metrics` - System metrics

### Frontend Pages
- `/` - Home page
- `/dashboard/forecasts` - Forecast visualization
- `/dashboard/inventory` - Inventory management
- `/dashboard/analytics` - Analytics dashboard

---

## 🛠️ Development

### Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Run Tests

```bash
cd backend
pytest tests/
```

### Organize Reports

```bash
python backend/scripts/organize_reports.py
```

---

## 📝 Configuration

- **Backend Config**: `backend/.env` (copy from `.env.example`)
- **Frontend Config**: `frontend/.env.local`
- **ML Config**: `backend/ml/config.yaml`
- **Pipeline Config**: `config/datasets_config.json`

---

## 🚀 Deployment

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

### Quick Docker Deployment

```bash
docker-compose up -d
```

### Production Deployment

1. Set environment variables
2. Build Docker images
3. Deploy with docker-compose or Kubernetes

---

## 📊 Archive System

Reports are automatically organized by:
- **Topic**: pipeline, datasets, models, dashboard, api, etc.
- **Type**: reports, success, benchmarks, changelogs, etc.
- **Timeline**: by year, month, quarter

Access archive index at: `docs/archives/ARCHIVE_INDEX.md`

---

## 🎉 Status

✅ **Production Ready** - Fully reorganized and ready for deployment!

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-01

---

*Built with Next.js, FastAPI, and ML/DL models*
"""

def update_readme():
    """Update README.md with new structure."""
    readme_path = BASE_DIR / "README.md"
    
    # Backup original
    if readme_path.exists():
        backup_path = BASE_DIR / "README.md.backup"
        if not backup_path.exists():
            shutil.copy2(str(readme_path), str(backup_path))
            print(f"[OK] Backed up original README.md")
    
    # Write new README
    readme_path.write_text(README_CONTENT, encoding="utf-8")
    print(f"[OK] Updated README.md with new structure")

if __name__ == "__main__":
    import shutil
    update_readme()
    print("\n[SUCCESS] README.md updated!")





