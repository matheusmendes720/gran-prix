# 📊 Deep Technical Documentation: 5G3E Virtualized Infrastructure Dataset

**Dataset ID:** `github_5g3e`
**Source:** github
**Evaluation Score:** 60/100
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
- **Data Quality:** 10 points
- **Logistics Info:** 0 points
- **Research Value:** 0 points

### Evaluation Reasons

- Contains demand/forecast data
- Direct spare parts/inventory focus
- Telecom industry data
- Maintenance/failure data
- Time-series data available
- Item/product identification available

### Categories

- `demand_forecasting`
- `telecom_industry`
- `high_quality`

---

## 📋 Dataset Information

**Name:** 5G3E Virtualized Infrastructure Dataset
**Description:** 14 days of time-series from virtualized 5G infrastructure with radio, server, OS, and network function data. Thousands of features grouped by resource/node type.

**URL:** [https://github.com/cedric-cnam/5G3E-dataset](https://github.com/cedric-cnam/5G3E-dataset)

### Column Mapping

| Mapped Column | Original Column | Notes |
|--------------|----------------|-------|
| `date` | `timestamp` | - |
| `item_id` | `node_id` | - |
| `quantity` | `N/A` | - |
| `site_id` | `resource_type` | - |

### Preprocessing Notes

Excellent for predictive maintenance in telecom logistics. Forecasts demand for replacement parts amid long-tail failures (rare node outages). Integrates well with SARIMAX/Prophet/LSTM ensembles for uncertainty hedging. Size may require sampling or batch processing.

### Additional Notes

Large multivariate time-series - may need to process in batches

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
python backend/scripts/fetch_all_ml_datasets.py --dataset github_5g3e

# Structure for ML
python backend/scripts/structure_ml_datasets.py --dataset github_5g3e

# Enrich with external factors
python backend/scripts/comprehensive_dataset_pipeline.py --dataset github_5g3e
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
