## Predictive Analytics Dashboard — 60-Minute Demo Playbook

### Objective
- Prove Nova Corrente’s AI-powered demand foresight during the roadshow using a polished, “looks-live” frontend.
- Juxtapose business problem framing (`STRATEGIC_BUSINESS_PROBLEM_SETUP_PT_BR.md`) with ML differentiators (`EXTERNAL_FACTORS_ML_MODELING_PT_BR.md`) and industry benchmarks (`INDUSTRY_STANDARDS_SUPPLY_CHAIN_DYNAMICS_PT_BR.md`, `MARKET_ANALYSIS_INDUSTRY_WISDOM_PT_BR.md`).
- Deliver scripted storytelling that highlights SLA protection, inventory intelligence, and ROI impacts without relying on production data.

### Guiding Principles
- **Speed over fidelity**: mock deterministic datasets crafted to support the narrative.
- **Story-first UX**: every widget echoes a key talking point from the strategic docs.
- **Confidence theater**: blend motion, alerting, and scenario toggles to show “alive” intelligence.
- **Executive clarity**: surface ROI, SLA, and risk mitigation metrics above the fold.

### Dashboard Topology
1. **Hero Overview** – KPI ribbon, forecast pulse chart, SLA risk radar.
2. **Demand Intelligence** – time-series with confidence band, anomaly timeline, seasonality heatmap.
3. **Inventory & Logistics** – geo inventory map, lead-time stress gauge, reorder alert table.
4. **Scenario Lab** – slider-driven what-if controls, instant narrative cards.
5. **External Signals** – macro & climate contribution waterfall, factor badges.
6. **Executive Console** – ROI meter, action queue, downloadable executive summary.

### Widget Catalogue
- **KPI Strip**: auto-animated cards for `Forecast Accuracy 92%`, `Stockout Prevention 80%`, `Capital Savings 18%`, `SLA Health 99.2%`.
- **Forecast Pulse**: dual-axis area chart (demand vs. reorder line) with storm/holiday badges.
- **Supply Stress Radar**: polar chart covering `Lead Time`, `Supplier Risk`, `Cash Pressure`, `SLA Exposure`, `Weather`.
- **Seasonality Heatmap**: week × hour matrix referencing Bahia climate seasonality.
- **Anomaly Timeline**: stacked actual vs. predicted, click reveals root cause from scenario scripts.
- **Geo Inventory**: Mapbox scatter for tower clusters + linked table with status chips.
- **Alert Drawer**: severity-tagged insights (“Greve transporte → +12d lead time”).
- **Scenario Simulator**: sliders (`Inventory Budget`, `Weather Stress`, `Currency Shock`, `SLA Target`) producing precomputed KPI deltas.
- **External Waterfall**: contributions from rainfall, FX volatility, 5G rollout, SLA renewal cycles.
- **ROI Meter & Action Queue**: gauge chart plus Kanban cards for Procurement, Ops, Finance.

