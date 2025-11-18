# Demo Dashboard Next Steps — Bifurcated Roadmap by Feature Engineering

## 📊 Executive Summary

This document splits the "Next Steps" from `demo_dashboard_quick_strategy.md` into **two bifurcations** organized by feature engineering sub-tabs/pages:

- **Bifurcation A**: Feature Engineering & Data Integration (Backend/ML Focus)
- **Bifurcation B**: Frontend Story-Telling & UX/UI Improvements (Frontend Focus)

Each bifurcation is further organized by route (`/features` vs `/main`) and sub-tabs, with deep analysis of story-telling and UX/UI improvement plans.

---

## 🗺️ Feature Route Classification

### `/features` Route (9 Feature Tabs)

| Tab | Feature Family | Current State | Target Experience | Data Hooks |
|-----|---------------|---------------|-------------------|------------|
| **Temporal** | Time-based patterns | Static menu only | Seasonality heatmap + weekday trend + forecast decomposition | `timeseries.temporal_summary` |
| **Climate** | Weather impacts | No content | Weather-impact tiles (rainfall, humidity, wind) + storm alert timeline | `externalDrivers.weather`, `alerts.climate` |
| **Economic** | FX & macro | No content | FX & inflation shock gauge + procurement cost scenarios | `externalDrivers.economic`, `roi.macrosensitivity` |
| **5G** | Network expansion | No content | Coverage expansion map + equipment demand uplift | `externalDrivers.5g`, `inventory.projects` |
| **Lead Time** | Supplier logistics | No content | Supplier heatmap + backlog waterfall + ETA forecast | `prescriptions.lead_time_panel` |
| **SLA** | Service level | No content | SLA breach risk meter + mitigation checklist | `hero.sla_health`, `alerts.sla` |
| **Hierarchical** | Aggregations | No content | Parent-child demand rollup chart + variance table | `timeseries.hierarchical` |
| **Categorical** | Feature importance | No content | Feature importance bar chart + categorical split table | `models.feature_importance` |
| **Business** | Financial metrics | No content | Cashflow vs. inventory view + executive KPIs | `roi`, `hero.kpis` |

### `/main` Route (3 Sub-tabs)

| Sub-tab | Current Issue | Target Experience | Dependencies |
|---------|---------------|-------------------|--------------|
| **Modelos** | Backend unavailable | Ensemble performance dashboard with accuracy trends, confidence intervals, model lineage cards | `storytelling_timeseries`, `models.metrics`, `alerts.model` |
| **Clustering** | Backend unavailable | Visualize equipment failure clusters & tower performance segments, each with quick insights + link to feature tabs | `analytics.clusters`, `inventory.geo` |
| **Prescritivo** | Empty (planned) | Prescriptive playbook board: recommended purchase orders, SLA interventions, cashflow impacts | `storytelling_prescriptions`, `roi` |

---

## 🔀 Bifurcation A: Feature Engineering & Data Integration

**Focus**: Backend/ML infrastructure, data pipelines, model enhancements, BFF integration

### A.1 `/features` Route — Data Integration Tasks

#### A.1.1 Temporal Feature Tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/features/temporal/summary` endpoint
  - Aggregate seasonality patterns from `timeseries.temporal_summary`
  - Return weekday trends, monthly seasonality, forecast decomposition
  - Cache results for 1 hour (Redis)
- [ ] **Data Pipeline**: Enhance temporal feature extraction
  - Add Brazilian holiday regressors (Carnaval, Festa Junina)
  - Implement cyclical encoding (hour of day, day of week, month)
  - Calculate lag features (7-day, 30-day moving averages)
- [ ] **ML Model Integration**: Connect Prophet/ARIMA outputs
  - Expose forecast decomposition (trend, seasonality, residuals)
  - Provide confidence intervals for seasonality components

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Seasonality Heatmap** → Week × Hour matrix with Bahia climate patterns
- **Sub-tab 2: Weekday Trends** → Day-of-week demand patterns with confidence bands
- **Sub-tab 3: Forecast Decomposition** → Trend/seasonality/residual breakdown

#### A.1.2 Climate Feature Tab
**Next Steps:**
- [ ] **External Data Integration**: Connect INMET API for real-time weather
  - Rainfall data (daily aggregates)
  - Humidity, wind speed, temperature
  - Storm alert triggers (>50mm rainfall threshold)
