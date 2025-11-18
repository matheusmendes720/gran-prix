 <div align="center">

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                                           ║
║    ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗      ██████╗ ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗████████╗███████╗           ║
║    ████╗  ██║██╔═══██╗██║   ██║██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔════╝           ║
║    ██╔██╗ ██║██║   ██║██║   ██║███████║    ██║     ██║   ██║██████╔╝██████╔╝█████╗  ██╔██╗ ██║   ██║   █████╗             ║
║    ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║    ██║     ██║   ██║██╔══██╗██╔══██╗██╔══╝  ██║╚██╗██║   ██║   ██╔══╝             ║
║    ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║    ╚██████╗╚██████╔╝██║  ██║██║  ██║███████╗██║ ╚████║   ██║   ███████╗           ║
║    ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝           ║
║                                                                                                                           ║
║         Enterprise-Grade Demand Forecasting & Analytics Platform                                                          ║
║                    Production-Ready for Telecom Industry                                                                  ║ 
║                                                                                                                           ║
║                                                                                                                           ║ 
║                      ____                        ______  ______                                                           ║
║                     /\  _`\                     /\  _  \/\__  _\                                                          ║
║                     \ \ \L\ \_ __    __   __  __\ \ \L\ \/_/\ \/                                                          ║
║                      \ \ ,__/\`'__\/'__`\/\ \/\ \\ \  __ \ \ \ \                                                          ║
║                       \ \ \/\ \ \//\  __/\ \ \_/ |\ \ \/\ \ \_\ \__                                                       ║ 
║                        \ \_\ \ \_\\ \____\\ \___/  \ \_\ \_\/\_____\                                                      ║ 
║                         \/_/  \/_/ \/____/ \/__/    \/_/\/_/\/_____/                                                      ║ 
║                                                                                                                           ║ 
║                                                                                                                           ║ 
║                                                                                                                           ║
║                                                                                                                           ║
║                    🏆 GRAND PRIX 2025 - SENAI 🏆                                                                         ║
║                                                                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-success.svg)](CHANGELOG.md)
[![Production](https://img.shields.io/badge/deployment-production-green.svg)](docs/proj/roadmaps/prod/)
[![Enterprise](https://img.shields.io/badge/scale-enterprise-purple.svg)](CHANGELOG_PROD.md)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node.js-18%2B-green.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0%2B-blue.svg)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/next.js-14-black.svg)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-14%2B-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/redis-latest-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

[![Architecture](https://img.shields.io/badge/architecture-postgresql%20%2B%20offline--ml-lightgrey.svg)](docs/ARCHITECTURE_BIFURCATION_ANALYSIS.md)
[![ML](https://img.shields.io/badge/ML-offline--first-orange.svg)](docs/proj/roadmaps/prod/TECHNICAL_STACK_PROD.md)
[![Security](https://img.shields.io/badge/security-JWT%20%2B%20RBAC-yellow.svg)](backend/services/auth_service.py)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Production Architecture](#️-production-architecture)
- [🚀 Quick Start](#-quick-start)
- [📊 Project Structure](#-project-structure)
- [🔌 API Endpoints](#-api-endpoints)
- [🛠️ Technical Stack](#️-technical-stack)
- [📈 Performance &amp; Scalability](#-performance--scalability)
- [🔐 Security &amp; Compliance](#-security--compliance)
- [📚 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)

---

## 🎯 Overview

<div align="center">

**Enterprise-Grade Demand Forecasting & Analytics Platform**

🏭 **PRODUCTION-READY FOR GRAND PRIX 2025** 🏭

</div>

Nova Corrente is a **production-ready, enterprise-scale** analytics platform that combines **PostgreSQL**, **offline-first ML architecture**, and **real-time dashboards** to provide actionable insights for telecom supply chain management.

### 🎯 **Production Highlights**

- ✅ **PostgreSQL 14+** - Production-grade database with partitioning, JSONB, materialized views
- ✅ **Offline-First ML** - Precomputed results, no ML dependencies in deployment
- ✅ **Enterprise Security** - JWT authentication, RBAC, comprehensive audit logging
- ✅ **High Performance** - Redis caching, connection pooling, optimized queries
- ✅ **Scalable Architecture** - Multi-schema design, horizontal scaling ready
- ✅ **Production Deployment** - Docker Compose, health checks, monitoring ready

### 🚀 **Future Roadmap**

- 🔄 **AWS Cloud Infrastructure** - S3, RDS, ECS/EKS deployment
- 🔄 **Advanced Data Engineering** - Delta Lake, Spark, Databricks
- 🔄 **Orchestration** - Airflow DAGs for complex workflows
- 🔄 **Transformations** - dbt models for analytics engineering
- 🔄 **BI Tools** - Metabase/Superset integration

📖 **[Complete PROD Roadmap →](docs/proj/roadmaps/prod/README_PROD_ROADMAPS.md)**

---

## ✨ Key Features

### 📊 **Real-Time Analytics Dashboard**

- 🗺️ Interactive Brazil map (27 states)
- 📑 5-tab analytics interface
- 🎯 K-means clustering analysis
- 🤖 LLM-powered prescriptive recommendations
- 📐 Mathematical formula calculators

### 🤖 **Advanced ML/AI (Offline-First)**

- 🎯 Ensemble forecasting (ARIMA + Prophet + LSTM)
- ⚠️ Equipment failure prediction
- 📡 Tower performance clustering
- 📈 Regional demand forecasting
- 💰 Cost optimization recommendations
- 🔄 **Precomputed Results** - No ML processing in deployment

### 📈 **Business Intelligence**

- 📊 Real-time KPIs (Stockout Rate, MAPE, Savings)
- 🏢 Supplier performance tracking
- ⏱️ SLA penalty monitoring
- 📦 Regional inventory optimization
- 📋 Project status tracking

### 🔐 **Enterprise Features**

- 🔒 **JWT Authentication** - Secure token-based auth
- 👥 **Role-Based Access Control** - ADMIN, ANALYST, VIEWER roles
- 📝 **Audit Logging** - Comprehensive activity tracking
- ⚡ **Redis Caching** - High-performance caching layer
- 🐳 **Docker Deployment** - Production-ready containers
- 🔄 **Database Migrations** - Alembic for schema management

---

## 🏗️ Production Architecture

<div align="center">

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                             │
│  ERP | External APIs | Precomputed ML Results              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE (14+)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  core    │  │analytics │  │ support  │  │ staging  │  │
│  │ Business │  │ ML Output│  │ Auth/Audit│ │ ETL Stage│  │
│  │   Data   │  │          │  │          │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  • Partitioning  • Materialized Views  • JSONB Support    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              ML PROCESSING (Offline, Separate)              │
│  Prophet | ARIMA | LSTM | Ensemble                         │
│  Output: PostgreSQL Tables (via ETL)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              BACKEND API (Flask, Read-Only)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   REST   │  │   JWT    │  │  Redis   │  │  Health  │  │
│  │ Endpoints│  │   Auth   │  │  Cache   │  │  Checks  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  NO ML Dependencies | Production-Ready                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND DASHBOARD (Next.js 14)                │
│  TypeScript | Tailwind CSS | Recharts | D3.js             │
│  SSR/CSR Hybrid | Type-Safe | Production-Optimized         │
└─────────────────────────────────────────────────────────────┘
```

</div>

### 🔄 **Offline-First ML Architecture**

- ✅ **NO ML OPS IN DEPLOYMENT** - ML processing runs in separate environment
- ✅ **Precomputed Results** - Deployment only reads from PostgreSQL
- ✅ **Lightweight Containers** - No ML dependencies (PyTorch, TensorFlow, etc.)
- ✅ **Scalable** - Handles millions of records efficiently
- ✅ **Production-Grade** - Enterprise-ready architecture

📖 **[Complete Architecture Details →](docs/proj/diagrams/Project.md)**

---

## 🚀 Quick Start

### 📦 Prerequisites

```bash
✅ Python 3.8+
✅ Node.js 18+
✅ PostgreSQL 14+
✅ Redis (for caching)
✅ Docker & Docker Compose (recommended)
```

### 🏃 Production Setup

<details>
<summary><b>📥 1. Clone Repository</b></summary>

```bash
git clone <repository-url>
cd gran_prix
```

</details>

<details>
<summary><b>🐘 2. Setup PostgreSQL Database</b></summary>

```bash
# Using Docker
docker run --name postgres-nova-corrente \
  -e POSTGRES_USER=nova_corrente \
  -e POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD \
  -e POSTGRES_DB=nova_corrente \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:14

# Or use existing PostgreSQL instance
# Update backend/.env with connection details
```

</details>

<details>
<summary><b>🔴 3. Setup Redis Cache</b></summary>

```bash
# Using Docker
docker run -d -p 6379:6379 redis:alpine

# Or use existing Redis instance
# Update backend/.env with connection details
```

</details>

<details>
<summary><b>🐍 4. Backend Setup</b></summary>

```bash
cd backend

# Install dependencies (production, no ML)
pip install -r requirements_deployment.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL and Redis credentials

# Run database migrations
alembic upgrade head

# Start backend server
python run_server.py
# API available at http://localhost:5000
```

</details>

<details>
<summary><b>⚛️ 5. Frontend Setup</b></summary>

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with API URL

# Start development server
npm run dev
# Dashboard available at http://localhost:3000
```

</details>

<details>
<summary><b>🐳 6. Docker Compose (Recommended)</b></summary>

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

</details>

### 🌐 Access Application

```
📊 Main Dashboard: http://localhost:3000/main
🔍 Analytics: http://localhost:3000/features
📈 Forecasts: http://localhost:3000/forecasts
📦 Materials: http://localhost:3000/materials
💡 Recommendations: http://localhost:3000/recommendations
🔌 API Health: http://localhost:5000/health
```

📖 **[Complete Setup Guide →](docs/development/QUICK_START_BACKEND.md)**

---

## 📊 Project Structure

```
gran_prix/
├── 📄 README.md                    # This file
├── 📋 CHANGELOG.md                 # Main changelog
├── 📋 CHANGELOG_PROD.md            # PROD path changelog
│
├── 🐳 docker-compose.prod.yml      # Production Docker setup
├── 🐳 docker-compose.yml           # Development Docker setup
│
├── 📁 backend/                     # Backend API & Services
│   ├── app/                        # Flask application
│   │   ├── api/v1/routes/         # API endpoints
│   │   ├── core/                  # Core business logic
│   │   └── config.py              # Configuration
│   ├── alembic/                   # Database migrations
│   ├── config/                    # Configuration modules
│   ├── etl/                       # ETL scripts
│   │   ├── load_ml_outputs.py     # Load ML results to PostgreSQL
│   │   └── calculate_kpis.sql     # KPI calculations
│   ├── ml_pipeline/               # Offline ML processing
│   │   └── main.py                # ML pipeline entry point
│   ├── services/                  # Business services
│   │   ├── auth_service.py        # JWT authentication
│   │   ├── audit_service.py       # Audit logging
│   │   └── database_service.py    # Database operations
│   ├── db/                        # Database schemas
│   └── requirements_deployment.txt # Production dependencies
│
├── 📁 frontend/                    # Next.js Frontend
│   ├── src/
│   │   ├── app/                   # Next.js app router
│   │   │   ├── main/              # Main dashboard
│   │   │   ├── features/          # Analytics tabs
│   │   │   ├── forecasts/         # Forecasts page
│   │   │   └── materials/         # Materials pages
│   │   ├── components/            # React components
│   │   └── lib/                   # Utilities & API client
│   └── public/                    # Static assets
│
├── 📁 data/                        # Data Storage
│   ├── raw/                       # Raw datasets
│   ├── processed/                 # Processed data
│   └── gold/                      # Gold layer (Parquet)
│
├── 📁 docs/                        # Documentation
│   ├── proj/roadmaps/prod/        # PROD roadmaps
│   ├── development/               # Development guides
│   └── proj/diagrams/             # Architecture diagrams
│
└── 📁 scripts/                     # Utility scripts
```

📖 **[Complete Project Structure →](docs/proj/roadmaps/prod/README_PROD_ROADMAPS.md)**

---

## 🔌 API Endpoints

### 📊 Analytics & Data

```
GET  /api/v1/kpis                    # Real-time KPIs
GET  /api/v1/alerts                  # Inventory alerts
GET  /api/v1/forecasts               # Demand forecasts
GET  /api/v1/items                   # Material items
GET  /api/v1/materials               # Materials with details
GET  /api/v1/materials/{itemId}      # Material details
```

### 🎯 Clustering & Analysis

```
GET  /api/v1/clustering/equipment-failure    # Equipment failure clusters
GET  /api/v1/clustering/tower-performance    # Tower performance clusters
```

### 🤖 Prescriptive Analytics

```
GET  /api/v1/recommendations         # LLM-powered recommendations
```

### 🗺️ Geographic Data

```
GET  /api/v1/geographic/data         # Brazil regional data
```

### 📈 Model Performance

```
GET  /api/v1/models/performance      # ML model comparison
```

### 🔍 Health & Status

```
GET  /health                         # Health check
GET  /api/v1/health                  # Detailed health status
```

### 🔐 Authentication (Protected Endpoints)

```
POST /api/v1/auth/login              # User login
POST /api/v1/auth/logout             # User logout
GET  /api/v1/auth/me                 # Current user info
```

📚 **[Complete API Documentation →](docs/development/BACKEND_INTEGRATION_GUIDE.md)**

---

## 🛠️ Technical Stack

### 🔧 Backend (Production)

| Technology           | Purpose             | Version | Status |
| -------------------- | ------------------- | ------- | ------ |
| **Python**     | Core language       | 3.8+    | ✅     |
| **Flask**      | API framework       | 2.3+    | ✅     |
| **PostgreSQL** | Production database | 14+     | ✅     |
| **Redis**      | Caching layer       | Latest  | ✅     |
| **Alembic**    | Database migrations | Latest  | ✅     |
| **SQLAlchemy** | ORM                 | Latest  | ✅     |
| **JWT**        | Authentication      | Latest  | ✅     |
| **bcrypt**     | Password hashing    | Latest  | ✅     |

### ⚛️ Frontend (Production)

| Technology             | Purpose                 | Version | Status |
| ---------------------- | ----------------------- | ------- | ------ |
| **Next.js**      | React framework         | 14      | ✅     |
| **TypeScript**   | Type safety             | 5.0+    | ✅     |
| **Tailwind CSS** | Styling                 | Latest  | ✅     |
| **Recharts**     | Data visualization      | Latest  | ✅     |
| **D3.js**        | Advanced visualizations | Latest  | ✅     |
| **react-katex**  | LaTeX rendering         | Latest  | ✅     |

### 🤖 ML/AI (Offline Processing)

| Technology             | Purpose                 | Status |
| ---------------------- | ----------------------- | ------ |
| **Prophet**      | Time series forecasting | ✅     |
| **ARIMA**        | Statistical forecasting | ✅     |
| **LSTM**         | Deep learning           | ✅     |
| **scikit-learn** | Clustering & utilities  | ✅     |
| **Pandas**       | Data processing         | ✅     |
| **NumPy**        | Numerical computing     | ✅     |

### 🐳 Infrastructure

| Technology               | Purpose          | Status |
| ------------------------ | ---------------- | ------ |
| **Docker**         | Containerization | ✅     |
| **Docker Compose** | Orchestration    | ✅     |
| **PostgreSQL**     | Database server  | ✅     |
| **Redis**          | Cache server     | ✅     |

### 🔄 Future Stack (Planned)

| Technology           | Purpose                | Status |
| -------------------- | ---------------------- | ------ |
| **AWS S3**     | Object storage         | 🔄     |
| **Delta Lake** | Data lakehouse         | 🔄     |
| **Spark**      | Big data processing    | 🔄     |
| **Databricks** | ML platform            | 🔄     |
| **Airflow**    | Workflow orchestration | 🔄     |
| **dbt**        | Data transformations   | 🔄     |

📖 **[Complete Technical Stack →](docs/proj/roadmaps/prod/TECHNICAL_STACK_PROD.md)**

---

## 📈 Performance & Scalability

### ⚡ API Performance

| Endpoint     | Response Time | Cache TTL | Status |
| ------------ | ------------- | --------- | ------ |
| Health Check | <10ms         | N/A       | ✅     |
| KPIs         | <50ms         | 30s       | ✅     |
| Forecasts    | <200ms        | 1h        | ✅     |
| Clustering   | <500ms        | 5m        | ✅     |
| Prescriptive | <100ms        | 1h        | ✅     |

### 🎯 Database Performance

- ✅ **Partitioning** - Large fact tables partitioned by date
- ✅ **Materialized Views** - Precomputed analytics queries
- ✅ **Indexing** - Optimized indexes for common queries
- ✅ **Connection Pooling** - Efficient connection management
- ✅ **Query Optimization** - Tuned SQL queries

### 📊 Scalability

- ✅ **Horizontal Scaling** - Load balancer ready
- ✅ **Caching Strategy** - Redis for high-traffic endpoints
- ✅ **Database Scaling** - PostgreSQL read replicas ready
- ✅ **Container Orchestration** - Docker Compose → Kubernetes ready

### 🎯 Code Quality

```
✅ Zero TypeScript errors
✅ Zero linting issues
✅ 100% type safety
✅ Production-grade quality
✅ Comprehensive test coverage
✅ Security best practices
```

---

## 🔐 Security & Compliance

### 🔒 Authentication & Authorization

- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Role-Based Access Control** - ADMIN, ANALYST, VIEWER roles
- ✅ **Password Security** - bcrypt hashing with salt
- ✅ **Token Expiration** - Configurable token lifetimes
- ✅ **Secure Headers** - CORS, security headers configured

### 📝 Audit & Compliance

- ✅ **Comprehensive Audit Logging** - All API calls logged
- ✅ **User Activity Tracking** - Authentication events logged
- ✅ **Data Change Tracking** - Database changes audited
- ✅ **Compliance Ready** - GDPR, data privacy ready

### 🛡️ Security Features

- ✅ **Input Validation** - All inputs validated and sanitized
- ✅ **SQL Injection Protection** - Parameterized queries
- ✅ **XSS Protection** - Content Security Policy
- ✅ **Environment Variables** - Secrets management
- ✅ **HTTPS Ready** - SSL/TLS configuration ready

---

## 📚 Documentation

### 🗺️ **Master Navigation**

- **[📚 Complete Navigation Index](docs/NAVIGATION_INDEX.md)** - **START HERE** - Master index of all documentation, roadmaps, and changelogs

### 📖 Main Documentation

- **[📋 Changelog](CHANGELOG.md)** - Complete version history
- **[🏭 PROD Path Changelog](CHANGELOG_PROD.md)** - Production path history
- **[🗺️ PROD Roadmaps](docs/proj/roadmaps/prod/README_PROD_ROADMAPS.md)** - Production roadmaps
- **[🏗️ Architecture](docs/proj/diagrams/Project.md)** - Complete architecture specification

### 🚀 Quick Start Guides

- **[⚡ Quick Start](docs/development/QUICK_START_BACKEND.md)** - Backend setup guide
- **[🔧 Backend Integration](docs/development/BACKEND_INTEGRATION_GUIDE.md)** - API integration
- **[🎨 Frontend Setup](frontend/README.md)** - Frontend development
- **[🐳 Deployment](docs/development/DEPLOYMENT.md)** - Production deployment

### 📊 Technical Documentation

- **[📐 Technical Stack](docs/proj/roadmaps/prod/TECHNICAL_STACK_PROD.md)** - Complete stack details
- **[📈 Implementation Checklist](docs/development/IMPLEMENTATION_CHECKLIST.md)** - Implementation guide
- **[🔄 Migration Guide](docs/MIGRATION_DEMO_TO_PROD.md)** - Upgrade from DEMO

### 🔄 Future Roadmap

- **[☁️ Cloud Infrastructure](docs/proj/roadmaps/prod/PRODUCTION_DEPLOYMENT_GUIDE_PT_BR.md)** - AWS deployment
- **[📊 Data Engineering](docs/proj/roadmaps/prod/DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md)** - Advanced pipelines
- **[🔄 Orchestration](docs/proj/roadmaps/prod/ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md)** - Airflow & dbt

---

## 🤝 Contributing

This project is developed for **Grand Prix 2025** by the Nova Corrente team at SENAI.

### 📝 Contribution Guidelines

1. Follow the production architecture patterns
2. Maintain code quality standards (TypeScript, linting)
3. Update documentation for all changes
4. Write tests for new features
5. Follow the offline-first ML architecture
6. Ensure security best practices

### 🔄 Development Workflow

1. Create feature branch from `master`
2. Implement changes with tests
3. Update documentation
4. Submit pull request
5. Code review and approval
6. Merge to `master`

---

<div align="center">

### ⭐ Star this repository if you find it useful! ⭐

**Status:** ✅ **PRODUCTION READY**
**Last Updated:** November 2025
**Version:** 4.0.0 (PROD)

---

*Built with ❤️ for Nova Corrente Telecom - Enterprise Production Platform*

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                                                                           ║
║                    🏆 GRAND PRIX 2025 - SENAI 🏆                         ║
║                  🏭 PRODUCTION-READY ENTERPRISE PLATFORM 🏭              ║
║                                                                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

</div>
