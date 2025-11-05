# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Kaggle Cloud Supply Chain Dataset

**Dataset ID:** `kaggle_cloud_supply_chain`  
**Source:** Kaggle  
**Status:** ✅ Processed (if applicable)  
**Relevance:** ⭐⭐⭐ (Medium - Cloud/Logistics, Some Relevance)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Cloud Supply Chain Operations Data  
**Records:** 3,200+ rows  
**Features:** 15 columns (timestamp, product, category, warehouse, inventory, sales, price, lead time, restock, promotion, weather, delay, forecast)  
**Date Range:** 2024-01-01+ (sample data)  
**Target Variable:** `demand_forecast` - Demand forecast

**Business Context:**
- Cloud supply chain operations
- Multi-product inventory management
- Lead time tracking
- Weather integration (temperature, humidity)
- Delivery delay tracking

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Platform:** Kaggle  
**Dataset ID:** Cloud supply chain dataset  
**URL:** https://www.kaggle.com/datasets/cloud-supply-chain  
**License:** Open Database License (ODbL)

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Description | Business Context |
|--------|------|-------------|------------------|
| `timestamp` | DateTime | Timestamp | Temporal key |
| `product_id` | String | P001, P002, etc. | Product identifier |
| `product_category` | String | Apparel, Home Goods, Electronics, FMCG | Category |
| `warehouse_location` | String | WH01, WH02, etc. | Warehouse location |
| `inventory_level` | Integer | 100-500 | Current inventory | Stock level |
| `units_sold` | Integer | 20-50 | Daily sales | Demand |
| `unit_price` | Float | 100-500 | Unit price | Price |
| `lead_time_days` | Integer | 1-14 | **Lead time** | **Critical for PP ⭐** |
| `restock_quantity` | Integer | 60-300 | Restock quantity | Order size |
| `promotion_flag` | Integer | 0, 1 | Promotion flag | Promotional factor |
| `temperature_celsius` | Float | 15-40 °C | Temperature | Climate factor |
| `humidity_percent` | Float | 30-80% | Humidity | Climate factor |
| `truck_arrival_delay_mins` | Integer | 0-100 | Delivery delay | **Lead time variability ⭐** |
| `demand_forecast` | Float | **TARGET** | Demand forecast | **ML forecast ⭐** |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ Lead time tracking (critical for Nova Corrente)
- ✅ Weather integration (temperature, humidity - relevant for Salvador)
- ✅ Delivery delay tracking (lead time variability)
- ✅ Large dataset volume

**Limitations:**
- ⚠️ Generic supply chain (not telecom-specific)
- ⚠️ Promotional factors (not relevant for B2B)
- ⚠️ Multi-warehouse (Nova Corrente centralized)

**Adaptation Strategy:**
```python
# Cloud Supply Chain → Nova Corrente
# Use: Lead time, weather factors, delivery delays
# Ignore: Promotions, multi-warehouse, generic categories
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/kaggle_cloud_supply_chain/Cloud_SupplyChain_Dataset.csv` (~600 KB, 3,200+ rows)

**Processed Data:**
- `data/processed/kaggle_cloud_supply_chain_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Medium relevance - Lead time and weather factors useful, but generic supply chain focus

**Recommendation:** Use selectively - Lead time and weather features only.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

