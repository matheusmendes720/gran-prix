# 🚢 Freight & Shipping Indices Integration – Project Summary

Last updated: 2025-11-11

## 1. Objective

Provide the Nova Corrente forecasting stack with a reproducible pathway to ingest, normalize, and engineer logistics indicators that capture external shocks to supply-chain lead times and costs. We now cover:

| Coverage Layer | Status | Source(s) | Ingestion Script |
| --- | --- | --- | --- |
| Bulk shipping (BDI) | ✅ Automated via manual ingest hook | `Baltic Dry Index Historical Data.csv` (Investing.com download) | `python -m scripts.etl.manual.baltic_dry_ingest` |
| Container benchmark (World Bank IMF SCI proxy) | ✅ Already handled under `freight_worldbank.parquet` | `scripts/etl/external/fetch_all.py` → worldbank downloader | – |
| Container spot – Freightos FBX | 🚧 Manual staging supported | `data/manual/freightos/*.csv` (Freightos export) | `python -m scripts.etl.manual.freightos_ingest` |
| Container spot – Drewry WCI | 🚧 Manual staging supported | `data/manual/drewry/*.csv` (Drewry weekly sheet) | `python -m scripts.etl.manual.drewry_ingest` |
| Domestic logistics – ANP Diesel/Fuel | ✅ Automated | `scripts/etl/external/openweather_ingest.py` + ANP downloader | – |

## 2. Repository Components

| Area | Key Files / Commands | Notes |
| --- | --- | --- |
| Manual ingest hooks | `scripts/etl/manual/baltic_dry_ingest.py`, `scripts/etl/manual/freightos_ingest.py`, `scripts/etl/manual/drewry_ingest.py` | Normalize CSVs into landing zone. Handles column aliases & date cleaning. |
| Silver transformation | `scripts/etl/transform/external_to_silver.py` | Aggregates ANP, World Bank, Baltic, Freightos, Drewry into Parquet tables under `data/silver/external_factors/logistics/`. |
| Feature engineering | `scripts/etl/feature/build_external_features.py` | Adds rolling averages, volatility, spreads (`freightos_fbx_ma7`, `fbx_wci_spread`, `diesel_vs_baltic_ratio`, etc.) and writes `data/feature_store/external/macro_climate_daily.parquet`. |
| Orchestration | `python -m scripts.etl.external.fetch_all` | Full external fetch (OpenWeather, BACEN, IBGE, World Bank) before logistics ingest. |

### 2.1 Exported Automation Toolkit (`data/landing/external_factors-raw`)

The standalone automation package that was exported for sharing/testing lives under `data/landing/external_factors-raw/` and mirrors the conceptual diagram (freight indices → central orchestrator → CSV/feature store). Key assets:

- **Orchestrator & Sources:** `freight_data_automation.py`, `trading_econ_fetcher.py`, `worldbank_freight_fetcher.py`, `selenium_freight_scraper.py`, `freight_config.py`
- **Scheduling & Ops:** `freight_data_scheduler.py`, `freight-cronjob.yaml`, `.github/workflows/fetch-freight-data.yml`, `Makefile`, `docker-run.sh`, `Dockerfile`, `docker-compose.yml`
- **Documentation & Guides:** `freight_automation_guide.md`, `implementation_summary.md`, `README.md`, `QUICKREF.md`, `example_notebook.py`
- **Supporting Scripts:** `requirements.txt`, `script.py`, `script_1.py`, `script_2.py`, `script_3.py`, `scripts/etl/manual/antt_ingest.py`, `scripts/etl/external/fred_downloader.py`
- **Runbook:** `docs/operations/manual_downloads.md` (step-by-step manual fetch instructions for Freightos, Drewry, ANTT, etc.)

> These exports provide a portable bundle: run `make install && make download` inside that directory to exercise the central orchestrator, or drop the contents into CI/Kubernetes using the provided manifests.

## 3. Manual Download Cheat Sheet

| Dataset | How to Download | Output | Where to Drop |
| --- | --- | --- | --- |
| Baltic Dry Index | <https://www.investing.com/indices/baltic-dry-historical-data> → set `2021-01-01` to today → “Download Data” | CSV with columns `Date, Price…` | `data/landing/external_factors-raw/Baltic Dry Index Historical Data.csv` (already added) |
| Freightos FBX (Global) | <https://terminal.freightos.com/> → FBX → Historical → Export CSV (requires account) | CSV with `date,value` columns | `data/manual/freightos/fbx_global.csv` |
| Drewry WCI | <https://www.drewry.co.uk/supply-chain-advisors/world-container-index> → download weekly report or request spreadsheet | CSV (or convert from XLS/PDF) | `data/manual/drewry/wci_global.csv` |
| ANTT Logistics KPIs | <https://dados.antt.gov.br> (Painel Indicadores → exportar CSV/XLSX) | CSV/XLSX with period + metric columns | `data/manual/antt/<indicator>.xlsx` (ingest via `antt_ingest.py`) |

