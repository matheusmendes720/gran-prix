---
title: "Nova Corrente ML Strategy Plan – Internal Data Track"
date: "2025-11-11"
authors:
  - Nova Corrente Data & Analytics
status: "Accepted Plan"
---

# 0. Purpose

Provide a consolidated, step-by-step ML strategy that leverages the **existing enriched Nova Corrente dataset** without introducing new external fetches. This plan synthesises the current diagnostics (`NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md`, `NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md`, `NOVA_CORRENTE_ENRICHMENT_COMPLETE.md`, `chat-Time Series Data Modeling.txt`) and the operational batch pipeline to define the next phases required to maximise predictive and prescriptive accuracy, veracity, and reliability.


# 1. Current State Summary

| Domain | Key Artifacts | Highlights | Risks / Gaps |
|--------|---------------|-----------|--------------|
| Enriched Dataset | `data/processed/unified_brazilian_telecom_nova_corrente_enriched.csv`<br>`docs/archives/reports/datasets/2025/2025-11-01/NOVA_CORRENTE_ENRICHMENT_COMPLETE.md` | 2,880 records × 74 columns (44 added features). Backfill complementar 2019-01-01→2024-10-08 disponível em `nova_corrente_fact_backfill.parquet`. | Necessário promover backfill ao fact principal para cobrir análises futuras (fase 5.1 concluída). |
| Exploratory Diagnostics | `docs/reports/NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md` | Daily/monthly enriched joins, correlation matrices, risk identification, missingness mapping | External factors overlap <25% of fact timeline; weather/regulatory gaps ≥96% |
| Prescriptive Outputs | `docs/reports/NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md` | Composite risk ranking, macro sensitivities, actionable mitigations | Safety stock & reorder calculations flagged for inflation; risk scores saturate at 100% |
| ML Pipeline | `docs/reports/NOVA_CORRENTE_ML_PIPELINE_TECH_SPEC.md`<br>`scripts/run_batch_cycle.py` | Pipeline reexecutado em 2025-11-11: backfill incorporado, snapshot `gold/20251111T164236`, forecasts/prescrições para 15 séries (ARIMA + XGBoost; Prophet desativado por padrão). | CmdStan/TensorFlow ausentes; `metrics.json/summary` vazios e LSTM indisponível até instalar dependências opcionais. |
| Dimensional/Time-Series Strategy | `docs/proj/scafold/extern_modeling/chat-Time Series Data Modeling.txt` | Guidance for timeline extension, feature engineering, partitioning, model selection, validation | Requires execution of historical extension via existing sub-datasets; not yet actioned |


# 2. Strategic Objectives (Internal Data Focus)

1. **Stabilise Forecasting Accuracy** – Reach telecom benchmark (MAPE ≤ 15%) using enriched internal/external factors already available locally.
2. **Validate Prescriptive Reliability** – Recompute safety stock, reorder points, and risk scores with transparent formulas aligned to the enriched features.
3. **Document Finance & Operations Alignment** – Build auditable ROI and inventory policy narratives using current outputs.
4. **Stage for Historical Extension** – Use archived enrichment tables to backfill fact timelines before any new API fetch.


# 3. Data Assets & Cross-References

| Asset | Location | Role in Plan |
|-------|----------|--------------|
| Enriched master dataset | `data/processed/unified_brazilian_telecom_nova_corrente_enriched.csv` | Primary training/validation source (74 features). |
| Enrichment summary | `docs/archives/reports/datasets/2025/2025-11-01/NOVA_CORRENTE_ENRICHMENT_COMPLETE.md` | Feature catalogue & business impacts (SLA penalties, climate, 5G, logistics, contracts). |
| Exploratory report | `docs/reports/NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md` | Coverage analysis, missingness diagnostics, correlation matrices. |
| Prescriptive brief | `docs/reports/NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md` | Current risk rankings, recommendations, macro sensitivity tables. |
| ML pipeline spec | `docs/reports/NOVA_CORRENTE_ML_PIPELINE_TECH_SPEC.md` | Architecture, validation, limitations, runbook references. |
| Time-series modelling strategy | `docs/proj/scafold/extern_modeling/chat-Time Series Data Modeling.txt` | Detailed guidance on timeline extension, feature engineering, partitioning, CV. |
| Batch outputs | `data/warehouse/gold/20251111T164236/`<br>`data/outputs/nova_corrente/forecasts/` | Latest gold snapshot, features, forecasts, prescriptive JSON, metrics summary. |
| Scripts | `scripts/run_batch_cycle.py`<br>`scripts/run_training_pipeline.py`<br>`scripts/build_warehouse.py`<br>`scripts/analysis/run_nova_corrente_exploratory.py`<br>`scripts/analysis/run_nova_corrente_prescriptive.py` | Execution entry points for batch, modelling, diagnostics. |


# 4. Diagnosis → Strategy Mapping

