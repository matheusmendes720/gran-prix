<div align="center">

```
╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║                                                                             ║
║                ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗                          ║
║                ████╗  ██║██╔═══██╗██║   ██║██╔══██╗                         ║
║                ██╔██╗ ██║██║   ██║██║   ██║███████║                         ║
║                ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║                         ║
║                ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║                         ║
║                ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝                         ║
║                                                                             ║
║   ██████╗ ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗████████╗███████╗       ║
║  ██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔════╝       ║
║  ██║     ██║   ██║██████╔╝██████╔╝█████╗  ██╔██╗ ██║   ██║   █████╗         ║
║  ██║     ██║   ██║██╔══██╗██╔══██╗██╔══╝  ██║╚██╗██║   ██║   ██╔══╝         ║
║  ╚██████╗╚██████╔╝██║  ██║██║  ██║███████╗██║ ╚████║   ██║   ███████╗       ║
║   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝       ║
║                                                                             ║
║                                                                             ║
║    Plataforma Empresarial de Previsão de Demanda e Analytics                ║
║              Pronta para Produção - Indústria de Telecom                    ║
║              ____                        ______  ______                     ║
║             /\  _`\                     /\  _  \/\__  _\                    ║
║             \ \ \L\ \_ __    __   __  __\ \ \L\ \/_/\ \/                    ║
║              \ \ ,__/\`'__\/'__`\/\ \/\ \\ \  __ \ \ \ \                    ║
║               \ \ \/\ \ \//\  __/\ \ \_/ |\ \ \/\ \ \_\ \__                 ║
║                \ \_\ \ \_\\ \____\\ \___/  \ \_\ \_\/\_____\                ║
║                 \/_/  \/_/ \/____/ \/__/    \/_/\/_/\/_____/                ║ 
║                                                                             ║ 
║                                                                             ║ 
║                                                                             ║
║                                                                             ║
║                    🏆 GRAND PRIX 2025 - SENAI 🏆                           ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
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

## 📋 Índice

