# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## OECD Brazil Regulatory Indicators Dataset

**Dataset ID:** `oecd_indicators`  
**Source:** OECD (Organisation for Economic Co-operation and Development)  
**Status:** ✅ Processed  
**Relevance:** ⭐⭐⭐ (Medium - Regulatory Context, Not Primary Training)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** OECD Regulatory & Competition Indicators for Brazil  
**Records:** 26+ rows (quarterly data)  
**Features:** 9 columns (date, competition, investment, regulatory quality, spectrum, tax, market concentration)  
**Date Range:** 2019-Q1 to 2024-Q4 (quarterly)  
**Target Variable:** `competition_index` - Competition index (0-1)

**Business Context:**
- OECD standardized regulatory indicators
- Competition index (market competitiveness)
- Infrastructure investment tracking (% of GDP)
- Regulatory quality score (0-1)
- Spectrum efficiency (0-1)
- Tax burden tracking (% of revenue)
- Market concentration (HHI - Herfindahl-Hirschman Index)

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Organization:** OECD (Organisation for Economic Co-operation and Development)  
**URL:** https://www.oecd.org/brazil/  
**Data Basis:** OECD regulatory reviews  
**Country:** Brazil  
**Update Frequency:** Quarterly/Annual

### Academic References

**Papers:**
1. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

2. **OECD (2024).** "Digital Economy Outlook 2024." OECD Publishing.

3. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." Agência Nacional de Telecomunicações.

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `date` | DateTime | 2019-03-31 to 2024-12-31 | Quarterly date | Temporal key |
| `year` | Integer | 2019-2024 | Year | Temporal feature |
| `quarter` | Integer | 1-4 | Quarter | Temporal feature |
| `competition_index` | Float | 0.7-0.85 | **TARGET: Competition index** | **Market competitiveness ⭐** |
| `infrastructure_investment_pct_gdp` | Float | 0.025-0.035 | Investment % of GDP | Investment level |
| `regulatory_quality` | Float | 0.65-0.85 | Regulatory quality (0-1) | Regulatory environment |
| `spectrum_efficiency` | Float | 0.75-0.90 | Spectrum efficiency (0-1) | Resource utilization |
| `tax_burden_pct` | Float | 0.38-0.42 | Tax burden % | Cost factor |
| `market_concentration_hhi` | Integer | 2400-2800 | HHI (0-10000) | Market concentration |
| `country` | String | brazil | Country identifier | Geographic identifier |

### Regulatory Trends (2019-2024)

| Indicator | 2019 | 2024 | Change | Significance |
|-----------|------|------|--------|--------------|
| **Competition Index** | 0.70 | 0.85 | +21% | Increased competition |
| **Investment % GDP** | 2.5% | 3.3% | +32% | Infrastructure investment |
| **Regulatory Quality** | 0.65 | 0.85 | +31% | Improved regulation |
| **Spectrum Efficiency** | 0.75 | 0.90 | +20% | Better resource use |
| **Tax Burden** | 42% | 38% | -10% | Reduced taxes |
| **Market Concentration** | 2800 | 2400 | -14% | Less concentrated |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **Regulatory context** (competition, investment, quality)
- ✅ Infrastructure investment tracking (relevant for demand forecasting)
- ✅ Market concentration (operator market dynamics)
- ✅ Tax burden (affects import costs)

**Limitations:**
- ⚠️ **Reference indicators only** (not for primary model training)
- ⚠️ Quarterly granularity (not daily/hourly)
- ⚠️ Aggregated national data (not regional/operational detail)

**Adaptation Strategy:**
```python
# OECD Regulatory → Nova Corrente (Regulatory Context)
def regulatory_factors_to_demand(competition_index, investment_pct_gdp, regulatory_quality):
    """
    Maps regulatory factors to demand adjustment
    """
    # Infrastructure investment impact (higher investment = more demand)
    investment_multiplier = 1.0 + (investment_pct_gdp - 0.025) / 0.025 * 0.15  # +15% for +1% GDP
    
    # Regulatory quality impact (better regulation = more investment = more demand)
    quality_multiplier = 1.0 + (regulatory_quality - 0.65) / 0.65 * 0.10  # +10% for +0.2 quality
    
    # Competition impact (higher competition = more operators = more demand)
    competition_multiplier = 1.0 + (competition_index - 0.7) / 0.7 * 0.20  # +20% for +0.15 index
    
    total_multiplier = investment_multiplier * quality_multiplier * competition_multiplier
    
    return total_multiplier
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/oecd_indicators/oecd_brazil_regulatory.csv` (CSV format, 26+ rows)

**Processed Data:**
- `data/processed/oecd_indicators_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Medium relevance - Regulatory context and reference indicators only

**Key Insight:** Regulatory factors (competition, investment, quality) impact infrastructure demand. Higher competition (+21%) and investment (+32%) → More infrastructure demand for Nova Corrente.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

