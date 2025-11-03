# 🚀 QUICK START GUIDE
## Nova Corrente - Analytics Engineering

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Guia Rápido Completo

---

## 📋 INÍCIO RÁPIDO

### Para Quem Quer Começar Agora

**Escolha seu perfil:**

1. [Data Engineer](#data-engineer) - Setup infraestrutura
2. [Analyst](#analyst) - Criar dashboards
3. [Data Scientist](#data-scientist) - Otimizar modelos ML
4. [DevOps](#devops) - Setup Airflow/Infra

---

<a name="data-engineer"></a>

## 👨‍💻 DATA ENGINEER

### Setup Rápido (30 minutos)

**1. Terraform (Infraestrutura):**
```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

**2. dbt (Transformações):**
```bash
cd dbt
pip install dbt-databricks
dbt deps
dbt debug  # Test connection
dbt run --models staging  # Run staging models
```

**3. Airflow (Orquestração):**
```bash
cd infrastructure/airflow
docker-compose up -d
# Access: http://localhost:8080
# Login: airflow/airflow
```

**Próximos passos:**
- Ver [PHASE_0_FOUNDATION_DETAILED_PT_BR.md](./PHASE_0_FOUNDATION_DETAILED_PT_BR.md)

---

<a name="analyst"></a>

## 📊 ANALYST

### Setup Rápido (15 minutos)

**1. Conectar ao Databricks:**
```sql
-- Acessar Gold layer
SELECT * FROM nova_corrente.gold.marts.fact_forecasts
WHERE date >= CURRENT_DATE - 30
LIMIT 100;
```

**2. Criar Query no Metabase:**
```
1. Acessar: http://metabase.novacorrente.com
2. Add Database → Databricks
3. Configurar conexão
4. Criar query visual
```

**3. Criar Dashboard:**
```
1. New Dashboard
2. Add Card (query)
3. Customize layout
4. Save
```

**Próximos passos:**
- Ver [PHASE_2_ANALYTICS_LAYER_DETAILED_PT_BR.md](./PHASE_2_ANALYTICS_LAYER_DETAILED_PT_BR.md)

---

<a name="data-scientist"></a>

## 🧪 DATA SCIENTIST

### Otimização Rápida (1 hora)

**1. Imputar Features Externas:**
```python
python scripts/impute_external_features.py
```

**2. Normalizar Dados:**
```python
python scripts/normalize_features.py
```

**3. Treinar Modelos:**
```python
python scripts/train_models.py
```

**4. Avaliar Performance:**
```python
python scripts/evaluate_models.py
# Verificar MAPE < 15%
```

**Próximos passos:**
- Ver [NEXT_STEPS_OPTIMIZATION_PT_BR.md](./NEXT_STEPS_OPTIMIZATION_PT_BR.md)

---

<a name="devops"></a>

## 🔧 DEVOPS

### Setup Rápido (45 minutos)

**1. Infraestrutura:**
```bash
cd infrastructure/terraform
terraform apply
```

**2. Airflow:**
```bash
cd infrastructure/airflow
docker-compose up -d
```

**3. Monitoramento:**
```bash
# Setup Prometheus/Grafana
# Configure alerts
```

**Próximos passos:**
- Ver [TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md](./TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md)

---

## 📚 REFERÊNCIAS RÁPIDAS

### Comandos Úteis

**dbt:**
```bash
dbt run                  # Run all models
dbt run --models staging # Run only staging
dbt test                 # Run tests
dbt docs serve          # View docs
```

**Airflow:**
```bash
airflow dags list                    # List DAGs
airflow tasks test dag_id task_id    # Test task
airflow dags trigger dag_id          # Trigger DAG
```

**Databricks:**
```bash
databricks jobs list              # List jobs
databricks jobs run-now --job-id 12345  # Run job
databricks clusters list          # List clusters
```

---

## 🔗 LINKS RÁPIDOS

**Documentação:**
- [Roadmap Completo](./ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md)
- [Estado Atual](./CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md)
- [Próximos Passos](./NEXT_STEPS_OPTIMIZATION_PT_BR.md)

**Guias:**
- [Fase 0](./PHASE_0_FOUNDATION_DETAILED_PT_BR.md)
- [Fase 1](./PHASE_1_DATA_FOUNDATION_DETAILED_PT_BR.md)
- [Fase 2](./PHASE_2_ANALYTICS_LAYER_DETAILED_PT_BR.md)

**Referências:**
- [Arquitetura Técnica](./TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md)
- [Stack Técnico](./REFERENCE_TECHNICAL_STACK_PT_BR.md)
- [Troubleshooting](./TROUBLESHOOTING_GUIDE_PT_BR.md)

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Quick Start Guide Completo

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

