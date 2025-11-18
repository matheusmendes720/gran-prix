# Feature Engineering Workspace — Complete Structure Index

## 📊 Overview

Complete folder structure organized by bifurcation logic with granular sub-tabs organization.

**✅ Files Reorganized**: All specification and planning files have been moved to their respective sub-folders. Only main overall files remain in the root directory.

## 🗂️ Complete Folder Structure

```
feature-engineering/
│
├── README.md                                    # Main workspace index
├── REORGANIZATION_SUMMARY.md                   # Reorganization details
├── STRUCTURE_INDEX.md                          # This file
├── demo_dashboard_quick_strategy.md            # Original 60-minute demo playbook
├── demo_dashboard_next_steps_bifurcation.md    # Complete bifurcated roadmap
├── go_horse_roadshow_index.md                  # Roadshow execution index
│
├── bifurcation-a-data-integration/             # Backend/ML Focus
│   ├── README.md
│   ├── features/                               # `/features` route data tasks
│   │   ├── README.md
│   │   ├── temporal/                           # Temporal feature data integration
│   │   ├── climate/                            # Climate feature data integration
│   │   ├── economic/                           # Economic feature data integration
│   │   ├── 5g/                                # 5G feature data integration
│   │   ├── lead-time/                         # Lead time feature data integration
│   │   ├── sla/                               # SLA feature data integration
│   │   ├── hierarchical/                      # Hierarchical feature data integration
│   │   ├── categorical/                       # Categorical feature data integration
│   │   └── business/                          # Business feature data integration
│   ├── main/                                   # `/main` route data tasks
│   │   ├── README.md
│   │   ├── modelos/                           # Modelos sub-tab data integration
│   │   ├── clustering/                        # Clustering sub-tab data integration
│   │   └── prescritivo/                       # Prescritivo sub-tab data integration
│   └── cross-cutting/                          # Cross-cutting data integration
│       └── README.md
│
└── bifurcation-b-frontend-ux/                  # Frontend/UX Focus
    ├── README.md
    ├── features/                               # `/features` route frontend tasks
    │   ├── README.md
    │   ├── features_route_planning.md          # Overall features route planning
    │   ├── temporal/                           # Temporal feature frontend
    │   │   ├── specs_features_temporal.md
    │   │   └── features_temporal_breakdown.md
    │   ├── climate/                            # Climate feature frontend
    │   │   └── specs_features_climate.md
    │   ├── economic/                           # Economic feature frontend
    │   │   └── specs_features_economic.md
    │   ├── 5g/                                # 5G feature frontend
    │   │   └── specs_features_5g.md
    │   ├── lead-time/                         # Lead time feature frontend
    │   │   └── specs_features_lead_time.md
    │   ├── sla/                               # SLA feature frontend
    │   │   └── specs_features_sla.md
    │   ├── hierarchical/                      # Hierarchical feature frontend
    │   │   └── specs_features_hierarchical.md
    │   ├── categorical/                       # Categorical feature frontend
    │   │   └── specs_features_categorical.md
    │   └── business/                          # Business feature frontend
    │       └── specs_features_business.md
    ├── main/                                   # `/main` route frontend tasks
    │   ├── README.md
    │   ├── main_route_planning.md              # Overall main route planning
    │   ├── modelos/                           # Modelos sub-tab frontend
    │   │   ├── specs_main_analytics_overview.md
    │   │   ├── specs_main_formulas.md
    │   │   └── specs_main_visuals_blitz.md
    │   ├── clustering/                        # Clustering sub-tab frontend
    │   │   └── main_models_clustering_breakdown.md
    │   └── prescritivo/                       # Prescritivo sub-tab frontend
    └── cross-cutting/                          # Cross-cutting frontend tasks
        ├── frontend_feature_engineering_masterplan.md
        └── demo_execution_scaffold.md
```

## 🎯 Bifurcation Logic

### Bifurcation A: Feature Engineering & Data Integration
**Location**: `bifurcation-a-data-integration/`