- [ ] **BFF Endpoint**: Create `/api/v1/features/climate/impacts`
  - Map weather events to demand anomalies
  - Calculate correlation coefficients (rainfall → demand)
  - Generate storm alert timeline
- [ ] **Feature Engineering**: Climate impact features
  - Rainfall intensity buckets (0-25mm, 25-50mm, 50mm+)
  - Humidity stress index
  - Wind damage risk score

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Weather Impact Tiles** → Rainfall, humidity, wind cards with KPI deltas
- **Sub-tab 2: Storm Alert Timeline** → Chronological weather events with demand impact
- **Sub-tab 3: Climate-Demand Correlation** → Scatter plots showing weather → demand relationships

#### A.1.3 Economic Feature Tab
**Next Steps:**
- [ ] **External Data Integration**: Connect BACEN API for FX/economic data
  - USD/BRL exchange rate (daily)
  - Inflation indices (IPCA)
  - Interest rates (SELIC)
- [ ] **BFF Endpoint**: Create `/api/v1/features/economic/shocks`
  - Calculate FX volatility (30-day rolling std dev)
  - Map currency shocks to procurement cost impacts
  - Generate economic scenario projections
- [ ] **Feature Engineering**: Economic impact features
  - FX volatility index (normalized 0-1)
  - Procurement cost multiplier (FX-adjusted)
  - Inflation-adjusted demand forecasts

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: FX & Inflation Shock Gauge** → Real-time currency/inflation meters
- **Sub-tab 2: Procurement Cost Scenarios** → What-if analysis for FX fluctuations
- **Sub-tab 3: Economic-Demand Correlation** → Macro factors → demand impact waterfall

#### A.1.4 5G Feature Tab
**Next Steps:**
- [ ] **External Data Integration**: Connect ANATEL API for 5G coverage data
  - 5G tower deployment locations
  - Coverage expansion timeline
  - Equipment demand projections
- [ ] **BFF Endpoint**: Create `/api/v1/features/5g/expansion`
  - Map 5G rollout to equipment demand uplift
  - Calculate demand multipliers per city/region
  - Generate equipment requirement forecasts
- [ ] **Feature Engineering**: 5G impact features
  - Coverage expansion index (0-100%)
  - Equipment demand multiplier (1.0x - 2.5x)
  - Project timeline features (days until rollout)

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Coverage Expansion Map** → Interactive map showing 5G rollout + demand hotspots
- **Sub-tab 2: Equipment Demand Uplift** → Bar charts showing RF kit requirements per city
- **Sub-tab 3: Project Timeline** → Gantt-style view of 5G rollout schedule

#### A.1.5 Lead Time Feature Tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/features/lead-time/analysis`
  - Aggregate lead time by supplier/family
  - Calculate supplier risk scores
  - Generate ETA forecasts with confidence intervals
- [ ] **Data Pipeline**: Lead time feature extraction
  - Historical lead time distributions
  - Supplier reliability scores (on-time delivery %)
  - Backlog analysis (pending orders)
- [ ] **ML Model Integration**: Lead time prediction model
  - Forecast lead times with uncertainty bands
  - Identify supplier bottlenecks
  - Recommend alternative suppliers

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Supplier Heatmap** → Color-coded supplier performance matrix
- **Sub-tab 2: Backlog Waterfall** → Pending orders breakdown by supplier/family
- **Sub-tab 3: ETA Forecast** → Lead time predictions with confidence intervals

#### A.1.6 SLA Feature Tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/features/sla/risk`
  - Calculate SLA breach risk scores (0-100%)
  - Map stockout risk to SLA penalties
  - Generate mitigation recommendations
- [ ] **Data Pipeline**: SLA feature extraction
  - Historical SLA compliance rates
  - Penalty cost calculations
  - Stockout-to-SLA breach mapping
- [ ] **ML Model Integration**: SLA risk prediction
  - Forecast SLA breach probability
  - Recommend safety stock adjustments
  - Alert on high-risk scenarios

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: SLA Breach Risk Meter** → Gauge chart showing current risk level
- **Sub-tab 2: Mitigation Checklist** → Actionable steps to prevent breaches
- **Sub-tab 3: Penalty Cost Analysis** → Financial impact of SLA breaches

