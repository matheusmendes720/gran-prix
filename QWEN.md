# 🎯 Nova Corrente - Demand Forecasting & Analytics System

## Project Overview

Nova Corrente is a comprehensive demand forecasting and analytics platform for a telecom company in Salvador, Brazil. The system is designed to provide predictive analytics, demand forecasting, inventory management, and business intelligence capabilities for the telecom industry.

## Architecture

The system follows a modern full-stack architecture with:

- **Frontend**: Next.js 14 application with TypeScript, Tailwind CSS, and data visualization libraries
- **Backend**: FastAPI (primary) with additional Flask APIs for specific services
- **ML/DL Models**: ARIMA, Prophet, LSTM, and ensemble models for forecasting
- **Database**: SQLite with potential for PostgreSQL in production
- **Containerization**: Docker and Docker Compose for deployment

## Project Structure

```
gran-prix/
├── backend/                 # FastAPI backend (primary)
│   ├── api/                 # API routes
│   ├── app/                 # FastAPI application
│   ├── services/            # Business logic services
│   ├── ml/                  # ML model implementations
│   ├── data/                # Data processing modules
│   └── run_server.py        # Server startup script
├── demand_forecasting/      # Flask API (secondary)
│   ├── api.py              # Flask API endpoints
│   ├── pipeline.py         # Forecasting pipeline
│   ├── models/             # ML model implementations
│   └── data/               # Data processing modules
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # Main dashboard pages
│   │   ├── components/     # React components
│   │   └── lib/            # API client and utilities
├── data/                   # Data files and datasets
├── docs/                   # Documentation
├── docker-compose.yml      # Container orchestration
└── infrastructure/         # Deployment configs
```

## Key Features

### Analytics Dashboard
- 5-tab analytics interface with geographic, formulas, clustering, models, and prescriptive tabs
- Interactive Brazil map with state-level analytics
- K-means clustering for equipment failure prediction
- LLM-powered prescriptive recommendations

### Advanced ML/AI
- Ensemble forecasting (ARIMA + Prophet + LSTM)
- Equipment failure prediction
- Tower performance clustering
- Regional demand forecasting
- Cost optimization recommendations

### Business Intelligence
- Real-time KPIs (Stockout Rate, MAPE, Savings)
- Supplier performance tracking
- SLA penalty monitoring
- Regional inventory optimization

## Building and Running

### Prerequisites
- Python 3.8+
- Node.js 18+
- Docker and Docker Compose (for containerized deployment)
- Pandas, NumPy, scikit-learn

### Installation

1. **Clone Repository**
```bash
git clone <repository-url>
cd gran-prix
```

2. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Install Frontend Dependencies**
```bash
cd frontend
npm install
```

### Run Development Server

**Option 1: Separate Services**
- Terminal 1 - Backend API:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

- Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

**Option 2: Docker Compose (Production)**
```bash
docker-compose up --build
```

**Open Browser:**
```
http://localhost:3000/main
```

## API Endpoints

### Primary API (FastAPI Backend)
- `GET /docs` - API Documentation
- `GET /health` - Health check
- `/api/v1/` - Main API endpoints for all services

### Secondary API (Flask Demand Forecasting)
- `GET /api/kpis` - Real-time KPIs
- `GET /api/forecast` - Demand forecasting
- `GET /api/alerts` - Inventory alerts
- `GET /api/forecast/30days` - 30-day forecast
- `GET /api/clustering` - Clustering endpoints
- `GET /api/prescriptive/recommendations` - LLM recommendations
- `GET /api/geographic/data` - Geographic data
- `GET /api/models/performance` - ML model comparison

## Development Conventions

### Code Style
- Python: Follow PEP 8 style guidelines
- TypeScript: Use TypeScript with strict mode
- Documentation: Include docstrings for all functions and classes
- Logging: Use structured logging with appropriate levels

### Data Processing
- Data validation and cleaning pipeline
- Feature engineering with external factors (climate, economic, 5G coverage)
- 125+ engineered features for comprehensive analysis

### Testing
- Unit tests for all core functions
- Integration tests for API endpoints
- Model validation and performance testing

## Datasets

The system includes 33 datasets with complete technical documentation:
- Zenodo Milan Telecom (public telecom + weather dataset)
- Brazilian Operators Structured (B2B contracts)
- Brazilian Demand Factors (integrated external factors)
- Kaggle Equipment Failure (predictive maintenance)
- GitHub Network Fault (telecom faults)

Main Training Dataset:
- File: `data/processed/unified_dataset_with_factors.csv`
- Size: 27.25 MB, 118,082 rows, 31 features
- Date Range: 2013-11-01 to 2025-01-31

## ML/AI Components

- **ARIMA**: Statistical forecasting model
- **Prophet**: Facebook's forecasting model
- **LSTM**: Deep learning for sequential prediction
- **Ensemble**: Weighted combination of models
- **K-means clustering**: For equipment failure and tower performance analysis
- **LSTMForecaster**: Custom deep learning model for time series

## Business Value

- **Predictive Maintenance**: Identify high-risk equipment
- **Tower Optimization**: 4-tier performance classification
- **Cost Reduction**: Prescriptive recommendations with impact estimates
- **Regional Analysis**: 27-state Brazil coverage
- **Mathematical Accuracy**: LaTeX formula explanations

## Performance Metrics

- API Response Times: Health Check <10ms, Clustering <500ms, Prescriptive <100ms
- Code Quality: Zero TypeScript errors, zero linting issues, 100% type safety
- Clustering Accuracy: Equipment Failure (3 risk clusters), Tower Performance (4 tiers)

## Documentation

- `docs/BENCHMARK_REGISTRY.md` - Changelog & improvements
- `README.md` - Complete feature overview
- Individual dataset documentation files in `data/` directory
- Technical documentation for all 33 datasets

## Deployment

The system is designed for production deployment using Docker Compose, with services for:
- Backend API (FastAPI)
- Frontend (Next.js)
- Scheduled Forecast Service

## Technical Stack

### Backend (Primary)
- FastAPI
- Uvicorn ASGI server
- Pandas, NumPy, scikit-learn
- TensorFlow (for LSTM models)

### Backend (Secondary/Flask)
- Flask API
- Pandas, NumPy
- scikit-learn

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Recharts (visualizations)
- react-katex (LaTeX)
- D3.js (maps)

### ML/AI
- ARIMA (statsmodels)
- Prophet (Facebook forecasting)
- LSTM (TensorFlow/Keras)
- Ensemble models
- K-means clustering

## Status
**Production Ready** - This system was built for Grand Prix 2025 demoday with comprehensive functionality and documentation.

## Git Workflow

The project follows a structured Git workflow to ensure code quality and proper collaboration:

- **Branching Strategy**: Git Flow adapted for the project
  - `main`: Production-ready code
  - `develop`: Integration branch for features
  - `feature/*`: New feature development
  - `bugfix/*`: Bug fixes
  - `release/*`: Release preparation

- **Commit Conventions**: Follows Conventional Commits specification
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  - Format: `<type>(<scope>): <description>`

- **Setup**: Run `scripts/setup-git-workflow.bat` to initialize the workflow
- **Documentation**: Detailed workflow in `docs/GIT_WORKFLOW.md`
- **Tools**: Pre-commit hooks configured in `.pre-commit-config.yaml`