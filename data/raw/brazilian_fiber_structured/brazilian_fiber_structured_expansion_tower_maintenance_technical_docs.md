# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Brazilian Fiber Expansion Structured Dataset

**Dataset ID:** `brazilian_fiber_structured`  
**Source:** Industry Research & Market Reports  
**Status:** ✅ Processed & Ready for ML  
**Relevance:** ⭐⭐⭐⭐ (High - Fiber Expansion → Tower Maintenance)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Brazilian Fiber Optic Network Expansion Analysis  
**Records:** 100+ rows (quarterly data)  
**Features:** 7 columns (date, region, penetration, households, growth)  
**Date Range:** 2020-Q1 to 2024-Q4 (quarterly)  
**Target Variable:** `estimated_households_millions` - Connected households in millions

**Business Context:**
- Brazilian fiber optic network expansion tracking
- Regional penetration analysis (Southeast, South, Northeast, North, Central-West)
- Household penetration percentage (25% in 2020 → 49% in 2024)
- Fiber expansion → Tower maintenance increase

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Source:** Industry Research & Market Reports  
**Research:** Brazilian Fiber Optic Network Expansion  
**Data Basis:** Anatel, industry reports, market research  
**Region:** Brazil (all regions)

### Academic References

**Papers:**
1. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." Agência Nacional de Telecomunicações. https://www.gov.br/anatel/pt-br/dados/dados-abertos

2. **ITU (2023).** "Big Data for Development: Brazil Country Report." International Telecommunication Union.

3. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `date` | DateTime | 2020-03-31 to 2024-12-31 | Quarterly date | Temporal key |
| `year` | Integer | 2020-2024 | Year | Temporal feature |
| `quarter` | Integer | 1-4 | Quarter | Temporal feature |
| `region` | String | southeast, south, northeast, north, central_west | Region | Geographic region |
| `household_penetration` | Float | 0.125-0.49 | **TARGET: Household penetration** | **Penetration rate ⭐** |
| `estimated_households_millions` | Float | 4.38-29.57 | Connected households (millions) | Market size |
| `growth_rate` | Float | 0.15 (15%) | Quarterly growth rate | Growth metric |

### Penetration Statistics by Region

| Region | 2020 Penetration | 2024 Penetration | Growth | Households (2024) |
|--------|-----------------|------------------|--------|-------------------|
| **Southeast** | 32.5% | 49% | +51% | 29.57M |
| **South** | 30% | 47% | +57% | 25.2M |
| **Northeast** | 17.5% | 35% | +100% | 8.57M |
| **North** | 12.5% | 28% | +124% | 4.38M |
| **Central-West** | 22.5% | 42% | +87% | 14.18M |
| **Brazil (Avg)** | 25% | 49% | +96% | 82.9M |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ Brazilian regional data (Northeast/Bahia relevant)
- ✅ Fiber expansion → Tower maintenance increase
- ✅ Regional penetration tracking (predictive factor)
- ✅ Quarterly granularity (good for forecasting)

**Adaptation Strategy:**
```python
# Fiber Expansion → Tower Maintenance Demand
def fiber_expansion_to_demand(households_millions, penetration, region):
    """
    Maps fiber expansion to tower maintenance demand
    """
    # Base maintenance demand per million households
    base_demand_per_million = 0.8  # Towers per million households
    
    # Regional adjustment (Northeast/Bahia specific)
    regional_multiplier = {
        'northeast': 1.3,  # Higher maintenance (harsh climate, rural areas)
        'southeast': 1.0,  # Standard maintenance
        'south': 0.9,      # Lower maintenance (milder climate)
        'north': 1.2,      # Higher maintenance (tropical climate)
        'central_west': 1.0 # Standard maintenance
    }
    
    # Penetration adjustment (higher penetration = more maintenance)
    penetration_multiplier = 1.0 + (penetration - 0.25) * 0.5  # +50% for 100% penetration
    
    base_demand = households_millions * base_demand_per_million
    adjusted_demand = base_demand * regional_multiplier.get(region, 1.0) * penetration_multiplier
    
    return adjusted_demand

# Example: Northeast region, 35% penetration, 8.57M households
households = 8.57  # Million households
penetration = 0.35  # 35%
region = 'northeast'

demand = fiber_expansion_to_demand(households, penetration, region)
# Result: 8.57 * 0.8 * 1.3 * 1.05 ≈ 9.4 towers maintenance demand
```

---

## 🤖 ML ALGORITHMS APPLICABLE

### Recommended Algorithms

1. **Prophet** (Primary)
   - **Justification:** Quarterly seasonality, external factors
   - **Expected Performance:** MAPE 6-10%
   - **Hyperparameters:** `yearly_seasonality=True, quarterly_seasonality=True`

2. **ARIMA** (Alternative)
   - **Justification:** Time-series forecasting
   - **Expected Performance:** MAPE 8-12%
   - **Hyperparameters:** `order=(2,1,2), seasonal_order=(1,1,1,4)`

3. **Linear Regression** (Baseline)
   - **Justification:** Growth trend modeling
   - **Expected Performance:** MAPE 10-15%
   - **Features:** Year, quarter, region, penetration, growth_rate

---

## 📈 CASE STUDY

### Original Problem

**Context:** Brazilian Fiber Optic Network Expansion Planning  
**Challenge:** Predict fiber penetration growth for infrastructure planning  
**Solution:** Time-series forecasting with regional trends  
**Results:** Accurate penetration predictions (96% growth 2020-2024)

### Application to Nova Corrente

**Use Case:** Fiber expansion → Tower maintenance demand  
**Model:** Prophet with regional regressors  
**Expected Results:** MAPE 6-10% for penetration prediction  
**Business Impact:**
- Forecast tower maintenance needs
- Plan for fiber expansion (Northeast growing fastest)
- Optimize resource allocation by region

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/brazilian_fiber_structured/brazilian_fiber_expansion_structured.csv` (~8 KB, 100+ rows)

**Processed Data:**
- `data/processed/brazilian_fiber_structured_preprocessed.csv` (if applicable)

---

## ✅ PREPROCESSING NOTES

### Transformations Applied

1. **Schema Normalization:**
   - `date` → `date` (datetime format)
   - `estimated_households_millions` → `quantity` (target variable)
   - `region` → `region` (preserved)
   - `household_penetration` → `penetration_rate` (feature)

2. **Feature Engineering:**
   - Year/quarter extraction
   - Growth rate calculation
   - Regional encoding (one-hot)
   - Penetration categories (Low: <30%, Medium: 30-40%, High: >40%)

3. **Validation:**
   - Missing values: Forward fill
   - Outliers: IQR method
   - Range checks: Penetration (0-1), households (>0)

---

## 🔗 ADDITIONAL RESOURCES

### Related Papers

1. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." https://www.gov.br/anatel/pt-br/dados/dados-abertos

2. **ITU (2023).** "Big Data for Development: Brazil Country Report." International Telecommunication Union.

3. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." DOI: 10.1787/30ab8568-en

### Market Reports

- Anatel: Broadband Access Reports
- TeleSíntese: Fiber Expansion Analysis
- ABDI: Infrastructure Investment Reports

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ✅ High relevance - Brazilian fiber expansion → Tower maintenance

**Key Insight:** Northeast region has highest growth (+100% penetration) → Higher maintenance demand for Nova Corrente (Bahia, Salvador)

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

