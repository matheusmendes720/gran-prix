# 📊 Nova Corrente Demand Forecasting System

## Sistema de Previsão de Demanda - Grand Prix SENAI

Sistema modular em Python para previsão diária de demanda, integrando ARIMA, Prophet e LSTM para calcular Pontos de Reposição (PP) e gerar alertas, reduzindo rupturas de estoque em até 50%.

---

## 🎯 Características Principais

- **Modelos Múltiplos**: ARIMA/SARIMA, Prophet, LSTM
- **Ensemble**: Combinação ponderada de modelos para robustez
- **Cálculo de PP**: Ponto de Reposição baseado em Safety Stock
- **Sistema de Alertas**: Notificações automáticas quando estoque ≤ PP
- **Relatórios**: CSV e PDF com previsões, PP e alertas
- **Fatores Externos**: Suporte a temperatura, feriados, indicadores econômicos
- **Escalável**: Suporta 18,000+ torres através de agregação por item/categoria

---

## 📋 Requisitos

- Python 3.8+
- Bibliotecas principais:
  - `pandas`, `numpy`, `scipy`
  - `statsmodels`, `pmdarima`
  - `prophet`
  - `tensorflow` (opcional, para LSTM)
  - `scikit-learn`

**Instalação:**
```bash
pip install -r requirements_forecasting.txt
```

---

## 🚀 Uso Rápido

### 1. Preparar Dados

Formato CSV/Excel com colunas:
- `date` ou `Date`: Data (datetime)
- `Item_ID`: Identificador do item
- `Quantity_Consumed`: Quantidade consumida
- `Site_ID`: Identificador do site (opcional)
- `Lead_Time`: Lead time em dias (opcional)

### 2. Executar Pipeline

```python
from demand_forecasting import DemandForecastingPipeline

# Configuração
config = {
    'service_level': 0.95,
    'ensemble_weights': {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3},
    'forecast_horizon': 30,
    'use_ensemble': True
}

# Inicializar pipeline
pipeline = DemandForecastingPipeline(config=config)

# Executar
results = pipeline.run(
    data_file='demand_data.csv',
    lead_times={'CONN-001': 14, 'CONN-002': 14},
    current_stocks={'CONN-001': 100, 'CONN-002': 150},
    output_dir='output'
)
```

### 3. Script Principal

```bash
python nova_corrente_forecasting_main.py
```

---

## 📁 Estrutura do Projeto

```
demand_forecasting/
├── __init__.py                    # Package initialization
├── data_loader.py                 # Data loading and preprocessing
├── pp_calculator.py               # PP calculation and alerts
├── pipeline.py                    # Main pipeline
└── models/
    ├── arima_model.py             # ARIMA/SARIMA forecaster
    ├── prophet_model.py           # Prophet forecaster
    ├── lstm_model.py              # LSTM forecaster
    └── ensemble_model.py          # Ensemble forecaster
```

---

## 🔧 Componentes Principais

### 1. Data Loader (`data_loader.py`)

Carrega e preprocessa dados:
- Feature engineering temporal (dia, mês, semana)
- Codificação cíclica (sin/cos para meses)
- Feriados brasileiros
- Fatores externos (temperatura, indicadores econômicos)
- Tratamento de valores faltantes

### 2. Modelos de Previsão

#### ARIMA (`arima_model.py`)
- Auto-seleção de ordem (p, d, q)
- Suporte a SARIMA (sazonal)
- Regressores exógenos
- Validação com métricas (RMSE, MAE, MAPE)

#### Prophet (`prophet_model.py`)
- Modelagem de sazonalidade
- Suporte a feriados e eventos
- Regressores externos
- Intervalos de confiança

#### LSTM (`lstm_model.py`)
- Rede neural para padrões complexos
- Look-back configurável
- Early stopping
- Normalização MinMax

#### Ensemble (`ensemble_model.py`)
- Combinação ponderada de modelos
- Pesos configuráveis
- Robustez através de múltiplos modelos

### 3. PP Calculator (`pp_calculator.py`)

Calcula Reorder Points:
- Safety Stock: `SS = Z_α × σ_D × √LT`
- Reorder Point: `PP = (avg_demand × LT) + SS`
- Dias até ruptura
- Sistema de alertas automáticos

### 4. Pipeline (`pipeline.py`)

Orquestra todo o processo:
1. Carregamento e preprocessamento
2. Preparação de modelos
3. Treinamento
4. Geração de previsões
5. Cálculo de PP
6. Geração de relatórios

---

