## `/features/temporal` – Detailed Scaffold

### Mission
Turn the empty temporal feature view into a guided exploration of Brazilian seasonal drivers that showcases Nova Corrente’s foresight, while keeping existing working widgets untouched elsewhere.

### User Promise
- **Explain** how temporal signals (calendar events, seasonality, cyclic encoding) drive demand fluctuations.
- **Visualize** the patterns with intuitive charts backed by deterministic mock data.
- **Recommend** concrete operational actions based on upcoming temporal risks/opportunities.

### Core KPIs / OKRs
- Time-on-tab ≥ 45s during demo.
- Users identify at least one actionable event (Carnaval, feriados, rainy season) per session.
- Alignment with demand forecast accuracy: demonstrate <15% MAPE during highlighted periods.

### Content Blocks
1. **Hero Summary**
   - Metric badges: `Próximo Evento`, `Impacto Previsto`, `Confiança`.
   - Inline narrative referencing `Solucao-Completa-Resumida-Final.md` seasonal cascades.
2. **Event Timeline**
   - Horizontal timeline integrating Brazilian holidays + Nova Corrente maintenance cycles.
   - Tooltip copy linking to SLA risk (“Carnaval → acesso restrito → estoque +30%”).
3. **Seasonality Heatmap**
   - Week vs. month matrix for demand intensity.
   - Overlay markers for rainy season (Nov–Apr) and high-temperature intervals.
4. **Cyclical Encoding Panel**
   - Sin/Cos illustration chart (no backend needed) showing how cyclical features smooth predictions.
   - Callout snippet referencing `DataLoader.engineer_features`.
5. **Action Playbook**
   - Cards per upcoming 30 days: `Planejamento Preventivo`, `Compras`, `Operações`.
   - Each card references relevant KPIs (safety stock, SLA buffer).

### Data Requirements (Mock-Friendly)
- `temporalEvents`: array with event name, date, impact_score, recommendation.
- `seasonalityMatrix`: 12×7 grid with normalized demand index (0–1).
- `cyclicalDemo`: sample sin/cos values for visuals.
- `forecastComparisons`: actual vs. predicted data slices for key events.

### Storytelling Notes
- Lead with Carnaval example (−30% atividades semana, +50% antes/depois).
- Highlight rainy season’s effect on corrosion demand (+40%) using timeline tooltips.
- Emphasize predictive buffer: “Alertamos 14 dias antes graças ao calendário inteligente”.

### Backlog (Planning Only)
- Define TypeScript interfaces for the mock data module.
- Draft copy for tooltips / card descriptions using messaging cheat sheet.
- Sketch wireframes for heatmap + timeline (attach separately later).
- Document navigation CTA (“Ver visão executiva em /main/modelos”) for future routing work.

