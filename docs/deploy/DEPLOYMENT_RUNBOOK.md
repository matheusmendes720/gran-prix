# 🚀 DEPLOYMENT RUNBOOK
## Nova Corrente - Production Deployment Guide

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Production-Ready

---

## 📋 OVERVIEW

This runbook provides step-by-step instructions for deploying the Nova Corrente analytics dashboard with **NO ML Ops logic in deployment**.

**Key Constraint:** All ML processing runs in a separate environment. Deployment only reads precomputed ML results.

---

## ✅ PRE-DEPLOYMENT VALIDATION CHECKLIST

### Before Deployment
- [ ] **ML Dependency Validation:** Run `python scripts/validation/validate_deployment.py`
- [ ] **Docker Image Validation:** Verify image size < 600 MB
- [ ] **Environment Variables:** Copy `.env.deployment.template` to `.env` and configure
- [ ] **Health Checks:** Verify all services have health check endpoints
- [ ] **ML Results Path:** Verify ML results path exists and is readable
- [ ] **No ML Services:** Verify docker-compose.yml has NO scheduler/ML services

### Validation Commands
```bash
# Run full validation suite
python scripts/validation/validate_deployment.py

# Check ML dependencies
python scripts/validation/check_ml_dependencies.py

# Check ML endpoints
python scripts/validation/check_ml_endpoints.py

# Check ML imports
python scripts/validation/check_ml_imports.py

# Check Docker image (if Docker available)
python scripts/validation/check_docker_image.py
```

---

## 🚀 DEPLOYMENT PROCESS

### Step 1: Prepare Environment
```bash
# 1. Copy environment template
cp .env.deployment.template .env

# 2. Configure environment variables
# Edit .env with your values:
# - DATABASE_URL
# - MINIO_ENDPOINT
# - REDIS_URL
# - ML_RESULTS_PATH (read-only path to precomputed ML results)
# - SECRET_KEY (generate strong random key)
# - CORS_ORIGINS

# 3. Verify ML results path exists
ls -la $ML_RESULTS_PATH
```

### Step 2: Build Docker Images
```bash
# Build backend image (NO ML dependencies)
docker build -t nova-corrente-backend:deployment \
  -f infrastructure/docker/Dockerfile.backend.deployment .

# Verify image size
docker images | grep nova-corrente-backend

# Verify NO ML dependencies
docker run --rm nova-corrente-backend:deployment pip list | grep -iE "(torch|tensorflow|sklearn|mlflow)"
# Should return: No matches (empty)
```

### Step 3: Start Services
```bash
# Start all services
docker-compose up -d

# Verify all services are running
docker-compose ps

# Check health endpoints
curl http://localhost:5000/health
curl http://localhost:9000/minio/health/live
redis-cli ping
```

### Step 4: Verify Deployment
```bash
# Run smoke tests
curl http://localhost:5000/api/v1/items
curl http://localhost:5000/api/v1/forecasts/summary?start=2025-11-01&end=2025-11-30

# Check health endpoint includes ML validation
curl http://localhost:5000/health | jq '.ml_dependencies'
# Should return: {"status": "compliant", "message": "No ML dependencies detected"}
```

---

## 📊 MONITORING & HEALTH CHECKS

### Health Endpoints
- **Backend:** `http://localhost:5000/health`
- **MinIO:** `http://localhost:9000/minio/health/live`
- **Redis:** `redis-cli ping`

### Health Check Response
```json
{
  "status": "healthy",
  "database": "connected",
  "parquet_access": "ok",
  "cache": "ok",
  "ml_dependencies": {
    "status": "compliant",
    "message": "No ML dependencies detected",
    "checked_packages": ["torch", "tensorflow", "sklearn", "mlflow"],
    "violations": []
  },
  "timestamp": "2025-11-01T10:00:00Z"
}
```

---

## 🔄 ROLLBACK PROCEDURE

### Rollback to Previous Version
```bash
# 1. Stop current services
docker-compose down

# 2. Restore previous docker-compose.yml
git checkout <previous-commit> -- docker-compose.yml

# 3. Restore previous images (if needed)
docker pull nova-corrente-backend:<previous-tag>

# 4. Start services
docker-compose up -d

# 5. Verify health
curl http://localhost:5000/health
```

---

## 🚨 TROUBLESHOOTING

### Issue: ML Dependencies Detected
**Symptom:** Health check returns ML dependency violations

**Solution:**
1. Verify `requirements_deployment.txt` has NO ML dependencies
2. Rebuild Docker image: `docker build -t nova-corrente-backend:deployment -f infrastructure/docker/Dockerfile.backend.deployment .`
3. Run validation: `python scripts/validation/check_ml_dependencies.py`

### Issue: ML Results Not Found
**Symptom:** API returns 404 for ML results

**Solution:**
1. Verify ML results path exists: `ls -la $ML_RESULTS_PATH`
2. Check ML results mount in docker-compose.yml
3. Verify ML environment has output results to shared storage

### Issue: Image Size Too Large
**Symptom:** Docker image > 600 MB

**Solution:**
1. Check for unnecessary dependencies in `requirements_deployment.txt`
2. Remove unused packages
3. Use multi-stage build if needed
4. Rebuild image

---

## 📝 POST-DEPLOYMENT CHECKLIST

- [ ] All services running (docker-compose ps)
- [ ] Health checks passing (curl /health)
- [ ] ML dependency validation passing (health check response)
- [ ] API endpoints accessible (curl /api/v1/items)
- [ ] ML results readable (verify ML_RESULTS_PATH)
- [ ] Frontend accessible (http://localhost:3000)
- [ ] Monitoring configured (health checks, logs)

---

## 📚 REFERENCE LINKS

- [Global Constraints](../diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)
- [Deploy Cluster](../diagnostics/clusters/04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md)
- [Validation Guide](../validation/VALIDATION_GUIDE.md)
- [ML Environment Setup](../ml/ML_ENVIRONMENT_SETUP.md)

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Production-Ready

