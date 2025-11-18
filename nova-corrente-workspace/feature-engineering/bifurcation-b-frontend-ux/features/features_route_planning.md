## `/features` Route – ML Feature Intelligence Plan

### Goal
Transform the currently empty ML feature tabs into a guided exploration of Nova Corrente’s unique signal stack (Temporal, Climate, Economic, 5G, Lead Time, SLA, Hierarchical, Categorical, Business) without touching widgets that already work on other routes.

### Experience Pillars
1. **Signal Spotlight Cards** – one hero card per feature family with KPI deltas, confidence, and last refresh time.
2. **Diagnostics Drilldowns** – per-feature charts/tables explaining how that factor influences demand, reorder points, and SLA risk.
3. **Actionable Playbooks** – contextual “What to do now?” guidance mapped to Procurement, Operações, Financeiro.

### Tab Structure Blueprint
| Tab | Empty State Today | Target Experience | Data Hooks | Notes |
|-----|-------------------|-------------------|------------|-------|
| Temporal | Static menu only | Seasonality heatmap + weekday trend + forecast decomposition | `timeseries.temporal_summary` | Reuse working formulas for explanation copy |
| Climate | No content | Weather-impact tiles (rainfall, humidity, wind) + storm alert timeline | `externalDrivers.weather`, `alerts.climate` | Align with climate narrative from strategic docs |
| Economic | No content | FX & inflation shock gauge + procurement cost scenarios | `externalDrivers.economic`, `roi.macrosensitivity` | Keep consistent with ROI messaging |
| 5G | No content | Coverage expansion map + equipment demand uplift | `externalDrivers.5g`, `inventory.projects` | Leverage tower geo data |
| Lead Time | No content | Supplier heatmap + backlog waterfall + ETA forecast | `prescriptions.lead_time_panel` | Tie to reorder calculator |
| SLA | No content | SLA breach risk meter + mitigation checklist | `hero.sla_health`, `alerts.sla` | Reuse working SLA KPIs |
| Hierarchical | No content | Parent-child demand rollup chart + variance table | `timeseries.hierarchical` | Show aggregated vs. SKU level |
| Categorical | No content | Feature importance bar chart + categorical split table | `models.feature_importance` | Focus on explainability |
| Business | No content | Cashflow vs. inventory view + executive KPIs | `roi`, `hero.kpis` | Mirror executive console narrative |

### Interaction Concepts
- Breadcrumb navigation between `/features` clusters and `/main` overview (no route changes yet; document desired UX).
- Side drawer for glossary/FAQ (reuse existing copy from strategic docs).
- Export button per feature to download related CSV/insight PDF.

### KPIs & OKRs
- **Adoption**: time-on-tab ≥ 30s for at least 6 feature families per demo.
- **Comprehension**: add tooltips referencing equations (PP, Safety Stock) where relevant.
- **Actionability**: each tab surfaces at least one recommended next step linked to alerts queue.

### Backlog (No Code Yet)
1. Define data contracts for each feature family (mock vs. production).
2. Outline widget specs (charts, tables, copy) per tab.
3. Draft narrative snippets linking feature insight → business impact.
4. Map dependencies with working widgets to avoid regressions.
5. Document navigation expectation (tabs ↔ `/main`) for future routing work.

