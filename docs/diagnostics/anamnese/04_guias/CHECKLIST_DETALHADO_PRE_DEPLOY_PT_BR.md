# ✅ CHECKLIST DETALHADO PRÉ-DEPLOY
## Nova Corrente - Checklist Completo para Validação Antes do Deploy de Sábado

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Checklist Completo - Pronto para Uso  
**Objetivo:** Checklist detalhado para validar que todas as simplificações foram aplicadas

---

## 📋 ÍNDICE

1. [Checklist de Código](#checklist-codigo)
2. [Checklist de Dependências](#checklist-dependencias)
3. [Checklist de Configuração](#checklist-configuracao)
4. [Checklist de Testes](#checklist-testes)
5. [Checklist de Deployment](#checklist-deployment)
6. [Checklist de Validação Final](#checklist-validacao)

---

<a name="checklist-codigo"></a>

## 1. 🔍 CHECKLIST DE CÓDIGO

### 1.1 Remoção de ML Services

#### `backend/api/enhanced_api.py`
- [ ] ❌ Removido import de `model_registry`
- [ ] ❌ Removido uso de `model_registry` no código
- [ ] ✅ Arquivo não importa mais nenhuma dependência ML

#### `backend/app/core/integration_manager.py`
- [ ] ❌ Removida inicialização de `prediction_service` (linhas ~109-117)
- [ ] ❌ Removido import de `prediction_service`
- [ ] ✅ Código não referencia mais ML services

#### `backend/app/api/v1/routes/`
- [ ] ❌ Removidos endpoints que usam ML services
- [ ] ❌ Removidos endpoints de predição em tempo real
- [ ] ✅ Mantidos apenas endpoints de analytics (dados pré-computados)
- [ ] ✅ Mantidos endpoints de forecasts (dados pré-computados)

#### `backend/services/`
- [ ] ❌ `prediction_service.py` não é inicializado em produção
- [ ] ❌ `ml_models/model_registry.py` não é importado em produção
- [ ] ✅ Services ML existem apenas para referência (não usados em produção)

---

### 1.2 Desabilitação de APIs Externas

#### `backend/app/core/integration_manager.py`
- [ ] ❌ Removida inicialização de `external_data_service` (linhas ~61-62)
- [ ] ❌ Removida inicialização de external API clients:
  - [ ] INMET (Climate) - linhas ~122-134
  - [ ] BACEN (Economic) - linhas ~136-148
  - [ ] ANATEL (5G) - linhas ~150-162
  - [ ] OpenWeatherMap - linhas ~164-176
  - [ ] Expanded API Integration - linhas ~178-186
- [ ] ✅ Código não referencia mais APIs externas

#### `backend/pipelines/orchestrator_service.py`
- [ ] 🟡 Desabilitadas chamadas a `climate_etl.run()` (linhas ~84-102)
- [ ] 🟡 Desabilitadas chamadas a `economic_etl.run()`
- [ ] 🟡 Desabilitadas chamadas a `anatel_5g_etl.run()`
- [ ] ✅ Logs informam sobre uso de dados pré-computados

#### `backend/pipelines/climate_etl.py`
- [ ] 🟡 Desabilitadas chamadas API em tempo real
- [ ] ✅ Verifica `ENABLE_EXTERNAL_APIS=false` para usar dados pré-computados
- [ ] ✅ Logs informam sobre desabilitação

#### `backend/pipelines/economic_etl.py`
- [ ] 🟡 Desabilitadas chamadas API em tempo real
- [ ] ✅ Verifica `ENABLE_EXTERNAL_APIS=false` para usar dados pré-computados
- [ ] ✅ Logs informam sobre desabilitação

#### `backend/pipelines/anatel_5g_etl.py`
- [ ] 🟡 Desabilitadas chamadas API em tempo real
- [ ] ✅ Verifica `ENABLE_EXTERNAL_APIS=false` para usar dados pré-computados
- [ ] ✅ Logs informam sobre desabilitação

#### `backend/app/api/v1/routes/integration.py`
- [ ] 🟡 Desabilitados endpoints de refresh de APIs externas
- [ ] ✅ Endpoints retornam erro informando que APIs externas estão desabilitadas

---

### 1.3 Simplificação de Integration Manager

#### `backend/app/core/integration_manager.py`
- [ ] ✅ Removidos imports não utilizados
- [ ] ✅ Removidas variáveis não utilizadas
- [ ] ✅ Código limpo e organizado
- [ ] ✅ Documentação atualizada
- [ ] ✅ Health check não verifica serviços removidos

---

### 1.4 Remoção de API Legacy

#### `backend/api/enhanced_api.py`
- [ ] ❌ Arquivo removido completamente OU
- [ ] 🟡 Arquivo marcado como DEPRECATED
- [ ] ✅ FastAPI (`backend/app/main.py`) é a única API em produção

---

<a name="checklist-dependencias"></a>

## 2. 📦 CHECKLIST DE DEPENDÊNCIAS

### 2.1 Requirements Files

#### `backend/requirements_deployment.txt`
- [ ] ✅ Não contém ML dependencies (torch, tensorflow, sklearn, prophet, etc.)
- [ ] ✅ Contém apenas dependências necessárias para deployment
- [ ] ✅ DuckDB incluído para queries SQL
- [ ] ✅ Pandas incluído (sem ML usage)
- [ ] ✅ FastAPI incluído
- [ ] ✅ Redis incluído (caching)

#### `backend/requirements_ml.txt`
- [ ] ✅ Existe e contém ML dependencies
- [ ] ✅ Não é usado em deployment
- [ ] ✅ Usado apenas em ambiente ML local

#### `backend/requirements.txt`
- [ ] ✅ Contém todas as dependências (incluindo ML)
- [ ] ✅ Usado apenas para desenvolvimento local
- [ ] ✅ Não é usado em deployment

---

### 2.2 Dockerfile

#### `infrastructure/docker/Dockerfile.backend.deployment`
- [ ] ✅ Usa `requirements_deployment.txt` (não `requirements.txt`)
- [ ] ✅ Verifica ausência de ML dependencies após instalação
- [ ] ✅ Falha build se ML dependencies forem detectadas
- [ ] ✅ Não copia código ML para container
- [ ] ✅ Não copia collectors de APIs externas para container

---

<a name="checklist-configuracao"></a>

## 3. ⚙️ CHECKLIST DE CONFIGURAÇÃO

### 3.1 Variáveis de Ambiente

#### `.env` (ou variáveis no docker-compose.yml)
- [ ] ✅ `ENABLE_EXTERNAL_APIS=false` configurado
- [ ] ✅ `ENABLE_ML_PROCESSING=false` configurado
- [ ] ✅ `ML_RESULTS_PATH` configurado (caminho para dados pré-computados)
- [ ] ✅ `DATA_DIR` configurado
- [ ] ✅ `LOG_DIR` configurado
- [ ] ✅ `MINIO_ENDPOINT` configurado (se usando MinIO)
- [ ] ✅ `REDIS_URL` configurado

---

### 3.2 Docker Compose

#### `docker-compose.yml`
- [ ] ✅ Backend usa `Dockerfile.backend.deployment`
- [ ] ✅ Variáveis de ambiente configuradas corretamente
- [ ] ✅ Volumes configurados para dados pré-computados
- [ ] ✅ Health checks configurados
- [ ] ✅ MinIO configurado (se necessário)
- [ ] ✅ Redis configurado
- [ ] ✅ Frontend configurado
- [ ] ✅ Sem serviços de ML ou collectors

---

<a name="checklist-testes"></a>

## 4. 🧪 CHECKLIST DE TESTES

### 4.1 Testes Unitários

- [ ] ✅ Testes passando sem ML dependencies
- [ ] ✅ Testes passando sem APIs externas
- [ ] ✅ Cobertura de testes adequada
- [ ] ✅ Testes de endpoints analytics funcionando

---

### 4.2 Testes de Integração

- [ ] ✅ Aplicação inicia sem erros
- [ ] ✅ Health check retorna status saudável
- [ ] ✅ Endpoints respondendo corretamente
- [ ] ✅ Dados pré-computados sendo lidos
- [ ] ✅ Não há tentativas de chamar APIs externas
- [ ] ✅ Não há tentativas de usar ML services

---

### 4.3 Testes Offline

- [ ] ✅ Aplicação funciona completamente offline
- [ ] ✅ Não há chamadas a APIs externas
- [ ] ✅ Dados pré-computados sendo usados
- [ ] ✅ Sem erros relacionados a conectividade

---

### 4.4 Testes de Deployment

- [ ] ✅ Docker Compose build sem erros
- [ ] ✅ Containers iniciam corretamente
- [ ] ✅ Health checks passando
- [ ] ✅ Verificação de ML dependencies passando
- [ ] ✅ Aplicação funcionando

---

<a name="checklist-deployment"></a>

## 5. 🚀 CHECKLIST DE DEPLOYMENT

### 5.1 Preparação

- [ ] ✅ Dados pré-computados disponíveis
- [ ] ✅ Variáveis de ambiente configuradas
- [ ] ✅ Docker Compose configurado
- [ ] ✅ Backup do código atual feito
- [ ] ✅ Branch de trabalho criada

---

### 5.2 Build

- [ ] ✅ `docker-compose build` sem erros
- [ ] ✅ Containers build sem ML dependencies
- [ ] ✅ Verificação de ML dependencies passando
- [ ] ✅ Imagens criadas corretamente

---

### 5.3 Start

- [ ] ✅ `docker-compose up -d` sem erros
- [ ] ✅ Containers iniciam corretamente
- [ ] ✅ Health checks passando
- [ ] ✅ Logs sem erros críticos

---

### 5.4 Verificação

- [ ] ✅ Backend respondendo em `http://localhost:5000`
- [ ] ✅ Frontend respondendo em `http://localhost:3000`
- [ ] ✅ Health check retorna status saudável
- [ ] ✅ Endpoints retornando dados
- [ ] ✅ Dashboard carregando

---

<a name="checklist-validacao"></a>

## 6. ✅ CHECKLIST DE VALIDAÇÃO FINAL

### 6.1 Validação Automática

- [ ] ✅ Script de validação executado: `python scripts/validation/validate_deployment_simplified.py`
- [ ] ✅ Validação passou sem erros
- [ ] ✅ Relatório de validação gerado
- [ ] ✅ Todos os checks passando

---

### 6.2 Validação Manual

#### Verificação de ML Dependencies
- [ ] ✅ `grep -r "model_registry" backend/app/` não retorna resultados
- [ ] ✅ `grep -r "prediction_service" backend/app/` não retorna resultados
- [ ] ✅ `grep -r "import torch\|import tensorflow\|import sklearn" backend/app/` não retorna resultados
- [ ] ✅ Docker container não contém ML dependencies: `docker exec <container> pip list | grep -iE "(torch|tensorflow|sklearn)"`

#### Verificação de APIs Externas
- [ ] ✅ `grep -r "climate_etl.run\|economic_etl.run\|anatel_5g_etl.run" backend/app/` não retorna chamadas ativas
- [ ] ✅ `grep -r "external_data_service" backend/app/core/` não retorna resultados
- [ ] ✅ `grep -r "INMET_CONFIG\|BACEN_CONFIG\|ANATEL_CONFIG" backend/app/core/` não retorna resultados
- [ ] ✅ Logs não mostram tentativas de chamar APIs externas

#### Verificação de Funcionalidade
- [ ] ✅ Dashboard renderizando corretamente
- [ ] ✅ Dados pré-computados sendo exibidos
- [ ] ✅ Sistema de recomendações funcionando
- [ ] ✅ Sistema de notificações funcionando
- [ ] ✅ Monitoramento funcionando

---

### 6.3 Validação de Performance

- [ ] ✅ Tempo de resposta < 2s para queries
- [ ] ✅ Tempo de resposta < 500ms para endpoints cached
- [ ] ✅ Tempo de resposta < 2s para endpoints cold
- [ ] ✅ Frontend carrega < 2.5s
- [ ] ✅ Containers iniciam < 2 minutos

---

### 6.4 Validação de Segurança

- [ ] ✅ Sem ML dependencies expostas
- [ ] ✅ Sem APIs externas sendo chamadas
- [ ] ✅ Aplicação funciona offline (air-gapped)
- [ ] ✅ Dados pré-computados seguros
- [ ] ✅ Health checks funcionando

---

## 7. 📊 RESUMO DO CHECKLIST

### Estatísticas

**Total de Itens:** ~100 itens  
**Itens Críticos:** ~30 itens  
**Itens de Validação:** ~20 itens  
**Itens de Testes:** ~15 itens  
**Itens de Deployment:** ~15 itens  

### Status

- [ ] ✅ Código: ___ / ___ itens completos
- [ ] ✅ Dependências: ___ / ___ itens completos
- [ ] ✅ Configuração: ___ / ___ itens completos
- [ ] ✅ Testes: ___ / ___ itens completos
- [ ] ✅ Deployment: ___ / ___ itens completos
- [ ] ✅ Validação: ___ / ___ itens completos

**Status Geral:** ⏳ Pendente / ✅ Completo

---

## 8. 🚨 ITENS CRÍTICOS (DEVEM SER COMPLETADOS)

### Antes de Qualquer Deploy:

1. ✅ Remover ML services de produção
2. ✅ Desabilitar APIs externas em produção
3. ✅ Simplificar integration manager
4. ✅ Executar script de validação
5. ✅ Testar aplicação offline
6. ✅ Verificar health checks

---

## 9. 📝 NOTAS

### Itens que Podem Ser Feitos Após Deploy:

- Migrar storage para Parquet (pode ser feito após deploy)
- Remover API legacy Flask (pode ser feito após deploy)
- Otimizações de performance (podem ser feitas após deploy)

### Itens que DEVEM Ser Feitos Antes do Deploy:

- Remover ML services
- Desabilitar APIs externas
- Simplificar integration manager
- Validação completa
- Testes offline

---

## 10. ✅ CONCLUSÃO

Este checklist fornece:

1. **Verificação Completa:** Todos os itens necessários para deploy simplificado
2. **Validação Automática:** Script de validação incluído
3. **Validação Manual:** Checklist detalhado para verificação manual
4. **Priorização:** Itens críticos identificados

**Próximos Passos:**
1. Executar todas as ações do checklist
2. Executar script de validação
3. Verificar todos os itens manualmente
4. Deploy de Sábado

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Checklist Completo - Pronto para Uso

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

