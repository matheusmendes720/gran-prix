# 📊 Guia de Visualização - Nova Corrente Telecom

## Visão Geral

Este guia descreve o sistema completo de visualização para dados brasileiros de telecomunicações, incluindo dashboards Plotly Dash interativos e mapas D3.js.

---

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

Isso instala:
- `dash` - Framework para dashboards web
- `plotly` - Bibliotecas de visualização interativa
- `dash-bootstrap-components` - Componentes de UI profissionais

### 2. Executar Dashboard Plotly Dash

```bash
python run_dashboard.py
```

O dashboard estará disponível em: **http://localhost:8050**

### 3. Visualizar Mapa D3.js Interativo

Abra o arquivo `src/visualization/d3_map.html` em um navegador web moderno.

---

## 📊 Componentes do Sistema

### 1. Dashboard Plotly Dash (`src/visualization/dash_app.py`)

**Características:**
- ✅ Visualizações interativas de séries temporais
- ✅ Análise de fatores externos (temperatura, câmbio, inflação)
- ✅ Padrões temporais (semanal, mensal, horário)
- ✅ Previsões simuladas com intervalos de confiança
- ✅ Estatísticas descritivas em tempo real
- ✅ Interface responsiva e moderna

**Funcionalidades:**

#### a) Séries Temporais
- Evolução da demanda ao longo do tempo
- Overlay de fatores externos (temperatura, precipitação, câmbio)
- Marcação automática de feriados
- Zoom e pan interativos

#### b) Análise de Padrões
- Padrão semanal (segunda a domingo)
- Padrão mensal (Janeiro a Dezembro)
- Padrão horário (se disponível)
- Identificação de sazonalidades

#### c) Previsões Simuladas
- Modelo linear para demonstração
- Intervalos de confiança (90%)
- Extensão de 30 dias no futuro
- Integração futura com ARIMA/Prophet/LSTM

#### d) Distribuições e Correlações
- Histogramas de frequência
- Matriz de correlação entre variáveis
- Análise de tendências com médias móveis

**Uso:**

```python
from src.visualization.dash_app import NovaCorrenteDashboard

# Criar instância do dashboard
dashboard = NovaCorrenteDashboard()

# Executar (por padrão na porta 8050)
dashboard.run(port=8050, debug=True)
```

**Interface:**
- Dropdown para seleção de Item ID
- Dropdown para tipo de visualização
- Checkboxes para fatores externos
- Métricas principais no topo
- Gráficos principais e secundários

---

### 2. Mapa D3.js Interativo (`src/visualization/d3_map.html`)

**Características:**
- ✅ Mapa cloroplético do Brasil
- ✅ Dados de telecomunicações por estado
- ✅ Interatividade com hover e click
- ✅ Legendas dinâmicas
- ✅ Tooltips informativos
- ✅ Painel de estatísticas

**Dados Visualizados:**

| Métrica | Descrição | Intervalo |
|---------|-----------|-----------|
| **Assinantes** | Número de assinantes móveis (mil) | 0-20K |
| **Penetração** | Taxa de penetração de mercado (%) | 50-95% |
| **Torres** | Número de torres de celular | 0-10K |
| **Cobertura 5G** | Percentual de cobertura 5G (%) | 0-100% |

**Funcionalidades:**

#### a) Seleção de Métrica
- Dropdown para escolher métrica visualizada
- Atualização automática de cores
- Legenda dinâmica

#### b) Interatividade
- **Hover:** Destaca estado e mostra tooltip
- **Click:** Atualiza painel de estatísticas
- **Zoom:** Futura funcionalidade com D3.zoom

#### c) Dados por Estado
- 27 estados brasileiros mapeados
- Dados simulados baseados em tendências reais
- Preparado para integração com Anatel API

**Integração Futura:**
```javascript
// Exemplo de integração com API da Anatel
async function loadRealData(year) {
    const response = await fetch(`https://api.anatel.gov.br/data/${year}`);
    const data = await response.json();
    
    // Atualizar telecomData com dados reais
    Object.assign(telecomData, processAnatelData(data));
    
    // Re-renderizar mapa
    renderMap();
}
```

---

## 🎨 Personalização

### 1. Tema de Cores

**Dashboard Plotly:**
```python
# Alterar cores no dash_app.py
fig.update_layout(
    template='plotly_white',  # Opções: plotly, plotly_white, plotly_dark, etc.
    colorway=['#003366', '#ff6b6b', '#4ecdc4', '#f7b731']
)
```

**Mapa D3.js:**
```javascript
// Alterar escala de cores no d3_map.html
const colorScale = d3.scaleThreshold()
    .domain([0, 100, 200, 500])
    .range(['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26']);