#### A.1.7 Hierarchical Feature Tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/features/hierarchical/rollup`
  - Aggregate demand by family → site → region
  - Calculate variance between levels
  - Generate parent-child demand forecasts
- [ ] **Data Pipeline**: Hierarchical feature extraction
  - Multi-level aggregations (SKU → Family → Category)
  - Variance decomposition (within vs. between levels)
  - Top-down vs. bottom-up forecast reconciliation
- [ ] **ML Model Integration**: Hierarchical forecasting
  - Ensemble forecasts at multiple levels
  - Variance analysis and reconciliation
  - Cross-level consistency checks

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Parent-Child Rollup Chart** → Tree diagram showing demand aggregation
- **Sub-tab 2: Variance Table** → Breakdown of forecast variance by level
- **Sub-tab 3: Reconciliation View** → Top-down vs. bottom-up forecast comparison

#### A.1.8 Categorical Feature Tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/features/categorical/importance`
  - Calculate feature importance scores (SHAP values)
  - Generate categorical split analysis
  - Provide explainability metrics
- [ ] **Data Pipeline**: Categorical feature extraction
  - One-hot encoding for categorical variables
  - Target encoding for high-cardinality categories
  - Feature interaction analysis
- [ ] **ML Model Integration**: Feature importance analysis
  - SHAP value calculations
  - Permutation importance scores
  - Feature interaction effects

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Feature Importance Bar Chart** → Top 20 features ranked by importance
- **Sub-tab 2: Categorical Split Table** → Demand breakdown by category values
- **Sub-tab 3: Explainability Dashboard** → SHAP waterfall charts for predictions

#### A.1.9 Business Feature Tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/features/business/financial`
  - Aggregate ROI, cashflow, inventory metrics
  - Calculate capital efficiency scores
  - Generate executive KPI summaries
- [ ] **Data Pipeline**: Business feature extraction
  - Cashflow projections (inventory costs, savings)
  - ROI calculations (payback period, year-1 ROI)
  - Capital efficiency metrics (inventory turnover)
- [ ] **ML Model Integration**: Financial forecasting
  - Cashflow-at-risk calculations
  - ROI scenario projections
  - Capital optimization recommendations

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Cashflow vs. Inventory View** → Dual-axis chart showing financial trade-offs
- **Sub-tab 2: Executive KPIs** → High-level financial metrics dashboard
- **Sub-tab 3: Capital Efficiency Analysis** → Inventory turnover, working capital metrics

### A.2 `/main` Route — Data Integration Tasks

#### A.2.1 Modelos Sub-tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/main/models/performance`
  - Aggregate ensemble performance metrics (MAPE, RMSE, MAE)
  - Provide model lineage (retraining history)
  - Expose confidence intervals per model
- [ ] **ML Model Integration**: Ensemble model outputs
  - Prophet, ARIMA, LSTM/TFT predictions
  - Model weight optimization
  - Ensemble forecast aggregation
- [ ] **Drift Monitoring**: Great Expectations integration
  - Data drift detection (PSI, KS tests)
  - Model performance degradation alerts
  - Automatic retraining triggers

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Ensemble Performance Dashboard** → Accuracy trends, confidence intervals
- **Sub-tab 2: Model Lineage Cards** → Retraining history with performance deltas
- **Sub-tab 3: Drift Monitoring Alerts** → Data/model drift detection dashboard

#### A.2.2 Clustering Sub-tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/main/clustering/segments`
  - Aggregate equipment failure clusters
  - Calculate tower performance segments
  - Generate cluster insights and recommendations
- [ ] **ML Model Integration**: Clustering algorithms
  - K-means clustering for equipment failures
  - DBSCAN for tower performance segmentation
  - Cluster stability analysis
- [ ] **Data Pipeline**: Cluster feature extraction
  - Equipment failure patterns (time, location, type)
  - Tower performance metrics (uptime, SLA compliance)
  - Root cause analysis features

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Equipment Failure Clusters** → Scatter plot with cluster assignments
- **Sub-tab 2: Tower Performance Segments** → Performance matrix with segment labels
- **Sub-tab 3: Cluster Insights** → Root cause analysis and recommendations

