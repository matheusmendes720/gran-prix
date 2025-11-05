# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Kaggle Telecom Network Dataset

**Dataset ID:** `kaggle_telecom_network`  
**Source:** Kaggle  
**Status:** ✅ Processed (if applicable)  
**Relevance:** ⭐⭐ (Low - Capacity Focus, Not Maintenance)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Telecom Network Tower Capacity & Performance Data  
**Records:** 3,600+ rows (hourly data)  
**Features:** 8 columns (timestamp, tower_id, users, speed, latency, weather, congestion)  
**Date Range:** 2025-01-01 (sample)  
**Target Variable:** `users_connected` - Users connected (capacity proxy)

**Business Context:**
- Tower-level capacity tracking
- User connectivity monitoring
- Network performance metrics (download/upload speed, latency)
- Weather impact on network performance
- **NOTE:** Focus on capacity, NOT maintenance demand

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Platform:** Kaggle  
**Dataset ID:** praveenaparimi/telecom-network-dataset  
**URL:** https://www.kaggle.com/datasets/praveenaparimi/telecom-network-dataset  
**License:** Open Database License (ODbL)

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Range | Description | Business Context |
|--------|------|-------|-------------|------------------|
| `timestamp` | DateTime | 2025-01-01 00:00:00+ | Hourly timestamp | Temporal key |
| `tower_id` | Integer | 1+ | Tower identifier | Network node |
| `users_connected` | Integer | 100-1000+ | Users connected | **Capacity proxy** |
| `download_speed` | Float | 5-100 Mbps | Download speed | Performance metric |
| `upload_speed` | Float | 2-50 Mbps | Upload speed | Performance metric |
| `latency` | Integer | 30-200 ms | Network latency | Performance metric |
| `weather` | String | Clear, Rain, Snow | Weather condition | Climate factor |
| `congestion` | Integer | 0, 1 | Congestion indicator | Network load |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Limitations:**
- ⚠️ **Focus on capacity**, NOT maintenance demand
- ⚠️ User connectivity ≠ spare parts demand
- ⚠️ Performance metrics ≠ equipment failure

**Potential Use:**
- Low-traffic towers identification (intermittent demand patterns)
- Weather correlation validation (for Milan dataset)
- Capacity planning (not maintenance forecasting)

**Recommendation:** **ARCHIVE** or use only for validation

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/kaggle_telecom_network/Telecom_Network_Data.csv` (~1 MB, 3,600+ rows)

**Processed Data:**
- `data/processed/kaggle_telecom_network_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Low relevance - Capacity focus, not maintenance demand

**Recommendation:** ARCHIVE or use only for validation/clustering low-traffic towers

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

