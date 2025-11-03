# 🚀 START HERE - Demand Forecasting System

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Everything!
```bash
python setup_and_run.py
```

**OR directly:**
```bash
python scripts/run_all.py
```

### Step 3: Check Results
Results are in the `reports/` directory:
- CSV reports with forecasts
- PDF reports with details  
- Visualization plots

## 📋 What Gets Created

1. **Sample Data** (if needed)
   - `data/nova_corrente_demand.csv`
   - `data/current_stocks.json`

2. **Trained Models**
   - `models/ITEM_ensemble_*.pkl`

3. **Reports**
   - `reports/forecast_report_YYYYMMDD.csv`
   - `reports/forecast_report_YYYYMMDD.pdf`
   - `reports/forecast_ITEM_YYYYMMDD.png`
   - `reports/inventory_ITEM_YYYYMMDD.png`

## 🎯 Complete System Overview

This system includes:

✅ **Core Forecasting**
- ARIMA/SARIMA models
- Prophet models
- LSTM neural networks
- Ensemble combination

✅ **Inventory Management**
- Reorder point calculation
- Safety stock computation
- Alert system

✅ **Advanced Features**
- Model persistence
- Backtesting framework
- REST API server
- Scheduled tasks
- Interactive dashboard

## 📚 Full Documentation

- **Quick Start**: See `QUICKSTART.md`
- **Run Guide**: See `RUN.md`
- **Full README**: See `README.md`

## 🔧 Common Commands

```bash
# Run everything
python setup_and_run.py

# Run with options
python scripts/run_all.py --item CONN-001
python scripts/run_all.py --skip-training
python scripts/run_all.py --no-viz

# Other scripts
python scripts/train_models.py --data data/demand_data.csv
python scripts/backtest_models.py --data data/demand_data.csv
python scripts/api_server.py
streamlit run scripts/dashboard.py
```

## ⚙️ Configuration

Edit `config.yaml` to customize:
- Forecast period
- Service level
- Lead time
- Model parameters
- Alert thresholds

## 🎉 Ready to Go!

Just run:
```bash
python setup_and_run.py
```

**That's it!** The system will:
1. Check dependencies
2. Create sample data if needed
3. Train all models
4. Generate forecasts
5. Calculate reorder points
6. Create reports
7. Generate visualizations

---

**Let's forecast!** 🚀