| Diagnosis (source) | Strategic Response | Reference |
|--------------------|-------------------|-----------|
| Fact timeline ≈380 days causes under-fitting and high MAPE (enrichment report, time-series chat) | Backfill historical demand using archived enrichment tables; create multi-year surrogate timelines before new APIs | §5.1 |
| External factors overlap <25% despite enriched features (telecom enrichment report) | Align enriched tables with fact timeline (resample/forward-fill using documented business rules) | §5.1 |
| Safety stock & ROP inflated; risk scores 100% (prescriptive brief) | Rebuild inventory policy calculator with enriched features (lead-time sigma, service levels, demand volatility) | §5.2 |
| ROI claim lacks supporting drivers (critique summary) | Construct finance model using enriched outputs (stockout cost, holding cost, service improvements) | §5.3 |
| Pipeline fallbacks produce warnings but succeed (tech spec) | Decide optional dependency posture; adjust model ensemble weights and logging | §5.4 |
| Need pilot validation before rollout (critique summary, time-series chat) | Define Phase 0 pilot using enriched dataset only; simulate policy impact | §5.5 |


# 5. Next-Phase Roadmap (Internal Data Only)

## 5.1 Historical Backfill & Feature Alignment *(status: executado em 2025-11-11)*

- **Objective:** Extend effective modelling horizon to ≥730 days using existing enriched sub-datasets (macro, climate, 5G, logistics, contract factors).
- **Actions:**
  1. Compile archived enrichment tables (see `_ENRICHMENT_COMPLETE.md` references) into a **historical surrogate fact table** by stitching months/quarters prior to the current 380-day window.
  2. Apply the time-series blueprint in `chat-Time Series Data Modeling.txt`:
     - Partition ingestion (historical backfill vs. recent stream).
     - Ensure dimensions (e.g., `DimExternalFactors`) include future projection columns for inference.
     - Generate lag/rolling features at 1/7/30/90/183/365 day windows (matching guidance).
  3. Rehydrate the Gold snapshot (`scripts/build_warehouse.py`) using the extended timeline; persist to `data/warehouse/gold/<new_ts>/`.
  4. Document data quality deltas (coverage, missingness) in an appendix of the enrichment report for audit.
- **Deliverables:** `data/warehouse/gold/<new_ts>/FactDemand.parquet` covering ≥730 days; update `NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md` with refreshed coverage tables.

## 5.2 Inventory Policy Calibration

- **Objective:** Replace placeholder safety stock and reorder calculations with formulas grounded in enriched data.
- **Actions:**
  1. Extract demand and lead-time statistics from the new Gold snapshot (mean, σ, coefficient of variation).
  2. Rebuild the prescriptive calculator (`demand_forecasting/pp_calculator.py`) to:
     - Parameterise service levels per family/site based on risk scores.
     - Incorporate lead-time variability from `Import Lead Time Factors`.
     - Derive buffer stock using standard formulas: `SS = Z * σ_demand_leadTime`, `ROP = daily_avg * lead_time + SS`.
  3. Update `NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md` with new tables (safety stock, ROP, risk scores with thresholds).
  4. Publish an inventory policy appendix detailing assumptions, formulas, and parameter sources.
- **Deliverables:** Updated prescriptive outputs (`data/outputs/nova_corrente/forecasts/*_prescriptive.json`), revised brief, calculator documentation.

## 5.3 ROI & Finance Alignment

- **Objective:** Provide auditable, sensitivity-tested ROI analysis using current outputs.
- **Actions:**
  1. Build a finance workbook/script that references:
     - Stockout reduction scenarios (from updated forecasts/prescriptive metrics).
     - Holding cost changes due to recalibrated safety stock.
     - SLA penalty avoidance using enriched SLA penalty features.
  2. Produce sensitivity tables (best/expected/worst) with explicit driver values.
  3. Embed results in a finance addendum to `NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md` and link from `NOVA_CORRENTE_ML_PIPELINE_TECH_SPEC.md`.
- **Deliverables:** ROI report (markdown or spreadsheet) with drivers, formulas, and traceability to forecasts/prescriptions.

## 5.4 Pipeline Hardening & Model Strategy

- **Objective:** Finalise model stack and dependency posture while maintaining fallbacks.
- **Actions:**
  1. Decide on optional dependency strategy (install `pmdarima`, CUDA XGBoost/TensorFlow vs. disable advanced models). Reflect in `environment.local.yml` and pipeline spec.
  2. Ajustar ensemble em `ForecastingPipeline` para priorizar modelos suportados (Prophet habilitado via flag `--enable-prophet`; padrão atual usa ARIMA/XGBoost).
  3. Enrich `metrics_summary.json` with actual error metrics (MAPE, MAE, RMSE) per family/site using the extended timeline.
  4. Improve logging: separate warnings for stub data vs. model fallback; add run classifications (baseline vs. full).
- **Deliverables:** Updated pipeline spec, `metrics_summary.json`, dependency guidelines in runbook.

