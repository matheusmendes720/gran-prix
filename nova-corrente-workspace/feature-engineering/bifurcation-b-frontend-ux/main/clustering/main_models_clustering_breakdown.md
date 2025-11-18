## `/main` – Models & Clustering Empty State Breakdown

### Goal
Design a high-level, demo-ready experience for the “Modelos” and “Clustering” tabs that currently show backend-unavailable messages, without altering working sections.

### Audience Promise
- **Modelos**: Give executives confidence that the ensemble is accurate, stable, and governed.
- **Clustering**: Surface actionable groupings (equipment failures, tower performance) to prioritize interventions.

### Key Outcomes
- Showcase <15% MAPE trend and explain ensemble composition.
- Highlight top 3 risk clusters with recommended actions.
- Keep presentations self-contained (hardcoded data OK).

### Modelos Tab Plan
1. **Ensemble Overview**
   - Cards for Prophet, ARIMA, LSTM/TFT with accuracy, weight, drift status.
   - Narrative referencing `frontend_feature_engineering_masterplan.md`.
2. **Accuracy Trend Chart**
   - Line chart of MAPE/RMSE over last 90 days (mock data).
   - Confidence band annotated with major events (rainfall spike, FX volatility).
3. **Model Lineage Timeline**
   - Horizontal timeline showing retraining cadence and approvals.
   - Tooltips: “Retrained 05/11 – data validated com PSI 0.12”.
4. **Risk Alerts**
   - List of monitored warnings (e.g., “FX volatility > 10% → reajustar pesos ensemble”).
5. **CTA**
   - Button linking to `/features/hierarchical` for deeper breakdown (documented only).

### Clustering Tab Plan
1. **Cluster Snapshot Cards**
   - `Falhas de Equipamentos`, `Performance de Torres`, `Rotatividade`.
   - Each card: cluster name, size, SLA impact, recommended play.
2. **Cluster Map / Scatter**
   - Static scatter grouped by cluster color (mock coordinates).
   - Toggle between Failure vs. Performance modes.
3. **Cluster Details Table**
   - Columns: `Cluster`, `Qtde Torress`, `SLA`, `Risco`, `Ação`.
4. **Action Panel**
   - Quick tasks: “Agendar inspeção”, “Aumentar estoque de refrigeração”.
5. **Insights Narrative**
   - Text block connecting clusters to ROI/capital (tie to `Solucao-Completa-Resumida-Final.md`).

### Data Contracts (Mock)
- `ensembleMetrics`: array of `{model, mape, weight, last_trained, drift_score}`.
- `accuracyTrend`: time series with `date`, `mape`, `rmse`, plus `events`.
- `modelAlerts`: list of severity-tagged items.
- `clusters`: array with metadata + coordinates.
- `clusterActions`: recommended steps per cluster.

### KPIs / Monitoring
- Keep model accuracy narrative aligned with hero KPIs.
- Clustering tab should highlight at least one SLA-critical cluster.
- Ensure both tabs provide CTA back to operational actions (alerts, scenario lab).

### Backlog Tasks (No Code Yet)
- Draft copy for cards/tooltips referencing strategic docs.
- Produce simple wireframes for ensemble trend and cluster scatter.
- Confirm mock data schema with `demoSnapshot` plan (extend as needed).
- Document navigation improvements (breadcrumbs, cross-links) for future sprint.

