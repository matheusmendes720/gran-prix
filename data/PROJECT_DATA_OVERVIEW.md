# 📊 PROJECT DATA OVERVIEW
## Nova Corrente Demand Forecasting System

**Last Updated:** 2025-11-01  
**Status:** ✅ Complete Documentation & Organization

---

## 🎯 QUICK NAVIGATION

| Document | Purpose | Location |
|----------|---------|----------|
| **DATASETS_INDEX.md** | Complete index by category | `data/raw/DATASETS_INDEX.md` |
| **DATASETS_EXECUTIVE_SUMMARY.md** | Executive summary & status | `data/raw/DATASETS_EXECUTIVE_SUMMARY.md` |
| **PROJECT_DATA_OVERVIEW.md** | This document - Complete overview | `data/PROJECT_DATA_OVERVIEW.md` |

---

## 📁 DATA DIRECTORY STRUCTURE

```
data/
├── raw/                          📥 RAW DATA (33 datasets)
│   ├── [DATASET_ID]/
│   │   ├── [data files]
│   │   └── [DATASET_ID]_[SOURCE]_[CONTEXT]_technical_docs.md
│   │
│   ├── DATASETS_INDEX.md         📚 Complete index (this file)
│   └── DATASETS_EXECUTIVE_SUMMARY.md  📊 Executive summary
│
├── processed/                    🔄 PROCESSED DATA
│   ├── *_preprocessed.csv        Individual preprocessed datasets
│   ├── unified_dataset.csv       Unified merged dataset
│   ├── unified_dataset_with_factors.csv  ⭐ Main dataset (27.25 MB, 118K rows)
│   └── samples/                  Sample data files
│
├── training/                     🎓 TRAINING DATA
│   ├── unknown_train.csv         ⭐ Main training split (93,881 rows)
│   ├── unknown_test.csv          Test split (23,471 rows)
│   ├── CONN-001_train.csv        Item-specific training
│   ├── CONN-001_test.csv         Item-specific test
│   ├── metadata.json             Training metadata
│   └── training_summary.json     Statistical summary
│
├── registry/                     📝 METADATA REGISTRY
│   ├── datasets_registry.json   Dataset discovery registry
│   └── live_fetch_results.json   Live fetch results
│
└── PROJECT_DATA_OVERVIEW.md     📊 This document
```

---

## 📊 DATASET COLLECTION STATISTICS

### By Source

| Source | Count | Status |
|--------|-------|--------|
| **Kaggle** | 7 | ✅ Ready |
| **Zenodo** | 2 | ✅ Ready |
| **GitHub** | 2 | ✅ Ready |
| **Anatel** | 6 | ⏳ 50% Ready |
| **Brazilian (Structured)** | 8 | ✅ Ready |
| **Reference (GSMA/ITU/OECD)** | 5 | ✅ Ready |
| **Academic** | 2 | ⏳ Pending |
| **Test** | 1 | ✅ Ready |
| **TOTAL** | **33** | **75% Ready** |

### By Relevance

| Relevance | Count | Use Case |
|-----------|-------|----------|
| ⭐⭐⭐⭐⭐ **Essential** | 8 | Primary ML training |
| ⭐⭐⭐⭐ **High** | 12 | Secondary ML training |
| ⭐⭐⭐ **Medium** | 8 | Context/Reference |
| ⭐⭐ **Low** | 5 | Archive/Ignore |

---

## 🔍 KEY DATASETS HIGHLIGHTS

### ⭐ ESSENTIAL (Must Use for Training)

1. **Zenodo Milan Telecom** (116K rows)
   - ONLY public dataset with telecom + weather integration
   - Weather correlations validated (inverse for Nova Corrente)

2. **Brazilian Operators Structured** (290 rows)
   - B2B contracts with operators = Stable demand (CRITICAL!)
   - Vivo, Claro, TIM market share tracking

3. **Brazilian Demand Factors** (2,190 rows)
   - Integrated external factors (economic, climate, regulatory)
   - Daily granularity, 16 columns

4. **Kaggle Equipment Failure** (10K rows)
   - Predictive maintenance → Spare parts demand
   - AI4I 2020 competition data

5. **GitHub Network Fault** (7.4K rows)
   - Telecom-specific fault patterns
   - Telstra competition data

---

## 📈 PROCESSED DATA SUMMARY

### Main Unified Dataset

