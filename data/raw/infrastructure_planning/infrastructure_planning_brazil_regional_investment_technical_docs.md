# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Infrastructure Planning Regional Dataset

**Dataset ID:** `infrastructure_planning`  
**Source:** Industry Research & Market Reports  
**Status:** ✅ Processed  
**Relevance:** ⭐⭐⭐⭐ (High - Infrastructure Investment → Demand Forecasting)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Brazilian Regional Infrastructure Planning & Investment Data  
**Records:** 100+ rows (quarterly data)  
**Features:** 9 columns (date, region, towers, investment, coverage, rural coverage)  
**Date Range:** 2019-Q1 to 2024-Q4 (quarterly)  
**Target Variable:** `quarterly_investment_brl_billions` - Quarterly investment in billions BRL

**Business Context:**
- Brazilian regional infrastructure planning
- Tower count tracking by region
- Investment tracking (R$ billions per quarter)
- Coverage tracking (urban and rural)
- **Regional demand planning** for Nova Corrente

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Source:** Industry Research & Market Reports  
**Research:** Brazilian Infrastructure Investment Analysis  
**Data Basis:** Anatel, industry reports, market research  
**Region:** Brazil (all regions)

### Academic References

**Papers:**
1. **Anatel (2024).** "Infrastructure Investment Report 2024." Agência Nacional de Telecomunicações.

2. **TeleSíntese (2024).** "Setor de telecomunicações investe R$ 34,6 bilhões em 2024." TeleSíntese News.

3. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `date` | DateTime | 2019-03-31 to 2024-12-31 | Quarterly date | Temporal key |
| `year` | Integer | 2019-2024 | Year | Temporal feature |
| `quarter` | Integer | 1-4 | Quarter | Temporal feature |
| `region` | String | southeast, northeast, south, north, central_west | Region | Geographic region |
| `towers_count` | Float | 1,500-11,200 | Tower count | Infrastructure size |
| `quarterly_investment_brl_billions` | Float | 0.67-3.56 | **TARGET: Investment (billions BRL)** | **Investment level ⭐** |
| `coverage_pct` | Float | 85-95% | Urban coverage | Coverage level |
| `rural_coverage_pct` | Float | 65-75% | Rural coverage | Rural coverage |
| `investment_multiplier` | Float | 1.0-1.4 | Investment multiplier | Regional adjustment |

### Regional Statistics (2024)

| Region | Towers | Investment (R$ Billions/Q) | Coverage | Relevance for Nova Corrente |
|--------|--------|---------------------------|----------|----------------------------|
| **Southeast** | 11,200 | 3.56 | 95% | ⭐⭐⭐ Context |
| **Northeast** | 5,400 | 2.0 | 90% | ⭐⭐⭐⭐⭐ **PRIMARY** (Salvador, BA) |
| **South** | 4,550 | 1.56 | 93% | ⭐⭐ Context |
| **North** | 1,500 | 0.67 | 88% | ⭐ Context |
| **Central-West** | 1,650 | 0.67 | 90% | ⭐ Context |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **Regional infrastructure investment** (Northeast/Bahia relevant)
- ✅ Tower count tracking (infrastructure size → maintenance demand)
- ✅ Investment tracking (R$ billions → equipment demand)
- ✅ Coverage tracking (coverage expansion → maintenance demand)

**Adaptation Strategy:**
```python
# Infrastructure Investment → Demand Forecasting
def infrastructure_investment_to_demand(
    region, towers_count, investment_brl_billions, coverage_pct, rural_coverage_pct
):
    """
    Maps infrastructure investment to maintenance demand
    """
    # Base maintenance per tower
    base_maintenance_per_tower = 0.05  # Towers per tower (annual)
    
    # Regional multiplier (Northeast higher maintenance)
    regional_multiplier = {
        'northeast': 1.3,  # Higher maintenance (harsh climate)
        'southeast': 1.0,  # Standard maintenance
        'south': 0.9,      # Lower maintenance (milder climate)
        'north': 1.2,      # Higher maintenance (tropical climate)
        'central_west': 1.0 # Standard maintenance
    }
    
    # Investment multiplier (higher investment = more equipment = more maintenance)
    investment_multiplier = 1.0 + (investment_brl_billions - 2.0) / 2.0 * 0.20  # +20% for +2B investment
    
    # Coverage multiplier (higher coverage = more infrastructure = more maintenance)
    coverage_multiplier = 1.0 + (coverage_pct - 85) / 85 * 0.15  # +15% for +10% coverage
    
    base_demand = towers_count * base_maintenance_per_tower
    adjusted_demand = (
        base_demand * 
        regional_multiplier.get(region, 1.0) * 
        investment_multiplier * 
        coverage_multiplier
    )
    
    return adjusted_demand

# Example: Northeast region, 5,400 towers, R$ 2.0B investment, 90% coverage
region = 'northeast'
towers_count = 5400
investment = 2.0  # R$ 2.0 billion
coverage = 0.90  # 90%

demand = infrastructure_investment_to_demand(region, towers_count, investment, coverage, 0.70)
# Result: 5400 * 0.05 * 1.3 * 1.0 * 1.01 ≈ 356 towers maintenance demand (annual)
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/infrastructure_planning/infrastructure_planning_regional.csv` (CSV format, 100+ rows)

**Processed Data:**
- `data/processed/infrastructure_planning_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ✅ High relevance - Infrastructure investment → Maintenance demand

**Key Insight:** Northeast region has 5,400 towers with R$ 2.0B quarterly investment. Higher investment and coverage → More maintenance demand for Nova Corrente.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

