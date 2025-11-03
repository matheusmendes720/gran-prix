# 🇧🇷 Resumo de Novos Datasets Brasileiros Adicionados

## Nova Corrente - Demand Forecasting System

---

## ✅ Datasets Adicionados ao Config

### 1. **anatel_mobile_brazil** ⭐⭐⭐⭐⭐

**Fonte:** Anatel / Data Basis  
**URL:** https://data-basis.org/dataset/d3c86a88-d9a4-4c0-bdec-08ab61e8f63c

**Descrição:**
- Dados oficiais da Anatel sobre acessos móveis no Brasil
- Estatísticas de assinantes e breakdown tecnológico (GSM, 5G)
- Granularidade regional

**Mapeamento:**
- `date` → Date
- `quantity` → Subscribers
- `category` → Technology
- `site_id` → Region

**Relevância:** ⭐⭐⭐⭐⭐ (Dados oficiais regulatórios)

**Aplicações:**
- Previsão de demanda para logística 5G
- Rastreamento de crescimento de assinantes → demanda por upgrades
- Análise regional de adoção tecnológica

**Limitações:**
- Dados podem estar defasados (meses)
- Recomendação: verificação cruzada com fontes comerciais

---

### 2. **zenodo_broadband_brazil** ⭐⭐⭐⭐⭐

**Fonte:** Zenodo  
**URL:** https://zenodo.org/records/10482897

**Descrição:**
- Dataset real de uma operadora brasileira
- Parâmetros de modem (força de sinal, uptime)
- Demografia de usuários para milhares de usuários de banda larga

**Mapeamento:**
- `date` → timestamp
- `item_id` → modem_id
- `quantity` → signal_strength
- `site_id` → operator_site

**Relevância:** ⭐⭐⭐⭐⭐ (Dados reais de operadora)

**Aplicações:**
- Modelagem preditiva para demanda em manutenção de rede
- Insights de long-tail sobre eventos raros de downtime
- Integração com ensembles (SARIMAX/Prophet/LSTM)

**Limitações:**
- Viés específico de operadora
- Escala pode ser limitada

---

### 3. **internet_aberta_forecast** ⭐⭐⭐⭐⭐

**Fonte:** Internet Aberta  
**URL:** https://internetaberta.com.br/wp-content/uploads/2024/05/Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf

**Descrição:**
- Projeções top-down sobre usuários de banda larga
- Prevalência de 4G/5G, correlações com PIB
- Consumo de dados (297 a 400 exabytes até 2033)

**Mapeamento:**
- `date` → Year
- `quantity` → Data_Traffic_TB
- `category` → Technology_Type

**Relevância:** ⭐⭐⭐⭐⭐ (Forecasts essenciais)

**Aplicações:**
- Planejamento logístico de longo prazo
- Endereçamento de períodos intermitentes de alta demanda
- Modelagem de investimentos futuros

**Limitações:**
- Formato PDF (pode requerer parsing)
- Incertezas inerentes a forecasts
- Requer estratégias de hedging

---

### 4. **springer_digital_divide** ⭐⭐⭐⭐

**Fonte:** Springer / Ookla  
**URL:** https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-024-00508-8

**Descrição:**
- ~100 milhões de entradas do Ookla
- Testes de velocidade e conectividade em cidades brasileiras
- Foco em gaps urbano-rurais

**Mapeamento:**
- `date` → test_timestamp
- `item_id` → test_id
- `quantity` → download_speed_mbps
- `site_id` → city_id
- `category` → urban_rural

**Relevância:** ⭐⭐⭐⭐ (Dados espaciais massivos)

**Aplicações:**
- Previsão de demanda espacial para logística de banda larga
- Análise de digital divide
- Modelagem de cobertura de conectividade

**Limitações:**
- Dataset massivo (~100M registros)
- Requer Dask para processamento
- Recomendação: amostrar 1-5M registros inicialmente
- Possíveis viéses de amostragem

---

## 📊 Datasets Já Configurados (Adicionados Anteriormente)

### 5. **github_5g3e** ⭐⭐⭐⭐⭐

**Fonte:** GitHub (CNAM)  
**URL:** https://github.com/cedric-cnam/5G3E-dataset

**Descrição:**
- 14 dias de time-series de infraestrutura 5G virtualizada
- Dados de rádio, servidor, OS e network functions
- Milhares de features agrupadas por tipo de recurso/nó

**Relevância:** ⭐⭐⭐⭐⭐ (Excelente para manutenção preditiva)

---

### 6. **kaggle_equipment_failure** ⭐⭐⭐⭐

**Fonte:** Kaggle  
**Dataset:** geetanjalisikarwar/equipment-failure-prediction-dataset

**Descrição:**
- 10,000 pontos com 14 features sobre falhas de máquinas
- Tipos de hardware/software
- Modela falhas long-tail em equipamentos de telecomunicações

**Relevância:** ⭐⭐⭐⭐ (Modela long-tail failures)

---

### 7. **github_network_fault** ⭐⭐⭐⭐

**Fonte:** GitHub  
**URL:** https://github.com/subhashbylaiah/Network-Fault-Prediction