#### A.2.3 Prescritivo Sub-tab
**Next Steps:**
- [ ] **BFF Endpoint**: Create `/api/v1/main/prescriptive/recommendations`
  - Generate purchase order recommendations
  - Calculate SLA intervention strategies
  - Provide cashflow impact projections
- [ ] **ML Model Integration**: Prescriptive analytics
  - Reorder point optimization
  - Safety stock recommendations
  - Supplier selection optimization
- [ ] **Data Pipeline**: Prescriptive feature extraction
  - Stockout risk scores
  - Lead time uncertainty
  - Cost-benefit analysis features

**Deep Sub-tabs Analysis:**
- **Sub-tab 1: Purchase Order Recommendations** → Kanban board with recommended actions
- **Sub-tab 2: SLA Intervention Strategies** → Actionable steps to prevent breaches
- **Sub-tab 3: Cashflow Impact Projections** → Financial impact of prescriptive actions

### A.3 Cross-Cutting Data Integration Tasks

#### A.3.1 BFF (Backend-for-Frontend) Architecture
**Next Steps:**
- [ ] **API Gateway**: Create unified BFF layer
  - Aggregate multiple backend services
  - Provide optimized data contracts for frontend
  - Implement caching strategy (Redis)
- [ ] **Data Contracts**: Define TypeScript interfaces
  - Match frontend component prop types
  - Ensure type safety end-to-end
  - Version API contracts
- [ ] **Error Handling**: Robust error responses
  - Graceful degradation (fallback to mock data)
  - Error logging and monitoring (Sentry)
  - User-friendly error messages

#### A.3.2 Live Drift Monitoring
**Next Steps:**
- [ ] **Great Expectations Integration**: Data quality checks
  - Schema validation
  - Statistical distribution tests
  - Anomaly detection
- [ ] **TFT Ensemble Monitoring**: Model performance tracking
  - Prediction accuracy trends
  - Confidence interval coverage
  - Model degradation alerts
- [ ] **Alerting System**: Real-time notifications
  - Slack/email alerts for drift detection
  - Dashboard widgets for monitoring
  - Automated retraining triggers

#### A.3.3 Scenario Lab Expansion
**Next Steps:**
- [ ] **Cost-to-Serve Analysis**: Add cost modeling
  - Calculate total cost of ownership
  - Optimize inventory allocation
  - Minimize logistics costs
- [ ] **Predictive Maintenance Insights**: Equipment health
  - Failure prediction models
  - Maintenance scheduling optimization
  - Downtime cost analysis

---

## 🎨 Bifurcation B: Frontend Story-Telling & UX/UI Improvements

**Focus**: Widget implementation, interactive storytelling, UX polish, demo mode enhancements

### B.1 `/features` Route — Frontend Implementation Tasks

#### B.1.1 Temporal Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Seasonality heatmap component
  - Week × Hour matrix with color-coded intensity
  - Interactive tooltips showing demand values
  - Export to CSV/PNG functionality
- [ ] **Story-Telling Elements**: Narrative tooltips
  - Explain seasonality patterns (e.g., "Higher demand on Fridays due to weekend maintenance")
  - Link to business impact (SLA, inventory)
  - Reference strategic docs for credibility
- [ ] **UX/UI Polish**: Responsive design
  - Mobile-friendly heatmap (swipe gestures)
  - Loading states and skeleton screens
  - Smooth animations (React Spring)

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Seasonality Heatmap** → Interactive matrix with drill-down capability
- **Sub-tab 2: Weekday Trends** → Line chart with confidence bands + narrative annotations
- **Sub-tab 3: Forecast Decomposition** → Stacked area chart with trend/seasonality/residual breakdown

#### B.1.2 Climate Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Weather impact tiles
  - Card components for rainfall, humidity, wind
  - KPI deltas with color coding (green/yellow/red)
  - Last refresh timestamp
- [ ] **Story-Telling Elements**: Storm alert timeline
  - Chronological weather events with demand impact
  - Root cause explanations (e.g., "Heavy rainfall → +40% structural demand")
  - Link to inventory alerts
- [ ] **UX/UI Polish**: Visual hierarchy
  - Hero card for current weather conditions
  - Secondary cards for historical patterns
  - Alert badges for severe weather events

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Weather Impact Tiles** → Card grid with animated KPI counters
- **Sub-tab 2: Storm Alert Timeline** → Vertical timeline with event cards
- **Sub-tab 3: Climate-Demand Correlation** → Scatter plot with regression line + narrative

