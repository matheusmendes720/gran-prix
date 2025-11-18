## Frontend Visual Blitz Specs – `/main/analises-aprofundadas`

> **Goal:** Replace every “BACKEND_UNAVAILABLE” gap with a fully visual, interactive, data-driven experience using deterministic mock data. Keep the existing text blocks but wrap them with live calculators, charts, and storytelling widgets that make the demo look production-ready right now.

---

### 0. Global Setup
- **Data Source**: extend `demoSnapshot.ts` (or `demo_dashboard.db`) with `mainTabs` payload:
```typescript
interface MainTabsPayload {
  formulas: Record<FormulaId, FormulaConfig>;
  clustering: ClusteringConfig;
  models: ModelsConfig;
}
```
- **Seed**: deterministic arrays; use utility to simulate daily demand, stock levels, error metrics, cluster coordinates.
- **Shared Components**: `FormulaHero`, `LiveCalculator`, `ScenarioDeck`, `ChartPanel`, `InsightDrawer`, `ActionPill`, `ClusterCard`, `ModelTimeline`, `GaugeMeter`.
- **Interaction**: sliders, toggles, scenario buttons must update charts instantly (no backend call).

---

### 1. Formulas Subtabs (PP, SS, MAPE, RMSE, MAE, Ensemble)

#### Spec Contract
```typescript
type FormulaId = 'pp' | 'ss' | 'mape' | 'rmse' | 'mae' | 'ensemble';

interface FormulaConfig {
  title: string;
  latex: string;
  summary: string;
  inputs: Array<{ id: string; label: string; type: 'number' | 'slider' | 'select'; min?: number; max?: number; step?: number; value: number; options?: Array<{ label: string; value: number }> }>;
  compute: (inputs: Record<string, number>) => { value: number; unit: string; narrative: string; breakdown: string[] };
  scenarios: Array<{ name: string; result: number; narrative: string }>;
  charts: Array<{ type: 'line' | 'area' | 'bar' | 'heatmap' | 'stacked'; title: string; data: Array<{ x: string | number; y: number; series?: string }>; caption: string }>;
  insights: string[];
  actions: Array<{ label: string; route: string }>;
}
```

#### Ponto de Pedido (PP)
- **Inputs**: Demand diária, Lead time, Safety stock, Supplier reliability factor.
- **Compute**: `PP = (D * LT * reliability) + SS`.
- **Visuals**: 21-day stock projection line chart vs. reorder threshold; scenario spark cards (Chuva forte, Normal, Expansão 5G); small bar chart of top 3 itens com dias até PP.
- **Insights**: keep bullet copy; add “Alertas agendados em 6 dias para Conector Óptico”.
- **Actions**: `Ver fornecedores (Lead Time)`, `Criar ordem de compra mock`.

#### Estoque de Segurança (SS)
- **Inputs**: Z (select 1.28/1.65/2.33), Sigma, Lead time, Demand variance.
- **Visuals**: area chart `Confidence vs Buffer`; slider showing capital tie-up vs SLA risk; donut chart splitting stock levels.
- **Insights**: highlight materials needing SS boost; footnote referencing capital savings.

#### MAPE
- **Inputs**: horizon (7/30/60 dias), segment (Global, Conectores, Torretas).
- **Visuals**: gauge (MAPE actual vs thresholds), line chart actual vs forecast with shaded error, bar chart `MAPE por família`.
- **Insights**: “LSTM atingiu 10.5%, 2x melhor que benchmark 20%”; call to hierarchical tab.

#### RMSE
- **Inputs**: timeframe range; toggle “Incluir outliers”.
- **Visuals**: bar chart `RMSE por modelo`; scatter showing residuals; table comparing RMSE vs MAE vs MAPE.
- **Insights**: emphasise large error penalty; note retraining triggers.

#### MAE
- **Inputs**: smoothing window slider (1–7), segment selection.
- **Visuals**: heatmap `MAE por família × semana`; mini line chart showing trend after smoothing.
- **Insights**: “MAE facilita comunicação executiva”; link to Executive console.

#### Ensemble de Modelos
- **Inputs**: weights sliders (ARIMA, Prophet, LSTM) with locked sum; toggle “Alta volatilidade” adjusting default weights.
- **Visuals**: stacked area showing forecast contributions; line chart final vs actual; table of metrics per model.
- **Insights**: “Se FX volátil > 10%, elevar LSTM a 50%”; CTA to modelos tab.

