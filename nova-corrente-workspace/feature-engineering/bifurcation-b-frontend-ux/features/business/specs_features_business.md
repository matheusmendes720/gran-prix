## Feature Spec – `/features/business`

### Vision
Create a business intelligence layer that consolidates Nova Corrente’s B2B-specific metrics (families, tiers, penalties, revenue) to tell a compelling story about commercial performance and strategic priorities.

### User Story
As an executive or account manager, I need a clear view of business KPIs (top families, tier analysis, penalties, revenue impact) to align sales, operations, and finance around data-driven decisions.

### KPIs
- Display top 5 families by revenue/volume with growth trend
- Show tier-based penalties and SLA status
- Provide actionable insights for upsell, risk mitigation, and cashflow

### Data Interface
```typescript
type BusinessFamilyMetric = {
  familyId: string
  familyName: string
  revenue: number
  volume: number
  growthPct: number
  slaCompliance: number // %
  penaltyRisk: number
}

type BusinessTierMetric = {
  tier: 'Tier 1' | 'Tier 2' | 'Tier 3'
  revenue: number
  contracts: number
  slaCompliance: number
  penaltyExposure: number
}

type BusinessInsight = {
  category: 'Revenue' | 'Risk' | 'Opportunity'
  title: string
  description: string
  recommendedAction: string
}

interface BusinessFeaturePayload {
  families: BusinessFamilyMetric[]
  tiers: BusinessTierMetric[]
  insights: BusinessInsight[]
  summary: {
    totalRevenue: number
    growthQoQ: number
    biggestRisk: string
    narrative: string
  }
}
```

### Widget Breakdown
1. **Business Summary Banner**
   - Show total revenue, QoQ growth, risk narrative.
   - Tie to ROI metrics from executive console.

2. **Top Families Chart**
   - Bar or stacked chart of `families` revenue/volume.
   - Include growth indicators and SLA compliance badges.

3. **Tier Analysis Matrix**
   - Table or heatmap of `tiers`, showing revenue vs. penalty exposure.
   - Highlight Tier 3 for risk discussion.

4. **Penalty & Opportunity Cards**
   - Derived from `families` & `tiers`.
   - Example: “Tier 2 – SLA 98.5%, risco R$120k”.

5. **Insights Carousel**
   - Items from `insights` with recommended actions.
   - Categories color-coded (Revenue, Risk, Opportunity).

6. **Action CTA**
   - Document future button to open action queue or contact sales plan.

### Synthetic Data Plan
- Create 5 families with revenue (R$) and volume metrics.
- Tiers: Tier 1 (R$40M, SLA 99.5%), Tier 2 (R$25M, SLA 98.7%), Tier 3 (R$10M, SLA 97.8%).
- Insights referencing cross-sell, penalty avoidance, contract renewals.

### Storytelling Flow
1. Open with summary and growth narrative.
2. Highlight top family (Conectores) driving revenue and risk.
3. Discuss Tier matrix to show where penalties threaten margin.
4. Present opportunity insight (upsell to Tier 2 client) and risk mitigation (extra preventive visits).
5. Link to SLA and ROI discussions.

### Future Integration
- Endpoint `/storytelling/features/business`.
- Align with finance/CRM datasets.
- Potential to export executive summary (PDF) directly from this tab.

