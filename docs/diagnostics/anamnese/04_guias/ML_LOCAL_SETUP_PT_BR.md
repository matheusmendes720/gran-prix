# 🤖 SETUP LOCAL DE ML PROCESSING
## Nova Corrente - Como Rodar ML Localmente e Gerar Resultados Pré-Computados

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Guia Completo - Setup Local de ML  
**Objetivo:** Documentar como rodar ML localmente e gerar resultados pré-computados para produção

---

## 📋 ÍNDICE

1. [Visão Geral](#visao-geral)
2. [Pré-requisitos](#pre-requisitos)
3. [Setup do Ambiente ML](#setup-ambiente)
4. [Rodando ML Localmente](#rodando-ml)
5. [Gerando Resultados Pré-Computados](#gerando-resultados)
6. [Atualizando Dados em Produção](#atualizando-producao)
7. [Troubleshooting](#troubleshooting)

---

<a name="visao-geral"></a>

## 1. 📖 VISÃO GERAL

### 1.1 Estratégia

**ML Processing:**
- ✅ Roda **localmente** (separado do deployment)
- ✅ Gera resultados pré-computados em Parquet
- ✅ Resultados são copiados para storage de produção
- ✅ Deployment apenas lê resultados pré-computados

**Deployment:**
- ❌ **NÃO** roda ML processing
- ❌ **NÃO** tem ML dependencies
- ✅ Apenas lê resultados pré-computados

---

### 1.2 Fluxo de Dados

```
1. ML Processing (Local)
   ├── Coleta dados históricos
   ├── Treina modelos (Prophet, ARIMA, LSTM)
   ├── Gera previsões
   └── Salva resultados em Parquet

2. Storage (Compartilhado)
   ├── Recebe resultados pré-computados
   └── Disponibiliza para deployment

3. Deployment (Produção)
   ├── Lê resultados pré-computados
   ├── Exibe no dashboard
   └── Sistema de recomendações
```

---

<a name="pre-requisitos"></a>

## 2. ✅ PRÉ-REQUISITOS

### 2.1 Software Necessário

- ✅ Python 3.8+
- ✅ pip (gerenciador de pacotes)
- ✅ Git (para clonar repositório)
- ✅ Docker (opcional - para ambiente isolado)

### 2.2 Dependências ML

**Arquivo:** `backend/requirements_ml.txt`

**Dependências principais:**
- pandas>=2.0.0
- numpy>=1.24.0
- statsmodels>=0.14.0
- prophet>=1.1.5
- pmdarima>=2.0.0
- scikit-learn>=1.3.0
- tensorflow>=2.13.0

---

<a name="setup-ambiente"></a>

## 3. 🔧 SETUP DO AMBIENTE ML

### 3.1 Criar Ambiente Virtual

**Ação:**
```bash
# 1. Criar ambiente virtual
python -m venv venv_ml

# 2. Ativar ambiente virtual
# Windows:
venv_ml\Scripts\activate
# Linux/Mac:
source venv_ml/bin/activate

# 3. Instalar dependências ML
pip install -r backend/requirements_ml.txt
```

**Verificação:**
```bash
# Verificar que dependências foram instaladas
pip list | grep -iE "(prophet|arima|tensorflow|sklearn)"
```

---

### 3.2 Configurar Variáveis de Ambiente

**Arquivo:** `.env.ml` (criar novo arquivo)

**Conteúdo:**
```bash
# ML Processing Environment
ENABLE_EXTERNAL_APIS=true
ENABLE_ML_PROCESSING=true
ML_RESULTS_PATH=./data/ml_results
MODELS_DIR=./models
DATA_DIR=./data
LOG_DIR=./logs
```

**Ação:**
```bash
# Copiar arquivo de exemplo
cp .env.example .env.ml

# Editar com suas configurações
nano .env.ml
```

---

<a name="rodando-ml"></a>

## 4. 🚀 RODANDO ML LOCALMENTE

### 4.1 Coletar Dados Históricos

**Ação:**
```bash
# 1. Ativar ambiente ML
source venv_ml/bin/activate

# 2. Coletar dados de APIs externas (se necessário)
python backend/pipelines/climate_etl.py
python backend/pipelines/economic_etl.py
python backend/pipelines/anatel_5g_etl.py

# 3. Processar dados
python backend/pipelines/feature_calculation_etl.py
```

**Nota:** Coleta de dados pode ser feita periodicamente (não precisa ser em tempo real)

---

### 4.2 Treinar Modelos

**Ação:**
```bash
# 1. Treinar modelos Prophet
python backend/ml/train_prophet.py

# 2. Treinar modelos ARIMA
python backend/ml/train_arima.py

# 3. Treinar modelos LSTM
python backend/ml/train_lstm.py

# 4. Ensemble de modelos
python backend/ml/train_ensemble.py
```

**Resultado:**
- Modelos salvos em `models/nova_corrente/`
- Métricas de avaliação em `reports/results/`

---

### 4.3 Gerar Previsões

**Ação:**
```bash
# 1. Gerar previsões para todos os itens
python backend/ml/generate_forecasts.py

# 2. Gerar previsões para itens específicos
python backend/ml/generate_forecasts.py --items "item1,item2,item3"

# 3. Gerar previsões para horizonte específico
python backend/ml/generate_forecasts.py --horizon 30
```

**Resultado:**
- Previsões salvas em `data/ml_results/forecasts/`
- Formato: Parquet files com metadata

---

<a name="gerando-resultados"></a>

## 5. 📊 GERANDO RESULTADOS PRÉ-COMPUTADOS

### 5.1 Estrutura de Resultados Pré-Computados

**Estrutura:**
```
data/ml_results/
├── forecasts/
│   ├── forecasts_2025-11-XX.parquet
│   ├── forecasts_2025-11-XX_metadata.json
│   └── ...
├── recommendations/
│   ├── recommendations_2025-11-XX.parquet
│   └── ...
├── metrics/
│   ├── metrics_2025-11-XX.parquet
│   └── ...
└── metadata/
    ├── model_versions.json
    └── last_updated.json
```

---

### 5.2 Gerar Resultados Completos

**Script:** `scripts/generate_ml_results.py`

**Ação:**
```bash
# 1. Gerar todos os resultados
python scripts/generate_ml_results.py

# 2. Gerar apenas previsões
python scripts/generate_ml_results.py --only-forecasts

# 3. Gerar apenas recomendações
python scripts/generate_ml_results.py --only-recommendations
```

**Resultado:**
- Todos os resultados em Parquet
- Metadata incluída (model_version, generated_at, source, dataset_id)
- Prontos para copiar para produção

---

### 5.3 Formato de Metadata

**Arquivo:** `data/ml_results/metadata/model_versions.json`

**Conteúdo:**
```json
{
  "model_version": "v1.0.0",
  "generated_at": "2025-11-05T10:00:00Z",
  "source": "ml_processing_local",
  "dataset_id": "dataset_2025-11-05",
  "models": {
    "prophet": "v1.0.0",
    "arima": "v1.0.0",
    "lstm": "v1.0.0",
    "ensemble": "v1.0.0"
  },
  "metrics": {
    "mape": 12.5,
    "rmse": 45.2,
    "accuracy": 87.5
  }
}
```

---

<a name="atualizando-producao"></a>

## 6. 📤 ATUALIZANDO DADOS EM PRODUÇÃO

### 6.1 Copiar Resultados para Storage Compartilhado

**Ação:**
```bash
# 1. Copiar resultados para MinIO (se usando MinIO)
mc cp data/ml_results/ minio/nova-corrente/ml_results/ --recursive

# 2. OU copiar para diretório compartilhado
cp -r data/ml_results/ /shared/ml_results/

# 3. OU usar script de deploy
python scripts/deploy_ml_results.py
```

---

### 6.2 Atualizar Deployment

**Ação:**
```bash
# 1. Se usando Docker Compose
docker-compose restart backend

# 2. Backend vai ler automaticamente novos resultados
# 3. Verificar health check
curl http://localhost:5000/health

# 4. Verificar que novos dados estão disponíveis
curl http://localhost:5000/api/v1/forecasts
```

---

### 6.3 Atualização Automática (Opcional)

**Script:** `scripts/auto_update_ml_results.py`

**Ação:**
```bash
# 1. Configurar cron job (Linux/Mac)
# Rodar diariamente às 2 AM
0 2 * * * cd /path/to/gran_prix && python scripts/auto_update_ml_results.py

# 2. OU usar Task Scheduler (Windows)
# Criar tarefa agendada para rodar diariamente
```

---

<a name="troubleshooting"></a>

## 7. 🔧 TROUBLESHOOTING

### 7.1 Problemas Comuns

#### Erro: "ModuleNotFoundError: No module named 'prophet'"
**Solução:**
```bash
# Instalar dependências ML
pip install -r backend/requirements_ml.txt
```

#### Erro: "TensorFlow not found"
**Solução:**
```bash
# Instalar TensorFlow
pip install tensorflow>=2.13.0
```

#### Erro: "Dados não encontrados"
**Solução:**
```bash
# Verificar que dados históricos existem
ls data/raw/
ls data/processed/

# Coletar dados se necessário
python backend/pipelines/climate_etl.py
```

---

### 7.2 Verificação de Setup

**Checklist:**
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências ML instaladas
- [ ] Dados históricos coletados
- [ ] Modelos treinados
- [ ] Resultados gerados em Parquet
- [ ] Metadata incluída
- [ ] Resultados copiados para storage compartilhado

---

## 8. ✅ CHECKLIST DE USO

### Antes de Rodar ML:
- [ ] Ambiente virtual criado
- [ ] Dependências ML instaladas
- [ ] Variáveis de ambiente configuradas
- [ ] Dados históricos coletados

### Rodando ML:
- [ ] Modelos treinados
- [ ] Previsões geradas
- [ ] Resultados salvos em Parquet
- [ ] Metadata incluída

### Após Gerar Resultados:
- [ ] Resultados copiados para storage compartilhado
- [ ] Deployment atualizado (se necessário)
- [ ] Health check passando
- [ ] Dados disponíveis no dashboard

---

## 9. 📝 CONCLUSÃO

Este guia fornece:

1. **Setup Completo:** Como configurar ambiente ML local
2. **Processo de ML:** Como rodar ML localmente
3. **Geração de Resultados:** Como gerar resultados pré-computados
4. **Atualização:** Como atualizar dados em produção
5. **Troubleshooting:** Solução de problemas comuns

**Próximos Passos:**
1. Setup do ambiente ML local
2. Treinar modelos
3. Gerar resultados pré-computados
4. Copiar para produção
5. Verificar funcionamento

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia Completo - Pronto para Uso

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

