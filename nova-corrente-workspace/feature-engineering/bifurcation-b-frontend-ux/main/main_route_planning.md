## `/main` Route – Executive Overview Plan

### Objective
Provide a bird’s-eye aggregation of predictive insights that stitches together the ML feature families while keeping the working widgets intact. Focus on filling empty states in “Modelos”, “Clustering”, and “Prescritivo” tabs and ensuring smooth storytelling back to `/features`.

### View Summary
| Sub-tab | Current Issue | Target Rolling Experience | Dependencies |
|---------|---------------|---------------------------|--------------|
| Modelos | Backend unavailable message | Showcase ensemble performance dashboard with accuracy trends, confidence intervals, and model lineage cards | `storytelling_timeseries`, `models.metrics`, `alerts.model` |
| Clustering | Backend unavailable message | Visualize equipment failure clusters & tower performance segments, each with quick insights + link to feature tabs | `analytics.clusters`, `inventory.geo` |
| Prescritivo | Empty (planned) | Prescriptive playbook board: recommended purchase orders, SLA interventions, cashflow impacts | `storytelling_prescriptions`, `roi` |

### Macro Widgets (Leave Working Ones Untouched)
1. **Global KPI Banner** (already functional) – continue to mirror hero metrics.
2. **Alert Feed** – reuse existing component; extend to reference newly filled sub-tabs.
3. **Navigation Bridge** – document requirement for cross-linking buttons (e.g., “Ver detalhes no /features/climate”).

### Aggregation Strategy
- **Model Cohesion**: Display ensemble composition (Prophet, ARIMA, LSTM/TFT) with attribution to reduce confusion about “Erro ao carregar métricas”.
- **Cluster Storytelling**: Summaries for “Falhas de Equipamentos” and “Performance de Torres” that highlight root causes and tie back to SLA & safety stock.
- **Prescriptive Outcomes**: stack impact cards for Procurement, Operações, Financeiro showing expected stockout prevention, working capital change, SLA uplift.

### KPIs for High-Level Monitoring
- Forecast Accuracy (global) vs. per-model breakdown.
- Stockout Prevention Rate vs. Prescriptive compliance.
- Cluster risk index (equipment/tower) vs. SLA exposure.
- Cashflow at risk vs. recommended actions executed.

### Navigation & UX Notes
- Plan CTA buttons from each sub-tab to the specific `/features` family (e.g., Modelos → `/features/hierarchical`).
- Document desired breadcrumb pattern and keyboard shortcuts (without implementing yet).
- Ensure consistent header copy and tooltip language between routes.

### Backlog (Planning Stage Only)
1. Draft data contract sketches for `models.metrics`, `analytics.clusters`, `prescriptions.recommendations`.
2. Storyboard each empty sub-tab with wireframe notes (attach in future doc).
3. Align with `frontend_feature_engineering_masterplan.md` to avoid scope drift.
4. Capture navigation requirements for routing fixes in later sprint.

