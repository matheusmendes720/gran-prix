# Manual Download & Ingest Checklist – Nova Corrente External Factors

Last updated: 2025-11-11

Use this runbook whenever a data source requires human interaction before automation can take over. Each section covers the download location, the expected filename pattern, and the command that pushes the file into the landing zone.

---

## 1. Freightos FBX (Partial lanes)

- **Portal:** <https://terminal.freightos.com/> → FBX → Historical → Export CSV (requires login)
- **Recommended range:** rolling 4 years (set start date to `2019-01-01`)
- **Save as:** `data/manual/freightos/fbx_global.csv`
- **Ingest:**  
  ```bash
  python -m scripts.etl.manual.freightos_ingest \
         --source data/manual/freightos/fbx_global.csv
  ```
- **Notes:** Free tier exposes four lanes (Mexico, New Zealand, Sweden, Thailand). Paid plan unlocks full route coverage; update `freight_config.py` with API credentials if upgraded.

---

## 2. Drewry World Container Index (WCI)

- **Portal:** <https://www.drewry.co.uk/supply-chain-advisors/world-container-index>
- **Action:** Download weekly CSV or request historical spreadsheet via `supplychain@drewry.co.uk`
- **Save as:** `data/manual/drewry/wci_global.csv`
- **Ingest:**  
  ```bash
  python -m scripts.etl.manual.drewry_ingest \
         --source data/manual/drewry/wci_global.csv
  ```
- **Notes:** Drewry files sometimes arrive as XLSX/PDF. Convert to CSV before running the ingest command. The loader keeps the latest run per date.

---

## 3. Baltic Dry Index (manual backup)

- **Portal:** <https://www.investing.com/indices/baltic-dry-historical-data>
- **Action:** Set start date to `2019-01-01`, click “Download Data”
- **Save as:** `data/landing/external_factors-raw/Baltic Dry Index Historical Data.csv`
- **Ingest:**  
  ```bash
  python -m scripts.etl.manual.baltic_dry_ingest \
         --source "data/landing/external_factors-raw/Baltic Dry Index Historical Data.csv"
  ```
- **Notes:** TradingEconomics API already covers BDI automatically; use this manual route if the API quota is exhausted or connectivity fails.

---

## 4. ANTT Logistics KPIs

- **Portal:** <https://dados.antt.gov.br> → Painel de Indicadores → exportar CSV/XLSX
- **Suggested tabs:** RNTRC active fleet, Sascar telemetry KPIs, OTIF performance
- **Save as:** `data/manual/antt/<indicator_name>.xlsx`
- **Ingest:**  
  ```bash
  python -m scripts.etl.manual.antt_ingest \
         --source data/manual/antt/indicadores_logisticos.xlsx \
         --indicator kpi_operational
  ```
- **Notes:** Use `--indicator` to set a clean slug (only lowercase/underscore). The loader auto-detects the date column and melts metrics. After ingest, rerun:
  ```bash
  python -m scripts.etl.transform.external_to_silver
  python -m scripts.etl.feature.build_external_features
  ```
  to propagate new ANTT features (`antt_logistics_stress_index`, etc.) into the feature store.

---

## 5. UNCTAD Liner Shipping Connectivity Index (LSCI)

- **Portal:** <https://unctadstat.unctad.org/wds/TableViewer/tableView.aspx?ReportId=92>
- **Action:** Apply filters (Brazil + comparator countries), export CSV
- **Save as:** `data/manual/unctad/lsci_brazil.csv`
- **Ingest:** *(loader pending)* – drop file and record in this log; ingestion script will mirror the ANTT pattern once source cadence is confirmed.

---

## Operational Reminders

- Verify each file before ingest: open the CSV/XLSX, check the date column and units.
- Keep raw exports in the `data/manual/` tree; do not overwrite previous months—stamp them with the download date (e.g. `fbx_global_20251110.csv`) if multiple versions coexist.
- After every manual ingest, run:
  ```bash
  python -m scripts.etl.transform.external_to_silver
  python -m scripts.etl.feature.build_external_features
  ```
  so Silver/Feature Store reflect the latest drops.
- Log any anomalies (missing columns, layout changes) directly in this file under the relevant section with date + description.

---

Maintainer: External Factors Working Group – contact `dataops@novacorrente.ai`

