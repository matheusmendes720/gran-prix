# 🚀 Startup Guide - Nova Corrente Fullstack Dashboard

## Quick Start

### Option 1: Automated Startup (Windows)

Run the automated startup script:

```bash
scripts\start_fullstack.bat
```

This will:
1. Start the FastAPI backend server on `http://localhost:5000`
2. Wait 5 seconds for backend to initialize
3. Start the Next.js frontend on `http://localhost:3000`

### Option 2: Manual Startup

#### Step 1: Start Backend API Server

Open a terminal in the `backend` directory:

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

Or using Python directly:

```bash
cd backend
python -m app.main
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend:**
- API: http://localhost:5000/docs (Swagger UI)
- Health: http://localhost:5000/health

#### Step 2: Start Frontend Development Server

Open a **new** terminal in the `frontend` directory:

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
▲ Next.js 14.2.33
- Local:        http://localhost:3000
✓ Ready in 6.6s
```

**Verify Frontend:**
- Dashboard: http://localhost:3000
- ML Features: http://localhost:3000/features/temporal

## Troubleshooting

### Backend Not Starting

**Issue**: `ERR_CONNECTION_REFUSED` on `http://localhost:5000`

**Solutions:**
1. **Check if backend is running:**
   ```bash
   curl http://localhost:5000/health
   # Or visit: http://localhost:5000/health in browser
   ```

2. **Check if port 5000 is already in use:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # Linux/Mac
   lsof -i :5000
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install fastapi uvicorn[standard]
   ```

4. **Check Python environment:**
   ```bash
   python --version  # Should be 3.8+
   python -m pip list | grep fastapi
   ```

### Frontend Not Connecting to Backend

**Issue**: Frontend shows "Backend Offline" indicator

**Solutions:**
1. **Verify backend is running:**
   - Check terminal where backend is running
   - Visit http://localhost:5000/health

2. **Check CORS settings:**
   - Backend should allow `http://localhost:3000`
   - Check `backend/app/config.py` for `CORS_ORIGINS`

3. **Check API base URL:**
   - Frontend uses `http://localhost:5000` by default
   - Verify `frontend/src/lib/api.ts` has correct `baseURL`

4. **Check browser console:**
   - Open DevTools (F12)
   - Check Network tab for failed requests
   - Check Console for error messages

### SSR Errors

**Issue**: `ReferenceError: document is not defined`

**Solution:**
- Components using browser APIs must have `'use client'` directive
- Use `useEffect` for browser-only code
- Check if `typeof window !== 'undefined'` before accessing `document`

## Development Workflow

### 1. Start Both Servers

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload --port 5000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 2. Monitor Console Logs

**Backend Logs:**
- Watch terminal for API requests
- Check FastAPI automatic reload logs

**Frontend Logs:**
- Browser DevTools Console
- Next.js terminal output
- BackendStatus component indicator

### 3. Debug Issues

**Backend Debugging:**
- Visit http://localhost:5000/docs for interactive API docs
- Check FastAPI logs in terminal
- Use Python debugger: `python -m pdb -m uvicorn app.main:app`

**Frontend Debugging:**
- Chrome DevTools (F12)
- React DevTools extension
- Next.js error overlay

## Environment Variables

### Backend (.env)

Create `backend/.env`:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nova_corrente
DB_USER=root
DB_PASSWORD=your_password

# API
API_HOST=127.0.0.1
API_PORT=5000
API_RELOAD=true

# CORS
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

### Frontend (.env.local)

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Testing the Setup

### 1. Test Backend Health

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T...",
  "version": "1.0.0",
  "service": "nova-corrente-api"
}
```

### 2. Test Frontend Connection

1. Open http://localhost:3000
2. Check for "Backend Offline" indicator (top-right)
3. If backend is running, indicator should not appear
4. Navigate to http://localhost:3000/features/economic
5. Should see charts (may show empty data if database not populated)

### 3. Test API Endpoint

Visit http://localhost:5000/api/v1/features/economic

Expected: JSON response with feature data or empty array

## Common Commands

### Backend

```bash
# Start backend
cd backend
python -m uvicorn app.main:app --reload --port 5000

# Start with custom host
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# Check backend status
curl http://localhost:5000/health

# View API docs
# Open: http://localhost:5000/docs
```

### Frontend

```bash
# Start frontend
cd frontend
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type check
npm run type-check

# Lint
npm run lint
```

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │    Backend      │
│  Next.js:3000   │────────▶│  FastAPI:5000   │
│                 │  HTTP   │                 │
│  - React        │◀────────│  - FastAPI      │
│  - TypeScript   │         │  - Python       │
│  - Recharts     │         │  - MySQL        │
└─────────────────┘         └─────────────────┘
```

## Next Steps

1. ✅ Backend and Frontend running
2. ✅ Verify connection (BackendStatus indicator)
3. ✅ Navigate to ML Features pages
4. ⚠️ Populate database with feature data
5. ⚠️ Test chart visualizations
6. ⚠️ Verify API endpoints returning data

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review console logs (browser and terminal)
3. Verify both servers are running
4. Check network requests in browser DevTools
5. Review backend FastAPI logs

---

**Status**: ✅ Startup Guide Complete
**Last Updated**: November 2025







