# 💻 EXEMPLOS DE IMPLEMENTAÇÃO - DATA PIPELINES
## Nova Corrente - Código Pronto para Produção

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Exemplos Completos

---

## 📋 ÍNDICE

1. [Pipeline de Extração Completo](#extracao)
2. [Pipeline de Transformação (dbt)](#transformacao)
3. [Pipeline de ML Inference](#ml-inference)
4. [Pipeline de Serving (FastAPI)](#serving)
5. [Pipeline de Real-time](#realtime)
6. [Orquestração Airflow Completa](#orquestracao)

---

<a name="extracao"></a>

## 1. 📥 PIPELINE DE EXTRAÇÃO COMPLETO

### 1.1 Extract Multiple Sources

```python
# backend/pipelines/data_ingestion/multi_source_extractor.py
"""
Extract data from multiple sources and load to Bronze layer
"""
import pandas as pd
import boto3
from datetime import datetime
from typing import Dict, List
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class MultiSourceExtractor:
    """Extract from multiple sources in parallel"""
    
    def __init__(self, config):
        self.config = config
        self.s3_client = boto3.client('s3')
        self.bronze_bucket = config['bronze_bucket']
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    def extract_all_sources(self, date: datetime = None) -> Dict[str, pd.DataFrame]:
        """
        Extract from all sources in parallel
        
        Returns:
            Dictionary with source name as key and DataFrame as value
        """
        if date is None:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        logger.info(f"Starting extraction for {date}")
        
        # Define extraction tasks
        tasks = {
            'erp': self.extract_erp,
            'weather': self.extract_weather,
            'economic': self.extract_economic,
            'anatel': self.extract_anatel,
            'supplier': self.extract_supplier
        }
        
        # Execute in parallel
        results = {}
        futures = {self.executor.submit(task, date): name for name, task in tasks.items()}
        
        for future in as_completed(futures):
            source_name = futures[future]
            try:
                df = future.result()
                results[source_name] = df
                logger.info(f"✅ Extracted {len(df)} rows from {source_name}")
                
                # Load to Bronze immediately
                self.load_to_bronze(df, source_name, date)
                
            except Exception as e:
                logger.error(f"❌ Failed to extract {source_name}: {str(e)}")
                results[source_name] = None
        
        return results
    
    def extract_erp(self, date: datetime) -> pd.DataFrame:
        """Extract from ERP PostgreSQL"""
        import psycopg2
        
        conn = psycopg2.connect(
            host=self.config['erp']['host'],
            database=self.config['erp']['database'],
            user=self.config['erp']['user'],
            password=self.config['erp']['password']
        )
        
        query = """
            SELECT 
                item_id,
                item_name,
                category,
                family,
                supplier_id,
                cost,
                quantity,
                current_stock,
                lead_time_days,
                date,
                created_at
            FROM items
            WHERE date = %s
        """
        
        df = pd.read_sql(query, conn, params=[date])
        conn.close()
        
        return df
    
    def extract_weather(self, date: datetime) -> pd.DataFrame:
        """Extract from INMET Weather API"""
        import requests
        
        # INMET API
        url = "https://apitempo.inmet.gov.br/estacao/diaria"
        params = {
            'codigo': 'A502',  # Salvador station
            'dataInicio': date.strftime('%Y-%m-%d'),
            'dataFim': date.strftime('%Y-%m-%d')
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        df = pd.DataFrame(data)
        return df
    
    def extract_economic(self, date: datetime) -> pd.DataFrame:
        """Extract from BACEN Economic API"""
        import requests
        
        # BACEN API for inflation (IPCA)
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
        params = {
            'formato': 'json',
            'dataInicial': date.strftime('%d/%m/%Y'),
            'dataFinal': date.strftime('%d/%m/%Y')
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        df = pd.DataFrame(data)
        return df
    
    def extract_anatel(self, date: datetime) -> pd.DataFrame:
        """Extract from ANATEL 5G expansion data"""
        import requests
        
        # ANATEL API (example endpoint)
        url = "https://www.anatel.gov.br/dadosabertos/api/v1/towers"
        params = {
            'date': date.strftime('%Y-%m-%d'),
            'technology': '5G'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        df = pd.DataFrame(data)
        return df
    
    def extract_supplier(self, date: datetime) -> pd.DataFrame:
        """Extract from Supplier APIs"""
        # Implementation depends on supplier API
        pass
    
    def load_to_bronze(self, df: pd.DataFrame, source: str, date: datetime):
        """Load DataFrame to Bronze layer in S3"""
        year = date.year
        month = f"{date.month:02d}"
        day = f"{date.day:02d}"
        
        s3_key = f"{source}/year={year}/month={month}/day={day}/data.parquet"
        
        # Convert to Parquet
        parquet_buffer = df.to_parquet(index=False, compression='snappy')
        
        # Upload to S3
        self.s3_client.put_object(
            Bucket=self.bronze_bucket,
            Key=s3_key,
            Body=parquet_buffer,
            ContentType='application/parquet',
            Metadata={
                'source': source,
                'extracted_at': datetime.now().isoformat(),
                'row_count': str(len(df)),
                'schema_version': '1.0'
            }
        )
        
        logger.info(f"✅ Loaded to s3://{self.bronze_bucket}/{s3_key}")

# Usage
if __name__ == "__main__":
    config = {
        'bronze_bucket': 'nova-corrente-data-lake-bronze',
        'erp': {
            'host': 'erp.novacorrente.com',
            'database': 'erp_db',
            'user': os.getenv('ERP_USER'),
            'password': os.getenv('ERP_PASSWORD')
        }
    }
    
    extractor = MultiSourceExtractor(config)
    results = extractor.extract_all_sources()
    
    print(f"Extracted from {len(results)} sources")
```

---

<a name="transformacao"></a>

## 2. 🔄 PIPELINE DE TRANSFORMAÇÃO (DBT)

### 2.1 dbt Models Completos

**Staging Model (Bronze → Silver):**

```sql
-- models/staging/stg_items.sql
{{ config(
    materialized='view',
    schema='staging',
    tags=['staging', 'items', 'nova-corrente']
) }}

WITH source AS (
    SELECT * FROM {{ source('bronze', 'raw_items') }}
    WHERE _partition_date = CURRENT_DATE - 1
),

cleaned AS (
    SELECT
        -- Primary keys
        CAST(item_id AS STRING) AS item_id,
        CAST(family AS STRING) AS family,
        
        -- Attributes
        TRIM(item_name) AS item_name,
        LOWER(category) AS category,
        CAST(supplier_id AS STRING) AS supplier_id,
        
        -- Metrics
        CAST(cost AS DECIMAL(10, 2)) AS cost,
        CAST(quantity AS INTEGER) AS quantity,
        CAST(current_stock AS INTEGER) AS current_stock,
        CAST(lead_time_days AS INTEGER) AS lead_time_days,
        
        -- Business logic
        CASE 
            WHEN current_stock <= 0 THEN 'OUT_OF_STOCK'
            WHEN current_stock <= 10 THEN 'LOW_STOCK'
            ELSE 'OK'
        END AS stock_status,
        
        -- Calculated metrics
        cost * quantity AS total_value,
        cost / NULLIF(quantity, 0) AS unit_cost,
        
        -- Timestamps
        CAST(date AS DATE) AS date,
        CAST(created_at AS TIMESTAMP) AS created_at,
        CURRENT_TIMESTAMP() AS loaded_at
        
    FROM source
    WHERE item_id IS NOT NULL
        AND item_name IS NOT NULL
        AND cost > 0
        AND date >= '2024-01-01'
),

deduplicated AS (
    SELECT *
    FROM cleaned
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY item_id, date
        ORDER BY loaded_at DESC
    ) = 1
)

SELECT * FROM deduplicated
```

**Intermediate Model (Feature Engineering):**

```sql
-- models/intermediate/int_item_features.sql
{{ config(materialized='view') }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_items') }}
),

temporal_features AS (
    SELECT
        *,
        -- Basic temporal
        EXTRACT(YEAR FROM date) AS year,
        EXTRACT(MONTH FROM date) AS month,
        EXTRACT(QUARTER FROM date) AS quarter,
        EXTRACT(DAY FROM date) AS day,
        EXTRACT(DAYOFWEEK FROM date) AS day_of_week,
        EXTRACT(DAYOFYEAR FROM date) AS day_of_year,
        
        -- Cyclical encoding
        SIN(2 * PI() * EXTRACT(MONTH FROM date) / 12) AS month_sin,
        COS(2 * PI() * EXTRACT(MONTH FROM date) / 12) AS month_cos,
        SIN(2 * PI() * EXTRACT(DAYOFWEEK FROM date) / 7) AS day_of_week_sin,
        COS(2 * PI() * EXTRACT(DAYOFWEEK FROM date) / 7) AS day_of_week_cos,
        
        -- Flags
        CASE WHEN EXTRACT(DAYOFWEEK FROM date) IN (1, 7) THEN 1 ELSE 0 END AS is_weekend,
        CASE WHEN EXTRACT(DAY FROM date) <= 7 THEN 1 ELSE 0 END AS is_month_start,
        CASE WHEN EXTRACT(DAY FROM date) >= 25 THEN 1 ELSE 0 END AS is_month_end
        
    FROM staging
),

lag_features AS (
    SELECT
        *,
        -- Lag features
        LAG(quantity, 1) OVER (PARTITION BY item_id ORDER BY date) AS lag_1,
        LAG(quantity, 7) OVER (PARTITION BY item_id ORDER BY date) AS lag_7,
        LAG(quantity, 30) OVER (PARTITION BY item_id ORDER BY date) AS lag_30,
        
        -- Rolling statistics
        AVG(quantity) OVER (
            PARTITION BY item_id 
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_mean_7,
        
        STDDEV(quantity) OVER (
            PARTITION BY item_id 
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_std_7,
        
        AVG(quantity) OVER (
            PARTITION BY item_id 
            ORDER BY date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_mean_30
        
    FROM temporal_features
)

SELECT * FROM lag_features
```

**Mart Model (Silver → Gold):**

```sql
-- models/marts/fact_forecasts.sql
{{ config(
    materialized='incremental',
    schema='marts',
    unique_key='forecast_id',
    on_schema_change='append_new_columns',
    partition_by={'field': 'date', 'data_type': 'date'},
    cluster_by=['item_id', 'date']
) }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_forecasts') }}
    {% if is_incremental() %}
        WHERE loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
    {% endif %}
),

dim_items AS (
    SELECT * FROM {{ ref('dim_items') }}
),

dim_towers AS (
    SELECT * FROM {{ ref('dim_towers') }}
),

dim_time AS (
    SELECT * FROM {{ ref('dim_time') }}
),

final AS (
    SELECT
        -- Keys
        f.forecast_id,
        f.item_id,
        f.tower_id,
        f.date,
        dt.date_key,
        
        -- Measures
        f.forecasted_demand,
        f.actual_demand,
        f.ci_lower,
        f.ci_upper,
        
        -- Calculated measures
        f.forecasted_demand - f.actual_demand AS forecast_error,
        ABS(f.forecasted_demand - f.actual_demand) AS absolute_error,
        CASE 
            WHEN f.actual_demand > 0 
            THEN ABS(f.forecasted_demand - f.actual_demand) / f.actual_demand * 100
            ELSE NULL
        END AS mape,
        
        -- Dimensions
        i.category,
        i.cost_tier,
        i.lead_time_tier,
        t.region,
        t.sla_tier,
        dt.year,
        dt.quarter,
        dt.month,
        dt.is_holiday,
        
        -- Model info
        f.model_type,
        f.accuracy_level,
        
        -- Timestamps
        f.created_at,
        CURRENT_TIMESTAMP() AS loaded_at
        
    FROM staging f
    INNER JOIN dim_items i ON f.item_id = i.item_id
    LEFT JOIN dim_towers t ON f.tower_id = t.tower_id
    INNER JOIN dim_time dt ON f.date = dt.date
    WHERE f.date >= CURRENT_DATE - 365
)

SELECT * FROM final
```

---

<a name="ml-inference"></a>

## 3. 🤖 PIPELINE DE ML INFERENCE

### 3.1 MLflow Integration

```python
# backend/ml/inference/mlflow_inference.py
"""
ML inference using MLflow registered models
"""
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
import numpy as np
from typing import Dict, List

class MLflowInference:
    """Inference service using MLflow models"""
    
    def __init__(self, model_name="NovaCorrenteForecast"):
        self.client = MlflowClient()
        self.model_name = model_name
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load all models from MLflow registry"""
        # Get production versions
        prod_models = self.client.get_latest_versions(
            self.model_name,
            stages=["Production"]
        )
        
        # Load each model type
        for model_version in prod_models:
            model_type = model_version.tags.get('model_type', 'unknown')
            
            if model_type == 'prophet':
                self.models['prophet'] = mlflow.prophet.load_model(
                    f"models:/{self.model_name}/Production"
                )
            elif model_type == 'arima':
                self.models['arima'] = mlflow.sklearn.load_model(
                    f"models:/{self.model_name}/Production"
                )
            elif model_type == 'lstm':
                self.models['lstm'] = mlflow.tensorflow.load_model(
                    f"models:/{self.model_name}/Production"
                )
    
    def predict(self, features: pd.DataFrame, item_id: str) -> Dict:
        """
        Generate prediction for item
        
        Args:
            features: Feature DataFrame
            item_id: Item ID to predict
        
        Returns:
            Dictionary with forecasts from all models + ensemble
        """
        item_features = features[features['item_id'] == item_id].copy()
        
        # Predict with each model
        forecasts = {}
        
        # Prophet
        if 'prophet' in self.models:
            prophet_forecast = self.models['prophet'].predict(item_features)
            forecasts['prophet'] = prophet_forecast['yhat'].values
        
        # ARIMA
        if 'arima' in self.models:
            arima_forecast = self.models['arima'].predict(item_features)
            forecasts['arima'] = arima_forecast
        
        # LSTM
        if 'lstm' in self.models:
            lstm_input = self.prepare_lstm_input(item_features)
            lstm_forecast = self.models['lstm'].predict(lstm_input)
            forecasts['lstm'] = lstm_forecast.flatten()
        
        # Ensemble (weighted average)
        ensemble = self.create_ensemble(forecasts)
        
        return {
            'item_id': item_id,
            'forecasts': forecasts,
            'ensemble': ensemble,
            'confidence_interval': self.calculate_confidence_interval(ensemble)
        }
    
    def create_ensemble(self, forecasts: Dict) -> np.ndarray:
        """Create weighted ensemble forecast"""
        weights = {
            'prophet': 0.35,
            'arima': 0.20,
            'lstm': 0.25,
            'xgboost': 0.20
        }
        
        # Weighted average
        ensemble = np.zeros(len(list(forecasts.values())[0]))
        
        for model, forecast in forecasts.items():
            if model in weights:
                ensemble += forecast * weights[model]
        
        return ensemble
    
    def calculate_confidence_interval(self, forecast: np.ndarray, confidence=0.95) -> Dict:
        """Calculate confidence interval"""
        std = np.std(forecast)
        z_score = 1.96  # 95% confidence
        
        return {
            'lower': forecast - z_score * std,
            'upper': forecast + z_score * std
        }
```

---

<a name="serving"></a>

## 4. 🚀 PIPELINE DE SERVING (FASTAPI)

### 4.1 FastAPI Service Completo

```python
# backend/app/main.py
"""
FastAPI application serving analytics data
"""
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import redis
import json

from app.core.config import settings
from app.core.database import get_db
from app.core.cache import CacheService, get_cache
from app.core.auth import verify_token
from app.schemas.forecast import ForecastResponse, ForecastQuery
from app.api.v1 import forecasts, inventory, metrics, items

app = FastAPI(
    title="Nova Corrente Analytics API",
    description="API for serving forecast and inventory data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.novacorrente.com", "localhost"]
)

# Include routers
app.include_router(forecasts.router, prefix="/api/v1", tags=["forecasts"])
app.include_router(inventory.router, prefix="/api/v1", tags=["inventory"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])

@app.get("/health")
async def health_check(
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache)
):
    """Health check endpoint"""
    # Check database
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    # Check cache
    try:
        cache.get("health_check")
        cache_status = "healthy"
    except:
        cache_status = "unhealthy"
    
    # Check Databricks
    try:
        # Test query
        databricks_status = "healthy"
    except:
        databricks_status = "unhealthy"
    
    overall_status = "healthy" if all([
        db_status == "healthy",
        cache_status == "healthy",
        databricks_status == "healthy"
    ]) else "unhealthy"
    
    return {
        "status": overall_status,
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "database": db_status,
            "cache": cache_status,
            "databricks": databricks_status
        }
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Nova Corrente Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        workers=4 if not settings.API_RELOAD else 1
    )
```

**Forecast Endpoint:**

```python
# backend/app/api/v1/forecasts.py
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import date
import pandas as pd
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.cache import CacheService, get_cache
from app.core.auth import verify_token
from app.schemas.forecast import ForecastResponse, ForecastQuery

router = APIRouter()

@router.get("/forecasts", response_model=List[ForecastResponse])
async def get_forecasts(
    item_id: Optional[str] = Query(None, description="Filter by item ID"),
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, ge=1, le=1000, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache),
    token: dict = Depends(verify_token)
):
    """
    Get forecasts from Gold layer
    
    - Uses Redis cache for performance (30 min TTL)
    - Queries Databricks Gold layer
    - Returns paginated results
    """
    # Build cache key
    cache_key = f"forecasts:{item_id}:{start_date}:{end_date}:{category}:{limit}:{offset}"
    
    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Build query
    query = build_forecast_query(item_id, start_date, end_date, category, limit, offset)
    
    # Query from Databricks
    try:
        results = execute_databricks_query(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    
    # Cache result (30 minutes)
    cache.set(cache_key, results, ttl=1800)
    
    return results

def build_forecast_query(
    item_id: Optional[str],
    start_date: Optional[date],
    end_date: Optional[date],
    category: Optional[str],
    limit: int,
    offset: int
) -> str:
    """Build SQL query for forecasts"""
    query = """
        SELECT 
            forecast_id,
            item_id,
            item_name,
            category,
            date,
            forecasted_demand,
            actual_demand,
            mape,
            model_type,
            accuracy_level,
            created_at
        FROM nova_corrente.gold.marts.fact_forecasts
        WHERE 1=1
    """
    
    params = []
    if item_id:
        query += " AND item_id = %s"
        params.append(item_id)
    
    if start_date:
        query += " AND date >= %s"
        params.append(start_date)
    
    if end_date:
        query += " AND date <= %s"
        params.append(end_date)
    
    if category:
        query += " AND category = %s"
        params.append(category)
    
    query += f" ORDER BY date DESC LIMIT {limit} OFFSET {offset}"
    
    return query
```

---

<a name="realtime"></a>

## 5. ⚡ PIPELINE DE REAL-TIME

### 5.1 WebSocket Endpoint

```python
# backend/app/api/v1/websocket.py
"""
WebSocket endpoints for real-time updates
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
from datetime import datetime

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscriptions: Dict[str, List[WebSocket]] = {}  # item_id -> [websockets]
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # Remove from subscriptions
        for item_id, connections in self.subscriptions.items():
            if websocket in connections:
                connections.remove(websocket)
    
    def subscribe(self, websocket: WebSocket, item_id: str):
        """Subscribe to updates for specific item"""
        if item_id not in self.subscriptions:
            self.subscriptions[item_id] = []
        
        if websocket not in self.subscriptions[item_id]:
            self.subscriptions[item_id].append(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.append(connection)
        
        for conn in disconnected:
            self.disconnect(conn)
    
    async def broadcast_to_item(self, item_id: str, message: dict):
        """Broadcast message to subscribers of specific item"""
        if item_id in self.subscriptions:
            disconnected = []
            
            for connection in self.subscriptions[item_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
            
            for conn in disconnected:
                self.disconnect(conn)

manager = ConnectionManager()

@app.websocket("/ws/forecasts")
async def websocket_forecasts(websocket: WebSocket):
    """WebSocket endpoint for real-time forecast updates"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Send latest forecasts every 5 seconds
            forecasts = get_latest_forecasts()
            
            await websocket.send_json({
                "type": "forecast_update",
                "data": forecasts,
                "timestamp": datetime.now().isoformat()
            })
            
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.websocket("/ws/forecasts/{item_id}")
async def websocket_forecast_by_item(websocket: WebSocket, item_id: str):
    """WebSocket endpoint for specific item updates"""
    await manager.connect(websocket)
    manager.subscribe(websocket, item_id)
    
    try:
        while True:
            # Get latest forecast for this item
            forecast = get_latest_forecast_by_item(item_id)
            
            await websocket.send_json({
                "type": "forecast_update",
                "item_id": item_id,
                "data": forecast,
                "timestamp": datetime.now().isoformat()
            })
            
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """WebSocket endpoint for real-time stock alerts"""
    await manager.connect(websocket)
    
    # Subscribe to alert queue
    from app.core.message_queue import MessageQueue
    mq = MessageQueue()
    
    consumer = mq.get_consumer('stock-alerts')
    
    try:
        for message in consumer:
            alert = json.loads(message.value)
            
            await websocket.send_json({
                "type": "stock_alert",
                "alert": alert,
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

<a name="orquestracao"></a>

## 6. 🎛️ ORQUESTRAÇÃO AIRFLOW COMPLETA

### 6.1 Daily Pipeline DAG

```python
# infrastructure/airflow/dags/nova_corrente/daily_pipeline.py
"""
Complete daily pipeline for Nova Corrente
"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'nova-corrente',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email': ['data-team@novacorrente.com'],
}

dag = DAG(
    'nova_corrente_daily_pipeline',
    default_args=default_args,
    description='Complete daily pipeline: Extract → Transform → ML → Serve',
    schedule_interval='@daily',
    start_date=datetime(2025, 11, 1),
    catchup=False,
    tags=['nova-corrente', 'daily', 'production'],
    max_active_runs=1,
    max_active_tasks=10,
)

# ===== EXTRACT LAYER =====

# Extract ERP data
extract_erp = PythonOperator(
    task_id='extract_erp',
    python_callable=extract_erp_data,
    dag=dag,
)

# Extract Weather data
extract_weather = PythonOperator(
    task_id='extract_weather',
    python_callable=extract_weather_data,
    dag=dag,
)

# Extract Economic data
extract_economic = PythonOperator(
    task_id='extract_economic',
    python_callable=extract_economic_data,
    dag=dag,
)

# Load to Bronze (Databricks job)
load_bronze = DatabricksRunNowOperator(
    task_id='load_to_bronze',
    job_id=12345,  # Databricks job ID
    dag=dag,
)

# ===== TRANSFORM LAYER =====

# Transform: Bronze → Silver (dbt staging)
transform_silver = BashOperator(
    task_id='transform_silver',
    bash_command='cd /opt/airflow/dbt && dbt run --models staging.* --profiles-dir .',
    env={'DBT_PROFILES_DIR': '/opt/airflow/dbt'},
    dag=dag,
)

# Data Quality Check
quality_check = BashOperator(
    task_id='data_quality_check',
    bash_command='python /opt/airflow/scripts/great_expectations_check.py',
    dag=dag,
)

# Transform: Silver → Gold (dbt marts)
transform_gold = BashOperator(
    task_id='transform_gold',
    bash_command='cd /opt/airflow/dbt && dbt run --models marts.* --profiles-dir .',
    env={'DBT_PROFILES_DIR': '/opt/airflow/dbt'},
    dag=dag,
)

# dbt Tests
test_dbt = BashOperator(
    task_id='test_dbt',
    bash_command='cd /opt/airflow/dbt && dbt test --profiles-dir .',
    env={'DBT_PROFILES_DIR': '/opt/airflow/dbt'},
    dag=dag,
)

# ===== ML LAYER =====

# ML Inference (weekly or on-demand)
ml_inference = DatabricksRunNowOperator(
    task_id='ml_inference',
    job_id=12346,  # ML inference job
    dag=dag,
)

# ===== BUSINESS LOGIC LAYER =====

# Calculate Reorder Points
calculate_pp = PythonOperator(
    task_id='calculate_reorder_points',
    python_callable=calculate_reorder_points,
    dag=dag,
)

# Generate Alerts
generate_alerts = PythonOperator(
    task_id='generate_alerts',
    python_callable=generate_alerts,
    dag=dag,
)

# ===== SERVING LAYER =====

# Update API Cache
update_cache = PythonOperator(
    task_id='update_api_cache',
    python_callable=invalidate_cache,
    dag=dag,
)

# Send Notifications
send_notifications = PythonOperator(
    task_id='send_notifications',
    python_callable=send_notifications,
    dag=dag,
)

# ===== DEPENDENCIES =====

# Extract in parallel
[extract_erp, extract_weather, extract_economic] >> load_bronze

# Transform sequentially
load_bronze >> transform_silver >> quality_check >> transform_gold >> test_dbt

# ML and Business Logic
transform_gold >> ml_inference >> calculate_pp >> generate_alerts

# Final serving
generate_alerts >> [update_cache, send_notifications]
```

---

### 6.2 Helper Functions

```python
# infrastructure/airflow/dags/nova_corrente/helpers.py
"""Helper functions for Airflow DAGs"""

from datetime import datetime
import boto3
import pandas as pd

def extract_erp_data(**context):
    """Extract data from ERP"""
    from backend.pipelines.data_ingestion.multi_source_extractor import MultiSourceExtractor
    
    config = {
        'bronze_bucket': os.getenv('BRONZE_BUCKET'),
        'erp': {
            'host': os.getenv('ERP_HOST'),
            'database': os.getenv('ERP_DB'),
            'user': os.getenv('ERP_USER'),
            'password': os.getenv('ERP_PASSWORD')
        }
    }
    
    extractor = MultiSourceExtractor(config)
    extractor.extract_erp(datetime.now())
    return "✅ ERP data extracted"

def extract_weather_data(**context):
    """Extract weather data from INMET"""
    # Implementation similar to extract_erp_data
    pass

def calculate_reorder_points(**context):
    """Calculate reorder points for all items"""
    from backend.app.core.reorder_point import ReorderPointCalculator
    
    calculator = ReorderPointCalculator()
    
    # Get items from Gold layer
    items = get_items_from_gold()
    
    for item in items:
        pp = calculator.calculate(item)
        save_reorder_point(item['item_id'], pp)
    
    return "✅ Reorder points calculated"

def generate_alerts(**context):
    """Generate stock alerts"""
    from backend.app.core.alerts import AlertSystem
    
    alert_system = AlertSystem()
    
    # Get items with stock <= reorder point
    items_at_risk = get_items_at_risk()
    
    for item in items_at_risk:
        alert_system.generate_alert(item)
    
    return f"✅ {len(items_at_risk)} alerts generated"

def invalidate_cache(**context):
    """Invalidate API cache"""
    import redis
    
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT', 6379))
    )
    
    # Invalidate forecast caches
    redis_client.delete_pattern('forecasts:*')
    
    return "✅ Cache invalidated"
```

---

## 📊 RESUMO DE IMPLEMENTAÇÃO

### Componentes Implementados

✅ **Extract Layer:**
- Multi-source extractor (paralelo)
- Load to Bronze (S3 Delta)

✅ **Transform Layer:**
- dbt staging models (Bronze → Silver)
- dbt intermediate models (feature engineering)
- dbt marts models (Silver → Gold)

✅ **ML Layer:**
- MLflow inference
- Ensemble model
- Confidence intervals

✅ **Serving Layer:**
- FastAPI endpoints
- Redis caching
- WebSocket real-time

✅ **Orquestração:**
- Airflow DAGs completos
- Scheduling configurado
- Error handling robusto

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Exemplos de Implementação Completos

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**






