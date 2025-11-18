## Spec – `/main` → `Análises Aprofundadas / Fórmulas`

### Vision
Turn the mathematics tab into a fully interactive, data-driven storytelling hub that keeps existing explanatory copy while enriching each formula with visuals, calculators, examples, and cross-links to the rest of the dashboard.

### User Personas
- **Procurement Lead**: wants quick calculators to validate reorder decisions.
- **Operations Manager**: needs confidence that forecasts meet SLA thresholds.
- **Executive**: seeks proof points (KPIs) and easy summaries for presentations.

### Global Requirements
1. Maintain current explanatory text + formula LaTeX.
2. Add interactive widgets fed by deterministic data (`demoSnapshot.ts` or SQLite mock).
3. Provide consistent visual styling (cards, highlights, callouts) aligned with Nova Corrente branding.
4. Ensure each subtab links to related feature tabs (e.g., Lead Time, SLA).

### Shared Components
- `FormulaHeader`: formula title, LaTeX render, one-line summary.
- `ContextHighlight`: chip with “Usado para…”.
- `InteractiveCalculator`: input fields + computed result + explanation.
- `ScenarioCards`: show best/base/worst case outputs.
- `VisualizationPanel`: chart or graphic specific to the formula.
- `InsightsDrawer`: bullet insights auto-populated from deterministic data.
- `CTAButtons`: navigate to deeper tabs (`/features/*`) or download cheat sheet.

### Data Contracts
```typescript
type FormulaScenario = {
  scenario: 'Conservador' | 'Base' | 'Agressivo'
  inputs: Record<string, number>
  result: number
  narrative: string
}

interface FormulaPayload {
  id: 'ponto_pedido' | 'estoque_seguranca' | 'mape' | 'rmse' | 'mae' | 'ensemble'
  defaultInputs: Record<string, number>
  scenarios: FormulaScenario[]
  chartSeries: Array<{ label: string; data: { x: string | number; y: number }[] }>
  example: string
  notes: string[]
}
```
- Populate `FormulaPayload` entries in `demoSnapshot.ts` for each subtab.

### Subtab Specifications

#### 1. Ponto de Pedido (PP)
- **Calculator Enhancements**: current inputs stay; add slider for safety stock, toggle to include supplier reliability factor.
- **Visualization**: dual-axis chart showing stock projection over time (current stock vs. reorder threshold).
- **Scenario Cards**: show upcoming 30/60/90 day reorder needs.
- **Insight Drawer**: highlight top 3 items nearing PP (pull from mock inventory).
- **CTA**: “Ver fornecedores críticos” → `/features/lead-time`.

#### 2. Estoque de Segurança (SS)
- **Calculator**: keep Z, sigma, LT inputs; add dropdown for confidence presets (90/95/99%).
- **Visualization**: area chart illustrating buffer size vs. confidence level with data from `chartSeries`.
- **Scenario Cards**: effect on capital tied up vs. SLA risk.
- **Insight Drawer**: summarize recommended SS adjustments for key materials (link to business tab).
- **CTA**: “Ajustar estoque na simulação” → Scenario Lab.

#### 3. MAPE (Mean Absolute Percentage Error)
- **Explainer**: maintain text; add accuracy gauge showing current MAPE vs. industry benchmarks.
- **Visualization**: line chart comparing actual vs. predicted for sample period, overlaying error band.
- **Scenario Cards**: show how MAPE changes under different data volumes or forecast horizons.
- **Insight Drawer**: highlight segments with best/worst accuracy; link to `/features/hierarchical`.
- **CTA**: “Detalhar por hierarquia”.

#### 4. RMSE (Root Mean Squared Error)
- **Visualization**: bar chart showing RMSE by model (ARIMA, Prophet, LSTM) from ensemble payload.
- **Comparison Table**: RMSE vs. MAE vs. MAPE for quick understanding.
- **Tooltip**: emphasise penalty on large errors.
- **CTA**: “Ver ensemble completo” → Modelos tab.

#### 5. MAE (Mean Absolute Error)
- **Visualization**: heatmap showing MAE by material family vs. time window.
- **Scenario Cards**: demonstrate how MAE shifts with data smoothing or outlier removal.
- **Insight Drawer**: highlight that MAE is used for executive-friendly communication; link to Executive Console.

#### 6. Ensemble de Modelos
- **Visualization**: stacked area or waterfall showing weighted contribution of each model.
- **What-If Slider**: adjust weights (sum 1.0) and view resulting forecast accuracy (deterministic calculations from payload).
- **Scenario Cards**: baseline vs. extreme cases (e.g., high volatility uses more LSTM).
- **Insight Drawer**: listing data conditions favoring each model.
- **CTA**: “Ver performance detalhada” → `/main` Modelos tab.

### Additional Tabs

#### Clustering (within `Análises Aprofundadas`)
- **Widgets**:
  - `ClusterOverviewCards`: summary of major clusters (Falhas vs. Performance).
  - `ClusterScatterPlot`: static chart using mock coordinates from `clusters`.
  - `ClusterDetailTable`: metrics per cluster (size, SLA impact, recommended action).
  - `ActionPanel`: quick tasks referencing clusters.
- **Data**: reuse `clusters` payload from `main_models_clustering_breakdown.md`.
- **CTA**: “Explorar por torre” → `/features/hierarchical`.

#### Modelos (Performance Overview)
- **Widgets**:
  - `EnsemblePerformanceChart`: accuracy trend.
  - `ModelLineageTimeline`: pipeline of retraining events.
  - `AlertList`: model drift alerts.
  - `ConfidenceMeter`: gauge for forecast confidence.
- **Data**: align with `ensembleMetrics`, `accuracyTrend`, `modelAlerts`.
- **CTA**: cross-link to ensemble formula and scenario lab.

### Interaction & UX Notes
- Ensure calculators update charts in real time (even with mock data).
- Provide “Reset to demo defaults” button.
- Add copy-to-clipboard for formula outputs (for reports).
- Maintain responsive layout (two-column for desktop, stacked for mobile).
- Accessibility: ARIA labels for sliders, charts have descriptive titles.

### Synthetic Data Strategy
- Extend `demoSnapshot.ts` with `formulas` section providing default inputs & chart data.
- Example for PP `chartSeries`: stock projection for 14 days given deterministic consumption.
- Example for MAPE `chartSeries`: daily error values seeded with reproducible noise.

### Storytelling Flow (Demo)
1. Begin with PP calculator: show reorder decision and link to lead time risks.
2. Move to SS to highlight buffer strategy and capital trade-offs.
3. Showcase MAPE/RMSE/MAE gauges to prove precision.
4. Finish with Ensemble interactive weight slider to show adaptability.
5. Transition to Clustering → Modelos tabs to demonstrate depth.

### Future Integration Hooks
- Replace deterministic data with BFF responses once backend is ready (`/api/storytelling/formulas`).
- Connect scenario outputs to Alerts queue on Executive Console.
- Offer export (`Download PDF/CSV`) using current calculator outputs.