**Focus Areas**:
- BFF endpoint development
- External API integration (INMET, BACEN, ANATEL)
- Data pipeline enhancements
- ML model integration
- Feature extraction and engineering
- Drift monitoring

**Structure**:
- `features/` - 9 feature tabs (temporal, climate, economic, 5g, lead-time, sla, hierarchical, categorical, business)
- `main/` - 3 sub-tabs (modelos, clustering, prescritivo)
- `cross-cutting/` - BFF architecture, drift monitoring, scenario lab expansion

### Bifurcation B: Frontend Story-Telling & UX/UI Improvements
**Location**: `bifurcation-b-frontend-ux/`

**Focus Areas**:
- Widget implementation
- Interactive storytelling
- UX polish
- Demo mode enhancements
- Responsive design
- Accessibility

**Structure**:
- `features/` - 9 feature tabs with specs and breakdowns
- `main/` - 3 sub-tabs with specs and breakdowns
- `cross-cutting/` - Masterplan, execution scaffold

## 📋 Feature Tabs (9 Total)

### `/features` Route
1. **Temporal** - Seasonality, weekday trends, forecast decomposition
2. **Climate** - Weather impacts, storm alerts, climate-demand correlation
3. **Economic** - FX volatility, inflation, procurement costs
4. **5G** - Coverage expansion, equipment demand uplift
5. **Lead Time** - Supplier heatmap, backlog, ETA forecasts
6. **SLA** - Breach risk meter, mitigation checklist
7. **Hierarchical** - Parent-child rollups, variance analysis
8. **Categorical** - Feature importance, categorical splits
9. **Business** - Cashflow, inventory, executive KPIs

### `/main` Route (3 Sub-tabs)
1. **Modelos** - Ensemble performance, accuracy trends, model lineage
2. **Clustering** - Equipment failure clusters, tower performance segments
3. **Prescritivo** - Purchase orders, SLA interventions, cashflow impacts

## 🔍 Navigation Guide

### For Backend/ML Developers
1. Start with: [bifurcation-a-data-integration/README.md](bifurcation-a-data-integration/README.md)
2. Choose route: [features/](bifurcation-a-data-integration/features/README.md) or [main/](bifurcation-a-data-integration/main/README.md)
3. Select feature/sub-tab folder (see links above)
4. Review: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) for detailed tasks

### For Frontend/UX Developers
1. Start with: [bifurcation-b-frontend-ux/README.md](bifurcation-b-frontend-ux/README.md)
2. Choose route: [features/](bifurcation-b-frontend-ux/features/README.md) or [main/](bifurcation-b-frontend-ux/main/README.md)
3. Select feature/sub-tab folder (see links above)
4. Review specs in that folder (see links above)
5. Review: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) for detailed tasks

### For Project Managers
1. Review: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) for complete roadmap
2. Check: [REORGANIZATION_SUMMARY.md](REORGANIZATION_SUMMARY.md) for structure changes
3. Monitor: Implementation phases in bifurcation READMEs (see links above)

## 📚 Key Documents

- **[demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md)** - Complete bifurcated roadmap with deep sub-tabs analysis
- **[demo_dashboard_quick_strategy.md](demo_dashboard_quick_strategy.md)** - Original 60-minute demo playbook
- **[frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md)** - Overall frontend strategy
- **[features_route_planning.md](bifurcation-b-frontend-ux/features/features_route_planning.md)** - Features route planning
- **[main_route_planning.md](bifurcation-b-frontend-ux/main/main_route_planning.md)** - Main route planning

## 🚀 Implementation Phases

### Phase 1: Critical Path (Week 1-2)
- BFF endpoint scaffolding
- Hero Overview tab
- Scenario Lab tab
- Demo mode overlay

### Phase 2: Feature Expansion (Week 3-4)
- External data integration
- ML model integration
- `/features` route tabs
- `/main` route sub-tabs

### Phase 3: Polish & Optimization (Week 5-6)
- Scenario lab expansion
- UX/UI polish
- Performance optimization
- Production hardening

---

## 🗺️ Ultimate Navigation Index — All Related Documents

### 📍 Quick Navigation by Role

