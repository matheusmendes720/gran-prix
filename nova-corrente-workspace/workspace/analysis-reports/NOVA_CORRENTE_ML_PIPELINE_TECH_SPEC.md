---
title: "Nova Corrente Batch Pipeline – Technical Specification"
date: "2025-11-07"
authors:
  - Nova Corrente Data Engineering
status: "Draft"
---

# 1. Executive Summary

Nova Corrente now runs a fully orchestrated batch pipeline that ingests external demand drivers, curates a gold-layer warehouse, engineers features, trains multiple forecasting models, and publishes prescriptive inventory recommendations. The implementation emphasizes local GPU compatibility while remaining resilient when optional libraries or credentials are absent. This document details the architecture, data contracts, execution flow, failure handling, and next-phase recommendations.

# 2. Objectives & Scope

| Objective | Description | Status |
|-----------|-------------|--------|
| Decouple API integrations | Ingest external data outside the frontend, storing curated artifacts in the data lake/warehouse | ✅ Complete |
| Local GPU readiness | Allow execution on GPU-enabled laptops; gracefully degrade when GPU libs missing | ✅ Complete (with fallbacks) |
| End-to-end automation | Orchestrate ingest → warehouse → features → modeling → prescriptive outputs | ✅ Complete (`scripts/run_batch_cycle.py`) |
| Prescriptive stock policy | Compute safety stock, reorder points, alerts per item/site | ✅ Outputs produced |
| Finance-grade ROI & policy calibration | Reconcile ROI assumptions, risk scoring thresholds, and pilot validation | 🚧 Pending (next phase) |

Out-of-scope items (for future phases):

* Real-time (streaming) ingestion.
* Automated deployment of model artifacts into production APIs.
* Automated monitoring/alerting beyond Prefect logs.

# 3. High-Level Architecture

```
External APIs           Internal Excel/CSV
   |                         |
   v                         v
Prefect Ingestion Flows  (Bronze Landing) -------------------------------
   | (stub fallback)                                            |
   v                                                             v
Silver Layer (validated parquet via Polars)                      |
   |                                                             |
   v                                                             v
Gold Warehouse Builder (Prefect task) --> `data/warehouse/gold/<timestamp>/`
   |                                                             |
   v                                                             |
Feature Builder (Polars -> Pandas/cudf fallback)                 |
   |                                                             |
   v                                                             |
Model Pipeline (Prophet / ARIMA / XGBoost / TFT fallback)        |
   |                                                             |
   v                                                             |
Prescriptive Calculator (Safety Stock, ROP, Alerts)              |
   |                                                             |
   v                                                             v
Outputs (`data/outputs/nova_corrente/forecasts/`)        Logs / Validation Manifests
```

Core technologies:

* **Prefect 3** for orchestration (flows: `climate`, `economic`, `regulatory`, `batch_cycle_flow`).
* **Polars** for columnar transformations; **Pandas** fallback for downstream compatibility.
* **Optional** GPU stack: `cudf`, `temporal_fusion_transformer_pytorch`, CUDA-enabled `xgboost`. Pipeline handles absence gracefully.
* **Data storage**: Parquet artifacts in `data/landing`, `data/warehouse`, `data/outputs`.

# 4. Repository Components

| Path | Description |
|------|-------------|
| `demand_forecasting/flows/` | Prefect flow definitions for ingestion and orchestration. |
| `demand_forecasting/warehouse/` | Gold-layer builder, CSV/Excel fallbacks. |
| `demand_forecasting/features/` | Feature builder, scaling manifests, validation logging. |
| `demand_forecasting/models/` | Prophet, ARIMA, XGBoost, TFT, LSTM (optional) models. |
| `demand_forecasting/pipelines/training.py` | End-to-end training pipeline orchestrator. |
| `demand_forecasting/prescriptive/pp_calculator.py` | Reorder point and safety stock calculations. |
| `demand_forecasting/validation/` | Lightweight validators for Bronze/Silver/Gold. |
| `scripts/run_ingestion_flows.py` | Manual entry point for the ingestion flows. |
| `scripts/build_warehouse.py` | Manual snapshot builder. |
| `scripts/run_training_pipeline.py` | Manual training pipeline runner. |
| `scripts/run_batch_cycle.py` | Full batch orchestration script (ingest → outputs). |

