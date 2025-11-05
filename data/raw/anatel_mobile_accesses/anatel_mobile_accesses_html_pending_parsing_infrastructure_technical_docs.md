# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Anatel Mobile Accesses Dataset

**Dataset ID:** `anatel_mobile_accesses`  
**Source:** Anatel (Agência Nacional de Telecomunicações)  
**Status:** ⏳ Pending Parsing (HTML Format)  
**Relevance:** ⭐⭐⭐⭐ (High - Mobile Infrastructure → Maintenance Demand)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Brazilian Mobile Phone Access Data  
**Format:** HTML (requires parsing)  
**Files:** mobile_accesses.html  
**Status:** ⏳ Requires HTML → CSV conversion  
**Business Context:**
- Brazilian mobile phone access tracking
- Mobile infrastructure coverage
- Regional mobile access patterns
- **Mobile infrastructure → Tower maintenance demand**

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Organization:** Anatel (Agência Nacional de Telecomunicações)  
**URL:** https://www.gov.br/anatel/pt-br/dados/dados-abertos  
**Data Basis:** Anatel regulatory data (mobile accesses)  
**License:** Open Government Data (Brazil)  
**Update Frequency:** Monthly/Quarterly

### Academic References

**Papers:**
1. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

2. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." Agência Nacional de Telecomunicações. https://www.gov.br/anatel/pt-br/dados/dados-abertos

---

## 📊 DATA STRUCTURE

### Expected Columns (After Parsing)

| Column | Type | Description | Business Context |
|--------|------|-------------|------------------|
| `date` | DateTime | Monthly date | Temporal key |
| `region` | String | Northeast, Southeast, etc. | Geographic region |
| `operator` | String | Vivo, Claro, TIM, Oi | Operator name |
| `technology` | String | 2G, 3G, 4G, 5G | Technology generation |
| `accesses` | Integer | Number of accesses | Market size |
| `coverage_pct` | Float | Coverage percentage | Infrastructure coverage |
| `penetration_pct` | Float | Penetration percentage | Market maturity |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **Mobile infrastructure** → Tower maintenance demand
- ✅ Technology migration (2G → 3G → 4G → 5G)
- ✅ Regional coverage tracking (Northeast/Bahia relevant)
- ✅ Operator-specific tracking (B2B contracts)

**Adaptation Strategy:**
```python
# Mobile Accesses → Maintenance Demand
def mobile_accesses_to_demand(accesses, technology, operator, region):
    """
    Maps mobile accesses to maintenance demand
    """
    # Base maintenance per access
    base_maintenance_per_access = 0.0005  # Towers per access
    
    # Technology multiplier (5G requires more maintenance)
    tech_multiplier = {
        '5G': 2.0,   # +100% maintenance (new technology)
        '4G': 1.5,   # +50% maintenance (mature technology)
        '3G': 1.0,   # Standard maintenance
        '2G': 0.8    # -20% maintenance (legacy)
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
- `data/raw/anatel_mobile_accesses/mobile_accesses.html` (HTML, requires parsing)

---

## ✅ PREPROCESSING NOTES

### Pending Tasks

1. **HTML Parsing:**
   - Parse `mobile_accesses.html` → CSV
   - Extract table data (date, region, operator, technology, accesses)
   - Clean HTML tags and formatting

2. **Schema Normalization:**
   - `date` → datetime format
   - `accesses` → integer
   - `region` → standardized region names
   - `operator` → standardized operator names
   - `technology` → standardized technology types (2G, 3G, 4G, 5G)

3. **Validation:**
   - Missing values: Forward fill
   - Outliers: IQR method
   - Range checks: Accesses (>=0), coverage (0-1), penetration (0-1)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⏳ Pending - Requires HTML parsing

**Key Insight:** Mobile infrastructure (5G expansion) → Tower maintenance demand. 5G requires 100% more maintenance than 4G (new technology, more complex equipment).

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

