<!-- 00b8baf3-93c4-4633-a724-0d7dc3e27a9e c213513b-376b-4bde-9d40-a67d378496cb -->
# Nova Corrente Data Services, Algorithms, and Data Structures Implementation

## Overview

Design and implement a complete data services layer connecting the ML-ready database with feature engineering, ML models (Prophet, ARIMA, LSTM, Ensemble), ETL pipelines for Brazilian external data, and fullstack algorithms for forecasting, reorder point calculation, and anomaly detection.

## Architecture Components

### 1. Data Services Layer

**Location:** `backend/services/`

**Services to implement:**

- `database_service.py` - Connection pool, query builder, transaction management
- `material_service.py` - Material CRUD, feature retrieval, historical data access
- `feature_service.py` - Feature extraction, aggregation, caching
- `prediction_service.py` - ML prediction orchestration, model selection
- `external_data_service.py` - External API integrations (INMET, BACEN, ANATEL)
- `analytics_service.py` - KPI calculations, insights generation

**Data structures:**

- Connection pool singleton pattern
- Query result DTOs (Data Transfer Objects)
- Feature vector data structures
- Time-series data structures

### 2. Feature Engineering Services

**Location:** `backend/services/feature_engineering/`

**Algorithms to implement:**

- `temporal_features.py` - Cyclical encoding, Brazilian calendar features
- `statistical_features.py` - Lag features, moving averages, volatility
- `external_features.py` - Climate, economic, 5G feature extraction
- `hierarchical_features.py` - Family, site, supplier aggregations
- `feature_pipeline.py` - End-to-end feature engineering pipeline

**Data structures:**

- Feature matrix (numpy/pandas optimized)
- Feature metadata registry
- Temporal feature cache

### 3. ML Model Services

**Location:** `backend/services/ml_models/`

**Models to implement:**

- `prophet_model.py` - Prophet with Brazilian holiday regressors
- `arima_model.py` - ARIMA/ARIMAX with external regressors
- `lstm_model.py` - LSTM multivariate time-series
- `ensemble_model.py` - Weighted ensemble of all models
- `model_registry.py` - Model versioning, persistence, loading

**Algorithms:**

- Time-series cross-validation
- Hyperparameter tuning (optional)
- Model evaluation metrics (MAPE, RMSE, MAE)
- Prediction confidence intervals

**Data structures:**

- Model metadata
- Prediction results with confidence intervals
- Model performance tracking

### 4. ETL Pipelines

**Location:** `backend/pipelines/`

**Pipelines to implement:**

- `climate_etl.py` - INMET API integration, Salvador/BA climate data
- `economic_etl.py` - BACEN API integration, inflation, exchange rate
- `anatel_5g_etl.py` - ANATEL data scraping/API, 5G expansion tracking
- `brazilian_calendar_etl.py` - Brazilian holidays calendar generation
- `feature_calculation_etl.py` - Daily feature calculation job

**Algorithms:**

- API rate limiting
- Data validation and cleaning
- Incremental updates
- Error handling and retry logic

### 5. Core Algorithms

**Location:** `backend/algorithms/`

**Algorithms to implement:**

- `reorder_point_calculator.py` - PP = (D × LT) + SS calculation
- `safety_stock_calculator.py` - SS = Z × σ × √LT calculation
- `demand_forecaster.py` - Multi-horizon demand forecasting
- `anomaly_detector.py` - Isolation Forest / statistical anomaly detection
- `abc_classifier.py` - ABC classification algorithm
- `sla_calculator.py` - SLA penalty calculations

**Data structures:**

- Forecasting result DTOs
- Anomaly detection results
- Classification metadata

### 6. API Integration Layer

**Location:** `backend/api/`

**Enhance existing `api_standalone.py`:**

- Connect to MySQL database instead of CSV
- Integrate with feature engineering services
- Add ML prediction endpoints
- Add real-time feature calculation endpoints
- Add external data refresh endpoints

**New endpoints:**