#### B.1.3 Economic Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: FX & inflation shock gauge
  - Semi-circle gauge chart (0-100% risk)
  - Real-time currency rate display
  - Historical volatility chart
- [ ] **Story-Telling Elements**: Procurement cost scenarios
  - What-if analysis sliders
  - Narrative cards explaining FX impact
  - Link to ROI calculations
- [ ] **UX/UI Polish**: Executive-friendly design
  - Large, readable numbers
  - Color-coded risk levels
  - Export to PDF functionality

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: FX & Inflation Shock Gauge** → Gauge chart with risk meter + narrative
- **Sub-tab 2: Procurement Cost Scenarios** → Interactive sliders + scenario cards
- **Sub-tab 3: Economic-Demand Correlation** → Waterfall chart showing macro factor impacts

#### B.1.4 5G Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Coverage expansion map
  - Interactive Mapbox map with tower locations
  - 5G coverage polygons
  - Equipment demand hotspots
- [ ] **Story-Telling Elements**: Equipment demand uplift
  - Bar charts showing RF kit requirements
  - Narrative explaining 5G rollout impact
  - Link to inventory planning
- [ ] **UX/UI Polish**: Map interactions
  - Zoom/pan controls
  - Click-to-drill-down functionality
  - Legend and filters

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Coverage Expansion Map** → Interactive map with 5G rollout visualization
- **Sub-tab 2: Equipment Demand Uplift** → Bar charts with demand multipliers
- **Sub-tab 3: Project Timeline** → Gantt-style view with interactive milestones

#### B.1.5 Lead Time Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Supplier heatmap
  - Color-coded supplier performance matrix
  - Interactive cells showing lead time details
  - Filter by family/region
- [ ] **Story-Telling Elements**: Backlog waterfall
  - Stacked bar chart showing pending orders
  - Narrative explaining supplier bottlenecks
  - Link to reorder recommendations
- [ ] **UX/UI Polish**: Data table enhancements
  - Sortable columns
  - Pagination for large datasets
  - Export to Excel functionality

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Supplier Heatmap** → Interactive matrix with tooltips
- **Sub-tab 2: Backlog Waterfall** → Stacked bar chart with drill-down
- **Sub-tab 3: ETA Forecast** → Line chart with confidence intervals + narrative

#### B.1.6 SLA Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: SLA breach risk meter
  - Gauge chart (0-100% risk)
  - Color-coded risk levels (green/yellow/red)
  - Historical risk trend line
- [ ] **Story-Telling Elements**: Mitigation checklist
  - Actionable steps with checkboxes
  - Narrative explaining each mitigation action
  - Link to prescriptive recommendations
- [ ] **UX/UI Polish**: Alert-focused design
  - Prominent risk meter
  - Action buttons for immediate response
  - Success/failure feedback

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: SLA Breach Risk Meter** → Gauge chart with risk level + narrative
- **Sub-tab 2: Mitigation Checklist** → Interactive checklist with action buttons
- **Sub-tab 3: Penalty Cost Analysis** → Bar chart showing financial impact

#### B.1.7 Hierarchical Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Parent-child rollup chart
  - Tree diagram showing demand aggregation
  - Interactive nodes (click to expand/collapse)
  - Variance indicators per level
- [ ] **Story-Telling Elements**: Variance table
  - Breakdown of forecast variance by level
  - Narrative explaining aggregation patterns
  - Link to reconciliation view
- [ ] **UX/UI Polish**: Tree visualization
  - Smooth expand/collapse animations
  - Color-coded variance levels
  - Export to PNG/SVG functionality

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Parent-Child Rollup Chart** → Interactive tree diagram
- **Sub-tab 2: Variance Table** → Sortable table with variance breakdown
- **Sub-tab 3: Reconciliation View** → Side-by-side comparison of top-down vs. bottom-up

#### B.1.8 Categorical Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Feature importance bar chart
  - Horizontal bar chart (top 20 features)
  - Color-coded by feature type (temporal, climate, economic, etc.)
  - Interactive tooltips with SHAP values
- [ ] **Story-Telling Elements**: Categorical split table
  - Demand breakdown by category values
  - Narrative explaining feature importance
  - Link to model explainability
