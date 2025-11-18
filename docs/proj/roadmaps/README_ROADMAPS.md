# 📚 ROADMAPS & STRATEGIC DOCUMENTATION INDEX
## Nova Corrente Demand Forecasting - Complete Guide

**Last Updated:** November 2025  
**Version:** 4.0 (DEMO vs PROD Path Split)  
**Status:** ✅ **DOCUMENTATION REORGANIZED - DEMO & PROD PATHS SEPARATED**

---

## 🎯 CHOOSE YOUR PATH

The Nova Corrente project has evolved into two distinct paths. Choose the path that matches your needs:

### 🚀 DEMO Path - 4-Day Sprint, Roadshow-Ready
**Timeline:** 4 days (D0-D4)  
**Stack:** Parquet + MinIO + DuckDB + Pandas + Simple Scheduler  
**Use Case:** Roadshow demonstrations, MVP, rapid deployment, cost-sensitive  
**Complexity:** Low  
**Cost:** Minimal

👉 **[Go to DEMO Path Roadmaps →](demo/README_DEMO_ROADMAPS.md)**

---

### 🏭 PROD Path - Production-Ready, Enterprise-Scale
**Timeline:** 16 weeks (phased implementation)  
**Stack:** PostgreSQL + (future: AWS + Airflow + dbt + Delta Lake + Spark)  
**Use Case:** Production deployment, enterprise scale, long-term investment  
**Complexity:** High  
**Cost:** (Future: Cloud costs)

👉 **[Go to PROD Path Roadmaps →](prod/README_PROD_ROADMAPS.md)**

---

## 📊 PATH COMPARISON

| Aspect | DEMO Path | PROD Path |
|--------|-----------|-----------|
| **Timeline** | 4 days | 16 weeks |
| **Storage** | Parquet + MinIO | PostgreSQL + (future: S3 + Delta Lake) |
| **Compute** | DuckDB + Pandas | PostgreSQL + (future: Spark + Databricks) |
| **Orchestration** | Simple scheduler | (future: Airflow) |
| **Transformations** | Python scripts | (future: dbt models) |
| **Deployment** | Local Docker Compose | Production Docker + (future: AWS) |
| **Use Case** | Roadshow, MVP | Production, enterprise |
| **Complexity** | Low | High |
| **Cost** | Minimal | (Future: Cloud costs) |

**See:** [Complete Stack Comparison](../../STACK_COMPARISON_DEMO_VS_PROD.md) for detailed comparison

---

## 🔄 MIGRATION BETWEEN PATHS

- **[DEMO → PROD Migration Guide](../../MIGRATION_DEMO_TO_PROD.md)** - Step-by-step upgrade from DEMO to PROD
- **[PROD → DEMO Simplification Guide](../../MIGRATION_PROD_TO_DEMO.md)** - Step-by-step simplification from PROD to DEMO

---

## 📖 SHARED DOCUMENTATION

These documents apply to both DEMO and PROD paths:

### Strategic Overview
- **[EXECUTIVE_ENRICHMENT_SUMMARY.md](shared/EXECUTIVE_ENRICHMENT_SUMMARY.md)** - Executive-level justification for external data enrichment
- **[COMPREHENSIVE_DATA_MODELING_STRATEGY.md](shared/COMPREHENSIVE_DATA_MODELING_STRATEGY.md)** - Complete technical specification for data warehouse design
- **[COMPLETE_CHAT_HISTORY_ANALYSIS.md](shared/COMPLETE_CHAT_HISTORY_ANALYSIS.md)** - Full context from all chat sessions
- **[Annotation_Sugestion.md](shared/Annotation_Sugestion.md)** - MIT Telecom dataset fit assessment

### Quick Start Guides
- **[QUICK_START_GUIDE.md](shared/QUICK_START_GUIDE.md)** - Get started in 60 minutes
- **[QUICK_START_GUIDE_PT_BR.md](shared/QUICK_START_GUIDE_PT_BR.md)** - Guia rápido em português

### Implementation Support
- **[CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md](shared/CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md)** - Current data processing state
- **[NEXT_STEPS_OPTIMIZATION_PT_BR.md](shared/NEXT_STEPS_OPTIMIZATION_PT_BR.md)** - Optimization roadmap
- **[TROUBLESHOOTING_GUIDE_PT_BR.md](shared/TROUBLESHOOTING_GUIDE_PT_BR.md)** - Troubleshooting guide
- **[IMPLEMENTATION_TEMPLATES_PT_BR.md](shared/IMPLEMENTATION_TEMPLATES_PT_BR.md)** - Implementation templates

