# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## GSMA Latin America Regional Dataset

**Dataset ID:** `gsma_regional`  
**Source:** GSMA (Global System for Mobile Communications Association)  
**Status:** ✅ Processed  
**Relevance:** ⭐⭐⭐ (Medium - Regional Context, Reference Data)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Latin America Regional Telecom Market Analysis  
**Records:** 310+ rows (quarterly data)  
**Features:** 10 columns (date, country, region, users, market share, ARPU, 5G penetration)  
**Date Range:** 2014-Q1 to 2024-Q4 (quarterly)  
**Target Variable:** `mobile_internet_users_millions` - Mobile internet users in millions

**Business Context:**
- Latin America regional telecom market analysis
- Country-specific data (Brazil, Mexico, Argentina, Colombia, Chile, Peru)
- Market share tracking (Brazil dominant)
- 5G penetration tracking (0% in 2014 → 60%+ in 2024)
- **Regional context** for Nova Corrente (Brazil in Latin America)

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Organization:** GSMA (Global System for Mobile Communications Association)  
**URL:** https://www.gsma.com/latinamerica/  
**Data Basis:** GSMA market research, operator data  
**Region:** Latin America  
**Update Frequency:** Quarterly/Annual

### Academic References

**Papers:**
1. **GSMA (2024).** "The Mobile Economy Latin America 2024." GSMA Intelligence. https://www.gsma.com/mobileeconomy/

2. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

3. **ITU (2023).** "Big Data for Development: Brazil Country Report." International Telecommunication Union.

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `date` | DateTime | 2014-03-31 to 2024-12-31 | Quarterly date | Temporal key |
| `year` | Integer | 2014-2024 | Year | Temporal feature |
| `quarter` | Integer | 1-4 | Quarter | Temporal feature |
| `country` | String | brazil, mexico, argentina, etc. | Country name | Geographic identifier |
| `region` | String | latin_america | Geographic region | Regional context |
| `mobile_internet_users_millions` | Float | 12-120+ | **TARGET: Mobile internet users** | **Market size ⭐** |
| `market_share` | Float | 0.05-0.45 | Market share (0-1) | Market dominance |
| `arpu_usd` | Float | 5-15 | ARPU (USD) | Revenue per user |
| `5g_penetration_pct` | Float | 0-0.65 | 5G penetration (0-1) | Technology adoption |
| `total_regional_users_millions` | Float | 225-300+ | Total regional users | Market size |

### Market Statistics (2024)

| Country | Users (M) | Market Share | 5G Penetration | Relevance for Nova Corrente |
|---------|-----------|--------------|----------------|----------------------------|
| **Brazil** | ~120M | 45% | ~65% | ⭐⭐⭐⭐⭐ **Primary market** |
| **Mexico** | ~50M | 18% | ~60% | ⭐⭐⭐ Regional context |
| **Argentina** | ~30M | 10% | ~55% | ⭐⭐ Regional context |
| **Colombia** | ~25M | 9% | ~50% | ⭐⭐ Regional context |
| **Chile** | ~15M | 5% | ~55% | ⭐ Regional context |
| **Peru** | ~18M | 6% | ~45% | ⭐ Regional context |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **Regional context** for Nova Corrente (Brazil in Latin America)
- ✅ Market share tracking (Brazil dominance)
- ✅ 5G penetration trends (technology adoption)
- ✅ Quarterly granularity (good for forecasting)

**Limitations:**
- ⚠️ Regional/aggregated data (not Brazilian-specific detail)
- ⚠️ Reference data only (not for primary model training)

**Adaptation Strategy:**
```python
# GSMA Regional → Nova Corrente (Reference Context)
# Use for: Regional context, market share validation
# Not for: Primary model training (use Anatel/Brazilian data instead)
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/gsma_regional/gsma_latin_america_regional.csv` (CSV format, 310+ rows)

**Processed Data:**
- `data/processed/gsma_regional_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Medium relevance - Regional context and reference data only

**Recommendation:** Use for regional context and market validation. Not for primary model training (use Anatel/Brazilian data instead).

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

