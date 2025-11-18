# Nova Corrente Frontend – Deep Analysis & UX Roadmap

## 1. Executive Summary
- **Scope**: Frontend apps under `frontend/` plus supporting assets in `nova-corrente-workspace/`. Includes dashboards, ML feature pages, notebooks, and generated ML outputs.
- **Objective**: Diagnose UI/UX, data & algorithm wiring, and produce a concrete roadmap for an interactive, storytelling-first predictive analytics experience.
- **Key Findings**: 
  - Pages rely heavily on mocked data despite rich ML outputs available in `workspace/ml-outputs/`.
  - Dual API clients (`lib/api.ts` vs `lib/api-client.ts`) diverge from FastAPI contracts; several methods called in components are undefined.
  - Clustering/model tabs attempt to hit endpoints that are stubs or unimplemented, yielding empty canvases.
  - UI styling is coherent but lacks responsive orchestration, accessibility semantics, and guided narratives for sales demos.

## 2. Current Asset Inventory
- **Frontend entry points**:
  - `app/page.tsx`: Demand dashboard using `KPIDashboard`, `MaterialsTable`, and `DemandChart`.
  - `app/main/page.tsx`: Legacy “Análises Aprofundadas” shell composing `Dashboard`, `Reports`, `Analytics`, `Settings`.
  - `app/features/*/page.tsx`: ML feature stories (temporal, climate, economic, 5g, lead-time, SLA, categorical, business, hierarchical).
  - `app/materials/[itemId]/page.tsx`: Item drill-down (requires BFF data).
- **Component families** (`src/components/`):
  - **Shared layout**: `Sidebar`, `Header`, `BackendStatus`, `ErrorBoundary`, `Toast*`.
  - **Dashboards**: `Dashboard`, `Analytics`, `ClusteringDashboard`, `ModelPerformanceDashboard`, `PrescriptiveRecommendations*`.
  - **Visualization**: `components/charts/*` using Recharts; `InteractiveMap`, `BrazilMap`.
  - **Data tables**: `MaterialsTable`, `AlertsTable`, `Reports`, `FavoriteReports`.
  - **Forms/Controls**: Inline date pickers, filters scattered in feature pages.
- **Data clients**:
  - `hooks/use-api.ts` + `lib/api-client.ts`: SWR hooks with typed responses for `/api/v1/*`.
  - `lib/api.ts`: Older client lacking climate, clustering, prescriptive methods but still imported by several components (`BackendStatus`, `ClimateTimeSeriesChart`, `PrescriptiveRecommendationsEnhanced`), causing runtime `undefined` fetchers.
- **Workspace assets**:
  - ML notebooks (`workspace/dashboard-notebooks/*.ipynb`) for quick visuals.
  - `workspace/ml-outputs/` – parquet/CSV/JSON artifacts covering forecasts, prescriptive JSONs, feature manifests.
  - `workspace/frontend-improvements/improvements-summary.json` – prior roadmap seeds.

### Selected Code References
```37:43:frontend/src/app/features/layout.tsx
          <Header
            title="ML Features Dashboard"
            subtitle="Visualização de features de machine learning para previsão de demanda"
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
          />
```

```118:128:frontend/src/components/KPIDashboard.tsx
        <KPICard
          title="MAPE Forecast"
          value={latestKPI?.forecast_mape ?? 0}
          trend={mapeTrend}
          unit="%"
          description="Erro médio de previsão"
          isLoading={isLoading}
        />
```

```27:41:frontend/src/components/charts/ClimateTimeSeriesChart.tsx
        const [climateResponse, salvadorResponse] = await Promise.all([
          apiClient.getClimateFeatures(materialId, startDate, endDate),
          apiClient.getSalvadorClimate(startDate, endDate),
        ]);
```

## 3. UX & Storytelling Diagnostics
- **Empty states**: Clustering and models tabs render blank panels when the backend is offline or returns stub data (no guided message or sample dataset fallback).
- **Mock data overload**: Core dashboards (`Dashboard.tsx`, `Analytics.tsx`) hardcode inventory, supplier, and alert values. This undermines credibility for live demos.
- **Backend coupling**: Components assume `http://localhost:5000` (see `BackendStatus.tsx`) instead of respecting `NEXT_PUBLIC_API_URL`, complicating deployments.
- **Accessibility**: Buttons served as `<div>` or `<button>` without `aria-*`, no keyboard trap prevention in modals, minimal focus outlines.
- **Responsive gaps**: Sidebars hidden on mobile without replacement navigation, charts overflow on small screens, and data tables lack responsive virtualization.
- **Narrative flow**: Feature pages provide introductory cards but lack guided storylines (no scenario toggles, no “so what” callouts). Alerts -> analytics journey is manual.
- **Localization**: Mixed Portuguese/English labels, inconsistent plurals, lacks i18n scaffolding for future markets.

