# 🚀 Quick Start - Nova Corrente Fullstack Dashboard

## Start Both Servers

### Windows (Automated)

```bash
scripts\start_fullstack.bat
```

### Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Verify

1. **Backend**: http://localhost:5000/health
2. **Frontend**: http://localhost:3000
3. **API Docs**: http://localhost:5000/docs

## Troubleshooting

**Backend not running?**
- Check if port 5000 is in use
- Verify Python dependencies: `pip install -r backend/requirements.txt`

**Frontend showing "Backend Offline"?**
- Start backend server first
- Check http://localhost:5000/health

See `docs/development/STARTUP_GUIDE.md` for detailed instructions.





