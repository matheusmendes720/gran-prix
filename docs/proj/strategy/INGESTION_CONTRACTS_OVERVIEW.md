# Ingestion Contracts Overview

## Context

This addendum documents the external data feeds that flow into the Nova Corrente demand forecasting platform and aligns them with the internal supply workbook `docs/proj/dadosSuprimentos.xlsx`. It complements the strategic dossiers (`STRATEGIC_BUSINESS_PROBLEM_SETUP_PT_BR.md`, `INDUSTRY_STANDARDS_SUPPLY_CHAIN_DYNAMICS_PT_BR.md`) and the mathematical formulations referenced in `MATH_ADVANCED_FORMULAS.md` and `ADVANCED_ML_FORMULATIONS_COMPLETE_PT_BR.md`.

## Data Domains & Sources

| Domain          | Source/API                  | Cadence  | Bronze File Pattern                                | Notes |
|-----------------|-----------------------------|----------|----------------------------------------------------|-------|
| Climate         | INMET Previsão (REST JSON)   | Daily    | `data/landing/bronze/climate/{yyyyMMdd}/raw.json`  | Region keyed by tower cluster; requires `INMET_API_TOKEN`. |
| Economic        | BACEN PTAX & SELIC (REST)    | Daily    | `data/landing/bronze/economic/{yyyyMMdd}/*.json`   | Daily captures; weekly aggregates for modeling. |
| Inflation       | IBGE IPCA (CSV download)     | Weekly   | `data/landing/bronze/economic/{isoWeek}/ipca.csv`  | Weekly snapshot with `week_end_date`. |
| 5G Expansion    | ANATEL Coverage (REST CSV)   | Monthly  | `data/landing/bronze/5g/{yyyyMM}/coverage.csv`     | Maintain Slowly Changing Dimension (SCD Type 2). |
| Operational SLA | Internal logs (CSV exports)  | Daily    | `data/landing/bronze/sla/{yyyyMMdd}/events.csv`    | Exported from internal ticketing system. |
| Lead Time       | Supplier portal (CSV)        | Weekly   | `data/landing/bronze/lead_time/{isoWeek}/lt.csv`   | Contains `supplier_id`, `item_id`, `lead_time_days`. |

## Excel Workbook Mapping

The workbook `dadosSuprimentos.xlsx` is the authoritative source for present item hierarchy and internal metrics. The following mapping guides the Silver-to-Gold transformations:

| Workbook Tab              | Gold Table       | Key Columns                                   | Notes |
|---------------------------|------------------|-----------------------------------------------|-------|
| `Itens`                   | `DimItem`        | `item_id`, `item_name`, `category`, `sku`     | Category aligns with ML feature taxonomy (Categorical, Business). |
| `Sites`                   | `DimSite`        | `site_id`, `region`, `latitude`, `longitude`  | Region maps to climate cluster for INMET joins. |
| `Fornecedores`            | `DimSupplier`    | `supplier_id`, `lead_time_days`               | Weekly lead time feeds update this dimension. |
| `ConsumoHistorico`        | `FactDemand`     | `date`, `item_id`, `site_id`, `qty_consumed`  | Serves as fact grain; forecasting adds `qty_forecast`. |
| `SLAs`                    | `DimOperational` | `sla_id`, `sla_tier`, `response_hours`        | Combined with operational event feeds for SLA features. |

## Validation Contracts

- **Schema enforcement:** Pydantic models per Bronze feed ensure field presence, types, and enumerations before landing in Silver.
- **Great Expectations suites:** Located under `demand_forecasting/expectations/`, covering uniqueness of surrogate keys, non-null checks, and domain ranges (e.g., precipitation ≥ 0).
- **Manifest logging:** Each Bronze load writes `manifest.json` containing `source_url`, `ingested_at`, `hash`, `record_count`, and storage version.

## Delivery & Consumption

- **Silver layer:** Normalized parquet tables stored under `data/landing/silver/{domain}/`. Keys unify on `date`, `iso_week`, or `effective_date` to facilitate joins.
- **Gold layer:** `data/landing/gold/` holds star-schema parquet snapshots keyed by execution timestamp. Artifacts promoted to `data/warehouse/` for versioned analytics.
- **Outputs:** Forecasts and prescriptive metrics materialize within `data/outputs/nova_corrente/`, respecting schemas shared with frontend teams.

## Operational Notes

1. Retain 90-day Bronze history for reprocessing; archive older data to `data/archive/` (future enhancement).
2. API credentials live in `.env.local` (developer machines) and never in source control.
3. Prefect flow names follow `ingest-{domain}` and log run metadata to `logs/pipeline/`.

