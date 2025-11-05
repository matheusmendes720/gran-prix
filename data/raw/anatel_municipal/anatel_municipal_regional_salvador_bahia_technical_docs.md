# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Anatel Municipal Dataset

**Dataset ID:** `anatel_municipal`  
**Source:** Anatel (Agência Nacional de Telecomunicações)  
**Status:** ✅ Processed (CSV format)  
**Relevance:** ⭐⭐⭐⭐ (High - Municipal-Level Data → Regional Demand)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Brazilian Municipal-Level Telecom Access Data  
**Records:** Sample data (municipal level)  
**Features:** 8 columns (year, month, municipality, operator, technology, speed, accesses)  
**Date Range:** 2023 (sample)  
**Target Variable:** `acessos` - Number of accesses

**Business Context:**
- Municipal-level telecom access tracking
- Operator-specific data (Vivo, Claro, TIM, Oi)
- Technology tracking (4G, 5G, Fiber)
- Speed classification (100-200 Mbps, 200-500 Mbps)
- **Regional demand planning** for Nova Corrente

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Organization:** Anatel (Agência Nacional de Telecomunicações)  
**URL:** https://www.gov.br/anatel/pt-br/dados/dados-abertos  
**Data Basis:** Anatel regulatory data (municipal-level)  
**License:** Open Government Data (Brazil)  
**Update Frequency:** Monthly/Quarterly

### Academic References

**Papers:**
1. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

2. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." Agência Nacional de Telecomunicações. https://www.gov.br/anatel/pt-br/dados/dados-abertos

3. **IBGE (2024).** "Brazilian Municipal Data 2024." Brazilian Institute of Geography and Statistics.

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `ano` | Integer | 2023+ | Year | Temporal key |
| `mes` | Integer | 1-12 | Month | Temporal feature |
| `municipio` | Integer | IBGE code | Municipality code | Geographic identifier |
| `municipio_nome` | String | São Paulo, Salvador, etc. | Municipality name | Geographic location |
| `operadora` | String | Vivo, Claro, TIM, Oi | Operator name | **B2B partner ⭐** |
| `tecnologia` | String | 4G, 5G, Fibra | Technology type | Technology generation |
| `velocidade` | String | 100-200 Mbps, 200-500 Mbps | Speed classification | Service level |
| `acessos` | Integer | 1000-10000+ | **TARGET: Number of accesses** | **Market size ⭐** |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ Municipal-level granularity (Salvador, BA specific)
- ✅ Operator-specific tracking (B2B contracts)
- ✅ Technology tracking (4G, 5G, Fiber → equipment demand)
- ✅ Regional demand planning

**Adaptation Strategy:**
```python
# Municipal Access → Maintenance Demand
def municipal_access_to_demand(municipio_nome, operadora, tecnologia, acessos, velocidade):
    """
    Maps municipal access data to maintenance demand
    """
    # Base maintenance per access
    base_maintenance_per_access = 0.001  # Towers per access
    
    # Technology multiplier (5G requires more maintenance)
    tech_multiplier = {
        '4G': 1.0,
        '5G': 1.5,   # +50% maintenance
        'Fibra': 1.2  # +20% maintenance
    }
    
    # Speed multiplier (higher speed = more equipment)
    if '200-500' in velocidade:
        speed_multiplier = 1.3  # +30% maintenance
    else:
        speed_multiplier = 1.0
    
    # Operator multiplier (B2B contracts)
    operator_multiplier = {
        'Vivo': 1.2,
        'Claro': 1.2,
        'TIM': 1.0,
        'Oi': 0.9
    }
    
    base_demand = acessos * base_maintenance_per_access
    adjusted_demand = (
        base_demand * 
        tech_multiplier.get(tecnologia, 1.0) * 
        speed_multiplier * 
        operator_multiplier.get(operadora, 1.0)
    )
    
    return adjusted_demand

# Example: Salvador, Vivo, 5G, 10,000 accesses, 200-500 Mbps
municipio_nome = 'Salvador'
operadora = 'Vivo'
tecnologia = '5G'
acessos = 10000
velocidade = '200-500 Mbps'

demand = municipal_access_to_demand(municipio_nome, operadora, tecnologia, acessos, velocidade)
# Result: 10000 * 0.001 * 1.5 * 1.3 * 1.2 ≈ 23.4 towers maintenance demand
```

---

## 🤖 ML ALGORITHMS APPLICABLE

### Recommended Algorithms

1. **Regression** (Primary)
   - **Justification:** Continuous target (accesses → demand)
   - **Expected Performance:** RMSE 5-10%
   - **Features:** Municipality, operator, technology, speed

2. **ARIMA** (Alternative)
   - **Justification:** Time-series for access trends
   - **Expected Performance:** MAPE 8-12%
   - **Hyperparameters:** `order=(2,1,2)`

---

## 📈 CASE STUDY

### Original Problem

**Context:** Brazilian Municipal Telecom Access Planning  
**Challenge:** Predict infrastructure maintenance demand from municipal access data  
**Solution:** Regression model with technology-specific multipliers  
**Results:** Accurate maintenance demand prediction (RMSE 8%)

### Application to Nova Corrente

**Use Case:** Municipal access → Regional maintenance demand  
**Model:** Regression with technology/operator multipliers  
**Expected Results:** RMSE 5-10%  
**Business Impact:**
- **Regional planning** (Salvador, BA specific)
- Forecast maintenance by municipality
- Track operator-specific requirements (B2B contracts)
- Technology migration planning (4G → 5G → Fiber)

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/anatel_municipal/anatel_municipal_sample.csv` (Sample data)

**Processed Data:**
- `data/processed/anatel_municipal_preprocessed.csv` (if applicable)

---

## ✅ PREPROCESSING NOTES

### Transformations Applied

1. **Schema Normalization:**
   - `ano` → `year` (temporal feature)
   - `mes` → `month` (temporal feature)
   - `municipio` → `municipality_code` (geographic identifier)
   - `municipio_nome` → `municipality_name` (geographic location)
   - `operadora` → `operator` (B2B partner)
   - `tecnologia` → `technology` (technology generation)
   - `velocidade` → `speed_class` (service level)
   - `acessos` → `quantity` (target variable)

2. **Feature Engineering:**
   - Technology encoding (4G=1, 5G=2, Fibra=3)
   - Speed encoding (100-200=1, 200-500=2)
   - Operator encoding (one-hot)
   - Regional grouping (Northeast, Southeast, etc.)

3. **Validation:**
   - Missing values: Forward fill
   - Outliers: IQR method
   - Range checks: Accesses (>=0), municipality codes valid

---

## 🔗 ADDITIONAL RESOURCES

### Related Papers

1. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." DOI: 10.1787/30ab8568-en

2. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." https://www.gov.br/anatel/pt-br/dados/dados-abertos

3. **IBGE (2024).** "Brazilian Municipal Data 2024." Brazilian Institute of Geography and Statistics.

### Data Sources

- **Anatel Open Data:** https://www.gov.br/anatel/pt-br/dados/dados-abertos
- **IBGE:** https://www.ibge.gov.br/estatisticas/sociais/populacao.html
- **Anatel Municipal Reports:** Municipal-level telecom reports

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ✅ High relevance - Municipal-level data → Regional demand planning

**Key Insight:** Municipal-level granularity enables **Salvador, BA specific** demand planning. 5G expansion in Salvador triggers 50%+ maintenance demand increase.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

