"""
Main FastAPI application entry point
Integrates all inner data services and outer API clients
"""
import sys
from pathlib import Path

# Fix import paths - add project root and backend directory to path
backend_dir = Path(__file__).parent.parent
project_root = backend_dir.parent

# Add project root first (so 'backend' module is found)
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
# Add backend directory
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from app.config import settings
from app.core.startup import lifespan
from app.api.v1.routes import (
    health, forecasts, inventory, metrics, items,
    temporal_features, climate_features, economic_features, fiveg_features,
    lead_time_features, sla_features, hierarchical_features,
    categorical_features, business_features,
    # Expanded feature routes
    transport_features, trade_features, energy_features, employment_features,
    construction_features, industrial_features, expanded_economic_features,
    logistics_features, regional_features,
    # Integration routes
    integration,
)

# Load environment variables - silently ignore parsing errors
try:
    load_dotenv(encoding='utf-8')
except Exception:
    # Ignore .env parsing errors - settings will use defaults
    pass

app = FastAPI(
    title="Nova Corrente Demand Forecasting API",
    description="Production-ready API for ML/DL demand forecasting with full integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(forecasts.router)
app.include_router(inventory.router)
app.include_router(metrics.router)
app.include_router(items.router)

# Include feature category routers
app.include_router(temporal_features.router)
app.include_router(climate_features.router)
app.include_router(economic_features.router)
app.include_router(fiveg_features.router)
app.include_router(lead_time_features.router)
app.include_router(sla_features.router)
app.include_router(hierarchical_features.router)
app.include_router(categorical_features.router)
app.include_router(business_features.router)

# Include expanded feature category routers
app.include_router(transport_features.router)
app.include_router(trade_features.router)
app.include_router(energy_features.router)
app.include_router(employment_features.router)
app.include_router(construction_features.router)
app.include_router(industrial_features.router)
app.include_router(expanded_economic_features.router)
app.include_router(logistics_features.router)
app.include_router(regional_features.router)

# Include integration management router
app.include_router(integration.router)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn
    import sys
    from pathlib import Path
    
    # Add backend directory to path if needed
    backend_dir = Path(__file__).parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    
    print("🚀 Starting Nova Corrente API Server...")
    print(f"📡 Host: {settings.API_HOST}")
    print(f"🔌 Port: {settings.API_PORT}")
    print(f"📚 Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level="info",
    )

