# 📘 Blueprint Consolidado de Rollout ML – Nova Corrente

## 1. Visão Executiva
Síntese do desafio B2B descrito em `Solucao-Completa-Resumida-Final.md` e `STRATEGIC_BUSINESS_PROBLEM_SETUP_PT_BR.md`: a Nova Corrente precisa reduzir rupturas de estoque em 60%, otimizar capital de giro em 20% e manter SLA ≥ 99% para contratos multimilionários com operadoras e tower companies. O pipeline automatizado já entrega dados enriquecidos; falta concluir a modelagem preditiva/prescritiva, consolidar governança e publicar narrativas executivas. O target financeiro continua sendo ROI de 80-180% com payback < 12 meses.

## 2. Referenciais e Documentos Base
Este blueprint orquestra oito pilares documentais:
- `MARKET_ANALYSIS_INDUSTRY_WISDOM_PT_BR.md`: métricas de mercado, padrões sazonais, fatores externos críticos.
- `EXTERNAL_FACTORS_ML_MODELING_PT_BR.md`: catálogo de variáveis macro/climáticas/logísticas, design de features e escolhas de modelos (Prophet/ARIMAX/LSTM/TFT).
- `NOVA_CORRENTE_ENRICHMENT_COMPLETE.md`: resultado de 44 novas features (SLA, clima Salvador, 5G, logística, contratos).
- `NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md`: inventário, gaps de cobertura (<25%), recomendações de backfill.
- `NOVA_CORRENTE_ML_STRATEGY_PLAN.md`: roadmap interno (fases 5.1-5.5), governança e artefatos a atualizar.
- `STRATEGIC_BUSINESS_PROBLEM_SETUP_PT_BR.md` + `Solucao-Completa-Resumida-Final.md`: objetivos estratégicos, KPIs e narrativa para stakeholders.
- `docs/pipeline/*` + `complete_pipeline_push.py`/`finalize_pipeline.py`: execução fim-a-fim e produção de documentação operacional.

## 3. Inventário de Dados e Cobertura Atual
1. **Landing / Bronze (`data/raw/`)**  
   - APIs automatizadas (BACEN, IBGE, ANP, World Bank, Freight blockers) e fontes fallback.  
   - Scripts: `scripts/etl/external/*.py`, `scripts/automation/freight_blockers/*.py`.  
   - Metadados: `complete_pipeline_push.py` registra ingestões, erros e tamanhos.

2. **Silver (`data/silver/`)**  
   - Normalização por domínio: `macro`, `logistics`, `freight`, `climate`.  
   - Freight blockers geram `xeneta_xsi_c.parquet`, `drewry_wci_alternatives.parquet`, `antt_logistics_kpis.parquet`.  
   - Validações: `scripts/etl/transform/validation/logistics_dataset_checks.py`, relatórios de `complete_pipeline_push.py`.  
   - Cobertura atual (último run 2025-11-11): 23 tabelas, 75.189 registros, 3 alertas de qualidade (tabelas vazias e null rate alto).  
   - Gap-chave: séries climáticas (INMET) e World Bank GDP ainda com 0 registros (prioridade para 5.1 Backfill).

3. **Gold / Feature Store (`data/warehouse/gold/<ts>/`, `data/feature_store/`)**  
   - `build_gold_layer.py` produz features por domínio (econômico, logístico, eventos).  
   - `activate_gold_layer.py` concatena features, normaliza datas, gera dataset mestre.  
   - `data/outputs/nova_corrente/` contém forecasts/parâmetros prescritivos mais recentes, com relatórios e métricas.

4. **Documentação e Inventário (`docs/pipeline/`)**  
   - `finalize_pipeline.py` gera: inventário de dados, arquitetura, catálogo de features, guia ML, manual operacional, resumo executivo.  
   - `COMPLETE_PIPELINE_REPORT.json` consolida status e métricas de cada execução completa.

