# 🚀 DEPLOY CLUSTER - 4-DAY SPRINT PLAN
## Nova Corrente - Deployment & Infrastructure

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** 🚀 Execution-Ready  
**Sprint:** 4 Days (D0-D4)  
**Cluster Lead:** DevOps/Backend Lead  
**Team Size:** 1 Engineer

---

## 📋 QUICK ORIENTATION

**Goal:** Deploy the minimal stack to run in a reproducible dev/staging environment and make it accessible to stakeholders by Day 4.

**Key Constraint:** Use Docker Compose for local/staging, or single cloud VM if account exists. Default to local compose for reliability in 4 days. **NO ML dependencies in containers.**

**Reference Documents:**
- [Data Cluster](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md) - MinIO/S3 setup
- [Backend Cluster](./02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - API deployment
- [Frontend Cluster](./03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - Frontend deployment
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy

---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Reference:** [Global Constraints Document](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Deployment containers must exclude all ML dependencies.

**Deploy Cluster Specific Rules:**
- ✅ Containers must **exclude** any ML dependencies (PyTorch, TensorFlow, scikit-learn, MLflow)
- ✅ Docker images remain lightweight (target: < 600 MB per image)
- ✅ Compute layer limited to CPU—no GPU scheduling or drivers required
- ✅ Only services deployed: `minio`/`s3`, `backend`, `frontend`, `redis`, `duckdb` runtime
- ✅ Deployment runs identically in air-gapped or offline environments
- ❌ **NO ML services** in docker-compose
- ❌ **NO GPU drivers** or CUDA dependencies

**Validation:**
- [ ] Check all Dockerfiles have NO ML dependencies
- [ ] Verify image sizes < 600 MB per container
- [ ] Verify CPU-only deployment (no GPU required)
- [ ] Test offline deployment (disconnect from internet, verify all services work)
- [ ] Verify docker-compose has NO ML services

---

## 🎯 KEY CONSTRAINTS & ASSUMPTIONS

### Technical Stack
- ✅ **Orchestration:** Docker Compose (local/staging)
- ✅ **Services:** MinIO (or S3), Backend (FastAPI), Frontend (Nginx), Redis (optional)
- ✅ **Monitoring:** Health checks, basic logging
- ✅ **Security:** Environment variables, API keys
- ❌ **Deferred:** Kubernetes, Terraform, CI/CD pipelines, monitoring tools
- ❌ **NO ML services:** No MLflow, no model serving, no scheduler with ML processing

### Deployment Strategy
- **Local/Staging:** Docker Compose (default)
- **Cloud (if available):** Single VM with Docker Compose or ECS/Fargate minimal
- **Public Access:** Cloudflare Tunnel or ngrok (if needed)
- **ML Processing:** Separate environment (NOT in deployment)

---

## 📅 DELIVERABLES (DAY-BY-DAY)

### **D0 (TODAY): Prepare Dockerfiles & Compose** ⏱️ 2-4 hours
**Owner:** DevOps/Backend Lead  
**Deliverables:**

#### Docker Setup
- [ ] Create Dockerfile for backend (Python, FastAPI, Uvicorn) - **NO ML dependencies**
- [ ] Create Dockerfile for frontend (build + Nginx)
- [ ] Create `docker-compose.yml` with services:
  - [ ] MinIO (or S3 stub)
  - [ ] Backend (FastAPI) - **NO ML dependencies**
  - [ ] Frontend (Nginx)
  - [ ] Redis (optional, for caching)
  - [ ] **NO ML services** (no MLflow, no model serving, no scheduler with ML)
- [ ] **Verify Dockerfile excludes ML dependencies:**
  - [ ] Check `requirements_deployment.txt` has NO PyTorch, TensorFlow, scikit-learn, MLflow
  - [ ] Target image size < 600 MB
  - [ ] No GPU drivers or CUDA
- [ ] Configure volumes and networks
- [ ] Add health checks

**Acceptance Criteria:**
- ✅ Dockerfiles created
- ✅ Docker-compose.yml configured
- ✅ NO ML dependencies in Dockerfiles
- ✅ All services defined

**Output Files:**
- `backend/Dockerfile` or `infrastructure/docker/Dockerfile.backend.deployment` - Backend Dockerfile
- `frontend/Dockerfile` or `infrastructure/docker/Dockerfile.frontend` - Frontend Dockerfile
- `docker-compose.yml` - Main compose file
- `docker-compose.prod.yml` - Production compose (optional)

**Technical Specs:**
```yaml
# docker-compose.yml excerpt - NO ML services
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
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
  
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.backend.deployment
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - MINIO_ENDPOINT=http://minio:9000
      - REDIS_URL=redis://redis:6379
    depends_on:
      - minio
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    # NO ML environment variables
    # NO GPU devices
  
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  # NO scheduler service (ML processing removed)
  # NO MLflow service
  # NO model serving service
```

---

### **D1: Infra & Secrets** ⏱️ 4-6 hours
**Owner:** 1 DevOps Engineer  
**Deliverables:**

#### Local Deployment
- [ ] Start MinIO, backend, frontend, redis (if using)
- [ ] **Verify NO ML dependencies** in running containers:
  - [ ] Check backend container has NO ML frameworks
  - [ ] Check image sizes < 600 MB
  - [ ] Verify CPU-only (no GPU required)
  - [ ] Run validation script: `scripts/validation/check_docker_image.py`
- [ ] Populate MinIO with sample data (from Data cluster)
- [ ] Test all services health checks
- [ ] Verify network connectivity between services
- [ ] **Test offline deployment** (disconnect from internet, verify all services work)

#### Secrets Management
- [ ] Add `.env.template` with required environment variables
- [ ] Document secrets handling (API keys, database URLs)
- [ ] Configure `.env` for local development
- [ ] Add `.gitignore` entries for sensitive files
- [ ] **NO ML-related environment variables** (no MLflow, no model paths)

**Acceptance Criteria:**
- ✅ All services start successfully
- ✅ Health checks pass
- ✅ NO ML dependencies in containers
- ✅ Offline deployment works
- ✅ Secrets configured

**Output Files:**
- `.env.template` - Environment variables template
- `.env` - Local environment variables (not committed)
- `docs/deploy/SECRETS.md` - Secrets handling documentation

---

### **D2: CI Pipeline + Automated Builds** ⏱️ 4-6 hours
**Owner:** 1 DevOps Engineer  
**Deliverables:**

#### CI/CD Setup
- [ ] Add GitHub Action to build and push images on main (optional if deploying locally)
- [ ] Configure automated tests in CI pipeline
- [ ] **Add ML dependency validation** to CI pipeline:
  - [ ] Run `scripts/validation/validate_deployment.py`
  - [ ] Fail build if ML dependencies detected
- [ ] Add build status badges
- [ ] Document deployment process

**Acceptance Criteria:**
- ✅ CI pipeline runs successfully
- ✅ ML dependency validation passes
- ✅ Build fails if ML dependencies detected
- ✅ Documentation complete

**Output Files:**
- `.github/workflows/build.yml` - CI pipeline
- `.github/workflows/validate-deployment.yml` - ML constraint validation
- `.github/workflows/deploy.yml` - Deployment pipeline (optional)
- `docs/deploy/DEPLOYMENT.md` - Deployment documentation

---

### **D3: Smoke Tests + Domain** ⏱️ 4-6 hours
**Owner:** 1 DevOps Engineer  
**Deliverables:**

#### Testing & Access
- [ ] Run end-to-end smoke tests for all endpoints and UI flows
- [ ] Test health checks for all services
- [ ] **Verify ML dependency validation** in health checks
- [ ] Verify data ingestion pipeline works (NO ML processing)
- [ ] If public access needed: Setup Cloudflare Tunnel or ngrok
- [ ] Configure domain (if available) or use tunnel URL

**Acceptance Criteria:**
- ✅ All smoke tests pass
- ✅ Health checks return ML compliance status
- ✅ Data pipeline works (precomputed only)
- ✅ Public access configured (if needed)

**Output Files:**
- `tests/e2e/smoke.test.sh` - Smoke test script
- `docs/deploy/ACCESS.md` - Access documentation

---

### **D4: Handover & Rollback Plan** ⏱️ 2-4 hours
**Owner:** 1 DevOps Engineer  
**Deliverables:**

#### Documentation & Operations
- [ ] Document how to roll back to previous compose state
- [ ] Create triage checklist for common failures
- [ ] Document monitoring and logging
- [ ] Create runbook for common operations
- [ ] **Document ML results update process:**
  - [ ] How to update precomputed ML results (Parquet files)
  - [ ] How to trigger data refresh endpoint
  - [ ] How ML environment outputs results to shared storage
- [ ] Stakeholder demo preparation

**Acceptance Criteria:**
- ✅ Documentation complete
- ✅ Runbook created
- ✅ Rollback procedure documented
- ✅ ML results update process documented

**Output Files:**
- `docs/deploy/ROLLBACK.md` - Rollback procedure
- `docs/deploy/TROUBLESHOOTING.md` - Troubleshooting guide
- `docs/deploy/RUNBOOK.md` - Operations runbook

---

## ✅ SUCCESS CRITERIA (ACCEPTANCE TESTS)

### Functional Requirements
- [ ] ✅ Stack boots with `docker-compose up --build` and runs all services
- [ ] ✅ Health check passes for backend, frontend returns index, MinIO contains sample `gold` data
- [ ] ✅ Stakeholder can open the dashboard and view data
- [ ] ✅ All API endpoints accessible and working
- [ ] ✅ Data ingestion pipeline runs successfully (NO ML processing)

### Performance Requirements
- [ ] ✅ Services start within 2 minutes
- [ ] ✅ Health checks return 200 OK
- [ ] ✅ No service crashes during smoke tests

### ML Ops Validation (MANDATORY)
- [ ] ✅ No ML dependencies in Dockerfiles
- [ ] ✅ Image sizes < 600 MB per container
- [ ] ✅ CPU-only deployment (no GPU required)
- [ ] ✅ Offline deployable (air-gapped environment)
- [ ] ✅ No ML services in docker-compose
- [ ] ✅ Health checks validate NO ML dependencies

### Security Requirements
- [ ] ✅ API keys stored in environment variables (not in code)
- [ ] ✅ Basic rate limits on API and auth for ingestion triggers
- [ ] ✅ TLS optional for local, required for public staging (if applicable)

---

## 🚨 SCOPE-REDUCTION OPTIONS (IF BLOCKERS)

### Option 1: Local Dev Runbook (No Docker)
**Trigger:** Docker Compose fails on host

**Changes:**
- Provide purely local dev runbook
- Run backend with `uvicorn` directly
- Run frontend with `npm run build` and `serve` static
- Manual service startup

**Impact:** ⚠️ Less reproducible, but functional for demo

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 2: No Public Access (Local Only)
**Trigger:** Domain/TLS blocks or tunnel setup fails

**Changes:**
- Deploy locally only
- Stakeholder access via VPN or screen share
- No public URL needed

**Impact:** ⚠️ Limited access, but functional for demo

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 3: Minimal Monitoring (Health Checks Only)
**Trigger:** Monitoring tools unavailable or time pressure

**Changes:**
- Health checks only (no full monitoring)
- Basic logging (stdout/stderr)
- Manual health check verification
- **NO ML monitoring** (no model metrics, no inference tracking)

**Impact:** ⚠️ Less visibility, but functional

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

## 🔗 KEY RECOMMENDATIONS

### Technical Decisions
1. **Docker Compose** - Fastest reproducible delivery
2. **Health Checks** - Essential for monitoring (includes ML validation)
3. **Environment Variables** - Secure secrets management
4. **Cloudflare Tunnel** - Quick secure public access (if needed)
5. **Validation Scripts** - Automated ML dependency checks

### Follow-Up Questions (Answer Quickly)
1. **Deployment:** Local Docker Compose OK, or need cloud VM?
2. **Public Access:** Need public URL, or local-only OK?
3. **Monitoring:** Health checks only OK, or need full monitoring?
4. **CI/CD:** Need automated builds, or manual deployment OK?
5. **ML Results Storage:** Where will precomputed ML results be stored? (shared path)

---

## 📚 REFERENCE LINKS

- [Data Cluster](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md) - MinIO/S3 setup
- [Backend Cluster](./02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - API deployment
- [Frontend Cluster](./03_FRONTEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - Frontend deployment
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy

---

## 📝 NEXT STEPS

1. **Assign Cluster Lead:** DevOps/Backend Lead
2. **Assign Team:** 1 Engineer
3. **Kickoff Meeting:** Review Dockerfiles, align with teams
4. **Daily Standup:** 9 AM - Review progress, blockers
5. **End of Day:** Acceptance test for each day's deliverables

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Execution-Ready - 4-Day Sprint Plan

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

