## Feature Spec – `/features/5g`

### Vision
Showcase how 5G rollout affects material demand, coverage expansion, and project planning, using deterministic mock data linking ANATEL milestones to Nova Corrente operations.

### User Story
As a commercial or operations executive, I need to know where 5G expansion is occurring so I can plan resource deployment, procurement, and customer discussions around tower upgrades.

### KPIs
- Highlight new municipalities (coverage %) and associated demand uplift
- Present timeline of 5G milestones with investment figures
- Provide action items for procurement and project teams

### Data Interface
```typescript
type FiveGCoveragePoint = {
  date: string
  municipalities: number
  populationCovered: number
  investmentMillions: number
}

type FiveGEvent = {
  id: string
  date: string
  type: 'coverage' | 'license' | 'upgrade'
  description: string
  region: string
  demandImpact: number // %
  materials: string[]
}

type FiveGRecommendation = {
  id: string
  title: string
  owner: 'Procurement' | 'Operations' | 'Sales'
  action: string
  dueDate: string
}

interface FiveGFeaturePayload {
  coverageTrend: FiveGCoveragePoint[]
  events: FiveGEvent[]
  projections: {
    horizon: string
    additionalMunicipalities: number
    demandUplift: number
    narrative: string
  }
  recommendations: FiveGRecommendation[]
}
```

### Widget Breakdown
1. **Coverage Trend Chart**
   - Area chart showing municipalities & population from `coverageTrend`.
   - Secondary axis for investment.

2. **Events Timeline**
   - Horizontal timeline listing `events`.
   - Filter by event type; tooltips show `demandImpact` and targeted materials.

3. **Impact Map**
   - Static map with markers for `region`; fallback to list if map not ready.
   - Color-coded by demand impact severity.

4. **Projection Summary**
   - Cards summarizing `projections` horizon (30/60/90 days).
   - Combine with scenario slider (optional).

5. **Action Checklist**
   - Cards from `recommendations`, grouped by owner.
   - Example: “Procurement – garantir 500 conectores RF até 15/11”.

6. **Sales Narrative Box**
   - Pull text from `events` describing opportunities for upselling services.

### Synthetic Data Plan
- Create 12-month coverage trend (municipalities 600→900).
- Insert events (e.g., “Salvador phase 2 upgrade 20/10 – demanda +150 kits RF”).
- Link to ROI by referencing how 5G expansion drives revenue.

### Storytelling Flow
1. Begin with coverage growth and investment figures.
2. Highlight key events (new city onboarding) and associated demand impact.
3. Show projection card projecting next 90 days.
4. Present action checklist ensuring procurement and operations prepare.
5. Close with sales narrative linking to market differentiation.

### Future Integration
- Endpoint `/storytelling/features/5g`.
- Data ingestion from ANATEL API / manual dataset.
- Connect action checklist to BFF tasks.

