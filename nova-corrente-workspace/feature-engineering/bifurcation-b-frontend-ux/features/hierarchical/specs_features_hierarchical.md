## Feature Spec – `/features/hierarchical`

### Vision
Enable multi-level analysis (family, site/tower, supplier) to show how demand aggregates and diverges across Nova Corrente’s hierarchy, using deterministic mock data and drill-down narratives.

### User Story
As a demand analyst, I want to explore how consumption behaves at different levels (material family, tower, supplier) so I can identify hotspots, balance inventory, and coordinate with field teams.

### KPIs
- Present aggregated vs. granular demand variance
- Highlight top 3 towers/sites contributing to volatility
- Provide supplier-level insights tied to lead time & SLA

### Data Interface
```typescript
type HierarchicalNode = {
  level: 'family' | 'site' | 'supplier'
  id: string
  name: string
  parentId?: string
  demand: number
  forecast: number
  variancePct: number
  slaImpact: number // %
}

type HierarchicalInsight = {
  level: 'family' | 'site' | 'supplier'
  title: string
  description: string
  recommendation: string
}

interface HierarchicalFeaturePayload {
  nodes: HierarchicalNode[]
  insights: HierarchicalInsight[]
  summary: {
    totalDemand: number
    varianceTopLevel: number
    criticalPath: string[]
    narrative: string
  }
}
```

### Widget Breakdown
1. **Aggregation Tabs** (`Por Família`, `Por Site/Torre`, `Por Fornecedor`)
   - Each tab pulls filtered `nodes`.
   - Display tree-map or stacked bar to compare demand vs forecast.

2. **Variance Table**
   - Show variance %, SLA impact for selected level.
   - Highlight rows with variance > ±15%.

3. **Drill-down Panel**
   - When selecting a node, show children nodes details with mini charts.

4. **Insights Carousel**
   - Cards from `insights` describing patterns (“Torre Salvador Norte → demanda +25% por clima”).

5. **Critical Path Flow**
   - Timeline or list from `summary.criticalPath`, linking family → site → supplier.

6. **Navigation CTA**
   - Buttons to jump to `/features/lead-time` or `/main/clustering` (document requirement).

### Synthetic Data Plan
- Create hierarchical dataset:
  - Families: `Conectores`, `Cabos`, `Refrigeração`
  - Sites: `Salvador Centro`, `Recife Norte`, etc.
  - Suppliers: `Supplier A/B/C`
- Provide demand/forecast numbers with variance to highlight stories.

### Storytelling Flow
1. Start with family-level variance (e.g., Conectores +18% vs forecast).
2. Drill into site-level (Salvador Centro surge due to storm).
3. Connect to supplier (Supplier A lead time trending up).
4. Present insight card referencing SLA risk and actions.
5. Bridge to other tabs for deeper investigation (Lead Time / Clustering).

### Future Integration
- Endpoint `/storytelling/features/hierarchical`.
- Consider caching aggregated data due to size.
- Support dynamic filtering by client or region.

