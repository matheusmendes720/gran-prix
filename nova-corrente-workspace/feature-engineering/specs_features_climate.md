## Feature Spec – `/features/climate`

### Vision
Populate the climate feature tab with actionable weather intelligence for Salvador/BA (and future regions) using deterministic mock data while aligning with Nova Corrente’s SLA risk narrative.

### User Story
As an operations planner, I need to monitor climate trends (temperature, precipitation, storm risk) so I can adjust safety stock, crew scheduling, and maintenance plans before adverse weather hits.

### KPIs
- Highlight at least one weather-driven alert per session
- Show correlation between rainfall spikes and demand uplift
- Emphasize SLA risk reduction measures (≥80% prevention)

### Data Interface
```typescript
type ClimateMetric = {
  date: string
  temperature: { avg: number; max: number; min: number }
  rainfall: number
  humidity: number
  wind: number
  stormRisk: 'low' | 'medium' | 'high'
}

type ClimateAlert = {
  id: string
  title: string
  severity: 'info' | 'warning' | 'critical'
  impact: string
  recommendation: string
  effectiveFrom: string
  effectiveTo: string
}

interface ClimateFeaturePayload {
  metrics: ClimateMetric[]
  summary: {
    period: string
    avgTemp: number
    avgRainfall: number
    riskLevel: 'low' | 'medium' | 'high'
    narrative: string
  }
  alerts: ClimateAlert[]
  correlations: Array<{
    factor: 'temperature' | 'rainfall' | 'humidity' | 'wind'
    demandImpact: number // %
    slaRiskDelta: number // %
  }>
}
```

### Widget Breakdown
1. **Summary Header**
   - Displays overall averages, risk level, narrative text.
   - Should highlight rainy season or heatwave context.

2. **Climate Metric Tabs (Temperatura / Precipitação / Riscos)**
   - Line / bar charts fed by `metrics`.
   - Sub-tabs reuse existing layout; populate with deterministic series.
   - Add callouts: “Chuva +60mm → Demanda +40% (Conectores)”.

3. **Storm Risk Timeline**
   - Derived from `stormRisk` values.
   - Color-coded band chart, highlight critical dates.

4. **Climate Alerts Panel**
   - Cards sourced from `alerts`, sorted by severity.
   - Include CTA: “Ver cenário” linking to scenario lab (document only).

5. **Correlation Insights**
   - Radar or bar chart using `correlations`.
   - Text summary: “Umidade >80% aumenta corrosão (estoque de anticorrosivos +25%)”.

6. **Operational Checklist**
   - Derived from alerts and correlations.
   - Example sections: `Procurement`, `Field Ops`, `Logística`.

### Synthetic Data Plan
- Build deterministic 30-day dataset with sinusoidal patterns for temperature, rainfall spikes every 7 days.
- Use `np.random.seed(42)` style reproducibility.
- Map rainfall >50mm to `stormRisk = 'critical'`.

### Storytelling Flow
1. Start with summary: “Semana chuvosa → risco médio”.
2. Show precipitation spikes and reference demand uplift for specific materials.
3. Highlight storm alert card with recommended action.
4. Show correlation chart linking humidity to SLA risk.
5. Close with checklist pointing to procurement adjustments.

### Future Integration
- API endpoint `/storytelling/features/climate?region=salvador`.
- Potential integration with INMET API snapshots.
- Replace synthetic alerts with ML-generated risk predictions.

