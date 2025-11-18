# Nova Corrente Knowledge Index

## Navigation

- [Nova Corrente Telecom Enrichment Report](NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md) — visão executiva da estratégia de enriquecimento brasileiro
- [Nova Corrente B2B Enrichment Complete](../archives/reports/datasets/2025/2025-11-01/NOVA_CORRENTE_ENRICHMENT_COMPLETE.md) — ETL + feature catalogue
- [Nova Corrente Exploratory Analysis](NOVA_CORRENTE_EXPLORATORY_ANALYSIS.md) — diagnóstico de dados e correlações
- [Nova Corrente Prescriptive Brief](NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md) — risco operacional e sensibilidade macro
- [Relatório Final de Performance (PT-BR)](../../data/outputs/nova_corrente/optimized/FINAL_PERFORMANCE_REPORT_PT_BR.md) — comparação baseline vs otimizado
- [Nova Corrente Exploratory Summaries (`data/outputs/analysis/`)](../../data/outputs/analysis/) — tabelas diárias/mensais, correlações e métricas derivadas
- [Nova Corrente Risk Tables (`data/outputs/analysis/`)](../../data/outputs/analysis/nova_corrente_family_risk.csv) — ranking de risco por família exportado em CSV
- [External Factors & ML Modeling Guide](../proj/strategy/EXTERNAL_FACTORS_ML_MODELING_PT_BR.md) — referência expandida de fatores exógenos
- [Nova Corrente ML Technical Note](../mathematics/NOVA_CORRENTE_ML_TECHNICAL_NOTE.md) — fórmulas, métricas e resultados detalhados
- [Nova Corrente Note Index (PT-BR)](NOVA_CORRENTE_NOTE_INDEX.md) — índice completo e briefs rápidos

## Contexto do Repositório

- **Fluxo completo:** dados crus (`dadosSuprimentos.xlsx`) → enriquecimento (`run_nova_corrente_enrichment.py`) → análises exploratória/prescritiva → avaliação de modelos → relatórios.
- **Feature store:** artefatos consolidados residem em `data/processed/*` e alimentam scripts analíticos sob `scripts/analysis/`.
- **Stack principal:** Python (pandas, statsmodels, prophet, xgboost), TensorFlow (experimentos LSTM), automação planejada com Airflow/Prefect.

## Quick Briefs

### Nova Corrente Telecom Enrichment Report

- **Objetivo:** Consolidar a busca de datasets brasileiros, estratégias de junção e resultados (exploratório + prescritivo).
- **Conteúdo-chave:** inventário dos 5 datasets principais (macro, operadoras, IoT, fibra, Anatel), pipeline de integração, achados e recomendações estratégicas.
- **Artefatos gerados:** `scripts/analysis/run_nova_corrente_exploratory.py`, `scripts/analysis/run_nova_corrente_prescriptive.py`, tabelas em `data/outputs/analysis/`.
- **Insights fundamentais:** correlação de inflação (-0.42) e PIB (+0.39) com demanda, missingness de clima/regulatório >96%, riscos compostos destacados para famílias de maior criticidade.
- **Complementos:** integra-se aos relatórios exploratório/prescritivo e estabelece pré-requisitos para feature store e modelos intermitentes (Croston/SBA).
- **Próximos passos destacados:** backfill de macro/clima, parse completo de Anatel, criação da feature store, experimentos Croston/SBA e modelos bayesianos.

### Nova Corrente B2B Enrichment Complete

- **Objetivo:** Documenta o enriquecimento do dataset com 44 novas colunas cobrindo SLA, clima de Salvador, expansão 5G, logística de importação, localização de torres e contratos B2B.
- **Outputs-chave:** `data/processed/unified_brazilian_telecom_nova_corrente_enriched.csv`, `data/processed/nova_corrente_enrichment_summary.json`.
- **Highlights:** Cobertura climática costeira detalhada, multiplicadores de demanda 5G de até 3x, atraso crítico de importação >25 dias, penalidades SLA até R$ 30 milhões.
- **Próximos passos principais:** Treinar modelos com fatores específicos, validar penalidades SLA, testar forecasting completo.
- **Notas técnicas:**
  - **Pipeline:** ingestão `unified_brazilian_telecom_ml_ready.csv` → joins com clima (INMET/OpenWeather), macro (BACEN/IBGE), 5G (ANATEL), logística (customs/strikes) e contratos → validação de consistência via `external_factors_log.txt`.
  - **Transformações chave:** cálculo `lead_time_multiplier = base_lead_time_days × seasonal_factor × strike_multiplier`, `demand_multiplier_5g = 1 + (new_5g_cities/total_municipalities) × 3`.
  - **Qualidade:** regras de missingness (threshold 5%) e outlier winsorization aplicadas antes da exportação.
  - **Infra:** scripts previstos `scripts/engineering/merge_external_factors.py` (WIP) e automação futura com Prefect (pipeline `flow_nova_corrente_enrichment`).
  - **Relacionamentos:** serve como base para `NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md` e alimenta o feature store planejado (`data/processed/feature_store_daily.parquet`).