## 4. Modelo Relacional e Camadas
### 4.1 Estrutura em Camadas
- **Bronze (Landing):** tabelas brutas por fonte com timestamp de ingestão. Mantêm schema original para auditoria.  
- **Silver:** padroniza chaves temporais (`date`, `region`, `currency`, `sku_id`), aplica tipos numéricos, remove duplicidades.  
- **Feature / Gold:** promove agregações diárias/mensais, cria lags, rolling windows, indicadores compostos.  
- **Outputs Analíticos:** forecasts, cenários, safety stock, reorder points, relatórios de risco.

### 4.2 Modelo Dimensional
- **Fato `FactDemand`** (base Nova Corrente)  
  - Chaves: `date`, `family`, `sku_id`, `site_id`, `client_id`.  
  - Métricas: `quantity`, `lead_time_days`, `cost`.  
  - Fonte: dataset enriquecido (`unified_brazilian_telecom_nova_corrente_enriched.csv`).

- **Dimensões Externas**  
  - `DimMacroEconomics`: PTAX (`buy_rate`, `sell_rate`), SELIC (`selic_rate`), IPCA (`ipca_index`).  
  - `DimLogistics`: Freight rates alternativos, ANP fuel, ANTT KPIs, Baltic Dry.  
  - `DimClimate`: Temperatura, precipitação, umidade, vento (INMET/OpenMeteo).  
  - `DimTechnology`: Cobertura 5G, migração fibra, upgrades ANATEL.  
  - `DimOperations`: SLA cycles, feriados nacionais/regionais, greves, backlog/SLAs internos.

- **Tabelas de Relacionamento**  
  - `Bridge_FactDemand_External`: join diário por `date` + `region`/`currency`/`client_tier`.  
  - `Bridge_Forecast_Prescriptive`: armazena forecasts, intervalos, recomendações e cálculo de estoque seguro por item/cliente/família.

### 4.3 Governança de Schema
- `complete_pipeline_push.py` valida schemas esperados antes de promover arquivos para Silver/Gold.  
- `build_external_features.py` aplica renomeações (`cotacaoCompra` → `buy_rate`, `ipca` → `ipca_mom`) garantindo consistência com o modelo.  
- Futuro: implementar **`schema_registry.json`** para versionar colunas obrigatórias e sinalizar breaking changes ao Airflow.

## 5. Arquitetura de Pipeline ML
1. **Orquestração**  
   - Airflow DAG `nova_corrente_external_etl.py` agenda ingestões diárias/mensais.  
   - CLI principal: `python -m scripts.etl.transform.complete_pipeline_push` (executa ingestão → silver → gold → validações → documentação).  
   - CI/CD: pipeline inclui `fetch_all.py` e `transform_all()` com flag para freight blockers.

2. **Transformações**  
   - `external_to_silver.py` chama `FreightBlockersETLStep.execute()` antes de validações de logística.  
   - Validações automáticas registram alertas `WARN` ASCII-safe e interrompem pipeline se arquivos críticos estiverem ausentes.

3. **Feature Engineering**  
   - `build_external_features.py` gera dataset macro/logístico unificado com lags (1/7/30/90d), volatilidades, correlações.  
   - `build_gold_layer.py` cria features temáticos (econômicos, logística, eventos) e salva em `data/warehouse/gold/<ts>`.  
   - `activate_gold_layer.py` concatena, trata data duplication, aplica `ffill()` e gera dataset ML-ready.

4. **Modelagem**  
   - `run_training_pipeline.py` (baseline) + `scripts/analysis/*` para exploratory/prescriptive.  
   - Model stack (Prophet, ARIMAX, LSTM, TFT) com ensemble ponderado conforme volatilidade (`EXTERNAL_FACTORS_ML_MODELING_PT_BR.md`).  
   - Optional deps: `pmdarima`, `tensorflow`, `xgboost` (GPU opcional). Documentar fallback para rodar somente Prophet/ARIMAX.

5. **Prescrição**  
   - `complete_pipeline_push.py` recalcula safety stock (`SS = Z * σ_demand * sqrt(lead_time)`) e ROP (`daily_avg * lead_time + SS`).  
   - `NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md` deve ser atualizado com novas tabelas (safety stock, ROP, ROI).

