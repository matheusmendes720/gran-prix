# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Kaggle Retail Store Inventory Dataset

**Dataset ID:** `kaggle_retail_inventory`  
**Source:** Kaggle  
**Status:** ✅ Processed (if applicable)  
**Relevance:** ⭐⭐ (Low - B2C Focus, Irrelevant for B2B)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Retail Store Inventory & Demand Forecasting (B2C)  
**Records:** 73,000+ rows  
**Features:** 14 columns (date, store, product, category, inventory, sales, forecast, weather, etc.)  
**Date Range:** 2022+ (daily data)  
**Target Variable:** `Units_Sold` - Retail sales (B2C demand)

**Business Context:**
- **B2C retail store** inventory management
- Consumer demand patterns (volatile, price-sensitive)
- Promotional impacts (not relevant for B2B)
- Weather integration (similar to Milan dataset)
- **NOTE:** B2C focus, NOT relevant for Nova Corrente B2B model

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Platform:** Kaggle  
**Dataset ID:** Retail store inventory forecasting  
**URL:** https://www.kaggle.com/datasets/retail-store-inventory  
**License:** Open Database License (ODbL)

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Description | Business Context |
|--------|------|-------------|------------------|
| `Date` | DateTime | Daily date | Temporal key |
| `Store ID` | String | Store identifier | Location |
| `Product ID` | String | Product SKU | Item identifier |
| `Category` | String | Groceries, Toys, Electronics, etc. | Category classification |
| `Region` | String | North, South, East, West | Geographic region |
| `Inventory Level` | Integer | Current inventory | Stock level |
| `Units Sold` | Integer | Daily sales | **B2C demand** |
| `Units Ordered` | Integer | Daily orders | Reorder quantity |
| `Demand Forecast` | Float | Forecasted demand | ML forecast |
| `Price` | Float | Unit price | Price factor |
| `Discount` | Float | Discount percentage | Promotional factor |
| `Weather Condition` | String | Rainy, Sunny, Cloudy, Snowy | Climate factor |
| `Holiday/Promotion` | Integer | 0, 1 | Promotional flag | **B2C specific** |
| `Competitor Pricing` | Float | Competitor price | Price competition |
| `Seasonality` | String | Autumn, Spring, Summer, Winter | Seasonal factor |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Limitations:**
- ⚠️ **B2C retail** focus, NOT B2B telecom maintenance
- ⚠️ Promotional impacts (not relevant for B2B contracts)
- ⚠️ Price-sensitive demand (B2B contracts fixed)
- ⚠️ Volatile consumer demand (B2B demand stable)

**Potential Use:**
- Weather integration validation (similar patterns)
- Large dataset for deep learning (73K+ rows)
- Seasonal pattern analysis (can be adapted)

**Recommendation:** **ARCHIVE** or use only for:
- Weather correlation validation
- Deep learning dataset volume (for testing)
- **NOT for production model training**

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/kaggle_retail_inventory/retail_store_inventory.csv` (~5 MB, 73,000+ rows)

**Processed Data:**
- `data/processed/kaggle_retail_inventory_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Low relevance - B2C focus, not relevant for B2B telecom maintenance

**Recommendation:** **ARCHIVE** - B2C retail data not relevant for Nova Corrente B2B telecom maintenance problem. Use only for weather validation or deep learning testing.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