---

### 2. Clustering Tab

#### Data Structure
```typescript
interface ClusteringConfig {
  clusters: Array<{ id: string; label: string; type: 'Falha' | 'Performance'; size: number; slaRisk: number; avgDowntime: number; demandImpact: number; narrative: string; action: string }>;
  scatterPoints: Array<{ clusterId: string; x: number; y: number; label: string }>; // x = falhas/mês, y = tempo de reparo
  timeline: Array<{ date: string; clusterId: string; event: string }>;
  table: Array<{ clusterId: string; material: string; towers: number; penaltyRisk: number; recommendation: string }>;
}
```

- **Widgets**:
  - `ClusterOverviewCards`: show size, risk, highlight color-coded status.
  - `ScatterPlot`: bubble chart with zoom; tooltip shows cluster narrative + recommended actions.
  - `TimelineSlider`: top bar to scroll events (e.g., “Tempestade 05/11 → Cluster Falha Elétrica ↑”).
  - `DetailTable`: filter by cluster type; pre-populate with deterministic rows.
  - `ActionDrawer`: tasks grouped by owner (Operações, Compras, Financeiro).
  - `CTA Buttons`: `Abrir /features/hierarchical`, `Gerar plano de inspeção`.

---

### 3. Modelos Tab

#### Data Structure
```typescript
interface ModelsConfig {
  ensemble: Array<{ model: string; weight: number; mape: number; rmse: number; mae: number }>;
  accuracyTrend: Array<{ date: string; mape: number; rmse: number }>;
  retraining: Array<{ date: string; model: string; trigger: string; note: string }>;
  alerts: Array<{ severity: 'warning' | 'info' | 'critical'; message: string; recommendation: string }>;
  confidence: { score: number; narrative: string; factors: string[] };
}
```

- **Widgets**:
  - `AccuracyTrendChart`: dual line with thresholds; event markers for retraining.
  - `WeightMatrix`: table with weights, metrics, mini sparklines.
  - `ModelTimeline`: horizontal cards describing retraining events (data drift, climate shocks).
  - `AlertCenter`: severity badges; CTA to adjust ensemble (opens Ensemble tab).
  - `ConfidenceGauge`: numeric + narrative (“Confiável: 0.87 – drivers: MAPE<12%, RMSE estável”).
  - `ActionQueue`: `Planejar retraining 15/11`, `Rever pesos após greve`.

---

### 4. Implementation Sprint (Go Horse)
1. **Mock Data**: extend `demoSnapshot.ts` with payloads above (create helper `loadMainTabs()`).
2. **Components**: implement shared components; ensure config-driven rendering (map `FormulaConfig` to UI).
3. **Charts**: use Recharts/Visx/ECharts; use brand colors (`#0CD1A0`, `#FFB03A`, `#1B2A4B`).
4. **State Management**: store selected scenario/inputs in Zustand/Context for calculators.
5. **Tooltips**: embed quotes from strategic docs (SLA penalties, ROI).
6. **Navigation**: wire `Action` buttons to route pushes (even if target tab uses mock data).
7. **QA**: run through script, confirm no backend errors appear, capture fallback images.

---

### 5. Storytelling Checklist
- [ ] Start in PP tab, demonstrate reorder calculation & stock projection.
- [ ] Jump to SS, show capital vs SLA buffer.
- [ ] Rotate through MAPE/RMSE/MAE gauges to prove accuracy.
- [ ] Tweak Ensemble weights to show adaptability.
- [ ] Switch to Clustering to highlight failure cluster & recommended action.
- [ ] Open Modelos tab to show ensemble governance & alerts.
- [ ] Close with CTA to Executive console & scenario lab.

---

### 6. Post-Demo Hookups
- Replace mock payload with `/api/storytelling/main/*` once backend ready.
- Connect Action buttons to workflow tasks.
- Add PDF/CSV export summarising calculators.
- Add telemetry events for analytics (tab view, slider adjustments).

---

**Remember**: hardcode now, wow the audience, retrofit later. All visuals must be ready to screenshot or screen-record without backend support. Go horse! 🐎💥


