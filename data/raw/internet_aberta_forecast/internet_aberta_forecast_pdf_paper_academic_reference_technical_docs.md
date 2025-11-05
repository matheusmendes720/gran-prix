# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Internet Aberta Forecast Paper

**Dataset ID:** `internet_aberta_forecast`  
**Source:** Academic Paper (PDF)  
**Status:** ⏳ Pending PDF Parsing  
**Relevance:** ⭐⭐⭐ (Medium - Academic Reference, Table Extraction Needed)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Data Traffic Demand Forecast for Brazil - Academic Paper  
**Format:** PDF (Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf)  
**Status:** ⏳ Requires PDF → Table extraction  
**Business Context:**
- Academic paper on Brazilian data traffic demand forecasting
- Predictive modeling for Brazilian telecom market
- Methodology and results documentation
- **Reference paper** for Nova Corrente demand forecasting

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Paper:** "Data Traffic Demand Forecast for Brazil"  
**Format:** PDF  
**File:** Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf  
**Source:** Internet Aberta (Open Internet) research  
**URL:** Research paper (PDF format)

### Academic References

**Papers:**
1. **Internet Aberta (2024).** "Data Traffic Demand Forecast for Brazil." Research Paper (PDF).

2. **Related:** ITU, OECD, Anatel research on Brazilian telecom forecasting

---

## 📊 DATA STRUCTURE

### Expected Data (After PDF Parsing)

| Column | Type | Description | Business Context |
|--------|------|-------------|------------------|
| `date` | DateTime | Monthly/Quarterly date | Temporal key |
| `region` | String | Northeast, Southeast, etc. | Geographic region |
| `data_traffic_tb` | Float | Data traffic (TB) | Traffic volume |
| `forecast_tb` | Float | Forecasted traffic (TB) | ML forecast |
| `growth_rate` | Float | Growth rate | Traffic growth |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **Academic reference** for demand forecasting methodology
- ✅ Brazilian data traffic forecasting (relevant context)
- ✅ Methodology documentation (forecasting techniques)

**Limitations:**
- ⚠️ **PDF format** - Requires table extraction
- ⚠️ Academic paper (not operational data)
- ⚠️ Reference/documentation only

**Adaptation Strategy:**
```python
# Internet Aberta Forecast → Nova Corrente (Reference Methodology)
# 1. Extract tables from PDF
# 2. Use methodology from paper
# 3. Adapt to Nova Corrente maintenance demand forecasting
# NOT for primary model training (use operational datasets)
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/internet_aberta_forecast/Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf` (PDF, requires parsing)

---

## ✅ PREPROCESSING NOTES

### Pending Tasks

1. **PDF Parsing:**
   - Extract tables from PDF
   - Convert to CSV format
   - Extract methodology documentation

2. **Schema Normalization:**
   - `date` → datetime format
   - `data_traffic_tb` → float
   - `region` → standardized region names
   - `forecast_tb` → float (forecast column)

3. **Validation:**
   - Missing values: Forward fill
   - Outliers: IQR method
   - Range checks: Traffic (>=0)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⏳ Pending - Requires PDF table extraction

**Recommendation:** Use as **academic reference** for forecasting methodology. NOT for primary model training (use operational datasets like Anatel/Brazilian structured data).

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

