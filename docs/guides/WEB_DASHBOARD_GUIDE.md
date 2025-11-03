# 🌐 Web Dashboard Guide

## Interactive Web Dashboard for Demand Forecasting

### Quick Start

#### Start the Web Dashboard Server
```bash
python scripts/web_dashboard_server.py
```

Access at: **http://localhost:8080**

### Features

✅ **Real-Time Data**
- Live item selection
- Dynamic forecast generation
- Interactive charts with Plotly

✅ **Inventory Management**
- Current stock levels
- Reorder point calculations
- Alert status with urgency levels

✅ **System Metrics**
- Total items available
- Data points count
- Trained models status
- System health

✅ **Interactive Charts**
- Historical demand trends
- 30-day forecasts
- Zoom and pan capabilities
- Hover tooltips

### API Endpoints

The server provides RESTful API:

- `GET /` - Main dashboard page
- `GET /api/health` - Health check
- `GET /api/items` - List all items
- `GET /api/forecast/<item_id>` - Get forecast for item
- `GET /api/inventory/<item_id>` - Get inventory metrics
- `GET /api/metrics` - System-wide metrics

### Usage

1. **Start Server**
   ```bash
   python scripts/web_dashboard_server.py --port 8080
   ```

2. **Open Browser**
   ```
   http://localhost:8080
   ```

3. **Select Item**
   - Choose item from dropdown
   - Click "Generate Forecast"
   - View forecast chart and inventory metrics

### Configuration

Customize server:
```bash
# Custom host and port
python scripts/web_dashboard_server.py --host 0.0.0.0 --port 8080

# Debug mode
python scripts/web_dashboard_server.py --debug
```

## 📊 System Monitoring

### Monitor System Health

```bash
# Single health check
python scripts/monitor_system.py

# Continuous monitoring (every 60 seconds)
python scripts/monitor_system.py --continuous

# Custom interval
python scripts/monitor_system.py --continuous --interval 30
```

### What It Checks

✅ Data availability  
✅ Trained models  
✅ Directory structure  
✅ System readiness  

### Log Analysis

```bash
# Analyze all logs
python scripts/log_analyzer.py
```

Generates:
- Forecast run summaries
- Health check history
- System performance insights

## 🎯 Complete System Overview

### Available Dashboards

1. **Web Dashboard** (Flask)
   - Interactive HTML dashboard
   - Real-time API integration
   - Location: `scripts/web_dashboard_server.py`

2. **Streamlit Dashboard**
   - Python-based interactive UI
   - Location: `scripts/dashboard.py`
   - Run: `streamlit run scripts/dashboard.py`

3. **Plotly Dash Dashboard**
   - Advanced visualizations
   - Location: `src/visualization/dash_app.py`
   - Run: `python run_dashboard.py`

### All Available Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| **Web Dashboard** | Interactive web UI | `python scripts/web_dashboard_server.py` |
| **Streamlit** | Python dashboard | `streamlit run scripts/dashboard.py` |
| **Plotly Dash** | Advanced viz | `python run_dashboard.py` |
| **Complete Run** | Full system | `python scripts/run_all.py` |
| **API Server** | REST API | `python scripts/api_server.py` |
| **Monitor** | Health checks | `python scripts/monitor_system.py` |
| **Log Analyzer** | Log analysis | `python scripts/log_analyzer.py` |

## 🚀 Quick Commands

```bash
# Start web dashboard
python scripts/web_dashboard_server.py

# Monitor system
python scripts/monitor_system.py --continuous

# Run complete system
python scripts/run_all.py

# Analyze logs
python scripts/log_analyzer.py
```

---

**All dashboards ready!** 🎉

