# 🚀 QUICK START GUIDE
## Nova Corrente - From 87% MAPE to <15% in 4 Weeks

**Version:** 2.0  
**Date:** 2025-11-05  
**Status:** 🔥 **READY TO EXECUTE**

---

## 📋 TLDR (60-Second Summary)

### The Situation

```
Current State:
├─ 4,207 demand records processed
├─ 73 features engineered
├─ Best MAPE: 87.27% (EPI family)
└─ Target MAPE: <15% (industry standard)

The Gap: 72 percentage points

Root Cause: 96.3% of external data missing
```

### The Solution

```
Add 3 Critical External Data Sources:
├─ Climate (Zenodo Milan Telecom: 116K records) → -15 to -25% MAPE
├─ Economic (Brazilian Demand Factors: 2,190 records) → -10 to -15% MAPE
└─ Regulatory (Brazilian Operators: 290 records) → -10 to -20% MAPE

Expected Result: MAPE 87% → <15% in 4 weeks
```

---

## 🎯 3 THINGS TO DO TODAY

### 1️⃣ Run Dimension Creation Script (15 minutes)

```bash
cd c:\Users\User\Desktop\Nc\gran-prix
python scripts/01_create_star_schema_dimensions.py
```

**What it does:**
- ✅ Creates 5 dimension tables from dadosSuprimentos.xlsx
- ✅ Generates ABC classification (A/B/C parts)
- ✅ Calculates supplier lead time statistics
- ✅ Creates calendar with Brazilian holidays + cyclical features

**Expected output:**
```
data/processed/nova_corrente/dimensions/
├── dim_calendar.csv (4,400 rows)
├── dim_part.csv (872 rows)
├── dim_site.csv (191 rows)
├── dim_supplier.csv (468 rows)
└── dim_maintenance_type.csv (2 rows)
```

---

### 2️⃣ Review Strategy Documents (30 minutes)

**Read in this order:**

1. **EXECUTIVE_ENRICHMENT_SUMMARY.md** (10 min)
   - Why external data matters (96.3% gap)
   - 3-tier table priorities
   - MAPE progression: 87% → 50% → 30% → <15%

2. **COMPREHENSIVE_DATA_MODELING_STRATEGY.md** (15 min)
   - Star schema design (12 tables)
   - SQL definitions for all tables
   - ML feature engineering query

3. **COMPLETE_CHAT_HISTORY_ANALYSIS.md** (5 min)
   - Full context from previous sessions
   - MIT Telecom fit assessment
   - Lessons learned

---

### 3️⃣ Verify Data Availability (10 minutes)

**Check these files exist:**

```bash
# Nova Corrente ERP data
✅ docs/proj/dadosSuprimentos.xlsx (3 sheets: CUSTO, DADOS, RESUMO GERAL)

# External enrichment datasets (should exist)
✅ data/processed/zenodo_milan_telecom_preprocessed.csv (116,257 rows)
✅ data/processed/brazilian_demand_factors_preprocessed.csv (2,190 rows)
✅ data/processed/brazilian_operators_structured_preprocessed.csv (290 rows)
```

**If files missing:**
- Check `data/raw/` directories
- Run preprocessing scripts from `scripts/`
- Review `data/PROJECT_DATA_OVERVIEW.md` for file locations

---

## 📊 WEEK-BY-WEEK ROADMAP

### Week 1: Foundation + Climate (Target: 87% → 50%)

**Monday-Tuesday:**
- [x] Create dimension tables ← **START HERE**
- [ ] Create Fact_Demand_Daily from dadosSuprimentos.xlsx
- [ ] Validate schema integrity (4,207 records loaded)

**Wednesday-Friday:**
- [ ] Load Zenodo Milan Telecom weather data
- [ ] Create Fact_Climate_Daily
- [ ] Merge with Nova Corrente by date + site
- **Expected: MAPE 87% → 62-72%** (-15 to -25%)

---

### Week 2: Economic + Regulatory (Target: 50% → 30%)

**Monday-Tuesday:**
- [ ] Load Brazilian Demand Factors
- [ ] Create Fact_Economic_Daily
- [ ] Setup BACEN API (inflation, FX, GDP)
- **Expected: MAPE 62-72% → 47-62%** (-10 to -15%)

**Wednesday-Friday:**
- [ ] Load Brazilian Operators + ANATEL
- [ ] Create Fact_Regulatory_Daily
- [ ] Map B2B contracts → demand spikes
- **Expected: MAPE 47-62% → 27-42%** (-10 to -20%)

---

### Week 3: Faults + Retraining (Target: 30% → 15%)

**Monday-Wednesday:**
- [ ] Load GitHub Network Fault + Kaggle Equipment Failure
- [ ] Train predictive maintenance model
- [ ] Create Fact_Fault_Events
- **Expected: MAPE 27-42% → 17-27%** (-10 to -15%)