## 5.5 Phase 0 Pilot Definition

- **Objective:** Validate the refreshed forecasting + prescriptive pipeline on a controlled subset before wider rollout.
- **Actions:**
  1. Select one high-impact family (e.g., `FERRO E AÇO`) from the enriched dataset.
  2. Run scenario simulations comparing baseline vs. new forecasts/policies (stock levels, SLA compliance, capital impact).
  3. Document pilot checklist, success criteria, and required operational touchpoints.
  4. Prepare stakeholder briefing summarising pilot results and step-up plan to Phase 1 (broader rollout).
- **Deliverables:** Pilot report, updated roadmap with go/no-go gates.


# 6. Execution Sequencing & Ownership

| Phase | Timeline | Lead | Artifacts to Update |
|-------|----------|------|---------------------|
| 5.1 Historical Backfill | Week 1–2 | Data Engineering | Enrichment report, Gold snapshot | ✅ Backfill executado e snapshot `20251111T164236` gerado |
| 5.2 Inventory Calibration | Week 2–3 | Data Science + Ops | Prescriptive brief, calculator, output JSON |
| 5.3 ROI Alignment | Week 3 | Finance Analyst + Data Science | ROI addendum, pipeline spec cross-links |
| 5.4 Pipeline Hardening | Week 3–4 | MLOps | Pipeline spec, runbook, metrics summary |
| 5.5 Pilot (Phase 0) | Week 4–5 | Analytics Lead + Ops | Pilot report, roadmap update |


# 7. Dependencies & Assumptions

* All enrichment tables referenced in `NOVA_CORRENTE_ENRICHMENT_COMPLETE.md` remain accessible locally.
* No new external API fetches required for this phase; historical extension leverages existing sub-datasets.
* Scripts under `scripts/analysis/` and `scripts/run_*` continue to operate against enriched inputs.
* Optional dependencies permanecem configuráveis; pipeline opera apenas com ARIMA/XGBoost enquanto Prophet/LSTM estiverem desabilitados.
* Stakeholder alignment (finance, operations) will participate during ROI and pilot stages.


# 8. Reporting & Documentation Updates

| Document | Update Required | Trigger |
|----------|----------------|---------|
| `NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md` | Add historical extension results, coverage metrics, data quality appendix | After §5.1 |
| `NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md` | Update risk rankings, safety stock, ROP, recommendations, finance addendum | After §5.2 & §5.3 |
| `NOVA_CORRENTE_ML_PIPELINE_TECH_SPEC.md` | Reflect dependency decision, metrics summary, pilot plan | After §5.4 & §5.5 |
| `BATCH_RUNBOOK.md` | Add notes on extended timeline, optional dependencies, pilot switch | After §5.4 |
| Pilot Report (new) | Summarise Phase 0 outcomes, readiness for Phase 1 | After §5.5 |


# 9. Appendix – Key Script & Directory Map

| Script / Directory | Purpose | Notes |
|--------------------|---------|-------|
| `scripts/run_batch_cycle.py` | Orchestrates full batch cycle; successes logged in `logs/pipeline/runs.csv` | Use after each major phase to verify outputs. |
| `scripts/build_warehouse.py` | Builds Gold snapshot; accepts extended timeline data | Run after historical backfill. |
| `scripts/run_training_pipeline.py` | Standalone training/forecasting; useful for model testing | `--enable-prophet` ativa componente Prophet quando CmdStan estiver disponível. |
| `scripts/analysis/run_nova_corrente_exploratory.py` | Generates exploratory summaries & coverage metrics | Re-run post-backfill to update enrichment report. |
| `scripts/analysis/run_nova_corrente_prescriptive.py` | Computes risk tables & prescriptive stats | Modify once inventory logic updated. |
| `data/warehouse/gold/<timestamp>/` | Gold-layer parquet tables | Verify new snapshot path after each rebuild. |
| `data/outputs/nova_corrente/forecasts/` | Forecast parquet, prescriptive JSON, metrics summary | Inspect after each batch cycle. |
| `logs/pipeline/validation/` | Validation logs per domain | Ensure new timeline passes validators. |
| `logs/pipeline/metrics/` | Rolling cross-validation outputs | Expand with new metrics post-hardening. |


# 10. Conclusion

By concentrating on the already-enriched dataset, this plan eliminates immediate dependency on fresh external pulls while still addressing the primary bottlenecks identified in the diagnostics. Executing the roadmap above will:

* Provide the minimum historical depth required for telecom-grade accuracy.
* Deliver auditable, finance-aligned ROI and inventory policies.
* Establish a hardened, well-documented ML pipeline ready for broader rollout.
* Position the team for future API integrations once credentials and coverage needs are satisfied.

**Next Action:** Avançar para Fase 5.2 (Inventory Calibration) utilizando o snapshot `gold/20251111T164236` e os novos arquivos de forecasts/prescrição.