## 4. Data & Algorithm State
- **Backend APIs**: Many FastAPI routes in `backend/app/api/v1/routes` remain TODO stubs (e.g., `metrics`, `items`). Feature routes (temporal/climate lead-time) execute SQL via `database_service`. Forecast outputs exist offline but are not exposed via `/api/v1`.
- **ML Outputs**: 
  - Forecasts: `workspace/ml-outputs/data/consolidated_forecast_*.json` (family-level) and item/site parquet files.
  - Prescriptive recommendations: `item*_prescriptive.json` with `reorder_point`, `safety_stock`, `stock_status`.
  - Feature manifests: `gold-layers/feature_manifest.json` enumerating engineered columns.
- **Data gaps**: Frontend types (e.g., `Alert`, `PrescriptiveRecommendation`) do not align with backend schema. Methods such as `apiClient.getClimateFeatures` and `getPrescriptiveRecommendations` are undefined in `lib/api.ts`, causing runtime failures.
- **BFF Recommendation**:
  1. **Aggregation layer** (FastAPI or Node BFF) reading parquet/JSON from `workspace/ml-outputs` or Postgres.
  2. Provide coarse-grained endpoints:
     - `GET /bff/dashboard/summary`: KPIs, demand vs forecast, stockout risk.
     - `GET /bff/alerts`: join prescriptive JSON + forecast risk for UI cards.
     - `GET /bff/forecasts/{item_id}`: merge forecast parquet with metadata.
     - `GET /bff/features/{category}`: wrap SQL queries into compact payloads.
     - `GET /bff/geospatial/towers`: provide GeoJSON for Brazil map overlays.
  3. Introduce caching & snapshot versioning via manifest metadata (e.g., `feature_manifest.json` timestamp).

## 5. Interactive Enhancement Blueprint
### 5.1 Widget Concepts
- **Storytelling timeline**: Animated slider syncing demand, stock levels, and prescriptive actions.
- **Geo-impact map**: Use deck.gl or Mapbox to display tower performance, weather alerts, and SLA risks (feed from `storytelling_timeseries.parquet` + weather dims). ✅ MVP live via `GeoHeatmap` with regional corrosion risk overlays and tooltip narrative.
- **Forecast scenario explorer**: ✅ Demand chart now ships with demand spike & lead-time sliders that derive a simulated forecast curve, highlight safety stock deltas, and narrate recommended replenishment moves.
- **Climate feature storyline**: ✅ `/features/climate` consome `/bff/features/climate`, exibe insights automáticos (corrosão, campo) e guia narrativo com dados do feature store macro-climate.
- **Scenario propagation**: ✅ Sliders alimentam alertas/recomendações com PP ajustado, estoque de segurança e narrativa de buffer (ver `STORYTELLING_SCENARIO_GUIDE.md`).
- **Scenario simulator**: Controls to adjust lead time, demand spike, or supplier failure with live recalculation from prescriptive JSON (simple front-end calc).
- **Comparative KPI board**: Multi-series charts for baseline vs optimized ROI leveraging `metrics_summary.json`.
- **Feature spotlight carousels**: Narrative modules summarizing “Why climate matters”, “SLA violation forecast” with supporting visuals.

### 5.2 UX & Branding Guidelines
- Harmonize typography (pair sans-serif headlines with numeric monospace when showing metrics).
- Define responsive layout grid (12-column desktop, 6-column tablet, stacked mobile).
- Expand color system: add semantic palettes (`success`, `warning`, `critical`) with contrast checks.
- Provide microcopy guidelines: Portuguese-first with consistent voice; remind about ROI impact near key actions.
- Accessibility targets: WCAG 2.1 AA; add focus indicators, keyboard navigation, ARIA for charts (summary text + table export).

### 5.3 Testing Strategy
- **Component**: Strengthen Jest + React Testing Library coverage for data-bound components using MSW to mock BFF responses.
- **Visual regression**: Integrate Playwright screenshot testing for dashboards to ensure chart theming stability.
- **Performance**: Lighthouse CI for core flows; watch TTI/CLS when loading large chart datasets by enabling lazy loading & virtualization.
- **Storytelling demos**: Record deterministic test scripts that load curated snapshot data (frozen JSON) for sales pitch rehearsals.

## 6. Implementation Roadmap
### Phase 0 – Foundations (Week 0-1)
- Stand up BFF prototype exposing dashboard summary/alerts/forecast endpoints.
- Normalize API client (`lib/api.ts`) to consume BFF; deprecate duplicates.
- Implement feature flags to toggle between mock data and live data for demo readiness.

### Phase 1 – Data-Driven Dashboards (Week 1-3)
- Replace mock KPI and alert data with BFF responses.
- Build reusable chart adapters mapping parquet/JSON to Recharts (with streaming placeholders).
- Implement prescriptive panel using actual `*_prescriptive.json` fields (stock status, reorder point).

### Phase 2 – Feature Storytelling (Week 3-5)
- Connect climate, economic, SLA pages to feature endpoints with caching and pagination.
- Design interactive map overlay using enriched datasets; integrate clustering metrics once APIs live.
- Add narrative tooltips, guided walkthrough modals, and scenario toggles per feature tab.