---

## 🔁 RELEASE NOTES & ARCHITECTURE OVERVIEW

### 🗺️ **Master Navigation**
- **[📚 Complete Navigation Index](../../NAVIGATION_INDEX.md)** - **START HERE** - Master index of all documentation, roadmaps, and changelogs

### Changelogs
- **[CHANGELOG.md](../../CHANGELOG.md)** - Main changelog (references both paths)
- **[CHANGELOG_DEMO.md](../../CHANGELOG_DEMO.md)** - Complete DEMO path history
- **[CHANGELOG_PROD.md](../../CHANGELOG_PROD.md)** - Complete PROD path history

### Architecture Analysis
- **[Architecture Bifurcation Analysis](../../ARCHITECTURE_BIFURCATION_ANALYSIS.md)** - Complete analysis of path divergence
- **[Stack Comparison](../../STACK_COMPARISON_DEMO_VS_PROD.md)** - Detailed technology stack comparison
- **[Bifurcation Timeline](../../ROADMAP_BIFURCATION_TIMELINE.md)** - Visual timeline of path divergence

---

## 🎯 START HERE

### New to This Project? Read These 3 Files (45 minutes)

1. **[QUICK_START_GUIDE.md](shared/QUICK_START_GUIDE.md)** (15 min) 🔥 **START HERE**
   - 60-second TLDR
   - 3 things to do today
   - Week-by-week roadmap
   - Troubleshooting guide

2. **[EXECUTIVE_ENRICHMENT_SUMMARY.md](shared/EXECUTIVE_ENRICHMENT_SUMMARY.md)** (20 min)
   - The opportunity: 96.3% missing data = 72 point MAPE gap
   - Best tables to add (3-tier priorities)
   - MAPE progression: 87% → <15%
   - Business impact metrics

3. **[Annotation_Sugestion.md](shared/Annotation_Sugestion.md)** (10 min)
   - MIT Telecom fit assessment
   - Core columns to use
   - Required enrichments
   - Recommended schema

---

## 📖 COMPLETE DOCUMENTATION SET

### 1. Strategic Overview (Read First)

#### [EXECUTIVE_ENRICHMENT_SUMMARY.md](shared/EXECUTIVE_ENRICHMENT_SUMMARY.md)
**Purpose:** Executive-level justification for external data enrichment  
**Audience:** Managers, stakeholders, decision-makers  
**Length:** 403 lines  
**Key Sections:**
- The Opportunity (96.3% missing data)
- What We Discovered (dadosSuprimentos.xlsx + 33 datasets)
- Recommended Data Model (star schema)
- Best Tables to Add (3-tier priorities)
- Implementation Roadmap (4 weeks)
- Expected Outcomes (MAPE 87% → <15%)

**Read if:** You need to justify budget/resources for external data integration

---

#### [QUICK_START_GUIDE.md](shared/QUICK_START_GUIDE.md)
**Purpose:** Get started in 60 minutes  
**Audience:** Developers, data engineers, anyone implementing  
**Length:** 432 lines  
**Key Sections:**
- TLDR (60-second summary)
- 3 Things to Do Today
- Week-by-Week Roadmap
- File Structure
- Key Concepts (Star Schema, ABC, MAPE)
- Troubleshooting
- Success Metrics

**Read if:** You're ready to start coding today

---

### 2. Technical Blueprint (Reference Material)

#### [COMPREHENSIVE_DATA_MODELING_STRATEGY.md](shared/COMPREHENSIVE_DATA_MODELING_STRATEGY.md)
**Purpose:** Complete technical specification for data warehouse design  
**Audience:** Data architects, database engineers, ML engineers  
**Length:** 1,378 lines (intentionally incomplete - continues in implementation scripts)  
**Key Sections:**
- Part 1: Current Data Assets Inventory
- Part 2: Recommended Star Schema Architecture (SQL schemas)
- Part 3: External API Integration Tables
- Part 4: Relational Mapping & Join Strategies
- Part 5: Data Quality & Enrichment Opportunities
- Part 6: Strategic Recommendations
- Part 7: Technical Implementation Guide (Python code examples)

**Read if:** You need SQL schema definitions, field-level documentation, or ML feature engineering queries

---

### 3. Context & History (Background)

#### [COMPLETE_CHAT_HISTORY_ANALYSIS.md](shared/COMPLETE_CHAT_HISTORY_ANALYSIS.md)
**Purpose:** Full context from all chat sessions  
**Audience:** Anyone joining mid-project, auditors, documentation readers  
**Length:** 569 lines  
**Key Sections:**
- Chat Chronology & Key Decisions
- Key Insights & Patterns
- Dataset Selection Evolution
- Schema Design Progression
- External API Strategy
- Best Tables to Add (consolidated)
- Lessons Learned & Best Practices

