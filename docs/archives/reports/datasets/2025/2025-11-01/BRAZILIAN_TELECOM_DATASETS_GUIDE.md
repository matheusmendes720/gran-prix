# 🇧🇷 Guia Completo de Datasets Brasileiros de Telecomunicações

## Nova Corrente - Demand Forecasting System

---

## 📊 Visão Geral

Este documento fornece uma análise completa de datasets brasileiros de telecomunicações disponíveis publicamente, com foco em aplicações para previsão de demanda e logística de manutenção de torres.

**Contexto Brasileiro:**
- **Regulador:** Anatel (Agência Nacional de Telecomunicações)
- **Mercado:** Investimentos superiores a R$34.6 bilhões em infraestrutura (2024)
- **Cobertura:** ISPs dominam ~60% do mercado de banda larga
- **5G:** Expansão rápida com cobertura crescente

---

## 🏛️ Datasets Regulatórios e Oficiais (Anatel)

### 1. Mobile Phone Accesses in Brazil

**Fonte:** Anatel / Data Basis  
**Descrição:** Dados abrangentes sobre acessos móveis no Brasil, incluindo estatísticas de assinantes e breakdown tecnológico (GSM, 5G, etc.)

**Características:**
- **Formato:** CSV/Excel
- **Acesso:** [Data Basis](https://data-basis.org/dataset/d3c86a88-d9a4-4fc0-bdec-08ab61e8f63c) ou [Teleco](https://www.teleco.com.br/en/en_ncel.asp)
- **Granularidade:** Regional, municipal
- **Período:** Histórico disponível

**Aplicações:**
- Modelagem de demanda para equipamentos de rede durante expansão 5G
- Previsão de crescimento de assinantes → demanda por upgrades de torres
- Análise de long-tail para áreas rurais com acesso intermitente

**Limitações:**
- Dados podem estar defasados por meses
- Requer verificação cruzada com fontes comerciais
- Agregações podem mascarar padrões locais

**Relevância para Nova Corrente:** ⭐⭐⭐⭐⭐

---

### 2. Internet Access and Broadband Data

**Fonte:** Anatel  
**Descrição:** Arquivos CSV detalhados sobre conexões de banda larga, velocidades e cobertura, agregados por município e estado.

**Características:**
- **Formato:** CSV
- **Acesso:** [Net Data Directory](https://netdatadirectory.org/node/2336) ou portais oficiais da Anatel
- **Tamanho:** Variável (milhões de entradas para cobertura nacional)
- **Histórico:** Tendências históricas dos dashboards da Anatel

**Aplicações:**
- Análise espacial em logística de telecomunicações
- Modelagem de demanda por infraestrutura de banda larga
- Planejamento de expansão de cobertura

**Limitações:**
- Dados podem estar defasados
- Requer suplementação para previsão em tempo real
- Recomendação: usar hedging cruzando com fontes comerciais

**Relevância para Nova Corrente:** ⭐⭐⭐⭐

---

### 3. Anatel Tracker and Market Reports

**Fonte:** Anatel  
**Descrição:** Relatórios mensais sobre ganhos de assinantes e market shares (ex: Claro liderando adições pós-pagas em 2023).

**Características:**
- **Formato:** PDF/CSV
- **Acesso:** [Scribd](https://www.scribd.com/document/637889675/Untitled) ou plataformas integradas com Anatel
- **Frequência:** Mensal

**Aplicações:**
- Suporte a modelos de supply chain ligando dinâmicas de mercado a necessidades de aquisição de hardware
- Análise competitiva
- Modelagem de demanda por equipamentos baseada em crescimento de mercado

**Limitações:**
- Acesso pode ser restrito em alguns relatórios
- Formato PDF pode requerer extração manual

**Relevância para Nova Corrente:** ⭐⭐⭐⭐

---

## 📚 Datasets Acadêmicos e de Pesquisa

### 4. Real Dataset from Broadband Customers of a Brazilian Telecom Operator

**Fonte:** Zenodo  
**Descrição:** Dataset extraído de uma operadora brasileira, incluindo parâmetros de modem (força de sinal, uptime) e demografia de usuários para milhares de usuários de banda larga.

**Características:**
- **Formato:** CSV
- **Tamanho:** Variável (snapshots de time-series)
- **Acesso:** [Zenodo](https://zenodo.org/records/10482897)
- **Período:** Histórico disponível

**Aplicações:**
- Modelagem preditiva para demanda em manutenção de rede
- Insights de long-tail sobre eventos raros de downtime
- Integração com ensembles para hedging de incerteza

**Limitações:**
- Viés específico da operadora
- Escala pode ser limitada
- Dados podem estar anonimizados

**Relevância para Nova Corrente:** ⭐⭐⭐⭐⭐

---

### 5. Data Traffic Demand Forecast for Brazil

**Fonte:** Internet Aberta  
**Descrição:** Projeções top-down sobre usuários de banda larga, prevalência de 4G/5G, correlações com PIB e consumo de dados (ex: 297 a 400 exabytes até 2033).

**Características:**
- **Formato:** PDF com CSV embutido
- **Acesso:** [Internet Aberta](https://internetaberta.com.br/wp-content/uploads/2024/05/Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf)
- **Tipo:** Projeções e forecasts

**Aplicações:**
- Planejamento logístico de longo prazo em telecomunicações
- Endereçamento de períodos intermitentes de alta demanda (ex: grandes eventos)
- Modelagem de investimentos futuros em infraestrutura

**Limitações:**
- Incertezas inerentes a forecasts
- Pode não capturar eventos disruptivos
- Requer atualização periódica

**Relevância para Nova Corrente:** ⭐⭐⭐⭐⭐

---

### 6. Public Telephones Dataset Analysis

**Fonte:** GitHub Pages  
**Descrição:** Dados espaciais e de uso sobre a rede de telefones públicos do Brasil, processados com R para visualização e tendências.

**Características:**
- **Formato:** CSV/R scripts
- **Acesso:** [GitHub Pages](https://guilhermegch.github.io/blog/posts/public-telephone/)
- **Enfoque:** Infraestrutura legada

**Aplicações:**
- Estudos comparativos sobre transições digitais
- Necessidades de telecomunicações long-tail em áreas rurais
- Análise de padrões históricos de infraestrutura

**Limitações:**
- Limitado a telefones públicos
- Dados podem estar desatualizados (infraestrutura em declínio)
- Escopo geográfico pode ser limitado

**Relevância para Nova Corrente:** ⭐⭐⭐

---

### 7. Bridging the Digital Divide: Internet Connectivity Evolution

**Fonte:** Springer  
**Descrição:** Quase 100 milhões de entradas do Ookla sobre testes de velocidade e conectividade em cidades brasileiras, com foco em gaps urbano-rurais.

**Características:**
- **Formato:** CSV
- **Tamanho:** ~100 milhões de registros
- **Acesso:** [Springer](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-024-00508-8)
- **Cobertura:** Nacional com granularidade urbano-rural

**Aplicações:**
- Previsão de demanda espacial para logística de banda larga
- Análise de digital divide
- Modelagem de cobertura de conectividade

**Limitações:**
- Possíveis viéses de amostragem
- Dados podem estar agregados
- Requer processamento em escala (Dask recomendado)

**Relevância para Nova Corrente:** ⭐⭐⭐⭐

---

## 💼 Datasets Comerciais e de Mercado

### 8. Brazil Telecom Market 2024 Report

**Fonte:** Analysys Mason  
**Descrição:** KPIs sobre assinantes, penetração, receita e ARPU.

**Características:**
- **Formato:** Relatório com dados embutidos
- **Acesso:** [Analysys Mason](https://www.analysysmason.com/research/content/country-reports/brazil-country-report-rddj0/)
- **Frequência:** Anual

**Aplicações:**
- Suporte a modelos de demanda para investimento em logística 5G
- Análise de market share
- Estudos de investimento

**Limitações:**
- Restrições de acesso comercial
- Pode ter viés comercial
- Requer assinatura ou pagamento

**Relevância para Nova Corrente:** ⭐⭐⭐

---

### 9. Telecoms Industry Statistics

**Fonte:** Statista  
**Descrição:** Índices de receita e satisfação do cliente, com dados de 2023 mostrando pré-pago móvel com maior satisfação.

**Características:**
- **Formato:** Tabelas agregadas
- **Acesso:** [Statista](https://www.statista.com/topics/7187/telecommunications-in-brazil/)
- **Cobertura:** KPIs agregados do setor

**Aplicações:**
- Benchmarking de demandas long-tail dirigidas por consumidor
- Análise de satisfação do cliente → demanda por upgrades
- Estudos comparativos de mercado

**Limitações:**
- Agregado, menos granular
- Pode ter restrições de acesso
- Dados podem estar defasados

**Relevância para Nova Corrente:** ⭐⭐⭐

---

### 10. BrazilDataAPI

**Fonte:** CRAN / R Package  
**Descrição:** Datasets curados sobre demografia e indicadores de telecomunicações, acessíveis via APIs para consultas em tempo real.

**Características:**
- **Formato:** API/CSV
- **Acesso:** [CRAN Package](https://cran.r-project.org/web/packages/BrazilDataAPI/BrazilDataAPI.pdf)
- **Tipo:** API em tempo real

**Aplicações:**
- Facilita integração para pesquisa em variações estaduais
- Análise de demografia vs. demanda de telecomunicações
- Modelagem regional de demanda

**Limitações:**
- Requer conhecimento de R ou integração de API
- Pode ter limitações de taxa de requisição
- Dados podem estar agregados

**Relevância para Nova Corrente:** ⭐⭐⭐⭐

---

## 📊 Tabela Comparativa de Datasets

| Dataset | Fonte | Características Principais | Formato/Acesso | Aplicações | Limitações |
|---------|-------|----------------------------|----------------|------------|------------|
| **Mobile Phone Accesses** | Anatel/Data Basis | Assinantes, tipos tech, regiões | CSV; data-basis.org | Previsão de demanda para logística 5G | Pode estar defasado |
| **Broadband Customers** | Zenodo | Parâmetros modem, métricas usuário | CSV; zenodo.org/records/10482897 | Modelos preditivos de manutenção | Viés específico de operadora |
| **Data Traffic Forecast** | Internet Aberta | Projeções banda larga/5G, links PIB | PDF/CSV; internetaberta.com.br | Planejamento logístico de longo prazo | Incertezas de forecast |
| **Public Telephones** | GitHub Pages | Uso espacial, tendências | CSV/R; guilhermegch.github.io | Análise de infraestrutura legada | Limitado a telefones públicos |
| **Internet Connectivity Evolution** | Springer | Testes velocidade, dados urbano-rural | CSV; epjdatascience.springeropen.com | Digital divide e logística de cobertura | Possíveis viéses de amostragem |
| **Brazil Telecom Market 2024** | Analysys Mason | KPIs, receita, ARPU | Relatório; analysysmason.com | Market share e estudos de investimento | Restrições de acesso comercial |
| **Telecoms Industry Stats** | Statista | Receita, índices satisfação | Tabelas; statista.com | Benchmarking de demanda de consumidor | Agregado, menos granular |

---

## 🎯 Aplicações Específicas para Nova Corrente

### Previsão de Demanda para Manutenção de Torres

**Datasets Recomendados:**
1. **Mobile Phone Accesses (Anatel)** - Crescimento de assinantes → demanda por upgrades
2. **Broadband Customers (Zenodo)** - Padrões de uso → manutenção preditiva
3. **Data Traffic Forecast** - Planejamento de longo prazo

**Modelos:**
- SARIMAX com variáveis externas (crescimento de assinantes)
- Prophet com sazonalidade (eventos, feriados)
- LSTM para padrões complexos de long-tail

---

### Logística de Peças de Reposição

**Datasets Recomendados:**
1. **Equipment Failure Prediction** - Modela falhas long-tail
2. **Network Fault Prediction** - Severidade de falhas → priorização
3. **Anatel Market Reports** - Dinâmicas de mercado → demanda por hardware

**Modelos:**
- Zero-inflated models para lidar com esparsidade
- Classification models para tipos de falha
- Ensemble methods para hedging de incerteza

---

### Planejamento Espacial de Infraestrutura

**Datasets Recomendados:**
1. **Internet Connectivity Evolution** - Digital divide → áreas prioritárias
2. **OpenCellid Tower Coverage** - Cobertura espacial de torres
3. **Anatel Broadband Data** - Análise municipal/estadual

**Modelos:**
- Spatial regression models
- Geographic clustering
- Coverage optimization algorithms

---

## 🔄 Estratégias de Integração

### 1. Merge Anatel + Ookla para Forecasting Híbrido

**Abordagem:**
- Anatel fornece dados regulatórios oficiais
- Ookla fornece métricas de performance em tempo real
- Combine para forecasting híbrido com menor incerteza

**Implementação:**
```python
# Exemplo de merge
anatel_df = load_anatel_mobile_data()
ookla_df = load_ookla_connectivity_data()

# Merge por região/timestamp
merged_df = pd.merge(
    anatel_df,
    ookla_df,
    on=['region', 'date'],
    how='outer'
)

# Use merged para forecasting com ensemble
```

---

### 2. Hedging de Incertezas com Ensemble Methods

**Abordagem:**
- Combine forecasts de múltiplos datasets
- Use ensemble weighting baseado em incerteza
- Aplique hedging para eventos raros (long-tail)

**Implementação:**
```python
# Ensemble forecasting com hedging
forecasts = {
    'anatel': anatel_forecast,
    'zenodo': zenodo_forecast,
    'internet_aberta': forecast_forecast
}

# Weighted ensemble com incerteza
weights = calculate_uncertainty_weights(forecasts)
ensemble_forecast = weighted_average(forecasts, weights)

# Hedging para long-tail
hedged_forecast = apply_hedging(ensemble_forecast, long_tail_params)
```

---

### 3. Zero-Inflated Models para Long-Tail Demand

**Abordagem:**
- Use zero-inflated models para lidar com esparsidade
- Modelos separados para eventos raros vs. normais
- Combine para forecasting final

**Implementação:**
```python
# Zero-inflated model para long-tail
from statsmodels.discrete.discrete_model import ZeroInflatedPoisson

# Modelo para demandas raras
zip_model = ZeroInflatedPoisson(
    endog=demand_data,
    exog=external_factors,
    exog_infl=zero_inflation_factors
)

# Forecasting com hedging para incerteza
forecast = zip_model.predict(...)
```

---

## ⚠️ Desafios e Limitações

### 1. Qualidade de Dados

**Problemas:**
- Dados da Anatel podem estar defasados
- Datasets acadêmicos podem ter viés específico
- Agregações podem mascarar padrões locais

**Soluções:**
- Verificação cruzada com múltiplas fontes
- Hedging de incerteza com ensemble methods
- Análise de sensibilidade

---

### 2. Integração de Formatos

**Problemas:**
- Formatos variados (CSV, PDF, API)
- Diferentes granularidades temporais
- Agregações geográficas inconsistentes

**Soluções:**
- Pipeline de preprocessing padronizado
- Normalização de granularidades
- Mapeamento de regiões/municípios

---

### 3. Long-Tail Demand

**Problemas:**
- Eventos raros (falhas de equipamento)
- Sparsidade em dados de manutenção
- Incerteza alta em forecasts de long-tail

**Soluções:**
- Zero-inflated models
- Ensemble methods com hedging
- Análise de cenários

---

## 📋 Checklist de Integração

### Fase 1: Preparação
- [ ] Identificar datasets relevantes
- [ ] Verificar acesso e formatos
- [ ] Avaliar qualidade e completude
- [ ] Planejar estratégia de integração

### Fase 2: Download e Preprocessing
- [ ] Download de datasets primários
- [ ] Preprocessing e normalização
- [ ] Mapeamento de colunas para schema unificado
- [ ] Validação de qualidade

### Fase 3: Integração
- [ ] Merge de datasets complementares
- [ ] Criação de features derivadas
- [ ] Validação de consistência
- [ ] Documentação de transformações

### Fase 4: Modelagem
- [ ] Feature engineering específico
- [ ] Treinamento de modelos base
- [ ] Ensemble methods
- [ ] Validação e avaliação

---

## 🔗 Links e Referências

### Fontes Primárias

- [Data Basis - Mobile Accesses](https://data-basis.org/dataset/d3c86a88-d9a4-4c0-bdec-08ab61e8f63c)
- [Teleco - Mobile Statistics](https://www.teleco.com.br/en/en_ncel.asp)
- [Net Data Directory - Broadband](https://netdatadirectory.org/node/2336)
- [Zenodo - Broadband Customers](https://zenodo.org/records/10482897)
- [Internet Aberta - Traffic Forecast](https://internetaberta.com.br/wp-content/uploads/2024/05/Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf)
- [Springer - Digital Divide](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-024-00508-8)

### Relatórios e Análises

- [Analysys Mason - Brazil Report](https://www.analysysmason.com/research/content/country-reports/brazil-country-report-rddj0/)
- [Statista - Telecom Statistics](https://www.statista.com/topics/7187/telecommunications-in-brazil/)
- [CRAN - BrazilDataAPI](https://cran.r-project.org/web/packages/BrazilDataAPI/BrazilDataAPI.pdf)

---

## ✅ Próximos Passos

1. **Priorizar Datasets:** Começar com Anatel Mobile + Zenodo Broadband
2. **Criar Integrations:** Implementar downloaders para cada fonte
3. **Preprocessing:** Adaptar pipeline para formatos brasileiros
4. **Feature Engineering:** Criar features específicas para contexto brasileiro
5. **Modelagem:** Treinar modelos com dados brasileiros integrados

---

**Status:** 📚 **DOCUMENTAÇÃO COMPLETA - Pronto para Integração**

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

