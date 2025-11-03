# 📊 Complete Dataset Context Summary

## Nova Corrente - Demand Forecasting System

---

## 🎯 Executive Summary

This document provides **comprehensive context** for all 15 datasets in the Nova Corrente project, with deep understanding of each column, variable, and business context derived from web research and data exploration.

**Total Datasets Analyzed:** 15  
**Data Sources:** Kaggle, Zenodo, GitHub, Brazilian Regulators, Academic Research  
**Documentation Status:** ✅ Complete with deep context

---

## 📁 Dataset Quick Reference

### ✅ **Ready for ML Training** (5 datasets)

1. **test_dataset** - 732 rows, 7 cols, synthetic baseline
2. **zenodo_milan_telecom** - 116K rows, 38 cols, 5G slice demand
3. **zenodo_broadband_brazil** - 2,044 rows, 8 cols, QoS metrics
4. **unified_dataset_with_factors** - 118K rows, 31 cols, complete merged
5. **training splits** (unknown + CONN-001) - ready for ML

### ⚠️ **Requires Parsing** (3 datasets)

6. **anatel_mobile_brazil** - HTML/JSON → CSV conversion needed
7. **internet_aberta_forecast** - PDF → table extraction needed
8. **springer_digital_divide** - HTML → data link scraping needed

### 🔧 **Complex Processing** (4 datasets)

9. **github_5g3e** - Prometheus format (767+ columns)
10. **github_network_fault** - Multi-file log feature extraction
11. **kaggle_supply_chain** - High-dimensional, 91K rows
12. **kaggle_retail_inventory** - 73K rows, weather integration

### 📊 **Kaggle Competition Datasets** (3 datasets)

13. **kaggle_equipment_failure** - AI4I 2020 binary classification
14. **kaggle_telecom_network** - Tower capacity forecasting
15. **kaggle_daily_demand** - MVP multi-sector orders
16. **kaggle_logistics_warehouse** - Inventory KPIs

---

## 🔍 Key Insights by Category

### **1. Telecom/Network Datasets** (7 datasets)

**Common Patterns:**
- **Demand Proxy:** users_connected, totalSched, traffic_load
- **Quality Metrics:** latency, jitter, packet_loss, rejectRate
- **Capacity Planning:** tower load → infrastructure investment
- **Weather Impact:** storms affect network performance

**Brazilian Context:**
- Anatel regulations drive tower expansion
- 5G rollout creates demand spikes
- Rural coverage gaps = business opportunity
- Climate (tropical storms, humidity) impacts infrastructure

### **2. Inventory/Supply Chain** (4 datasets)

**Common Patterns:**
- **Multi-Echelon:** Warehouse → Supplier coordination
- **Lead Times:** Critical for inventory optimization
- **Stockouts:** Binary flags indicate service failures
- **Promotions:** Discount lift analysis

**Business Intelligence:**
- Balance holding costs vs stockout costs
- Regional demand variability
- Category-specific patterns
- Supplier reliability metrics

### **3. Predictive Maintenance** (2 datasets)

**Common Patterns:**
- **Sensor Telemetry:** Temperature, vibration, pressure
- **Failure Modes:** Multiple failure types
- **Binary Classification:** Failure vs normal operation
- **Feature Engineering:** Interaction terms crucial

**Nova Corrente Context:**
- Apply to telecom tower equipment
- Power system failures
- Cooling system degradation
- RF equipment wear patterns

### **4. Academic/Research** (2 datasets)

**Common Patterns:**
- **Long-Term Forecasts:** 10+ year projections
- **Policy Analysis:** Digital divide research
- **Spatial Data:** Urban vs rural patterns
- **Scale Challenges:** 100M+ records

---

## 📊 Column Dictionary

### **Temporal Columns**

| Column Name | Format | Usage | Examples |
|-------------|--------|-------|----------|
| `Date` | YYYY-MM-DD | Primary temporal key | 2023-01-01 |
| `timestamp` | ISO 8601 | High-frequency data | 2023-01-01 00:00:00 |
| `step` | Integer | Episode/sequence index | 0-116,256 |
| `episode` | Integer | Algorithm episode ID | 0-41 |
| `year`, `month`, `day_of_week` | Integer | Derived temporal features | 2023, 1, 0 |

### **Identity Columns**

| Column Name | Type | Purpose | Examples |
|-------------|------|---------|----------|
| `item_id` | String | Product identifier | CONN-001, P0001 |
| `Product ID` | String | Alternative product ID | M14860, L47181 |
| `Customer_ID` | Integer | Customer identifier | 1-2043 |
| `bsId` | Integer | Base Station ID | 1 |
| `site_id` | String | Location identifier | TORRE001 |
| `tower_id` | Integer | Cell tower ID | 1 |