**Read if:** You need to understand why decisions were made, what was tried before, or historical context

---

#### [Annotation_Sugestion.md](shared/Annotation_Sugestion.md)
**Purpose:** MIT Telecom dataset fit assessment (from previous chat session)  
**Audience:** Data scientists evaluating dataset compatibility  
**Length:** 55 lines  
**Key Sections:**
- Summary (fit verdict)
- Where it's referenced
- Core columns to use
- Fit to our problem
- Required enrichments
- Granularity note
- Standardized join keys
- Recommended schema

**Read if:** You need to evaluate whether MIT Telecom dataset fits Nova Corrente use case

---

### 🔁 Release Notes & Architecture Overview

- **[CHANGELOG.md](../../CHANGELOG.md)** – Complete versioned changelog (1.0.0 → 2.0.0 → 3.0.0-postgres → 3.1.0-docs), including links to implementation plans, PostgreSQL migration, offline-ML pipeline, and deployment guides.

---

## 🗂️ DOCUMENT RELATIONSHIPS

### Information Flow

```
Chat History
    ↓
COMPLETE_CHAT_HISTORY_ANALYSIS.md (Context)
    ↓
EXECUTIVE_ENRICHMENT_SUMMARY.md (Strategy)
    ↓
QUICK_START_GUIDE.md (Action Plan)
    ↓
COMPREHENSIVE_DATA_MODELING_STRATEGY.md (Technical Specs)
    ↓
Implementation Scripts (Code)
```

### Reading Paths

**Path 1: "I want to start coding now"**
```
1. shared/QUICK_START_GUIDE.md (15 min)
2. Run 01_create_star_schema_dimensions.py (15 min)
3. shared/COMPREHENSIVE_DATA_MODELING_STRATEGY.md - Part 7 (30 min)
```

**Path 2: "I need to justify this to management"**
```
1. shared/EXECUTIVE_ENRICHMENT_SUMMARY.md (20 min)
2. shared/QUICK_START_GUIDE.md - Success Metrics section (5 min)
3. Present findings
```

**Path 3: "I'm a new team member joining mid-project"**
```
1. shared/COMPLETE_CHAT_HISTORY_ANALYSIS.md (25 min)
2. shared/EXECUTIVE_ENRICHMENT_SUMMARY.md (20 min)
3. shared/QUICK_START_GUIDE.md (15 min)
4. shared/COMPREHENSIVE_DATA_MODELING_STRATEGY.md (60 min)
```

**Path 4: "I need SQL schema definitions"**
```
1. shared/COMPREHENSIVE_DATA_MODELING_STRATEGY.md - Part 2 (30 min)
2. shared/COMPREHENSIVE_DATA_MODELING_STRATEGY.md - Part 4.2 (15 min)
```

**Path 5: "I want to understand dataset selection rationale"**
```
1. shared/Annotation_Sugestion.md (10 min)
2. shared/COMPLETE_CHAT_HISTORY_ANALYSIS.md - Dataset Selection section (10 min)
3. shared/COMPREHENSIVE_DATA_MODELING_STRATEGY.md - Part 1 (15 min)
```

---

## 📊 QUICK REFERENCE

### The Problem
- **Current MAPE:** 87.27% (EPI family - best performer)
- **Target MAPE:** <15% (industry standard)
- **Gap:** 72 percentage points
- **Root Cause:** 96.3% missing external data (climate, economic, regulatory)

### The Solution
- **Add 3 Critical Tables:** Climate (Milan Telecom), Economic (Demand Factors), Regulatory (Operators)
- **Expected Impact:** -35 to -60% MAPE reduction
- **Timeline:** 4 weeks to <15% MAPE
- **Implementation:** Star schema with 12 tables (6 core + 6 external)

### The Data
- **Nova Corrente ERP:** 4,207 records (dadosSuprimentos.xlsx)
- **External Datasets:** 33 available (16 analyzed, 75% ready)
- **Enrichment Sources:** Zenodo (116K), Brazilian (2,190), Operators (290)
- **Current Coverage:** 3.7% (96.3% gap to fill)

### The Roadmap
- **Week 1:** Foundation + Climate → MAPE 87% → 50%
- **Week 2:** Economic + Regulatory → MAPE 50% → 30%
- **Week 3:** Faults + Retraining → MAPE 30% → 15%
- **Week 4:** Optimization → MAPE <15% ✅

---

