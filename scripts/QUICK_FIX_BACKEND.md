# 🔧 Quick Fix: Backend Startup

## Problem
Backend server won't start - scripts can't find `run_server.py` or have path issues.

## ✅ FIXED: Multiple Startup Options

### Option 1: Use Fixed Startup Script (Recommended)
```bash
scripts\start_backend.bat
```

### Option 2: Use Simple Startup Script
```bash
scripts\start_backend_simple.bat
```

### Option 3: Manual Start (Most Reliable)
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

## What Was Fixed

1. ✅ **Path Resolution** - All scripts now use absolute paths
2. ✅ **Fallback to Uvicorn** - If `run_server.py` not found, uses uvicorn directly
3. ✅ **Error Checking** - Scripts verify files exist before running
4. ✅ **Better Error Messages** - Clear messages about what's wrong

## Verify Backend is Running

### Option 1: Check Health Endpoint
```bash
curl http://localhost:5000/health
```

### Option 2: Check Script
```bash
scripts\check_backend.bat
```

### Option 3: Browser
Visit: http://localhost:5000/health
Visit: http://localhost:5000/docs

## Troubleshooting

### Backend Won't Start?

1. **Check Python:**
   ```bash
   python --version
   ```

2. **Check Dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Check Port:**
   ```bash
   netstat -ano | findstr :5000
   ```
   If port is in use, kill the process or change port in `.env`

4. **Check Logs:**
   Look at the terminal window where backend is running for errors

### Still Not Working?

**Use Direct Uvicorn Command:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

This bypasses all scripts and runs the server directly.

## Status

✅ **All startup scripts fixed**
✅ **Multiple startup options available**
✅ **Fallback to direct uvicorn if scripts fail**

---

**Quick Start**: `cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000`






