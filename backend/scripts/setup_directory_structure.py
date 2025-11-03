"""Script to create the complete new directory structure."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

DIRECTORIES = [
    # Frontend structure
    "frontend/src/app/dashboard/forecasts",
    "frontend/src/app/dashboard/inventory",
    "frontend/src/app/dashboard/analytics",
    "frontend/src/app/api/health",
    "frontend/src/components/ui",
    "frontend/src/components/charts",
    "frontend/src/components/dashboard",
    "frontend/src/components/layout",
    "frontend/src/lib",
    "frontend/src/hooks",
    "frontend/src/store",
    "frontend/src/styles",
    "frontend/public/images",
    "frontend/public/icons",
    
    # Backend structure
    "backend/app/api/v1/routes",
    "backend/app/api/v1/schemas",
    "backend/app/core/forecasting",
    "backend/app/core/inventory",
    "backend/app/core/analytics",
    "backend/app/models",
    "backend/app/utils",
    
    # ML structure
    "backend/ml/data",
    "backend/ml/models/arima",
    "backend/ml/models/prophet",
    "backend/ml/models/lstm",
    "backend/ml/models/xgboost",
    "backend/ml/models/ensemble",
    "backend/ml/training",
    "backend/ml/inference",
    "backend/ml/evaluation",
    "backend/ml/persistence",
    
    # Pipelines
    "backend/pipelines/data_ingestion/scrapy_spiders",
    "backend/pipelines/data_processing",
    "backend/pipelines/feature_engineering",
    "backend/pipelines/monitoring",
    
    # Scripts and tests
    "backend/scripts/maintenance",
    "backend/tests/unit",
    "backend/tests/integration",
    "backend/tests/e2e",
    "backend/tests/fixtures",
    
    # Shared
    "shared/types",
    "shared/schemas",
    
    # Infrastructure
    "infrastructure/docker",
    "infrastructure/kubernetes",
    "infrastructure/terraform",
    "infrastructure/scripts",
    
    # Data
    "data/raw/kaggle",
    "data/raw/zenodo",
    "data/raw/scraped",
    "data/processed/datasets",
    "data/processed/features",
    "data/processed/unified",
    "data/training/splits",
    "data/validation",
    "data/registry",
    
    # Models
    "models/arima/v1",
    "models/arima/v2",
    "models/prophet",
    "models/lstm",
    "models/ensemble",
    "models/metadata",
    
    # Reports
    "reports/forecasts",
    "reports/training",
    "reports/evaluation",
    "reports/analytics",
    
    # Docs
    "docs/architecture",
    "docs/api",
    "docs/ml",
    "docs/guides",
    "docs/changelog",
    
    # Config
    "config",
    
    # Logs (will be created at runtime, but include structure)
    "logs",
]

def create_directories():
    """Create all directory structure."""
    created = []
    existing = []
    
    for directory in DIRECTORIES:
        full_path = BASE_DIR / directory
        try:
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(str(full_path))
            print(f"[OK] Created: {directory}")
        except Exception as e:
            existing.append(str(full_path))
            print(f"[EXISTS] {directory} - {e}")
    
    print(f"\n{'='*60}")
    print(f"Created {len(created)} directories")
    if existing:
        print(f"Already existed: {len(existing)} directories")
    print(f"{'='*60}")
    
    return created, existing

if __name__ == "__main__":
    print("Creating directory structure...")
    print(f"Base directory: {BASE_DIR}\n")
    create_directories()
    print("\n[SUCCESS] Directory structure creation complete!")

