# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Subscriber Forecasting Dataset

**Dataset ID:** `subscriber_forecasting`  
**Source:** Industry Research & Market Reports  
**Status:** ✅ Processed  
**Relevance:** ⭐⭐ (Low - Subscriber Forecasting, Not Maintenance Demand)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Subscriber Technology Migration & Forecasting Data  
**Records:** 1,154+ rows (monthly data)  
**Features:** 9 columns (date, technology, operator, subscribers, technology share, operator share, trend)  
**Date Range:** 2019-01 to 2024-12 (monthly)  
**Target Variable:** `subscribers_millions` - Subscribers in millions

**Business Context:**
- Subscriber technology migration tracking (2G → 3G → 4G → 5G)
- Operator-specific subscriber tracking (Vivo, Claro, TIM, Others)
- Technology share analysis (2G declining, 5G growing)
- Operator market share tracking
- **NOTE:** Subscriber forecasting, NOT maintenance demand forecasting

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Source:** Industry Research & Market Reports  
**Research:** Subscriber Technology Migration Analysis  
**Data Basis:** Anatel, operator data, market research  
**Region:** Brazil

### Academic References

**Papers:**
1. **Anatel (2024).** "Subscriber Technology Migration Report 2024." Agência Nacional de Telecomunicações.

2. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `date` | DateTime | 2019-01-31 to 2024-12-31 | Monthly date | Temporal key |
| `year` | Integer | 2019-2024 | Year | Temporal feature |
| `month` | Integer | 1-12 | Month | Temporal feature |
| `technology` | String | 2g, 3g, 4g, 5g | Technology generation | Technology migration |
| `operator` | String | vivo, claro, tim, others | Operator name | B2B partner |
| `subscribers_millions` | Float | 0.2-60+ | **TARGET: Subscribers** | **Market size ⭐** |
| `technology_share_pct` | Float | 0.35-60.15% | Technology share | Technology dominance |
| `operator_market_share` | Float | 0.20-0.35 | Operator market share | Market dominance |
| `trend` | String | declining, stable, growing | Technology trend | Migration pattern |

### Technology Migration Trends (2019-2024)

| Technology | 2019 Share | 2024 Share | Trend | Significance |
|------------|-----------|------------|-------|--------------|
| **2G** | 4.95% | ~1% | Declining | Legacy phase-out |
| **3G** | 26.49% | ~5% | Declining | Legacy phase-out |
| **4G** | 60.15% | ~30% | Stable | Mature technology |
| **5G** | 0.35% | ~60% | Growing | **Technology migration ⭐** |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Limitations:**
- ⚠️ **Subscriber forecasting**, NOT maintenance demand forecasting
- ⚠️ Subscriber migration ≠ spare parts demand
- ⚠️ Technology migration ≠ equipment failure

**Potential Use:**
- Technology migration planning (2G → 4G → 5G)
- Operator-specific tracking (B2B contracts validation)
- **NOT for primary model training**

**Adaptation Strategy:**
```python
# Subscriber Migration → Equipment Migration (Indirect)
# 5G migration (0.35% → 60%) → New 5G equipment demand
# 2G/3G phase-out → Legacy equipment replacement demand
# But this is INDIRECT and NOT the primary use case
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/subscriber_forecasting/subscriber_forecasting_detailed.csv` (CSV format, 1,154+ rows)

**Processed Data:**
- `data/processed/subscriber_forecasting_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Low relevance - Subscriber forecasting, not maintenance demand forecasting

**Recommendation:** Use only for technology migration context (5G expansion → equipment demand). **NOT for primary model training** (use maintenance/spare parts datasets instead).

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

