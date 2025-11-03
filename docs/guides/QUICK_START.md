# 🚀 QUICK START GUIDE

## Nova Corrente Dashboard - Launch Instructions

### 📋 Prerequisites
✅ All dependencies installed  
✅ Training data available  
✅ Python environment ready  

---

## 🎯 EASIEST LAUNCH METHODS

### Method 1: Batch File (Windows)
```bash
# Double-click this file:
launch_dashboard.bat
```

### Method 2: Command Line
```bash
# In project directory:
python run_dashboard.py --port 8050
```

### Method 3: Custom Port
```bash
# Use different port (e.g., 8080):
python run_dashboard.py --port 8080
```

---

## 🌐 ACCESS YOUR DASHBOARD

Once running, open in browser:
- **Default:** http://localhost:8050
- **Network:** http://0.0.0.0:8050

---

## 📊 WHAT YOU'LL SEE

### Dashboard Features
- ✅ 7 types of visualizations
- ✅ 119,747 records ready
- ✅ Brazilian telecom data
- ✅ Network quality metrics
- ✅ Interactive charts

### Available Charts
1. Time-Series Analysis
2. Distribution Histograms
3. External Factors Heatmaps
4. Seasonal Patterns
5. Forecast Comparisons
6. Network Quality (Latency, Jitter, Packet Loss)
7. Brazilian State Maps

---

## 🗺️ D3.js INTERACTIVE MAP

Separate HTML file:
```
src/visualization/d3_map.html
```

**Open in browser:** Double-click the file

---

## ❓ TROUBLESHOOTING

### Dashboard Won't Start
```bash
# Check dependencies
pip install -r requirements.txt

# Verify data exists
python -c "import os; print(os.path.exists('data/training/CONN-001_full.csv'))"

# Check for errors
python run_dashboard.py 2>&1 | tee dashboard.log
```

### Port Already in Use
```bash
# Find what's using port 8050
netstat -ano | findstr :8050

# Use different port
python run_dashboard.py --port 8051
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 📚 DOCUMENTATION

- **Complete Guide:** `docs/VISUALIZATION_GUIDE.md`
- **Implementation:** `docs/VISUALIZATION_IMPLEMENTATION_SUMMARY.md`
- **Launch Status:** `DASHBOARD_LAUNCH_COMPLETE.md`
- **Benchmark:** `docs/BENCHMARK_REGISTRY.md`

---

## ✅ SUCCESS INDICATORS

When dashboard is running:
- ✅ Terminal shows "Running on http://127.0.0.1:8050"
- ✅ Browser loads dashboard interface
- ✅ Can select items from dropdown
- ✅ Charts render successfully

---

## 🎉 YOU'RE READY!

**Launch the dashboard and explore your data!**

**Nova Corrente Grand Prix SENAI**  
**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