#### 🎯 For Project Managers & Stakeholders
- **Start Here**: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) - Complete roadmap overview
- **Strategy**: [demo_dashboard_quick_strategy.md](demo_dashboard_quick_strategy.md) - Original 60-minute demo playbook
- **Execution**: [go_horse_roadshow_index.md](go_horse_roadshow_index.md) - Roadshow execution index
- **Structure**: [REORGANIZATION_SUMMARY.md](REORGANIZATION_SUMMARY.md) - Reorganization details
- **Overall Plan**: [frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md)

#### 🔧 For Backend/ML Engineers
- **Main Entry**: [bifurcation-a-data-integration/README.md](bifurcation-a-data-integration/README.md)
- **Features Route**: [bifurcation-a-data-integration/features/README.md](bifurcation-a-data-integration/features/README.md)
- **Main Route**: [bifurcation-a-data-integration/main/README.md](bifurcation-a-data-integration/main/README.md)
- **Cross-Cutting**: [bifurcation-a-data-integration/cross-cutting/README.md](bifurcation-a-data-integration/cross-cutting/README.md)
- **Detailed Tasks**: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) (Section A)
- **Related Docs**:
  - [FRONTEND_UX_TECHNICAL_DIAGNOSIS.md](../../docs/development/FRONTEND_UX_TECHNICAL_DIAGNOSIS.md) - Technical diagnosis
  - [feature_catalog.md](../../docs/pipeline/feature_catalog.md) - Feature catalog
  - [STATIC_ANALYSIS_REQUIREMENTS_VS_FEATURE_ENGINEERING_PT_BR.md](../../docs/proj/strategy/STATIC_ANALYSIS_REQUIREMENTS_VS_FEATURE_ENGINEERING_PT_BR.md) - Requirements analysis

#### 🎨 For Frontend/UX Engineers
- **Main Entry**: [bifurcation-b-frontend-ux/README.md](bifurcation-b-frontend-ux/README.md)
- **Features Route**: [bifurcation-b-frontend-ux/features/README.md](bifurcation-b-frontend-ux/features/README.md)
- **Main Route**: [bifurcation-b-frontend-ux/main/README.md](bifurcation-b-frontend-ux/main/README.md)
- **Masterplan**: [frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md)
- **Execution**: [demo_execution_scaffold.md](bifurcation-b-frontend-ux/cross-cutting/demo_execution_scaffold.md)
- **Detailed Tasks**: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) (Section B)
- **Related Docs**:
  - [FRONTEND_UX_TECHNICAL_DIAGNOSIS.md](../../docs/development/FRONTEND_UX_TECHNICAL_DIAGNOSIS.md) - UX technical diagnosis
  - [frontend_feature_engineering/INDEX.md](../../docs/development/frontend_feature_engineering/INDEX.md) - Frontend feature engineering index
  - [storytelling_frontend_plan.md](../storytelling/storytelling_frontend_plan.md) - Storytelling frontend plan
  - [frontend.md](../../docs/proj/roadmaps/shared/frontend.md) - Frontend roadmap

---

### 📚 Complete Document Catalog

#### 🎯 Core Strategy & Planning Documents

**Feature Engineering Workspace (Root)**
- [README.md](README.md) - Main workspace index
- [STRUCTURE_INDEX.md](STRUCTURE_INDEX.md) - This file (complete structure & navigation)
- [REORGANIZATION_SUMMARY.md](REORGANIZATION_SUMMARY.md) - Reorganization details and file movements
- [demo_dashboard_quick_strategy.md](demo_dashboard_quick_strategy.md) - Original 60-minute demo playbook
- [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) - **MASTER ROADMAP** - Complete bifurcated roadmap with deep sub-tabs analysis
- [go_horse_roadshow_index.md](go_horse_roadshow_index.md) - Roadshow execution index

#### 🔀 Bifurcation A: Data Integration Documents

**Root Level**
- [bifurcation-a-data-integration/README.md](bifurcation-a-data-integration/README.md) - Overview of Backend/ML tasks