6. **Documentação & Storytelling**  
   - `finalize_pipeline.py` gera docs markdown (inventário, arquitetura, catálogo) e JSON de resumo.  
   - Este blueprint unifica referências para equipe de dados, ciência, finanças e operações.

## 6. Estratégia de Modelagem e Orquestração
1. **Segmentação de Itens** (`EXTERNAL_FACTORS_ML_MODELING_PT_BR.md`, `Solucao-Completa-Resumida-Final.md`)  
   - **Fast-moving (conectores):** Prophet com regressors (temperatura, chuva, câmbio, feriados).  
   - **Slow-moving (equipamentos RF, estruturas):** ARIMAX com exógenas macro/logística.  
   - **Multifatores (famílias críticas):** Ensemble Prophet + LSTM/TFT para capturar não-linearidades.  
   - **Eventos extremos:** modelos de previsão de risco (storm_economy, holiday_inflation).

2. **Processo de Treino**  
   - Split temporal (TimeSeriesSplit n=5).  
   - Métricas comparativas MAPE/RMSE/MAE + métricas de negócio (stockout prevention).  
   - MLflow (planejado) para versionamento de modelos e monitoramento.

3. **Orquestração Operacional**  
   - Agendar re-treinos semanais ou disparados por drift (PSI > 0.2).  
   - Airflow: tasks específicas (`train_models`, `update_prescriptive`) após `activate_gold_layer`.  
   - Logging centralizado `logs/pipeline/metrics/` com resumo por execução.

4. **Fallbacks & Resiliência**  
   - Caso dependências avançadas indisponíveis, fallback para ARIMAX/XGBoost e prescrição determinística.  
   - Prophet é desativado automaticamente quando CmdStan falha; registrar instalação futura ou manter fallback registrado.  
   - Documentar no runbook como habilitar GPU (TensorFlow) e bibliotecas opcionais.

## 7. Validação, KPIs e Monitoramento
1. **Precisão de Previsão**  
   - Targets: MAPE < 15%, RMSE relativo ≤ 0.2 * média demanda, Bias próximo de 0.  
   - Monitoramento contínuo: `metrics_summary.json` deve registrar métricas por família/SKU a cada run.

2. **KPIs de Negócio** (`MARKET_ANALYSIS_INDUSTRY_WISDOM_PT_BR.md`, `STRATEGIC_BUSINESS_PROBLEM_SETUP_PT_BR.md`)  
   - Stockout Prevention Rate ≥ 80%.  
   - Capital Savings 15-20% (estoque médio).  
   - Disponibilidade SLA (>99%) e MTTR < 4h.  
   - Inventory Turnover alvo 6-12x/ano por categoria.

3. **Qualidade de Dados**  
   - Alertas automáticos para tabelas vazias/null rate > 30% (corrigir antes de promover para Gold).  
   - Checklist de retroalimentação para times responsáveis (ENG coleta, DS modelagem, Finanças ROI, Operações SLA).

4. **Monitoramento Contínuo**  
   - Dashboards de controle: pipelines (Airflow), qualidade (logs/pipeline/validation), métricas (Grafana/Metabase).  
   - Automação de alertas (email/Teams) quando KPIs fora do limite.

## 8. Roadmap Final e Backlog
### Fase 5.1 – Backfill Histórico & Alinhamento de Features
- Reprocessar datasets externos (`data/raw/archives`) para cobrir ≥730 dias.  
- Atualizar `FactDemand` com dados históricos (meses/anos anteriores) via scripts de reidratação.  
- Rerrodar `build_warehouse.py`, atualizar `NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md` com nova cobertura.

### Fase 5.2 – Calibração de Política de Estoque
- Extrair estatísticas de demanda/lead-time da nova base Gold.  
- Atualizar `pp_calculator.py` (ou módulo equivalente) com service levels por família cliente-tier.  
- Revisar `NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md` com tabelas de SS/ROP, recomendações e finance addendum.

### Fase 5.3 – ROI & Finance Alignment
- Construir workbook/markdown com cenários (melhor/base/pior) e drivers (penalidade SLA, capital de giro).  
- Integrar resultados ao `ML_PIPELINE_TECH_SPEC.md` e runbook financeiro.

