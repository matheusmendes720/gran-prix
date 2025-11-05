# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Anatel Mobile Brazil Dataset

**Dataset ID:** `anatel_mobile_brazil`  
**Source:** Anatel (via Data Basis)  
**Status:** ⏳ Pending Parsing (HTML/JSON Format)  
**Relevance:** ⭐⭐⭐⭐ (High - Brazilian Mobile Subscribers → B2B Demand)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Brazilian Mobile Phone Subscriber Data  
**Format:** HTML/JSON (requires parsing)  
**Files:** d3c86a88-d9a4-4c0-bdec-08ab61e8f63c  
**Status:** ⏳ Requires HTML/JSON → CSV conversion  
**Source:** Data Basis (data-basis.org)  
**Business Context:**
- Brazilian mobile phone subscriber tracking
- Operator-specific subscriber data
- Regional subscriber patterns
- **B2B contracts with operators → Stable demand for Nova Corrente**

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Organization:** Anatel (Agência Nacional de Telecomunicações)  
**Data Basis:** https://data-basis.org/search?organization=anatel  
**URL:** https://www.gov.br/anatel/pt-br/dados/dados-abertos  
**License:** Open Government Data (Brazil)  
**Update Frequency:** Monthly/Quarterly

### Academic References

**Papers:**
1. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

2. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." Agência Nacional de Telecomunicações. https://www.gov.br/anatel/pt-br/dados/dados-abertos

3. **Data Basis:** https://data-basis.org/search?organization=anatel

---

## 📊 DATA STRUCTURE

### Expected Columns (After Parsing)

| Column | Type | Description | Business Context |
|--------|------|-------------|------------------|
| `date` | DateTime | Monthly date | Temporal key |
| `region` | String | Northeast, Southeast, etc. | Geographic region |
| `operator` | String | Vivo, Claro, TIM, Oi | **B2B partner ⭐** |
| `subscribers_millions` | Integer | Number of subscribers | Market size |
| `technology` | String | 2G, 3G, 4G, 5G | Technology generation |
| `coverage_pct` | Float | Coverage percentage | Infrastructure coverage |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **B2B contracts with operators** → Stable demand (CRITICAL!)
- ✅ Operator-specific subscriber tracking (Vivo, Claro, TIM)
- ✅ Regional subscriber patterns (Northeast/Bahia relevant)
- ✅ Technology migration (5G expansion → Equipment demand)

**Adaptation Strategy:**
```python
# Mobile Subscribers → B2B Demand
def mobile_subscribers_to_demand(subscribers_millions, operator, technology, region):
    """
    Maps mobile subscribers to B2B maintenance demand
    """
    # Base maintenance per million subscribers (B2B contracts)
    base_maintenance_per_million = 0.05  # Towers per million subscribers
    
    # Operator multiplier (B2B contract intensity)
    operator_multiplier = {
        'Vivo': 1.3,    # Strong B2B contracts (market leader)
        'Claro': 1.2,   # Strong B2B contracts
        'TIM': 1.0,     # Moderate B2B contracts
        'Oi': 0.8       # Weak B2B contracts
    }
    
    # Technology multiplier (5G requires more maintenance)
    tech_multiplier = {
        '5G': 1.8,   # +80% maintenance (new technology)
        '4G': 1.3,   # +30% maintenance (mature technology)
        '3G': 1.0,   # Standard maintenance
        '2G': 0.7    # -30% maintenance (legacy)
    }
    
    base_demand = subscribers_millions * base_maintenance_per_million
    adjusted_demand = (
        base_demand * 
        operator_multiplier.get(operator, 1.0) * 
        tech_multiplier.get(technology, 1.0)
    )
    
    return adjusted_demand

# Example: Vivo, 5G, 85M subscribers, Northeast
operator = 'Vivo'
technology = '5G'
subscribers = 85.0  # 85 million
region = 'northeast'

demand = mobile_subscribers_to_demand(subscribers, operator, technology, region)
# Result: 85 * 0.05 * 1.3 * 1.8 ≈ 10 towers maintenance demand (annual)
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/anatel_mobile_brazil/d3c86a88-d9a4-4c0-bdec-08ab61e8f63c` (HTML/JSON, requires parsing)

---

## ✅ PREPROCESSING NOTES

### Pending Tasks

1. **HTML/JSON Parsing:**
   - Parse `d3c86a88-d9a4-4c0-bdec-08ab61e8f63c` → CSV
   - Extract table/data structure (date, region, operator, subscribers)
   - Clean HTML/JSON formatting

2. **Schema Normalization:**
   - `date` → datetime format
   - `subscribers_millions` → integer
   - `region` → standardized region names
   - `operator` → standardized operator names
   - `technology` → standardized technology types

3. **Validation:**
   - Missing values: Forward fill
   - Outliers: IQR method
   - Range checks: Subscribers (>=0), coverage (0-1)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⏳ Pending - Requires HTML/JSON parsing

**Key Insight:** **B2B contracts with operators (Vivo, Claro, TIM) = Stable demand for Nova Corrente.** Mobile subscribers (85M Vivo) → Maintenance demand (10+ towers annual for 5G).

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

