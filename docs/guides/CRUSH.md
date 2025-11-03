# Nova Corrente - Demand Forecasting System

## Build/Test Commands

### Backend (Python)
```bash
# Install dependencies
pip install -r backend/requirements.txt
pip install -r backend/requirements_api.txt
pip install -r backend/requirements_forecasting.txt

# Type checking and linting
mypy backend/
ruff check backend/
ruff format backend/

# Testing
pytest backend/tests/                    # Run all tests
pytest backend/tests/test_basic.py       # Run single test file
pytest backend/tests/ -v                  # Verbose output
pytest backend/tests/ --cov=app           # With coverage

# API server
python scripts/api_server.py              # Flask API server
cd backend && uvicorn app.main:app --reload  # FastAPI server

# ML training
python scripts/train_models.py
python scripts/generate_forecast.py
```

### Frontend (TypeScript/Next.js)
```bash
cd frontend
npm install
npm run dev                               # Development server
npm run build                             # Production build
npm run start                             # Production server
npm run lint                              # ESLint
npm run type-check                        # TypeScript checking
```

## Code Style Guidelines

### Python
- **Style**: Black formatting (100 char line length)
- **Imports**: Grouped (stdlib, third-party, local)
- **Types**: Type hints required for all functions
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Try/except with specific exceptions, meaningful error messages
- **Docstrings**: Triple quotes for all modules, classes, and functions
- **Dependencies**: Use pyproject.toml for package management

### TypeScript/React
- **Style**: ESLint + Next.js config
- **Imports**: Named exports preferred, React imports at top
- **Types**: Strict TypeScript, no `any` types
- **Naming**: PascalCase for components, camelCase for variables/functions
- **Components**: Functional components with hooks
- **File Structure**: Co-located components, styles, and tests

### ML/AI
- **Models**: Inherit from base model classes in `backend/ml/models/base.py`
- **Data**: Use DataLoader from `demand_forecasting.data_loader`
- **Validation**: Metrics in `backend/ml/evaluation/`
- **Persistence**: Model storage via `backend/ml/persistence/`

## Key Dependencies
- **Backend**: FastAPI, Flask, Pandas, NumPy, scikit-learn, TensorFlow, Prophet
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Recharts, React-KaTeX
- **ML**: ARIMA, Prophet, LSTM, ensemble methods
- **Testing**: pytest (Python), Jest/TypeScript (frontend)

## Project Structure
- `/backend/` - Python API and ML models
- `/frontend/` - Next.js dashboard
- `/demand_forecasting/` - Core ML modules
- `/scripts/` - Utility and server scripts
- `/data/` - Datasets and training splits