- [ ] **UX/UI Polish**: Explainability-focused design
  - Clear visual hierarchy
  - Interactive charts with drill-down
  - Export to PDF for reports

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Feature Importance Bar Chart** → Horizontal bar chart with SHAP values
- **Sub-tab 2: Categorical Split Table** → Sortable table with category breakdown
- **Sub-tab 3: Explainability Dashboard** → SHAP waterfall charts for predictions

#### B.1.9 Business Feature Tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Cashflow vs. inventory view
  - Dual-axis chart (cashflow + inventory levels)
  - Interactive tooltips showing trade-offs
  - Scenario toggles (optimistic/base/pessimistic)
- [ ] **Story-Telling Elements**: Executive KPIs
  - High-level financial metrics dashboard
  - Narrative explaining ROI and payback
  - Link to executive console
- [ ] **UX/UI Polish**: Executive-friendly design
  - Large, readable numbers
  - Color-coded metrics (green/yellow/red)
  - Export to PDF for presentations

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Cashflow vs. Inventory View** → Dual-axis chart with scenario toggles
- **Sub-tab 2: Executive KPIs** → Card grid with financial metrics
- **Sub-tab 3: Capital Efficiency Analysis** → Bar charts with efficiency metrics

### B.2 `/main` Route — Frontend Implementation Tasks

#### B.2.1 Modelos Sub-tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Ensemble performance dashboard
  - Line chart showing accuracy trends (MAPE, RMSE, MAE)
  - Confidence intervals shaded areas
  - Model weight matrix table
- [ ] **Story-Telling Elements**: Model lineage cards
  - Chronological retraining history
  - Performance deltas per retraining
  - Narrative explaining model improvements
- [ ] **UX/UI Polish**: Technical dashboard design
  - Tabbed interface (Accuracy / Weights / Lineage)
  - Interactive charts with zoom/pan
  - Export to CSV/PNG functionality

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Ensemble Performance Dashboard** → Line charts with confidence intervals
- **Sub-tab 2: Model Lineage Cards** → Timeline view with retraining events
- **Sub-tab 3: Drift Monitoring Alerts** → Alert feed with drift detection results

#### B.2.2 Clustering Sub-tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Equipment failure clusters
  - Scatter plot with cluster assignments
  - Color-coded clusters
  - Interactive tooltips with cluster details
- [ ] **Story-Telling Elements**: Tower performance segments
  - Performance matrix with segment labels
  - Narrative explaining cluster patterns
  - Link to root cause analysis
- [ ] **UX/UI Polish**: Cluster visualization
  - Interactive scatter plot (zoom/pan/filter)
  - Cluster legend with size indicators
  - Export to PNG/SVG functionality

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Equipment Failure Clusters** → Scatter plot with cluster assignments
- **Sub-tab 2: Tower Performance Segments** → Performance matrix with segment labels
- **Sub-tab 3: Cluster Insights** → Root cause analysis cards with recommendations

#### B.2.3 Prescritivo Sub-tab — Frontend
**Next Steps:**
- [ ] **Widget Implementation**: Purchase order recommendations
  - Kanban board (To Do / In Progress / Done)
  - Action cards with priority indicators
  - Drag-and-drop functionality
- [ ] **Story-Telling Elements**: SLA intervention strategies
  - Actionable steps with checkboxes
  - Narrative explaining each intervention
  - Link to SLA risk meter
- [ ] **UX/UI Polish**: Action-focused design
  - Prominent action buttons
  - Success/failure feedback
  - Export to PDF for procurement

**Deep Sub-tabs UX/UI:**
- **Sub-tab 1: Purchase Order Recommendations** → Kanban board with action cards
- **Sub-tab 2: SLA Intervention Strategies** → Interactive checklist with action buttons
- **Sub-tab 3: Cashflow Impact Projections** → Bar charts showing financial impact

### B.3 Cross-Cutting Frontend Tasks

#### B.3.1 Demo Mode Enhancements
**Next Steps:**
- [ ] **React Joyride Integration**: Guided tour overlay
  - Step-by-step walkthrough of key features
  - Highlight important widgets
  - Narrative script for each step
- [ ] **Auto-play Toggles**: Scenario slider automation
  - Auto-advance scenario sliders every 15s
  - Smooth animations between states
  - Pause/play controls
