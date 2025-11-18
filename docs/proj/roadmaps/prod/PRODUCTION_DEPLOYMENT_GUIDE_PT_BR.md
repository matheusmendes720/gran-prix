# 🚀 GUIA DE DEPLOYMENT EM PRODUÇÃO (4-DAY SPRINT)
## Nova Corrente - Analytics Engineering + Fullstack App

**Versão:** 2.0 (Atualizado para 4-Day Sprint)  
**Data:** Novembro 2025  
**Status:** ✅ Guia Atualizado - Escopo Reduzido para 4-Day Sprint

---

## 🚨 ATUALIZAÇÃO DE ESCOPO - 4-DAY SPRINT

**Última Atualização:** Novembro 2025  
**Escopo Atual:** 4-Day Sprint (Reduzido)  
**Referência:** [docs/diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md](../../diagnostics/clusters/00_OVERVIEW_INDEX_4DAY_SPRINT_PT_BR.md)

### 🔄 Mudanças de Escopo:

**Timeline:**
- ❌ **Anterior:** 16 semanas (4 meses)
- ✅ **Atual:** 4 dias (D0-D4) - Sprint intensivo

**Stack Tecnológico:**
- ❌ **Anterior:** Terraform + S3 + Databricks + Airflow + dbt + MLflow
- ✅ **Atual:** Docker Compose + MinIO + DuckDB + Simple Scheduler + Python Scripts

**ML Strategy:**
- ❌ **Anterior:** ML Ops completo em deployment
- ✅ **Atual:** **NO ML OPS IN DEPLOYMENT** - ML processing separado

### 📋 Escopo Anterior (Arquivado):

O guia original de deployment foi planejado para 16 semanas com stack completo. O escopo foi reduzido para um sprint de 4 dias com foco em MVP funcional. O guia original foi mantido para referência futura nas seções marcadas como "Futuro - Referência Original".

---

## 📋 ÍNDICE