### **Demand/Quantity Columns**

| Column Name | Range | Meaning | Context |
|-------------|-------|---------|---------|
| `quantity` | Float | General demand | Unified schema |
| `Order_Demand` | 3-11 | Daily order count | Test dataset |
| `totalSched` | 0-40 | Admitted traffic | Zenodo Milan |
| `users_connected` | 0-1000 | Concurrent users | Tower capacity |
| `units_sold` | Variable | Actual sales | Supply chain |
| `daily_demand` | Variable | Average demand | Logistics |

### **Quality/Performance Columns**

| Column Name | Units | Normal Range | Critical Value |
|-------------|-------|--------------|----------------|
| `latency` | ms | 0-30 | >100ms = bad |
| `jitter` | ms | 2-4 | >10ms = bad |
| `packet_loss` | % | 0-1% | >5% = critical |
| `rejectRate` | Ratio | 0-0.3 | >0.5 = overloaded |
| `download_speed` | Mbps | 10-100 | <1 Mbps = issue |
| `upload_speed` | Mbps | 5-50 | <1 Mbps = issue |

### **Failure/Status Columns**

| Column Name | Type | Values | Meaning |
|-------------|------|--------|---------|
| `Machine failure` | Binary | 0, 1 | Equipment failure |
| `CRM_Complaint?` | Binary | 0, 1 | Customer complaint |
| `congestion` | Binary | 0, 1 | Network congested |
| `stockout_flag` | Binary | 0, 1 | Out of stock |
| `TWF`, `HDF`, `PWF`, `OSF`, `RNF` | Binary | 0, 1 | Failure mode flags |

### **Geographic Columns**

| Column Name | Type | Values | Context |
|-------------|------|--------|---------|
| `Region` | Categorical | North, South, East, West | Geographic breakdown |
| `country` | String | Brazil, etc. | National context |
| `state` | String | Brazilian states | Regional analysis |
| `latitude`, `longitude` | Float | GPS coordinates | Spatial analysis |

### **Weather Columns**

| Column Name | Type | Values | Impact |
|-------------|------|--------|--------|
| `weather` | Categorical | Clear, Rain, Snow, Storm | Network performance |
| `temperature` | Float | 20-35°C | Equipment stress |
| `precipitation` | Float | mm | Signal degradation |
| `humidity` | Float | 70-90% | Equipment wear |

### **Financial Columns**

| Column Name | Type | Meaning | Range |
|-------------|------|---------|-------|
| `cost` | Float | Unit cost | 300.0 (fixed) |
| `Unit_Cost` | Float | Procurement cost | Variable |
| `Unit_Price` | Float | Selling price | Variable |
| `exchange_rate_brl_usd` | Float | Currency rate | 5.0-6.0 |
| `inflation_rate` | Float | Economic indicator | 3-6% |

### **Operational Columns**

| Column Name | Type | Values | Purpose |
|-------------|------|--------|---------|
| `lead_time` | Integer | Days | Delivery time |
| `Lead_Time_Days` | Integer | Days | Supplier lead time |
| `reorder_point` | Integer | Units | Inventory trigger |
| `capacity` | Integer | Units | Maximum load |
| `Inventory_Level` | Integer | Units | Current stock |

---

## 🎯 Use Case Matrix

| Use Case | Primary Datasets | Target Variable | Algorithm Types |
|----------|-----------------|-----------------|-----------------|
| **Demand Forecasting** | test, milan, telecom | quantity, totalSched | ARIMA, Prophet, LSTM |
| **Maintenance Prediction** | equipment_failure, fault | Machine failure | RF, XGBoost, NN |
| **Capacity Planning** | milan, telecom, 5g3e | load, users | Regression, SVR |
| **Inventory Optimization** | warehouse, supply_chain | inventory_level | EOQ, ML-based |
| **Customer Quality** | broadband_brazil | CRM_Complaint | Classification |
| **Stockout Prediction** | supply_chain, retail | stockout_flag | Binary classification |

---

## 📈 Data Quality Scores

### **Highest Quality (⭐⭐⭐⭐⭐)**
- **test_dataset:** Synthetic, controlled, perfect for baselines
- **equipment_failure:** Competition-grade, labeled
- **zenodo_broadband:** Research-quality, real operator data
- **logistics_warehouse:** Comprehensive KPIs, structured
- **zenodo_milan:** Academic dataset, well-documented

### **Good Quality (⭐⭐⭐⭐)**
- **telecom_network:** Synthetic but realistic
- **supply_chain:** High-dimensional, complex
- **retail_inventory:** Large-scale, weather-integrated
- **network_fault:** Competition dataset, structured

