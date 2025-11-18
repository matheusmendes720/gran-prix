## Feature Spec – `/features/sla`

### Vision
Provide a risk dashboard for SLA compliance that turns availability metrics, penalties, and violation forecasts into actionable insights with deterministic demo data.

### User Story
As a service delivery manager, I need to monitor SLA health, predicted breaches, and penalty exposure so I can coordinate with procurement and operations to maintain 99%+ availability.

### KPIs
- Display current SLA vs. target (with traffic-light status)
- Highlight penalty exposure for top materials/customers
- Provide mitigation actions reducing risk by ≥20%

### Data Interface
```typescript
type SlaMetric = {
  clientTier: 'Tier 1' | 'Tier 2' | 'Tier 3'
  availability: number // %
  target: number // %
  downtimeHours: number
  penaltyRisk: number // monetary
}

type SlaViolationForecast = {
  id: string
  materialId: string
  materialName: string
  riskLevel: 'low' | 'medium' | 'high'
  probability: number // %
  etaDate: string
  driver: string
}

type SlaAction = {
  id: string
  title: string
  owner: 'Operations' | 'Procurement' | 'Finance'
  impact: string
  deadline: string
}

interface SlaFeaturePayload {
  metrics: SlaMetric[]
  violations: SlaViolationForecast[]
  penalties: Array<{
    client: string
    potentialPenalty: number
    reason: string
  }>
  actions: SlaAction[]
  summary: {
    globalAvailability: number
    target: number
    riskLevel: 'low' | 'medium' | 'high'
    narrative: string
  }
}
```

### Widget Breakdown
1. **SLA Overview Banner**
   - Show global availability vs. target with gauge.
   - Narrative referencing `INDUSTRY_STANDARDS_SUPPLY_CHAIN_DYNAMICS_PT_BR.md`.

2. **Tier Metrics Table**
   - List `metrics` by client tier.
   - Highlight penalty risk values and downtime hours.

3. **Violation Forecast Timeline**
   - Chart showing upcoming `violations` (probability vs time).
   - Use icons for severity; tooltip explains driver.

4. **Penalty Exposure Cards**
   - Summaries from `penalties`.
   - Include CTA referencing action queue.

5. **Mitigation Action Board**
   - Kanban-style list using `actions`.
   - Each action includes owner, impact, due date.

6. **What-if Button (Future)**
   - Document idea to open scenario lab focusing on SLA; no implementation yet.

### Synthetic Data Plan
- Create metrics for Tier 1 (99.2%), Tier 2 (98.5%), Tier 3 (97.8% with risk).
- Violation forecasts tied to lead time issues, weather, etc.
- Penalty exposures: e.g., R$250k for American Tower if connector stockouts occur.

### Storytelling Flow
1. Start with global SLA gauge showing 99.2% vs 99% target.
2. Point out Tier 3 risk and associated penalty.
3. Show violation timeline for connectors next week due to storm.
4. Highlight mitigation actions (increase stock, schedule maintenance).
5. Reinforce financial impact reduction.

### Future Integration
- Endpoint `/storytelling/features/sla`.
- Link to backend penalty computation and alert system.
- Align with action queue for follow-up tasks.

