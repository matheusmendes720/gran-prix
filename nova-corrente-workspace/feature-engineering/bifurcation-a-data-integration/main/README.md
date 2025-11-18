# `/main` Route — Data Integration

## 📊 Overview

This folder contains data integration tasks for all 3 sub-tabs in the `/main` route.

## 🗂️ Sub-tabs

Each sub-tab has its own folder for data integration tasks:

1. **`modelos/`** - Ensemble performance endpoints, model lineage tracking, drift monitoring
2. **`clustering/`** - Cluster segmentation endpoints, equipment failure analysis, tower performance metrics
3. **`prescritivo/`** - Prescriptive recommendations endpoints, purchase order generation, cashflow impact calculations

## 📋 Common Tasks

Each sub-tab data integration includes:
- BFF endpoint development (`/api/v1/main/{subtab}/...`)
- ML model integration (ensemble, clustering, prescriptive)
- Data pipeline enhancements
- Performance metrics tracking
- Alert generation

## 📚 Related Documents

- `../features/` - `/features` route data integration tasks
- `../cross-cutting/` - Cross-cutting data integration tasks
- `../../demo_dashboard_next_steps_bifurcation.md` - Complete bifurcation roadmap

---

*Last Updated: 2025-11-12*

