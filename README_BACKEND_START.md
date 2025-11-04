# 🚀 Start Backend Server

## Quick Start

### Option 1: Automated Script (Windows)

```bash
scripts\start_backend.bat
```

### Option 2: Python Script

```bash
cd backend
python run_server.py
```

### Option 3: Uvicorn Direct

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

## Verify It's Running

1. **Check Health:**
   ```bash
   curl http://localhost:5000/health
   ```
   Or visit: http://localhost:5000/health

2. **Check Integration Status:**
   ```bash
   curl http://localhost:5000/api/v1/integration/status
   ```

3. **Check API Docs:**
   Visit: http://localhost:5000/docs

## Expected Output

When the server starts successfully, you'll see:
- ✅ All services initialized
- ✅ All external API clients configured
- ✅ Server running on http://127.0.0.1:5000

## Troubleshooting

**Backend won't start?**
- Check Python is installed: `python --version`
- Check dependencies: `pip install -r requirements.txt`
- Check database connection in `.env`

**Connection refused?**
- Verify server is running on port 5000
- Check if port is in use: `netstat -ano | findstr :5000`
- Check firewall settings

## Full Documentation

See `docs/development/BACKEND_INTEGRATION_GUIDE.md` for complete integration details.





