## Go-Horse Roadshow Index – Demo Blitz Playbook

### 0. Mission Snapshot
- **Objective**: Ship a “looks-live” predictive analytics dashboard in under an hour for the Nova Corrente roadshow using deterministic mock data.
- **Focus**: Frontend storytelling, interactive widgets, hardcoded datasets, and scripted narrative. Forget deployment & backend reliability for now.
- **Audience**: Executives, operations, procurement—prove ROI, SLA protection, and intelligence breadth instantly.

---

### 1. Rapid Timeline (T-60 → T+0)
| Time | Action | Key Docs / Assets |
|------|--------|-------------------|
| T-60 | Align demo scope, load `demoSnapshot.ts` or SQLite mock | `demo_dashboard_quick_strategy.md`, `demo_execution_scaffold.md` |
| T-45 | Scaffold layout + tab navigation (Hero, Features, Main) | `frontend_feature_engineering_masterplan.md` |
| T-30 | Implement priority widgets (KPI → Forecast → Scenario → Alerts → Map → Waterfall → ROI) | `demo_execution_scaffold.md` |
| T-20 | Fill `/features` tabs with deterministic visuals | `features_route_planning.md`, per-feature specs |
| T-15 | Populate `/main` analytics (Formulas, Clustering, Modelos) | `specs_main_analytics_overview.md` |
| T-10 | Hook narrative tooltips, CTA links, autoplay | `demo_dashboard_quick_strategy.md` |
| T-05 | Rehearse scripted flow, capture screenshots backup | `frontend_feature_engineering_masterplan.md`, Messaging cheat sheet |
| T-00 | Deliver demo using walkthrough script | `demo_dashboard_quick_strategy.md` |

---

### 2. Core Documents (What to Read & When)
1. **Strategy & Storytelling**
   - `demo_dashboard_quick_strategy.md` – 60-minute demo flow + narrative.
   - `frontend_feature_engineering_masterplan.md` – Ignite/Fusion/Ascend sprints, messaging cheatsheet.
2. **Execution Planning**
   - `demo_execution_scaffold.md` – immediate tasks for mock data & widgets.
   - `features_route_planning.md` + `main_route_planning.md` – route-level experience architecture.
3. **Feature Specs**
   - `/features/*` specs (Temporal, Climate, Economic, 5G, Lead Time, SLA, Hierarchical, Categorical, Business).
   - `/main` specs: `specs_main_formulas.md`, `specs_main_analytics_overview.md`, `main_models_clustering_breakdown.md`.
4. **Strategic Context**
   - `Solucao-Completa-Resumida-Final.md` + business docs for messaging pull quotes.

---

### 3. Mock Data Plan
- **Primary Source**: `frontend/src/data/demoSnapshot.ts`.
- **Optional DB**: `demo_dashboard.db` (SQLite) with tables: `hero_kpis`, `demand_series`, `alerts`, `external_drivers`, `scenario_matrix`, `geo_inventory`, `formulas_config`, `clusters`, `models`.
- **Generator**: Use `backend/ml/data/data_loader.py` to seed pseudo-seasonal data (temporal features, climate simulation).
- **Guarantees**: deterministic arrays, seeded randomness (e.g., `np.random.seed(42)`), timestamps frozen to demo day.

---

### 4. Widget Priority Stack
1. **Hero Overview** – KPI strip, Forecast Pulse, SLA Radar.
2. **Scenario Lab** – sliders map to `scenarioMatrix`, auto-narrative.
3. **Alerts & Action Queue** – severity badges, CTA modals.
4. **External Signals** – waterfall (rainfall, FX, 5G, SLA renewal).
5. **Geo Inventory** – map + table, status chips.
6. **ROI Gauge & Exec Console** – payback timeline, action cards.
7. **/features Tabs** – Signal spotlights (temporal, climate, economic, etc.).
8. **/main Formulas** – calculators + charts per formula.
9. **Clustering & Modelos** – ensemble performance, cluster storytelling.

---

### 5. Storytelling Cheat Sheet (Pitch Sequence)
1. **Problem Hook** – SLA penalties, manual planning (quote from strategy docs).
2. **Hero KPIs** – Forecast accuracy 92%, stockout prevention 80%, ROI 1.6x.
3. **Forecast Pulse** – show confidence bands, highlight storm alert.
4. **Inventory / Lead Time** – drill to procurement action (PP & SS calculators).
5. **Scenario Lab** – adjust weather severity; narrate proactive decision.
6. **External Signals** – demonstrate macro/climate integration.
7. **Models** – ensemble slider, accuracy gauges (MAPE 10.5%).
8. **Clustering** – show equipment failure cluster with recommended actions.
9. **Executive Console** – ROI meter, action queue, PDF export.
10. **Close** – “Ready for rollout; backend swap-in after roadshow.”

---

### 6. Callouts & Messaging Anchors
- **SLA**: 99%+, penalties 2–10% contract value. Use SLA tab for visual proof.
- **Financial**: Payback < 0.1 month; R$56M/year savings (ref `Solucao-Completa-Resumida-Final.md`).
- **Differentiators**: multi-layer data integration, external drivers, ensemble ML, proactive alerts.
- **Operations**: “Equipe deixa modo reativo → planejamento orientado a risco.”

---

### 7. To-Do Blitz (Check Before Demo)
- [ ] Populate `demoSnapshot.ts` (hero, demand, alerts, external drivers, scenario matrix, geo, ROI, formulas, clusters, models).
- [ ] Implement shared frontend components (KPI strip, ChartPanel, ScenarioDeck, etc.).
- [ ] Fill `/features` and `/main` tabs with deterministic visuals.
- [ ] Wire navigation CTAs (even if stubbed).
- [ ] Script tooltips & copy referencing strategy docs.
- [ ] Run through storytelling once; record backup capture.
- [ ] Prepare presenter notes + cheat sheet.

---

### 8. After Roadshow (Nice-to-Haves)
- Swap mock data for BFF endpoints (FastAPI) when ready.
- Add telemetry and analytics.
- Automate export (PDF/CSV) for stakeholders.
- Integrate action queue with backend workflows.
- Expand scenario lab (cost-to-serve, predictive maintenance).

---

### 9. Quick Links
- Strategy: `Solucao-Completa-Resumida-Final.md`
- Demo Blueprint: `demo_dashboard_quick_strategy.md`
- Execution Scaffold: `demo_execution_scaffold.md`
- Frontend Masterplan: `frontend_feature_engineering_masterplan.md`
- Route Plans: `features_route_planning.md`, `main_route_planning.md`
- Feature Specs: `specs_features_*.md`
- Main Analytics Specs: `specs_main_formulas.md`, `specs_main_analytics_overview.md`
- Clustering/Modelos Breakdown: `main_models_clustering_breakdown.md`

---

**Remember:** Go-horse mode—hardcode, fake it, make it shine. Demo > perfection. Once the roadshow is done, we circle back for proper integrations. Good luck! 💥