**Features Route**
- [bifurcation-a-data-integration/features/README.md](bifurcation-a-data-integration/features/README.md) - Features route data integration overview
- [bifurcation-a-data-integration/features/temporal/](bifurcation-a-data-integration/features/temporal/) - Temporal feature data integration tasks
- [bifurcation-a-data-integration/features/climate/](bifurcation-a-data-integration/features/climate/) - Climate feature data integration tasks
- [bifurcation-a-data-integration/features/economic/](bifurcation-a-data-integration/features/economic/) - Economic feature data integration tasks
- [bifurcation-a-data-integration/features/5g/](bifurcation-a-data-integration/features/5g/) - 5G feature data integration tasks
- [bifurcation-a-data-integration/features/lead-time/](bifurcation-a-data-integration/features/lead-time/) - Lead time feature data integration tasks
- [bifurcation-a-data-integration/features/sla/](bifurcation-a-data-integration/features/sla/) - SLA feature data integration tasks
- [bifurcation-a-data-integration/features/hierarchical/](bifurcation-a-data-integration/features/hierarchical/) - Hierarchical feature data integration tasks
- [bifurcation-a-data-integration/features/categorical/](bifurcation-a-data-integration/features/categorical/) - Categorical feature data integration tasks
- [bifurcation-a-data-integration/features/business/](bifurcation-a-data-integration/features/business/) - Business feature data integration tasks

**Main Route**
- [bifurcation-a-data-integration/main/README.md](bifurcation-a-data-integration/main/README.md) - Main route data integration overview
- [bifurcation-a-data-integration/main/modelos/](bifurcation-a-data-integration/main/modelos/) - Modelos sub-tab data integration tasks
- [bifurcation-a-data-integration/main/clustering/](bifurcation-a-data-integration/main/clustering/) - Clustering sub-tab data integration tasks
- [bifurcation-a-data-integration/main/prescritivo/](bifurcation-a-data-integration/main/prescritivo/) - Prescritivo sub-tab data integration tasks

**Cross-Cutting**
- [bifurcation-a-data-integration/cross-cutting/README.md](bifurcation-a-data-integration/cross-cutting/README.md) - BFF architecture, drift monitoring, scenario lab

#### 🎨 Bifurcation B: Frontend/UX Documents

**Root Level**
- [bifurcation-b-frontend-ux/README.md](bifurcation-b-frontend-ux/README.md) - Overview of Frontend/UX tasks

**Features Route**
- [bifurcation-b-frontend-ux/features/README.md](bifurcation-b-frontend-ux/features/README.md) - Features route frontend overview
- [bifurcation-b-frontend-ux/features/features_route_planning.md](bifurcation-b-frontend-ux/features/features_route_planning.md) - Overall features route planning
- [bifurcation-b-frontend-ux/features/temporal/](bifurcation-b-frontend-ux/features/temporal/) - Temporal feature frontend
  - [specs_features_temporal.md](bifurcation-b-frontend-ux/features/temporal/specs_features_temporal.md) - Temporal feature specifications
  - [features_temporal_breakdown.md](bifurcation-b-frontend-ux/features/temporal/features_temporal_breakdown.md) - Temporal feature breakdown
- [bifurcation-b-frontend-ux/features/climate/specs_features_climate.md](bifurcation-b-frontend-ux/features/climate/specs_features_climate.md) - Climate feature specifications
- [bifurcation-b-frontend-ux/features/economic/specs_features_economic.md](bifurcation-b-frontend-ux/features/economic/specs_features_economic.md) - Economic feature specifications
- [bifurcation-b-frontend-ux/features/5g/specs_features_5g.md](bifurcation-b-frontend-ux/features/5g/specs_features_5g.md) - 5G feature specifications
- [bifurcation-b-frontend-ux/features/lead-time/specs_features_lead_time.md](bifurcation-b-frontend-ux/features/lead-time/specs_features_lead_time.md) - Lead time feature specifications
- [bifurcation-b-frontend-ux/features/sla/specs_features_sla.md](bifurcation-b-frontend-ux/features/sla/specs_features_sla.md) - SLA feature specifications
- [bifurcation-b-frontend-ux/features/hierarchical/specs_features_hierarchical.md](bifurcation-b-frontend-ux/features/hierarchical/specs_features_hierarchical.md) - Hierarchical feature specifications
- [bifurcation-b-frontend-ux/features/categorical/specs_features_categorical.md](bifurcation-b-frontend-ux/features/categorical/specs_features_categorical.md) - Categorical feature specifications
- [bifurcation-b-frontend-ux/features/business/specs_features_business.md](bifurcation-b-frontend-ux/features/business/specs_features_business.md) - Business feature specifications

