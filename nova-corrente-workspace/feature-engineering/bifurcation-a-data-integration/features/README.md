# `/features` Route — Data Integration

## 📊 Overview

This folder contains data integration tasks for all 9 feature tabs in the `/features` route.

## 🗂️ Feature Tabs

Each feature tab has its own subfolder for data integration tasks:

1. **`temporal/`** - BFF endpoints, temporal feature extraction, Prophet/ARIMA integration
2. **`climate/`** - INMET API integration, climate impact features, storm alert pipeline
3. **`economic/`** - BACEN API integration, FX volatility features, economic scenario projections
4. **`5g/`** - ANATEL API integration, 5G coverage features, equipment demand projections
5. **`lead-time/`** - Lead time analysis endpoints, supplier risk scores, ETA forecasts
6. **`sla/`** - SLA risk calculation endpoints, penalty cost features, mitigation recommendations
7. **`hierarchical/`** - Hierarchical rollup endpoints, variance decomposition, forecast reconciliation
8. **`categorical/`** - Feature importance endpoints, SHAP value calculations, explainability metrics
9. **`business/`** - Financial metrics endpoints, ROI calculations, capital efficiency features

## 📋 Common Tasks

Each feature tab data integration includes:
- BFF endpoint development (`/api/v1/features/{feature}/...`)
- External API integration (INMET, BACEN, ANATEL)
- Feature engineering pipeline
- ML model integration
- Data contracts (TypeScript interfaces)

## 📚 Related Documents

- `../main/` - `/main` route data integration tasks
- `../cross-cutting/` - Cross-cutting data integration tasks
- `../../demo_dashboard_next_steps_bifurcation.md` - Complete bifurcation roadmap

---

*Last Updated: 2025-11-12*

