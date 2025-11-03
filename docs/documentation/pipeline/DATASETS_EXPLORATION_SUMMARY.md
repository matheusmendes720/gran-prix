# 📊 New Datasets Exploration Summary

## Dataset Structure Analysis

### ✅ Successfully Downloaded & Analyzed

---

## 1. **5G3E Virtualized Infrastructure Dataset** ⭐⭐⭐⭐⭐

**Location:** `data/raw/github_5g3e/`
**Files:** 5 CSV files
**Total Size:** ~259 MB

### Structure
- **Format:** Prometheus exporter CSV (wide format)
- **Columns:** 767+ columns (multivariate time-series)
- **First Row:** Header with complex metric names
- **Metrics Include:**
  - CPU metrics (node_cpu_seconds_total with 32 CPUs, various modes)
  - Disk I/O metrics (node_disk_*)
  - Network metrics (node_network_*)
  - Memory metrics (node_memory_*)
  - System metrics (load, processes, etc.)
  - Thermal sensors
  - Network statistics
  - File system metrics

### Complexity
This is a **Prometheus monitoring format** with:
- High-dimensional multivariate data
- Time-series format
- System metrics for infrastructure monitoring
- **NOT ready for direct preprocessing** with current pipeline
- Requires specialized parsing for Prometheus format

### Recommendations
1. **Parse Prometheus format** first
2. **Extract key metrics** (CPU usage, memory, network throughput)
3. **Convert to time-series** format
4. **Feature engineering** for infrastructure patterns
5. **Use for:** Predictive maintenance modeling, capacity planning

---

## 2. **Equipment Failure Prediction Dataset** ⭐⭐⭐⭐

**Location:** `data/raw/kaggle_equipment_failure/`
**Files:** `ai4i2020.csv`
**Size:** ~150 KB (10,000 rows)

### Structure
```csv
UDI, Product ID, Type, Air temperature [K], Process temperature [K], 
Rotational speed [rpm], Torque [Nm], Tool wear [min], Machine failure, 
TWF, HDF, PWF, OSF, RNF
```

### Columns Mapping (Ready for Preprocessing)
```json
{
  "date": null,  // NO DATE COLUMN - classification dataset
  "item_id": "Product ID",
  "category": "Type",
  "quantity": "Machine failure",  // Binary: 0/1
  // Features:
  "air_temperature": "Air temperature [K]",
  "process_temperature": "Process temperature [K]",
  "rotational_speed": "Rotational speed [rpm]",
  "torque": "Torque [Nm]",
  "tool_wear": "Tool wear [min]",
  // Failure types (binary flags):
  "twf": "TWF",  // Tool Wear Failure
  "hdf": "HDF",  // Heat Dissipation Failure
  "pwf": "PWF",  // Power Failure
  "osf": "OSF",  // Overstrain Failure
  "rnf": "RNF"   // Random Failure
}
```

### Characteristics
- **Classification dataset** (no time-series)
- **Target variable:** Machine failure (binary)
- **Features:** 14 columns total
- **Product types:** M (Medium), L (Low), H (High) - categorized by operation
- **Ready for:** Binary classification, failure prediction models

---

## 3. **Network Fault Prediction Dataset** ⭐⭐⭐⭐

**Location:** `data/raw/github_network_fault/`
**Files:** 5 CSV files
**Total Size:** ~9 MB

### Files Structure
1. **event_type.csv** - Event type classifications
2. **feature_Extracted_test_data.csv** - Test features
3. **feature_Extracted_trian_data.csv** - Train features (typo: trian)
4. **log_feature.csv** - Log-based features
5. **processed_test1.csv** - Processed test data

### Characteristics
- **Classification dataset** for fault severity
- **Event types:** Multiple (11, 15, 20, etc.)
- **Telstra competition data**
- **Ready for:** Fault classification models, severity prediction

---

## 4. **Telecom Network Dataset** ⭐⭐⭐

**Location:** `data/raw/kaggle_telecom_network/`
**Files:** `Telecom_Network_Data.csv`
**Size:** Variable

### Structure
```csv
timestamp, tower_id, users_connected, download_speed, upload_speed, 
latency, weather, congestion
```

### Columns Mapping (Ready for Preprocessing)
```json
{
  "date": "timestamp",
  "site_id": "tower_id",
  "quantity": "users_connected",  // Demand proxy
  // Features:
  "download_speed": "download_speed",
  "upload_speed": "upload_speed",
  "latency": "latency",
  "weather": "weather",
  "congestion": "congestion"  // Binary: 0/1
}
```

### Characteristics
- **Time-series dataset** (hourly data)
- **Tower-level operations**
- **Weather integration** included
- **Congestion flags** for capacity issues
- **Ready for:** Capacity forecasting, demand prediction

---

## 📋 Preprocessing Readiness

| Dataset | Time-Series | Classification | Ready | Complexity |
|---------|-------------|----------------|-------|------------|
| **5G3E** | ✅ Yes | ❌ No | ⚠️ Special | High (Prometheus format) |
| **Equipment Failure** | ❌ No | ✅ Yes | ✅ Yes | Low |
| **Network Fault** | ❌ No | ✅ Yes | ⚠️ Partial | Medium |
| **Telecom Network** | ✅ Yes | ❌ No | ✅ Yes | Low |

---

## 🔧 Required Preprocessing Updates

### 1. **Equipment Failure** - Add Custom Handler
```python
# Already structured well
# Map columns to unified schema
# Handle binary classification
# No date column needed (classification task)
```

### 2. **Telecom Network** - Standard Time-Series
```python
# Standard time-series preprocessing
# Parse timestamp column
# Map weather categories
# Handle congestion as binary feature
```

### 3. **Network Fault** - Classification Handler
```python
# Multi-file handling
# Merge training/test splits
# Parse event types
# Handle severity classification
```

### 4. **5G3E** - Special Parser Required
```python
# Parse Prometheus CSV format
# Extract key metrics
# Convert to time-series
# Feature engineering
# Heavy processing needed
```

---

## 🎯 Next Steps

### Immediate Actions

1. **Update Configuration** ⏳
   - Add proper column mappings for Equipment Failure
   - Add Telecom Network mappings
   - Document 5G3E special handling

2. **Add Preprocessing Handlers** ⏳
   - Binary classification handler
   - Multi-file dataset handler
   - Prometheus parser (future)

3. **Testing** ⏳
   - Test Equipment Failure preprocessing
   - Test Telecom Network time-series
   - Validate Network Fault files

4. **Integration** ⏳
   - Merge with existing datasets
   - Update training pipeline
   - Add model support

---

## 📊 Expected Model Enhancements

### With New Datasets

**Equipment Failure:**
- Binary classification model
- Failure probability prediction
- Spare parts demand forecasting

**Telecom Network:**
- Capacity forecasting
- Congestion prediction
- Weather impact analysis

**Network Fault:**
- Fault severity classification
- Response prioritization
- Maintenance scheduling

**5G3E:**
- Infrastructure monitoring
- Predictive maintenance
- Resource optimization

---

## ✅ Status Summary

**Dataset Exploration:** ✅ **COMPLETE**

- ✅ **4 datasets** downloaded and analyzed
- ✅ **Structure** identified for all datasets
- ✅ **Preprocessing requirements** documented
- ✅ **Next steps** defined

**Ready for Integration:** 🎯 **NEXT PHASE**

---

**Date:** 2025-10-31  
**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

