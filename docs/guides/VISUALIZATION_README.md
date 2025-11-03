# 📊 Sistema de Visualização Nova Corrente

## Início Rápido

### 1️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Executar dashboard
```bash
python run_dashboard.py
```
Acesse: **http://localhost:8050**

### 3️⃣ Visualizar mapa D3.js
Abra: **`src/visualization/d3_map.html`** no navegador

---

## 📁 Estrutura dos Arquivos

```
gran_prix/
├── src/
│   └── visualization/
│       ├── __init__.py          # Módulo de visualização
│       ├── dash_app.py          # Dashboard Plotly Dash principal
│       └── d3_map.html          # Mapa interativo D3.js
├── docs/
│   └── VISUALIZATION_GUIDE.md   # Guia completo de uso
├── run_dashboard.py             # Script de execução rápida
├── requirements.txt             # Dependências atualizadas
└── VISUALIZATION_README.md      # Este arquivo
```

---

## 🎯 Funcionalidades

### Dashboard Plotly Dash
- ✅ Séries temporais interativas
- ✅ Análise de padrões (semanal, mensal, horário)
- ✅ Correlações com fatores externos
- ✅ Previsões simuladas
- ✅ Estatísticas descritivas
- ✅ Interface responsiva

### Mapa D3.js
- ✅ Mapa cloroplético do Brasil
- ✅ Dados de 27 estados
- ✅ 4 métricas: Assinantes, Penetração, Torres, Cobertura 5G
- ✅ Hover e tooltips
- ✅ Painel de estatísticas
- ✅ Legendas dinâmicas

---

## 📊 Visualizações Disponíveis

| Tipo | Descrição | Uso |
|------|-----------|-----|
| **Série Temporal** | Demanda ao longo do tempo | Análise de tendências |
| **Distribuição** | Histograma de frequências | Identificar padrões |
| **Fatores Externos** | Temperatura, câmbio, etc. | Correlações |
| **Padrões** | Semanal, mensal, horário | Sazonalidades |
| **Previsão** | Forecast 30 dias | Planejamento futuro |
| **Mapa** | Telecom por estado | Análise geográfica |

---

## 🚀 Comandos Úteis

```bash
# Executar dashboard em porta customizada
python run_dashboard.py --port 8080

# Permitir acesso externo
python run_dashboard.py --host 0.0.0.0

# Modo produção (sem debug)
python run_dashboard.py --no-debug

# Servidor local para mapa D3.js
python -m http.server 8000
```

---

## 📈 Exemplos de Uso

### Python API

```python
from src.visualization.dash_app import NovaCorrenteDashboard

# Criar e executar dashboard
dashboard = NovaCorrenteDashboard()
dashboard.run(port=8050)

# Carregar dados customizados
import pandas as pd
df = pd.read_csv('data/training/CONN-001_full.csv')
dashboard = NovaCorrenteDashboard(data={'CONN-001': df})
```

### JavaScript (Mapa D3.js)

```javascript
// Modificar dados
const telecomData = {
    "São Paulo": { subscribers: 20000, penetration: 90, ... },
    // adicione mais estados
};

// Atualizar cores
const colorScale = d3.scaleLinear()
    .domain([0, 100])
    .range(['#fef0d9', '#b30000']);
```

---

## 🔗 Links Úteis

- 📖 [Guia Completo](docs/VISUALIZATION_GUIDE.md)
- 📚 [Plotly Dash Docs](https://dash.plotly.com/)
- 🗺️ [D3.js Gallery](https://observablehq.com/@d3/gallery)
- 🇧🇷 [Anatel Datasets](https://www.anatel.gov.br/)

---

## ✅ Status

**Sistema Completo e Funcional**
- Dashboard Plotly Dash: ✅ Implementado
- Mapa D3.js: ✅ Implementado  
- Dependências: ✅ Atualizadas
- Documentação: ✅ Completa

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