- [ ] **Alert Animations**: Visual feedback
  - Icon glow effects for critical alerts
  - Subtle audio pings (optional)
  - Toast notifications for new alerts

#### B.3.2 Story-Telling Infrastructure
**Next Steps:**
- [ ] **Narrative Tooltips**: Contextual explanations
  - Hover tooltips with strategic stats
  - Reference to strategic docs
  - Link to related features
- [ ] **Scripted Story Beats**: 4-minute pitch flow
  - Predefined navigation path
  - Highlight key talking points
  - Auto-advance through story beats
- [ ] **Executive Summary Export**: PDF generation
  - One-page summary with KPIs
  - Charts and visualizations
  - Narrative explanations

#### B.3.3 UX/UI Polish
**Next Steps:**
- [ ] **Branding Consistency**: Nova Corrente design system
  - Color tokens (primary, secondary, accent)
  - Typography scale (headings, body, captions)
  - Icon library (consistent style)
- [ ] **Responsive Design**: Mobile-friendly layouts
  - Breakpoints (mobile, tablet, desktop)
  - Touch-friendly interactions
  - Optimized chart rendering
- [ ] **Accessibility**: WCAG 2.1 AA compliance
  - ARIA labels on interactive elements
  - Keyboard navigation support
  - Screen reader compatibility
  - Color contrast ratios

#### B.3.4 Performance Optimization
**Next Steps:**
- [ ] **Lazy Loading**: Code splitting
  - Route-based code splitting
  - Component lazy loading
  - Chart library lazy loading
- [ ] **Data Virtualization**: Large dataset handling
  - Virtual scrolling for tables
  - Pagination for charts
  - Debounced search/filter
- [ ] **Caching Strategy**: Client-side caching
  - React Query for API caching
  - LocalStorage for user preferences
  - Service worker for offline support

---

## 📋 Implementation Priority Matrix

### Phase 1: Critical Path (Week 1-2)
**Bifurcation A:**
- BFF endpoint scaffolding (`/api/v1/features/*`, `/api/v1/main/*`)
- Mock data contracts (TypeScript interfaces)
- Basic data pipeline integration

**Bifurcation B:**
- Hero Overview tab (KPI strip, forecast chart, radar)
- Scenario Lab tab (sliders, narrative cards)
- Demo mode overlay (React Joyride)

### Phase 2: Feature Expansion (Week 3-4)
**Bifurcation A:**
- External data integration (INMET, BACEN, ANATEL)
- ML model integration (Prophet, ARIMA, LSTM)
- Drift monitoring setup (Great Expectations)

**Bifurcation B:**
- `/features` route tabs (Temporal, Climate, Economic, 5G)
- `/main` route sub-tabs (Modelos, Clustering, Prescritivo)
- Story-telling tooltips and narratives

### Phase 3: Polish & Optimization (Week 5-6)
**Bifurcation A:**
- Scenario lab expansion (cost-to-serve, predictive maintenance)
- Performance optimization (caching, query optimization)
- Production hardening (error handling, monitoring)

**Bifurcation B:**
- UX/UI polish (branding, responsive design, accessibility)
- Performance optimization (lazy loading, data virtualization)
- Executive summary export (PDF generation)

---

## 🎯 Success Metrics

### Bifurcation A (Data Integration)
- **API Response Time**: < 200ms (p95)
- **Data Freshness**: < 1 hour (cached data)
- **Drift Detection**: < 5 min (alert latency)
- **Model Accuracy**: MAPE < 15% (all families)

### Bifurcation B (Frontend)
- **Page Load Time**: < 2s (initial render)
- **Time-on-Tab**: ≥ 30s (6+ feature families)
- **Demo Completion Rate**: ≥ 80% (4-minute pitch)
- **Accessibility Score**: WCAG 2.1 AA compliant

---

## 📚 Reference Documents

- `demo_dashboard_quick_strategy.md` - Original demo playbook
- `features_route_planning.md` - `/features` route specifications
- `main_route_planning.md` - `/main` route specifications
- `frontend_feature_engineering_masterplan.md` - Overall frontend strategy
- `specs_main_analytics_overview.md` - `/main` analytics specifications

---

*Generated: 2025-11-12*  
*Status: Ready for Implementation*

