# 🚀 Quick Start Guide

## ⚡ **Fast Track to Running Everything**

### **Step 1: Start Backend (30 seconds)**
```bash
cd backend
python run_server.py
```

**Wait for:** `Uvicorn running on http://127.0.0.1:5000`

---

### **Step 2: Verify Backend (10 seconds)**
```bash
# In new terminal/PowerShell
curl http://localhost:5000/health
```

**Expected:** `{"status": "healthy", ...}`

---

### **Step 3: Start Frontend (30 seconds)**
```bash
# In new terminal
cd frontend
npm run dev
```

**Wait for:** `Ready on http://localhost:3000`

---

### **Step 4: Open Browser (5 seconds)**
```
http://localhost:3000/features/temporal
```

**Expected:** Page loads with chart showing temporal features

---

### **Step 5: Test More Pages (2 minutes)**
Navigate to:
- `/features/climate`
- `/features/economic`
- `/features/5g`
- `/features/hierarchical`

**Expected:** Each page loads with its respective chart

---

## ✅ **Quick Verification Checklist:**

- [ ] Backend running on port 5000
- [ ] Health endpoint returns "healthy"
- [ ] Frontend running on port 3000
- [ ] At least one feature page loads
- [ ] Chart displays data (or shows error gracefully)

---

## 🔧 **Quick Troubleshooting:**

**Backend not starting?**
```bash
# Kill old processes
Get-Process python | Stop-Process -Force

# Try direct uvicorn
cd backend
python -m uvicorn app.main:app --reload --port 5000
```

**Frontend shows "Backend Offline"?**
- Check backend is running: `http://localhost:5000/health`
- Check port 5000 is not blocked
- Restart backend

**Charts not showing data?**
- Check browser console for errors
- Verify backend endpoint returns data
- Check network tab for failed requests

---

## 📊 **Quick Status Check:**

```bash
# Check backend
Invoke-WebRequest -Uri http://localhost:5000/health

# Check frontend
Invoke-WebRequest -Uri http://localhost:3000
```

---

**Everything should work now! 🎉**





