# 🔍 SCRIPTS DE VALIDAÇÃO
## Nova Corrente - Scripts para Validar Deployment Simplificado

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Scripts Prontos - Validação Automática  
**Objetivo:** Scripts para validar ausência de ML dependencies e APIs externas

---

## 📋 SCRIPTS DISPONÍVEIS

### 1. `validate_deployment_simplified.py`

**Descrição:** Script completo de validação para deployment simplificado

**Uso:**
```bash
python scripts/validation/validate_deployment_simplified.py
```

**Validações:**
- ✅ ML Dependencies (requirements, imports, inicializações)
- ✅ External APIs (chamadas, clients, services)
- ✅ Dockerfile (verificação de ML dependencies)
- ✅ Environment Variables (configuração correta)

**Saída:**
- Relatório JSON em `reports/deployment_validation_results.json`
- Status no console (PASS/FAIL)
- Lista de erros e warnings

---

### 2. `check_no_ml_imports.py`

**Descrição:** Verifica ausência de imports ML no código de deployment

**Uso:**
```bash
python scripts/validation/check_no_ml_imports.py
```

**Validações:**
- ✅ Imports ML em `backend/app/`
- ✅ Imports ML em `backend/api/` (se existir)
- ✅ Inicializações de ML services

**Saída:**
- Lista de arquivos com imports ML
- Exit code 1 se erros encontrados

---

### 3. `check_no_external_apis.py`

**Descrição:** Verifica ausência de chamadas a APIs externas no código de deployment

**Uso:**
```bash
python scripts/validation/check_no_external_apis.py
```

**Validações:**
- ✅ Chamadas a ETL pipelines (climate_etl, economic_etl, anatel_5g_etl)
- ✅ Uso de external_data_service
- ✅ Uso de external API clients
- ✅ Chamadas a APIs externas

**Saída:**
- Lista de arquivos com chamadas a APIs externas
- Exit code 1 se erros encontrados

---

## 🚀 USO RECOMENDADO

### Antes de Cada Deploy:

```bash
# 1. Validar ML dependencies
python scripts/validation/check_no_ml_imports.py

# 2. Validar APIs externas
python scripts/validation/check_no_external_apis.py

# 3. Validação completa
python scripts/validation/validate_deployment_simplified.py
```

### Em CI/CD:

```bash
# Adicionar ao pipeline CI/CD
python scripts/validation/validate_deployment_simplified.py
if [ $? -ne 0 ]; then
    echo "Validation failed - deployment blocked"
    exit 1
fi
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

### Antes de Deploy:
- [ ] ✅ Script `check_no_ml_imports.py` passou
- [ ] ✅ Script `check_no_external_apis.py` passou
- [ ] ✅ Script `validate_deployment_simplified.py` passou
- [ ] ✅ Relatório de validação gerado
- [ ] ✅ Nenhum erro crítico encontrado

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Scripts Prontos - Pronto para Uso

