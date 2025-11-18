## Specs – `/main/analises-aprofundadas` (Formulas, Clustering, Modelos)

### Mission
Ship a fully visual, interactive “big-picture” experience powered by deterministic mock data so the dashboard looks live today. Keep existing explanatory copy, but surround it with charts, calculators, storytelling widgets, and cross-links that prove Nova Corrente’s value instantly.

---

## Global Requirements
1. **Data Source**: hardcode deterministic payloads (extend `demoSnapshot.ts`) or load from lightweight SQLite (`demo_dashboard.db`). Every widget must render without a running backend.
2. **Performance**: initial render < 1s; lazy load heavy charts; reuse colors/typography from brand palette.
3. **Interactivity**: sliders, toggles, tooltips, scenario buttons, tabs all respond instantly with mock recalculations.
4. **Storytelling**: each subtab finishes with an “Insight → Action” block referencing Nova Corrente metrics (ROI, SLA, stockout prevention).
5. **Accessibility**: ARIA labels on sliders, charts have descriptive captions, keyboard navigation across tabs.

### Shared Components
- `FormulaHero` – title, formula LaTeX, contextual chip (“Por que usar?”).
- `LiveCalculator` – dynamic inputs + output card (result, equation breakdown, delta vs. baseline).
- `ScenarioDeck` – best/base/worst cards pulling from deterministic scenarios.
- `ChartPanel` – pluggable chart container with caption + tooltip copy.
- `InsightDrawer` – bullet insights with CTA buttons linking to related tabs.
- `DataPill` – highlight KPIs (MAPE 10.5%, SLA 99.2%, etc.).
- `ActionButtons` – `Ver detalhes`, `Adicionar à fila`, `Baixar PDF`.

### Data Contract (per subtab)
```typescript
type ChartSeries = { label: string; color?: string; data: Array<{ x: number | string; y: number }> };

interface FormulaTabConfig {
  id: 'pp' | 'ss' | 'mape' | 'rmse' | 'mae' | 'ensemble';
  title: string;
  summary: string;
  inputs: Array<{ id: string; label: string; type: 'number' | 'slider' | 'select'; value: number; min?: number; max?: number; step?: number; options?: Array<{ label: string; value: number }> }>;
  resultExpression: string;
  output: { value: number; unit: string; narrative: string; highlight?: 'success' | 'warning' | 'critical' };
  scenarios: Array<{ name: string; output: number; narrative: string }>;
  charts: ChartSeries[];
  insights: string[];
  actions: Array<{ label: string; route: string }>;
}

interface ClusterConfig {
  clusters: Array<{ id: string; name: string; size: number; slaRisk: number; demandDelta: number; color: string; narrative: string; recommendedAction: string }>;
  scatter: Array<{ clusterId: string; x: number; y: number; label: string }>;
  timeline: Array<{ date: string; clusterId: string; event: string }>;
}

interface ModelsConfig {
  ensembleWeights: Array<{ model: string; weight: number; mape: number; rmse: number }>;
  accuracyTrend: ChartSeries;
  retrainingEvents: Array<{ date: string; model: string; note: string }>;
  alerts: Array<{ severity: 'info' | 'warning' | 'critical'; message: string; recommendation: string }>;
}
```
- Add `formulasConfig`, `clusterConfig`, `modelsConfig` sections to mock data module.

---

## Subtab Specs – Fórmulas

### 1. Ponto de Pedido (PP)
- **Calculator Inputs**: Demand diária, Lead time, Safety stock, Supplier reliability (0.8–1.2 multiplier).
- **Output Card**: `PP = 175 unidades` with dynamic text describing days until rupture.
- **Visualization**: stock projection line chart (current stock vs. PP threshold for next 21 days).
- **ScenarioDeck**: `Chuva forte`, `Base`, `Expansão 5G`.
- **Insights**: highlight top 3 materiais com `dias até PP <= 7`.
- **Actions**: `Ir para Lead Time`, `Adicionar alerta no Executive`.

### 2. Estoque de Segurança (SS)
- **Calculator**: Z dropdown (90/95/99%), Sigma, Lead time, Demand variation.
- **Output**: `SS = 42 unidades`, color-coded by capital impact.
- **Visualization**: area chart `Confidence Level vs Buffer`.
- **ScenarioDeck**: compare capital tied up vs. SLA risk.
- **Insights**: call out materials needing SS boost.
- **Actions**: `Simular Cenário`, `Exportar recomendação`.