```

### 2. Configuração de Métricas

Adicionar novas métricas ao dashboard:

```python
def _create_new_metric_chart(self, df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    # Seu código de visualização aqui
    return fig
```

### 3. Integração com Dados Reais

Para usar dados reais do sistema:

```python
# Carregar dados processados
from src.pipeline import DatasetMerger

merger = DatasetMerger()
df = merger.load_unified_dataset()

# Passar para dashboard
dashboard = NovaCorrenteDashboard(data=df)
```

---

## 📈 Tipos de Visualização

### 1. Séries Temporais

**Uso:** Análise de tendências ao longo do tempo

**Exemplo:**
- Demanda histórica de CONN-001
- Crescimento de 250M para 272M
- Identificação de sazonalidades

### 2. Distribuições

**Uso:** Análise de frequência e padrões

**Exemplo:**
- Histograma de demandas diárias
- Identificação de picos e vales
- Análise de normalidade

### 3. Fatores Externos

**Uso:** Correlação entre demanda e variáveis externas

**Exemplo:**
- Temperatura vs demanda
- Câmbio BRL/USD vs demanda
- Feriados e impacto na demanda

### 4. Análise de Padrões

**Uso:** Identificação de sazonalidades

**Exemplo:**
- Maior demanda às quintas-feiras
- Picos em dezembro (Natal)
- Diminuição em fins de semana

### 5. Previsões

**Uso:** Forecasts futuros com incerteza

**Exemplo:**
- Demanda prevista: 275M em 30 dias
- Intervalo: 248M - 303M (90% confiança)
- Tendência de crescimento

---

## 🔧 Troubleshooting

### Problema: Dashboard não inicia

**Solução:**
```bash
# Verificar dependências
pip install --upgrade dash plotly

# Verificar dados de treinamento
ls data/training/
# Deve conter: *_full.csv, metadata.json, training_summary.json
```

### Problema: Mapa D3.js não carrega

**Solução:**
1. Abrir console do navegador (F12)
2. Verificar erros de CORS
3. Usar servidor local:
```bash
# Python 3
python -m http.server 8000

# Abrir http://localhost:8000/src/visualization/d3_map.html
```

### Problema: Dados não aparecem

**Solução:**
```python
# Verificar se dados foram carregados
dashboard = NovaCorrenteDashboard()
print(dashboard.data.keys())  # Deve mostrar: ['CONN-001', 'unknown']

# Re-executar pipeline de dados
python run_pipeline.py
```

---

## 📚 Recursos Adicionais

### Documentação Plotly Dash

- [Dash Tutorial](https://dash.plotly.com/tutorial)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Dash Callbacks](https://dash.plotly.com/basic-callbacks)

### Documentação D3.js

- [D3.js Gallery](https://observablehq.com/@d3/gallery)
- [D3.js Geographic](https://d3indepth.com/geographic/)
- [Brazil Map Examples](https://observablehq.com/@arbezerra/brazil-map)

### Datasets Brasileiros

- [Anatel Datasets](https://www.anatel.gov.br/)
- [Data Basis](https://data-basis.org/)
- [Zenodo Brazilian Telecom](https://zenodo.org/records/10482897)

---

## 🎯 Próximos Passos

### Melhorias Planejadas

1. **Integração Real-Time**
   - WebSocket para atualizações live
   - Dashboard em tempo real

2. **Análise Comparativa**
   - Comparação entre múltiplos items
   - Benchmarking de performance

3. **Exportação**
   - PDF reports automáticos
   - Exportação de dados filtrados

4. **Modelos Avançados**
   - Integração com ARIMA/Prophet
   - Ensemble forecasting
   - Uncertainty quantification

5. **Geografias**
   - Mapas municipais
   - Heatmaps de densidade
   - Roteamento logístico

---

## 📞 Suporte

Para questões ou problemas:
1. Verificar logs em `data/dashboard.log`
2. Consultar documentação em `docs/`
3. Abrir issue no repositório

---

**Status:** ✅ **SISTEMA COMPLETO E FUNCIONAL**

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