### **Medium Quality (⭐⭐⭐)**
- **daily_demand:** Too small for ML (62 rows)
- **anatel_mobile:** Requires parsing
- **internet_aberta:** PDF extraction needed
- **springer_divide:** HTML scraping required

---

## 🔧 Preprocessing Status

### ✅ **Fully Processed** (5 datasets)
- test_dataset → test_dataset_preprocessed.csv
- zenodo_milan → zenodo_milan_telecom_preprocessed.csv
- Unified all → unified_dataset_with_factors.csv
- Training splits → unknown_train/test, CONN-001_train/test

### ⏳ **Partially Processed** (4 datasets)
- kaggle_daily_demand (raw, needs external factors)
- kaggle_logistics_warehouse (raw, needs unified schema)
- kaggle_retail_inventory (raw, needs external factors)
- kaggle_supply_chain (raw, needs unified schema)

### ❌ **Not Processed** (6 datasets)
- kaggle_equipment_failure (classification, no unified schema)
- github_5g3e (Prometheus format, complex)
- github_network_fault (multi-file, classification)
- anatel_mobile (parsing required)
- internet_aberta (PDF extraction)
- springer_divide (HTML scraping)

---

## 🎓 Academic Context References

### **Zenodo Milan Telecom**
**Paper:** "5G Network Slice Resource Demand Prediction"  
**Original:** MILANO dataset (Nov 2013 - Jan 2014)  
**Transformation:** Game-theoretic AI consensus admission control

### **Brazilian Broadband**
**Source:** Brazilian telecom operator (anonymized)  
**Research:** Customer churn prediction, QoS analysis  
**Application:** Predictive maintenance of CPE

### **Equipment Failure**
**Competition:** AI4I 2020 Predictive Maintenance  
**Domain:** Industrial IoT sensor data  
**Failure Modes:** 5 distinct types (TWF, HDF, PWF, OSF, RNF)

### **Telstra Network Fault**
**Competition:** Kaggle Telstra Fault Detection  
**Domain:** Telecommunications infrastructure logs  
**Challenge:** Multi-class severity prediction

### **Internet Aberta Forecast**
**Publication:** Academic research paper  
**Scope:** Brazil internet growth through 2033  
**Projections:** 297-400 exabytes data traffic

### **Springer Digital Divide**
**Journal:** EPJ Data Science  
**Data Source:** Ookla Speedtest Intelligence  
**Scale:** ~100M speed test records  
**Focus:** Urban-rural connectivity inequality

---

## 🔗 Cross-Dataset Relationships

### **Demand Chain Mapping**

```
zenodo_milan (5G slice demand)
    ↓
telecom_network (tower capacity)
    ↓
equipment_failure (infrastructure health)
    ↓
broadband_brazil (customer quality)
    ↓
anatel_mobile (regulatory compliance)
```

### **Supply Chain Mapping**

```
supply_chain (warehouse operations)
    ↓
logistics_warehouse (inventory KPIs)
    ↓
retail_inventory (store operations)
    ↓
daily_demand (order aggregation)
```

### **Infrastructure Chain**

```
5g3e_servers (virtualized infrastructure)
    ↓
network_fault (log analysis)
    ↓
equipment_failure (predictive maintenance)
    ↓
capacity_planning (demand forecasting)
```

---

## 🚀 Recommended Next Steps

### **Immediate Priorities**

1. **Complete Brazilian Dataset Parsing**
   - PDF extraction from internet_aberta
   - HTML scraping from springer_divide
   - JSON parsing from anatel_mobile

2. **Process Remaining Kaggle Datasets**
   - Add to unified schema
   - Enrich with external factors
   - Create training splits

3. **Handle Complex Formats**
   - Prometheus parser for 5g3e
   - Log feature extraction for network_fault
   - Multi-file dataset handler

4. **Model Training Pipeline**
   - Use unknown_train.csv for production models
   - Use CONN-001_train.csv for quick iterations
   - Implement multi-model ensemble

5. **Feature Engineering**
   - Temporal decomposition
   - Interaction terms
   - Aggregation features
   - Weather encoding

---

## 📊 Dataset Statistics Summary

**Total Rows Across All Datasets:** ~1.5 Million records  
**Total Columns (Combined):** 200+ unique features  
**Data Volume:** ~300 MB raw + 50 MB processed  
**Time Span:** 2013 - 2033 (historical + projections)  
**Geographic Coverage:** Brazil, Italy, Germany, Australia, Global  

---

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

**Generated:** 2025-10-31  
**Status:** ✅ Complete deep analysis with web research context  
**Next:** Continue preprocessing and model training

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**


