## Frontend Feature Engineering Masterplan

### Purpose
- Fuse the end-to-end solution blueprint (`Solucao-Completa-Resumida-Final.md`) with the rapid demo playbook (`demo_dashboard_quick_strategy.md`).
- Provide a single source of truth for frontend widgets, data contracts, and storytelling messaging that highlight Nova Corrente’s competitive edge.
- Align hour-zero demo priorities with the post-roadshow production roadmap (BFF + ML integration).

### North-Star Narrative
1. **Prevent SLA penalties** (99%+ availability) by predicting demand, triggering reorder alerts early, and guiding decision-makers.
2. **Optimize capital** (−20% inventory) through prescriptive recommendations that weigh lead time, safety stock, and macro factors.
3. **Own the story**: deliver a visually compelling, scripted experience that moves from business pain → AI insight → financial outcome in under 5 minutes.

### Experience Architecture
| Tab / Surface | Key Widgets | Core Message | Data Contract | Reference Docs |
|---------------|-------------|--------------|---------------|----------------|
| **Hero Overview** | KPI strip, Forecast Pulse, SLA Risk Radar | “IA mantém SLA 99%+, -60% rupturas, ROI <15 dias” | `storytelling_summary.json` → `hero.kpis`, `forecast.band`, `sla_radar` | `Solucao-Completa-Resumida-Final.md`, `impacto-financeiro-prevía.md` |
| **Demand Intelligence** | Actual vs. forecast time series, anomaly ribbons, seasonality heatmap | “Precisão <15% MAPE mesmo com clima extremo” | `storytelling_timeseries.parquet` (per family) + `external_events` | `EXTERNAL_FACTORS_ML_MODELING_PT_BR.md`, `MARKET_ANALYSIS_INDUSTRY_WISDOM_PT_BR.md` |
| **Inventory & Logistics** | Geo inventory map, reorder alerts, lead-time stress gauge | “Alertamos 14 dias antes; buffer ajustado por risco de logística” | `storytelling_prescriptions.parquet` + `inventory_snapshot.json` | `INDUSTRY_STANDARDS_SUPPLY_CHAIN_DYNAMICS_PT_BR.md` |
| **Scenario Lab** | Slider-driven simulator, narrative cards, KPI deltas | “Planejamos cenários: clima, câmbio, SLA renewal” | `scenarioMatrix` (precomputed), `roi.projections` | `demo_dashboard_quick_strategy.md` |
| **External Signals** | Macro/climate waterfall, factor badges | “Integramos dados IBGE, BACEN, INMET para responder a choques” | `externalDrivers` array + `macro_history.parquet` | `EXTERNAL_FACTORS_ML_MODELING_PT_BR.md` |
| **Executive Console** | ROI gauge, action queue, PDF exporter | “Decisões executivas em 60s, com prova financeira” | `hero.kpis`, `alerts`, `roi` | `estrategia-competitiva-ceo.md`, `prevía-executive-summary-1page.md` |

### Widget Engineering Guide
- **KPI Strip** → Animated counters (React Spring), inline sparklines from 30-day slices.
- **Forecast Pulse** → Area chart with deterministic mock band; annotate events (`rainfall_spike`, `currency_crisis`).
- **Anomaly Timeline** → Stacked bar; tooltip narrates root cause referencing macro/weather features.
- **Reorder Alert Table** → Columns: `item`, `days_to_stockout`, `pp`, `lead_time`, `cta`. Button triggers modal with `Safety Stock` formula snippet.
- **Lead-Time Stress Gauge** → Semi-circle gauge; color-coded by `supplier_risk_score`.
- **Scenario Simulator** → Precomputed matrix; slider change fetches combination (no runtime calc needed for demo).
- **External Factor Waterfall** → Show additive impact to base forecast; highlight `Rainfall`, `USD/BRL`, `5G rollout`, `SLA renewal`.
- **ROI Meter & Action Queue** → Gauge + Kanban; CTA for downloading executive PDF.

### Data & Mocking Strategy
- **Demo Mode (now)**: rely on `demoSnapshot` TypeScript module with deterministic arrays.
- **BFF Transition (post-roadshow)**: connect to `storytelling_api_stub.py` endpoints, preserving identical interface.
- **Validation Hooks**: ensure widget props mirror naming from Gold layer (`forecast_accuracy`, `stockout_prevention`, `capital_savings`, `sla_health`).

### Implementation Sprints
#### Sprint “Ignite” (Today – Demo Ready)
1. Scaffold store/hooks (`useDemoSnapshot`, `useScenarioMatrix`).
2. Build hero tab + alert drawer with mock data.
3. Implement scenario lab + waterfall; wire demo tour overlay.
4. Polish brand tokens, responsive layout, export modal.

#### Sprint “Fusion” (Post-Roadshow, Week 1–2)
1. Swap mock store for real `useStorytellingKpis` etc. hitting BFF.
2. Add data validation overlay (flag drift using cues from ML pipeline).
3. Instrument telemetry (time-on-widget, CTA click tracking).
4. Integrate screenshot automation for pitch deck updates.

#### Sprint “Ascend” (Weeks 3+)
1. Expand scenario lab with cost-to-serve + predictive maintenance nodes.
2. Introduce personalization (filters by client tier, region, SLA window).
3. Add benchmarking comparisons vs. historical quarter.
4. Prepare multi-tenant theming for SaaS pivot.

### Messaging Cheat Sheet
- **SLA**: “Disponibilidade 99%+ garantida com alertas 14 dias antes de qualquer ruptura.” (Use during alert demo)
- **Financials**: “ROI em 0.1 mês; economia potencial R$ 56M/ano.” (Hero summary)
- **Differentiation**: “Integração multi-layer de dados (Bronze→Gold→Storytelling) + fatores externos = concorrência não alcança.” (External tab)
- **Operations**: “Equipe sai do modo reativo (‘apagar incêndio’) para planejar com base em risco.” (Scenario lab)

### Quality Gates
- Delta logging: confirm mock vs. production values align before enabling live endpoints.
- Demo rehearsals: run scripted flow 3×, time to <4 min; record fallback clip.
- Accessibility: ensure keyboard navigation across tabs, ARIA labels on charts/tooltips.

### Deliverables Tracker
- [ ] Frontend source updates (tabs, hooks, components).
- [ ] Demo assets (screenshots/GIFs for `pitch_deck.md`).
- [ ] Presenter cheat sheet (1-page summary referencing this masterplan).
- [ ] Rollout plan (JIRA/Notion tasks aligned with Sprint “Fusion” & “Ascend”).

### Next Actions
1. Implement remaining high-impact widgets per Ignite sprint list.
2. Update pitch deck slides with new UI captures and narrative copy.
3. Brief presenters using Messaging Cheat Sheet + demo walkthrough.
4. Schedule handoff meeting to align BFF integration and telemetry instrumentation.

