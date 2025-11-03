# Complete Dataset System Guide - Nova Corrente Grand Prix SENAI

## 🎯 System Overview

Complete end-to-end data pipeline for downloading, preprocessing, merging, and preparing datasets for ML model training in the Nova Corrente demand forecasting project.

## 📋 System Components

### Core Pipeline Scripts

1. **`run_pipeline.py`** - Main orchestrator (run this first!)
   - Executes complete pipeline: Download → Preprocess → Merge → Add Factors
   - Command-line interface with options
   - Progress tracking and error handling

2. **`download_datasets.py`** - Download datasets from multiple sources
   - Kaggle API integration
   - Direct URL downloads (Zenodo, MIT)
   - Retry logic and progress tracking

3. **`preprocess_datasets.py`** - Standardize and clean datasets
   - Column mapping to unified schema
   - Date standardization
   - Feature engineering
   - Outlier removal

4. **`merge_datasets.py`** - Merge multiple datasets
   - Schema validation
   - Conflict resolution
   - Unified dataset creation

5. **`add_external_factors.py`** - Add external factors
   - Climate factors (temperature, precipitation, humidity)
   - Economic factors (exchange rate, inflation, GDP)
   - Regulatory factors (5G coverage)
   - Operational factors (holidays, vacations, SLA periods)

### Quality & Validation Scripts

6. **`validate_data.py`** - Data validation
   - Schema validation
   - Data quality checks
   - Completeness validation
   - Consistency checks

7. **`data_quality_report.py`** - Generate quality reports
   - Descriptive statistics
   - Visualizations (if matplotlib available)
   - JSON statistics export

### Training Preparation Scripts

8. **`prepare_for_training.py`** - Prepare data for ML models
   - Create item-specific datasets
   - Split train/test data
   - Format for ARIMA, Prophet, LSTM
   - Generate training metadata

### Utility Scripts

9. **`example_usage.py`** - Code examples
   - Usage demonstrations
   - Programmatic examples
   - Best practices

## 🚀 Quick Start Guide

### Step 1: Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure Kaggle API (optional, for Kaggle datasets)
cp config/kaggle_config.json.template config/kaggle_config.json
# Edit config/kaggle_config.json with your Kaggle credentials
```

### Step 2: Run Complete Pipeline

```bash
# Run full pipeline (download, preprocess, merge, add factors)
python run_pipeline.py
```

### Step 3: Validate Data

```bash
# Validate the unified dataset
python validate_data.py

# Generate quality report
python data_quality_report.py
```

### Step 4: Prepare for Training

```bash
# Prepare data for ML model training
python prepare_for_training.py
```

## 📊 Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Download Datasets (download_datasets.py)            │
│   ├─ Kaggle API downloads                                    │
│   ├─ Direct URL downloads                                    │
│   └─ Scrapy scraping (if needed)                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Preprocess Datasets (preprocess_datasets.py)       │
│   ├─ Column mapping                                          │
│   ├─ Date standardization                                   │
│   ├─ Feature engineering                                    │
│   └─ Outlier removal                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Merge Datasets (merge_datasets.py)                  │
│   ├─ Schema validation                                       │
│   ├─ Conflict resolution                                    │
│   └─ Unified dataset creation                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Add External Factors (add_external_factors.py)     │
│   ├─ Climate factors                                         │
│   ├─ Economic factors                                        │
│   ├─ Regulatory factors                                      │
│   └─ Operational factors                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Validate & Report (validate_data.py,                 │
│        data_quality_report.py)                              │
│   ├─ Schema validation                                       │
│   ├─ Quality checks                                          │
│   └─ Generate reports                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: Prepare for Training (prepare_for_training.py)     │
│   ├─ Item-specific datasets                                  │
│   ├─ Train/test splits                                       │
│   └─ Format for ARIMA/Prophet/LSTM                          │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Output Files Structure

```
data/
├── raw/                              # Raw downloaded datasets
│   ├── kaggle_daily_demand/
│   ├── kaggle_logistics_warehouse/
│   ├── kaggle_retail_inventory/
│   ├── kaggle_supply_chain/
│   ├── zenodo_milan_telecom/
│   └── mit_telecom_parts/
│
├── processed/                        # Preprocessed data
│   ├── {dataset_id}_preprocessed.csv  # Individual preprocessed datasets
│   ├── unified_dataset.csv            # Merged unified dataset
│   ├── unified_dataset_with_factors.csv  # Final enriched dataset
│   ├── preprocessing_log.txt          # Preprocessing logs
│   └── merge_log.txt                  # Merge logs
│
├── training/                         # Training-ready datasets
│   ├── {item_id}_full.csv            # Full item dataset
│   ├── {item_id}_train.csv           # Training split
│   ├── {item_id}_test.csv            # Test split
│   ├── metadata.json                 # Training metadata
│   └── training_summary.json          # Summary statistics
│
├── reports/                          # Quality reports
│   ├── data_quality_report.txt       # Text report
│   ├── statistics.json               # JSON statistics
│   ├── daily_demand_timeseries.png   # Visualizations
│   ├── top_items_quantity.png
│   ├── quantity_distribution.png
│   └── source_distribution.png
│
└── *.log                             # Pipeline logs
```

## 🎯 Usage Examples

### Example 1: Download Specific Datasets

```bash
# Download only specific datasets
python download_datasets.py --datasets kaggle_daily_demand kaggle_logistics_warehouse
```

### Example 2: Skip Steps (if data already exists)

```bash
# Skip download and preprocess, only add external factors
python run_pipeline.py --skip-download --skip-preprocess --skip-merge
```

### Example 3: Preprocess Only

```bash
# Preprocess specific datasets
python preprocess_datasets.py --datasets kaggle_daily_demand
```

### Example 4: Programmatic Usage

```python
from download_datasets import DatasetDownloader
from preprocess_datasets import DatasetPreprocessor
from merge_datasets import DatasetMerger
from add_external_factors import ExternalFactorsAdder

