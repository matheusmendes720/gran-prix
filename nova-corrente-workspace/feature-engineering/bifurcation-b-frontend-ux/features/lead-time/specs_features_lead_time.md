## Feature Spec – `/features/lead-time`

### Vision
Render a comprehensive view of supplier lead times, backlog, and ETA forecasts, enabling planners to preempt stockouts and align with reorder point logic.

### User Story
As a procurement coordinator, I need to monitor supplier performance and forecasted ETAs so I can trigger purchase orders before safety stock is exhausted and communicate risks to operations.

### KPIs
- Highlight suppliers with lead time variance > 20%
- Provide recommended reorder date tied to PP formula
- Showcase alignment with SLA and capital optimization goals

### Data Interface
```typescript
type SupplierLeadTime = {
  supplierId: string
  supplierName: string
  avgLeadTimeDays: number
  trendDays: number
  reliabilityScore: number // 0-1
  backlogOrders: number
  criticalMaterials: string[]
}

type LeadTimeAlert = {
  id: string
  severity: 'info' | 'warning' | 'critical'
  supplierId: string
  message: string
  recommendedAction: string
  etaDate: string
}

type EtaForecast = {
  materialId: string
  materialName: string
  currentStock: number
  demandDaily: number
  leadTimeDays: number
  reorderPoint: number
  recommendedOrderDate: string
}

interface LeadTimeFeaturePayload {
  suppliers: SupplierLeadTime[]
  alerts: LeadTimeAlert[]
  etaForecasts: EtaForecast[]
  summary: {
    averageLeadTime: number
    highestRiskSupplier: string
    narrative: string
  }
}
```

### Widget Breakdown
1. **Summary Banner**
   - Display average lead time, risk supplier, narrative referencing SLA.

2. **Supplier Performance Table**
   - Data: `suppliers`.
   - Columns: `avgLeadTime`, `trend`, `reliabilityScore`, `backlogOrders`.
   - Conditional formatting for high variance.

3. **Lead Time Variance Chart**
   - Bar chart or box plot highlighting variance across suppliers.

4. **Alert Center**
   - Cards from `alerts`, sorted by severity.
   - CTA linking to reorder calculator (document only).

5. **ETA Forecast Grid**
   - Derived from `etaForecasts`.
   - Show recommended order dates and impact on reorder point.

6. **Safety Stock vs. Lead Time Visual**
   - Simple chart aligning PP formula components to `etaForecasts`.

### Synthetic Data Plan
- 6 suppliers with distinct patterns: one improving, one deteriorating, etc.
- Example: Supplier A avg lead 14 days (trend +3), reliability 0.6 → alert critical.
- `etaForecasts` for key materials (conectores, cabos, refrigeração).

### Storytelling Flow
1. Highlight summary risk (Supplier A reliability drop).
2. Show table + chart to visualize variance.
3. Walk through alert card (“Greve transporte → +12 dias”).
4. Use ETA grid to show recommended order date vs. PP.
5. Tie back to SLA/Capital: “Evita multa de R$200k e estoque excessivo”.

### Future Integration
- Endpoint `/storytelling/features/lead-time`.
- Potential integration with ERP/Procurement data feeds.
- Connect CTA to automated purchase workflow.

