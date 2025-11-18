# Pipeline Architecture

## Overview
End-to-end data pipeline for Nova Corrente demand forecasting with external factors.

## Architecture Diagram
```
External APIs/Sources → Landing Layer → Silver Layer → Gold Layer → ML Models → Predictions
```

## Layer Details

### 1. Landing Layer (Raw Data)
- **Source**: External APIs, web scrapers, manual uploads
- **Format**: JSON, CSV, raw API responses
- **Frequency**: Daily updates
- **Validation**: Basic format checking
- **Storage**: `D:\codex\datamaster\senai\gran_prix\data\landing\external_factors-raw`

### 2. Silver Layer (Cleaned Data)
- **Process**: Data cleaning, normalization, type conversion
- **Format**: Parquet (columnar, compressed)
- **Frequency**: Automated transformation
- **Validation**: Data quality checks, null rate monitoring
- **Storage**: `D:\codex\datamaster\senai\gran_prix\data\silver\external_factors`

### 3. Gold Layer (ML Features)
- **Process**: Feature engineering, time-series creation, lag variables
- **Format**: Parquet with engineered features
- **Frequency**: Daily feature updates
- **Features**: Rate changes, rolling averages, correlations, lagged values
- **Storage**: `D:\codex\datamaster\senai\gran_prix\data\gold\ml_features`

## Data Flow
1. **Ingestion**: External APIs → Landing (JSON/CSV)
2. **Transformation**: Landing → Silver (Parquet, normalized)
3. **Feature Engineering**: Silver → Gold (ML-ready features)
4. **ML Integration**: Gold → Models (training/inference)

## Key Components
- **Data Downloaders**: Automated API clients
- **Transformers**: Schema normalization and validation
- **Feature Engineers**: Time-series and statistical features
- **Quality Monitors**: Continuous data quality checks
- **Automation**: Daily refresh cycles

## Scalability
- **Incremental Updates**: Only process new/changed data
- **Parallel Processing**: Multiple categories processed simultaneously
- **Storage Efficiency**: Parquet compression and columnar format
- **Version Control**: Timestamped snapshots for rollback

---

*Architecture Last Updated: 2025-11-11 13:46:25*
