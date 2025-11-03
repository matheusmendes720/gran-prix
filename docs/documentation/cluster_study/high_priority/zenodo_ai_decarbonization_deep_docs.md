# 📊 Deep Technical Documentation: AI-driven Decarbonization of Buildings: Predictive Maintenance

**Dataset ID:** `zenodo_ai_decarbonization`
**Source:** zenodo
**Evaluation Score:** 70/100
**Tier:** High Priority
**Generated:** 2025-11-02 21:34:35

---

## 🎯 Business Case Relevance

### Nova Corrente Use Case

**Primary Problem:** Spare parts demand forecasting for 18,000+ telecom towers

**Key Requirements:**
- Predict future consumption of spare parts/services
- Support inventory optimization and reorder point calculation
- Maintain SLA compliance (99%+ uptime)
- Account for lead times, seasonality, and external factors

**This Dataset's Fit:** HIGH - Strong relevance, recommended for pipeline

---

## 📊 Detailed Evaluation

### Score Breakdown

- **Demand Relevance:** 25 points
- **Telecom Fit:** 25 points
- **Brazil Market:** 0 points
- **Data Quality:** 15 points
- **Logistics Info:** 0 points
- **Research Value:** 5 points

### Evaluation Reasons

- Contains demand/forecast data
- Direct spare parts/inventory focus
- Telecom industry data
- Maintenance/failure data
- Time-series data available
- Quantity/demand column present
- Item/product identification available
- Academic/research dataset

### Categories

- `demand_forecasting`
- `telecom_industry`
- `high_quality`
- `research_reference`

---

## 📋 Dataset Information

**Name:** AI-driven Decarbonization of Buildings: Predictive Maintenance
**Description:** Predictive maintenance dataset for energy systems. Adaptable to telecom towers with MAPE metrics.

**URL:** [https://zenodo.org/records/15004071](https://zenodo.org/records/15004071)

### Column Mapping

| Mapped Column | Original Column | Notes |
|--------------|----------------|-------|
| `date` | `timestamp` | - |
| `item_id` | `system_id` | - |
| `quantity` | `maintenance_demand` | - |
| `category` | `system_type` | - |

### Preprocessing Notes

Predictive maintenance for energy systems, adaptable to telecom towers.

### Additional Notes

MAPE metrics included for model validation

---

## 🤖 Recommended ML Algorithms

### Time-Series Forecasting

1. **ARIMA/SARIMA:** For univariate time-series with trend and seasonality
2. **Prophet:** Facebook's forecasting tool, handles holidays and seasonality well
3. **LSTM:** Deep learning for complex non-linear patterns
4. **XGBoost:** Gradient boosting with feature engineering

### Predictive Maintenance

1. **Random Forest:** For classification of failure types
2. **XGBoost:** For failure prediction with feature importance
3. **LSTM:** For sequential failure pattern detection

---

## 🔗 Integration Guide

### How to Use This Dataset

1. **Download:** Use the download script in `cluster_study/download_scripts/`
2. **Structure:** Run through ML data structuring pipeline
3. **Enrich:** Integrate with external factors (climate, economy)
4. **Validate:** Run quality validation checks
5. **Model:** Train forecasting models (ARIMA, Prophet, LSTM)

### Pipeline Integration

```bash
# Download dataset
python backend/scripts/fetch_all_ml_datasets.py --dataset zenodo_ai_decarbonization

# Structure for ML
python backend/scripts/structure_ml_datasets.py --dataset zenodo_ai_decarbonization

# Enrich with external factors
python backend/scripts/comprehensive_dataset_pipeline.py --dataset zenodo_ai_decarbonization
```

---

## 💼 Business Impact

### Expected Benefits

- **HIGH VALUE:** Strong relevance to business case
- Good accuracy for demand forecasting
- Helps optimize inventory levels

### ROI Potential

Based on Internet Aberta ROI analysis (internet_aberta_roi_brazil dataset):
- B2B telecom solutions typically show ROI >100%
- Predictive maintenance can reduce costs by 20-30%
- Inventory optimization can free 15-20% of capital
