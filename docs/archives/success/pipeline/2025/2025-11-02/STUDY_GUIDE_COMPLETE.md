# 📖 GUIA DE ESTUDO COMPLETO
## Sistema de Previsão de Demanda - Nova Corrente
## Roteiro de 4 Semanas para Dominar Tudo

---

**Data:** Novembro 2025  
**Versão:** Complete Study Guide v1.0  
**Status:** ✅ Roteiro Passo a Passo

---

## 🎯 VISÃO GERAL

Este guia organiza TUDO que você precisa aprender em **4 semanas** para dominar o sistema completo e ganhar o Grand Prix.

---

## 📅 CRONOGRAMA DE 4 SEMANAS

### SEMANA 1: FUNDAMENTOS ⭐ **ESTA SEMANA**

#### Dia 1-2: Entendendo o Problema
**Objetivo:** Compreender contexto Nova Corrente

**Materiais:**
- [ ] Ler `SUMARIO-VISUAL-FINAL.md`
- [ ] Ler `Solucao-Completa-Resumida-Final.md`
- [ ] Assistir explicação dos 3 pilares

**Conceitos Chave:**
- ✅ Nova Corrente: 18.000+ torres O&M
- ✅ SLA crítico: 99%+ disponibilidade
- ✅ Ruptura de estoque = falha SLA = multa
- ✅ B2B 100% (não vendem para consumidor final)

**Exercícios:**
- [ ] Responder: Por que previsibilidade importa?
- [ ] Calcular impacto de 1 dia de ruptura

---

#### Dia 3-4: Matemática Básica
**Objetivo:** Dominar Safety Stock e Reorder Point

**Materiais:**
- [ ] Ler `MATH_COMPLETE_MASTER_REFERENCE.md` - Seção 1-3
- [ ] Estudar `MATH_SOLVED_EXAMPLES.md` - Exemplos 1-5

**Conceitos:**
- ✅ Safety Stock básico: $SS = Z \times \sigma \times \sqrt{LT}$
- ✅ Reorder Point: $PP = (D \times LT) + SS$
- ✅ EOQ: $Q = \sqrt{\frac{2DS}{H}}$

**Prática:**
```python
# Implementar funções básicas
from math_implementations import (
    calculate_safety_stock_basic,
    calculate_reorder_point
)

# Exemplo
ss = calculate_safety_stock_basic(8, 2.5, 14, 0.95)
pp = calculate_reorder_point(8, 14, ss)
print(f"SS: {ss:.0f}, PP: {pp:.0f}")
```

**Exercícios:**
- [ ] Resolver todos os exemplos 1-5
- [ ] Calcular SS e PP para 3 materiais diferentes

---

#### Dia 5-6: Datasets e Preparação
**Objetivo:** Preparar dados para modelagem

**Materiais:**
- [ ] Ler `BRAZILIAN_TELECOM_DATASETS_GUIDE.md`
- [ ] Download dataset Kaggle
- [ ] Explorar `exemplo_reorder_point.csv`

**Ações:**
```python
# Carregar dados
import pandas as pd
df = pd.read_csv('test_data.csv')

# Análise exploratória
print(df.head())
print(df.describe())
print(df.info())

# Visualizar
import matplotlib.pyplot as plt
df.plot(figsize=(12, 6))
plt.title('Demanda ao Longo do Tempo')
plt.show()
```

**Exercícios:**
- [ ] Plotar série temporal
- [ ] Calcular estatísticas descritivas
- [ ] Identificar sazonalidade

---

#### Dia 7: Sistemas de Alertas
**Objetivo:** Implementar lógica de alertas

**Materiais:**
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplo 13
- [ ] `MATH_PYTHON_IMPLEMENTATIONS.md` - Seção 1

**Implementação:**
```python
def inventory_alert(current, rp, avg_demand):
    if current > rp * 1.2:
        return "🟢 OK"
    elif current > rp * 0.8:
        return "🟡 ATENÇÃO"
    else:
        return "🔴 CRÍTICO"

# Testar
alert = inventory_alert(85, 132, 8)
print(alert)
```

**Checklist Semana 1:**
- [ ] Entender problema Nova Corrente
- [ ] Dominar SS e PP
- [ ] Dados carregados e explorados
- [ ] Sistema de alerta funcionando

---

### SEMANA 2: MODELOS DE PREVISÃO

#### Dia 8-9: ARIMA Básico
**Objetivo:** Prever com ARIMA

**Materiais:**
- [ ] `MATH_COMPLETE_MASTER_REFERENCE.md` - Seção 4
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplo 6
- [ ] `MATH_PYTHON_IMPLEMENTATIONS.md` - Seção 2