**File:** `data/processed/unified_dataset_with_factors.csv`
- **Size:** 27.25 MB
- **Rows:** 118,082
- **Columns:** 31
- **Date Range:** 2013-11-01 to 2025-01-31 (11+ years)
- **Status:** ✅ Ready for ML training

### Training Splits

| Split | File | Rows | Size | Purpose |
|-------|------|------|------|---------|
| **Train** | `unknown_train.csv` | 93,881 | 11.61 MB | Model training |
| **Test** | `unknown_test.csv` | 23,471 | 2.90 MB | Model validation |
| **Full** | `unknown_full.csv` | 117,352 | 14.51 MB | Complete dataset |

---

## 🎯 ML TRAINING READINESS

### Ready for Training (~25 datasets)

**High Priority (8 datasets):**
- ✅ Zenodo Milan Telecom
- ✅ Brazilian Operators Structured
- ✅ Brazilian Demand Factors
- ✅ Kaggle Equipment Failure
- ✅ GitHub Network Fault
- ✅ Zenodo Broadband Brazil
- ✅ GitHub 5G3E
- ✅ Kaggle Logistics Warehouse

**Medium Priority (12 datasets):**
- ✅ Brazilian IoT/Fiber Structured
- ✅ Anatel Spectrum/Municipal
- ✅ Kaggle Supply Chain/Smart Logistics
- ✅ Reference datasets (for context)

**Low Priority (5 datasets):**
- ✅ Kaggle Daily Demand (MVP only)
- ✅ Test Dataset (validation)
- ⚠️ Low relevance datasets (archive)

### Pending Processing (~8 datasets)

**Anatel HTML/JSON (6 files):**
- ⏳ Anatel Comprehensive (HTML/CSV mixed)
- ⏳ Anatel Broadband (HTML)
- ⏳ Anatel Mobile Accesses (HTML)
- ⏳ Anatel Mobile Brazil (HTML/JSON)

**Academic Papers (2 files):**
- ⏳ Internet Aberta Forecast (PDF)
- ⏳ Springer Digital Divide (HTML/JSON)

---

## 📚 DOCUMENTATION STATUS

### Technical Documentation

- ✅ **33 technical docs files** - 100% complete
- ✅ **All files renamed** with descriptive names
- ✅ **DATASETS_INDEX.md** - Complete navigation guide
- ✅ **DATASETS_EXECUTIVE_SUMMARY.md** - Executive overview
- ✅ **PROJECT_DATA_OVERVIEW.md** - This document

### Documentation Quality

- ✅ **Source references** - All verified links
- ✅ **Academic papers** - DOIs and citations
- ✅ **Code examples** - Python implementations
- ✅ **Business context** - Nova Corrente applications
- ✅ **ML algorithms** - Recommendations per dataset

---

## 🚀 RECOMMENDED NEXT STEPS

### Immediate (Week 1)

1. **Start ML Training** with Essential Datasets:
   - Zenodo Milan Telecom
   - Brazilian Operators Structured
   - Brazilian Demand Factors

2. **Validate Pipeline** with Test Dataset:
   - `test_dataset` for pipeline validation

3. **Prepare Unified Dataset** for training:
   - `unified_dataset_with_factors.csv` (already processed)

### Short-term (Week 2-3)

4. **Parse Pending Datasets:**
   - Anatel HTML/JSON files
   - Academic PDF/HTML papers

5. **Feature Engineering:**
   - Extract features from 5G3E (767+ columns)
   - Engineer Brazilian context features

6. **Model Training:**
   - ARIMA/SARIMA baseline
   - Prophet with external regressors
   - LSTM for complex patterns

### Medium-term (Week 4-5)

7. **Ensemble Modeling:**
   - Combine ARIMA + Prophet + LSTM
   - Validate with Brazilian context

8. **Deployment:**
   - Integrate with Nova Corrente systems
   - Monitor performance in production

---

## 📝 NOTES

- **All datasets documented** with complete technical details
- **Naming convention** ensures unique, searchable files
- **Status clearly marked** (Ready, Pending, Low Relevance)
- **Recommendations provided** for each dataset category

---

## 🔗 RELATED DOCUMENTATION

- **Strategic Docs:** `docs/proj/strategy/README_STRATEGIC_DOCS.md`
- **Dataset Research:** `docs/proj/strategy/DEEP_DATASETS_RESEARCH_COMPREHENSIVE_PT_BR.md`
- **Business Problem:** `docs/proj/strategy/STRATEGIC_BUSINESS_PROBLEM_SETUP_PT_BR.md`
- **Main README:** `README.md`

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

