# Nova Corrente - Development Guide

## Frontend (Next.js + TypeScript)
```bash
npm run dev               # Start dev server (localhost:3000)
npm run build             # Production build
npm start                 # Start production server
npm test                  # Run all tests
npm test path/to/test.ts  # Run single test file
npm run lint              # ESLint check (Next.js config)
npx tsc --noEmit          # TypeScript type checking
node scripts/validate.js  # Complete pre-push validation
```

## Backend (FastAPI + Python)
```bash
python run_server.py      # Start FastAPI server (localhost:5000)
uvicorn app.main:app --reload  # Alternative dev server
pytest                    # Run all tests
pytest tests/test.py      # Run single test file
black .                   # Format code (100 char line length)
ruff check .              # Lint code (Python 3.11 target)
mypy .                    # Type checking
pre-commit run --all-files  # Run all pre-commit hooks
```

## ML Environment (Separate from Deployment)
```bash
pip install -r requirements_ml.txt  # ML dependencies (NOT for deployment)
python scripts/train_models.py       # Train ML models locally
python scripts/generate_forecast.py  # Generate forecasts
```

## Code Style & Conventions
**Frontend**: PascalCase components, camelCase vars, `@/` imports, functional React hooks, TypeScript interfaces in `types.ts`, Tailwind CSS classes
**Backend**: snake_case functions, PascalCase classes, type hints, Pydantic models, FastAPI HTTPException, SQLAlchemy models
**Testing**: Jest (frontend), pytest (backend), pre-push validation required
**Imports**: Frontend - absolute imports with `@/`, Backend - isort for import sorting
**Error Handling**: Frontend - proper error boundaries, Backend - HTTPException with proper status codes
**Documentation**: Docstrings for all Python functions, JSDoc for complex frontend logic
**ML Constraint**: ML dependencies separate from deployment (requirements_ml.txt vs requirements_deployment.txt)
**ByteRover MCP**: MUST use byterover-retrieve-knowledge before tasks, byterover-store-knowledge after learning patterns/debugging