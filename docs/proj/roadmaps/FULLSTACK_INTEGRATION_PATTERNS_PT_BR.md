# 🎨 FULLSTACK INTEGRATION PATTERNS
## Nova Corrente - Backend + Frontend Integration

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Patterns de Integração Completos

---

## 📋 ÍNDICE

1. [Arquitetura Fullstack](#arquitetura)
2. [API Design Patterns](#api-design)
3. [Frontend Integration](#frontend)
4. [Real-time Updates](#realtime)
5. [Caching Strategy](#caching)
6. [Authentication & Security](#security)
7. [Error Handling](#error-handling)

---

<a name="arquitetura"></a>

## 1. 🏗️ ARQUITETURA FULLSTACK

### 1.1 Stack Completo

```
┌─────────────────────────────────────┐
│   Next.js Frontend (React/TS)       │
│   - Dashboard                       │
│   - Visualizations (Chart.js)       │
│   - Real-time updates (WebSocket)   │
└──────────────┬──────────────────────┘
               │ HTTP/REST + WebSocket
┌──────────────▼──────────────────────┐
│   FastAPI Backend (Python)          │
│   - /api/v1/forecasts               │
│   - /api/v1/inventory               │
│   - /api/v1/metrics                 │
│   - /ws/forecasts (WebSocket)       │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐  ┌─────▼──────┐
│ Redis Cache │  │ Databricks  │
│ (Hot data)  │  │ (Gold Layer)│
└─────────────┘  └─────────────┘
```

---

### 1.2 Component Architecture

**Backend (FastAPI):**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── forecasts.py
│   │       ├── inventory.py
│   │       ├── metrics.py
│   │       └── websocket.py
│   ├── core/
│   │   ├── database.py
│   │   ├── cache.py
│   │   └── config.py
│   ├── schemas/
│   │   └── forecast.py
│   └── main.py
```

**Frontend (Next.js):**
```
frontend/
├── src/
│   ├── app/
│   │   ├── dashboard/
│   │   │   ├── forecasts/
│   │   │   ├── inventory/
│   │   │   └── analytics/
│   │   └── api/
│   ├── components/
│   │   ├── charts/
│   │   ├── tables/
│   │   └── alerts/
│   ├── lib/
│   │   ├── api.ts
│   │   └── websocket.ts
│   └── hooks/
│       ├── useForecasts.ts
│       └── useRealtime.ts
```

---

<a name="api-design"></a>

## 2. 🔌 API DESIGN PATTERNS

### 2.1 RESTful API Design

**FastAPI Endpoints:**

```python
# backend/app/api/v1/forecasts.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date

router = APIRouter()

@router.get("/forecasts", response_model=List[ForecastResponse])
async def get_forecasts(
    item_id: Optional[str] = Query(None, description="Filter by item ID"),
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, le=1000, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache)
):
    """
    Get forecasts with filtering and pagination
    
    - **item_id**: Filter by specific item
    - **start_date**: Start date range
    - **end_date**: End date range
    - **category**: Filter by category
    - **limit**: Max results (1-1000)
    - **offset**: Pagination offset
    """
    # Build cache key
    cache_key = f"forecasts:{item_id}:{start_date}:{end_date}:{category}:{limit}:{offset}"
    
    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Query from Databricks
    forecasts = query_forecasts(item_id, start_date, end_date, category, limit, offset)
    
    # Cache result
    cache.set(cache_key, forecasts, ttl=1800)
    
    return forecasts

@router.get("/forecasts/{item_id}")
async def get_forecast_by_item(
    item_id: str,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get forecasts for specific item"""
    forecasts = query_forecasts_by_item(item_id, days)
    return forecasts

@router.get("/forecasts/summary")
async def get_forecast_summary(
    period: str = Query("30d", regex="^(7d|30d|90d|1y)$"),
    category: Optional[str] = None
):
    """Get forecast summary metrics"""
    summary = calculate_forecast_summary(period, category)
    return summary
```

---

### 2.2 Response Schemas

```python
# backend/app/schemas/forecast.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ForecastResponse(BaseModel):
    """Forecast response schema"""
    forecast_id: int
    item_id: str
    item_name: str
    category: str
    date: date
    forecasted_demand: float = Field(..., description="Forecasted demand")
    actual_demand: Optional[float] = Field(None, description="Actual demand (if available)")
    mape: Optional[float] = Field(None, description="MAPE percentage")
    model_type: str = Field(..., description="Model used (prophet, arima, lstm, ensemble)")
    accuracy_level: str = Field(..., description="Accuracy level (EXCELLENT, GOOD, ACCEPTABLE, POOR)")
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "forecast_id": 12345,
                "item_id": "CONN-001",
                "item_name": "Connector Optical",
                "category": "connectors",
                "date": "2025-11-01",
                "forecasted_demand": 8.5,
                "actual_demand": 8.2,
                "mape": 3.66,
                "model_type": "ensemble",
                "accuracy_level": "EXCELLENT",
                "created_at": "2025-11-01T10:00:00Z"
            }
        }
```

---

<a name="frontend"></a>

## 3. 💻 FRONTEND INTEGRATION

### 3.1 API Client (TypeScript)

```typescript
// frontend/src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export interface Forecast {
  forecast_id: number;
  item_id: string;
  item_name: string;
  category: string;
  date: string;
  forecasted_demand: number;
  actual_demand?: number;
  mape?: number;
  model_type: string;
  accuracy_level: string;
  created_at: string;
}

export interface ForecastQuery {
  item_id?: string;
  start_date?: string;
  end_date?: string;
  category?: string;
  limit?: number;
  offset?: number;
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async getForecasts(query?: ForecastQuery): Promise<Forecast[]> {
    const params = new URLSearchParams();
    
    if (query?.item_id) params.append('item_id', query.item_id);
    if (query?.start_date) params.append('start_date', query.start_date);
    if (query?.end_date) params.append('end_date', query.end_date);
    if (query?.category) params.append('category', query.category);
    if (query?.limit) params.append('limit', query.limit.toString());
    if (query?.offset) params.append('offset', query.offset.toString());

    const response = await fetch(`${this.baseUrl}/api/v1/forecasts?${params}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return response.json();
  }

  async getForecastByItem(itemId: string, days: number = 30): Promise<Forecast[]> {
    const response = await fetch(
      `${this.baseUrl}/api/v1/forecasts/${itemId}?days=${days}`
    );
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return response.json();
  }

  async getForecastSummary(period: string = '30d', category?: string): Promise<any> {
    const params = new URLSearchParams();
    params.append('period', period);
    if (category) params.append('category', category);

    const response = await fetch(
      `${this.baseUrl}/api/v1/forecasts/summary?${params}`
    );
    
    return response.json();
  }
}

export const apiClient = new ApiClient();
```

---

### 3.2 React Hooks

```typescript
// frontend/src/hooks/useForecasts.ts
import { useState, useEffect } from 'react';
import { apiClient, Forecast, ForecastQuery } from '@/lib/api';

export function useForecasts(query?: ForecastQuery) {
  const [forecasts, setForecasts] = useState<Forecast[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchForecasts() {
      try {
        setLoading(true);
        const data = await apiClient.getForecasts(query);
        setForecasts(data);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    }

    fetchForecasts();
  }, [JSON.stringify(query)]);

  return { forecasts, loading, error };
}

export function useForecastByItem(itemId: string, days: number = 30) {
  const [forecast, setForecast] = useState<Forecast[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchForecast() {
      try {
        setLoading(true);
        const data = await apiClient.getForecastByItem(itemId, days);
        setForecast(data);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    }

    if (itemId) {
      fetchForecast();
    }
  }, [itemId, days]);

  return { forecast, loading, error };
}
```

---

### 3.3 React Components

```typescript
// frontend/src/components/dashboard/ForecastDashboard.tsx
'use client';

import { useForecasts } from '@/hooks/useForecasts';
import { ForecastChart } from './ForecastChart';
import { ForecastTable } from './ForecastTable';

export function ForecastDashboard() {
  const { forecasts, loading, error } = useForecasts({
    limit: 100,
    offset: 0
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="dashboard">
      <h1>Forecast Dashboard</h1>
      <ForecastChart data={forecasts} />
      <ForecastTable data={forecasts} />
    </div>
  );
}
```

---

<a name="realtime"></a>

## 4. ⚡ REAL-TIME UPDATES

### 4.1 WebSocket Integration

**Backend WebSocket:**

```python
# backend/app/api/v1/websocket.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.active_connections.remove(connection)

manager = ConnectionManager()

@app.websocket("/ws/forecasts")
async def websocket_forecasts(websocket: WebSocket):
    """WebSocket endpoint for real-time forecast updates"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Send latest forecasts
            forecasts = get_latest_forecasts()
            await websocket.send_json({
                "type": "forecast_update",
                "data": forecasts,
                "timestamp": datetime.now().isoformat()
            })
            
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

**Frontend WebSocket Hook:**

```typescript
// frontend/src/hooks/useRealtime.ts
import { useEffect, useState } from 'react';

export function useRealtimeForecasts() {
  const [forecasts, setForecasts] = useState<any[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:5000/ws/forecasts');

    ws.onopen = () => {
      setConnected(true);
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'forecast_update') {
        setForecasts(message.data);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      setConnected(false);
    };

    return () => {
      ws.close();
    };
  }, []);

  return { forecasts, connected };
}
```

---

<a name="caching"></a>

## 5. 💾 CACHING STRATEGY

### 5.1 Multi-Layer Caching

```
Frontend (React Query) → Backend (FastAPI) → Redis → Databricks (Gold Layer)
     (Client cache)           (API cache)      (Hot data)      (Source of truth)
```

**Frontend Caching (React Query):**

```typescript
// frontend/src/lib/react-query.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
});

// Usage
import { useQuery } from '@tanstack/react-query';

export function useForecasts(query?: ForecastQuery) {
  return useQuery({
    queryKey: ['forecasts', query],
    queryFn: () => apiClient.getForecasts(query),
    staleTime: 5 * 60 * 1000,
  });
}
```

**Backend Caching (Redis):**

```python
# backend/app/core/cache.py
from functools import wraps
import redis
import json

def cache_response(ttl: int = 3600):
    """Decorator to cache API responses"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Check Redis
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            redis_client.setex(cache_key, ttl, json.dumps(result, default=str))
            
            return result
        return wrapper
    return decorator

# Usage
@cache_response(ttl=1800)  # 30 minutes
async def get_forecasts(...):
    # API logic
    pass
```

---

<a name="security"></a>

## 6. 🔒 AUTHENTICATION & SECURITY

### 6.1 JWT Authentication

**Backend:**

```python
# backend/app/core/auth.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Protected endpoint
@router.get("/forecasts")
async def get_forecasts(
    token: dict = Depends(verify_token),
    ...
):
    # API logic
    pass
```

**Frontend:**

```typescript
// frontend/src/lib/auth.ts
export class AuthService {
  private token: string | null = null;

  async login(email: string, password: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    this.token = data.access_token;
    localStorage.setItem('token', this.token);
  }

  getToken(): string | null {
    return this.token || localStorage.getItem('token');
  }

  async authenticatedFetch(url: string, options: RequestInit = {}) {
    const token = this.getToken();
    
    return fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
      },
    });
  }
}
```

---

<a name="error-handling"></a>

## 7. ⚠️ ERROR HANDLING

### 7.1 Backend Error Handling

```python
# backend/app/core/exceptions.py
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class APIException(HTTPException):
    """Custom API exception"""
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

@app.exception_handler(APIException)
async def api_exception_handler(request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "error_code": exc.error_code,
            "timestamp": datetime.now().isoformat()
        }
    )
```

### 7.2 Frontend Error Handling

```typescript
// frontend/src/lib/error-handler.ts
export class ErrorHandler {
  static handle(error: Error): void {
    console.error('API Error:', error);
    
    // Show user-friendly message
    if (error.message.includes('401')) {
      // Redirect to login
      window.location.href = '/login';
    } else if (error.message.includes('500')) {
      // Show server error message
      alert('Server error. Please try again later.');
    } else {
      // Show generic error
      alert('An error occurred. Please try again.');
    }
  }
}
```

---

## ✅ CHECKLIST DE INTEGRAÇÃO

- [ ] API endpoints implementados
- [ ] Response schemas definidos
- [ ] Frontend API client criado
- [ ] React hooks implementados
- [ ] Components criados
- [ ] WebSocket funcionando
- [ ] Caching configurado (multi-layer)
- [ ] Authentication implementada
- [ ] Error handling robusto
- [ ] Testes automatizados

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Fullstack Integration Patterns Completos

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**