**Main Route**
- [bifurcation-b-frontend-ux/main/README.md](bifurcation-b-frontend-ux/main/README.md) - Main route frontend overview
- [bifurcation-b-frontend-ux/main/main_route_planning.md](bifurcation-b-frontend-ux/main/main_route_planning.md) - Overall main route planning
- [bifurcation-b-frontend-ux/main/modelos/](bifurcation-b-frontend-ux/main/modelos/) - Modelos sub-tab frontend
  - [specs_main_analytics_overview.md](bifurcation-b-frontend-ux/main/modelos/specs_main_analytics_overview.md) - Analytics overview specifications
  - [specs_main_formulas.md](bifurcation-b-frontend-ux/main/modelos/specs_main_formulas.md) - Formulas specifications
  - [specs_main_visuals_blitz.md](bifurcation-b-frontend-ux/main/modelos/specs_main_visuals_blitz.md) - Visuals blitz specifications
- [bifurcation-b-frontend-ux/main/clustering/main_models_clustering_breakdown.md](bifurcation-b-frontend-ux/main/clustering/main_models_clustering_breakdown.md) - Clustering breakdown
- [bifurcation-b-frontend-ux/main/prescritivo/](bifurcation-b-frontend-ux/main/prescritivo/) - Prescritivo sub-tab frontend (ready for specs)

**Cross-Cutting**
- [bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md) - **MASTER PLAN** - Overall frontend strategy
- [bifurcation-b-frontend-ux/cross-cutting/demo_execution_scaffold.md](bifurcation-b-frontend-ux/cross-cutting/demo_execution_scaffold.md) - Demo execution scaffold

---

### 🔗 Related Documents in Codebase

#### 📊 Dashboard & Implementation Docs
- [README_DASHBOARD.md](../../docs/documentation/general/README_DASHBOARD.md) - Dashboard complete implementation guide
- [DASHBOARD_COMPLETE.md](../../docs/documentation/general/DASHBOARD_COMPLETE.md) - Dashboard completion status
- [LAUNCH_DASHBOARD.md](../../docs/documentation/general/LAUNCH_DASHBOARD.md) - Dashboard launch instructions
- [QUICK_START.md](../../docs/documentation/general/QUICK_START.md) - Quick start guide
- [API_DASHBOARD_GUIDE.md](../../docs/guides/API_DASHBOARD_GUIDE.md) - API dashboard guide
- [WEB_DASHBOARD_GUIDE.md](../../docs/guides/WEB_DASHBOARD_GUIDE.md) - Web dashboard guide

#### 🔧 Development & Technical Docs
- [FRONTEND_UX_TECHNICAL_DIAGNOSIS.md](../../docs/development/FRONTEND_UX_TECHNICAL_DIAGNOSIS.md) - Frontend UX technical diagnosis
- [frontend_feature_engineering/INDEX.md](../../docs/development/frontend_feature_engineering/INDEX.md) - Frontend feature engineering index
- [legacy-dashboard-restoration.md](../../docs/development/frontend_feature_engineering/legacy-dashboard-restoration.md) - Legacy dashboard restoration
- [scenario-simulator-integration.md](../../docs/development/frontend_feature_engineering/scenario-simulator-integration.md) - Scenario simulator integration
- [bff-data-pipeline.md](../../docs/development/frontend_feature_engineering/bff-data-pipeline.md) - BFF data pipeline
- [climate-storytelling.md](../../docs/development/frontend_feature_engineering/climate-storytelling.md) - Climate storytelling
- [demo-snapshot-mode.md](../../docs/development/frontend_feature_engineering/demo-snapshot-mode.md) - Demo snapshot mode
- [geo-heatmap-insights.md](../../docs/development/frontend_feature_engineering/geo-heatmap-insights.md) - Geo heatmap insights
- [safe-restore-roadmap.md](../../docs/development/frontend_feature_engineering/safe-restore-roadmap.md) - Safe restore roadmap