### Fase 5.4 – Hardening & Monitoramento
- Definir postura de dependências opcionais (instalar pmdarima/TensorFlow?); atualizar `environment.local.yml`.  
- Ampliar `metrics_summary.json`, implementar logging diferenciado para fallback vs. full.  
- Garantir que `run_batch_cycle.py` distingue execuções baseline/full e registrá-las em `logs/pipeline/runs.csv`.

### Fase 5.5 – Piloto e Storytelling
- Selecionar família `FERRO E AÇO` (alto risco macro) para piloto.  
- Rodar comparativo baseline vs. novo pipeline (forecast + prescrição + ROI).  
- Criação de relatório para stakeholders e plano de rollout fase 1.

### Resumo de Backlog, Métricas e Responsáveis
| Macro-Atividade | Time Líder | Dependências | KPI de Saída | Entregável |
|-----------------|------------|--------------|--------------|------------|
| Backfill histórico (5.1) | Engenharia de Dados | Arquivos arquivados, scripts `build_warehouse.py` | Cobertura externa ≥ 60%, 730 dias úteis | Nova snapshot em `data/warehouse/gold`, atualização enrichment report |
| Revisão política estoque (5.2) | Data Science + Operações | Gold atualizado, estatísticas de demanda | SS/ROP recalculados, redução ≥20% estoque | `NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md` v2 + JSON prescritivo |
| ROI e finanças (5.3) | Finance + Data Science | Saída prescritiva, custos atualizados | ROI documentado por cenário, payback < 12 meses | Addendum financeiro + atualização `ML_STRATEGY_PLAN` |
| Hardening pipeline (5.4) | MLOps | Decisão deps opcionais, logs | Pipeline full sem warnings críticos, métricas registradas | `environment.local.yml`, `metrics_summary.json`, runbook |
| Piloto + storytelling (5.5) | Analytics Lead + Operações | Atividades 5.1-5.4 concluídas | Aprovação stakeholders, MAPE piloto < 15% | Relatório piloto, dashboards publicados, plano rollout fase 1 |

## 9. Riscos, Suposições e Mitigações
- **Cobertura Externa Insuficiente:** Backfill e forward-fill documentado (Fase 5.1). Fallbacks (World Bank) já implementados.  
- **Dependências Técnicas:** Documentar requisitos opcionais e preparar contêiner/conda com GPU quando disponível.  
  - CmdStan/Prophet ausente: pipeline ativa apenas ARIMAX/XGBoost; instalar `prophet` com backend Stan ou manter fallback.  
- **Data Drift:** Implementar rotina de monitoramento com alarmes PSI/KS e agendamento de re-treino.  
- **Mudanças de Processo Operacional:** Necessidade de alinhar com times de compras e operações para adoção do PP automatizado.  
- **Segurança e Governança:** Garantir que credenciais (API keys) estão rotacionadas e logs não armazenam dados sensíveis.

## 10. Plano de Data Storytelling e Entregáveis Finais
1. **Dashboards**  
   - Grafana/Metabase com: demanda prevista vs. realizada, estoque vs. PP, risco de ruptura, KPIs financeiros.  
   - Painel executivo destacando ROI, stockouts evitados, impacto em SLA.

2. **Front-end Narrativo**  
   - Storytelling inspirado em `Solucao-Completa-Resumida-Final.md`: problema → solução → resultados esperados.  
   - Visualizações por cenário (otimista/base/pessimista) e por família de itens.

3. **Publicação & Workflow**  
   - Pipeline gera datasets → `data/outputs/nova_corrente/forecasts/*.parquet/json`.  
   - Camada de API/notebook serve dashboards e relatórios PDF/Markdown.  
   - Ciclo semanal de revisão com Operações/Compras/Finanças para validação das recomendações.

4. **Próximos Entregáveis Documentais**  
   - Atualizar briefs (`PRESCRIPTIVE`, `EXPLORATORY`), runbook (`BATCH_RUNBOOK.md`) e este blueprint após fases 5.1-5.5.  
   - Adicionar apêndice com glossário de variáveis e mapeamento de dashboards.



