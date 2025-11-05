# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Brazilian Operators Market (JSON Summary)

**Dataset ID:** `brazilian_operators`  
**Source:** Public Reports, Wikipedia, Reuters  
**Status:** ✅ JSON Summary (CSV structured version available)  
**Relevance:** ⭐⭐⭐⭐⭐ (ESSENTIAL - B2B Contracts → Stable Demand)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Brazilian Telecom Operator Market Share Summary  
**Format:** JSON (summary data)  
**CSV Version:** `data/raw/brazilian_operators_structured/brazilian_operators_market_structured.csv`  
**Date Range:** 2019-2024 (monthly data)  
**Business Context:**
- Brazilian telecom operator market share tracking
- Operator-specific subscriber data (Vivo, Claro, TIM, Oi)
- Revenue tracking (R$ billions)
- Revenue growth tracking
- **B2B contracts with operators = Stable demand for Nova Corrente**

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Source:** Public Reports, Wikipedia, Reuters  
**Research:** Brazilian Telecom Operator Market Share  
**Data Basis:** Public company reports, Wikipedia, Reuters, market research  
**Region:** Brazil

### Academic References

**Papers:**
1. **OECD (2020).** "OECD Telecommunication and Broadcasting Review of Brazil 2020." OECD Publishing. DOI: 10.1787/30ab8568-en

2. **Anatel (2024).** "Plano de Dados Abertos 2024-2027." Agência Nacional de Telecomunicações. https://www.gov.br/anatel/pt-br/dados/dados-abertos

---

## 📊 DATA STRUCTURE

### JSON Schema

```json
{
  "dataset_name": "Brazilian Telecom Operator Market Share",
  "mobile_subscribers_2023_q1": {
    "vivo": {
      "company": "Telefônica Brasil",
      "subscribers_millions": 98.0,
      "market_share": 0.32,
      "revenue_2024_brl_billions": 55.85,
      "revenue_growth": 0.0719
    },
    ...
  }
}
```

### Market Share Statistics (2023 Q1)

| Operator | Company | Subscribers (M) | Market Share | Revenue (R$ B) | Growth |
|----------|---------|-----------------|--------------|----------------|--------|
| **Vivo** | Telefônica Brasil | 98.0 | 32% | 55.85 | 7.19% |
| **Claro** | América Móvil | 82.8 | 27% | N/A | N/A |
| **TIM** | Telecom Italia | 61.7 | 20% | N/A | 5% |
| **Oi** | Oi (mobile sold) | 0 | 0% | N/A | N/A |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **B2B contracts with operators** → Stable demand (CRITICAL!)
- ✅ Operator-specific tracking (Vivo, Claro, TIM)
- ✅ Revenue tracking (operator health → contract stability)
- ✅ Market share tracking (demand redistribution)

**Adaptation Strategy:**
```python
# Operator Market Share → B2B Demand (Same as structured version)
# See: data/raw/brazilian_operators_structured/CONTEXT_TECHNICAL_DOCS.md
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/brazilian_operators/brazilian_operators_market.json` (JSON summary)

**Structured Data:**
- `data/raw/brazilian_operators_structured/brazilian_operators_market_structured.csv` (✅ Use this for ML)

---

## ✅ PREPROCESSING NOTES

### JSON → CSV Conversion

**Already Done:** Structured CSV version available at:
- `data/raw/brazilian_operators_structured/brazilian_operators_market_structured.csv`

**Use Structured Version:** The CSV version has proper schema normalization and is ready for ML training.

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ✅ Summary data - Use structured CSV version for ML

**Key Insight:** **B2B contracts with operators (Vivo, Claro, TIM) = Stable demand for Nova Corrente.** Use the **structured CSV version** for ML training.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

