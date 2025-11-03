"""
Comprehensive migration script to move code to new structure.
This script migrates existing code to the new production-ready structure.
"""
import shutil
from pathlib import Path
import os
import json
from typing import List, Tuple

BASE_DIR = Path(__file__).parent

# Migration mappings
MIGRATIONS = [
    # ML Models
    ("demand_forecasting/models/arima_model.py", "backend/ml/models/arima/model.py"),
    ("demand_forecasting/models/prophet_model.py", "backend/ml/models/prophet/model.py"),
    ("demand_forecasting/models/lstm_model.py", "backend/ml/models/lstm/model.py"),
    ("demand_forecasting/models/ensemble.py", "backend/ml/models/ensemble/ensemble.py"),
    ("demand_forecasting/models/ensemble_model.py", "backend/ml/models/ensemble/ensemble_model.py"),
    
    # Data loading
    ("demand_forecasting/data/loader.py", "backend/ml/data/loader.py"),
    ("demand_forecasting/data_loader.py", "backend/ml/data/data_loader.py"),
    
    # Validation & Metrics
    ("demand_forecasting/validation/metrics.py", "backend/ml/evaluation/metrics.py"),
    
    # Utils
    ("demand_forecasting/utils/config.py", "backend/ml/config.py"),
    ("demand_forecasting/utils/model_persistence.py", "backend/ml/persistence/storage.py"),
    ("demand_forecasting/utils/backtesting.py", "backend/ml/training/backtesting.py"),
    
    # Inventory
    ("demand_forecasting/inventory/reorder_point.py", "backend/app/core/inventory/calculator.py"),
    ("demand_forecasting/inventory/alerts.py", "backend/app/core/inventory/alerts.py"),
    
    # Reporting
    ("demand_forecasting/reporting/report_generator.py", "backend/ml/evaluation/reports.py"),
    ("demand_forecasting/reporting/visualization.py", "backend/ml/evaluation/visualization.py"),
    
    # Pipelines
    ("src/pipeline/preprocess_datasets.py", "backend/pipelines/data_processing/preprocessor.py"),
    ("src/pipeline/merge_datasets.py", "backend/pipelines/data_processing/merger.py"),
    ("src/pipeline/add_external_factors.py", "backend/pipelines/data_processing/enrichment.py"),
    ("src/pipeline/brazilian_apis.py", "backend/pipelines/data_processing/brazilian_apis.py"),
    ("src/pipeline/download_datasets.py", "backend/pipelines/data_ingestion/kaggle_loader.py"),
    ("src/pipeline/download_brazilian_datasets.py", "backend/pipelines/data_ingestion/brazilian_loader.py"),
    
    # Scrapy
    ("src/scrapy/scrapy_spiders/anatel_spider.py", "backend/pipelines/data_ingestion/scrapy_spiders/anatel_spider.py"),
    ("src/scrapy/scrapy_spiders/github_spider.py", "backend/pipelines/data_ingestion/scrapy_spiders/github_spider.py"),
    ("src/scrapy/scrapy_spiders/internet_aberta_spider.py", "backend/pipelines/data_ingestion/scrapy_spiders/internet_aberta_spider.py"),
    ("src/scrapy/scrapy_spiders/mit_spider.py", "backend/pipelines/data_ingestion/scrapy_spiders/mit_spider.py"),
    ("src/scrapy/scrapy_spiders/springer_spider.py", "backend/pipelines/data_ingestion/scrapy_spiders/springer_spider.py"),
    ("src/scrapy/scrapy_spiders/settings.py", "backend/pipelines/data_ingestion/scrapy_spiders/settings.py"),
    ("src/scrapy/scrapy_spiders/items.py", "backend/pipelines/data_ingestion/scrapy_spiders/items.py"),
    ("src/scrapy/scrapy_spiders/pipelines.py", "backend/pipelines/data_ingestion/scrapy_spiders/pipelines.py"),
    
    # Scripts
    ("scripts/api_server.py", "backend/scripts/api_server.py"),
    ("scripts/web_dashboard_server.py", "backend/scripts/web_dashboard_server.py"),
    ("scripts/train_models.py", "backend/scripts/train_models.py"),
    ("scripts/generate_forecast.py", "backend/scripts/generate_forecast.py"),
    ("scripts/scheduled_forecast.py", "backend/scripts/scheduled_forecast.py"),
    ("scripts/backtest_models.py", "backend/scripts/backtest_models.py"),
    ("scripts/monitor_system.py", "backend/scripts/monitor_system.py"),
    
    # Config
    ("config.yaml", "backend/ml/config.yaml"),
    ("config/datasets_config.json", "backend/pipelines/data_ingestion/datasets_config.json"),
]