#### 📈 Storytelling & UX Docs
- [storytelling_frontend_plan.md](../storytelling/storytelling_frontend_plan.md) - Storytelling frontend plan
- [STORYTELLING_SCENARIO_GUIDE.md](../../docs/development/STORYTELLING_SCENARIO_GUIDE.md) - Storytelling scenario guide

#### 🗺️ Roadmaps & Strategy
- [frontend.md](../../docs/proj/roadmaps/shared/frontend.md) - Frontend roadmap
- [STATIC_ANALYSIS_REQUIREMENTS_VS_FEATURE_ENGINEERING_PT_BR.md](../../docs/proj/strategy/STATIC_ANALYSIS_REQUIREMENTS_VS_FEATURE_ENGINEERING_PT_BR.md) - Requirements vs feature engineering analysis

#### 📦 Pipeline & Features
- [feature_catalog.md](../../docs/pipeline/feature_catalog.md) - Feature catalog
- [FRONTEND_DATA_CONTRACT.md](../../docs/publish/FRONTEND_DATA_CONTRACT.md) - Frontend data contract

#### 📝 Reports & Fixes
- [FEATURES_FIX_SUMMARY.md](../workspace/analysis-reports/FEATURES_FIX_SUMMARY.md) - Features fix summary
- [EXTERNAL_FEATURES_FIX.md](../workspace/analysis-reports/EXTERNAL_FEATURES_FIX.md) - External features fix
- [FEATURES_FIX_SUMMARY.md](../../docs/reports/fixes/FEATURES_FIX_SUMMARY.md) - Features fix summary (docs)
- [EXTERNAL_FEATURES_FIX.md](../../docs/reports/fixes/EXTERNAL_FEATURES_FIX.md) - External features fix (docs)

---

### 🎯 Document Relationships & Dependencies

#### Master Documents (Start Here)
1. **[demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md)** ← **PRIMARY ROADMAP**
   - References: All feature specs, route planning docs
   - Used by: Both bifurcations for implementation tasks
   - Contains: Deep sub-tabs analysis for all features

2. **[frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md)**
   - References: [demo_dashboard_quick_strategy.md](demo_dashboard_quick_strategy.md), strategic docs
   - Used by: Frontend/UX developers
   - Contains: Overall frontend strategy and widget engineering guide

3. **[demo_dashboard_quick_strategy.md](demo_dashboard_quick_strategy.md)**
   - References: Strategic business problem docs, ML modeling docs
   - Used by: Both bifurcations for demo requirements
   - Contains: Original 60-minute demo playbook

#### Feature-Specific Documents
Each feature has:
- **Frontend Spec**: `bifurcation-b-frontend-ux/features/{feature}/specs_features_{feature}.md` (see links above)
- **Data Integration Tasks**: `bifurcation-a-data-integration/features/{feature}/` (folder ready, see links above)
- **Cross-Reference**: Both reference [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) Section A.1.X and B.1.X

#### Route Planning Documents
- **Features Route**: [features_route_planning.md](bifurcation-b-frontend-ux/features/features_route_planning.md)
  - References: All 9 feature specs
  - Used by: Frontend developers implementing `/features` route
  
- **Main Route**: [main_route_planning.md](bifurcation-b-frontend-ux/main/main_route_planning.md)
  - References: Modelos, Clustering, Prescritivo specs
  - Used by: Frontend developers implementing `/main` route

#### Cross-Cutting Documents
- **Bifurcation A Cross-Cutting**: [bifurcation-a-data-integration/cross-cutting/README.md](bifurcation-a-data-integration/cross-cutting/README.md)
  - BFF architecture, drift monitoring, scenario lab expansion
  
