# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## ITU Brazil Indicators Dataset

**Dataset ID:** `itu_indicators`  
**Source:** ITU (International Telecommunication Union)  
**Status:** ✅ Processed  
**Relevance:** ⭐⭐⭐ (Medium - Reference Indicators, Not Primary Training)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** ITU Telecom Indicators for Brazil  
**Records:** 74+ rows (monthly data)  
**Features:** 11 columns (date, penetration rates, digital divide, big data readiness)  
**Date Range:** 2019-01 to 2024-12 (monthly)  
**Target Variable:** `internet_penetration_pct` - Internet penetration percentage

**Business Context:**
- ITU standardized telecom indicators
- Penetration rates (internet, mobile broadband, fixed broadband)
- Digital divide tracking (urban vs rural)
- Big data readiness score
- **Reference indicators** for Nova Corrente context

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Organization:** ITU (International Telecommunication Union)  
**URL:** https://www.itu.int/en/ITU-D/Statistics/Pages/default.aspx  
**Data Basis:** ITU standardized indicators  
**Country:** Brazil  
**Update Frequency:** Monthly/Annual

### Academic References

**Papers:**
1. **ITU (2023).** "Big Data for Development: Brazil Country Report." International Telecommunication Union.

2. **ITU (2024).** "Measuring Digital Development: Facts and Figures 2024." ITU Publications.

3. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `date` | DateTime | 2019-01-31 to 2024-12-31 | Monthly date | Temporal key |
| `year` | Integer | 2019-2024 | Year | Temporal feature |
| `month` | Integer | 1-12 | Month | Temporal feature |
| `internet_penetration_pct` | Float | 86.6-92.0% | **TARGET: Internet penetration** | **Market maturity ⭐** |
| `mobile_broadband_penetration_pct` | Float | 83.0-90.0% | Mobile broadband penetration | Technology adoption |
| `fixed_broadband_penetration_pct` | Float | 45.0-55.0% | Fixed broadband penetration | Infrastructure coverage |
| `urban_internet_pct` | Float | 92.0-95.0% | Urban internet penetration | Urban coverage |
| `rural_internet_pct` | Float | 65.0-75.0% | Rural internet penetration | Rural coverage |
| `digital_divide_pct` | Float | 25.0-27.0% | Digital divide (urban-rural gap) | Inequality metric |
| `big_data_readiness_score` | Float | 0.6-0.7 | Big data readiness (0-1) | Technology readiness |
| `country` | String | brazil | Country identifier | Geographic identifier |

### Penetration Trends (2019-2024)

| Indicator | 2019 | 2024 | Growth | Significance |
|-----------|------|------|--------|--------------|
| **Internet Penetration** | 86.6% | 92.0% | +6.2% | Market maturity |
| **Mobile Broadband** | 83.0% | 90.0% | +8.4% | Mobile dominance |
| **Fixed Broadband** | 45.0% | 55.0% | +22% | Fiber expansion |
| **Digital Divide** | 27.0% | 25.0% | -7.4% | Inequality reduction |
| **Big Data Readiness** | 0.6 | 0.7 | +17% | Technology maturity |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **Standardized indicators** (ITU benchmarks)
- ✅ Market maturity tracking (penetration rates)
- ✅ Digital divide analysis (urban vs rural)
- ✅ Technology readiness (big data readiness)

**Limitations:**
- ⚠️ **Reference indicators only** (not for primary model training)
- ⚠️ Aggregated national data (not regional/operational detail)
- ⚠️ Monthly granularity (not daily/hourly)

**Adaptation Strategy:**
```python
# ITU Indicators → Nova Corrente (Reference Context)
# Use for: Market maturity validation, digital divide analysis
# Not for: Primary model training (use Anatel/Brazilian data instead)
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/itu_indicators/itu_brazil_indicators.csv` (CSV format, 74+ rows)

**Processed Data:**
- `data/processed/itu_indicators_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Medium relevance - Reference indicators and context only

**Recommendation:** Use for market maturity validation and digital divide analysis. Not for primary model training (use Anatel/Brazilian structured data instead).

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

