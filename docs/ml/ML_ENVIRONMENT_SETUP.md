# 🤖 ML ENVIRONMENT SETUP
## Nova Corrente - Separate ML Processing Environment

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Setup Guide

---

## 📋 OVERVIEW

This document describes how to set up the **separate ML processing environment** that outputs results to shared storage for deployment consumption.

**Key Principle:** ML processing runs separately from deployment. Deployment only reads precomputed results.

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────┐
│   ML Processing Environment     │
│   (Local/Cloud/HPC)              │
│                                  │
│   - PyTorch                      │
│   - TensorFlow                   │
│   - scikit-learn                 │
│   - Prophet, ARIMA, LSTM         │
│   - MLflow (optional)            │
│                                  │
│   Outputs: Parquet files         │
│   Location: /exports/ml_results/ │
└──────────────┬───────────────────┘
               │
               │ (Write Parquet)
               ▼
┌─────────────────────────────────┐
│   Shared Storage                 │
│   (MinIO/S3/Local)               │
│                                  │
│   /exports/ml_results/           │
│   - fact_forecast.parquet        │
│   - fact_metrics.parquet         │
│   - metadata.json                │
└──────────────┬───────────────────┘
               │
               │ (Read-only)
               ▼
┌─────────────────────────────────┐
│   Deployment Environment         │
│   (Docker Compose)                │
│                                  │
│   - FastAPI (NO ML)              │
│   - DuckDB (read Parquet)        │
│   - Redis (cache)                │
│                                  │
│   Reads: Precomputed results     │
└─────────────────────────────────┘
```

---

## 🔧 SETUP INSTRUCTIONS

### Option 1: Local ML Environment

#### Step 1: Install ML Dependencies
```bash
# Create virtual environment
python -m venv venv_ml
source venv_ml/bin/activate  # Linux/Mac
# or
venv_ml\Scripts\activate  # Windows

# Install ML requirements
pip install -r backend/requirements_ml.txt
```

#### Step 2: Configure ML Environment
```bash
# Set ML results output path
export ML_RESULTS_PATH=./exports/ml_results
mkdir -p $ML_RESULTS_PATH

# Configure ML processing (if using MLflow)
export MLFLOW_TRACKING_URI=file:./mlruns
export MLFLOW_REGISTRY_URI=file:./mlruns
```

#### Step 3: Run ML Processing
```bash
# Train models and generate forecasts
python -m backend.scripts.train_models_nova_corrente

# Or use Docker (ML environment)
docker build -t nova-corrente-ml:latest \
  -f infrastructure/docker/Dockerfile.backend.ml .
docker run -v ./exports/ml_results:/app/exports/ml_results \
  nova-corrente-ml:latest
```

#### Step 4: Export Results
```bash
# ML processing outputs Parquet files to:
# ./exports/ml_results/
#   - fact_forecast.parquet (with model_version, generated_at, source, dataset_id)
#   - fact_metrics.parquet
#   - metadata.json

# Verify outputs
ls -la ./exports/ml_results/
```

### Option 2: Cloud ML Environment (Optional)

#### AWS SageMaker
```python
# Example: Run ML job in SageMaker
# Outputs to S3: s3://nova-corrente-ml-results/
```

#### Google Cloud AI Platform
```python
# Example: Run ML job in GCP
# Outputs to GCS: gs://nova-corrente-ml-results/
```

---

## 📊 ML OUTPUT REQUIREMENTS

### Required Metadata
All ML-generated Parquet files must include:

```python
# Required columns in fact_forecast.parquet
{
    'date': 'date',
    'item_id': 'string',
    'forecast': 'float',
    'actual': 'float',
    'source': 'string',  # 'prophet', 'arima', 'lstm', 'ensemble'
    'model_version': 'string',  # e.g., 'v1.2.3'
    'generated_at': 'timestamp',  # When ML results were generated
    'dataset_id': 'string',  # Dataset identifier for traceability
}
```

### Example Output Script
```python
# backend/scripts/export_ml_results.py
import pandas as pd
from datetime import datetime
import os

def export_ml_results(forecasts_df, model_version, dataset_id):
    """Export ML results to shared storage"""
    # Add required metadata
    forecasts_df['model_version'] = model_version
    forecasts_df['generated_at'] = datetime.now()
    forecasts_df['dataset_id'] = dataset_id
    forecasts_df['source'] = 'prophet'  # or 'arima', 'lstm', 'ensemble'
    
    # Export to shared storage
    ml_results_path = os.getenv('ML_RESULTS_PATH', './exports/ml_results')
    output_path = f"{ml_results_path}/fact_forecast.parquet"
    
    forecasts_df.to_parquet(output_path, index=False)
    
    print(f"✅ ML results exported to: {output_path}")
    print(f"   Model version: {model_version}")
    print(f"   Dataset ID: {dataset_id}")
```

---

## 🔄 DATA REFRESH WORKFLOW

### Workflow
1. **ML Processing:** Runs in separate environment, outputs Parquet to shared storage
2. **Data Refresh:** Deployment triggers reload via `/api/v1/data/refresh` endpoint
3. **Deployment:** Reads updated Parquet files, updates cache

### Manual Data Refresh
```bash
# Trigger data refresh (admin only)
curl -X POST http://localhost:5000/api/v1/data/refresh \
  -H "X-API-Key: your-admin-api-key" \
  -H "Content-Type: application/json" \
  -d '{"source": "ml_results", "force": false}'
```

---

## 📚 REFERENCE LINKS

- [Global Constraints](../diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)
- [Deployment Runbook](../deploy/DEPLOYMENT_RUNBOOK.md)
- [Data Cluster](../diagnostics/clusters/01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md)

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Setup Guide

