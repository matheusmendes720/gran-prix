# Quick Start Guide - Demand Forecasting System

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Everything!

```bash
python scripts/run_all.py
```

This will:
- ✅ Create sample data if needed
- ✅ Load and preprocess data
- ✅ Train all models (ARIMA, Prophet, LSTM, Ensemble)
- ✅ Generate forecasts for all items
- ✅ Calculate reorder points
- ✅ Check for alerts
- ✅ Generate reports (CSV, PDF)
- ✅ Create visualizations

### Step 3: Check Results

Results will be in the `reports/` directory:
- `forecast_report_YYYYMMDD.csv` - CSV report with forecasts
- `forecast_report_YYYYMMDD.pdf` - PDF report with details
- `forecast_ITEM_YYYYMMDD.png` - Forecast visualizations
- `inventory_ITEM_YYYYMMDD.png` - Inventory metrics

## 📋 Available Scripts

### Main Scripts

1. **Run Everything**
   ```bash
   python scripts/run_all.py
   ```

2. **Generate Forecast**
   ```bash
   python scripts/generate_forecast.py
   ```

3. **Train Models**
   ```bash
   python scripts/train_models.py --data data/demand_data.csv
   ```

4. **Backtest Models**
   ```bash
   python scripts/backtest_models.py --data data/demand_data.csv --compare
   ```

5. **Start API Server**
   ```bash
   python scripts/api_server.py --host 0.0.0.0 --port 5000
   ```

6. **Scheduled Forecast**
   ```bash
   python scripts/scheduled_forecast.py
   ```

7. **Interactive Dashboard**
   ```bash
   streamlit run scripts/dashboard.py
   ```

### Command Line Options

#### Run All Script
```bash
# Create sample data
python scripts/run_all.py --create-sample

# Use existing models (skip training)
python scripts/run_all.py --skip-training

# Skip visualizations (faster)
python scripts/run_all.py --no-viz

# Process specific item
python scripts/run_all.py --item CONN-001

# Custom data file
python scripts/run_all.py --data data/my_data.csv

# Custom config
python scripts/run_all.py --config custom_config.yaml
```

## 📊 Data Format

Your CSV file should have:
- `date` - Date column (YYYY-MM-DD)
- `Item_ID` - Item identifier
- `Quantity_Consumed` - Demand quantity
- `Site_ID` - Optional site identifier
- `Lead_Time` - Optional lead time

Example:
```csv
date,Item_ID,Quantity_Consumed,Site_ID,Lead_Time
2022-01-01,CONN-001,15,SITE-001,14
2022-01-02,CONN-001,18,SITE-001,14
...
```

## 🔧 Configuration

Edit `config.yaml` to customize:
- Forecast period (default: 30 days)
- Service level (default: 95%)
- Lead time (default: 14 days)
- Model parameters
- Alert thresholds

## 📈 Example Output

After running, you'll see:

```
================================================================================
                        DEMAND FORECASTING SYSTEM
                   Nova Corrente - Complete Run
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
```

## 🎯 Next Steps

1. **Use Your Own Data**
   - Place your CSV file in `data/` directory
   - Update `config.yaml` with your settings
   - Run: `python scripts/run_all.py --data data/your_data.csv`

2. **Customize Current Stocks**
   - Edit `data/current_stocks.json`
   - Add your item IDs and stock levels

3. **Set Up Scheduled Runs**
   - Configure cron/Airflow job
   - Use: `python scripts/scheduled_forecast.py`

4. **API Integration**
   - Start API server: `python scripts/api_server.py`
   - Integrate with your systems

## ❓ Troubleshooting

**Issue: Module not found**
```bash
# Make sure you're in project root
cd /path/to/gran_prix
pip install -r requirements.txt
```

**Issue: TensorFlow not available**
- LSTM model will be skipped automatically
- System works with ARIMA + Prophet only

**Issue: Data file not found**
```bash
# Create sample data
python scripts/run_all.py --create-sample
```

**Issue: Out of memory**
- Reduce epochs in `config.yaml`
- Process items one at a time: `--item ITEM_ID`

## 📚 More Information

- Full documentation: See `README.md`
- API documentation: See `scripts/api_server.py` docstrings
- Configuration options: See `config.yaml`

---

**Ready to forecast!** 🚀

