MIT Telecom Spare Parts — Fit Assessment and Integration Notes

Summary
- Verdict: Fits very well as the core demand/inventory fact dataset for Nova Corrente.
- Why: Domain match (telecom spare parts across sites/towers), schema match (keys/measures aligned), multi-year scale supports robust forecasting and PP/SS.

Where it’s referenced
- STRATEGIC_DATASET_SELECTION_FINAL_PT_BR.md → “Dataset MÁXIMA RELEVÂNCIA (⭐⭐⭐⭐⭐) — MIT Telecom Spare Parts”
- Mentions: 2,058 sites, 3 years, weekly aggregation, spare parts consumption, expected variability CV 0.3–0.8.

Core columns to use and purpose
- Keys: date/week_id, site_id, part_id
- Measures: quantity (weekly consumption), unit_cost
- Dimensions: maintenance_type (preventive/corrective), region, tower_type (Macro/Small), technology (4G/5G/Fiber)
- Labels: part_name (human-readable for UI)

Fit to our problem
- Demand forecasting: quantity per site/part/week is the exact target for ARIMA/Prophet/LSTM.
- Inventory optimization: unit_cost enables ABC classification and cost-aware PP/SS; maintenance_type improves segmentation.
- SLA alignment: corrective demand spikes relate to fault events; site_id and technology help model risk and service levels.

Required enrichments for production
- ERP joins (part_id, site_id):
  - Lead times (lead_time_days), supplier_id, min_order_qty, stock_on_hand, purchase orders, price history.
- External APIs (site_id + week_id):
  - ANATEL coverage (technology rollout), climate (INMET: precipitation, temperature), economics (BACEN: FX, inflation).
- Fault/logs (site/location + period):
  - Aggregate event_type and log_feature_* weekly to create exogenous features for corrective demand.

Granularity note
- Dataset is weekly. Options:
  - Model weekly directly for PP/SS and forecasts, or
  - Disaggregate to daily using business rules (weekday weights/maintenance calendar) and validate.

Standardized join keys
- site_id → ERP Sites.site_code
- part_id → ERP Parts SKU
- week_id → ISO week (surrogate from date)
- region_id → IBGE region codes
- maintenance_type_id, tower_type_id, technology_id → normalized enums

Recommended core schema (anchor)
- Fact_Demand_Weekly(site_id, part_id, week_id, quantity, unit_cost, maintenance_type_id, tower_type_id, technology_id)
- Dim_Part(part_id, part_name, ABC, supplier_id, lead_time_days, min_order_qty)
- Dim_Site(site_id, region_id, tower_type_id, lat, lon)
- Dim_Region(region_id)
- Dim_Technology(technology_id)
- Dim_MaintenanceType(maintenance_type_id)
- Dim_Calendar(week_id, week_start_date, holiday_flag)

Decision and next steps
- Use MIT Telecom as the baseline training/validation dataset.
- Implement ERP and external API enrichment joins.
- Add fault/logs aggregates per site/week as exogenous regressors.
- Compute PP/SS using existing algorithms with unit_cost for cost optimization.