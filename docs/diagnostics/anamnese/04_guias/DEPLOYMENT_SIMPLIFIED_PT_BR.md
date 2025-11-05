# 🚀 DEPLOYMENT SIMPLIFICADO
## Nova Corrente - Deployment sem ML e sem APIs Externas

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Guia Completo - Deployment Simplificado  
**Objetivo:** Documentar deployment simplificado sem ML dependencies e sem APIs externas em tempo real

---

## 📋 ÍNDICE

1. [Visão Geral](#visao-geral)
2. [Pré-requisitos](#pre-requisitos)
3. [Preparação](#preparacao)
4. [Deployment com Docker Compose](#docker-compose)
5. [Deployment Manual](#manual)
6. [Verificação](#verificacao)
7. [Troubleshooting](#troubleshooting)

---

<a name="visao-geral"></a>

## 1. 📖 VISÃO GERAL

### 1.1 Arquitetura Simplificada

**Componentes do Deployment:**
- ✅ MinIO (Object Storage)
- ✅ Redis (Caching)
- ✅ Backend FastAPI (Read-only, sem ML, sem APIs externas)
- ✅ Frontend React/Next.js (Dashboard)

**Componentes Removidos:**
- ❌ ML Services (rodam localmente)
- ❌ APIs Externas em tempo real (dados pré-coletados)
- ❌ Collectors de APIs externas
- ❌ ETL pipelines de APIs externas

---

### 1.2 Fluxo de Dados Simplificado

```
1. ML Processing (Local - Separado)
   └── Gera resultados pré-computados
   
2. Storage (MinIO ou Local)
   └── Armazena resultados pré-computados
   
3. Deployment (Produção)
   ├── Backend FastAPI (Read-only)
   │   ├── Lê resultados pré-computados
   │   ├── Retorna dados para frontend
   │   └── Sistema de recomendações
   └── Frontend React
       ├── Dashboard analítico
       ├── Visualização de dados
       └── Sistema de notificações
```

---

<a name="pre-requisitos"></a>

## 2. ✅ PRÉ-REQUISITOS

### 2.1 Software Necessário

- ✅ Docker 20.10+
- ✅ Docker Compose 2.0+
- ✅ Git (para clonar repositório)
- ✅ 4GB RAM mínimo
- ✅ 10GB espaço em disco

### 2.2 Dados Pré-Computados

**Requisitos:**
- ✅ Resultados ML pré-computados em Parquet
- ✅ Dados históricos processados
- ✅ Metadata incluída

**Estrutura:**
```
data/ml_results/
├── forecasts/*.parquet
├── recommendations/*.parquet
├── metrics/*.parquet
└── metadata/*.json
```

---

<a name="preparacao"></a>

## 3. 🔧 PREPARAÇÃO

### 3.1 Verificar Dados Pré-Computados

**Ação:**
```bash
# 1. Verificar que resultados ML existem
ls data/ml_results/

# 2. Verificar metadata
cat data/ml_results/metadata/last_updated.json

# 3. Verificar formato Parquet
python -c "import pandas as pd; df = pd.read_parquet('data/ml_results/forecasts/*.parquet'); print(df.head())"
```

---

### 3.2 Configurar Variáveis de Ambiente

**Arquivo:** `.env` (criar ou editar)

**Conteúdo:**
```bash
# Deployment Environment
ENABLE_EXTERNAL_APIS=false
ENABLE_ML_PROCESSING=false
ML_RESULTS_PATH=./data/ml_results
DATA_DIR=./data
LOG_DIR=./logs

# MinIO Configuration
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Redis Configuration
REDIS_URL=redis://redis:6379

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:5000
```

---

### 3.3 Verificar Docker Compose

**Arquivo:** `docker-compose.yml`

**Verificar:**
- ✅ MinIO configurado
- ✅ Redis configurado
- ✅ Backend configurado (sem ML dependencies)
- ✅ Frontend configurado
- ✅ Volumes configurados corretamente

---

<a name="docker-compose"></a>

## 4. 🐳 DEPLOYMENT COM DOCKER COMPOSE

### 4.1 Build e Start

**Ação:**
```bash
# 1. Build imagens
docker-compose build

# 2. Iniciar serviços
docker-compose up -d

# 3. Verificar logs
docker-compose logs -f
```

**Verificação:**
- [ ] Build sem erros
- [ ] Containers iniciando
- [ ] Logs sem erros críticos

---

### 4.2 Verificar Health Checks

**Ação:**
```bash
# 1. Verificar backend
curl http://localhost:5000/health

# 2. Verificar MinIO
curl http://localhost:9000/minio/health/live

# 3. Verificar Redis
docker-compose exec redis redis-cli ping

# 4. Verificar frontend
curl http://localhost:3000
```

**Resposta Esperada:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-05T10:00:00Z",
  "version": "2.0.0"
}
```

---

### 4.3 Parar Serviços

**Ação:**
```bash
# Parar serviços
docker-compose down

# Parar e remover volumes (cuidado!)
docker-compose down -v
```

---

<a name="manual"></a>

## 5. 🔧 DEPLOYMENT MANUAL

### 5.1 Backend (FastAPI)

**Ação:**
```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# 2. Instalar dependências (sem ML)
pip install -r backend/requirements_deployment.txt

# 3. Configurar variáveis de ambiente
export ENABLE_EXTERNAL_APIS=false
export ENABLE_ML_PROCESSING=false
export ML_RESULTS_PATH=./data/ml_results

# 4. Iniciar backend
cd backend
python -m app.main
```

**Verificação:**
- [ ] Backend iniciando sem erros
- [ ] Health check respondendo
- [ ] Endpoints funcionando

---

### 5.2 Frontend (Next.js)

**Ação:**
```bash
# 1. Instalar dependências
cd frontend
npm install

# 2. Configurar variáveis de ambiente
export NEXT_PUBLIC_API_URL=http://localhost:5000

# 3. Build
npm run build

# 4. Iniciar
npm start
```

**Verificação:**
- [ ] Frontend build sem erros
- [ ] Dashboard carregando
- [ ] Dados sendo exibidos

---

<a name="verificacao"></a>

## 6. ✅ VERIFICAÇÃO

### 6.1 Checklist de Deployment

#### Antes do Deploy:
- [ ] ✅ Dados pré-computados disponíveis
- [ ] ✅ Variáveis de ambiente configuradas
- [ ] ✅ Docker Compose configurado
- [ ] ✅ Sem ML dependencies no deployment

#### Durante o Deploy:
- [ ] ✅ Docker Compose build sem erros
- [ ] ✅ Containers iniciando corretamente
- [ ] ✅ Health checks passando
- [ ] ✅ Logs sem erros críticos

#### Após o Deploy:
- [ ] ✅ Backend respondendo
- [ ] ✅ Frontend carregando
- [ ] ✅ Dashboard exibindo dados
- [ ] ✅ Sistema de recomendações funcionando
- [ ] ✅ Sistema de notificações funcionando

---

### 6.2 Testes de Funcionalidade

**Ação:**
```bash
# 1. Testar health check
curl http://localhost:5000/health

# 2. Testar endpoints de forecasts
curl http://localhost:5000/api/v1/forecasts

# 3. Testar endpoints de analytics
curl http://localhost:5000/api/v1/analytics

# 4. Testar frontend
curl http://localhost:3000

# 5. Verificar logs
docker-compose logs backend
docker-compose logs frontend
```

**Verificação:**
- [ ] Todos os endpoints respondendo
- [ ] Dados sendo retornados corretamente
- [ ] Frontend renderizando
- [ ] Sem erros nos logs

---

### 6.3 Testes Offline

**Ação:**
```bash
# 1. Desabilitar internet (ou bloquear APIs externas)
# 2. Verificar que aplicação funciona
# 3. Testar todos os endpoints
# 4. Verificar logs (não deve haver tentativas de chamar APIs externas)
```

**Verificação:**
- [ ] Aplicação funciona offline
- [ ] Não há tentativas de chamar APIs externas
- [ ] Dados pré-computados sendo usados
- [ ] Sem erros relacionados a conectividade

---

<a name="troubleshooting"></a>

## 7. 🔧 TROUBLESHOOTING

### 7.1 Problemas Comuns

#### Erro: "Container fails to start"
**Solução:**
```bash
# 1. Verificar logs
docker-compose logs backend

# 2. Verificar variáveis de ambiente
docker-compose config

# 3. Verificar volumes
docker-compose ps
```

#### Erro: "ML dependencies detected"
**Solução:**
```bash
# 1. Verificar Dockerfile
cat infrastructure/docker/Dockerfile.backend.deployment

# 2. Verificar requirements
cat backend/requirements_deployment.txt

# 3. Rebuild
docker-compose build --no-cache backend
```

#### Erro: "External APIs still being called"
**Solução:**
```bash
# 1. Verificar variável de ambiente
echo $ENABLE_EXTERNAL_APIS  # Deve ser "false"

# 2. Verificar código
grep -r "ENABLE_EXTERNAL_APIS" backend/

# 3. Verificar logs
docker-compose logs backend | grep "external"
```

---

### 7.2 Verificação de Dependências

**Checklist:**
- [ ] ✅ Sem ML dependencies no container
- [ ] ✅ Sem chamadas a APIs externas
- [ ] ✅ Aplicação funciona offline
- [ ] ✅ Dados pré-computados sendo lidos
- [ ] ✅ Health checks passando

---

## 8. ✅ CHECKLIST FINAL

### Pré-Deployment:
- [ ] ✅ Dados pré-computados disponíveis
- [ ] ✅ Variáveis de ambiente configuradas
- [ ] ✅ Docker Compose configurado
- [ ] ✅ Sem ML dependencies

### Deployment:
- [ ] ✅ Build sem erros
- [ ] ✅ Containers iniciando
- [ ] ✅ Health checks passando
- [ ] ✅ Endpoints respondendo

### Pós-Deployment:
- [ ] ✅ Dashboard funcionando
- [ ] ✅ Dados sendo exibidos
- [ ] ✅ Sistema de recomendações funcionando
- [ ] ✅ Sistema de notificações funcionando
- [ ] ✅ Monitoramento funcionando

---

## 9. 📝 CONCLUSÃO

Este guia fornece:

1. **Deployment Simplificado:** Sem ML e sem APIs externas
2. **Docker Compose:** Setup completo
3. **Deployment Manual:** Alternativa sem Docker
4. **Verificação:** Checklist completo
5. **Troubleshooting:** Solução de problemas

**Próximos Passos:**
1. Preparar dados pré-computados
2. Configurar variáveis de ambiente
3. Executar deployment
4. Verificar funcionamento
5. Monitorar em produção

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia Completo - Pronto para Deployment

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

