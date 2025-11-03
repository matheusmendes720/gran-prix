# 🚀 Run the System

## Quick Start (Easiest)

### Option 1: Setup & Run (Recommended)
```bash
python setup_and_run.py
```

This will:
1. ✅ Check all dependencies
2. ✅ Create sample data if needed
3. ✅ Run the complete system
4. ✅ Generate all reports

### Option 2: Direct Run
```bash
python scripts/run_all.py
```

### Option 3: With Sample Data
```bash
python scripts/run_all.py --create-sample
```

## 📋 What Happens When You Run

The system will:

1. **Load Data**
   - Checks for data file (creates sample if needed)
   - Preprocesses and validates data
   - Extracts features

2. **Train Models**
   - ARIMA/SARIMA with auto-order selection
   - Prophet with holiday support
   - LSTM neural network
   - Ensemble combination

3. **Generate Forecasts**
   - 30-day forecasts for each item
   - Ensemble predictions
   - Confidence intervals

4. **Calculate Inventory Metrics**
   - Reorder points (PP)
   - Safety stock
   - Days to rupture

5. **Check Alerts**
   - Low stock alerts
   - Urgency levels (critical, high, medium)

6. **Generate Reports**
   - CSV reports with forecasts
   - PDF reports with details
   - Visualization plots

## 🎯 Output Files

After running, check the `reports/` directory:

```
reports/
├── forecast_report_YYYYMMDD.csv       # CSV report
├── forecast_report_YYYYMMDD.pdf       # PDF report
├── forecast_ITEM_YYYYMMDD.png         # Forecast plots
└── inventory_ITEM_YYYYMMDD.png       # Inventory metrics
```

## ⚙️ Advanced Options

### Process Specific Item
```bash
python scripts/run_all.py --item CONN-001
```

### Skip Training (Use Existing Models)
```bash
python scripts/run_all.py --skip-training
```

### Skip Visualizations (Faster)
```bash
python scripts/run_all.py --no-viz
```

### Custom Data File
```bash
python scripts/run_all.py --data data/my_data.csv
```

### Custom Config
```bash
python scripts/run_all.py --config custom_config.yaml
```

## 📊 Example Run

```bash
$ python setup_and_run.py

================================================================================
                        DEMAND FORECASTING SYSTEM
                            Setup & Run
================================================================================

Checking dependencies...
✓ All required dependencies installed

================================================================================
Starting forecast system...
================================================================================

================================================================================
                        DEMAND FORECASTING SYSTEM
                   Nova Corrente - Complete Run
================================================================================

Timestamp: 2024-01-01 12:00:00
Data file: data/nova_corrente_demand.csv
Config file: config.yaml

================================================================================

STEP 1: Loading and Preprocessing Data
================================================================================
✓ Loaded data for 3 items

STEP 2: Processing Items
================================================================================
Processing: CONN-001
  [Model] Training ensemble...
    ✓ ARIMA
    ✓ Prophet
    ✓ LSTM
  [Forecast] Generating 30-day forecast...
    ✓ Generated forecast: 30 days
  [Inventory] Calculating reorder point...
    Current Stock: 100 units
    Reorder Point: 150 units
    Days to Rupture: 12.5 days
    ⚠️  ALERT: HIGH

STEP 3: Generating Reports
================================================================================
✓ CSV report: reports/forecast_report_20240101.csv
✓ PDF report: reports/forecast_report_20240101.pdf

SUMMARY
================================================================================
Items Processed: 3
Items with Alerts: 1
Total Alerts: 1

✅ Forecast run completed successfully!
```

## 🔧 Troubleshooting

### Dependencies Missing
```bash
# Install all dependencies
pip install -r requirements.txt

# Or use setup script
python setup_and_run.py
```

### Data File Not Found
```bash
# Create sample data
python scripts/run_all.py --create-sample
```

### TensorFlow Not Available
- LSTM model will be skipped automatically
- System works with ARIMA + Prophet

### Memory Issues
```bash
# Process one item at a time
python scripts/run_all.py --item CONN-001

# Or reduce epochs in config.yaml
```

## 🎓 Next Steps

1. **Review Reports**: Check `reports/` directory
2. **Customize Config**: Edit `config.yaml`
3. **Use Your Data**: Place CSV in `data/` directory
4. **Set Up Alerts**: Configure email in `config.yaml`
5. **Schedule Runs**: Set up cron/Airflow job

---

**Ready to forecast!** 🚀