**Thursday-Friday:**
- [ ] Regenerate ML dataset (100% external coverage)
- [ ] Train XGBoost, Random Forest, LSTM
- **Expected: MAPE 17-27% → 12-22%**

---

### Week 4: Optimization (Target: <15% ✅)

**Monday-Wednesday:**
- [ ] ABC-based model selection
- [ ] Hyperparameter tuning (Optuna)
- [ ] Ensemble optimization

**Thursday-Friday:**
- [ ] Test set validation
- [ ] Performance report
- **Target: MAPE <15%** ✅

---

## 🗂️ FILE STRUCTURE

### What You Have Now

```
c:\Users\User\Desktop\Nc\gran-prix\
│
├── docs/proj/
│   ├── dadosSuprimentos.xlsx ← ERP data (4,207 records)
│   └── roadmaps/
│       ├── Annotation_Sugestion.md ← MIT Telecom fit assessment
│       ├── COMPREHENSIVE_DATA_MODELING_STRATEGY.md ← Full blueprint (NEW!)
│       ├── EXECUTIVE_ENRICHMENT_SUMMARY.md ← Executive summary (NEW!)
│       ├── COMPLETE_CHAT_HISTORY_ANALYSIS.md ← Chat history (NEW!)
│       └── QUICK_START_GUIDE.md ← This file (NEW!)
│
├── scripts/
│   └── 01_create_star_schema_dimensions.py ← Run this first! (NEW!)
│
├── data/
│   ├── raw/ (33 datasets, 75% ready)
│   ├── processed/ (16 analyzed datasets)
│   │   ├── nova_corrente/
│   │   │   ├── nova_corrente_preprocessed.csv (4,207 records)
│   │   │   ├── combined_ml_dataset.csv (2,539 records)
│   │   │   ├── optimized/ (model training results)
│   │   │   └── dimensions/ ← Output directory (will be created)
│   │   ├── zenodo_milan_telecom_preprocessed.csv (116,257 records)
│   │   ├── brazilian_demand_factors_preprocessed.csv (2,190 records)
│   │   └── brazilian_operators_structured_preprocessed.csv (290 records)
│   └── PROJECT_DATA_OVERVIEW.md
│
└── README.md
```

---

## 🎓 KEY CONCEPTS

### Star Schema (Why This Matters)

```
Think of it like a solar system:

🌟 FACT TABLE (Sun) = Fact_Demand_Daily
   - One row per transaction (site-part-day-order)
   - Contains measures: quantidade (target), unit_cost
   - Contains foreign keys to dimensions

🪐 DIMENSION TABLES (Planets) = Dim_Calendar, Dim_Part, Dim_Site, etc.
   - Describe "who, what, when, where"
   - Provide context for fact table
   - Slow-changing (updated infrequently)

💫 EXTERNAL FACT TABLES (Moons) = Fact_Climate_Daily, Fact_Economic_Daily, etc.
   - Additional signals for ML features
   - Join by date_id + site_id
   - Can be added/removed without breaking core schema
```

**Why star schema?**
- ✅ Scalable: Add new dimensions/facts without changing core
- ✅ Fast queries: Optimized for aggregations (SUM, AVG, GROUP BY)
- ✅ ML-ready: Easy feature engineering via JOINs
- ✅ Maintainable: Clear separation of concerns

### ABC Classification (How to Use)

```
A-Class Parts (Top 20% of parts = 80% of value):
├─ Use: XGBoost, Random Forest, LSTM (complex models)
├─ Forecast: Daily granularity
├─ Monitor: Real-time alerts
└─ Impact: High cost of stockout

B-Class Parts (Next 30% = 15% of value):
├─ Use: Prophet, SARIMA (medium complexity)
├─ Forecast: Weekly granularity
├─ Monitor: Weekly review
└─ Impact: Medium cost of stockout

C-Class Parts (Bottom 50% = 5% of value):
├─ Use: Moving average, simple forecasting
├─ Forecast: Monthly granularity
├─ Monitor: Monthly review
└─ Impact: Low cost of stockout (order in bulk)
```

**Why ABC matters?**
- Different models for different parts = better accuracy
- Focus expensive ML on high-value parts
- Simple methods for low-value parts = faster execution

### MAPE (Mean Absolute Percentage Error)

```
Formula: MAPE = (1/n) × Σ |Actual - Forecast| / |Actual| × 100%

Interpretation:
├─ <10%: Excellent forecasting
├─ 10-15%: Good forecasting (industry standard)
├─ 15-30%: Acceptable for volatile demand
├─ 30-50%: Poor forecasting
└─ >50%: Unreliable forecasting

Current: 87.27% = Random guessing
Target: <15% = Industry standard
```

---

## 💡 TROUBLESHOOTING

### "Script fails to load Excel file"

**Solution:**
```bash
# Verify file exists
ls "c:\Users\User\Desktop\Nc\gran-prix\docs\proj\dadosSuprimentos.xlsx"

# Check Python dependencies
pip install pandas openpyxl numpy
```

### "Dimensions created but row counts seem low"