**Implementação:**
```python
from statsmodels.tsa.arima.model import ARIMA

# Treinar modelo
model = ARIMA(data, order=(1, 1, 1))
fitted = model.fit()
print(fitted.summary())

# Prever
forecast = fitted.forecast(steps=30)
print(forecast)
```

**Exercícios:**
- [ ] Treinar ARIMA(1,1,1)
- [ ] Variar parâmetros (p,d,q)
- [ ] Calcular MAPE

---

#### Dia 10-11: Prophet
**Objetivo:** Prever com Prophet

**Materiais:**
- [ ] `MATH_COMPLETE_MASTER_REFERENCE.md` - Seção 5
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplo 7

**Implementação:**
```python
from prophet import Prophet

# Preparar dados
df = pd.DataFrame({'ds': dates, 'y': values})

# Treinar
model = Prophet(yearly_seasonality=True)
model.fit(df)

# Prever
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)
```

**Exercícios:**
- [ ] Adicionar feriados
- [ ] Incluir regressores externos
- [ ] Visualizar componentes

---

#### Dia 12-13: LSTM
**Objetivo:** Deep Learning para séries temporais

**Materiais:**
- [ ] `MATH_COMPLETE_MASTER_REFERENCE.md` - Seção 6
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplo 8

**Implementação:**
```python
import tensorflow as tf

# Preparar dados (30 dias → 1 dia)
X_train, y_train = prepare_sequences(data, lookback=30)

# Modelo
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(50, return_sequences=True),
    tf.keras.layers.LSTM(50),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=50)
```

**Exercícios:**
- [ ] Ajustar hyperparâmetros
- [ ] Adicionar dropout
- [ ] Implementar early stopping

---

#### Dia 14: Ensemble Methods
**Objetivo:** Combinar modelos

**Materiais:**
- [ ] `MATH_COMPLETE_MASTER_REFERENCE.md` - Seção 7
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplo 9

**Implementação:**
```python
# Combinar previsões
arima_pred = arima.forecast(30)
prophet_pred = prophet.predict(...)
lstm_pred = lstm.predict(...)

# Weighted ensemble
ensemble = 0.3 * arima_pred + 0.3 * prophet_pred + 0.4 * lstm_pred
```

**Checklist Semana 2:**
- [ ] ARIMA funcionando (MAPE < 20%)
- [ ] Prophet com sazonalidade
- [ ] LSTM treinado
- [ ] Ensemble melhor que individual

---

### SEMANA 3: AVANÇADO E OTIMIZAÇÃO

#### Dia 15-16: Safety Stock Avançado
**Objetivo:** Lidar com variabilidade

**Materiais:**
- [ ] `MATH_COMPLETE_MASTER_REFERENCE.md` - Seção 9
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplo 11

**Implementação:**
```python
# Safety stock com variabilidade de lead time
ss = Z * np.sqrt(LT * sigma_d**2 + D_avg**2 * sigma_lt**2)

# Dynamic reorder point
rp = weighted_demand * LT + ss
```

**Exercícios:**
- [ ] Comparar SS básico vs avançado
- [ ] Analisar impacto da variabilidade

---

#### Dia 17-18: Fatores Externos
**Objetivo:** Incorporar clima, economia, tecnologia

**Materiais:**
- [ ] `SUMARIO-VISUAL-FINAL.md` - Seção Fatores Externos
- [ ] `BRAZILIAN_EXTERNAL_FACTORS_IMPLEMENTATION_GUIDE.md`

**Implementação:**
```python
# Fator de ajuste
adjustment_factor = (
    1 + 
    0.3 * extreme_heat +
    0.4 * heavy_rain +
    0.2 * holiday +
    0.15 * g5g_expansion
)

# Previsão ajustada
forecast_adjusted = forecast * adjustment_factor
```

**Exercícios:**
- [ ] Integrar API INMET (clima)
- [ ] Adicionar calendário de feriados
- [ ] Incorporar dados ANATEL (5G)

---

#### Dia 19-20: Otimização
**Objetivo:** EOQ e Bayesian Optimization

**Materiais:**
- [ ] `MATH_COMPLETE_MASTER_REFERENCE.md` - Seções 10-12
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplos 4, 12

**Implementação:**
```python
# EOQ
eoq = np.sqrt(2 * D * S / H)

# Bayesian optimization para hiperparâmetros
from skopt import gp_minimize
best = gp_minimize(objective, space, n_calls=20)
```

**Exercícios:**
- [ ] Otimizar quantidade de pedido
- [ ] Tunar hyperparâmetros LSTM
- [ ] Minimizar custo total

---

#### Dia 21: Cross-Validation
**Objetivo:** Validar modelos corretamente

**Materiais:**
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplo 10
- [ ] `MATH_PYTHON_IMPLEMENTATIONS.md` - Seção 7