- `POST /api/features/calculate` - Calculate features for material
- `POST /api/models/train` - Train ML model
- `GET /api/models/{model_id}/predict` - Get predictions
- `POST /api/external-data/refresh` - Refresh external data
- `GET /api/materials/{id}/forecast` - Material-specific forecast

### 7. Data Structures Library

**Location:** `backend/data_structures/`

**Data structures to implement:**

- `time_series.py` - Time-series wrapper with indexing
- `feature_vector.py` - Feature vector with metadata
- `prediction_result.py` - Prediction with confidence intervals
- `material_context.py` - Material context with all features
- `external_data_cache.py` - External data caching structure

### 8. Configuration and Utilities

**Location:** `backend/config/` and `backend/utils/`

**Files to create:**

- `database_config.py` - Database connection configuration
- `ml_config.py` - ML model hyperparameters
- `external_apis_config.py` - External API credentials and endpoints
- `feature_config.py` - Feature engineering configuration
- `logging_config.py` - Centralized logging
- `cache_manager.py` - Redis/file caching utilities

## Implementation Order

1. **Database Service Layer** - Foundation for all services
2. **Feature Engineering Services** - Core feature extraction
3. **ETL Pipelines** - External data integration
4. **Core Algorithms** - Forecasting and calculations
5. **ML Model Services** - Model implementation and training
6. **API Integration** - Connect everything via API
7. **Data Structures** - Optimize data handling

## Technical Specifications

**Database:**

- MySQL connection pooling (SQLAlchemy or async MySQL)
- Transaction management
- Query optimization with indexes

**ML Models:**

- Prophet: Facebook Prophet with Brazilian holidays
- ARIMA: statsmodels ARIMA/ARIMAX
- LSTM: TensorFlow/Keras LSTM
- Ensemble: Weighted average with performance-based weights

**Caching:**

- Feature calculation results (Redis or file cache)
- External data (daily refresh)
- Model predictions (short-term cache)

**Error Handling:**

- Comprehensive try-catch blocks
- Retry logic for external APIs
- Graceful degradation
- Logging and monitoring

## Files to Create/Modify

**New Files:**

- `backend/services/` (8+ service files)
- `backend/services/feature_engineering/` (5 feature engineering files)
- `backend/services/ml_models/` (5 ML model files)
- `backend/pipelines/` (5 ETL pipeline files)
- `backend/algorithms/` (6 algorithm files)
- `backend/data_structures/` (5 data structure files)
- `backend/config/` (5 config files)
- `backend/utils/` (utility files)

**Modify:**

- `backend/scripts/api_standalone.py` - Integrate with new services
- `backend/data/Nova_Corrente_ML_Ready_DB.sql` - Review/validate stored procedures

## Dependencies

**Python packages needed:**

- SQLAlchemy or async MySQL driver
- Prophet (fbprophet)
- statsmodels (ARIMA)
- TensorFlow/Keras (LSTM)
- pandas/numpy (data processing)
- scikit-learn (anomaly detection, preprocessing)
- requests (external APIs)
- redis (caching, optional)
- python-dateutil (Brazilian calendar)

**Estimated total files:** 40-50 new Python files + configuration filesReviewing the strategic documents for context, then implementing the ML-ready database scaffolding with all custom tuning needs.

[4 tools called]

Reviewing the strategy documents to capture all custom tuning requirements, then creating a complete ML-ready database scaffold.

[3 tools called]

Creating a complete ML-ready database scaffold that incorporates all custom tuning needs for Nova Corrente. Building the enhanced schema:

[2 tools called]

Creating the ML-ready database with all custom tunings:

[1 tool called]

Creating documentation for all custom tunings and updating the benchmark registry:

[2 tools called]

Updating the benchmark registry with the new ML database implementation:

[1 tool called]

Appending the ML database implementation to the benchmark registry:

[2 tools called]

Checking for linting errors:

[1 tool called]

Completed the ML-ready database scaffolding with all custom tuning needs. Summary:

## ML-ready database scaffolding

### Files created