def create_init_files():
    """Create __init__.py files for all new directories."""
    directories = [
        "backend/ml/models/arima",
        "backend/ml/models/prophet",
        "backend/ml/models/lstm",
        "backend/ml/models/ensemble",
        "backend/ml/data",
        "backend/ml/evaluation",
        "backend/ml/training",
        "backend/ml/inference",
        "backend/ml/persistence",
        "backend/app/core/forecasting",
        "backend/app/core/inventory",
        "backend/app/core/analytics",
        "backend/pipelines/data_ingestion/scrapy_spiders",
        "backend/pipelines/data_processing",
        "backend/pipelines/feature_engineering",
        "backend/pipelines/monitoring",
    ]
    
    for directory in directories:
        init_file = BASE_DIR / directory / "__init__.py"
        init_file.parent.mkdir(parents=True, exist_ok=True)
        if not init_file.exists():
            init_file.write_text('"""Module docstring."""\n', encoding="utf-8")
            print(f"[OK] Created: {init_file}")

def migrate_file(source: Path, dest: Path, dry_run: bool = False) -> bool:
    """Migrate a single file."""
    if not source.exists():
        print(f"[SKIP] Source not found: {source}")
        return False
    
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    if dry_run:
        print(f"[DRY RUN] Would migrate: {source} -> {dest}")
        return True
    
    try:
        # Copy file
        shutil.copy2(source, dest)
        
        # Update imports if needed (basic)
        content = dest.read_text(encoding="utf-8")
        # Add basic import updates here if needed
        
        print(f"[OK] Migrated: {source.name} -> {dest}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to migrate {source}: {e}")
        return False

def migrate_all(dry_run: bool = False):
    """Migrate all files to new structure."""
    migrated = []
    skipped = []
    errors = []
    
    print(f"\n{'='*60}")
    print("Starting Migration to New Structure")
    print(f"{'='*60}\n")
    
    # Create __init__.py files
    create_init_files()
    
    # Migrate files
    for source_rel, dest_rel in MIGRATIONS:
        source = BASE_DIR / source_rel
        dest = BASE_DIR / dest_rel
        
        if migrate_file(source, dest, dry_run):
            migrated.append((source_rel, dest_rel))
        else:
            skipped.append(source_rel)
    
    print(f"\n{'='*60}")
    print(f"Migration Summary:")
    print(f"  Migrated: {len(migrated)} files")
    print(f"  Skipped: {len(skipped)} files")
    if errors:
        print(f"  Errors: {len(errors)} files")
    print(f"{'='*60}\n")
    
    return migrated, skipped, errors

def backup_existing():
    """Create backup of existing structure."""
    backup_dir = BASE_DIR / "backup_migration"
    backup_dir.mkdir(exist_ok=True)
    
    print(f"Creating backup in: {backup_dir}")
    
    # Backup key directories
    to_backup = [
        "demand_forecasting",
        "src/pipeline",
        "src/scrapy",
        "scripts",
        "config",
    ]
    
    for item in to_backup:
        source = BASE_DIR / item
        if source.exists():
            dest = backup_dir / item
            dest.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(source, dest)
            print(f"[OK] Backed up: {item}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate code to new structure")
    parser.add_argument("--dry-run", action="store_true", help="Preview without migrating")
    parser.add_argument("--backup", action="store_true", help="Create backup before migrating")
    
    args = parser.parse_args()
    
    if args.backup:
        backup_existing()
    
    migrate_all(dry_run=args.dry_run)
    
    if not args.dry_run:
        print("\n[SUCCESS] Migration complete!")
        print("\nNext steps:")
        print("1. Update imports in migrated files")
        print("2. Test migrated code")
        print("3. Organize reports: python backend/scripts/organize_reports.py")
    else:
        print("\n[DRY RUN] Preview complete. Run without --dry-run to migrate.")

