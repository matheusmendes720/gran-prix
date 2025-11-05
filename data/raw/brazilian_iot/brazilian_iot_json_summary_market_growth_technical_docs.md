# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Brazilian IoT Market (JSON Summary)

**Dataset ID:** `brazilian_iot`  
**Source:** Industry Research (MVNO Index, Mordor Intelligence)  
**Status:** ✅ JSON Summary (CSV structured version available)  
**Relevance:** ⭐⭐⭐⭐ (High - IoT Expansion → Infrastructure Maintenance)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Brazilian IoT Market Summary  
**Format:** JSON (summary data)  
**CSV Version:** `data/raw/brazilian_iot_structured/brazilian_iot_market_structured.csv`  
**Date Range:** 2020-2024 (monthly data points)  
**Business Context:**
- Brazilian IoT connection growth tracking
- Annual growth rate (~18% CAGR)
- Sector-specific analysis (Agriculture, Logistics, Smart Cities, Utilities, Retail)
- **IoT expansion → Infrastructure maintenance demand**

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Source:** Industry Research (MVNO Index, Mordor Intelligence)  
**Research:** Brazilian IoT Market Analysis  
**Data Basis:** Industry reports, market research  
**Region:** Brazil

### Academic References

**Papers:**
1. **ITU (2023).** "Big Data for Development: Brazil Country Report." International Telecommunication Union.

2. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

---

## 📊 DATA STRUCTURE

### JSON Schema

```json
{
  "dataset_name": "Brazilian IoT Market Summary",
  "source": "Industry Research (MVNO Index, Mordor Intelligence)",
  "created_at": "2025-10-31T22:50:18.468067",
  "data_points": [
    {
      "date": "2020-10",
      "month": 10,
      "year": 2020,
      "iot_connections_millions": 28.0,
      "growth_rate_annual": 0.0
    },
    ...
  ]
}
```

### Growth Statistics

| Year | Connections (M) | Growth Rate | Significance |
|------|-----------------|-------------|--------------|
| **2020** | 28.0M | Baseline | Initial market |
| **2021** | 33.0M | 18% | Accelerated growth |
| **2022** | 38.5M | 17% | Stable growth |
| **2023** | 42.0M | 9% | Market maturity |
| **2024** | 46.2M | 10% | Continued growth |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **IoT expansion** → Infrastructure maintenance demand
- ✅ Sector-specific trends (Logistics, Smart Cities relevant)
- ✅ Annual growth tracking (~18% CAGR)
- ✅ Forecast data for planning

**Adaptation Strategy:**
```python
# IoT Expansion → Maintenance Demand (Same as structured version)
# See: data/raw/brazilian_iot_structured/CONTEXT_TECHNICAL_DOCS.md
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/brazilian_iot/brazilian_iot_summary.json` (JSON summary)
- `data/raw/brazilian_iot/brazilian_iot_timeline.csv` (Timeline CSV)

**Structured Data:**
- `data/raw/brazilian_iot_structured/brazilian_iot_market_structured.csv` (✅ Use this for ML)

---

## ✅ PREPROCESSING NOTES

### JSON → CSV Conversion

**Already Done:** Structured CSV version available at:
- `data/raw/brazilian_iot_structured/brazilian_iot_market_structured.csv`

**Use Structured Version:** The CSV version has proper schema normalization and is ready for ML training.

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ✅ Summary data - Use structured CSV version for ML

**Recommendation:** Use the **structured CSV version** (`brazilian_iot_structured/`) for ML training. This JSON is summary data only.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