- **Bifurcation B Cross-Cutting**: 
  - [frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md)
  - [demo_execution_scaffold.md](bifurcation-b-frontend-ux/cross-cutting/demo_execution_scaffold.md)

---

### 🔍 Search & Discovery Guide

#### By Task Type

**Implementing a Feature Tab?**
1. Read: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) (Section A.1.X for data, B.1.X for frontend)
2. Check: `bifurcation-b-frontend-ux/features/{feature}/specs_features_{feature}.md` (see feature links above)
3. Review: [features_route_planning.md](bifurcation-b-frontend-ux/features/features_route_planning.md)
4. Implement: Data integration in `bifurcation-a-data-integration/features/{feature}/` (see feature links above)

**Implementing Main Route Sub-tab?**
1. Read: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) (Section A.2.X for data, B.2.X for frontend)
2. Check: `bifurcation-b-frontend-ux/main/{subtab}/specs_main_*.md` (see main route links above)
3. Review: [main_route_planning.md](bifurcation-b-frontend-ux/main/main_route_planning.md)
4. Implement: Data integration in `bifurcation-a-data-integration/main/{subtab}/` (see main route links above)

**Setting Up BFF Architecture?**
1. Read: [bifurcation-a-data-integration/cross-cutting/README.md](bifurcation-a-data-integration/cross-cutting/README.md)
2. Review: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) (Section A.3.1)
3. Check: [bff-data-pipeline.md](../../docs/development/frontend_feature_engineering/bff-data-pipeline.md)

**Implementing Demo Mode?**
1. Read: [demo_dashboard_quick_strategy.md](demo_dashboard_quick_strategy.md)
2. Review: [demo_execution_scaffold.md](bifurcation-b-frontend-ux/cross-cutting/demo_execution_scaffold.md)
3. Check: [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) (Section B.3.1)

**Understanding Storytelling Requirements?**
1. Read: [frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md)
2. Review: [storytelling_frontend_plan.md](../storytelling/storytelling_frontend_plan.md)
3. Check: [STORYTELLING_SCENARIO_GUIDE.md](../../docs/development/STORYTELLING_SCENARIO_GUIDE.md)

#### By Feature Type

**Temporal Features?**
- Frontend: [bifurcation-b-frontend-ux/features/temporal/](bifurcation-b-frontend-ux/features/temporal/)
- Data: [bifurcation-a-data-integration/features/temporal/](bifurcation-a-data-integration/features/temporal/)
- Breakdown: [features_temporal_breakdown.md](bifurcation-b-frontend-ux/features/temporal/features_temporal_breakdown.md)

**Climate Features?**
- Frontend: [specs_features_climate.md](bifurcation-b-frontend-ux/features/climate/specs_features_climate.md)
- Data: [bifurcation-a-data-integration/features/climate/](bifurcation-a-data-integration/features/climate/)
- Related: [climate-storytelling.md](../../docs/development/frontend_feature_engineering/climate-storytelling.md)

**Economic Features?**
- Frontend: [specs_features_economic.md](bifurcation-b-frontend-ux/features/economic/specs_features_economic.md)
- Data: [bifurcation-a-data-integration/features/economic/](bifurcation-a-data-integration/features/economic/)

**5G Features?**
- Frontend: [specs_features_5g.md](bifurcation-b-frontend-ux/features/5g/specs_features_5g.md)
- Data: [bifurcation-a-data-integration/features/5g/](bifurcation-a-data-integration/features/5g/)

**Lead Time Features?**
- Frontend: [specs_features_lead_time.md](bifurcation-b-frontend-ux/features/lead-time/specs_features_lead_time.md)
- Data: [bifurcation-a-data-integration/features/lead-time/](bifurcation-a-data-integration/features/lead-time/)

**SLA Features?**
- Frontend: [specs_features_sla.md](bifurcation-b-frontend-ux/features/sla/specs_features_sla.md)
- Data: [bifurcation-a-data-integration/features/sla/](bifurcation-a-data-integration/features/sla/)

