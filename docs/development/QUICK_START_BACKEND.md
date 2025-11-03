# 🚀 Quick Start - Backend Server

## Start Backend Server

### Option 1: Using Startup Script (Recommended)

```bash
scripts\start_backend.bat
```

### Option 2: Using Python Script

```bash
cd backend
python run_server.py
```

### Option 3: Using Uvicorn Directly

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

## Verify Backend is Running

### Check Health Endpoint

```bash
curl http://localhost:5000/health
```

Or visit: http://localhost:5000/health

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T...",
  "version": "1.0.0",
  "service": "nova-corrente-api",
  "services": {
    "database": {
      "status": "healthy",
      "connected": true
    }
  },
  "external_apis": {
    "inmet": {
      "status": "configured",
      "configured": true
    }
  }
}
```

### Check Integration Status

```bash
curl http://localhost:5000/api/v1/integration/status
```

Or visit: http://localhost:5000/api/v1/integration/status

### Check API Documentation

Visit: http://localhost:5000/docs

## Startup Sequence

When the server starts, you'll see initialization logs:

```
🚀 Starting Nova Corrente API...
Initializing all services and external API clients...
✅ Database service initialized
✅ External data service initialized
✅ Integration service initialized
✅ Feature service initialized
✅ Material service initialized
✅ Analytics service initialized
✅ Prediction service initialized
✅ INMET (Climate) API client initialized
✅ BACEN (Economic) API client initialized
✅ ANATEL (5G) API client initialized
✅ OpenWeatherMap API client initialized
✅ Expanded API integration initialized (25+ sources)
✅ Startup complete - Status: healthy
📊 Services: 7/7 healthy
🌐 External APIs: 6/6 configured
```

## Troubleshooting

### Backend Won't Start

**Issue:** Module not found errors

**Solution:**
1. Make sure you're in the `backend` directory
2. Check Python version: `python --version` (should be 3.11+)
3. Install dependencies: `pip install -r requirements.txt`

### Database Connection Fails

**Issue:** Database service shows "unhealthy"

**Solution:**
1. Check MySQL is running
2. Verify credentials in `backend/.env`
3. Test connection: `mysql -h localhost -u root -p`

### External APIs Not Working

**Issue:** External API clients show "not_configured"

**Solution:**
1. APIs work without keys (limited functionality)
2. Add API keys to `backend/.env` for full functionality
3. Check network connectivity

## Next Steps

1. ✅ Backend server running
2. ✅ All services initialized
3. ✅ Health check passing
4. ⚠️ Test with frontend
5. ⚠️ Verify data endpoints

---

**Status**: ✅ Backend Quick Start Guide Complete
**Last Updated**: November 2025


