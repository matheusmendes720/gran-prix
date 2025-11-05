# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Test Dataset (Synthetic)

**Dataset ID:** `test_dataset`  
**Source:** Locally Generated  
**Status:** ✅ Created & Ready for ML  
**Relevance:** ⭐⭐⭐ (Medium - Pipeline Validation Only)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Pipeline validation and structure testing  
**Records:** 730 rows (2 years daily)  
**Features:** 7 columns  
**Date Range:** 2023-01-01 to 2024-12-30  
**Target Variable:** `Order_Demand` - Daily demand

**Business Context:**
- Synthetic dataset for pipeline validation
- Tests data structure and preprocessing
- Validates ML model compatibility
- **NOT for production model training**

---

## 🔗 SOURCE REFERENCES

### Source

**Created:** Locally by Nova Corrente team  
**Purpose:** Pipeline validation  
**Status:** Test dataset only  
**Not for:** Production model training

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `Date` | DateTime | 2023-01-01 to 2024-12-30 | Daily date | Temporal key |
| `Product` | String | "CONN-001" | Product identifier | Single item |
| `Order_Demand` | Integer | 3-11 | Daily demand | **TARGET VARIABLE** |
| `Site` | String | "TORRE001" | Site identifier | Single site |
| `Category` | String | "Conectores" | Product category | Category classification |
| `Cost` | Float | 300.0 | Unit cost | Fixed cost |
| `Lead_Time` | Integer | 14 | Lead time (days) | Fixed lead time |

### Statistics

| Metric | Value | Notes |
|--------|-------|-------|
| Mean Demand | 6.93 units/day | Average daily demand |
| Std Demand | 2.51 units | Demand variability |
| Min Demand | 3 units | Minimum observed |
| Max Demand | 11 units | Maximum observed |
| Lead Time | 14 days | Fixed lead time |
| Cost | 300.0 | Fixed unit cost |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Purpose:**
- ✅ Pipeline validation
- ✅ Structure testing
- ✅ Model compatibility checks
- ✅ Preprocessing validation

**Limitations:**
- ⚠️ Synthetic data (not real)
- ⚠️ Single item (CONN-001)
- ⚠️ Single site (TORRE001)
- ⚠️ **NOT for production model training**

---

## 🤖 ML ALGORITHMS APPLICABLE

### Test Algorithms

1. **ARIMA/SARIMA** (Baseline)
   - **Purpose:** Validate time-series pipeline
   - **Expected Performance:** Not applicable (test only)

2. **Prophet** (Baseline)
   - **Purpose:** Validate Prophet integration
   - **Expected Performance:** Not applicable (test only)

3. **Linear Regression** (Baseline)
   - **Purpose:** Validate regression pipeline
   - **Expected Performance:** Not applicable (test only)

---

## 📈 VALIDATION SCENARIOS

### Test Cases

1. **Data Loading:**
   - ✅ CSV reading
   - ✅ Date parsing
   - ✅ Schema validation

2. **Preprocessing:**
   - ✅ Missing value handling
   - ✅ Outlier detection
   - ✅ Feature engineering

3. **Model Training:**
   - ✅ Train/test split
   - ✅ Model fitting
   - ✅ Prediction generation

4. **Pipeline Integration:**
   - ✅ End-to-end pipeline
   - ✅ Error handling
   - ✅ Logging

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/test_dataset/test_data.csv` (37 KB, 730 rows)

**Processed Data:**
- `data/processed/test_dataset_preprocessed.csv` (0.05 MB, 730 rows)

**Training Data:**
- `data/training/CONN-001_train.csv` (584 rows, 80% split)
- `data/training/CONN-001_test.csv` (146 rows, 20% split)
- `data/training/CONN-001_full.csv` (730 rows, 100%)

---

## ✅ PREPROCESSING NOTES

### Transformations Applied

1. **Schema Normalization:**
   - `Date` → `date` (datetime format)
   - `Product` → `item_id`
   - `Order_Demand` → `quantity`
   - `Site` → `site_id`
   - `Category` → `category`
   - `Cost` → `cost`
   - `Lead_Time` → `lead_time`

2. **Feature Engineering:**
   - Date features (year, month, day, weekday)
   - Demand statistics (mean, std, rolling averages)

3. **Validation:**
   - No missing values
   - All columns validated
   - Range checks applied

---

## 🔗 ADDITIONAL RESOURCES

### Related Datasets

- Kaggle Daily Demand (similar structure)
- MIT Telecom (real telecom data)
- Zenodo Milan (real telecom + weather data)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ✅ Test dataset - Pipeline validation only

**Important:** This is a **synthetic test dataset**. Do NOT use for production model training.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