**Descrição:**
- Severidade de falhas em interrupções de rede de telecomunicações
- Features de classificação
- Previne eventos long-tail que dirigem demandas logísticas

**Relevância:** ⭐⭐⭐⭐ (Dados Telstra network)

---

### 8. **kaggle_telecom_network** ⭐⭐⭐

**Fonte:** Kaggle  
**Dataset:** praveenaparimi/telecom-network-dataset

**Descrição:**
- Dados de operações em nível de torre
- Tower ID, usuários conectados, velocidades de download
- Indicadores de performance

**Relevância:** ⭐⭐⭐ (Dados de torre)

---

### 9. **github_opencellid** ⭐⭐⭐⭐⭐

**Fonte:** GitHub  
**URL:** https://github.com/plotly/dash-world-cell-towers

**Descrição:**
- Mais de 40 milhões de registros de features de torres celulares
- Localizações (lat/long), tipos de rádio, alcance de sinal
- Cobertura espacial

**Relevância:** ⭐⭐⭐⭐⭐ (Dataset massivo espacial)

**Nota:** Requer amostragem devido a 40M+ registros. Crítico para forecasting geográfico e logística específica de torres.

---

## 📋 Status de Integração

### Prontos para Download

- ✅ **github_5g3e** - Requer implementação de download GitHub
- ✅ **kaggle_equipment_failure** - Pronto (via Kaggle API)
- ✅ **github_network_fault** - Requer implementação de download GitHub
- ✅ **kaggle_telecom_network** - Pronto (via Kaggle API)
- ✅ **github_opencellid** - Requer implementação de download GitHub
- ✅ **anatel_mobile_brazil** - Requer download direto (scraping possível)
- ✅ **zenodo_broadband_brazil** - Pronto (via Zenodo download)
- ✅ **internet_aberta_forecast** - Requer parsing de PDF
- ✅ **springer_digital_divide** - Requer download direto

### Requer Implementação

1. **Download de GitHub Repositories**
   - Clonar repo ou baixar arquivos específicos
   - Suporte para releases/assets
   - Suporte para arquivos grandes (Git LFS)

2. **Download de PDFs e Parsing**
   - Download de PDFs
   - Extração de tabelas/CSVs embutidos
   - OCR se necessário

3. **Scraping de Sites Regulatórios**
   - Scraping de sites da Anatel
   - Download de CSVs disponíveis
   - Suporte para formatos variados

---

## 🚀 Próximos Passos

### Fase 1: Implementar Downloads GitHub

1. Adicionar método `download_github_dataset()` em `download_datasets.py`
2. Suporte para:
   - Clonagem de repositórios
   - Download de releases/assets
   - Download de arquivos específicos via raw URLs
   - Git LFS para arquivos grandes

### Fase 2: Implementar Downloads de PDFs

1. Adicionar método `download_pdf_dataset()` 
2. Parsing de PDFs com `pdfplumber` ou `tabula-py`
3. Extração de tabelas/CSVs embutidos

### Fase 3: Integrar Datasets Brasileiros

1. Priorizar: Anatel Mobile + Zenodo Broadband
2. Implementar downloads para datasets brasileiros
3. Preprocessing específico para contexto brasileiro
4. Feature engineering para dados brasileiros

### Fase 4: Validação e Testes

1. Testar downloads de todos os novos datasets
2. Validar preprocessing e mapeamento de colunas
3. Verificar qualidade e completude dos dados
4. Integrar ao pipeline completo

---

## 📊 Resumo de Datasets

| Dataset | Fonte | Registros Estimados | Relevância | Status |
|---------|-------|---------------------|------------|--------|
| **anatel_mobile_brazil** | Anatel | Variável | ⭐⭐⭐⭐⭐ | ⏳ Pendente |
| **zenodo_broadband_brazil** | Zenodo | Milhares | ⭐⭐⭐⭐⭐ | ✅ Pronto |
| **internet_aberta_forecast** | Internet Aberta | Projeções | ⭐⭐⭐⭐⭐ | ⏳ Pendente |
| **springer_digital_divide** | Springer/Ookla | ~100M | ⭐⭐⭐⭐ | ⏳ Pendente |
| **github_5g3e** | GitHub | ~14 dias | ⭐⭐⭐⭐⭐ | ⏳ Pendente |
| **kaggle_equipment_failure** | Kaggle | 10K | ⭐⭐⭐⭐ | ✅ Pronto |
| **github_network_fault** | GitHub | Variável | ⭐⭐⭐⭐ | ⏳ Pendente |
| **kaggle_telecom_network** | Kaggle | Variável | ⭐⭐⭐ | ✅ Pronto |
| **github_opencellid** | GitHub | 40M+ | ⭐⭐⭐⭐⭐ | ⏳ Pendente |

---

## ✅ Status Atual

**Total de Novos Datasets Adicionados:** 9

- ✅ **Configurados:** 9/9 (100%)
- ✅ **Prontos para Download:** 3/9 (33%)
- ⏳ **Requerem Implementação:** 6/9 (67%)

**Próxima Prioridade:** Implementar downloads GitHub e integrar datasets brasileiros.

---

**Status:** 📚 **DOCUMENTAÇÃO COMPLETA - Datasets Adicionados ao Config**

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