> **Tip:** After dropping the files, run the corresponding ingest commands (below) to copy them into `data/landing/external_factors-raw/logistics/...`.

## 4. Ingestion → Feature Pipeline

```bash
# Stage manual logistics datasets
python -m scripts.etl.manual.baltic_dry_ingest \
       --source "data/landing/external_factors-raw/Baltic Dry Index Historical Data.csv"
python -m scripts.etl.manual.freightos_ingest \
       --source data/manual/freightos/fbx_global.csv
python -m scripts.etl.manual.drewry_ingest \
       --source data/manual/drewry/wci_global.csv
python -m scripts.etl.manual.antt_ingest \
       --source data/manual/antt/indicadores_logisticos.xlsx \
       --indicator kpi_operational

# Refresh Silver layer and engineered features
python -m scripts.etl.transform.external_to_silver
python -m scripts.etl.feature.build_external_features
```

Outputs:

- `data/silver/external_factors/logistics/baltic_dry.parquet`
- `data/silver/external_factors/logistics/freightos_fbx.parquet` (once staged)
- `data/silver/external_factors/logistics/drewry_wci.parquet` (once staged)
- `data/feature_store/external/macro_climate_daily.parquet` (1,168 rows as of 2025‑11‑11)

## 5. Engineered Signals Included

| Signal | Description |
| --- | --- |
| `diesel_price_ma7`, `diesel_price_ma30`, `diesel_price_volatility_30` | Rolling fuel cost indicators from ANP diesel series. |
| `baltic_dry_index_ma7`, `_ma30`, `_pct_change_7d`, `_zscore_90d` | Shipping momentum & standardized anomalies. |
| `freightos_fbx_ma7`, `_ma30`, `_pct_change_7d` | Container spot rolling signals (once FBX staged). |
| `drewry_wci_ma7`, `_ma30`, `_pct_change_7d` | Alternative container indicator (once WCI staged). |
| `diesel_vs_baltic_ratio`, `diesel_baltic_spread` | Fuel cost vs. bulk freight stress. |
| `diesel_s10_x_airfreight`, `diesel_x_container_traffic` | Interaction terms linking fuel price to World Bank container & air freight proxies. |
| `fbx_wci_spread`, `fbx_to_baltic_ratio` | Relative container indexes and container vs. bulk divergence. |
| `antt_*_ma7`, `_ma30`, `_pct_change_14d` | Rolling logistics KPIs from ANTT exports (fleet availability, RNTRC volumes, OTIF). |
| `antt_logistics_stress_index`, `diesel_vs_antt_stress` | Composite stress gauges combining ANTT trends with diesel/Baltic drivers. |
| `cds_spread_bps_ma7`, `_ma30`, `_pct_change_30d` | Sovereign risk proxy sourced from FRED CDS spreads (World Bank data). |
| `ppp_conversion_factor_yoy` | PPP fallback metric (FRED) to monitor relative pricing shifts. |

These features flow directly into the Nova Corrente feature store, ready for Prophet/ARIMAX/LSTM/TFT ensembles or cash-aware stocking heuristics.

## 6. Recommended Next Steps

1. **Stage Freightos & Drewry CSVs** to take advantage of the new ingest hooks (5–10 mins).
2. **Integrate ANTT freight reports** – drop source files into `data/manual/antt/` and expand the manual ingest pattern.
3. **Broaden IBGE coverage** – add IPCA‑15/INPC/PIB via `scripts/etl/external/ibge_downloader.py`.
4. **Automated QC** – extend `enrich_feature_space` or build a `tests/logistics_data_quality.py` to guard against stale/malformed manual uploads.
5. **Model retraining** – experiment with the new engineered features in demand/stock forecasting notebooks and document uplift.

## 7. References

- Trading Economics API docs – <https://docs.tradingeconomics.com/>
- Drewry WCI – <https://www.drewry.co.uk/supply-chain-advisors/world-container-index>
- Investing.com Historical Data – <https://www.investing.com/indices/baltic-dry-historical-data>
- World Bank API – <https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-api-documentation>

---

Maintained by: Nova Corrente Data & AI – External Factors Working Group