**Hierarchical Features?**
- Frontend: [specs_features_hierarchical.md](bifurcation-b-frontend-ux/features/hierarchical/specs_features_hierarchical.md)
- Data: [bifurcation-a-data-integration/features/hierarchical/](bifurcation-a-data-integration/features/hierarchical/)

**Categorical Features?**
- Frontend: [specs_features_categorical.md](bifurcation-b-frontend-ux/features/categorical/specs_features_categorical.md)
- Data: [bifurcation-a-data-integration/features/categorical/](bifurcation-a-data-integration/features/categorical/)

**Business Features?**
- Frontend: [specs_features_business.md](bifurcation-b-frontend-ux/features/business/specs_features_business.md)
- Data: [bifurcation-a-data-integration/features/business/](bifurcation-a-data-integration/features/business/)

---

### 📋 Document Status & Completeness

#### ✅ Complete Documents
- [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) - Complete with all 9 features + 3 main sub-tabs
- [frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md) - Complete masterplan
- All 9 feature specs in `bifurcation-b-frontend-ux/features/{feature}/` (see links above)
- All 3 main route specs in `bifurcation-b-frontend-ux/main/modelos/` (see links above)
- All README files in bifurcation folders (see links above)

#### 🚧 In Progress / Ready for Content
- `bifurcation-a-data-integration/features/{feature}/` - Folders created, ready for task documentation (see links above)
- `bifurcation-a-data-integration/main/{subtab}/` - Folders created, ready for task documentation (see links above)
- [bifurcation-b-frontend-ux/main/prescritivo/](bifurcation-b-frontend-ux/main/prescritivo/) - Folder created, ready for specs

#### 📝 Reference Documents (External)
- All documents in `docs/development/`, `docs/documentation/`, `docs/proj/` are reference materials
- Use for context, but implementation tasks are in bifurcation folders

---

### 🎯 Quick Reference Matrix

| Need | Document | Location |
|------|----------|----------|
| **Complete roadmap** | [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) | Root |
| **Frontend strategy** | [frontend_feature_engineering_masterplan.md](bifurcation-b-frontend-ux/cross-cutting/frontend_feature_engineering_masterplan.md) | `bifurcation-b-frontend-ux/cross-cutting/` |
| **Feature spec** | `specs_features_{feature}.md` | `bifurcation-b-frontend-ux/features/{feature}/` (see links above) |
| **Main route spec** | `specs_main_{subtab}.md` | `bifurcation-b-frontend-ux/main/{subtab}/` (see links above) |
| **Data integration tasks** | Section A in bifurcation doc | [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) |
| **Frontend tasks** | Section B in bifurcation doc | [demo_dashboard_next_steps_bifurcation.md](demo_dashboard_next_steps_bifurcation.md) |
| **Route planning** | [features_route_planning.md](bifurcation-b-frontend-ux/features/features_route_planning.md) or [main_route_planning.md](bifurcation-b-frontend-ux/main/main_route_planning.md) | `bifurcation-b-frontend-ux/{route}/` |
| **Demo execution** | [demo_execution_scaffold.md](bifurcation-b-frontend-ux/cross-cutting/demo_execution_scaffold.md) | `bifurcation-b-frontend-ux/cross-cutting/` |
| **BFF architecture** | [Cross-cutting README](bifurcation-a-data-integration/cross-cutting/README.md) | `bifurcation-a-data-integration/cross-cutting/` |

---

## ✅ Reorganization Status

**All files have been moved to their respective sub-folders!**

- ✅ All 9 feature specs → `bifurcation-b-frontend-ux/features/{feature}/`
- ✅ All 3 main route specs → `bifurcation-b-frontend-ux/main/{subtab}/`
- ✅ All planning documents → Organized by route
- ✅ All cross-cutting docs → `bifurcation-b-frontend-ux/cross-cutting/`
- ✅ Only main overall files remain in root

**All navigation links in this document are clickable and point to the correct locations!**

---

*Last Updated: 2025-11-12*  
*Navigation Index Version: 1.1*  
*Files Reorganized: All specification files moved to sub-folders*

