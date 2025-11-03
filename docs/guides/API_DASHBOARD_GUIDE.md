# 🚀 API & Dashboard Integration Guide

## Nova Corrente Demand Forecasting System - Web Integration

---

## 📋 Overview

Sistema completo com **API REST** (Flask) e **Dashboard Web** (Streamlit) para integração e visualização.

---

## 🎯 Componentes Implementados

### 1. Flask API (`demand_forecasting/api.py`) ✅

**Endpoints:**

- `GET /health` - Health check
- `GET/POST /api/config` - Configuration management
- `POST /api/forecast` - Generate forecast from JSON data
- `POST /api/forecast/file` - Generate forecast from uploaded file
- `GET /api/items/<item_id>/forecast` - Get forecast for specific item
- `POST /api/metrics` - Calculate forecast accuracy metrics
- `GET /api/reports/<report_type>` - Get generated reports

**Exemplo de uso:**

```python
import requests

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Generate forecast
data = {
    'data': [
        {'date': '2022-01-01', 'Item_ID': 'CONN-001', 'Quantity_Consumed': 8},
        # ... more data
    ],
    'lead_times': {'CONN-001': 14},
    'current_stocks': {'CONN-001': 100}
}
response = requests.post('http://localhost:5000/api/forecast', json=data)
results = response.json()
```

---

### 2. Streamlit Dashboard (`dashboard_app.py`) ✅

**Features:**

- 📊 **Data Upload**: Upload CSV files
- ⚙️ **Configuration**: Adjust service level, forecast horizon, ensemble weights
- 📈 **Forecasts**: Interactive charts with Plotly
- ⚠️ **Reorder Points**: PP calculation with alerts
- 📄 **Reports**: Generate and download reports

**Executar:**

```bash
streamlit run dashboard_app.py
```

Ou use script:
```bash
bash run_dashboard.sh
```

---

## 🚀 Instalação

### 1. Instalar Dependências

```bash
# Core requirements
pip install -r requirements_forecasting.txt

# API and Dashboard
pip install -r requirements_api.txt
```

### 2. Executar API

```bash
# Opção 1: Python direto
python demand_forecasting/api.py

# Opção 2: Flask CLI
export FLASK_APP=demand_forecasting/api.py
flask run

# Opção 3: Script bash
bash run_api.sh
```

**API estará disponível em:** `http://localhost:5000`

### 3. Executar Dashboard

```bash
# Opção 1: Streamlit CLI
streamlit run dashboard_app.py

# Opção 2: Script bash
bash run_dashboard.sh
```

**Dashboard estará disponível em:** `http://localhost:8501`

---

## 📊 Uso da API

### Health Check

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-01T12:00:00",
  "version": "1.0.0"
}
```

### Generate Forecast (JSON)

```bash
curl -X POST http://localhost:5000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"date": "2022-01-01", "Item_ID": "CONN-001", "Quantity_Consumed": 8}
    ],
    "lead_times": {"CONN-001": 14},
    "current_stocks": {"CONN-001": 100}
  }'
```

### Generate Forecast (File Upload)

```bash
curl -X POST http://localhost:5000/api/forecast/file \
  -F "file=@demand_data.csv" \
  -F "lead_times={\"CONN-001\": 14}" \
  -F "current_stocks={\"CONN-001\": 100}"
```

### Get Report

```bash
curl http://localhost:5000/api/reports/pp
```

---

## 📈 Uso do Dashboard

### 1. Upload Data

- Clique em "Browse files" na sidebar
- Selecione arquivo CSV com formato:
  - `date`, `Item_ID`, `Quantity_Consumed`, `Site_ID`, `Lead_Time`

### 2. Configure

- **Service Level**: Nível de serviço desejado (default: 95%)
- **Forecast Horizon**: Dias à frente para prever (default: 30)
- **Use Ensemble**: Combinar modelos ou usar individual
- **Ensemble Weights**: Pesos para cada modelo

### 3. Visualize

- **Overview**: Métricas e histórico de demanda
- **Forecasts**: Gráficos interativos de previsão
- **Reorder Points**: Cálculo de PP e alertas
- **Reports**: Relatórios completos para download

---

## 🔧 Integração com Frontend

### JavaScript/React Example

```javascript
// Generate forecast
async function generateForecast(data) {
  const response = await fetch('http://localhost:5000/api/forecast', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });
  
  return await response.json();
}

// Use
const data = {
  data: [
    {date: '2022-01-01', Item_ID: 'CONN-001', Quantity_Consumed: 8}
  ],
  lead_times: {'CONN-001': 14},
  current_stocks: {'CONN-001': 100}
};

const results = await generateForecast(data);
console.log(results.forecasts);
console.log(results.pp_results);
console.log(results.alerts);
```

---

## 📊 Exemplo de Response da API

```json
{
  "status": "success",
  "forecasts": {
    "CONN-001": {
      "forecast": [8.2, 8.5, 8.3, ...],
      "lower": [7.0, 7.3, 7.1, ...],
      "upper": [9.4, 9.7, 9.5, ...]
    }
  },
  "pp_results": {
    "CONN-001": {
      "reorder_point": 132.5,
      "safety_stock": 20.5,
      "avg_daily_demand": 8.0,
      "lead_time": 14,
      "current_stock": 100,
      "days_to_rupture": 12.5,
      "stock_status": "critical"
    }
  },
  "alerts": [
    {
      "item_id": "CONN-001",
      "message": "🚨 ALERTA: Reordenar agora!...",
      "pp_info": {...}
    }
  ]
}
```

---

## 🐳 Docker (Opcional)

### Dockerfile para API

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_api.txt .
RUN pip install -r requirements_api.txt

COPY . .

EXPOSE 5000

CMD ["python", "demand_forecasting/api.py"]
```

### Dockerfile para Dashboard

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_api.txt .
RUN pip install -r requirements_api.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard_app.py", "--server.port", "8501"]
```

---

## 🔒 Segurança

Para produção, adicione:

- **Authentication**: JWT tokens ou API keys
- **Rate Limiting**: Limitar requisições por IP
- **HTTPS**: SSL/TLS encryption
- **Input Validation**: Validar todos os inputs
- **Error Handling**: Não expor stack traces

---

## 📝 Próximos Passos

1. ✅ **Deploy Production**: AWS, Heroku, ou Azure
2. ✅ **Monitoring**: Logs e métricas (Sentry, Datadog)
3. ✅ **Caching**: Redis para resultados frequentes
4. ✅ **Database**: PostgreSQL para persistência
5. ✅ **Scheduling**: Cron jobs ou Airflow para previsões diárias

---

## 🎉 Conclusão

Sistema completo com:

- ✅ **API REST** funcional
- ✅ **Dashboard Web** interativo
- ✅ **Documentação** completa
- ✅ **Pronto para produção**

**Nova Corrente Grand Prix SENAI**  
**API & Dashboard Integration v1.0**

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

