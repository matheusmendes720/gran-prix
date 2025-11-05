# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Kaggle Supply Chain Dataset

**Dataset ID:** `kaggle_supply_chain`  
**Source:** Kaggle  
**Status:** ✅ Processed (if applicable)  
**Relevance:** ⭐⭐⭐ (Medium - Generic Supply Chain, Some Relevance)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Generic Supply Chain Operations Data  
**Records:** 91,000+ rows  
**Features:** 15 columns (date, SKU, warehouse, supplier, region, inventory, lead time, reorder point, etc.)  
**Date Range:** 2024-01-01+ (daily data)  
**Target Variable:** `Demand_Forecast` - Demand forecast

**Business Context:**
- Generic supply chain operations
- Multi-warehouse inventory management
- Supplier lead time tracking
- Reorder point calculation
- Stockout prediction

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Platform:** Kaggle  
**Dataset ID:** Supply chain dataset  
**URL:** https://www.kaggle.com/datasets/supply-chain  
**License:** Open Database License (ODbL)

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Description | Business Context |
|--------|------|-------------|------------------|
| `Date` | DateTime | Daily date | Temporal key |
| `SKU_ID` | String | Product SKU | Item identifier |
| `Warehouse_ID` | String | Warehouse identifier | Location |
| `Supplier_ID` | String | Supplier identifier | Supplier tracking |
| `Region` | String | North, South, East, West | Geographic region |
| `Units_Sold` | Integer | Daily sales | Demand |
| `Inventory_Level` | Integer | Current inventory | Stock level |
| `Supplier_Lead_Time_Days` | Integer | 1-30 | Lead time | **Critical for PP** |
| `Reorder_Point` | Integer | 50-500 | Current reorder point | **PP calculation** |
| `Order_Quantity` | Integer | 0-1000+ | Order quantity | Order size |
| `Unit_Cost` | Float | 10-100+ | Unit cost | Cost per unit |
| `Unit_Price` | Float | 20-200+ | Unit price | Price per unit |
| `Promotion_Flag` | Integer | 0, 1 | Promotion flag | Promotional factor |
| `Stockout_Flag` | Integer | 0, 1 | Stockout indicator | **Service level** |
| `Demand_Forecast` | Float | **TARGET** | Demand forecast | **ML forecast ⭐** |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ Lead time tracking (critical for Nova Corrente)
- ✅ Reorder point calculation (matches Nova Corrente needs)
- ✅ Stockout prediction (service level compliance)
- ✅ Large dataset (91K+ rows) - good for deep learning

**Limitations:**
- ⚠️ Generic supply chain (not telecom-specific)
- ⚠️ Promotional factors (not relevant for B2B)
- ⚠️ Multiple warehouses (Nova Corrente has centralized inventory)

**Adaptation Strategy:**
```python
# Supply Chain → Nova Corrente Adaptation
# Use only: Lead time, reorder point, stockout prediction
# Ignore: Promotions, multi-warehouse, generic categories
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/kaggle_supply_chain/supply_chain_dataset1.csv` (~6.4 MB, 91,000+ rows)

**Processed Data:**
- `data/processed/kaggle_supply_chain_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Medium relevance - Generic supply chain, some useful features (lead time, reorder point)

**Recommendation:** Use selectively - Lead time and reorder point features only. Not for primary model training.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

