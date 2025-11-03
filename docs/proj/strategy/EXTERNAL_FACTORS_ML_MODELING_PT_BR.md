# 🤖 FATORES EXTERNOS E MODELAGEM ML
## Guia Completo para Previsibilidade de Demandas

**Versão:** 1.0  
**Data:** Novembro 2025  
**Área:** Machine Learning & Modelagem Preditiva

---

## 📋 ÍNDICE

1. [Fatores Externos Detalhados](#fatores-externos)
2. [Integração com Modelos ML](#integracao-ml)
3. [Feature Engineering](#feature-engineering)
4. [Seleção de Modelos por Cenário](#selecao-modelos)
5. [Validação e Métricas](#validacao)
6. [Pipeline Completo](#pipeline-completo)

---

<a name="fatores-externos"></a>
## 1. 🌦️ FATORES EXTERNOS DETALHADOS

### 1.1 Fatores Climáticos

#### Temperatura (°C)

**Impacto na Demanda:**
```
Temperatura > 32°C:
- Refrigeração: +40% demanda (sistemas sobrecarregados)
- Isolamento térmico: +25% demanda (deterioração acelerada)
- Cabeamento: +15% demanda (expansão térmica)

Temperatura < 10°C:
- Aquecimento: +30% demanda
- Isolamento: +20% demanda
- Baterias: +35% demanda (redução eficiência)
```

**Fonte de Dados:**
- **INMET:** Histórico e previsão 7 dias
- **API OpenWeather:** Dados real-time

**Formato de Dados:**
```python
{
    "date": "2025-11-07",
    "temp_max": 34.5,
    "temp_min": 23.2,
    "temp_avg": 28.9,
    "region": "bahia_salvador"
}
```

**Feature Engineering:**
```python
# Categorias de temperatura
temp_category = {
    "very_hot": temp > 32,
    "hot": 25 < temp <= 32,
    "normal": 10 <= temp <= 25,
    "cold": temp < 10
}

# Bias sazonal
seasonal_bias = cosine(day_of_year)  # Verão vs inverno
```

#### Precipitação (mm)

**Impacto na Demanda:**
```
Chuva > 50mm/dia:
- Infiltração em torres: +40-50% demanda urgente
- Isolamento elétrico: +30% demanda
- Corrosão estrutural: +15% demanda (longo prazo)

Secas prolongadas (30+ dias sem chuva):
- Incêndio risco: +25% prevenção
- Estresse térmico: +10% demanda
```

**Feature Engineering:**
```python
# Acumulado 7 dias
rainfall_7d = sum(precipitation[-7:])

# Intensidade
intensity = precipitation / duration_hours

# Categorias
category = {
    "heavy": precipitation > 50,
    "moderate": 10 < precipitation <= 50,
    "light": precipitation <= 10
}
```

#### Umidade Relativa (%)

**Impacto na Demanda:**
```
Umidade > 80%:
- Corrosão: +25% demanda componentes metálicos
- Isolamento: +20% demanda
- Mofo/mofo: +15% demanda (longo prazo)

Umidade < 30%:
- Eletricidade estática: +10% demanda
- Riscos de fogo: +5% prevenção
```

**Dados em Feature:**
```python
# Risco de corrosão
corrosion_risk = (humidity > 80) * 1.0

# Desconforto térmico
thermal_discomfort = abs(humidity - 60) / 60
```

#### Vento (km/h)

**Impacto na Demanda:**
```
Vento > 80 km/h (tempestade):
- Estrutural: +50% demanda refração/apoio
- Cabos: +35% demanda (solicitação mecânica)
- Antenas: +40% demanda orientação

Vento < 5 km/h (sem vento):
- Refrigeração: +15% demanda (sem ventilação natural)
```

**Feature Engineering:**
```python
# Velocidade acima do limite estrutural
structural_risk = max(0, wind_speed - 80) / 20

# Rajadas
gust_factor = max_wind / avg_wind
```

### 1.2 Fatores Econômicos

#### Taxa de Câmbio BRL/USD

**Impacto na Demanda:**
```
Desvalorização > 10% em 30 dias:
- Custos importação: +20-30%
- Antecipar compras: +15% demanda (estoque)

Valorização > 10%:
- Redução antecipada: -10% demanda
- Benefício custo: +5% margem
```

**Fonte de Dados:**
- **BACEN:** https://www.bcb.gov.br/
- **API:** Taxa diária histórica e atual

**Feature Engineering:**
```python
# Volatilidade 30 dias
volatility_30d = std(exchange_rate[-30:])

# Tendência (mais relevante que valor absoluto)
trend = (exchange_rate[-1] - exchange_rate[-30]) / exchange_rate[-30]

# Dummy de crise cambial
currency_crisis = (volatility_30d > 0.05) * 1.0
```

#### Inflação (IPCA)

**Impacto na Demanda:**
```
IPCA > 1% ao mês (alta inflação):
- Antecipar compras: +15% demanda (custo futuro maior)
- Reduzir estoque: -10% (custo capital caro)

IPCA < 0.5%:
- Postergar: -5% demanda
- Estoque confortável: +5%
```

**Fonte de Dados:**
- **IBGE:** Índices mensais
- **BACEN:** Expectativas

**Feature Engineering:**
```python
# Inflação acumulada 12 meses
ipca_12m = sum(ipca_monthly[-12:])

# Expectativa de inflação
inflation_expectation = fetch_bacen_projection()

# Custo de espera
waiting_cost = inflation_expectation / 30  # Por dia
```

#### Greves e Interrupções

**Impacto na Demanda:**
```
Greve Transportes:
- Entrega -100%: Aumentar estoque +50% preventivamente
- Lead time: 14 → 30+ dias

Greve Petrobras:
- Combustível escassez: +20% demanda (emergência)
```

**Fonte de Dados:**
- **Google News API:** Alertas de greves
- **Sindicatos:** Calendário oficial

**Feature Engineering:**
```python
# Alertas de greve
strike_alert = fetch_google_news(keyword="greve transporte")

# Dummy de greve ativa
active_strike = (strike_alert > threshold) * 1.0

# Multiplicador lead time
lead_time_multiplier = 1.0 + (active_strike * 2.0)  # x3 lead time
```

### 1.3 Fatores Tecnológicos

#### Expansão 5G

**Impacto na Demanda:**
```
Nova Cidade com 5G:
- Infraestrutura: +200-300% demanda pontual
- Equipamentos RF: +150% demanda
- Backhaul: +100% demanda

Migração 4G → 5G:
- Substituição gradual: +50% demanda/ano
```

**Fonte de Dados:**
- **ANATEL:** https://www.gov.br/anatel/
- **Relatórios Setoriais:** ABR Telecom

**Feature Engineering:**
```python
# Cobertura 5G por município
anatel_data = fetch_anatel_5g_coverage()

# Novas cidades 5G (delta)
new_5g_cities = anatel_data['this_month'] - anatel_data['last_month']

# Múltiplo de demanda
demand_multiplier_5g = 1.0 + (new_5g_cities / total_municipalities) * 3.0
```

#### Migração Tecnológica (4G/5G/Fiber)

**Impacto na Demanda:**
```
Migração Fibra:
- Cabeamento: -40% cabo cobre, +80% fibra ótica
- Conectores: +60% demanda específica
- Infraestrutura: +30% nova

Migração 5G:
- Antenas: +100% redes novas
- Backhaul: +50% demanda
```

### 1.4 Fatores Operacionais

#### Feriados Brasileiros

**Impacto na Demanda:**
```
Feriado Nacional:
- Demanda imediata: -30% (não trabalho)
- Antecipação: +20% nos 2 dias anteriores
- Retorno: +15% primeiros 2 dias pós-feriado

Feriadão (4+ dias):
- Estoque prevenção: +40%
```

**Feature Engineering:**
```python
# Dummy feriado
is_holiday = (date in brazilian_holidays) * 1.0

# Dias até próximo feriado
days_to_holiday = min([h - date for h in brazilian_holidays if h > date])

# Dummy pré-feriado (2 dias antes)
pre_holiday = (days_to_holiday <= 2) * 1.0

# Dummy pós-feriado (2 dias depois)
post_holiday = (days_since_holiday <= 2) * 1.0
```

#### Renovação de SLA

**Impacto na Demanda:**
```
Período Renovação (Jan/Jul):
- Manutenções preventivas: +30% demanda
- Inspeções obrigatórias: +50% demanda
- Estoque ampliado: +40%

Período Normal:
- Demanda base
```

**Feature Engineering:**
```python
# Ciclo de renovação (6 meses)
sla_cycle = (month % 6) / 6

# Próximo renovação
days_to_renewal = days_until(month_end if month in [1, 7] else next_renewal)

# Multiplicador demanda
demand_multiplier_sla = 1.0 + (days_to_renewal <= 30) * 0.3
```

---

<a name="integracao-ml"></a>
## 2. 🔗 INTEGRAÇÃO COM MODELOS ML

### 2.1 ARIMA com Regressores Exógenos (ARIMAX)

**Aplicação:** Clima, econômico como variáveis exógenas

**Modelo:**
```python
from statsmodels.tsa.arima.model import ARIMA

# ARIMA(2,1,2) + regressores exógenos
model = ARIMA(demand, order=(2,1,2), exog=external_factors)
model_fit = model.fit()

# Previsão com fatores externos futuros
forecast, conf_int = model_fit.forecast(steps=30, exog=future_external)
```

**Regressores Recomendados:**
- Temperatura média
- Precipitação
- Taxa de câmbio
- Inflação acumulada
- Dummy feriados

**Limitação:**  
Variáveis exógenas requerem previsão (clima, economia).

### 2.2 Prophet com Regressores Aditivos

**Aplicação:** Eventos, feriados, fatores externos contínuos

**Modelo:**
```python
from prophet import Prophet

# Prophet com regressores
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    holidays=brazilian_holidays
)

# Adiciona regressores
model.add_regressor('temperature')
model.add_regressor('rainfall')
model.add_regressor('exchange_rate', prior_scale=0.5)
model.add_regressor('sla_renewal_period', prior_scale=0.3)

# Fit e previsão
model.fit(data)
forecast = model.predict(future)
```

**Vantagens:**
- Modelagem não-aditiva de feriados
- Regressores com prior_scale
- Intervalo de confiança automático

**Recomendação:**  
Modelo principal para Nova Corrente (vários fatores externos).

### 2.3 LSTM Multivariado

**Aplicação:** Padrões complexos e não-lineares

**Modelo:**
```python
from tensorflow import keras
from tensorflow.keras import layers

# LSTM multivariado
model = keras.Sequential([
    layers.LSTM(64, return_sequences=True, input_shape=(timesteps, features)),
    layers.LSTM(32, return_sequences=False),
    layers.Dense(16, activation='relu'),
    layers.Dense(1)  # Previsão 1 dia à frente
])

# Compilar
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Treinar
model.fit(X_train, y_train, epochs=100, validation_split=0.2)
```

**Features de Entrada:**
- Demanda lag (t-1, t-7, t-30)
- Temperatura, precipitação, umidade, vento
- Taxa de câmbio, inflação
- Dummies feriados, SLA, greves
- Tendências (média móvel 7d, 30d)

**Vantagens:**
- Captura não-linearidades
- Multivariado
- Escala para 50+ itens

**Desvantagens:**
- Exige muitos dados
- Poco interpretável
- Computacionalmente caro

### 2.4 Ensemble Métodos

**Aplicação:** Balancear precisão e robustez

**Modelo Ensemble:**
```python
def ensemble_forecast(demand, external_factors):
    # Modelo 1: ARIMA
    arima_forecast = arima_model.forecast(30)
    arima_weight = 0.3
    
    # Modelo 2: Prophet
    prophet_forecast = prophet_model.predict(30)
    prophet_weight = 0.3
    
    # Modelo 3: LSTM
    lstm_forecast = lstm_model.predict(30)
    lstm_weight = 0.4
    
    # Ensemble
    ensemble_forecast = (
        arima_weight * arima_forecast +
        prophet_weight * prophet_forecast +
        lstm_weight * lstm_forecast
    )
    
    # Confidence interval (método conservador)
    ensemble_conf = min(
        arima_forecast.conf_int,
        prophet_forecast.conf_int,
        lstm_forecast.conf_int
    )
    
    return ensemble_forecast, ensemble_conf
```

**Recomendação:**  
Peso adaptativo conforme performance por cenário.

---

<a name="feature-engineering"></a>
## 3. 🔧 FEATURE ENGINEERING

### 3.1 Features Temporais

```python
# Features temporais
features_temp = {
    # Cíclico (sin/cos para pegar periodicidade)
    'day_of_year_sin': np.sin(2 * np.pi * day_of_year / 365),
    'day_of_year_cos': np.cos(2 * np.pi * day_of_year / 365),
    'week_of_year_sin': np.sin(2 * np.pi * week / 52),
    'week_of_year_cos': np.cos(2 * np.pi * week / 52),
    
    # Categórico
    'month': month,  # 1-12
    'weekday': weekday,  # 0-6
    'quarter': quarter,  # 1-4
    
    # Dummies
    'is_weekend': (weekday >= 5) * 1,
    'is_month_start': (day <= 7) * 1,
    'is_month_end': (day >= 25) * 1
}
```

### 3.2 Features de Demanda

```python
# Features lag (valores passados)
features_lag = {
    'demand_t-1': demand.shift(1),  # Ontem
    'demand_t-7': demand.shift(7),  # Semana passada
    'demand_t-30': demand.shift(30),  # Mês passado
    'demand_t-365': demand.shift(365)  # Ano passado
}

# Médias móveis (tendências)
features_ma = {
    'ma_7': demand.rolling(7).mean(),  # Média 7 dias
    'ma_30': demand.rolling(30).mean(),  # Média 30 dias
    'ma_90': demand.rolling(90).mean()  # Média trimestral
}

# Volatilidade
features_vol = {
    'std_7': demand.rolling(7).std(),  # Desvio padrão 7 dias
    'cv_30': demand.rolling(30).std() / demand.rolling(30).mean()  # Coef variação
}
```

### 3.3 Features Externas Climáticas

```python
# Agregações climáticas
features_climate = {
    # Temperatura
    'temp_max_7d': temperature.rolling(7).max(),
    'temp_min_7d': temperature.rolling(7).min(),
    'temp_volatility': temperature.rolling(7).std(),
    
    # Precipitação
    'rainfall_7d_sum': rainfall.rolling(7).sum(),
    'rainfall_30d_avg': rainfall.rolling(30).mean(),
    'rainfall_cumulative': rainfall.cumsum(),
    
    # Combinações
    'temp_rain_interaction': temperature * rainfall,
    'humidity_risk': (humidity > 80) * 1.0
}
```

### 3.4 Features Econômicas

```python
# Features econômicas
features_econ = {
    # Câmbio
    'ex_rate_change_7d': exchange_rate.pct_change(7),
    'ex_rate_change_30d': exchange_rate.pct_change(30),
    'ex_rate_volatility': exchange_rate.rolling(30).std(),
    
    # Inflação
    'ipca_12m_accumulated': ipca.cumsum(),
    'inflation_expectation': fetch_bacen_projection(),
    
    # Riscos
    'currency_crisis': (ex_rate_volatility > 0.05) * 1.0,
    'high_inflation': (ipca > 1.0) * 1.0
}
```

### 3.5 Features Combinadas

```python
# Features combinadas (interações)
features_interactions = {
    # Clima × Econômico
    'storm_economy': (rainfall > 50) * (currency_crisis) * 1.0,
    
    # Tecnologia × Operacional
    '5g_renewal_period': (new_5g_cities > 0) * (sla_renewal) * 1.0,
    
    # Operacional × Econômico
    'holiday_inflation': is_holiday * high_inflation
}
```

---

<a name="selecao-modelos"></a>
## 4. 🎯 SELEÇÃO DE MODELOS POR CENÁRIO

### Cenário 1: Item Fast-Moving (Conectores Ópticos)

**Características:**
- Alta rotatividade (5-10/dia)
- Padrão relativamente estável
- Sazonalidade semanal/mensal clara

**Modelo Recomendado:** Prophet com regressores

**Justificativa:**
- Sazonalidades automáticas
- Feriados brasileiros
- Fatores climáticos simples
- Interpretável

**Implementação:**
```python
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    holidays=brazilian_holidays
)
model.add_regressor('temperature')
model.add_regressor('is_holiday')
model.add_regressor('sla_renewal_period')
```

**Performance Esperada:** MAPE 8-12%

### Cenário 2: Item Slow-Moving (Equipamentos RF)

**Características:**
- Baixa rotatividade (0.1-0.5/dia)
- Raro, mas crítico
- Alto valor unitário

**Modelo Recomendado:** ARIMA com regressores exógenos

**Justificativa:**
- Poucos dados (baseline simples)
- Padrões lineares
- Interpretável

**Implementação:**
```python
model = ARIMA(demand, order=(2,1,2), exog=external_factors)
model_fit = model.fit()
forecast, conf_int = model_fit.forecast(30, exog=future_external)
```

**Performance Esperada:** MAPE 15-20% (aceitável para slow-moving)

### Cenário 3: Item com Fatores Externos Complexos

**Características:**
- Demanda influenciada por clima, economia, tecnologia
- Padrões não-lineares

**Modelo Recomendado:** Ensemble (Prophet + LSTM)

**Justificativa:**
- Robustez
- Prophet: sazonalidades e eventos
- LSTM: padrões não-lineares

**Implementação:**
```python
# Ensemble weighted
ensemble = 0.4 * prophet_forecast + 0.6 * lstm_forecast
```

**Performance Esperada:** MAPE 10-15%

---

<a name="validacao"></a>
## 5. 📊 VALIDAÇÃO E MÉTRICAS

### 5.1 Métricas de Precisão

**MAPE (Mean Absolute Percentage Error):**
```python
def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Benchmark:
# < 10%: Excelente
# 10-15%: Muito bom
# 15-20%: Aceitável
# > 20%: Melhorar modelo
```

**RMSE (Root Mean Squared Error):**
```python
def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))
```

**MAE (Mean Absolute Error):**
```python
def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))
```

### 5.2 Cross-Validation Temporal

```python
# Time series split
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)

for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    # Treinar modelo
    model.fit(X_train, y_train)
    
    # Avaliar
    mape_score = mape(y_test, model.predict(X_test))
```

### 5.3 Métricas de Negócio

**Stockout Prevention Rate:**
```
Rate = (Nº stockouts previstos vs. reais evitados) / (Total stockouts históricos)
Target: > 80%
```

**Capital Optimization:**
```
Savings = Valor estoque redução / Valor estoque anterior
Target: 15-20%
```

---

<a name="pipeline-completo"></a>
## 6. 🏗️ PIPELINE COMPLETO

```python
# Pipeline end-to-end
def full_pipeline(raw_data):
    # 1. Preprocessing
    data = preprocess_data(raw_data)
    
    # 2. External factors
    climate_data = fetch_climate_data()
    economic_data = fetch_economic_data()
    tech_data = fetch_tech_data()
    operational_data = fetch_operational_data()
    
    # 3. Feature engineering
    features = engineer_features(
        data,
        climate_data,
        economic_data,
        tech_data,
        operational_data
    )
    
    # 4. Train/test split
    X_train, X_test, y_train, y_test = temporal_split(features, test_size=0.2)
    
    # 5. Model selection
    models = {
        'arima': train_arima(X_train, y_train),
        'prophet': train_prophet(X_train, y_train),
        'lstm': train_lstm(X_train, y_train)
    }
    
    # 6. Evaluate
    scores = {}
    for name, model in models.items():
        y_pred = model.predict(X_test)
        scores[name] = {
            'mape': mape(y_test, y_pred),
            'rmse': rmse(y_test, y_pred),
            'mae': mae(y_test, y_pred)
        }
    
    # 7. Select best model
    best_model_name = min(scores, key=lambda k: scores[k]['mape'])
    best_model = models[best_model_name]
    
    # 8. Forecast
    forecast = best_model.forecast(30)
    
    # 9. PP calculation
    pp = calculate_reorder_point(forecast, lead_times)
    
    # 10. Alerts
    alerts = generate_alerts(current_stock, pp)
    
    # 11. Reports
    generate_report(forecast, pp, alerts)
    
    return forecast, pp, alerts
```

---

## 📌 CONCLUSÃO

Este documento estabelece a estratégia de modelagem com fatores externos para Nova Corrente, com Prophet como base e ensemble quando necessário.

**Próximos Passos:**
1. Implementar pipeline de fatores externos
2. Testar modelos por cenário
3. Validar com MAPE < 15%
4. Deploy em produção

---

**Documento Final:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia de Implementação