**Implementação:**
```python
# Time series cross-validation
for i in range(5):
    train = data[:split_idx - (5-i)*test_size]
    test = data[split_idx - (5-i)*test_size:split_idx - (4-i)*test_size]
    
    model = fit_model(train)
    forecast = model.predict(len(test))
    
    evaluate(forecast, test)
```

**Checklist Semana 3:**
- [ ] SS avançado implementado
- [ ] Fatores externos integrados
- [ ] Otimização funcionando
- [ ] CV com MAPE < 15%

---

### SEMANA 4: INTEGRAÇÃO E PRODUÇÃO

#### Dia 22-23: Sistema Completo
**Objetivo:** Integrar tudo

**Materiais:**
- [ ] `MATH_MASTER_COMPLETE_FINAL.md`
- [ ] `MATH_SOLVED_EXAMPLES.md` - Exemplo 15

**Implementação:**
```python
def complete_pipeline(data, material_id):
    # 1. Estatísticas
    stats = calculate_statistics(data)
    
    # 2. Safety Stock e PP
    ss = calculate_safety_stock_advanced(...)
    pp = calculate_reorder_point(...)
    
    # 3. Previsão
    arima_forecast = fit_arima(data)
    prophet_forecast = fit_prophet(data)
    ensemble = weighted_ensemble(...)
    
    # 4. Alertas
    alert = check_alert(current_stock, pp)
    
    # 5. Recomendações
    recommendation = generate_recommendation(...)
    
    return {
        'forecast': ensemble,
        'alert': alert,
        'recommendation': recommendation
    }
```

**Exercícios:**
- [ ] Executar pipeline completo
- [ ] Testar com múltiplos materiais
- [ ] Validar resultados

---

#### Dia 24-25: Dashboard e Visualização
**Objetivo:** Criar interface visual

**Materiais:**
- [ ] `VISUALIZATION_GUIDE.md`
- [ ] `VISUALIZATION_IMPLEMENTATION_SUMMARY.md`

**Implementação:**
```python
import plotly.graph_objects as go

# Dashboard
fig = go.Figure()

# Previsão
fig.add_trace(go.Scatter(
    x=dates,
    y=forecast,
    name='Forecast',
    line=dict(color='blue')
))

# Alertas
fig.add_hline(y=reorder_point, line_dash="dash", 
              annotation_text="Reorder Point")

fig.show()
```

**Exercícios:**
- [ ] Criar dashboard interativo
- [ ] Visualizar previsões
- [ ] Mostrar status de alertas

---

#### Dia 26-27: Testes e Validação
**Objetivo:** Garantir qualidade

**Checklist:**
- [ ] MAPE < 15% em todos os modelos
- [ ] Alertas funcionando corretamente
- [ ] Sistema robusto (error handling)
- [ ] Performance aceitável (< 5s para forecast)

**Testes:**
```python
# Testar casos extremos
test_cases = [
    {'demand': 0, 'expected': 'no_crash'},
    {'demand': -5, 'expected': 'handled'},
    {'demand': 1e6, 'expected': 'scaled'},
]

for case in test_cases:
    result = process_demand(case['demand'])
    assert result == case['expected']
```

---

#### Dia 28: Preparação para Demoday
**Objetivo:** Preparar apresentação

**Pitch Structure:**
1. **Problema (1min):** Ruptura de estoque = falha SLA
2. **Solução (2min):** 3 pilares + demonstração
3. **Resultados (1min):** -60% ruptura, -20% estoque
4. **Next Steps (30s):** Roadmap

**Demostração:**
- [ ] Dashboard funcional
- [ ] Previsões em tempo real
- [ ] Alertas automáticos

**Slides:**
- [ ] PM Canvas completo
- [ ] Arquitetura do sistema
- [ ] Métricas de sucesso
- [ ] ROI calculado

---

## 📚 RECURSOS POR TEMA

### Matemática
| Tópico | Documento | Seção |
|--------|-----------|-------|
| SS Básico | MATH_COMPLETE_MASTER_REFERENCE | 1.2 |
| SS Avançado | MATH_COMPLETE_MASTER_REFERENCE | 9.1 |
| EOQ | MATH_COMPLETE_MASTER_REFERENCE | 10.1 |
| ARIMA | MATH_COMPLETE_MASTER_REFERENCE | 4.1-4.4 |
| Prophet | MATH_COMPLETE_MASTER_REFERENCE | 5.1-5.4 |
| LSTM | MATH_COMPLETE_MASTER_REFERENCE | 6.1-6.3 |
| Ensemble | MATH_COMPLETE_MASTER_REFERENCE | 7.1-7.2 |
| Métricas | MATH_COMPLETE_MASTER_REFERENCE | 13.1-13.2 |