## 🎓 KEY CONCEPTS GLOSSARY

**Star Schema:** Database design with fact table (center) + dimension tables (points). Optimized for analytics.

**MAPE (Mean Absolute Percentage Error):** Forecast accuracy metric. Lower = better. <15% = good.

**ABC Classification:** Pareto (80-20) rule for inventory. A=high-value (20% of parts = 80% of cost), B=medium, C=low.

**External Enrichment:** Adding data from outside sources (weather, economic, regulatory) to improve predictions.

**Fact Table:** Transactional data (who bought what, when, where). Grain = one row per event.

**Dimension Table:** Descriptive data (product details, customer info, calendar). Slow-changing.

**Cyclical Features:** Sin/cos encoding of circular values (month, day) so ML models understand seasonality.

**Lead Time:** Days between order placement and delivery. Critical for reorder point calculation.

**Coefficient of Variation (CV):** Std dev / mean. Measures demand variability. High CV = erratic demand.

**Transfer Learning:** Using pre-trained model (MIT Telecom) as starting point for Nova Corrente.

---

## 🚀 IMPLEMENTATION CHECKLIST

### Phase 0: Preparation (Today)
- [ ] Read QUICK_START_GUIDE.md
- [ ] Read EXECUTIVE_ENRICHMENT_SUMMARY.md
- [ ] Verify dadosSuprimentos.xlsx accessible
- [ ] Verify external datasets exist (Milan, Demand Factors, Operators)
- [ ] Review COMPREHENSIVE_DATA_MODELING_STRATEGY.md - Part 2 (star schema)

### Phase 1: Foundation (Week 1)
- [ ] Run 01_create_star_schema_dimensions.py
- [ ] Create Fact_Demand_Daily
- [ ] Integrate Climate data (Fact_Climate_Daily)
- [ ] Validate MAPE improvement: 87% → 62-72%

### Phase 2: Enrichment (Week 2)
- [ ] Integrate Economic data (Fact_Economic_Daily)
- [ ] Integrate Regulatory data (Fact_Regulatory_Daily)
- [ ] Setup BACEN API
- [ ] Validate MAPE improvement: 62-72% → 27-42%

### Phase 3: Advanced Features (Week 3)
- [ ] Integrate Fault events (Fact_Fault_Events)
- [ ] Retrain models with 100% external coverage
- [ ] Validate MAPE improvement: 27-42% → 17-27%

### Phase 4: Optimization (Week 4)
- [ ] ABC-based model selection
- [ ] Hyperparameter tuning
- [ ] Test set validation
- [ ] **Achieve MAPE <15%** ✅

---

## 📞 GETTING HELP

### Where to Look

**"How do I start?"**
→ QUICK_START_GUIDE.md

**"Why are we doing this?"**
→ EXECUTIVE_ENRICHMENT_SUMMARY.md

**"What tables should I create?"**
→ COMPREHENSIVE_DATA_MODELING_STRATEGY.md - Part 2

**"What went wrong before?"**
→ COMPLETE_CHAT_HISTORY_ANALYSIS.md - Lessons Learned

**"Does MIT Telecom fit?"**
→ Annotation_Sugestion.md

**"What's the SQL for [X]?"**
→ COMPREHENSIVE_DATA_MODELING_STRATEGY.md - Search for table name

**"What features should I engineer?"**
→ COMPREHENSIVE_DATA_MODELING_STRATEGY.md - Part 4.2

**"What's the business impact?"**
→ EXECUTIVE_ENRICHMENT_SUMMARY.md - Business Impact section

---

## 🎯 SUCCESS METRICS

### Technical Metrics
- **MAPE:** <15% on test set (vs. current 87.27%)
- **Coverage:** 100% external data (vs. current 3.7%)
- **Features:** 90+ (vs. current 73)
- **Training time:** <10 min per family

### Business Metrics
- **Forecast accuracy:** >85% (vs. current 12.73%)
- **Stockout rate:** <5% (vs. current 15-20%)
- **Excess inventory:** -20-30% cost reduction
- **SLA compliance:** >95% (vs. current 60-70%)

---

## 📂 FILE LOCATIONS