- [🎯 Visão Geral](#-visão-geral)
- [✨ Principais Funcionalidades](#-principais-funcionalidades)
- [🏗️ Arquitetura de Produção](#️-arquitetura-de-produção)
- [🚀 Início Rápido](#-início-rápido)
- [📊 Estrutura do Projeto](#-estrutura-do-projeto)
- [🔌 Endpoints da API](#-endpoints-da-api)
- [🛠️ Stack Técnico](#️-stack-técnico)
- [📈 Performance e Escalabilidade](#-performance-e-escalabilidade)
- [🔐 Segurança e Conformidade](#-segurança-e-conformidade)
- [📚 Documentação](#-documentação)
- [🤝 Contribuindo](#-contribuindo)

---

## 🎯 Visão Geral

<div align="center">

**Plataforma Empresarial de Previsão de Demanda e Analytics**

🏭 **PRONTO PARA PRODUÇÃO - GRAND PRIX 2025** 🏭

</div>

Nova Corrente é uma plataforma de analytics **pronta para produção, em escala empresarial** que combina **PostgreSQL**, **arquitetura ML offline-first**, e **dashboards em tempo real** para fornecer insights acionáveis para gestão da cadeia de suprimentos de telecomunicações.

### 🎯 **Destaques de Produção**

- ✅ **PostgreSQL 14+** - Banco de dados de nível empresarial com particionamento, JSONB, views materializadas
- ✅ **ML Offline-First** - Resultados pré-computados, sem dependências de ML no deployment
- ✅ **Segurança Empresarial** - Autenticação JWT, RBAC, auditoria abrangente
- ✅ **Alta Performance** - Cache Redis, pool de conexões, consultas otimizadas
- ✅ **Arquitetura Escalável** - Design multi-schema, pronto para escalonamento horizontal
- ✅ **Deployment de Produção** - Docker Compose, health checks, monitoramento pronto

### 🚀 **Roadmap Futuro**

- 🔄 **Infraestrutura Cloud AWS** - Deploy S3, RDS, ECS/EKS
- 🔄 **Engenharia de Dados Avançada** - Delta Lake, Spark, Databricks
- 🔄 **Orquestração** - DAGs Airflow para workflows complexos
- 🔄 **Transformações** - Modelos dbt para engenharia de analytics
- 🔄 **Ferramentas BI** - Integração Metabase/Superset

📖 **[Roadmap PROD Completo →](docs/proj/roadmaps/prod/README_PROD_ROADMAPS.md)**

---

## ✨ Principais Funcionalidades

### 📊 **Dashboard de Analytics em Tempo Real**

- 🗺️ Mapa interativo do Brasil (27 estados)
- 📑 Interface de analytics com 5 abas
- 🎯 Análise de clustering K-means
- 🤖 Recomendações prescritivas com LLM
- 📐 Calculadoras de fórmulas matemáticas

### 🤖 **ML/AI Avançado (Offline-First)**

- 🎯 Previsão por ensemble (ARIMA + Prophet + LSTM)
- ⚠️ Predição de falhas de equipamentos
- 📡 Clustering de performance de torres
- 📈 Previsão de demanda regional
- 💰 Recomendações de otimização de custos
- 🔄 **Resultados Pré-computados** - Sem processamento ML no deployment

### 📈 **Business Intelligence**

- 📊 KPIs em tempo real (Taxa de Ruptura, MAPE, Economias)
- 🏢 Acompanhamento de performance de fornecedores
- ⏱️ Monitoramento de penalidades SLA
- 📦 Otimização de inventário regional
- 📋 Acompanhamento de status de projetos

### 🔐 **Funcionalidades Empresariais**

- 🔒 **Autenticação JWT** - Autenticação segura baseada em tokens
- 👥 **Controle de Acesso Baseado em Funções** - Funções ADMIN, ANALYST, VIEWER
- 📝 **Auditoria** - Rastreamento abrangente de atividades
- ⚡ **Cache Redis** - Camada de cache de alta performance
- 🐳 **Deployment Docker** - Containers prontos para produção
- 🔄 **Migrações de Banco de Dados** - Alembic para gerenciamento de schema

---

## 🏗️ Arquitetura de Produção

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

### 🔄 **Arquitetura ML Offline-First**

- ✅ **SEM ML OPS NO DEPLOYMENT** - Processamento ML roda em ambiente separado
- ✅ **Resultados Pré-computados** - Deployment apenas lê do PostgreSQL
- ✅ **Containers Leves** - Sem dependências de ML (PyTorch, TensorFlow, etc.)
- ✅ **Escalável** - Processa milhões de registros eficientemente
- ✅ **Nível Empresarial** - Arquitetura pronta para produção

📖 **[Detalhes Completos da Arquitetura →](docs/proj/diagrams/Project.md)**

---

## 🚀 Início Rápido

### 📦 Pré-requisitos

```bash
✅ Python 3.8+
✅ Node.js 18+
✅ PostgreSQL 14+
✅ Redis (para cache)
✅ Docker & Docker Compose (recomendado)
```

### 🏃 Configuração de Produção

<details>
<summary><b>📥 1. Clonar Repositório</b></summary>

```bash
git clone <repository-url>
cd gran_prix
```

</details>

<details>
<summary><b>🐘 2. Configurar Banco de Dados PostgreSQL</b></summary>

```bash
# Usando Docker
docker run --name postgres-nova-corrente \
  -e POSTGRES_USER=nova_corrente \
  -e POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD \
  -e POSTGRES_DB=nova_corrente \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:14

# Ou use uma instância PostgreSQL existente
# Atualize backend/.env com os detalhes de conexão
```

</details>

<details>
<summary><b>🔴 3. Configurar Cache Redis</b></summary>

```bash
# Usando Docker
docker run -d -p 6379:6379 redis:alpine

# Ou use uma instância Redis existente
# Atualize backend/.env com os detalhes de conexão
```

</details>

<details>
<summary><b>🐍 4. Configurar Backend</b></summary>

```bash
cd backend

# Instalar dependências (produção, sem ML)
pip install -r requirements_deployment.txt

# Configurar ambiente
cp .env.example .env
# Edite .env com suas credenciais PostgreSQL e Redis

# Executar migrações do banco de dados
alembic upgrade head

# Iniciar servidor backend
python run_server.py
# API disponível em http://localhost:5000
```

</details>

<details>
<summary><b>⚛️ 5. Configurar Frontend</b></summary>

```bash
cd frontend

# Instalar dependências
npm install

# Configurar ambiente
cp .env.local.example .env.local
# Edite .env.local com a URL da API

# Iniciar servidor de desenvolvimento
npm run dev
# Dashboard disponível em http://localhost:3000
```

</details>

<details>
<summary><b>🐳 6. Docker Compose (Recomendado)</b></summary>

```bash
# Deploy de produção
docker-compose -f docker-compose.prod.yml up -d

# Verificar status
docker-compose -f docker-compose.prod.yml ps

# Visualizar logs
docker-compose -f docker-compose.prod.yml logs -f
```

</details>

### 🌐 Acessar Aplicação

```
📊 Dashboard Principal: http://localhost:3000/main
🔍 Analytics: http://localhost:3000/features
📈 Previsões: http://localhost:3000/forecasts
📦 Materiais: http://localhost:3000/materials
💡 Recomendações: http://localhost:3000/recommendations
🔌 Health da API: http://localhost:5000/health
```

📖 **[Guia Completo de Configuração →](docs/development/QUICK_START_BACKEND.md)**

---

## 📊 Estrutura do Projeto

```
gran_prix/
├── 📄 README.md                    # Este arquivo
├── 📋 CHANGELOG.md                 # Changelog principal
├── 📋 CHANGELOG_PROD.md            # Changelog do caminho PROD
│
├── 🐳 docker-compose.prod.yml      # Configuração Docker de produção
├── 🐳 docker-compose.yml           # Configuração Docker de desenvolvimento
│
├── 📁 backend/                     # API Backend e Serviços
│   ├── app/                        # Aplicação Flask
│   │   ├── api/v1/routes/         # Endpoints da API
│   │   ├── core/                  # Lógica de negócio principal
│   │   └── config.py              # Configuração
│   ├── alembic/                   # Migrações do banco de dados
│   ├── config/                    # Módulos de configuração
│   ├── etl/                       # Scripts ETL
│   │   ├── load_ml_outputs.py     # Carregar resultados ML para PostgreSQL
│   │   └── calculate_kpis.sql     # Cálculos de KPIs
│   ├── ml_pipeline/               # Processamento ML offline
│   │   └── main.py                # Ponto de entrada do pipeline ML
│   ├── services/                  # Serviços de negócio
│   │   ├── auth_service.py        # Autenticação JWT
│   │   ├── audit_service.py       # Logging de auditoria
│   │   └── database_service.py    # Operações de banco de dados
│   ├── db/                        # Schemas do banco de dados
│   └── requirements_deployment.txt # Dependências de produção
│
├── 📁 frontend/                    # Frontend Next.js
│   ├── src/
│   │   ├── app/                   # Next.js app router
│   │   │   ├── main/              # Dashboard principal
│   │   │   ├── features/          # Abas de analytics
│   │   │   ├── forecasts/         # Página de previsões
│   │   │   └── materials/         # Páginas de materiais
│   │   ├── components/            # Componentes React
│   │   └── lib/                   # Utilitários e cliente API
│   └── public/                    # Assets estáticos
│
├── 📁 data/                        # Armazenamento de Dados
│   ├── raw/                       # Datasets brutos
│   ├── processed/                 # Dados processados
│   └── gold/                      # Camada gold (Parquet)
│
├── 📁 docs/                        # Documentação
│   ├── proj/roadmaps/prod/        # Roadmaps PROD
│   ├── development/               # Guias de desenvolvimento
│   └── proj/diagrams/             # Diagramas de arquitetura
│
└── 📁 scripts/                     # Scripts utilitários
```

📖 **[Estrutura Completa do Projeto →](docs/proj/roadmaps/prod/README_PROD_ROADMAPS.md)**

---

## 🔌 Endpoints da API

### 📊 Analytics e Dados

```
GET  /api/v1/kpis                    # KPIs em tempo real
GET  /api/v1/alerts                  # Alertas de inventário
GET  /api/v1/forecasts               # Previsões de demanda
GET  /api/v1/items                   # Itens de material
GET  /api/v1/materials               # Materiais com detalhes
GET  /api/v1/materials/{itemId}      # Detalhes do material
```

### 🎯 Clustering e Análise

```
GET  /api/v1/clustering/equipment-failure    # Clusters de falhas de equipamentos
GET  /api/v1/clustering/tower-performance    # Clusters de performance de torres
```

### 🤖 Analytics Prescritivo

```
GET  /api/v1/recommendations         # Recomendações com LLM
```

### 🗺️ Dados Geográficos

```
GET  /api/v1/geographic/data         # Dados regionais do Brasil
```

### 📈 Performance do Modelo

```
GET  /api/v1/models/performance      # Comparação de modelos ML
```

### 🔍 Health e Status

```
GET  /health                         # Health check
GET  /api/v1/health                  # Status de health detalhado
```

### 🔐 Autenticação (Endpoints Protegidos)

```
POST /api/v1/auth/login              # Login de usuário
POST /api/v1/auth/logout             # Logout de usuário
GET  /api/v1/auth/me                 # Informações do usuário atual
```

📚 **[Documentação Completa da API →](docs/development/BACKEND_INTEGRATION_GUIDE.md)**

---

## 🛠️ Stack Técnico

### 🔧 Backend (Produção)

| Tecnologia           | Propósito                   | Versão | Status |
| -------------------- | ---------------------------- | ------- | ------ |
| **Python**     | Linguagem principal          | 3.8+    | ✅     |
| **Flask**      | Framework de API             | 2.3+    | ✅     |
| **PostgreSQL** | Banco de dados de produção | 14+     | ✅     |
| **Redis**      | Camada de cache              | Latest  | ✅     |
| **Alembic**    | Migrações de banco         | Latest  | ✅     |
| **SQLAlchemy** | ORM                          | Latest  | ✅     |
| **JWT**        | Autenticação               | Latest  | ✅     |
| **bcrypt**     | Hash de senhas               | Latest  | ✅     |

### ⚛️ Frontend (Produção)

| Tecnologia             | Propósito                 | Versão | Status |
| ---------------------- | -------------------------- | ------- | ------ |
| **Next.js**      | Framework React            | 14      | ✅     |
| **TypeScript**   | Segurança de tipos        | 5.0+    | ✅     |
| **Tailwind CSS** | Estilização              | Latest  | ✅     |
| **Recharts**     | Visualização de dados    | Latest  | ✅     |
| **D3.js**        | Visualizações avançadas | Latest  | ✅     |
| **react-katex**  | Renderização LaTeX       | Latest  | ✅     |

### 🤖 ML/AI (Processamento Offline)

| Tecnologia             | Propósito                     | Status |
| ---------------------- | ------------------------------ | ------ |
| **Prophet**      | Previsão de séries temporais | ✅     |
| **ARIMA**        | Previsão estatística         | ✅     |
| **LSTM**         | Deep learning                  | ✅     |
| **scikit-learn** | Clustering e utilitários      | ✅     |
| **Pandas**       | Processamento de dados         | ✅     |
| **NumPy**        | Computação numérica         | ✅     |

### 🐳 Infraestrutura

| Tecnologia               | Propósito        | Status |
| ------------------------ | ----------------- | ------ |
| **Docker**         | Containerização | ✅     |
| **Docker Compose** | Orquestração    | ✅     |
| **PostgreSQL**     | Servidor de banco | ✅     |
| **Redis**          | Servidor de cache | ✅     |

### 🔄 Stack Futuro (Planejado)

| Tecnologia           | Propósito                  | Status |
| -------------------- | --------------------------- | ------ |
| **AWS S3**     | Armazenamento de objetos    | 🔄     |
| **Delta Lake** | Data lakehouse              | 🔄     |
| **Spark**      | Processamento de big data   | 🔄     |
| **Databricks** | Plataforma ML               | 🔄     |
| **Airflow**    | Orquestração de workflows | 🔄     |
| **dbt**        | Transformações de dados   | 🔄     |

📖 **[Stack Técnico Completo →](docs/proj/roadmaps/prod/TECHNICAL_STACK_PROD.md)**

---

## 📈 Performance e Escalabilidade

### ⚡ Performance da API

| Endpoint     | Tempo de Resposta | Cache TTL | Status |
| ------------ | ----------------- | --------- | ------ |
| Health Check | <10ms             | N/A       | ✅     |
| KPIs         | <50ms             | 30s       | ✅     |
| Previsões   | <200ms            | 1h        | ✅     |
| Clustering   | <500ms            | 5m        | ✅     |
| Prescritivo  | <100ms            | 1h        | ✅     |

### 🎯 Performance do Banco de Dados

- ✅ **Particionamento** - Tabelas de fatos grandes particionadas por data
- ✅ **Views Materializadas** - Consultas de analytics pré-computadas
- ✅ **Indexação** - Índices otimizados para consultas comuns
- ✅ **Pool de Conexões** - Gerenciamento eficiente de conexões
- ✅ **Otimização de Consultas** - Consultas SQL ajustadas

### 📊 Escalabilidade

- ✅ **Escalonamento Horizontal** - Pronto para load balancer
- ✅ **Estratégia de Cache** - Redis para endpoints de alto tráfego
- ✅ **Escalonamento de Banco** - Réplicas de leitura PostgreSQL prontas
- ✅ **Orquestração de Containers** - Docker Compose → Kubernetes pronto

### 🎯 Qualidade do Código

```
✅ Zero erros TypeScript
✅ Zero problemas de linting
✅ 100% segurança de tipos
✅ Qualidade de nível de produção
✅ Cobertura de testes abrangente
✅ Melhores práticas de segurança
```

---

## 🔐 Segurança e Conformidade

### 🔒 Autenticação e Autorização

- ✅ **Autenticação JWT** - Autenticação segura baseada em tokens
- ✅ **Controle de Acesso Baseado em Funções** - Funções ADMIN, ANALYST, VIEWER
- ✅ **Segurança de Senhas** - Hash bcrypt com salt
- ✅ **Expiração de Tokens** - Tempos de vida de tokens configuráveis
- ✅ **Headers Seguros** - CORS, headers de segurança configurados

### 📝 Auditoria e Conformidade

- ✅ **Auditoria Abrangente** - Todas as chamadas de API registradas
- ✅ **Rastreamento de Atividades do Usuário** - Eventos de autenticação registrados
- ✅ **Rastreamento de Mudanças de Dados** - Mudanças no banco auditadas
- ✅ **Pronto para Conformidade** - GDPR, privacidade de dados pronta

### 🛡️ Funcionalidades de Segurança

- ✅ **Validação de Entrada** - Todas as entradas validadas e sanitizadas
- ✅ **Proteção contra SQL Injection** - Consultas parametrizadas
- ✅ **Proteção XSS** - Content Security Policy
- ✅ **Variáveis de Ambiente** - Gerenciamento de segredos
- ✅ **HTTPS Pronto** - Configuração SSL/TLS pronta

---

## 📚 Documentação

### 🗺️ **Navegação Principal**

- **[📚 Índice Completo de Navegação](docs/NAVIGATION_INDEX.md)** - **COMECE AQUI** - Índice principal de toda documentação, roadmaps e changelogs

### 📖 Documentação Principal

- **[📋 Changelog](CHANGELOG.md)** - Histórico completo de versões
- **[🏭 Changelog do Caminho PROD](CHANGELOG_PROD.md)** - Histórico do caminho de produção
- **[🗺️ Roadmaps PROD](docs/proj/roadmaps/prod/README_PROD_ROADMAPS.md)** - Roadmaps de produção
- **[🏗️ Arquitetura](docs/proj/diagrams/Project.md)** - Especificação completa da arquitetura

### 🚀 Guias de Início Rápido

- **[⚡ Início Rápido](docs/development/QUICK_START_BACKEND.md)** - Guia de configuração do backend
- **[🔧 Integração Backend](docs/development/BACKEND_INTEGRATION_GUIDE.md)** - Integração da API
- **[🎨 Configuração Frontend](frontend/README.md)** - Desenvolvimento frontend
- **[🐳 Deployment](docs/development/DEPLOYMENT.md)** - Deployment de produção

### 📊 Documentação Técnica

- **[📐 Stack Técnico](docs/proj/roadmaps/prod/TECHNICAL_STACK_PROD.md)** - Detalhes completos do stack
- **[📈 Checklist de Implementação](docs/development/IMPLEMENTATION_CHECKLIST.md)** - Guia de implementação
- **[🔄 Guia de Migração](docs/MIGRATION_DEMO_TO_PROD.md)** - Upgrade do DEMO

### 🔄 Roadmap Futuro

- **[☁️ Infraestrutura Cloud](docs/proj/roadmaps/prod/PRODUCTION_DEPLOYMENT_GUIDE_PT_BR.md)** - Deploy AWS
- **[📊 Engenharia de Dados](docs/proj/roadmaps/prod/DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md)** - Pipelines avançados
- **[🔄 Orquestração](docs/proj/roadmaps/prod/ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md)** - Airflow & dbt

---

## 🤝 Contribuindo

Este projeto é desenvolvido para o **Grand Prix 2025** pela equipe Nova Corrente no SENAI.

### 📝 Diretrizes de Contribuição

1. Seguir os padrões de arquitetura de produção
2. Manter padrões de qualidade de código (TypeScript, linting)
3. Atualizar documentação para todas as mudanças
4. Escrever testes para novas funcionalidades
5. Seguir a arquitetura ML offline-first
6. Garantir melhores práticas de segurança

### 🔄 Fluxo de Desenvolvimento

1. Criar branch de feature a partir de `master`
2. Implementar mudanças com testes
3. Atualizar documentação
4. Enviar pull request
5. Revisão de código e aprovação
6. Merge para `master`

---

<div align="center">

### ⭐ Dê uma estrela neste repositório se você achar útil! ⭐

**Status:** ✅ **PRONTO PARA PRODUÇÃO**
**Última Atualização:** Novembro 2025
**Versão:** 4.0.0 (PROD)

---

*Construído com ❤️ para Nova Corrente Telecom - Plataforma Empresarial de Produção*

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                                                                           ║
║                    🏆 GRAND PRIX 2025 - SENAI 🏆                         ║
║                  🏭 PRODUCTION-READY ENTERPRISE PLATFORM 🏭              ║
║                                                                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

</div>
