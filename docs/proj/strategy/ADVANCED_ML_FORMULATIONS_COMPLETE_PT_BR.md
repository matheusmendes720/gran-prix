# 🧮 FÓRMULAS AVANÇADAS ML/DL - GUIA COMPLETO
## Do Básico ao Avançado para Previsibilidade de Demandas

**Versão:** 1.0  
**Data:** Novembro 2025  
**Nível:** Iniciante → Intermediário → Avançado → Produção

---

## 📋 ÍNDICE

1. [Fundamentos Matemáticos](#fundamentos)
2. [Time Series Forecasting (Iniciante)](#iniciante)
3. [Ensemble Methods (Intermediário)](#intermediario)
4. [Deep Learning (Avançado)](#avancado)
5. [Pipeline Produção (Implementação)](#producao)

---

<a name="fundamentos"></a>
## 1. 📐 FUNDAMENTOS MATEMÁTICOS

### 1.1 Notação e Conceitos Base

**Notação:**
- $t$: Tempo (discreto, dias)
- $y_t$: Demanda observada no tempo $t$
- $\hat{y}_t$: Previsão da demanda no tempo $t$
- $\epsilon_t$: Erro no tempo $t$ (ruído)
- $\sigma$: Desvio padrão
- $\mu$: Média

**Operadores:**
- $B$: Backshift operator ($B y_t = y_{t-1}$)
- $\nabla$: Operador de diferença ($\nabla y_t = y_t - y_{t-1}$)
- $\Delta$: Primeira diferença ($\Delta y_t = (1-B)y_t$)

### 1.2 Métricas de Erro

**MAPE (Mean Absolute Percentage Error):**
$$\text{MAPE} = \frac{100}{n} \sum_{t=1}^{n} \left|\frac{y_t - \hat{y}_t}{y_t}\right|$$

**RMSE (Root Mean Squared Error):**
$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{t=1}^{n}(y_t - \hat{y}_t)^2}$$

**MAE (Mean Absolute Error):**
$$\text{MAE} = \frac{1}{n} \sum_{t=1}^{n}|y_t - \hat{y}_t|$$

**MASE (Mean Absolute Scaled Error):**
$$\text{MASE} = \frac{\text{MAE}}{\frac{1}{n-1}\sum_{t=2}^{n}|y_t - y_{t-1}|}$$

### 1.3 Estatística Descritiva

**Mean (Média):**
$$\bar{y} = \frac{1}{n} \sum_{t=1}^{n} y_t$$

**Variance (Variância):**
$$\sigma^2 = \frac{1}{n-1} \sum_{t=1}^{n}(y_t - \bar{y})^2$$

**Autocovariance (Autocovariância):**
$$\gamma_k = \text{Cov}(y_t, y_{t-k}) = E[(y_t - \mu)(y_{t-k} - \mu)]$$

**Autocorrelation (Autocorrelação):**
$$\rho_k = \frac{\gamma_k}{\gamma_0}$$

---

<a name="iniciante"></a>
## 2. 📊 TIME SERIES FORECASTING (INICIANTE)

### 2.1 Random Walk (Baseline)

**Formulação:**
$$y_t = y_{t-1} + \epsilon_t$$

**Previsão:**
$$\hat{y}_{t+1} = y_t$$

**Interpretação:** Previsão é igual ao último valor observado.

**Uso:** Baseline simples para comparação.

### 2.2 Simple Moving Average (SMA)

**Formulação:**
$$\hat{y}_{t+1} = \frac{1}{m} \sum_{i=0}^{m-1} y_{t-i}$$

Onde $m$ é a janela de média.

**Exemplo:** $m=7$ (média semanal)
$$\hat{y}_{t+1} = \frac{y_t + y_{t-1} + \cdots + y_{t-6}}{7}$$

**Vantagem:** Rápido, interpretável.  
**Desvantagem:** Não captura tendências.

### 2.3 Exponential Smoothing (Holt-Winters)

**Simple Exponential Smoothing:**
$$\hat{y}_{t+1} = \alpha y_t + (1-\alpha)\hat{y}_t$$

**Holt's Linear Method (Tendência):**
$$y_t = l_{t-1} + b_{t-1}$$
$$l_t = \alpha y_t + (1-\alpha)(l_{t-1} + b_{t-1})$$
$$b_t = \beta(l_t - l_{t-1}) + (1-\beta)b_{t-1}$$

**Holt-Winters (Tendência + Sazonalidade):**
$$y_t = (l_{t-1} + b_{t-1}) \cdot s_{t-m}$$
$$l_t = \alpha \frac{y_t}{s_{t-m}} + (1-\alpha)(l_{t-1} + b_{t-1})$$
$$b_t = \beta(l_t - l_{t-1}) + (1-\beta)b_{t-1}$$
$$s_t = \gamma \frac{y_t}{l_t} + (1-\gamma)s_{t-m}$$

**Parâmetros:**
- $\alpha$: Nível (0 < α < 1)
- $\beta$: Tendência (0 < β < 1)
- $\gamma$: Sazonalidade (0 < γ < 1)
- $m$: Período sazonal (7 semanal, 12 mensal)

---

### 2.4 ARIMA (AutoRegressive Integrated Moving Average)

**Formulação Geral ARIMA(p,d,q):**
$$\phi_p(B)(1-B)^d y_t = \theta_q(B) \epsilon_t$$

Onde:
- $p$: ordem AR (autoregressivo)
- $d$: ordem integração (diferenciação)
- $q$: ordem MA (média móvel)

**AR(1) - First Order Autoregressive:**
$$y_t = c + \phi_1 y_{t-1} + \epsilon_t$$

**MA(1) - First Order Moving Average:**
$$y_t = c + \epsilon_t + \theta_1 \epsilon_{t-1}$$

**ARMA(1,1) - Combined:**
$$y_t = c + \phi_1 y_{t-1} + \epsilon_t + \theta_1 \epsilon_{t-1}$$

**Estacionariedade:** Requer que as raízes de $\phi_p(B) = 0$ estejam fora do círculo unitário.

### 2.5 SARIMA (Sazonal ARIMA)

**Formulação SARIMA(p,d,q)(P,D,Q)[s]:**
$$\Phi_P(B^s) \phi_p(B)(1-B^s)^D(1-B)^d y_t = \Theta_Q(B^s)\theta_q(B)\epsilon_t$$

**Exemplo SARIMA(1,1,1)(1,1,1)[7]:**
$$(1 - \phi_1 B)(1 - \Phi_1 B^7)(1-B)(1-B^7)y_t = (1 + \theta_1 B)(1 + \Theta_1 B^7)\epsilon_t$$

**Parâmetros:**
- $(p,d,q)$: Componente não-sazonal
- $(P,D,Q)$: Componente sazonal
- $s$: Período sazonal (7=diário, 12=mensal)

**Para Nova Corrente:** SARIMA recomendado para capturar sazonalidade semanal.

---

<a name="intermediario"></a>
## 3. 🎯 ENSEMBLE METHODS (INTERMEDIÁRIO)

### 3.1 Prophet (Meta Forecasting)

**Modelo Aditivo:**
$$y_t = g(t) + s(t) + h(t) + \epsilon_t$$

**Componentes:**

**Trend (Tendência):**
$$g(t) = \beta_0 + \beta_1 t + \sum_{k=1}^{K} \gamma_k s_k(t)$$

**Sazonalidade:**
$$s(t) = \sum_{k=1}^{K} \left[ a_k \cos\left(\frac{2\pi kt}{P}\right) + b_k \sin\left(\frac{2\pi kt}{P}\right) \right]$$

**Feriados:**
$$h(t) = \sum_{i=1}^{H} \beta_{h,i} \mathbb{1}(t \in H_i)$$

**Regressores Exógenos:**
$$y_t = g(t) + s(t) + h(t) + \sum_{j=1}^{J} \beta_j x_{j,t} + \epsilon_t$$

**Vantagens:**
- Múltiplas sazonalidades automáticas
- Tolerante a missing data
- Interpretável
- Feriados customizáveis

### 3.2 Ensemble Weighted Average

**Fórmula:**
$$\hat{y}_{\text{ensemble}} = \sum_{i=1}^{M} w_i \hat{y}_i$$

**Restrição:** $\sum_{i=1}^{M} w_i = 1$

**Pesos por Performance:**
$$w_i = \frac{1/\text{MAPE}_i}{\sum_{j=1}^{M} 1/\text{MAPE}_j}$$

**Exemplo:** ARIMA(30%) + Prophet(30%) + LSTM(40%)
$$\hat{y}_{\text{final}} = 0.3 \cdot \hat{y}_{\text{ARIMA}} + 0.3 \cdot \hat{y}_{\text{Prophet}} + 0.4 \cdot \hat{y}_{\text{LSTM}}$$

### 3.3 Stacking Ensemble

**Fórmula:**
$$\hat{y}_{\text{stacked}} = f_{\text{meta}}(\hat{y}_1, \hat{y}_2, \ldots, \hat{y}_M)$$

Onde $f_{\text{meta}}$ é um modelo meta-aprendiz (ex: regressão linear).

**Implementação:**
```
Camada 1 (Base):
- Modelo 1: ARIMA
- Modelo 2: Prophet
- Modelo 3: XGBoost

Camada 2 (Meta):
- Input: Previsões Camada 1
- Output: Previsão final
- Algoritmo: Linear Regression ou MLP
```

---

<a name="avancado"></a>
## 4. 🧠 DEEP LEARNING (AVANÇADO)

### 4.1 LSTM (Long Short-Term Memory)

**Célula LSTM:**

**Forget Gate:**
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

**Input Gate:**
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$
$$\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$$

**Cell State:**
$$C_t = f_t * C_{t-1} + i_t * \tilde{C}_t$$

**Output Gate:**
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$
$$h_t = o_t * \tanh(C_t)$$

**Onde:**
- $\sigma$: Sigmoid function
- $*$: Element-wise multiplication
- $W$: Weight matrices
- $b$: Bias vectors

### 4.2 GRU (Gated Recurrent Unit) - Simplificação LSTM

**Reset Gate:**
$$r_t = \sigma(W_r \cdot [h_{t-1}, x_t])$$

**Update Gate:**
$$z_t = \sigma(W_z \cdot [h_{t-1}, x_t])$$

**Hidden State:**
$$\tilde{h}_t = \tanh(W \cdot [r_t * h_{t-1}, x_t])$$
$$h_t = (1 - z_t) * h_{t-1} + z_t * \tilde{h}_t$$

**Vantagem:** Menos parâmetros que LSTM, similar performance.

### 4.3 Attention Mechanism

**Self-Attention:**
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

**Multi-Head Attention:**
$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)W^O$$

Onde cada head:
$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

**Aplicação:** Previsão longa dependência temporal.

### 4.4 CNN-LSTM Hybrid

**Formulação:**
1. **CNN:** Extrair features locais de janela temporal
2. **LSTM:** Capturar dependências longas
3. **Dense:** Output final

**Arquitetura:**
$$h_{\text{cnn}} = \text{CNN}(x_{t-k:t})$$
$$h_{\text{lstm}} = \text{LSTM}(h_{\text{cnn}})$$
$$\hat{y}_t = \text{Dense}(h_{\text{lstm}})$$

---

<a name="producao"></a>
## 5. 🚀 PIPELINE PRODUÇÃO (IMPLEMENTAÇÃO)

### 5.1 Reorder Point (PP) Calculation

**Fórmula Base:**
$$\text{PP} = D \times L + SS$$

Onde:
- $D$: Demanda diária média (da IA)
- $L$: Lead time (dias)
- $SS$: Safety Stock

**Safety Stock Estatístico:**
$$SS = Z_{\alpha} \times \sigma_D \times \sqrt{L}$$

**Ajuste Risk Factor:**
$$SS = Z_{\alpha} \times \sigma_D \times \sqrt{L} \times RF$$

**Exemplo:** $Z_{0.95} = 1.65$, $\sigma_D = 2.5$, $L = 14$, $RF = 1.3$
$$SS = 1.65 \times 2.5 \times \sqrt{14} \times 1.3 = 18.8 \approx 19$$

### 5.2 Economic Order Quantity (EOQ)

**Fórmula Base:**
$$\text{EOQ} = \sqrt{\frac{2DS}{H}}$$

Onde:
- $D$: Demanda anual
- $S$: Custo do pedido (setup cost)
- $H$: Custo de manutenção de estoque por unidade/ano

**Com Lead Time:**
$$\text{EOQ} = \sqrt{\frac{2DS + L \times D^2}{H}}$$

### 5.3 Optimized Lead Time

**Fórmula:**
$$L_{\text{opt}} = \bar{L} + Z_{\alpha} \times \sigma_L$$

**Confidence Interval:**
$$L_{\text{adjusted}} = L_{\text{base}} \times (1 + \text{Risk Factor})$$

**Risk Factor Calculation:**
$$\text{RF} = f(\text{Clima}, \text{Econômico}, \text{Operacional})$$

---

## 📐 FÓRMULAS ESPECÍFICAS NOVA CORRENTE

### Reorder Point Completo com Fatores Externos

**Demanda Ajustada:**
$$D_{\text{adj}}(t) = \hat{D}(t) \times \prod_{i=1}^{n} M_i(t)$$

Onde $M_i(t)$ são multiplicadores de fatores externos:
- $M_{\text{clima}}(t)$: Multiplicador clima
- $M_{\text{econ}}(t)$: Multiplicador econômico
- $M_{\text{tech}}(t)$: Multiplicador tecnológico
- $M_{\text{op}}(t)$: Multiplicador operacional

**Reorder Point Final:**
$$\text{PP}(t) = D_{\text{adj}}(t) \times L_{\text{opt}} + SS(t)$$

### Intervalos de Confiança

**95% Confidence Interval:**
$$\hat{y}_t \pm 1.96 \times \sigma_{\text{forecast}}$$

**Prediction Interval:**
$$\hat{y}_t \pm t_{\alpha/2, n-2} \times s_e \times \sqrt{1 + \frac{1}{n} + \frac{(x_t - \bar{x})^2}{\sum(x_i - \bar{x})^2}}$$

---

## 🎯 RESUMO FORMULAÇÕES POR NÍVEL

**Iniciante:** SMA, Exponential Smoothing, ARIMA básico  
**Intermediário:** SARIMA, Prophet, Ensemble averaging  
**Avançado:** LSTM, GRU, Attention, CNN-LSTM  
**Produção:** PP calculation, EOQ, Confiança intervals

---

**Documento Final:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Referência Matemática Completa

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**


