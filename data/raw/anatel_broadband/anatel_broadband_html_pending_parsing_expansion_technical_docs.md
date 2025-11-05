# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Anatel Broadband Dataset

**Dataset ID:** `anatel_broadband`  
**Source:** Anatel (Agência Nacional de Telecomunicações)  
**Status:** ⏳ Pending Parsing (HTML Format)  
**Relevance:** ⭐⭐⭐⭐ (High - Broadband Expansion → Maintenance Demand)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Brazilian Broadband Access Data  
**Format:** HTML (requires parsing)  
**Files:** broadband_accesses.html, search  
**Status:** ⏳ Requires HTML → CSV conversion  
**Business Context:**
- Brazilian broadband access tracking
- Fiber expansion data
- Regional broadband coverage
- **Broadband expansion → Tower maintenance demand**

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Organization:** Anatel (Agência Nacional de Telecomunicações)  
**URL:** https://www.gov.br/anatel/pt-br/dados/dados-abertos  
**Data Basis:** Anatel regulatory data (broadband accesses)  
**License:** Open Government Data (Brazil)  
**Update Frequency:** Monthly/Quarterly

### Academic References

**Papers:**
1. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

2. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." Agência Nacional de Telecomunicações. https://www.gov.br/anatel/pt-br/dados/dados-abertos

3. **ITU (2023).** "Big Data for Development: Brazil Country Report." International Telecommunication Union.

---

## 📊 DATA STRUCTURE

### Expected Columns (After Parsing)

| Column | Type | Description | Business Context |
|--------|------|-------------|------------------|
| `date` | DateTime | Monthly date | Temporal key |
| `region` | String | Northeast, Southeast, etc. | Geographic region |
| `operator` | String | Vivo, Claro, TIM, Oi | Operator name |
| `technology` | String | Fiber, DSL, Cable | Technology type |
| `accesses` | Integer | Number of accesses | Market size |
| `speed_category` | String | 100-200 Mbps, 200-500 Mbps | Speed classification |
| `coverage_pct` | Float | Coverage percentage | Infrastructure coverage |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **Broadband expansion** → Tower maintenance demand
- ✅ Regional coverage tracking (Northeast/Bahia relevant)
- ✅ Technology migration (DSL → Fiber)
- ✅ Operator-specific tracking (B2B contracts)

**Adaptation Strategy:**
```python
# Broadband Expansion → Maintenance Demand
def broadband_expansion_to_demand(accesses, technology, operator, region):
    """
    Maps broadband expansion to maintenance demand
    """
    # Base maintenance per access
    base_maintenance_per_access = 0.001  # Towers per access
    
    # Technology multiplier (Fiber requires more maintenance)
    tech_multiplier = {
        'Fiber': 1.5,   # +50% maintenance
        'DSL': 1.0,     # Standard maintenance
        'Cable': 1.2    # +20% maintenance
    }
    
    # Operator multiplier (B2B contracts)
    operator_multiplier = {
        'Vivo': 1.2,
        'Claro': 1.2,
        'TIM': 1.0,
        'Oi': 0.9
    }
    
    base_demand = accesses * base_maintenance_per_access
    adjusted_demand = (
        base_demand * 
        tech_multiplier.get(technology, 1.0) * 
        operator_multiplier.get(operator, 1.0)
    )
    
    return adjusted_demand
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/anatel_broadband/broadband_accesses.html` (HTML, requires parsing)
- `data/raw/anatel_broadband/search` (Search interface)

---

## ✅ PREPROCESSING NOTES

### Pending Tasks

1. **HTML Parsing:**
   - Parse `broadband_accesses.html` → CSV
   - Extract table data (date, region, operator, technology, accesses)
   - Clean HTML tags and formatting

2. **Schema Normalization:**
   - `date` → datetime format
   - `accesses` → integer
   - `region` → standardized region names
   - `operator` → standardized operator names
   - `technology` → standardized technology types

3. **Validation:**
   - Missing values: Forward fill
   - Outliers: IQR method
   - Range checks: Accesses (>=0), coverage (0-1)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⏳ Pending - Requires HTML parsing

**Key Insight:** Broadband expansion (Fiber migration) → Tower maintenance demand. Northeast region has high growth (+100% penetration) → Higher maintenance demand for Nova Corrente.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

