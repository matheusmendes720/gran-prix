# Nova Corrente Data Services Architecture

## Overview
Complete data services layer for Nova Corrente ML-ready database system with feature engineering, ML models, ETL pipelines, and API integration.

## Architecture

### Service Layer (`backend/services/`)
- **DatabaseService** - Connection pooling, transactions, query execution
- **MaterialService** - Material CRUD, historical data, context
- **FeatureService** - Feature extraction, aggregation, caching
- **AnalyticsService** - KPI calculations, insights
- **PredictionService** - ML prediction orchestration
- **ExternalDataService** - External API integrations

### Feature Engineering (`backend/services/feature_engineering/`)
- **TemporalFeatureExtractor** - Brazilian calendar, cyclical encoding
- **StatisticalFeatureExtractor** - Lag features, moving averages
- **ExternalFeatureExtractor** - Climate, economic, 5G features
- **HierarchicalFeatureExtractor** - Family, site, supplier aggregations
- **FeaturePipeline** - End-to-end orchestration

### ML Models (`backend/services/ml_models/`)
- **ProphetModel** - Facebook Prophet with Brazilian holidays
- **ARIMAModel** - ARIMA/ARIMAX with external regressors
- **LSTMModel** - TensorFlow/Keras LSTM multivariate
- **EnsembleModel** - Weighted ensemble
- **ModelRegistry** - Model versioning and persistence

### Algorithms (`backend/algorithms/`)
- **ReorderPointCalculator** - PP = (D × LT) + SS
- **SafetyStockCalculator** - SS = Z × σ × √LT
- **DemandForecaster** - Multi-horizon forecasting
- **AnomalyDetector** - Statistical and Isolation Forest
- **ABCClassifier** - ABC classification
- **SLACalculator** - SLA penalty calculations

### Data Structures (`backend/data_structures/`)
- **TimeSeries** - Time-series wrapper with operations
- **FeatureVector** - Feature vector with metadata
- **PredictionResult** - Prediction with confidence intervals
- **MaterialContext** - Complete material context

### ETL Pipelines (`backend/pipelines/`)
- **ClimateETL** - INMET climate data
- **EconomicETL** - BACEN economic data
- **ANATEL5GETL** - ANATEL 5G expansion
- **BrazilianCalendarETL** - Brazilian holidays
- **FeatureCalculationETL** - Daily feature calculation

### Configuration (`backend/config/`)
- **database_config.py** - Database configuration
- **ml_config.py** - ML model hyperparameters
- **external_apis_config.py** - External API configs
- **feature_config.py** - Feature engineering config
- **logging_config.py** - Logging configuration

### API (`backend/api/`)
- **enhanced_api.py** - Enhanced Flask API with new endpoints

## Quick Start

### 1. Database Connection
```python
from backend.services.database_service import db_service

# Test connection
if db_service.test_connection():
    print("Database connected!")
```

### 2. Feature Engineering
```python
from backend.services.feature_engineering.feature_pipeline import feature_pipeline

# Calculate features for material
feature_vector = feature_pipeline.calculate_and_store_features(
    material_id=1,
    store_in_db=True
)
```

### 3. ML Predictions
```python
from backend.services.prediction_service import prediction_service

# Generate prediction
prediction = prediction_service.generate_prediction(
    model_id=1,
    material_id=1,
    prediction_type='DEMANDA',
    horizon=30
)
```

### 4. Algorithms
```python
from backend.algorithms.reorder_point_calculator import reorder_point_calculator

# Calculate reorder point
pp = reorder_point_calculator.calculate(
    demand=10.0,
    lead_time_days=14.0,
    safety_stock=20.0
)
```

### 5. ETL Pipelines
```python
from backend.pipelines.climate_etl import climate_etl
from datetime import date, timedelta

# Refresh climate data
rows = climate_etl.run(
    start_date=date.today() - timedelta(days=30),
    end_date=date.today()
)
```

## API Endpoints

### New Endpoints
- `POST /api/features/calculate` - Calculate features
- `POST /api/models/train` - Train ML model
- `GET /api/models/{model_id}/predict` - Get predictions
- `POST /api/external-data/refresh` - Refresh external data
- `GET /api/materials/{id}/forecast` - Material forecast
- `GET /api/materials/{id}/reorder-point` - Calculate PP
- `GET /api/materials/{id}/safety-stock` - Calculate SS

## Dependencies

### Core
- SQLAlchemy - Database ORM
- pandas - Data processing
- numpy - Numerical operations

### ML
- prophet - Facebook Prophet
- statsmodels - ARIMA
- tensorflow - LSTM models
- scikit-learn - Anomaly detection

### External APIs
- requests - HTTP requests
- python-dateutil - Date utilities

### Optional
- redis - Caching (with file fallback)

## Environment Variables

```bash
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=STOCK

# External APIs
INMET_API_KEY=
BACEN_API_KEY=
ANATEL_API_KEY=
OPENWEATHER_API_KEY=

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs
```

## File Structure

```
backend/
├── config/          # Configuration files
├── utils/           # Utilities
├── services/        # Service layer
│   ├── feature_engineering/  # Feature extractors
│   └── ml_models/   # ML models
├── algorithms/      # Core algorithms
├── data_structures/ # Data structures
├── pipelines/      # ETL pipelines
└── api/            # API endpoints
```

## Testing

```python
# Test database connection
python -c "from backend.services.database_service import db_service; print(db_service.test_connection())"

# Test feature extraction
python -c "from backend.services.feature_engineering.feature_pipeline import feature_pipeline; print(feature_pipeline.extract_all_features(1))"
```

## Status

✅ All components implemented and tested
✅ Database integration complete
✅ Feature engineering complete
✅ ML models complete
✅ ETL pipelines complete
✅ API integration complete

---

**Nova Corrente Grand Prix SENAI**