## 📊 Métricas de Performance

**Targets:**
- MAPE < 15%
- RMSE alinhado com média do dataset
- Backtest em histórico de rupturas

**Métricas Calculadas:**
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- MAPE (Mean Absolute Percentage Error)

---

## 📈 Outputs

### 1. Previsões (`forecasts_report.csv`)
- Previsão diária para próximos 30 dias
- Intervalos de confiança (lower, upper)
- Por item

### 2. Reorder Points (`weekly_pp_report.csv`)
- PP calculado para cada item
- Safety Stock
- Demand média diária
- Dias até ruptura
- Status (critical/normal)

### 3. Alertas (`alerts_report.csv`)
- Items com estoque ≤ PP
- Mensagens de alerta
- Recomendação de reordenação

---

## 🔍 Validação

### Walk-Forward Validation

```python
from demand_forecasting.data_loader import DataLoader

loader = DataLoader()
data_dict = loader.load_and_preprocess('demand_data.csv')

for item_id, df in data_dict.items():
    # Split time-based
    train_df, test_df = loader.split_train_test(df, test_size=0.2)
    
    # Train on train_df, test on test_df
    # Evaluate metrics
```

### Cross-Validation Temporal

Use `TimeSeriesSplit` do scikit-learn para validação temporal.

---

## 🛠️ Customização

### Configuração de Modelos

```python
config = {
    'service_level': 0.95,  # Nível de serviço
    'ensemble_weights': {
        'ARIMA': 0.4,
        'Prophet': 0.3,
        'LSTM': 0.3
    },
    'forecast_horizon': 30,  # Dias à frente
    'use_ensemble': True,    # Usar ensemble ou modelos individuais
    'external_features': True  # Incluir fatores externos
}
```

### Ajuste de Parâmetros

#### ARIMA
```python
forecaster = ARIMAForecaster(seasonal=True, m=7)
```

#### Prophet
```python
forecaster = ProphetForecaster(
    daily_seasonality=True,
    yearly_seasonality=True,
    weekly_seasonality=True
)
```

#### LSTM
```python
forecaster = LSTMForecaster(
    look_back=30,
    units=50,
    epochs=50,
    batch_size=32
)
```

---

## 📝 Exemplo Completo

```python
import pandas as pd
from demand_forecasting import DemandForecastingPipeline

# Dados
data_file = 'demand_data.csv'

# Configuração
config = {
    'service_level': 0.95,
    'ensemble_weights': {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3},
    'forecast_horizon': 30
}

# Lead times e estoques atuais
lead_times = {
    'CONN-001': 14,
    'CONN-002': 14,
}

current_stocks = {
    'CONN-001': 100,
    'CONN-002': 150,
}

# Executar pipeline
pipeline = DemandForecastingPipeline(config=config)
results = pipeline.run(
    data_file=data_file,
    lead_times=lead_times,
    current_stocks=current_stocks,
    output_dir='output'
)

# Verificar alertas
if results['alerts']:
    for alert_info in results['alerts']:
        print(alert_info['alert'])
```

---

## 🚨 Troubleshooting

### Erro: "TensorFlow not available"
- LSTM requer TensorFlow
- Instale: `pip install tensorflow`
- Ou remova LSTM do ensemble

### Erro: "Insufficient data"
- Requer mínimo 24 meses de dados históricos
- Verifique formato de datas

### Erro: "No target variable found"
- Verifique nome da coluna de demanda
- Padrão: `Quantity_Consumed`

---

## 📚 Referências

- [MachineLearningMastery - ARIMA](https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/)
- [MachineLearningPlus - ARIMA](https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/)
- [Medium - Time Series Forecasting](https://medium.com/@cdabakoglu/time-series-forecasting-arima-lstm-prophet-with-python-e73a750a9887)
- [DataCamp - LSTM](https://www.datacamp.com/tutorial/lstm-python-stock-market)
- [GeeksforGeeks - Inventory Forecasting](https://www.geeksforgeeks.org/machine-learning/inventory-demand-forecasting-using-machine-learning-python/)

---

## 📄 Licença

Projeto desenvolvido para Grand Prix SENAI - Nova Corrente

---

## 👥 Contribuição

Sistema desenvolvido conforme especificações do desenvolvimento:
- Phase 1: Data Prep ✅
- Phase 2: Model Implementation ✅
- Phase 3: PP Calculation & Alerts ✅
- Phase 4: Testing & Deployment ✅

---

**Nova Corrente Grand Prix SENAI**  
**Demand Forecasting System v1.0**

