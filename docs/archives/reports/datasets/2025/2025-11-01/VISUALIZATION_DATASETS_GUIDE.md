# 📊 Guia de Datasets para Visualização de Telecomunicações Brasileiras

## Nova Corrente - Demand Forecasting System

---

## 🎯 Visão Geral

Guia completo de datasets e recursos para criar visualizações interativas de dados de telecomunicações brasileiras usando D3.js e Plotly Dash.

---

## 📋 Datasets Principais para Visualização

### 1. **Anatel Mobile Accesses**

**Fonte:** Data Basis  
**URL:** https://data-basis.org/dataset/d3c86a88-d9a4-4fc0-bdec-08ab61e8f63c

**Descrição:** Acessos móveis por tecnologia (5G, 4G, 3G) e região.

**Estrutura Esperada:**
- Date: Data da medição
- Subscribers: Número de assinantes (milhões)
- Technology: Tipo de tecnologia (5G, 4G, 3G)
- State: Estado brasileiro
- Region: Região

**Uso:**
- **D3.js**: Mapas choropleth por estado
- **Plotly Dash**: Gráficos de série temporal
- **Combined**: Dashboard com mapa e gráficos

---

### 2. **Anatel Fixed Broadband**

**Fonte:** Data Basis / Anatel  
**Descrição:** Conexões de banda larga fixa por velocidade e município.

**Uso:**
- **D3.js**: Mapas de penetração por município
- **Plotly Dash**: Dashboards de velocidade média
- **Combined**: Visualização geoespacial completa

---

### 3. **Internet Aberta Forecast**

**Fonte:** Internet Aberta  
**URL:** PDF com projeções 2024-2033

**Descrição:** Projeções de longo prazo sobre tráfego de dados e adoção de 5G.

**Uso:**
- **Plotly Dash**: Gráficos de forecast
- **D3.js**: Linhas de tendência interativas

---

### 4. **Zenodo Broadband Customers**

**Fonte:** Zenodo  
**URL:** https://zenodo.org/records/10482897

**Descrição:** Dados reais de operadora brasileira com métricas de clientes.

**Uso:**
- **Plotly Dash**: Dashboards de performance
- **D3.js**: Visualizações de qualidade de rede

---

## 🗺️ Dados Geoespaciais

### 1. **Brazil States GeoJSON**

**URL:** https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.json

**Uso:** Mapas D3.js básicos

### 2. **Brazil States TopoJSON**

**URL:** https://github.com/topojson/world-atlas

**Uso:** Mapas D3.js otimizados (arquivos menores)

### 3. **Brazil Municipalities**

**URL:** https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojson-uf/

**Uso:** Mapas detalhados por município

---

## 🚀 Scripts de Busca

### Buscar Todos os Datasets de Visualização

```bash
python scripts/fetch_visualization_datasets.py --visualization --geospatial
```

### Apenas Dados Geoespaciais

```bash
python scripts/fetch_visualization_datasets.py --geospatial
```

---

## 📊 Exemplos de Uso

### D3.js - Mapa Interativo

```javascript
// Carregar dados Anatel
d3.csv("data/raw/visualization_anatel_mobile_accesses/anatel_mobile_accesses.csv")
  .then(function(data) {
    // Processar dados
    const stateData = d3.group(data, d => d.State);
    
    // Criar mapa
    d3.json("data/raw/geospatial/brazil-states.json")
      .then(function(map) {
        // Renderizar mapa com dados Anatel
        // ...
      });
  });
```

### Plotly Dash - Dashboard Temporal

```python
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Carregar dados Anatel
df = pd.read_csv('data/raw/visualization_anatel_mobile_accesses/anatel_mobile_accesses.csv')

app = dash.Dash(__name__)

fig = px.line(df, x='Date', y='Subscribers', color='Technology',
              title='Brazil Mobile Subscribers Growth')

app.layout = html.Div([
    html.H1('Brazilian Telecom Dashboard'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

---

## 🔗 Recursos e Links

### Fontes de Dados
- [Data Basis - Anatel Mobile](https://data-basis.org/dataset/d3c86a88-d9a4-4fc0-bdec-08ab61e8f63c)
- [Teleco Mobile Statistics](https://www.teleco.com.br/en/en_ncel.asp)
- [Net Data Directory](https://netdatadirectory.org/node/2336)
- [Internet Aberta Forecast](https://internetaberta.com.br/wp-content/uploads/2024/05/Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf)

### Dados Geoespaciais
- [Brazil States GeoJSON](https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.json)
- [TopoJSON World Atlas](https://github.com/topojson/world-atlas)
- [Brazil Municipalities](https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojson-uf/)

### Tutoriais
- [D3.js Tutorial](https://www.freecodecamp.org/news/d3js-tutorial-data-visualization-for-beginners/)
- [D3.js Map Explained](https://www.d3noob.org/2013/03/a-simple-d3js-map-explained.html)
- [Plotly Dash Tutorial](https://dash.plotly.com/tutorial)
- [Dash in 20 Minutes](https://dash.plotly.com/tutorial)

### Exemplos
- [D3.js Gallery](https://observablehq.com/@d3/gallery)
- [Dash Examples](https://plotly.com/examples/)
- [Dash World Cell Towers](https://github.com/plotly/dash-world-cell-towers)
- [Observable Brazil Map](https://observablehq.com/@arbezerra/brazil-map)

---

**Status:** ✅ **GUIA DE DATASETS PARA VISUALIZAÇÃO COMPLETO**

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

