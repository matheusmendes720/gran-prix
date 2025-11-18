## Nova Corrente Telecom Enrichment Report

### Executive Summary

This report documents the full enrichment initiative undertaken to strengthen the Nova Corrente demand forecasting dataset (`dadosSuprimentos.xlsx`) with Brazilian telecom contextual data. Five high-value external datasets were evaluated, ingested, and cross-analyzed to address under-fitting caused by the fact table’s limited 380-day history. Exploratory and prescriptive analytics were executed to quantify coverage gaps, uncover correlations, and produce actionable risk mitigation guidelines.

- **Scope:** Integrate macroeconomic, operator, IoT, fiber expansion, and regulatory access datasets with Nova Corrente transactional facts.
- **Outputs:** Daily and monthly enriched tables, correlation matrices, risk scoring, and the prescriptive brief.
- **Key finding:** Inflation, GDP, and FX signals exhibit meaningful correlations (> |0.3|) with demand where coverage exists, but external series currently overlap less than 25% of the fact timeline, requiring backfill for production modelling.

---

### 1. Source Inventory

| Dataset | Path | Temporal Granularity | Fields leveraged | Primary Use |
|---------|------|----------------------|------------------|-------------|
| `brazilian_demand_factors_structured.csv` | `data/raw/brazilian_demand_factors/` | Daily (2019–2024) | GDP growth, inflation, BRL/USD FX, weather metrics, risk flags, demand multiplier | Daily macro/weather enrichment |
| `brazilian_operators_market_structured.csv` | `data/raw/brazilian_operators_structured/` | Monthly (2019–2024) | Subscribers, market share, revenue growth, 5G coverage | Operator concentration signals |
| `brazilian_iot_market_structured.csv` | `data/raw/brazilian_iot_structured/` | Monthly (sector-level) | IoT connections, annual growth | Workload proxy for maintenance demand |
| `brazilian_fiber_expansion_structured.csv` | `data/raw/brazilian_fiber_structured/` | Quarterly (regional) | Household penetration, estimated households | Infrastructure rollout indicator |
| `anatel_municipal_sample.csv` | `data/raw/anatel_municipal/` | Monthly (sample 2023) | Operator, technology, speed, accesses | Regulatory view on connectivity demand |

---

### 2. Integration Pipeline

1. **Daily Fact Aggregation**
   - Script: `scripts/analysis/run_nova_corrente_exploratory.py`
   - Metrics computed: total quantity, families/items/suppliers active, average/median lead time, high lead-time ratio.

2. **Daily External Join**
   - Joined Nova Corrente daily summary with macro/weather dataset.
   - Data cleansing: clipped negative precipitation to zero; flagged missing weather/regulatory columns (~96% missing).

3. **Monthly Resampling & Contextual Joins**
   - Resampled daily series to calendar month-end (ME).
   - Added operator totals (subscribers, Herfindahl index), IoT totals, municipal accesses, and fiber penetration (via quarterly period join).
   - Data quality diagnostics stored as part of exploratory report.

4. **Analytical Outputs**
   - `data/outputs/analysis/nova_corrente_daily_summary.csv`
   - `data/outputs/analysis/nova_corrente_daily_with_context.csv`
   - `data/outputs/analysis/nova_corrente_monthly_with_context.csv`
   - Correlation matrices saved as CSV/JSON.
   - Narrative summary: `docs/reports/NOVA_CORRENTE_EXPLORATORY_ANALYSIS.md`

---

### 3. Exploratory Findings

- **Coverage:** 4,188 fact rows across 20 families and 872 items covering 2024-10-09 → 2025-10-24.
- **Volatility:** Daily total quantity mean ≈ 952, std ≈ 3,026. Lead time mean 11.29 days; 90th percentile 23.16 days.
- **Correlations:** Inflation (−0.42) and GDP (+0.39) correlated with demand where 10% macro overlap exists. FX and temperature align with the synthetic `demand_multiplier`, indicating placeholder values that need replacement.
- **Data gaps:** Weather/regulatory missingness ≥96%; operator/IoT coverage 23%; municipal/fiber join currently NaN due to limited historical overlap.

(See `docs/reports/NOVA_CORRENTE_EXPLORATORY_ANALYSIS.md` for full tables.)

---

### 4. Prescriptive Risk Assessment

- Script: `scripts/analysis/run_nova_corrente_prescriptive.py`
- Calculations:
  - Demand volatility (coefficient of variation).
  - Average lead time and proportion of orders exceeding 21 days.
  - Macro sensitivity (max absolute correlation where ≥10 overlapping points).
  - Composite risk score = 0.4 CV + 0.3 avg lead time + 0.2 high-lead ratio + 0.1 macro.
- Deliverables:
  - `data/outputs/analysis/nova_corrente_family_risk.csv`
  - `data/outputs/analysis/nova_corrente_family_macro_corr.csv`
  - `docs/reports/NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md`

**Top-Risk Families (Composite >0.39):**
1. SUPRIMENTOS ADMINISTRATIVO – CV 4.88, average lead 12.69 d.
2. Corretiva TBSA – lead 32 d, high-lead ratio 100%.
3. MATERIAL ELETRICO – CV 3.10, lead 15.22 d, high-lead ratio 22.9%.
4. FERRO E AÇO – CV 2.67, GDP/FX correlated (|corr| up to 0.80).
5. FERRAMENTAS E EQUIPAMENTOS – CV 3.50, lead 10.33 d.

---

### 5. Strategic Recommendations

1. **Data Backfill & Quality**
   - Expand macro/weather feeds to obtain ≥60% overlap.
   - Parse complete Anatel municipal/broadband archives to extend history beyond 12 months.
   - Replace synthetic fiber growth fields with real Anatel records.

2. **Operational Actions**
   - Implement dynamic safety stock and weekly monitoring for high-volatility families.
   - Negotiate supplier SLAs or pre-stage inventory where average lead time ≥15 days or >30% orders exceed 3 weeks.
   - Link forecasts for `FERRO E AÇO` and `MATERIAL ELETRICO` to macro scenarios (GDP, FX).

3. **Feature Store & Modelling**
   - Persist enriched daily/monthly tables to a feature store for Croston/SBA and probabilistic models.
   - Map operator/site codes to avoid leakage when joining external data.
   - Adopt sMAPE/MAE in addition to MAPE for low-volume demand families.

4. **Long-Term Roadmap**
   - Secure ≥2 seasonal cycles of external data to mitigate under-fitting.
   - Explore hierarchical Bayesian models capturing operator-region interactions once data coverage improves.

---

### 6. Next Steps

1. Automate ingestion pipelines for the identified datasets with validation to ensure consistent daily/monthly coverage.
2. Re-run exploratory (`run_nova_corrente_exploratory.py`) and prescriptive (`run_nova_corrente_prescriptive.py`) scripts after each backfill to refresh diagnostics.
3. Integrate risk outputs into the planning dashboard to drive procurement decisions and link to forecast experiments.
4. Develop notebook or pipeline for Croston/SBA baseline using the enriched feature store after coverage targets are achieved.

---

### Appendix: Key Files

- `scripts/analysis/run_nova_corrente_exploratory.py`
- `scripts/analysis/run_nova_corrente_prescriptive.py`
- `data/outputs/analysis/*.csv` (daily/monthly summaries, risk tables, correlations)
- `docs/reports/NOVA_CORRENTE_EXPLORATORY_ANALYSIS.md`
- `docs/reports/NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md`