# 5. Data Contracts & Storage Layout

## 5.1 Bronze Layer (`data/landing/bronze/`)

| Domain | Partition | Format | Notes |
|--------|-----------|--------|-------|
| Climate | `climate/{yyyyMMdd}/` | JSON payload + manifest | Prefect generates stub payloads when `INMET_API_TOKEN` missing. |
| Economic | `economic/{yyyyMMdd}/` | JSON payload + manifest | BACEN/PTAX/SELIC aggregator. |
| Regulatory | `regulatory/{yyyyMM}/` | CSV/JSON manifest | ANATEL coverage/regulation feed. |

## 5.2 Silver Layer (`data/landing/silver/`)

Validated parquet files with standardized schema. Validators (`demand_forecasting/validation/validators.py`) ensure:

* Non-null critical fields (date, region, indicator names).
* Value ranges (e.g., temperature, humidity, economic indicator bounds).
* Stub execution bypasses future-date checks to allow forecast horizons.

## 5.3 Gold Layer (`data/warehouse/gold/<timestamp>/`)

Tables include:

* `FactDemand.parquet`: aggregated demand (date, item_id, site_id, qty).
* Dimensions: `DimItem`, `DimSite`, `DimEconomic`, `DimWeather`, `DimRegulatory`, `DimOperational`, `DimCalendar`.
* Feature exports: `features/features.parquet`, `target.parquet`, manifests in `feature_manifests/`.

Fallback logic:

* When Excel sheets (`dadosSuprimentos.xlsx`) missing or misaligned, builder loads `data/processed/nova_corrente/nova_corrente_processed.csv` and infers dimensions/fact.

# 6. Prefect Orchestration

## 6.1 Flows

* `ingest-climate`: fetch → validate → persist Bronze/Silver → manifest.
* `ingest-economic`: merges economic indicators, stores results, logs validation manifest.
* `ingest-regulatory`: same pattern for regulatory data.
* `nova-corrente-batch-cycle`: orchestrates ingest flows, builds warehouse snapshot, exports features, runs training pipeline, logs metrics, writes prescriptive outputs.

## 6.2 Execution Scripts

* `python scripts/run_ingestion_flows.py` — run climate/economic/regulatory flows manually.
* `python scripts/build_warehouse.py` — rebuild gold snapshot from latest Silver + internal data.
* `python scripts/run_training_pipeline.py` — run models and prescriptive outputs in isolation.
* `python scripts/run_batch_cycle.py` — run the full pipeline; latest successful run marked in `logs/pipeline/runs.csv`.

# 7. Feature Engineering

Highlights:

* `FeatureBuilder` reads the latest snapshot (`data/warehouse/gold/<timestamp>/`).
* Temporal features: lags (1/7/28), rolling means/std, calendar features.
* External joins: weather by region/date, economic indicators by date, regulatory events.
* Fallback to Pandas when `cudf` or GPU is unavailable; metadata records `backend` used.
* Validation logs for feature tables stored via `write_validation_result`.

# 8. Modeling Pipeline

| Model | Module | Notes |
|-------|--------|-------|
| Prophet | `demand_forecasting/models/prophet_model.py` | Falls back to baseline constant forecast if Stan optimization fails; logs warning. |
| ARIMA/SARIMA | `demand_forecasting/models/arima_model.py` | `pmdarima` optional; defaults to (1,1,1) orders when absent; handles missing conf_int columns. |
| XGBoost | `demand_forecasting/models/xgboost_model.py` | Uses numeric-only features; returns fallback baseline on failure. |
| TFT/LSTM | `demand_forecasting/models/tft_model.py`, `lstm_model.py` | Optional; raise runtime warning if PyTorch/TFT libs missing. |

Training pipeline behavior (`demand_forecasting/pipelines/training.py`):

* Groups data by (`item_id`, `site_id`) with limit `max_series` (default 10).
* Sorts by date, generates model-specific forecasts, merges into a combined dataframe.
* Computes metrics (MSE, MAE) when actual tail data available.
* Runs rolling cross-validation via `RollingCrossValidator`.
* Generates prescriptive outputs (safety stock, reorder points) using `PPCalculator`.
* Writes artifacts:
  * `item{item}_site{site}.parquet` (forecast results with columns: `ds`, `forecast`, `lower`, `upper`, `arima_forecast`, `xgboost_forecast`).
  * `item{item}_site{site}_prescriptive.json` (recommended reorder point, safety stock, risk flags, notes).
  * `metrics.json` and `metrics_summary.json` (currently containing logging references).