### Nova Corrente Prescriptive Brief

- **Objetivo:** Prioriza famílias por risco composto combinando volatilidade de demanda, lead time e sensibilidade macro.
- **Indicadores:** SUPRIMENTOS ADMINISTRATIVO lidera risco (0.55 CV 4.88); Corretiva TBSA com lead time médio 32 dias; MATERIAL ELÉTRICO com alta volatilidade e lead >15 dias.
- **Ações recomendadas:** Ajustar estoque dinâmico, negociar SLAs acelerados, alinhar forecasts a cenários macroeconômicos.
- **Gaps sinalizados:** Cobertura limitada de fatores externos, necessidade de parsing de dados Anatel e loja de features persistente.
- **Notas técnicas:**
  - **Modelo de risco:** `risco_composto = 0.4 × CV_demand + 0.35 × lead_time_normalizado + 0.25 × sensibilidade_macro`, calibrado via `scripts/analysis/run_nova_corrente_prescriptive.py`.
  - **Sensibilidade macro:** regressões OLS por família (`y = β0 + β1 GDP + β2 FX + β3 inflação + ε`), com alertas quando `n_obs < 12`.
  - **Operacionalização:** recomendações mapeadas a playbooks (`docs/ops/playbooks/inventory_hedging.md`, `docs/ops/playbooks/supplier_escalation.md`) e thresholds (`lead_time > 15d` ⇒ SLA renegotiation).
  - **Próxima evolução:** incorporar variáveis de SLA (`sla_penalty_brl`, `availability_actual`) e priorizar famílias para modelos Croston/SBA (ver `docs/mathematics/NOVA_CORRENTE_ML_TECHNICAL_NOTE.md` seção 7).

### Relatório Final de Performance (PT-BR)

- **Objetivo:** Compara pipeline baseline vs otimizado para cinco famílias priorizadas.
- **Status:** Pipeline end-to-end concluído (imputação 100%, normalização RobustScaler, seleção de 30+ features). Melhor MAPE atual 87.27% (família EPI).
- **Destaques de melhoria:** 73 features geradas, modelos baseline treinados, progresso documentado em oito scripts e múltiplos datasets.
- **Pendências críticas:** Reduzir MAPE para <15%, corrigir features faltantes, treinar modelos avançados (XGBoost, ensembles), validar em conjunto de teste.
- **Notas técnicas:**
  - **Pipeline:** `preprocess_data` (imputação KNN/interp), `engineer_features` (lags 1/7/30/365, médias móveis, interações clima×macro), `select_features` (mutual information/top-k), `train_baselines`.
  - **Configuração:** partições temporais 64/16/20 (train/val/test), escalonamento com `RobustScaler`, eliminação de features com `missing_pct > 60%`.
  - **Modelos avaliados:** Naive, média móvel (k=7), mediana, tendência linear, ARIMA(1,1,1), XGBoost (`eta=0.1`, `max_depth=4`, `n_estimators=200`), ensemble ponderado (0.4 median, 0.3 naive, 0.3 moving average).
  - **Roadmap de otimização:** grid Optuna (`learning_rate`, `max_depth`, `subsample`), introdução de Prophet + regressors externos, experimentos LSTM (`timesteps=30`, `features=86`), validação cruzada temporal (`TimeSeriesSplit` com 5 folds).

### Nova Corrente Exploratory Analysis

- **Objetivo:** Diagnosticar cobertura de dados e correlações com fatores externos.
- **Cobertura temporal:** 380 dias (2024-10-09 a 2025-10-24) com 4.188 linhas, 20 famílias, 872 itens.
- **Insights:** Ausência de cobertura densa para clima e macro diários (>96% missing), correlação positiva de demanda com câmbio e precipitação, necessidade de backfill de métricas mensais (acessos, IoT, penetração residencial).
- **Próximos passos:** Ingerir sinais externos completos, substituir valores sintéticos de fibra, preparar feature store para experimentos prescritivos.
- **Notas técnicas:**
  - **Junções:** fact table `fact_nova_corrente_daily` ligada a tabelas externas (`macro_daily.csv`, `weather_salvador.csv`, `anatel_5g_municipal.csv`) via chaves `date`, `region`, `client`.
  - **Diagnósticos:** matriz de correlação (Spearman) destaca `exchange_rate_brl_usd` (ρ=0.115) e `precipitation_mm` (ρ=0.063) com demanda; cobertura efetiva 10% → sinal de viés.
  - **Qualidade:** relatório `data/processed/data_quality_report.json` sinaliza `sla_violation_risk`, `temperature_avg_c` com 96.3% missing ⇒ ação `backfill_external_sources`.
  - **Planejamento:** backlog `docs/proj/Roadmap-Completo-Nova-Corrente-Mermaid.md` define extração de histórico Anatel (>24 meses), integração OpenWeather API (`fetch_climate_data()`), criação de feature store (`feature_store_daily.parquet`).
  - **Outputs derivados:** `data/outputs/analysis/nova_corrente_daily_summary.csv`, `nova_corrente_daily_with_context.csv`, `nova_corrente_monthly_with_context.csv`.