### Phase 3 – Experience Polish (Week 5-7)
- Introduce responsive layout revamp, accessibility improvements, theming tokens.
- Add onboarding flows (tour, glossary popovers), export features (PDF/CSV).
- Instrument analytics (user interactions, time-on-chart) for validation metrics.

### Phase 4 – Production Hardening (Week 7-8)
- Implement automated test suites (unit + Playwright).
- Add resilience features: offline banners, retry logic, fallback snapshots.
- Document runbooks, API contracts, and create customer-facing storytelling scripts.

## 7. Backlog (Top-Down & Bottom-Up)
| Horizon | Initiative | Description | Owners | Dependencies |
|---------|------------|-------------|--------|--------------|
| Strategic | Storytelling Experience | Align dashboards with pitch narrative (discover → diagnose → prescribe). | Product + Design | BFF, real datasets |
| Strategic | Live Demo Mode | Toggle between live and curated data snapshots. | Frontend | Snapshot curation |
| Tactical | API Harmonization | Merge `api-client` and `api` modules; enforce typed hooks. | Frontend | BFF schema |
| Tactical | Forecast Explorer | Item-level drill-down with confidence intervals & scenario slider. | Frontend + DS | Forecast parquet |
| Tactical | Prescriptive Feed | Real-time alerts with impact/urgency scoring from prescriptive JSON. | Frontend + DS | BFF aggregator |
| Operational | Accessibility Pass | Landmark structure, keyboard nav, screen-reader friendly charts. | Frontend QA | Component refactor |
| Operational | Performance Budget | Lazy load heavy charts, implement data virtualization. | Frontend | BFF pagination |

### Detailed Task Buckets
- **Data Layer**: Snapshot manifest loader, parquet → JSON adapters, caching strategy (Redis optional).
- **UI Layer**: Navigation redesign, responsive grid, new map component, KPI cards wired to live data.
- **Storytelling**: Content authoring for feature intros, playbook for sales demo, interactive scenario scripts.
- **QA/DevEx**: Test harness updates, lint/test pipeline enforcement, monitoring dashboards for API health.

## 8. Validation & Metrics
- **Engagement**: Chart interaction rate (>60% of sessions), map selection events.
- **Data Freshness**: Dashboard data <= 2 hours behind latest batch; BFF health checks exposed to UI.
- **Accuracy**: Prescriptive alerts validated against ML outputs (100% parity with `*_prescriptive.json`).
- **Performance**: TTI < 4s on mid-tier laptop; Lighthouse scores > 85 mobile/desktop.
- **Demo Readiness**: Curated scenario loads under 10s; script coverage for all storytelling beats.
- **Geo Engagement**: 30% of users interact with map layers (zoom, filter, tooltip) during demos.
- **Accessibility**: WCAG 2.1 AA audit ≥ 90% pass rate across primary flows (keyboard nav, contrast, ARIA labels).

## 9. Next Steps & Deliverables
- Finalize BFF schema document and align backend team on implementation timeline.
- Conduct design workshop to define rebranding tokens, responsive grid, and storyboard.
- Schedule weekly check-ins (Design Ops Mondays, Eng Sync Wednesdays, Demo Prep Fridays).
- Prepare curated demo dataset (freeze snapshots) and integrate toggle into frontend.
- Prototype geo/heatmap widget using storytelling geo artifacts; define map design spec (layers, legends, interactions).
- Execute accessibility polish sprint (focus indicators, semantic markup, keyboard shortcuts) and prepare checklist for QA.

### 9.1 Demo Narrative (Sales Pitch Flow)
1. **Context Hook** – Start on the main dashboard with live KPI deltas (MAPE, SLA) to frame ROI (+194%).
2. **Diagnose** – Drill into alerts panel, highlighting prescriptive advice with urgency badges; pivot to analytics tab filtered by impacted state via `onSelectAlert`.
3. **Explain Drivers** – Navigate to feature tabs (climate → economic) using guided tooltips to show how external factors influence demand forecasts.
4. **Simulate** – Launch scenario sidebar (lead time vs demand spike) to demonstrate reorder point adjustments in real time.
5. **Geo Story** – Open interactive Brazil map, spotlighting towers at risk and overlaying weather clusters, linking back to SLA narrative.
6. **Close** – Showcase prescriptive export (PDF/CSV) and emphasize automation + early warning cycle; end with next steps CTA.

## 10. Reference Materials
- Strategic context: `docs/proj/strategy/STRATEGIC_BUSINESS_PROBLEM_SETUP_PT_BR.md`, `MARKET_ANALYSIS_INDUSTRY_WISDOM_PT_BR.md`.
- ML pipeline spec: `workspace/analysis-reports/NOVA_CORRENTE_ML_PIPELINE_TECH_SPEC.md`.
- Improvement seeds: `workspace/frontend-improvements/improvements-summary.json`.

---
**Maintainers**: Frontend Guild @ Nova Corrente  
**Last Updated**: 2025-11-12  
**Next Review**: Align with BFF delivery (target Week 1 phase gate).