# 9. Validation & Logging

* Validation logs stored in `logs/pipeline/validation/` (JSON per run, per domain).
* Pipeline run history captured in `logs/pipeline/runs.csv` with timestamp, status, snapshot path, metrics summary.
* Metrics directory `logs/pipeline/metrics/` contains rolling cross-validation results (parquet).
* Prefect stdout shows warnings for missing tokens/dependencies; final run succeeded despite fallback warnings (tracked for future tuning).

# 10. Known Limitations & Warnings

| Area | Issue | Current Handling | Future Action |
|------|-------|------------------|---------------|
| API credentials | Missing tokens produce stub data | Logged warnings, placeholder payload | Populate `.env.local` and rerun ingest |
| Optional libs | `pmdarima`, GPU XGBoost, TensorFlow not installed | Fallback to default ARIMA/XGB baseline; warnings logged | Decide to install or disable models |
| Prophet Stan errors | Frequent when time series short | Baseline fallback forecast; warnings recorded | Install CmdStan + tune changepoints or disable Prophet |
| Safety stock outputs | Current values may be inflated due to sigma inputs | Prescriptive JSON produced but flagged for validation | Revisit service level formulas, unit conversions |
| ROI / business metrics | Current doc claims lack audit trail | Not yet recalculated | Build finance-ready model (next step) |
| Metrics summary | Contains only rolling log references | Minimal due to fallback usage | Populate with real metrics after calibration |

# 11. Manual Checklist for Operations

1. **Credentials**
   * Update `.env.local` with live API tokens.
   * Export env vars if running in new shell (`Get-Content .env.local | ForEach-Object { ... }`).

2. **Dependencies**
   * Decide: install heavy GPU libs or disable corresponding models.
   * For heavy install: ensure CUDA drivers, run `pip install pmdarima xgboost[tensorflow] torch lightning temporal-fusion-transformer-pytorch` as needed.

3. **Run Batch**
   * `python scripts/run_batch_cycle.py`
   * Confirm Prefect logs show success.

4. **Review Outputs**
   * `data/warehouse/gold/<timestamp>/`
   * `data/outputs/nova_corrente/forecasts/`
   * `logs/pipeline/runs.csv`, `logs/pipeline/validation/`

5. **Business Validation (pending)**
   * Recalculate ROI (`docs/reports/`, to be updated).
   * Audit safety stock/reorder calculations with operations.
   * Define pilot (Phase 0) for one family.

# 12. Next-Phase Recommendations

1. **Live Data Activation**
   * Populate env secrets, rerun pipeline, confirm outputs with real indicators.

2. **Dependency Strategy**
   * Option A: Install optional libraries for richer forecasts.
   * Option B: Disable Prophet/XGBoost branches to suppress warnings.

3. **Finance Review**
   * Rebuild ROI and payback analyses with explicit assumptions and sensitivity tables.
   * Update `metrics_summary.json` and business reports accordingly.

4. **Inventory Policy Calibration**
   * Recompute safety stock / reorder points with transparent formulas.
   * Differentiate risk scores and align KPI badges with quantitative thresholds.
   * Document formula inputs for operations sign-off.

5. **Pilot & Change Management**
   * Select a product family; simulate vs baseline; document results.
   * Outline integration requirements (ERP/billing) before wide rollout.

6. **Documentation Enhancements**
   * Add data quality appendix (sources, coverage, missing-value handling).
   * Present trend/volatility metrics with visualizations and context.

# 13. References & Supporting Files

* `docs/reports/NOVA_CORRENTE_TELECOM_ENRICHMENT_REPORT.md` – business context.
* `docs/proj/strategy/business_analytics/BUSINESS_ANALYTICS_DEEP_ANALYSIS_PT_BR.md` – current analytics report (needs ROI/safety stock revisions).
* `docs/publish/BATCH_RUNBOOK.md` – operational runbook.
* `data/outputs/nova_corrente/combined_ml_dataset_summary.json` – dataset profile.
* `logs/pipeline/` – validation and metrics logs.

---

_Document history:_  
*2025-11-07* — Initial technical spec drafted after successful batch run with fallbacks.


