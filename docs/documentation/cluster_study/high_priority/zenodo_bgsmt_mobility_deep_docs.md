# 📊 Deep Technical Documentation: Brazilian GSM Telecom (BGSMT) Mobility Dataset

**Dataset ID:** `zenodo_bgsmt_mobility`
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
- **Telecom Fit:** 15 points
- **Brazil Market:** 15 points
- **Data Quality:** 10 points
- **Logistics Info:** 0 points
- **Research Value:** 5 points

### Evaluation Reasons

- Contains demand/forecast data
- Direct spare parts/inventory focus
- Telecom industry data
- Brazilian market data
- Time-series data available
- Item/product identification available
- Academic/research dataset

### Categories

- `demand_forecasting`
- `telecom_industry`
- `brazilian_market`
- `high_quality`
- `research_reference`

---

## 📋 Dataset Information

**Name:** Brazilian GSM Telecom (BGSMT) Mobility Dataset
**Description:** 526,894 mobility records from 4,545 users, September 2017 - September 2018, 15-minute intervals. Mobility patterns across multiple Brazilian states.

**URL:** [https://zenodo.org/records/8178782](https://zenodo.org/records/8178782)

### Column Mapping

| Mapped Column | Original Column | Notes |
|--------------|----------------|-------|
| `date` | `timestamp` | - |
| `item_id` | `user_id` | - |
| `quantity` | `N/A` | - |
| `site_id` | `location_id` | - |
| `category` | `mobility_type` | - |

### Preprocessing Notes

High-value mobility dataset for demand forecasting based on user movement, tower load prediction, and infrastructure planning.

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
python backend/scripts/fetch_all_ml_datasets.py --dataset zenodo_bgsmt_mobility

# Structure for ML
python backend/scripts/structure_ml_datasets.py --dataset zenodo_bgsmt_mobility

# Enrich with external factors
python backend/scripts/comprehensive_dataset_pipeline.py --dataset zenodo_bgsmt_mobility
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