1. `backend/data/Nova_Corrente_ML_Ready_DB.sql` (1,200+ lines)

    - ML-ready database schema

    - All custom tunings integrated

    - Stored procedures for feature engineering

    - ML-optimized views

2. `backend/data/ML_DATABASE_CUSTOM_TUNINGS_DOC.md` (800+ lines)

    - Documentation of all custom tunings

    - Usage examples

    - Feature category breakdown

3. Updated `docs/BENCHMARK_REGISTRY.md`

    - Implementation details logged

### Custom tunings implemented

#### Brazilian-specific

- CalendarioBrasil: Brazilian holidays, carnival, summer, rainy season

- ClimaSalvador: INMET climate data for Salvador/BA with calculated features

- IndicadoresEconomicos: BACEN economic indicators (inflation, exchange, GDP, SELIC)

- Expansao5G: ANATEL 5G expansion tracking

#### Nova Corrente B2B-specific

- Tier levels: TIER_1/2/3 criticality with SLA targets

- Top 5 families: Pre-configured (MATERIAL ELETRICO, FERRO E AÇO, EPI, MATERIAL CIVIL, FERRAMENTAS)

- Lead time tracking: Supplier and material-specific with categories

- Site/tower tracking: Support for 18,000+ towers

- SLA features: Penalty calculations and availability targets

#### ML infrastructure

- 73 features organized in `MaterialFeatures` table

- Model registry and prediction tracking

- Temporal aggregations (daily, weekly, monthly)

- Analytics and insights tables

- Anomaly detection system

### Features supported

| Category | Count | Features |

|----------|-------|----------|

| **TEMPORAL** | 15 | Year, month, day, cyclical, Brazilian holidays |

| **CLIMATE** | 12 | Temperature, precipitation, humidity, calculated risks |

| **ECONOMIC** | 6 | Inflation, exchange, GDP, SELIC |

| **5G** | 5 | Coverage, investment, milestones, expansion |

| **LEAD_TIME** | 8 | Supplier/material lead times, categories, risks |

| **SLA** | 4 | Penalties, availability, downtime, violations |

| **HIERARCHICAL** | 10 | Family, site, supplier aggregations |

| **CATEGORICAL** | 5 | Encoded categories |

| **BUSINESS** | 8 | Nova Corrente-specific business features |

Total: 73 features

### Stored procedures

1. `sp_calcular_historico_diario` — Daily aggregations with Brazilian calendar

2. `sp_extrair_features_material_completo` — Extract all 73 ML features

3. `sp_extrair_features_externas_brasil` — Extract Brazilian external features

### ML-optimized views

1. `vw_material_ml_features` — Material view with ML features

2. `vw_material_time_series_brasil` — Time-series with Brazilian context

3. `vw_top5_familias_nova_corrente` — Top 5 families statistics

4. `vw_predictions_summary` — ML predictions with tracking

### Next steps

1. Populate reference tables (CalendarioBrasil, ClimaSalvador, IndicadoresEconomicos, Expansao5G)

2. Run stored procedures to calculate initial features

3. Set up ETL pipelines for feature engineering

4. Train ML models and register in MLModelRegistry

5. Generate predictions using the ML infrastructure

The database is ready for ML processing with all custom tunings integrated.

### To-dos

- [ ] Implement database service layer with connection pooling, query builder, and transaction management (SQLAlchemy or async MySQL)
- [ ] Implement feature engineering services for temporal, statistical, external, and hierarchical features
- [ ] Implement ETL pipelines for INMET climate, BACEN economic, ANATEL 5G, and Brazilian calendar data
- [ ] Implement core algorithms: reorder point calculator, safety stock calculator, demand forecaster, anomaly detector
- [ ] Implement ML model services: Prophet, ARIMA, LSTM, and ensemble with model registry
- [ ] Implement data structures library: time series, feature vectors, prediction results, material context
- [ ] Enhance API standalone to integrate with database and new services, add ML endpoints
- [ ] Create configuration files and utilities for database, ML, external APIs, caching, and logging