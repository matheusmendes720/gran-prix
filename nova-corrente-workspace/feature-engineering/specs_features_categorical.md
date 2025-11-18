## Feature Spec – `/features/categorical`

### Vision
Show how categorical encodings (families, sites, suppliers) influence model performance and demand segmentation, providing transparency and actionable group insights with deterministic data.

### User Story
As a data scientist or product owner, I need to understand which categorical variables drive forecasts and how categories differ in behavior so I can refine models and coordinate business actions.

### KPIs
- Highlight top categorical contributors to forecast accuracy
- Surface category-level anomalies or growth opportunities
- Link insights to business actions (e.g., tier upgrades, supplier renegotiation)

### Data Interface
```typescript
type CategoricalEncoding = {
  categoryType: 'family' | 'site' | 'supplier'
  categoryId: string
  categoryName: string
  encodingValue: number
  importanceScore: number
  demandShare: number // %
  narrative: string
}

type CategoricalInsight = {
  categoryType: 'family' | 'site' | 'supplier'
  title: string
  description: string
  recommendation: string
}

interface CategoricalFeaturePayload {
  encodings: CategoricalEncoding[]
  insights: CategoricalInsight[]
  summary: {
    topContributor: string
    modelGain: number // %
    narrative: string
  }
}
```

### Widget Breakdown
1. **Summary Banner**
   - Show top contributor category and model gain percentage.

2. **Encoding Importance Chart**
   - Bar chart of `importanceScore` per category.
   - Toggle by category type (families/sites/suppliers).

3. **Encoding Table**
   - Shows encoding values, demand share, narrative.
   - Sorting and filtering by type.

4. **Insight Cards**
   - Derived from `insights`.
   - Example: “Família Refrigeração → alta importância, revisar estoque”.

5. **Drill-down Modal**
   - When selecting a category, show mini time-series comparing demand share vs. encoding value.

6. **Action Bridge**
   - Document CTA to jump to Business tab or lead time as needed.

### Synthetic Data Plan
- Create 3–4 categories per type.
- Assign encoding values (normalized 0-1) with consistent ordering.
- Importance scores sum to 1 per type.
- Provide narratives referencing ML modeling docs.

### Storytelling Flow
1. Summarize top contributor (e.g., Family Conectores with 0.35 importance).
2. Show bar chart of importance scores; highlight second-level categories.
3. Dive into encoding table for anomalies (site with low demand share but high importance).
4. Present insight card recommending action (promote tier, adjust inventory).
5. Link to Business tab to see combined view.

### Future Integration
- Endpoint `/storytelling/features/categorical`.
- Align with model explainability pipeline (SHAP, etc.).
- Potential to integrate with training dashboards for feature selection.

