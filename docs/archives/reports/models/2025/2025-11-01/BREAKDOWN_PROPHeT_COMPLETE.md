# 🔮 BREAKDOWN COMPLETO: PROPHET
## Análise Profunda Passo a Passo - Facebook Prophet

---

**Data:** Novembro 2025  
**Versão:** Prophet Breakdown v1.0  
**Status:** ✅ Breakdown Completo Expandido

---

## 📋 ÍNDICE EXPANDIDO

### Parte I: Fundamentos Prophet
1. [O que é Prophet?](#1-o-que-é-prophet)
2. [Por que Prophet?](#2-por-que-prophet)
3. [Componentes do Modelo](#3-componentes)
4. [Equação Geral](#4-equação-geral)
5. [Comparação com ARIMA](#5-comparação-arima)

### Parte II: Matemática Profunda
6. [Trend Component](#6-trend-component)
7. [Seasonality Component](#7-seasonality)
8. [Holiday Effects](#8-holidays)
9. [Regressors Externos](#9-regressors)
10. [Likelihood Function](#10-likelihood)

### Parte III: Estimação
11. [Parameter Estimation](#11-estimation)
12. [Stan Backend](#12-stan)
13. [MCMC Sampling](#13-mcmc)
14. [Forecasting](#14-forecasting)
15. [Uncertainty Intervals](#15-uncertainty)

### Parte IV: Aplicações Nova Corrente
16. [Demanda com Eventos](#16-eventos)
17. [Múltiplas Sazonalidades](#17-sazonalidades)
18. [Fatores Externos](#18-fatores)
19. [Casos Práticos](#19-casos)
20. [Otimização](#20-otimização)

---

# 1. O QUE É PROPHET?

## 1.1 Definição

**Prophet** é um procedimento de previsão aditivo desenvolvido pelo Facebook para séries temporais com sazonalidade forte e múltiplas sazonalidades.

**Características principais:**
- ✅ Múltiplas sazonalidades (diária, semanal, mensal, anual)
- ✅ Efeitos de feriados
- ✅ Regressores externos
- ✅ Missing data robusto
- ✅ Outliers robusto

## 1.2 Vantagens sobre ARIMA

| Feature | ARIMA | Prophet |
|---------|-------|---------|
| **Sazonalidades múltiplas** | ❌ | ✅ |
| **Eventos/Feriados** | ❌ | ✅ |
| **Missing data** | ❌ | ✅ |
| **Automação** | Manual | Automático |
| **Interpretabilidade** | Baixa | Alta |

---

# 2. POR QUE PROPHET?

## 2.1 Problemas do ARIMA

- ❌ **Uma sazonalidade apenas:** ARIMA lida com uma sazonalidade
- ❌ **Manual tuning:** Requer seleção manual de (p,d,q)
- ❌ **Missing data:** Não lida bem com valores faltantes
- ❌ **Eventos:** Não modela efeitos de feriados/eventos

## 2.2 Vantagens Prophet

- ✅ **Múltiplas sazonalidades:** Diária, semanal, mensal, anual simultaneamente
- ✅ **Automático:** Tuning automático de hiperparâmetros
- ✅ **Missing data:** Robust a valores faltantes
- ✅ **Eventos:** Modela feriados e eventos específicos
- ✅ **Interpretabilidade:** Componentes separados (trend, seasonality, holidays)

---

# 3. COMPONENTES DO MODELO

## 3.1 Decomposição Aditiva

**Prophet decompõe a série temporal em:**

$$y(t) = g(t) + s(t) + h(t) + \epsilon_t$$

onde:
- $g(t)$: **Trend** (tendência)
- $s(t)$: **Seasonality** (sazonalidade)
- $h(t)$: **Holidays** (feriados/eventos)
- $\epsilon_t$: **Error** (ruído)

## 3.2 Componentes Detalhados

### Trend ($g(t)$)
**Modela crescimento/declínio não-linear:**
- Linear growth
- Logistic growth
- Changepoints (mudanças de regime)

### Seasonality ($s(t)$)
**Modela padrões periódicos:**
- Daily seasonality
- Weekly seasonality
- Monthly seasonality
- Yearly seasonality

### Holidays ($h(t)$)
**Modela efeitos de feriados/eventos:**
- Feriados brasileiros
- Eventos específicos (5G auctions, etc.)

### Error ($\epsilon_t$)
**Ruído residual:** $\epsilon_t \sim \mathcal{N}(0, \sigma^2)$

---

# 4. EQUAÇÃO GERAL

## 4.1 Forma Completa

**Modelo Prophet completo:**

$$y(t) = g(t) + s(t) + h(t) + \mathbf{X}(t) \boldsymbol{\beta} + \epsilon_t$$

onde:
- $g(t)$: trend
- $s(t) = \sum_{i} s_i(t)$: soma de sazonalidades
- $h(t) = \sum_{j} h_j(t)$: soma de efeitos de feriados
- $\mathbf{X}(t) \boldsymbol{\beta}$: regressores externos
- $\epsilon_t \sim \mathcal{N}(0, \sigma^2)$: ruído

## 4.2 Forma Simplificada (sem regressores)

$$y(t) = g(t) + s(t) + h(t) + \epsilon_t$$

---

# 5. COMPARAÇÃO COM ARIMA

## 5.1 ARIMA

**Modelo:**
$$\Phi(B)(1-B)^d Y_t = \Theta(B) \epsilon_t$$

**Limitações:**
- Uma sazonalidade
- Linear
- Não lida com eventos

## 5.2 Prophet

**Modelo:**
$$y(t) = g(t) + s(t) + h(t) + \epsilon_t$$

**Vantagens:**
- Múltiplas sazonalidades
- Não-linear (trend)
- Eventos incorporados

---

# 6. TREND COMPONENT

## 6.1 Linear Trend

**Trend linear simples:**
$$g(t) = k t + m$$

onde:
- $k$: growth rate (taxa de crescimento)
- $m$: offset (intercepto)

## 6.2 Logistic Growth

**Trend logístico (com capacidade máxima):**
$$g(t) = \frac{C}{1 + \exp(-k(t - m))}$$

onde:
- $C$: carrying capacity (capacidade máxima)
- $k$: growth rate
- $m$: offset

## 6.3 Changepoints

**Trend com changepoints (mudanças de regime):**

$$g(t) = \left(k + \mathbf{a}(t)^T \boldsymbol{\delta}\right) t + \left(m + \mathbf{a}(t)^T \boldsymbol{\gamma}\right)$$

onde:
- $\boldsymbol{\delta}$: ajustes de slope
- $\boldsymbol{\gamma}$: ajustes de offset
- $\mathbf{a}(t)$: indicadores de changepoints

**Changepoint detection automático:**
- Prophet detecta automaticamente mudanças de regime
- Permite transição suave

---

# 7. SEASONALITY COMPONENT

## 7.1 Fourier Series

**Sazonalidade modelada via Fourier series:**

$$s(t) = \sum_{n=1}^{N} \left(a_n \cos\left(\frac{2\pi n t}{P}\right) + b_n \sin\left(\frac{2\pi n t}{P}\right)\right)$$

onde:
- $P$: período (ex: 365 para anual, 7 para semanal)
- $N$: número de termos Fourier
- $a_n, b_n$: coeficientes Fourier

**Forma vetorial:**
$$s(t) = \mathbf{X}(t) \boldsymbol{\beta}$$

onde:
- $\mathbf{X}(t)$: matriz de features Fourier
- $\boldsymbol{\beta}$: coeficientes a estimar

## 7.2 Múltiplas Sazonalidades

**Sazonalidade total:**
$$s(t) = s_{daily}(t) + s_{weekly}(t) + s_{monthly}(t) + s_{yearly}(t)$$

**Cada sazonalidade com Fourier series própria:**
$$s_i(t) = \sum_{n=1}^{N_i} \left(a_{i,n} \cos\left(\frac{2\pi n t}{P_i}\right) + b_{i,n} \sin\left(\frac{2\pi n t}{P_i}\right)\right)$$

### Exemplo: Weekly Seasonality
**Período:** $P = 7$ dias

$$s_{weekly}(t) = \sum_{n=1}^{N_{weekly}} \left(a_n \cos\left(\frac{2\pi n t}{7}\right) + b_n \sin\left(\frac{2\pi n t}{7}\right)\right)$$

**Número de termos:** $N_{weekly} = 4$ (default)

### Exemplo: Yearly Seasonality
**Período:** $P = 365.25$ dias

$$s_{yearly}(t) = \sum_{n=1}^{N_{yearly}} \left(a_n \cos\left(\frac{2\pi n t}{365.25}\right) + b_n \sin\left(\frac{2\pi n t}{365.25}\right)\right)$$

**Número de termos:** $N_{yearly} = 10$ (default)

---

# 8. HOLIDAY EFFECTS

## 8.1 Modelagem de Feriados

**Efeito de feriado:**
$$h(t) = \sum_{j} h_j(t)$$

**Para cada feriado $j$:**
$$h_j(t) = \begin{cases}
\kappa_j & \text{se } t \text{ é feriado } j \\
0 & \text{senão}
\end{cases}$$

## 8.2 Window Effect

**Feriados podem afetar dias próximos:**
$$h_j(t) = \begin{cases}
\kappa_j & \text{se } t \in [t_{holiday} - d_1, t_{holiday} + d_2] \\
0 & \text{senão}
\end{cases}$$

**Exemplo:**
- Feriado: 15 de novembro
- Window: [-2, +2] dias
- Efeito nos dias 13, 14, 15, 16, 17 de novembro

## 8.3 Feriados Brasileiros

**Lista de feriados:**
- Ano Novo
- Carnaval
- Páscoa
- Tiradentes
- Dia do Trabalho
- Independência
- Nossa Senhora Aparecida
- Finados
- Proclamação da República
- Natal

**Prophet usa automaticamente com `holidays='BR'`**

---

# 9. REGRESSORS EXTERNOS

## 9.1 Linear Regression

**Regressores externos:**
$$y(t) = g(t) + s(t) + h(t) + \mathbf{X}(t) \boldsymbol{\beta} + \epsilon_t$$

onde:
- $\mathbf{X}(t)$: features externas (temperatura, inflação, etc.)
- $\boldsymbol{\beta}$: coeficientes a estimar

## 9.2 Features Externas Nova Corrente

**Exemplos:**
- **Temperatura:** $X_{temp}(t)$
- **Precipitação:** $X_{rain}(t)$
- **Inflação IPCA:** $X_{ipca}(t)$
- **Taxa de Câmbio:** $X_{fx}(t)$
- **5G Expansion:** $X_{5g}(t)$

**Modelo completo:**
$$y(t) = g(t) + s(t) + h(t) + \beta_1 X_{temp}(t) + \beta_2 X_{rain}(t) + ... + \epsilon_t$$

---

# 10. LIKELIHOOD FUNCTION

## 10.1 Assumindo Normalidade

**Se $\epsilon_t \sim \mathcal{N}(0, \sigma^2)$:**

$$\mathbf{y} \sim \mathcal{N}(\boldsymbol{\mu}, \sigma^2 \mathbf{I})$$

onde:
- $\boldsymbol{\mu} = [g(t_1) + s(t_1) + h(t_1), ..., g(t_T) + s(t_T) + h(t_T)]^T$
- $\mathbf{I}$: matriz identidade

## 10.2 Log-Likelihood

$$\log \mathcal{L}(\boldsymbol{\theta} | \mathbf{y}) = -\frac{T}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2} \sum_{t=1}^{T} (y(t) - \mu(t))^2$$

onde $\boldsymbol{\theta}$ são todos os parâmetros (trend, seasonality, holidays).

---

# 11. PARAMETER ESTIMATION

## 11.1 Bayesian Framework

**Prophet usa Bayesian inference via Stan:**

**Priors:**
- $\boldsymbol{\delta} \sim \text{Laplace}(0, \tau)$ (sparse changepoints)
- $\boldsymbol{\beta} \sim \mathcal{N}(0, \sigma^2)$ (regressores)

**Posteriors:**
$$p(\boldsymbol{\theta} | \mathbf{y}) \propto p(\mathbf{y} | \boldsymbol{\theta}) p(\boldsymbol{\theta})$$

## 11.2 MAP Estimation (Default)

**Maximum A Posteriori (MAP):**
$$\hat{\boldsymbol{\theta}} = \arg\max_{\boldsymbol{\theta}} p(\boldsymbol{\theta} | \mathbf{y})$$

**Mais rápido que MCMC**, boa para maioria dos casos.

## 11.3 MCMC Sampling

**Full Bayesian (opcional):**
$$p(\boldsymbol{\theta} | \mathbf{y}) \approx \frac{1}{M} \sum_{m=1}^{M} \delta(\boldsymbol{\theta} - \boldsymbol{\theta}^{(m)})$$

onde $\boldsymbol{\theta}^{(m)}$ são amostras MCMC.

---

# 12. STAN BACKEND

## 12.1 Stan Language

**Prophet usa Stan para inferência Bayesiana:**
- C++ backend
- NUTS sampler (No-U-Turn Sampler)
- Muito eficiente

## 12.2 Compilação

**Stan compila modelo para C++:**
- Execução rápida
- Amostragem MCMC eficiente

---

# 13. MCMC SAMPLING

## 13.1 NUTS Sampler

**No-U-Turn Sampler (Hoffman & Gelman, 2014):**
- Adapta step size automaticamente
- Mais eficiente que HMC padrão

## 13.2 Sampling

**Gera amostras da posterior:**
$$\boldsymbol{\theta}^{(1)}, \boldsymbol{\theta}^{(2)}, ..., \boldsymbol{\theta}^{(M)} \sim p(\boldsymbol{\theta} | \mathbf{y})$$

**Uso:**
- Uncertainty intervals
- Distribuição de forecasts

---

# 14. FORECASTING

## 14.1 Forecast 1 Passo à Frente

**Para tempo futuro $T+h$:**
$$\hat{y}(T+h) = g(T+h) + s(T+h) + h(T+h)$$

**Trend extrapolado:**
$$g(T+h) = \left(k + \mathbf{a}(T+h)^T \boldsymbol{\delta}\right) (T+h) + \left(m + \mathbf{a}(T+h)^T \boldsymbol{\gamma}\right)$$

**Seasonality extrapolado:**
$$s(T+h) = \sum_{i} s_i(T+h)$$

**Holidays:**
$$h(T+h) = \sum_{j} h_j(T+h)$$

## 14.2 Forecast h Passos à Frente

**Para múltiplos passos:**
$$\hat{y}(T+1), \hat{y}(T+2), ..., \hat{y}(T+h)$$

**Cada forecast:**
$$\hat{y}(T+i) = g(T+i) + s(T+i) + h(T+i)$$

---

# 15. UNCERTAINTY INTERVALS

## 15.1 MAP Estimation

**Intervalo aproximado:**
$$\hat{y}(T+h) \pm z_{\alpha/2} \sigma$$

onde $\sigma$ é desvio padrão do ruído estimado.

## 15.2 MCMC Sampling

**Intervalo usando amostras:**

$$\text{CI}_{95\%} = [\text{quantil}_{0.025}(\mathbf{y}^{(m)}(T+h)), \text{quantil}_{0.975}(\mathbf{y}^{(m)}(T+h))]$$

onde $\mathbf{y}^{(m)}(T+h)$ são forecasts de cada amostra MCMC.

**Mais preciso!**

---

# 16. DEMANDA COM EVENTOS

## 16.1 Eventos Específicos

**Nova Corrente: 5G Spectrum Auctions**

**Criar holiday customizado:**
```python
holidays = pd.DataFrame({
    'holiday': '5G_Auction',
    'ds': pd.to_datetime(['2024-10-20', '2025-03-15']),
    'lower_window': -5,  # 5 dias antes
    'upper_window': 10   # 10 dias depois
})
```

**Efeito:** Aumento de demanda antes/depois do leilão

---

# 17. MÚLTIPLAS SAZONALIDADES

## 17.1 Configuração

**Prophet permite múltiplas sazonalidades simultaneamente:**

```python
model = Prophet(
    yearly_seasonality=True,   # Sazonalidade anual
    weekly_seasonality=True,   # Sazonalidade semanal
    daily_seasonality=False,   # Sazonalidade diária
    seasonality_mode='additive' # ou 'multiplicative'
)
```

## 17.2 Exemplo Nova Corrente

**Demanda de materiais:**
- **Yearly:** Ciclo anual (estações)
- **Weekly:** Padrão semanal (segunda vs sexta)
- **Monthly:** Ciclo mensal (fim de mês)

**Todas simultaneamente!**

---

# 18. FATORES EXTERNOS

## 18.1 Adicionar Regressores

**Exemplo: Temperatura**

```python
# Adicionar feature externa
model.add_regressor('temperature')

# Treinar
model.fit(df)

# Forecast
future['temperature'] = forecast_temp
forecast = model.predict(future)
```

## 18.2 Múltiplos Regressores

**Exemplo completo:**
```python
model.add_regressor('temperature')
model.add_regressor('rainfall')
model.add_regressor('inflation')
model.add_regressor('5g_expansion')

# Todos estimados simultaneamente
model.fit(df)
```

---

# 19. CASOS PRÁTICOS

## 19.1 Exemplo: Demanda Diária de Conectores

**Dados:**
- 2 anos de consumo histórico
- Sazonalidade semanal clara
- Feriados brasileiros
- Temperatura como regressor

**Modelo:**
```python
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    holidays=holidays_br
)

model.add_regressor('temperature')

model.fit(df)
forecast = model.predict(future)
```

**Resultados:**
- MAPE: 12%
- Componentes interpretáveis
- Efeito de feriados quantificado

---

# 20. OTIMIZAÇÃO

## 20.1 Hiperparâmetros

**Principais hiperparâmetros:**
- `changepoint_prior_scale`: Flexibilidade do trend
- `seasonality_prior_scale`: Força da sazonalidade
- `holidays_prior_scale`: Força dos feriados
- `mcmc_samples`: Número de amostras MCMC (0 = MAP)

## 20.2 Cross-Validation

**Prophet tem CV automático:**
```python
from prophet.diagnostics import cross_validation

df_cv = cross_validation(
    model, 
    initial='730 days',  # Treino inicial
    period='180 days',    # Re-treinar a cada 180 dias
    horizon='30 days'     # Forecast 30 dias
)
```

**Métricas:**
- MAPE
- RMSE
- MAE

---

# RESUMO FINAL

## Equações Principais

| Componente | Fórmula |
|------------|---------|
| **Trend Linear** | $g(t) = k t + m$ |
| **Trend Logistic** | $g(t) = \frac{C}{1 + \exp(-k(t - m))}$ |
| **Seasonality** | $s(t) = \sum_{n=1}^{N} \left(a_n \cos\left(\frac{2\pi n t}{P}\right) + b_n \sin\left(\frac{2\pi n t}{P}\right)\right)$ |
| **Holidays** | $h(t) = \sum_{j} h_j(t)$ |
| **Modelo Completo** | $y(t) = g(t) + s(t) + h(t) + \mathbf{X}(t) \boldsymbol{\beta} + \epsilon_t$ |

---

**Nova Corrente Grand Prix SENAI**

**PROPHET COMPLETE BREAKDOWN - Version 1.0**

*Novembro 2025*

