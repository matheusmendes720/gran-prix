## Demo Execution Scaffold – Hardcoded Data Strategy

### Immediate Goal
Stand up a fully presentable dashboard using deterministic mock data, ensuring every priority widget renders insights without relying on backend availability.

---

### 1. Populate `frontend/src/data/demoSnapshot.ts`
- **Structure**: copy the schema outlined in `demo_dashboard_quick_strategy.md` → `{ hero, demandSeries, reorderThreshold, alerts, externalDrivers, scenarioMatrix, roi, geoInventory }`.
- **Data Sources**:
  - **Synthetic generator**: leverage `backend/ml/data/data_loader.py` utilities (`DataLoader.engineer_features`) to create pseudo seasonality if desired.
  - **Fixed arrays**: craft deterministic arrays (length 90 for demand, 30 for forecast horizon) to keep animations stable.
- **Implementation Notes**:
  - Freeze timestamps (e.g., `generatedAt: '2025-11-12T09:30:00Z'`).
  - Include static `scenarioMatrix` lookup keyed by sliders (`{budget, weather, currency, sla}`).
  - Prepack `geoInventory` with lat/long + status for 6 demo towers.

---

### 2. Scaffold Demo Layout
| Section | Components | Data Hook | Notes |
|---------|------------|-----------|-------|
| Hero | `KpiStrip`, `ForecastPulse`, `SlaRadar` | `demoSnapshot.hero` | Mirror working KPI styling |
| Operational Dashboard | `DemandTimeline`, `AnomalyTimeline`, `SeasonalityHeatmap` | `demoSnapshot.demandSeries`, `externalDrivers` | Use existing chart libs |
| Alerts | `AlertDrawer`, `ActionQueue`, `InsightCards` | `demoSnapshot.alerts` | Color-code severity badges |
| Geo | `TowerMap`, `InventoryTable` | `demoSnapshot.geoInventory` | Static map placeholder acceptable |
| ROI | `RoiGauge`, `FinancialDeltaCards` | `demoSnapshot.roi` | Include call-to-action buttons |

- Create `layout/DemoShell` to manage tab/page sections without touching other working routes.
- Add demo-only routing guard or toggle (e.g., `?mode=demo`).

---

### 3. Widget Implementation Sequence
1. **KPI Strip** – animated counters with delta badges.
2. **Forecast Pulse** – dual-axis area chart with reorder line & events badges.
3. **Scenario Simulator** – slider inputs bound to `scenarioMatrix`.
4. **Alert Drawer** – list with inline CTA (“Gerar ordem de compra”).
5. **Geo Map/Table** – static Mapbox or choropleth with summary table.
6. **External Factor Waterfall** – contributions from rainfall, FX, 5G, SLA.
7. **ROI Gauge & Action Queue** – gauge plus Kanban-style recommendations.

Ensure each widget pulls from the deterministic data module and includes scripted tooltips (SLA, ROI stats).

---

### 4. Narrative Rehearsal Checklist
1. **Launch sequence**: confirm data loads instantly; autoplay scenario toggles.
2. **Story beats**: follow `demo_dashboard_quick_strategy.md` (Hero → Forecast → Inventory → Scenario → External → Executive).
3. **Fallback assets**: capture screenshots/GIFs for each beat.
4. **Presenter script**: align with Messaging Cheat Sheet (`frontend_feature_engineering_masterplan.md`).

---

### Synthetic Data Store (Optional Enhancement)
- **Purpose**: share the same mock dataset with AI agents or future BFF endpoints.
- **Approach**:
  - Create SQLite DB `demo/demo_dashboard.db`.
  - Tables: `hero_kpis`, `demand_series`, `alerts`, `external_drivers`, `scenario_matrix`, `geo_inventory`, `roi`.
  - Populate using a small Python script (`scripts/generate_demo_data.py`) that leverages `DataLoader` for seasonality & adds deterministic noise.
  - Provide lightweight FastAPI/Next.js API stub (`/api/demo/*`) reading from SQLite to feed both frontend and agents.
- **Benefits**: consistent data source, simple to export for agents, swap-in ready for production pipeline.

---

### Deliverables
- [ ] `demoSnapshot.ts` with deterministic data.
- [ ] Demo layout shell & sections wired to mock data.
- [ ] Priority widgets rendering mock insights.
- [ ] Rehearsal assets (script + media).
- [ ] Optional SQLite dataset + generator script outline.