# Download
downloader = DatasetDownloader()
results = downloader.download_all_datasets(
    selected_datasets=['kaggle_daily_demand']
)

# Preprocess
preprocessor = DatasetPreprocessor()
preprocessed = preprocessor.preprocess_all_datasets(
    selected_datasets=['kaggle_daily_demand']
)

# Merge
merger = DatasetMerger()
unified_df = merger.create_unified_dataset(
    selected_datasets=['kaggle_daily_demand']
)

# Add factors
adder = ExternalFactorsAdder()
enriched_df = adder.add_external_factors()
```

## 🔧 Configuration

### Add New Dataset

Edit `config/datasets_config.json`:

```json
{
  "datasets": {
    "your_new_dataset": {
      "name": "Your Dataset Name",
      "source": "kaggle",
      "dataset": "username/dataset-name",
      "description": "Dataset description",
      "relevance": "⭐⭐⭐⭐",
      "columns_mapping": {
        "date": "Date",
        "item_id": "Item_ID",
        "quantity": "Quantity"
      },
      "preprocessing_notes": "Any special notes"
    }
  }
}
```

### Customize Preprocessing

Edit `config/datasets_config.json` preprocessing section:

```json
{
  "preprocessing": {
    "min_historical_months": 24,
    "aggregation_level": "daily",
    "fill_missing": "forward_fill",
    "outlier_removal": "iqr_method"
  }
}
```

## 📈 Next Steps for ML Training

After running the pipeline:

1. **Load Training Data**
   ```python
   import pandas as pd
   
   # Load unified dataset
   df = pd.read_csv('data/processed/unified_dataset_with_factors.csv')
   
   # Or load item-specific training data
   train_df = pd.read_csv('data/training/{item_id}_train.csv')
   ```

2. **Train Models** (see `Grok-_27.md` for specifications)
   - ARIMA: Use item-specific datasets
   - Prophet: Use Prophet-ready format (ds, y columns)
   - LSTM: Use prepare_for_lstm() function

3. **Calculate Reorder Points (PP)**
   ```python
   # PP = (Demanda_Diária × Lead_Time) + Safety_Stock
   pp = (avg_daily_demand * lead_time) + safety_stock
   ```

4. **Generate Alerts & Reports**
   - When Estoque_Atual ≤ PP
   - Calculate days until rupture
   - Generate procurement recommendations

## 🔍 Data Quality Checks

Run validation before training:

```bash
# Full validation
python validate_data.py

# Quality report
python data_quality_report.py
```

## 📚 Documentation Files

- **`README_DATASETS.md`** - Main usage guide
- **`IMPLEMENTATION_SUMMARY.md`** - Technical implementation details
- **`COMPLETE_SYSTEM_GUIDE.md`** - This file (complete system overview)
- **`example_usage.py`** - Code examples

## ⚠️ Troubleshooting

### Kaggle API Issues
- Ensure `config/kaggle_config.json` exists with valid credentials
- Check Kaggle account has access to datasets
- Verify internet connection

### Missing Data Files
- Check `data/raw/` for downloaded files
- Re-run download step if files are missing
- Some datasets may require manual download (MIT PDF)

### Memory Issues
- Process datasets individually using `--datasets` flag
- Use `--skip-download` if raw data exists
- Use `--skip-preprocess` if preprocessed data exists

## ✅ Testing Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Configure Kaggle API (if using Kaggle datasets)
- [ ] Run full pipeline: `python run_pipeline.py`
- [ ] Validate data: `python validate_data.py`
- [ ] Generate quality report: `python data_quality_report.py`
- [ ] Prepare for training: `python prepare_for_training.py`
- [ ] Verify output files in `data/processed/` and `data/training/`

## 🎉 System Complete!

The complete dataset system is ready for use. The unified dataset can now be used for training predictive demand forecasting models for Nova Corrente's Grand Prix project.

**Next**: Implement ML models (ARIMA, Prophet, LSTM) using the prepared training data!