### 3. MAPE
- **KPI Banner**: gauge `Precisão Atual 10.5%` vs. benchmark thresholds.
- **Visualization**: line chart of actual vs. forecast with shaded error band; bar chart of MAPE por família.
- **ScenarioDeck**: `Jan/Chuva`, `Carnaval`, `Greve`.
- **Insights**: highlight best/worst families; tie to hierarchical tab.
- **Actions**: `Abrir /features/hierarchical`, `Enviar relatório`.

### 4. RMSE
- **Visualization**: bar chart `RMSE por modelo`; overlay with industry target.
- **Comparison Card**: table comparing RMSE, MAPE, MAE for quick reference.
- **ScenarioDeck**: show effect of outliers; toggle “Incluir outliers”.
- **Insights**: note when RMSE spike indicates model retraining need.
- **Actions**: `Ver Modelos`.

### 5. MAE
- **Visualization**: heatmap `MAE por família × semana`.
- **Calculator**: ability to exclude high-variance days (checkbox).
- **ScenarioDeck**: show impact of smoothing window.
- **Insights**: emphasize MAE for executive storytelling.
- **Actions**: `Adicionar insight ao PDF executivo`.

### 6. Ensemble de Modelos
- **Weight Slider**: adjust ARIMA/Prophet/LSTM weights (locks sum 1).
- **Visualization**: stacked area `Forecast Contributions` + line `Combined Forecast`.
- **ScenarioDeck**: `Alta Volatilidade`, `Estável`, `Expansão`.
- **Insights**: “Quando FX volátil > 10%, pese LSTM em 50%”.
- **Actions**: `Ir para Modelos`, `Registrar decisão`.

---

## Subtab Specs – Clustering
- **Overview Cards**: show cluster name, size, SLA impact, stock recommendation.
- **Scatter Plot**: x = falhas, y = tempo de reparo, color = cluster. Provide zoom/pan controls.
- **Timeline**: slider to filter events (e.g., “Chuva intensa 05/11 → Cluster crítico”).
- **Detail Table**: show `Materiais`, `Torres`, `Penalidades`, `Ação`.
- **Insights Drawer**: highlight 1) Equipamentos críticos, 2) Torres com performance baixa.
- **Actions**: `Gerar plano de inspeção`, `Enviar para compras`.
- **Mock Data**: 4 clusters (A – Falhas eléctricas, B – Corrosão, C – Alto desempenho, D – Novas torres).

---

## Subtab Specs – Modelos
- **Ensemble Performance Chart**: line chart (MAPE, RMSE) vs. time + shading for confidence intervals.
- **Weight Matrix**: table showing current weights vs. target weights; inline sparkline per model.
- **Lineage Timeline**: chronological cards for retraining events with tags (dados climáticos, cambiais).
- **Alert Center**: display dataset drift, high RMSE, overdue retraining.
- **Confidence Meter**: gauge showing *“Forecast Confiável”* with narrative (pull from summary).
- **Actions**: `Rever ensemble`, `Abrir relatório técnico`.
- **Mock Data**: trending improvement after last retraining, one warning about FX volatility.

---

## Implementation Checklist (30-Min Sprint)
1. Extend `demoSnapshot.ts` (or generator script) with `formulasConfig`, `clusterConfig`, `modelsConfig`.
2. Build shared components (`FormulaHero`, `LiveCalculator`, `ScenarioDeck`, `ChartPanel`, `InsightDrawer`, `ActionButtons`).
3. Wire each formula tab using config-driven rendering.
4. Populate charts with deterministic series (use arrays defined in config).
5. Implement clustering scatter + table + cards.
6. Implement model performance view (charts + timeline).
7. Hook actions to route navigation (even if stubbed).
8. QA storytelling flow; ensure tooltips reference ROI, SLA, forecasts.

---

## Storytelling Script (Demo)
1. **PP tab** – compute reorder in real time, show stock projection, mention ROI.
2. **SS tab** – highlight buffer vs. capital; tie to SLA.
3. **MAPE/RMSE/MAE** – show accuracy gauges; mention 10.5% benchmark.
4. **Ensemble** – adjust weights live; emphasize resilience.
5. **Clustering** – display falhas cluster; show recommended intervention.
6. **Modelos** – confirm ensemble governance, retraining cadence.
7. Call to action: move to Executive Console / Scenario Lab for decisions.

---

## Future Integration Hooks
- Replace hardcoded data with API endpoints (`/api/storytelling/main/formulas`, `/clusters`, `/models`).
- Connect actions to backend tasks (e.g., create purchase order request).
- Add export pipeline (PDF/CSV) summarizing calculators and insights.
- Integrate telemetry (time on tab, interactions) for analytics.