### Documentation Structure
```
docs/proj/roadmaps/
├── README_ROADMAPS.md ← This file (path selector)
├── demo/
│   ├── README_DEMO_ROADMAPS.md ← DEMO path index
│   ├── TECHNICAL_STACK_DEMO.md
│   └── ... (DEMO-specific roadmaps)
├── prod/
│   ├── README_PROD_ROADMAPS.md ← PROD path index
│   ├── TECHNICAL_STACK_PROD.md
│   └── ... (PROD-specific roadmaps)
└── shared/
    ├── QUICK_START_GUIDE.md ← Start here
    ├── EXECUTIVE_ENRICHMENT_SUMMARY.md ← Strategy
    ├── COMPREHENSIVE_DATA_MODELING_STRATEGY.md ← Technical specs
    ├── COMPLETE_CHAT_HISTORY_ANALYSIS.md ← Context
    └── Annotation_Sugestion.md ← MIT Telecom fit
```

### Data Files
```
docs/proj/
└── dadosSuprimentos.xlsx ← ERP data (3 sheets)

data/processed/
├── zenodo_milan_telecom_preprocessed.csv ← Climate (116K)
├── brazilian_demand_factors_preprocessed.csv ← Economic (2,190)
├── brazilian_operators_structured_preprocessed.csv ← Regulatory (290)
└── nova_corrente/
    ├── nova_corrente_preprocessed.csv (4,207 records)
    ├── combined_ml_dataset.csv (2,539 records)
    └── dimensions/ ← Output directory (created by script)
```

### Scripts
```
scripts/
└── 01_create_star_schema_dimensions.py ← Run this first
```

---

## 🙏 ACKNOWLEDGMENTS

**Data Sources:**
- dadosSuprimentos.xlsx (4,207 records) - Nova Corrente ERP
- Zenodo Milan Telecom (116,257 records) - Weather integration
- Brazilian Demand Factors (2,190 records) - Economic/climate signals
- Brazilian Operators (290 records) - B2B contracts
- MIT Telecom (321K records) - Benchmark dataset

**Strategic Documents Analyzed:**
- DEEP_DATASETS_RESEARCH_COMPREHENSIVE_PT_BR.md
- STRATEGIC_DATASET_SELECTION_FINAL_PT_BR.md
- ULTIMATE_COMPLETE_SUMMARY_PT_BR.md
- STRATEGIC_BUSINESS_PROBLEM_SETUP_PT_BR.md
- STRATEGIC_TECHNICAL_DEEP_DIVE_PT_BR.md

**Chat History:**
- Message 1: Best table identification (spare parts demand)
- Message 2: MIT Telecom fit assessment (⭐⭐⭐⭐⭐)
- Message 3: Annotation creation
- Message 4: Comprehensive repository analysis + implementation blueprint

---

## ✅ FINAL CHECKLIST

**Documentation complete:**
- [x] DEMO path roadmaps organized
- [x] PROD path roadmaps organized
- [x] Shared documentation organized
- [x] Path comparison and migration guides created
- [x] README_ROADMAPS.md (this file) updated with path selector

**Scripts complete:**
- [x] 01_create_star_schema_dimensions.py (454 lines)
- [ ] 02_create_fact_demand_daily.py (planned)
- [ ] 03_integrate_climate_data.py (planned)
- [ ] 04_create_ml_master_dataset.py (planned)

**Data verified:**
- [x] dadosSuprimentos.xlsx exists (3 sheets)
- [x] 33 datasets in repository (75% ready)
- [x] 16 datasets analyzed with quality reports
- [x] External datasets located (Milan, Demand Factors, Operators)

**Ready to execute:**
- [x] Week 1 plan defined
- [x] Dimension creation script ready
- [x] External data sources identified
- [x] Success metrics defined

---

**Status:** ✅ **DOCUMENTATION COMPLETE - READY TO EXECUTE**  
**Next Action:** Read QUICK_START_GUIDE.md and run 01_create_star_schema_dimensions.py  
**Timeline:** 4 weeks to <15% MAPE  
**Owner:** Nova Corrente Grand Prix SENAI Team

---

**Last Updated:** November 2025  
**Version:** 4.0 (DEMO vs PROD Split)  
**Documentation Suite:** Organized into DEMO, PROD, and shared folders  
**Status:** ✅ Complete reorganization with path separation

---

## 📚 QUICK NAVIGATION

- **DEMO Path:** [demo/README_DEMO_ROADMAPS.md](demo/README_DEMO_ROADMAPS.md)
- **PROD Path:** [prod/README_PROD_ROADMAPS.md](prod/README_PROD_ROADMAPS.md)
- **Shared Docs:** [shared/](shared/)
- **Changelogs:** [CHANGELOG_DEMO.md](../../CHANGELOG_DEMO.md) | [CHANGELOG_PROD.md](../../CHANGELOG_PROD.md)
- **Architecture Analysis:** [ARCHITECTURE_BIFURCATION_ANALYSIS.md](../../ARCHITECTURE_BIFURCATION_ANALYSIS.md)