### Nova Corrente Prescriptive Brief

- **Objetivo:** Prioriza famílias por risco composto combinando volatilidade de demanda, lead time e sensibilidade macro.
- **Indicadores principais:** SUPRIMENTOS ADMINISTRATIVO (risco 0.55), Corretiva TBSA (lead 32 dias, 100% pedidos >21 dias), MATERIAL ELETRICO (volatilidade + lead >15 dias), FERRO E AÇO (sensibilidade altas a PIB/FX).
- **Recomendações:** Estoque dinâmico, renegociação de SLA, vinculação de forecast a cenários macro, escalonamento de fornecedores.
- **Gaps sinalizados:** Cobertura limitada de fatores externos (necessidade de backfill Anatel e clima), criação da feature store, priorização de modelos Croston/SBA.
- **Notas técnicas adicionais:**
  - **Cálculo de risco:** `composite_risk = 0.4 * cv_score + 0.3 * lead_time_score + 0.2 * high_lead_time_score + 0.1 * macro_score`.
  - **Sensibilidade macro:** matriz `data/outputs/analysis/nova_corrente_family_macro_corr.csv` com correlações e `n_obs` para controle de confiabilidade.
  - **Artefatos auxiliares:** `data/outputs/analysis/nova_corrente_family_risk.csv`, relatório narrativo `docs/reports/NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md`.

### Scripts e Automação

- `scripts/analysis/run_nova_corrente_exploratory.py` — gera sumários diários/mensais, junções com macro/operadora/IoT/fibra e relatório exploratório.
- `scripts/analysis/run_nova_corrente_prescriptive.py` — calcula pontuação de risco por família, correlações macro e recomendações prescritivas.
- `scripts/analysis/run_nova_corrente_performance.py` (em andamento) — consolida métricas de treino/val/test e comparações baseline vs otimização.
- `scripts/engineering/merge_external_factors.py` (WIP) — pipeline planejado para unificar fatores externos em um feature store.
- `scripts/orchestration/flow_nova_corrente_enrichment.py` (futuro) — orquestração Prefect/Airflow para automação diária.
- `scripts/orchestration/flow_nova_corrente_monitoring.py` (planejado) — monitoramento diário de qualidade e alertas de missingness.
- `notebooks/analysis/nova_corrente_feature_store.ipynb` (to-do) — validação visual de features agregadas para experimentos Croston/SBA.

### Integração com Planejamento Estratégico

- **Roadmap:** `docs/proj/strategy/STRATEGIC_TECHNICAL_DEEP_DIVE_PT_BR.md` e `docs/proj/Roadmap-Completo-Nova-Corrente-Mermaid.md` mapeiam fases de ingestão e automação.
- **Playbooks operacionais:** `docs/ops/playbooks/inventory_hedging.md`, `docs/ops/playbooks/supplier_escalation.md` conectam recomendações de risco a ações tangíveis.
- **Matemática e modelos:** `docs/mathematics/NOVA_CORRENTE_ML_TECHNICAL_NOTE.md` sustenta fórmulas (MAPE, Croston, ARIMA, XGBoost), enquanto `docs/mathematics/MATH_ADVANCED_FORMULAS.md` amplia derivadas e probabilidades.
- **Dados complementares:** `docs/proj/strategy/EXTERNAL_FACTORS_ML_MODELING_PT_BR.md` fornece catálogo detalhado de fatores exógenos e integrações API.

## Referências e Artefatos Relacionados

- **Scripts:** `scripts/analysis/run_nova_corrente_exploratory.py`, `scripts/analysis/run_nova_corrente_prescriptive.py`, `scripts/analysis/run_nova_corrente_performance.py`.
- **Documentação:** `docs/mathematics/NOVA_CORRENTE_ML_TECHNICAL_NOTE.md`, `docs/proj/strategy/EXTERNAL_FACTORS_ML_MODELING_PT_BR.md`, `docs/proj/Roadmap-Completo-Nova-Corrente-Mermaid.md`.
- **Datasets:** `data/processed/unified_brazilian_telecom_ml_ready.csv`, `data/processed/unified_brazilian_telecom_nova_corrente_enriched.csv`, `data/processed/feature_store_daily.parquet` (planejado).
- **Logs & métricas:** `data/processed/external_factors_log.txt`, `data/processed/model_training_metrics.json`, `data/processed/data_quality_report.json`.
