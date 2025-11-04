# 🚀 GUIA DE DEPLOYMENT EM PRODUÇÃO
## Nova Corrente - Analytics Engineering + Fullstack App

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Guia Completo de Produção

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

### 1.1 Infraestrutura Base

**Cloud Provider (AWS/GCP/Azure):**
- [ ] Conta cloud configurada
- [ ] Terraform configurado
- [ ] S3/Cloud Storage buckets criados
- [ ] IAM roles e policies configurados
- [ ] VPC e networking configurados

**Databricks:**
- [ ] Workspace criado
- [ ] Clusters configurados (dev/staging/prod)
- [ ] Unity Catalog configurado
- [ ] SQL warehouses criados

**Airflow:**
- [ ] Airflow instalado (Managed ou self-hosted)
- [ ] DAGs configurados
- [ ] Connections configuradas
- [ ] Variables definidas

---

### 1.2 Serviços Adicionais

**Redis:**
- [ ] Redis instalado (AWS ElastiCache ou self-hosted)
- [ ] Configurado para cache
- [ ] Backup configurado

**Message Queue:**
- [ ] Kafka instalado (Confluent Cloud ou self-hosted)
- [ ] Topics criados
- [ ] Consumers/Producers configurados

**Monitoring:**
- [ ] Datadog/Prometheus configurado
- [ ] Grafana dashboards criados
- [ ] Alerting configurado

---

<a name="infraestrutura"></a>

## 2. 🏗️ INFRAESTRUTURA DE PRODUÇÃO

### 2.1 Terraform Production Setup

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

## 3. 🔄 DEPLOYMENT DE PIPELINES

### 3.1 dbt Deployment

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

### 3.2 Airflow DAGs Deployment

**Deployment automático:**

```bash
# Deploy DAGs to Airflow
scp dags/nova_corrente/*.py airflow@airflow-server:/opt/airflow/dags/nova_corrente/

# Ou usar git sync
# Airflow pode sincronizar DAGs de um repositório Git automaticamente
```

**Airflow Config:**

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

## 4. 🚀 DEPLOYMENT DA API (FASTAPI)

### 4.1 Docker Production Image

```dockerfile
# infrastructure/docker/Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ /app/

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=5000

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "4"]
```

**Build & Deploy:**
```bash
# Build image
docker build -f infrastructure/docker/Dockerfile.backend -t nova-corrente/backend:latest .

# Tag for registry
docker tag nova-corrente/backend:latest registry.novacorrente.com/backend:v1.0.0

# Push to registry
docker push registry.novacorrente.com/backend:v1.0.0

# Deploy to production
kubectl apply -f infrastructure/kubernetes/production/fastapi-deployment.yaml
```

---

### 4.2 Environment Variables

```bash
# backend/.env.production
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

## 5. 💻 DEPLOYMENT DO FRONTEND (NEXT.JS)

### 5.1 Docker Production Image

```dockerfile
# infrastructure/docker/Dockerfile.frontend
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./
RUN npm ci

# Copy source
COPY frontend/ ./

# Build
RUN npm run build

# Production image
FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy built files
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./

# Install production dependencies
RUN npm ci --only=production

EXPOSE 3000

CMD ["npm", "start"]
```

---

### 5.2 Environment Variables

```bash
# frontend/.env.production
NEXT_PUBLIC_API_URL=https://api.novacorrente.com
NEXT_PUBLIC_WS_URL=wss://api.novacorrente.com/ws
NODE_ENV=production
```

---

### 5.3 Vercel Deployment (Recomendado)

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