1. [Pré-requisitos de Produção](#pre-requisitos)
2. [Infraestrutura de Produção](#infraestrutura)
3. [Deployment de Pipelines](#deployment-pipelines)
4. [Deployment da API (FastAPI)](#deployment-api)
5. [Deployment do Frontend (Next.js)](#deployment-frontend)
6. [Monitoramento e Observabilidade](#monitoramento)
7. [Backup e Disaster Recovery](#backup)
8. [Checklist Final de Produção](#checklist)

---

<a name="pre-requisitos"></a>

## 1. ✅ PRÉ-REQUISITOS DE PRODUÇÃO

### 1.1 Infraestrutura Base (4-Day Sprint - Simplificada)

**Local/Docker Deployment:**
- [ ] Docker Compose configurado
- [ ] MinIO setup (local/Docker)
- [ ] PostgreSQL (opcional, para pequenos datasets)
- [ ] Redis (opcional, para cache)
- [ ] No Terraform (removido para simplificação)
- [ ] No Cloud Provider (removido para simplificação)

**Storage:**
- [ ] MinIO buckets criados (bronze/silver/gold)
- [ ] Parquet storage structure configurada
- [ ] No Databricks (removido para simplificação)
- [ ] No S3 (removido para simplificação)

**Orquestração:**
- [ ] Simple scheduler (Python scripts)
- [ ] Docker Compose for services
- [ ] No Airflow (removido para simplificação)

### 1.1.1 Infraestrutura Expandida (Futuro - Referência Original)

**Nota:** A infraestrutura original foi planejada para 16 semanas. Mantida para referência futura.

**Cloud Provider (Original):**
- [ ] Conta cloud configurada
- [ ] Terraform configurado
- [ ] S3/Cloud Storage buckets criados
- [ ] IAM roles e policies configurados
- [ ] VPC e networking configurados

**Databricks (Original):**
- [ ] Workspace criado
- [ ] Clusters configurados (dev/staging/prod)
- [ ] Unity Catalog configurado
- [ ] SQL warehouses criados

**Airflow (Original):**
- [ ] Airflow instalado (Managed ou self-hosted)
- [ ] DAGs configurados
- [ ] Connections configuradas
- [ ] Variables definidas

---

### 1.2 Serviços Adicionais (4-Day Sprint - Simplificados)

**Redis (Optional):**
- [ ] Redis instalado (Docker/local)
- [ ] Configurado para cache
- [ ] No backup necessário (opcional)

**No Message Queue:**
- [ ] No Kafka (removido para simplificação)
- [ ] No Message Queue (removido para simplificação)

**Monitoring (Simplificado):**
- [ ] Health checks configurados
- [ ] Basic logging (FastAPI/Python)
- [ ] No Datadog/Prometheus/Grafana (removido para simplificação)

### 1.2.1 Serviços Expandidos (Futuro - Referência Original)

**Nota:** Os serviços originais foram planejados para 16 semanas. Mantidos para referência futura.

**Redis (Original):**
- [ ] Redis instalado (AWS ElastiCache ou self-hosted)
- [ ] Configurado para cache
- [ ] Backup configurado

**Message Queue (Original):**
- [ ] Kafka instalado (Confluent Cloud ou self-hosted)
- [ ] Topics criados
- [ ] Consumers/Producers configurados

**Monitoring (Original):**
- [ ] Datadog/Prometheus configurado
- [ ] Grafana dashboards criados
- [ ] Alerting configurado

---

<a name="infraestrutura"></a>

## 2. 🏗️ INFRAESTRUTURA DE PRODUÇÃO - 4-DAY SPRINT

### 2.1 Docker Compose Production Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
      DUCKDB_PATH: /data/duckdb
    volumes:
      - ./data:/data
    depends_on:
      - minio
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
    depends_on:
      - backend

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  minio_data:
  redis_data:
```

### 2.1.1 Terraform Production Setup (Futuro - Referência Original)

**Nota:** O setup original com Terraform foi planejado para 16 semanas. Mantido para referência futura.

```hcl
# infrastructure/terraform/environments/prod/main.tf
terraform {
  backend "s3" {
    bucket         = "nova-corrente-terraform-prod"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks-prod"
  }
}

module "production" {
  source = "../../modules"
  
  environment = "prod"
  
  # S3 Buckets
  bronze_bucket_name = "nova-corrente-data-lake-bronze-prod"
  silver_bucket_name = "nova-corrente-data-lake-silver-prod"
  gold_bucket_name   = "nova-corrente-data-lake-gold-prod"
  
  # Databricks
  databricks_workspace_name = "nova-corrente-prod"
  
  # Networking
  vpc_cidr = "10.0.0.0/16"
  
  # Security
  enable_encryption = true
  enable_versioning = true
  
  tags = {
    Environment = "production"
    Project     = "analytics-engineering"
    ManagedBy   = "terraform"
  }
}
```

**Deploy:**
```bash
cd infrastructure/terraform/environments/prod
terraform init
terraform plan
terraform apply
```

---

### 2.2 Kubernetes Setup (Opcional)

**Para escalabilidade máxima:**

```yaml
# infrastructure/kubernetes/production/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nova-corrente-prod

---
# infrastructure/kubernetes/production/fastapi-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-backend
  namespace: nova-corrente-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-backend
  template:
    metadata:
      labels:
        app: fastapi-backend
    spec:
      containers:
      - name: fastapi
        image: nova-corrente/backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-secret
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  namespace: nova-corrente-prod
spec:
  selector:
    app: fastapi-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

---

<a name="deployment-pipelines"></a>

## 3. 🔄 DEPLOYMENT DE PIPELINES - 4-DAY SPRINT

### 3.1 Python Scripts Deployment (Simplificado)

**NOTA:** No dbt deployment. Python scripts + DuckDB são usados para transformações.

**Deployment (4-Day Sprint):**

```bash
# Deploy Python ETL scripts
cd scripts/etl
python extract_and_load.py
python transform_with_duckdb.py
python load_to_gold.py
```

**GitHub Actions (Optional):**

```yaml
# .github/workflows/data-pipeline.yml
name: Data Pipeline (4-Day Sprint)
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  run-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install duckdb pandas minio
      
      - name: Run ETL Pipeline
        env:
          MINIO_ENDPOINT: ${{ secrets.MINIO_ENDPOINT }}
          MINIO_ACCESS_KEY: ${{ secrets.MINIO_ACCESS_KEY }}
          MINIO_SECRET_KEY: ${{ secrets.MINIO_SECRET_KEY }}
        run: |
          python scripts/etl/extract_and_load.py
          python scripts/etl/transform_with_duckdb.py
          python scripts/etl/load_to_gold.py
      
      - name: Validate Pipeline
        run: |
          python scripts/etl/validate_pipeline.py
```

### 3.1.1 dbt Deployment (Futuro - Referência Original)

**Nota:** O deployment original com dbt foi planejado para 16 semanas. Mantido para referência futura.

### 3.1 dbt Deployment (Original)

**CI/CD Pipeline (GitHub Actions):**

```yaml
# .github/workflows/dbt-deploy.yml
name: dbt Deploy to Production

on:
  push:
    branches: [main]
    paths:
      - 'dbt/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dbt
        run: |
          pip install dbt-databricks
      
      - name: Run dbt tests (staging)
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: |
          cd dbt
          dbt deps
          dbt run --models staging.*
          dbt test --models staging.*
      
      - name: Run dbt (marts)
        if: success()
        run: |
          cd dbt
          dbt run --models marts.*
          dbt test --models marts.*
      
      - name: Generate docs
        run: |
          cd dbt
          dbt docs generate
```

---

### 3.2 Simple Scheduler Deployment (4-Day Sprint)

**NOTA:** No Airflow deployment. Simple scheduler (Python scripts) é usado para orquestração.

**Deployment (4-Day Sprint):**

```python
# scripts/scheduler.py
import schedule
import time
from scripts.etl.extract_and_load import extract_and_load
from scripts.etl.transform_with_duckdb import transform_with_duckdb
from scripts.etl.load_to_gold import load_to_gold

def run_data_pipeline():
    """Run complete data pipeline"""
    try:
        # Extract & Load
        extract_and_load()
        
        # Transform
        transform_with_duckdb()
        
        # Load to Gold
        load_to_gold()
        
        print("✅ Pipeline completed successfully")
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        # Send alert (email/Slack)

# Schedule daily at 2 AM
schedule.every().day.at("02:00").do(run_data_pipeline)

if __name__ == "__main__":
    print("🚀 Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)
```

**Docker Deployment:**

```yaml
# docker-compose.yml (add scheduler service)
  scheduler:
    build: ./scripts
    command: python scheduler.py
    environment:
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - ./data:/data
    depends_on:
      - minio
    restart: unless-stopped
```

### 3.2.1 Airflow DAGs Deployment (Futuro - Referência Original)

**Nota:** O deployment original com Airflow foi planejado para 16 semanas. Mantido para referência futura.

**Deployment automático (Original):**

```bash
# Deploy DAGs to Airflow
scp dags/nova_corrente/*.py airflow@airflow-server:/opt/airflow/dags/nova_corrente/

# Ou usar git sync
# Airflow pode sincronizar DAGs de um repositório Git automaticamente
```

**Airflow Config (Original):**

```python
# airflow.cfg
[core]
dags_folder = /opt/airflow/dags
dagbag_import_timeout = 30
dagbag_fetch_timeout = 10

[webserver]
reload_on_plugin_change = True
enable_proxy_fix = True
```

---

<a name="deployment-api"></a>

## 4. 🚀 DEPLOYMENT DA API (FASTAPI) - 4-DAY SPRINT

### 4.1 Docker Production Image (Simplificado)

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies (NO ML dependencies)
COPY backend/requirements_deployment.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ /app/

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV MINIO_ENDPOINT=minio:9000
ENV DUCKDB_PATH=/data/duckdb

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**NOTA:** `requirements_deployment.txt` deve conter apenas dependências não-ML:
- FastAPI, uvicorn, pydantic
- DuckDB, pandas
- MinIO client
- Redis client
- **NO PyTorch, TensorFlow, scikit-learn, MLflow**

**Build & Deploy (Docker Compose):**
```bash
# Build and start all services
docker-compose up -d --build

# Check health
docker-compose ps
curl http://localhost:8000/health
```

---

### 4.2 Environment Variables (4-Day Sprint)

```bash
# backend/.env.production
# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# MinIO
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_BRONZE=bronze
MINIO_BUCKET_SILVER=silver
MINIO_BUCKET_GOLD=gold

# DuckDB
DUCKDB_PATH=/data/duckdb
DUCKDB_READ_ONLY=true

# Redis (Optional)
REDIS_HOST=redis
REDIS_PORT=6379

# Security
SECRET_KEY=<secret-key>
ALGORITHM=HS256

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 4.2.1 Environment Variables Expandidos (Futuro - Referência Original)

**Nota:** As variáveis originais foram planejadas para 16 semanas. Mantidas para referência futura.

```bash
# backend/.env.production (Original)
# API
API_HOST=0.0.0.0
API_PORT=5000
API_RELOAD=false

# Database
DATABASE_URL=postgresql://user:pass@db-prod:5432/nova_corrente

# Databricks
DATABRICKS_HOST=https://workspace.cloud.databricks.com
DATABRICKS_TOKEN=<token>
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<warehouse-id>

# Redis
REDIS_HOST=redis-prod.cache.amazonaws.com
REDIS_PORT=6379
REDIS_PASSWORD=<password>

# Security
SECRET_KEY=<secret-key>
ALGORITHM=HS256

# CORS
CORS_ORIGINS=https://dashboard.novacorrente.com,https://app.novacorrente.com
```

---

<a name="deployment-frontend"></a>

## 5. 💻 DEPLOYMENT DO FRONTEND (REACT) - 4-DAY SPRINT

### 5.1 Docker Production Image (Simplificado)

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./
RUN npm ci

# Copy source
COPY frontend/ ./

# Build (React + Vite)
RUN npm run build

# Production image (Nginx)
FROM nginx:alpine

WORKDIR /app

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
```

**NOTA:** Frontend é React + Vite, não Next.js. Build produz arquivos estáticos servidos por Nginx.

---

### 5.2 Environment Variables (4-Day Sprint)

```bash
# frontend/.env.production
REACT_APP_API_URL=http://localhost:8000
REACT_APP_MINIO_ENDPOINT=http://localhost:9000
NODE_ENV=production
```

---

### 5.3 Docker Compose Deployment (4-Day Sprint)

**NOTA:** No Vercel deployment. Docker Compose é usado para deployment local/self-hosted.

**docker-compose.yml (frontend service):**

```yaml
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      REACT_APP_API_URL: http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped
```

### 5.3.1 Vercel Deployment (Futuro - Referência Original)

**Nota:** O deployment original com Vercel foi planejado para 16 semanas. Mantido para referência futura.

**vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "env": {
    "NEXT_PUBLIC_API_URL": "https://api.novacorrente.com"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        }
      ]
    }
  ]
}
```

**Deploy:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

---

<a name="monitoramento"></a>

## 6. 📊 MONITORAMENTO E OBSERVABILIDADE

### 6.1 Application Monitoring

**Datadog Integration:**

```python
# backend/app/core/monitoring.py
from datadog import initialize, statsd

initialize(api_key=os.getenv('DATADOG_API_KEY'), app_key=os.getenv('DATADOG_APP_KEY'))

def monitor_api_call(func):
    """Monitor API calls"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            statsd.increment('api.success', tags=[f'endpoint:{func.__name__}'])
            return result
        except Exception as e:
            statsd.increment('api.error', tags=[f'endpoint:{func.__name__}', f'error:{type(e).__name__}'])
            raise
        finally:
            duration = time.time() - start
            statsd.histogram('api.duration', duration, tags=[f'endpoint:{func.__name__}'])
    return wrapper
```

---

### 6.2 Pipeline Monitoring

**Airflow + Custom Metrics:**

```python
# Airflow DAG with monitoring
from airflow.operators.python import PythonOperator

def monitored_pipeline():
    """Pipeline with monitoring"""
    start_time = time.time()
    
    try:
        # Run pipeline
        extract()
        transform()
        load()
        
        # Log success
        statsd.increment('pipeline.success', tags=['pipeline:daily'])
        
    except Exception as e:
        # Log error
        statsd.increment('pipeline.error', tags=['pipeline:daily', f'error:{type(e).__name__}'])
        raise
    finally:
        duration = time.time() - start_time
        statsd.histogram('pipeline.duration', duration, tags=['pipeline:daily'])
```

---

### 6.3 Logging

**Structured Logging:**

```python
# backend/app/core/logging.py
import logging
import json
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Setup structured logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Usage
logger = setup_logging()
logger.info("Pipeline started", extra={
    "pipeline": "daily_forecast",
    "execution_date": execution_date.isoformat()
})
```

---

<a name="backup"></a>

## 7. 💾 BACKUP E DISASTER RECOVERY

### 7.1 Data Backup Strategy

**S3 Lifecycle Policies:**

```hcl
# Terraform: S3 lifecycle for backups
resource "aws_s3_bucket_lifecycle_configuration" "gold_backup" {
  bucket = aws_s3_bucket.gold.id

  rule {
    id     = "backup-to-glacier"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    transition {
      days          = 90
      storage_class = "DEEP_ARCHIVE"
    }
  }
}
```

**Delta Lake Backups:**

```python
# Backup Delta tables
def backup_delta_table(table_path, backup_path):
    """Backup Delta table"""
    df = spark.read.format("delta").load(table_path)
    df.write.format("delta").save(backup_path)
    print(f"✅ Backup created: {backup_path}")
```

---

### 7.2 Disaster Recovery Plan

**RTO (Recovery Time Objective):** < 4 horas  
**RPO (Recovery Point Objective):** < 1 hora

**Procedimentos:**
1. Backup automático diário
2. Testes de restore mensais
3. Documentação de procedimentos
4. Runbook de recuperação

---

<a name="checklist"></a>

## 8. ✅ CHECKLIST FINAL DE PRODUÇÃO

### Infraestrutura

- [ ] Terraform aplicado em produção
- [ ] S3 buckets criados (bronze/silver/gold)
- [ ] Databricks workspace configurado
- [ ] Airflow instalado e configurado
- [ ] Redis configurado
- [ ] Kafka configurado (se usado)

### Pipelines

- [ ] dbt models deployados em produção
- [ ] Airflow DAGs deployados
- [ ] Pipelines testados em staging
- [ ] Data quality validada
- [ ] Monitoring configurado

### API Backend

- [ ] FastAPI deployado em produção
- [ ] Health checks funcionando
- [ ] CORS configurado corretamente
- [ ] Authentication implementada
- [ ] Caching configurado
- [ ] Error handling robusto

### Frontend

- [ ] Next.js buildado para produção
- [ ] Environment variables configuradas
- [ ] API integration testada
- [ ] WebSocket funcionando
- [ ] Error boundaries implementados

### Monitoramento

- [ ] Logging configurado
- [ ] Metrics coletadas
- [ ] Alerts configurados
- [ ] Dashboards criados
- [ ] On-call rotacionado

### Segurança

- [ ] Secrets gerenciados (AWS Secrets Manager)
- [ ] SSL/TLS configurado
- [ ] Firewall rules aplicadas
- [ ] Access control implementado
- [ ] Backup encryptado

### Documentação

- [ ] Runbooks criados
- [ ] Procedures documentadas
- [ ] Troubleshooting guide atualizado
- [ ] Onboarding docs completos

---

## 🚀 DEPLOYMENT ORDER

**Sequência Recomendada:**

1. **Infraestrutura** (Terraform) → 1 dia
2. **Databricks** → 1 dia
3. **Airflow** → 1 dia
4. **Pipelines** (dbt) → 2 dias
5. **API Backend** → 1 dia
6. **Frontend** → 1 dia
7. **Monitoring** → 1 dia
8. **Testing** → 2 dias

**Total:** ~10 dias úteis

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia de Deployment Completo

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**