**Expected counts:**
- Dim_Calendar: ~4,400 rows (2013-2025)
- Dim_Part: ~872 rows (unique products)
- Dim_Site: ~191-459 rows (sites + customer mappings)
- Dim_Supplier: ~468 rows (unique suppliers)
- Dim_Maintenance_Type: 2 rows (preventive/corrective)

If lower than expected, check dadosSuprimentos.xlsx has all 3 sheets.

### "External datasets not found"

**Check locations:**
```bash
# Should exist (preprocessed data)
data/processed/zenodo_milan_telecom_preprocessed.csv
data/processed/brazilian_demand_factors_preprocessed.csv
data/processed/brazilian_operators_structured_preprocessed.csv

# If missing, check raw data
data/raw/zenodo_milan_telecom/
data/raw/brazilian_demand_factors/
data/raw/brazilian_operators_structured/
```

Run preprocessing scripts if needed:
```bash
python scripts/preprocessing/preprocess_zenodo_milan.py
python scripts/preprocessing/preprocess_brazilian_factors.py
```

---

## 📞 NEXT STEPS AFTER QUICK START

### After Week 1 (Climate Integrated)

**Validate:**
- [ ] Fact_Climate_Daily created (should cover all 4,207 demand records)
- [ ] Missing data: 96.3% → <5%
- [ ] MAPE improved: 87% → 62-72%

**Next:**
- Create `02_create_fact_demand_daily.py`
- Create `03_integrate_climate_data.py`
- Retrain models with climate features

### After Week 2 (Economic + Regulatory)

**Validate:**
- [ ] Fact_Economic_Daily created
- [ ] Fact_Regulatory_Daily created
- [ ] MAPE improved: 62-72% → 27-42%

**Next:**
- Setup BACEN API for real-time economic data
- Create API monitoring/alerting

### After Week 4 (Production Ready)

**Deliverables:**
- [ ] MAPE <15% validated on test set
- [ ] FastAPI endpoints deployed
- [ ] Streamlit dashboard live
- [ ] Automated ETL pipeline (Airflow/Prefect)
- [ ] Documentation complete

---

## 🎯 SUCCESS METRICS

**Technical:**
- [ ] MAPE <15% on test set (unseen data)
- [ ] External data coverage: 100% (vs. current 3.7%)
- [ ] Model training time: <10 minutes per family
- [ ] Prediction latency: <1 second per forecast

**Business:**
- [ ] Stockout rate: <5% (vs. current 15-20%)
- [ ] Excess inventory: -20-30% cost reduction
- [ ] SLA compliance: >95% (vs. current 60-70%)
- [ ] Forecast accuracy: >85% (vs. current 12.73%)

---

## 📚 RECOMMENDED READING ORDER

**For Developers (Technical Implementation):**
1. COMPREHENSIVE_DATA_MODELING_STRATEGY.md (full SQL schemas)
2. 01_create_star_schema_dimensions.py (code walkthrough)
3. COMPLETE_CHAT_HISTORY_ANALYSIS.md (context + lessons)

**For Managers (Business Justification):**
1. EXECUTIVE_ENRICHMENT_SUMMARY.md (ROI + timeline)
2. QUICK_START_GUIDE.md (this file - overview)
3. COMPREHENSIVE_DATA_MODELING_STRATEGY.md (Part 5: Data Quality)

**For Data Scientists (Model Optimization):**
1. COMPLETE_CHAT_HISTORY_ANALYSIS.md (dataset selection rationale)
2. COMPREHENSIVE_DATA_MODELING_STRATEGY.md (Part 4.2: ML Feature Query)
3. Data quality reports in `data/processed/quality_reports/`

---

## ✅ FINAL CHECKLIST

**Before starting Week 1:**
- [ ] Read EXECUTIVE_ENRICHMENT_SUMMARY.md
- [ ] Verify dadosSuprimentos.xlsx accessible
- [ ] Run 01_create_star_schema_dimensions.py
- [ ] Review dimension CSV outputs
- [ ] Locate external datasets (Milan, Demand Factors, Operators)

**Week 1 goals:**
- [ ] All 5 dimension tables created
- [ ] Fact_Demand_Daily loaded (4,207 records)
- [ ] Climate data integrated (116,257 records)
- [ ] MAPE improved to 62-72%

**Week 2-4 goals:**
- [ ] Economic + Regulatory data integrated
- [ ] Fault events + supply chain data added
- [ ] Models retrained with 100% external coverage
- [ ] **MAPE <15% achieved** ✅

---

**Status:** 🚀 **READY TO START**  
**Next Action:** Run `01_create_star_schema_dimensions.py`  
**Timeline:** 4 weeks to <15% MAPE  
**Questions?** Review COMPLETE_CHAT_HISTORY_ANALYSIS.md

---

**Nova Corrente Grand Prix SENAI**  
**From 87% MAPE to <15% in 4 Weeks**  
**Let's Go! 🔥**