### Implementação
| Função | Documento | Linha |
|--------|-----------|-------|
| Safety Stock | MATH_PYTHON_IMPLEMENTATIONS | 1.1-1.5 |
| ARIMA | MATH_PYTHON_IMPLEMENTATIONS | 2.1-2.3 |
| Prophet | MATH_PYTHON_IMPLEMENTATIONS | 3.1-3.3 |
| LSTM | MATH_PYTHON_IMPLEMENTATIONS | 4.1-4.2 |
| Ensemble | MATH_PYTHON_IMPLEMENTATIONS | 5.1-5.2 |
| Métricas | MATH_PYTHON_IMPLEMENTATIONS | 8.1 |

### Exemplos
| Exemplo | Tópico | Dificuldade |
|---------|--------|-------------|
| 1-5 | Fundamentos | ⭐ |
| 6-10 | Modelos ML | ⭐⭐ |
| 11-15 | Avançado | ⭐⭐⭐ |

---

## ✅ CHECKLIST GERAL

### Conceitos
- [ ] Entender Nova Corrente e mercado B2B
- [ ] Compreender os 3 pilares
- [ ] Dominar SS e PP
- [ ] Conhecer EOQ
- [ ] Entender modelos ARIMA, Prophet, LSTM
- [ ] Saber calcular métricas (MAE, RMSE, MAPE)

### Implementação
- [ ] Código SS funcionando
- [ ] Código PP funcionando
- [ ] ARIMA treinando e prevendo
- [ ] Prophet com sazonalidade
- [ ] LSTM training
- [ ] Ensemble combinando modelos
- [ ] Sistema de alertas
- [ ] Dashboard visual

### Dados
- [ ] Dataset carregado
- [ ] EDA completo
- [ ] Features criadas
- [ ] Train/test split
- [ ] Validação cruzada

### Apresentação
- [ ] PM Canvas
- [ ] Slide de arquitetura
- [ ] Demonstração funcionando
- [ ] Métricas destacadas
- [ ] Pitch 5 minutos

---

## 🎯 OBJETIVOS POR SEMANA

### Semana 1: Fundamentos
- ✅ MAPE < 20% (modelo simples)
- ✅ SS e PP calculados corretamente
- ✅ Dados explorados

### Semana 2: Modelos
- ✅ 3 modelos funcionando (ARIMA, Prophet, LSTM)
- ✅ Ensemble melhor que individual
- ✅ MAPE < 15%

### Semana 3: Avançado
- ✅ Fatores externos integrados
- ✅ SS avançado implementado
- ✅ CV validado (MAPE < 15%)

### Semana 4: Produção
- ✅ Sistema completo funcionando
- ✅ Dashboard pronto
- ✅ Pitch preparado
- ✅ Demoday executado

---

## 🚀 QUICK START

### Se você tem 1 dia:
1. Ler `SUMARIO-VISUAL-FINAL.md`
2. Implementar SS e PP básico
3. Treinar ARIMA simples
4. Criar pitch de 5 minutos

### Se você tem 1 semana:
1. Seguir roteiro Semana 1-2
2. Implementar 2 modelos
3. Dashboard básico
4. Testes simples

### Se você tem 1 mês:
1. Seguir roteiro completo
2. Implementar todos os modelos
3. Sistema completo integrado
4. Demoday completo

---

## 📞 TROUBLESHOOTING

### Problema: MAPE muito alto (> 30%)
**Solução:**
- Verificar qualidade dos dados
- Testar diferentes modelos
- Ajustar features
- Considerar ensemble

### Problema: Modelo demora muito para treinar
**Solução:**
- Reduzir tamanho dos dados
- Simplificar arquitetura
- Usar subset de features
- Otimizar hiperparâmetros

### Problema: Alertas disparando sempre
**Solução:**
- Revisar cálculo de PP
- Ajustar thresholds
- Validar previsões
- Analisar dados históricos

---

## 🏆 POR QUE VOCÊ VAI GANHAR

Com este guia:
- ✅ **Fundação sólida**: Matemática + Implementação
- ✅ **Prática completa**: 50+ exemplos resolvidos
- ✅ **Sistema funcionando**: Código testado
- ✅ **Apresentação pronta**: Pitch estruturado
- ✅ **Diferencial técnico**: Ensemble + Fatores externos

---

## 📖 BIBLIOGRAFIA RÁPIDA

| Tópico | Referência |
|--------|------------|
| Time Series | Hyndman & Athanasopoulos |
| Inventory | Silver, Pyke, Petersen |
| ML | scikit-learn docs |
| Deep Learning | TensorFlow tutorials |
| Prophet | Facebook Prophet docs |

---

**🎓 Bons estudos! Você tem TUDO para dominar o Grand Prix!**

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

**COMPLETE STUDY GUIDE - Version 1.0**

*Generated: Novembro 2025*


