# ✅ VALIDATION GUIDE
## Nova Corrente - ML Ops Constraint Validation

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Validation Guide

---

## 📋 OVERVIEW

This guide explains how to use the validation scripts to ensure deployment compliance with the **NO ML OPS LOGIC IN DEPLOYMENT** constraint.

---

## 🔧 VALIDATION SCRIPTS

### 1. Master Validation Script
**File:** `scripts/validation/validate_deployment.py`

**Description:** Runs all validation scripts and generates comprehensive report.

**Usage:**
```bash
python scripts/validation/validate_deployment.py
```

**Output:**
- ✅ All validations passed → Exit code 0
- ❌ Validation failed → Exit code 1 (with details)

---

### 2. ML Dependencies Check
**File:** `scripts/validation/check_ml_dependencies.py`

**Description:** Checks requirements files and Dockerfiles for ML dependencies.

**Usage:**
```bash
python scripts/validation/check_ml_dependencies.py
```

**Checks:**
- `backend/requirements_deployment.txt` (NO ML dependencies)
- `infrastructure/docker/Dockerfile.backend.deployment` (NO ML dependencies)

**ML Packages Detected:**
- torch, tensorflow, sklearn, mlflow, xgboost, lightgbm, prophet, pmdarima

---

### 3. ML Endpoints Check
**File:** `scripts/validation/check_ml_endpoints.py`

**Description:** Checks API routes for ML endpoints (inference, training, etc.).

**Usage:**
```bash
python scripts/validation/check_ml_endpoints.py
```

**Checks:**
- `backend/api/*.py`
- `backend/routes/*.py`
- `backend/app/routes/*.py`

**ML Endpoints Detected:**
- /predict, /forecast, /inference, /train, /retrain, /optimize, /model, /mlflow

---

### 4. ML Imports Check
**File:** `scripts/validation/check_ml_imports.py`

**Description:** Checks deployment code for ML imports.

**Usage:**
```bash
python scripts/validation/check_ml_imports.py
```

**Checks:**
- `backend/api/*.py`
- `backend/services/*.py`
- `backend/app/*.py`

**Excludes:**
- `backend/ml/` (ML code only)
- `backend/scripts/train_*.py` (ML code only)

**ML Imports Detected:**
- import torch, import tensorflow, import sklearn, import mlflow, etc.

---

### 5. Docker Image Check
**File:** `scripts/validation/check_docker_image.py`

**Description:** Validates Docker image has no ML dependencies.

**Usage:**
```bash
python scripts/validation/check_docker_image.py
```

**Checks:**
- Builds Docker image
- Checks installed packages (pip list)
- Validates image size < 600 MB

**Requirements:**
- Docker must be installed and running

---

## 🚀 CI/CD INTEGRATION

### GitHub Actions
Validation runs automatically on:
- Push to `main` or `develop`
- Pull requests
- Manual workflow dispatch

**Workflow:** `.github/workflows/validate-deployment.yml`

### Pre-Commit Hooks
Validation runs before commits (if configured):

**File:** `.pre-commit-config.yaml`

**Installation:**
```bash
pip install pre-commit
pre-commit install
```

---

## 📊 VALIDATION RESULTS

### Success Example
```
✅ VALIDATION PASSED
   Checked 4 deployment file(s)
   No ML dependencies found in deployment files
```

### Failure Example
```
❌ VALIDATION FAILED
   Found 2 ML dependency violation(s) in deployment files

Violations:
  - backend/requirements_deployment.txt:15: scikit-learn>=1.3.0
  - infrastructure/docker/Dockerfile.backend.deployment:20: pip install scikit-learn

Action required:
  1. Remove ML dependencies from deployment files
  2. Use requirements_deployment.txt for deployment (NO ML)
  3. Use requirements_ml.txt for ML processing (separate environment)
```

---

## 🔧 FIXING VIOLATIONS

### Fix ML Dependencies
1. Remove ML packages from `requirements_deployment.txt`
2. Use `requirements_ml.txt` for ML processing (separate environment)
3. Re-run validation

### Fix ML Endpoints
1. Remove ML endpoints from API routes
2. Only keep read operations for precomputed data
3. Re-run validation

### Fix ML Imports
1. Remove ML imports from deployment code
2. Move ML code to `backend/ml/` or `backend/scripts/train_*.py`
3. Re-run validation

---

## 📚 REFERENCE LINKS

- [Global Constraints](../diagnostics/clusters/GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)
- [Deployment Runbook](../deploy/DEPLOYMENT_RUNBOOK.md)

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Validation Guide

