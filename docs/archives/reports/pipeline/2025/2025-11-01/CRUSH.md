# Nova Corrente Demand Forecasting System - Development Guide

## Essential Commands

```bash
# Run complete pipeline
python run_pipeline.py [--datasets LIST] [--config PATH] [--skip-download] [--skip-preprocess] [--skip-merge] [--skip-factors]

# Start interactive dashboard
python run_dashboard.py [--port PORT] [--host HOST] [--no-debug]

# Utility testing scripts
python scripts/test_new_datasets.py
python scripts/test_pdf_parsing.py
python scripts/analyze_all_datasets.py
python scripts/check_zenodo_quantity.py
```

## Code Style Guidelines

### Imports & Structure
- Standard library → third-party → local imports (clear separation)
- Use `src.utils.paths` for all path operations (`PROJECT_ROOT`, `DATA_DIR`, etc.)
- Relative imports within `src/` package (e.g., `from .download_datasets import`)

### Naming Conventions
- Functions/variables: `snake_case`
- Classes: `PascalCase`  
- Constants: `UPPER_SNAKE_CASE`
- Config keys: `snake_case` (JSON)

### Error Handling
- Always wrap file operations in try-catch with informative messages
- Use logging module with file + stream handlers
- Validate paths using `Path.exists()` before operations

### Data Processing
- Use pandas for all data manipulation
- Validate data via `src.validation.validate_data`
- Store intermediate results in `data/processed/`
- Log progress with tqdm for long operations

### Testing & Validation
- No formal test framework - use `/scripts/` for manual testing
- Validate pipeline outputs via `src.utils.check_final_output`
- Check data quality with `src.validation.data_quality_report`

## Project Architecture
- `/src/pipeline/` - Core ETL orchestration
- `/src/utils/` - Shared utilities and helpers  
- `/src/validation/` - Data validation and quality checks
- `/src/visualization/` - Dash-based interactive dashboard
- `/config/` - JSON configuration files
- All paths resolved via `src.utils.paths.get_project_root()`

## ByteRover MCP Integration
- MUST use `byterover-store-knowledge` when learning new patterns/APIs
- MUST use `byterover-retrieve-knowledge` before starting new tasks