### Mock Data Blueprint
```typescript
export const demoSnapshot = {
  generatedAt: '2025-11-12T09:30:00Z',
  hero: {
    kpis: [
      { id: 'forecast_accuracy', label: 'Forecast Accuracy', value: 0.92, delta: +0.03 },
      { id: 'stockout_prevention', label: 'Stockout Prevention', value: 0.80, delta: +0.05 },
      { id: 'capital_savings', label: 'Capital Savings', value: 0.18, delta: +0.02 },
      { id: 'sla_health', label: 'SLA Availability', value: 0.992, delta: +0.004 },
    ],
    narrative: 'IA assegura 60% menos rupturas e preserva SLAs 99%+ sob clima extremo.'
  },
  demandSeries: generateTimeSeries({ base: 340, noise: 22, anomalies: [...] }),
  reorderThreshold: generateThresholdSeries(...),
  alerts: [
    { severity: 'critical', title: 'Connector Óptico', message: 'Ruptura em 7 dias; comprar 250 unidades', tags: ['SLA', 'Finance'] },
    { severity: 'warning', title: 'Refrigeração RF', message: 'Greve transporte → lead time +12 dias', tags: ['Logística'] },
    { severity: 'info', title: '5G Rollout', message: '18 cidades novas exigem kits RF em 15 dias', tags: ['Crescimento'] }
  ],
  externalDrivers: [
    { factor: 'Rainfall', impactPct: +18, description: 'Chuva >50mm: +40% demanda estrutural' },
    { factor: 'USD/BRL Volatility', impactPct: +12, description: 'Câmbio variou 11% em 30 dias' },
    { factor: '5G Rollout', impactPct: +9, description: 'Cobertura 5G libera upgrades planejados' },
    { factor: 'SLA Renewal Cycle', impactPct: +15, description: 'Jan/Jul renovação aumenta preventivas em 30%' }
  ],
  scenarioMatrix: precomputeScenarioGrid(),
  roi: { paybackMonths: 9, year1ROI: 1.6, cumulativeSavings: 280000 },
  geoInventory: loadGeoFeatures()
};
```
- Utility helpers (`generateTimeSeries`, `precomputeScenarioGrid`, `loadGeoFeatures`) output deterministic arrays that reinforce scripted insights.

### Interaction & Motion Hooks
- Launch with `Demo Mode` (React Joyride) overlay guiding the story beats.
- Auto-play toggles scenario sliders every 15 s to suggest real-time intelligence.
- Alerts trigger icon glow + subtle audio ping at severity thresholds.
- Tooltip copy quotes strategic stats (SLA penalties, ROI, weather impacts).
- Fake “Download Executive Summary” modal confirms output to impress executives.

### Storytelling Script (4-minute pitch)
1. **Problem & UVP** – highlight hero KPIs, cite `-60% rupturas`, `ROI 6–12 meses`.
2. **Forecast Pulse** – show confidence band; call out storm alert and proactive reorder.
3. **Inventory & Logistics** – drill into `American Tower` cluster; mention SLA penalties.
4. **Scenario Lab** – drag “Weather Stress”, narrate how lead-time buffer saves SLA.
5. **External Signals** – link rainfall + FX spikes to demand surge using waterfall.
6. **Executive Console** – close with ROI gauge and action queue, offer PDF export.

### Delivery Checklist (Next 60 Minutes)
1. Scaffold mock data (`frontend/src/data/demoSnapshot.ts`) and Zustand store.
2. Build layout + tab navigation (`app/page.tsx`, `components/TabShell.tsx`).
3. Implement KPI strip, forecast chart, radar, heatmap with preferred chart libs.
4. Wire alert drawer, scenario sliders, waterfall, and ROI gauge with precomputed outputs.
5. Add demo mode overlay + autoplay toggles.
6. Polish styling (color tokens, typography, icons) to match Nova Corrente branding.
7. Dry-run pitch using scripted beats; capture screenshots/GIFs as backup.

### Risk Mitigation
- **Time crunch**: prioritize hero + scenario tabs first; fallback is static screenshots.
- **Data credibility**: embed footnotes referencing strategic docs to justify narratives.
- **Technical hiccups**: package static build or record Loom as safety net.

### Stakeholder Prep
- Share doc + demo link with presenters 15 min before roadshow.
- Provide one-pager cheat sheet summarizing KPIs, scenarios, and call-to-actions.
- Align on Q&A responses (e.g., “Yes, backend pipeline already ingesting IBGE/BACEN per roadmap”).

### Next Steps Post-Roadshow
- Swap demo mocks with real BFF endpoints (`plan: backend-for-frontend + ML outputs`).
- Layer in live drift monitoring (Great Expectations + TFT ensemble) per ML roadmap memory.
- Expand scenario lab to include cost-to-serve and predictive maintenance insights.

