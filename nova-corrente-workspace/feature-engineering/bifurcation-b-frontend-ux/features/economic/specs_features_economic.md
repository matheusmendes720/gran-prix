## Feature Spec – `/features/economic`

### Vision
Convert the Economic features tab into a compact financial radar that shows how macro indicators (IPCA, USD/BRL, SELIC, GDP) drive demand and cost decisions, using deterministic data suited for the demo.

### User Story
As a procurement lead or CFO, I need to know how economic indicators shift material demand, cost of capital, and import decisions so that I can adjust purchasing timelines and budgets proactively.

### KPIs
- Communicate ROI sensitivity to FX/inflation changes
- Provide at least one recommendation linked to capital optimization
- Demonstrate synergy with ROI metrics on executive console

### Data Interface
```typescript
type EconomicIndicatorPoint = {
  date: string
  ipca: number
  usdBrl: number
  selic: number
  gdpGrowth: number
}

type EconomicImpact = {
  factor: 'ipca' | 'usd_brl' | 'selic' | 'gdp'
  demandImpact: number // %
  costImpact: number // %
  narrative: string
}

type EconomicRecommendation = {
  id: string
  severity: 'info' | 'warning' | 'critical'
  title: string
  description: string
  actionOwner: 'Procurement' | 'Finance' | 'Operations'
  dueDate: string
}

interface EconomicFeaturePayload {
  indicators: EconomicIndicatorPoint[]
  impacts: EconomicImpact[]
  recommendations: EconomicRecommendation[]
  summary: {
    period: string
    usdTrend: 'up' | 'down' | 'flat'
    inflationTrend: 'up' | 'down' | 'flat'
    liquidityRisk: 'low' | 'medium' | 'high'
    narrative: string
  }
}
```

### Widget Breakdown
1. **Summary Tiles**
   - Display trend arrows for USD/BRL, IPCA, SELIC, ROI impact.
   - Narrative referencing `MARKET_ANALYSIS_INDUSTRY_WISDOM_PT_BR.md`.

2. **Indicator Timeline**
   - Multi-line chart (FX, inflation, SELIC) pulled from `indicators`.
   - Event markers (e.g., “Selic +0.5pp”).

3. **Impact Waterfall**
   - Show additive effect on demand/cost using `impacts`.
   - Example: “USD/BRL +10% → Demand +15% (estoque), Cost +12%”.

4. **Scenario Selector**
   - Toggle between `Base`, `Adverso`, `Otimista` scenarios derived from `impacts`.
   - Drives text summary + chart shading (mocked).

5. **Action Recommendations**
   - Cards from `recommendations`, grouped by owner.
   - Example: “Financeiro – Aumentar hedge 30 dias” (due date).

6. **Cashflow vs. Inventory Gauge**
   - Derived indicator comparing cost impact to capital savings from ROI gauge.

### Synthetic Data Plan
- Build deterministic 90-day series with gentle trends:
  - FX climbs from 4.80 → 5.30
  - IPCA rising from 0.4% → 0.8% monthly
  - SELIC stable 12.25% with small adjustments
- Map changes to impact percentages using simple formulas.

### Storytelling Flow
1. Summarize macro environment (FX up, inflation up, liquidity risk medium).
2. Show timeline illustrating recent spikes with tooltips.
3. Walk through waterfall linking FX/inflation to demand uplift and cost pressure.
4. Present recommendations (anticipate purchases, adjust safety stock, hedge).
5. Tie back to ROI gauge: “Mesmo com câmbio volátil, mantemos ROI 1.6x via IA”.

### Future Integration
- Endpoint `/storytelling/features/economic?materialId=...`
- Potential linkage to BACEN/IBGE APIs.
- Connect recommendations to action queue tasks (future sprint).

