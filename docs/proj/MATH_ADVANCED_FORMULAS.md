# 📐 FÓRMULAS MATEMÁTICAS AVANÇADAS
## Sistema de Previsão de Demanda - Nova Corrente

---

## 🎯 1. DEMANDA E ESTOQUE - FÓRMULAS DETALHADAS

### 1.1 Demanda Agregada

**Demanda Total por Material:**
$$D_{total}(t) = \sum_{i=1}^{N_{sites}} D_{i}(t)$$

onde:
- $D_{i}(t)$ = Demanda no site $i$ no tempo $t$
- $N_{sites}$ = Número total de sites (18.000+ para Nova Corrente)

**Demanda Média Ponderada:**
$$D_{avg} = \frac{\sum_{i=1}^{n} D_i \times w_i}{\sum_{i=1}^{n} w_i}$$

onde $w_i$ são pesos (p.ex., por criticidade do site).

---

### 1.2 Safety Stock - Fórmulas Avançadas

**Safety Stock Básico:**
$$SS = Z_{\alpha} \times \sigma_D \times \sqrt{LT}$$

**Safety Stock com Variabilidade de Lead Time:**
$$SS = Z_{\alpha} \times \sqrt{LT \times \sigma_D^2 + D_{avg}^2 \times \sigma_{LT}^2}$$

onde:
- $\sigma_D$ = Desvio padrão da demanda
- $\sigma_{LT}$ = Desvio padrão do lead time
- $D_{avg}$ = Demanda média

**Safety Stock Adaptativo (com correlação):**
$$SS_{adaptive} = Z_{\alpha} \times \sigma_D \times \sqrt{LT} \times \sqrt{1 + \rho^2}$$

onde $\rho$ é o coeficiente de correlação entre demanda e lead time.

**Safety Stock Multi-Nível (para múltiplos fornecedores):**
$$SS_{multi} = \max_{j=1,...,J} \left( Z_{\alpha} \times \sigma_D^{(j)} \times \sqrt{LT^{(j)}} \right)$$

onde $J$ é o número de fornecedores alternativos.

---

### 1.3 Reorder Point - Cálculos Avançados

**Reorder Point Dinâmico:**
$$PP(t) = \left( \sum_{h=1}^{H} D_{avg}(t+h) \times w_h \right) \times LT + SS$$

onde:
- $H$ = Horizonte de previsão
- $w_h$ = Pesos temporais (médias móveis ponderadas)

**Reorder Point com Fatores Externos:**
$$PP_{adjusted}(t) = (D_{base}(t) \times AF(t) \times LT) + SS$$

$$AF(t) = 1 + \alpha_1 \cdot Climate_{impact}(t) + \alpha_2 \cdot Economic_{impact}(t) + \alpha_3 \cdot Operational_{impact}(t)$$

onde $AF(t)$ é o fator de ajuste no tempo $t$.

**Reorder Point Multi-Item (correlação entre materiais):**
$$PP_{correlated} = \sum_{i=1}^{M} PP_i + Z_{\alpha} \times \sqrt{\sum_{i=1}^{M}\sum_{j=1}^{M} \rho_{i,j} \times \sigma_i \times \sigma_j}$$

onde $\rho_{i,j}$ é a correlação entre items $i$ e $j$.

---

## 🤖 2. MODELOS ML - FÓRMULAS DETALHADAS

### 2.1 ARIMA Detalhado

**Modelo ARIMA(p,d,q) Geral:**
$$\Phi(B)(1-B)^d D_t = \Theta(B) \epsilon_t$$

onde:
- $\Phi(B) = 1 - \phi_1 B - \phi_2 B^2 - ... - \phi_p B^p$ (operador AR)
- $\Theta(B) = 1 + \theta_1 B + \theta_2 B^2 + ... + \theta_q B^q$ (operador MA)
- $B$ = Operador de defasagem: $B D_t = D_{t-1}$

**Expansão Completa:**
$$D_t = \sum_{i=1}^{p} \phi_i D_{t-i} + \sum_{j=1}^{q} \theta_j \epsilon_{t-j} + \epsilon_t$$

**ARIMA com Diferenciação:**
$$y_t = D_t - D_{t-1}$$
$$y_t = \sum_{i=1}^{p} \phi_i y_{t-i} + \sum_{j=1}^{q} \theta_j \epsilon_{t-j} + \epsilon_t$$

**Função de Autocorrelação (ACF):**
$$\rho(k) = \frac{Cov(D_t, D_{t-k})}{Var(D_t)} = \frac{E[(D_t - \mu)(D_{t-k} - \mu)]}{E[(D_t - \mu)^2]}$$

**Partial Autocorrelation Function (PACF):**
$$\phi_{kk} = \frac{Cov(D_t, D_{t-k} | D_{t-1}, ..., D_{t-k+1})}{Var(D_t | D_{t-1}, ..., D_{t-k+1})}$$

---

### 2.2 SARIMAX Detalhado

**Modelo SARIMAX(p,d,q)(P,D,Q,s):**
$$\Phi(B^s) \phi(B) (1-B^s)^D (1-B)^d D_t = \Theta(B^s) \theta(B) \epsilon_t + \sum_{j=1}^{K} \beta_j X_{j,t}$$

onde:
- $(p,d,q)$ = Ordem não-sazonal
- $(P,D,Q,s)$ = Ordem sazonal (s = período sazonal)
- $\Phi(B^s), \Theta(B^s)$ = Operadores sazonais

**Exemplo SARIMA(1,1,1)(1,1,1,7):**
$$(1 - \Phi_1 B^7)(1 - \phi_1 B)(1-B^7)(1-B)D_t = (1 + \Theta_1 B^7)(1 + \theta_1 B) \epsilon_t$$

**Expansão com Regressores:**
$$D_t = \mu + \sum_{i=1}^{p} \phi_i D_{t-i} + \sum_{j=1}^{q} \theta_j \epsilon_{t-j} + \sum_{k=1}^{P} \Phi_k D_{t-ks} + \sum_{l=1}^{Q} \Theta_l \epsilon_{t-ls} + \sum_{m=1}^{K} \beta_m X_{m,t} + \epsilon_t$$

---

### 2.3 Prophet Detalhado

**Modelo Aditivo Completo:**
$$D(t) = g(t) + s(t) + h(t) + \epsilon_t$$

**Tendência com Pontos de Mudança:**
$$g(t) = (k + \mathbf{a}(t)^T \boldsymbol{\delta}) t + (m + \mathbf{a}(t)^T \boldsymbol{\gamma})$$

onde:
$$\mathbf{a}(t) = [\mathbf{1}_{t \geq s_1}, \mathbf{1}_{t \geq s_2}, ..., \mathbf{1}_{t \geq s_j}]^T$$

É o vetor de mudanças nos tempos $s_1, s_2, ..., s_j$.

**Decomposição Sazonal com Fourier:**
$$s(t) = \sum_{n=1}^{N} \left[ a_n \cos\left(\frac{2\pi n t}{P}\right) + b_n \sin\left(\frac{2\pi n t}{P}\right) \right]$$

**Sazonalidade Anual (P=365.25):**
$$s_{yearly}(t) = \sum_{n=1}^{N} \left[ a_n \cos\left(\frac{2\pi n t}{365.25}\right) + b_n \sin\left(\frac{2\pi n t}{365.25}\right) \right]$$

**Sazonalidade Semanal (P=7):**
$$s_{weekly}(t) = \sum_{n=1}^{N} \left[ a_n \cos\left(\frac{2\pi n t}{7}\right) + b_n \sin\left(\frac{2\pi n t}{7}\right) \right]$$

**Componente de Feriados:**
$$h(t) = \sum_{i=1}^{L} \kappa_i \cdot Z_i(t)$$

onde $Z_i(t) = \mathbf{1}_{t \in [a_i, a_i + L_i]}$ para feriados com largura $L_i$ dias.

---

### 2.4 LSTM Detalhado

**Equações da Célula LSTM:**

**Forget Gate:**
$$f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)$$
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

**Input Gate:**
$$i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)$$
$$\tilde{C}_t = \tanh(W_C [h_{t-1}, x_t] + b_C)$$

**Update Cell State:**
$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

**Output Gate:**
$$o_t = \sigma(W_o [h_{t-1}, x_t] + b_o)$$
$$h_t = o_t \odot \tanh(C_t)$$

**LSTM com Peephole Connections:**
$$f_t = \sigma(W_f \cdot x_t + U_f \cdot h_{t-1} + V_f \cdot C_{t-1} + b_f)$$
$$i_t = \sigma(W_i \cdot x_t + U_i \cdot h_{t-1} + V_i \cdot C_{t-1} + b_i)$$

**LSTM Bidirecional:**
$$h_t^{forward} = LSTM^{forward}(x_t, h_{t-1}^{forward})$$
$$h_t^{backward} = LSTM^{backward}(x_t, h_{t+1}^{backward})$$
$$h_t = [h_t^{forward}, h_t^{backward}]$$

---

### 2.5 Ensemble Detalhado

**Weighted Ensemble:**
$$\hat{D}_{t+h} = \sum_{i=1}^{M} w_i \hat{D}_{i,t+h}$$

**Otimização de Pesos (Lagrange Multipliers):**
$$\mathcal{L} = \sum_{t=1}^{T} \left(D_t - \sum_{i=1}^{M} w_i \hat{D}_{i,t}\right)^2 + \lambda \left(\sum_{i=1}^{M} w_i - 1\right)$$

**Derivando e igualando a zero:**
$$\frac{\partial \mathcal{L}}{\partial w_i} = -2 \sum_{t=1}^{T} \left(D_t - \sum_{j=1}^{M} w_j \hat{D}_{j,t}\right) \hat{D}_{i,t} + \lambda = 0$$

**Solução:**
$$\mathbf{w}^* = \arg\min_{\mathbf{w}} \mathbf{w}^T \mathbf{C} \mathbf{w}$$

onde $\mathbf{C}$ é a matriz de covariância dos erros dos modelos.

**Stacking Ensemble (Meta-Learner Linear):**
$$\hat{D}_{t+h} = \beta_0 + \sum_{i=1}^{M} \beta_i \hat{D}_{i,t+h}$$

**Ridge Regression (regularização L2):**
$$\boldsymbol{\beta}^* = \arg\min_{\boldsymbol{\beta}} ||\mathbf{y} - \mathbf{X}\boldsymbol{\beta}||^2 + \alpha ||\boldsymbol{\beta}||^2$$

**Solução analítica:**
$$\boldsymbol{\beta}^* = (\mathbf{X}^T \mathbf{X} + \alpha \mathbf{I})^{-1} \mathbf{X}^T \mathbf{y}$$

---

## 📊 3. MÉTRICAS DE AVALIAÇÃO - FÓRMULAS EXPANDIDAS

### 3.1 Erros Pontuais

**Mean Absolute Error (MAE):**
$$MAE = \frac{1}{n} \sum_{i=1}^{n} |D_i - \hat{D}_i|$$

**Mean Squared Error (MSE):**
$$MSE = \frac{1}{n} \sum_{i=1}^{n} (D_i - \hat{D}_i)^2$$

**Root Mean Squared Error (RMSE):**
$$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (D_i - \hat{D}_i)^2}$$

**Mean Absolute Percentage Error (MAPE):**
$$MAPE = \frac{100}{n} \sum_{i=1}^{n} \left|\frac{D_i - \hat{D}_i}{D_i}\right|$$

**Symmetric MAPE (sMAPE):**
$$sMAPE = \frac{100}{n} \sum_{i=1}^{n} \frac{|D_i - \hat{D}_i|}{(|D_i| + |\hat{D}_i|)/2}$$

**Mean Absolute Scaled Error (MASE):**
$$MASE = \frac{MAE}{MAE_{naive}}$$

onde $MAE_{naive}$ é o MAE do modelo naive (p.ex., $D_{t+1} = D_t$).

---

### 3.2 Coeficientes

**R² (Coefficient of Determination):**
$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{\sum_{i=1}^{n} (D_i - \hat{D}_i)^2}{\sum_{i=1}^{n} (D_i - \bar{D})^2}$$

**R² Ajustado:**
$$R^2_{adj} = 1 - \frac{(1-R^2)(n-1)}{n-k-1}$$

onde $k$ é o número de parâmetros.

**Coeficiente de Correlação:**
$$r = \frac{\sum_{i=1}^{n} (D_i - \bar{D})(\hat{D}_i - \bar{\hat{D}})}{\sqrt{\sum_{i=1}^{n} (D_i - \bar{D})^2} \sqrt{\sum_{i=1}^{n} (\hat{D}_i - \bar{\hat{D}})^2}}$$

---

### 3.3 Métricas para Séries Temporais

**Diebold-Mariano Test:**
$$DM = \frac{\bar{d}}{\sigma_d / \sqrt{n}}$$

onde:
- $d_i = (e_{1,i}^2 - e_{2,i}^2)$
- $\bar{d} = \frac{1}{n}\sum_{i=1}^{n} d_i$
- $e_{1,i}, e_{2,i}$ são erros dos modelos 1 e 2

**Harvey-Leybourne-Newbold Test:**
$$HLN = \sqrt{\frac{n+1-2h+h(h-1)/n}{n}} \times DM$$

onde $h$ é o horizonte de previsão.

---

## 🔧 4. OTIMIZAÇÃO - FÓRMULAS AVANÇADAS

### 4.1 Bayesian Optimization

**Acquisition Function - Expected Improvement (EI):**
$$EI(x) = \mathbb{E}[\max(0, f^* - f(x))]$$

**Under Gaussian Process:**
$$EI(x) = \sigma(x) \left[ \Phi(Z) + Z \cdot \phi(Z) \right]$$

onde:
- $Z = \frac{f^* - \mu(x)}{\sigma(x)}$
- $\Phi, \phi$ = CDF e PDF da normal padrão
- $\mu(x), \sigma(x)$ = média e desvio da posterior GP

**Upper Confidence Bound (UCB):**
$$UCB(x) = \mu(x) + \kappa \sigma(x)$$

onde $\kappa$ controla exploration vs exploitation.

**Probability of Improvement (PI):**
$$PI(x) = \Phi\left(\frac{f^* - \mu(x)}{\sigma(x)}\right)$$

---

### 4.2 Gradient Descent Variants

**Gradient Descent:**
$$\theta_{t+1} = \theta_t - \alpha \nabla_{\theta} J(\theta_t)$$

**Momentum:**
$$v_t = \beta v_{t-1} + \alpha \nabla_{\theta} J(\theta_t)$$
$$\theta_{t+1} = \theta_t - v_t$$

**RMSprop:**
$$E[g^2]_t = \rho E[g^2]_{t-1} + (1-\rho) g_t^2$$
$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{E[g^2]_t + \epsilon}} g_t$$

**Adam (Adaptive Moment Estimation):**
$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
$$m_t^{corrected} = \frac{m_t}{1-\beta_1^t}$$
$$v_t^{corrected} = \frac{v_t}{1-\beta_2^t}$$
$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{v_t^{corrected}} + \epsilon} m_t^{corrected}$$

---

## 📈 5. TIME SERIES ANALYSIS - FÓRMULAS

### 5.1 Decomposição

**Decomposição Aditiva:**
$$D_t = T_t + S_t + R_t$$

onde:
- $T_t$ = Trend (tendência)
- $S_t$ = Seasonal (sazonalidade)
- $R_t$ = Residual (ruído)

**Decomposição Multiplicativa:**
$$D_t = T_t \times S_t \times R_t$$

**Hodrick-Prescott Filter (Trend Extraction):**
$$\min_{\{T_t\}} \sum_{t=1}^{n} (D_t - T_t)^2 + \lambda \sum_{t=2}^{n-1} [(T_{t+1} - T_t) - (T_t - T_{t-1})]^2$$

---

### 5.2 Estacionariedade

**Augmented Dickey-Fuller Test:**

Modelo:
$$\Delta y_t = \alpha + \beta t + \gamma y_{t-1} + \sum_{i=1}^{p} \phi_i \Delta y_{t-i} + \epsilon_t$$

Hipótese nula: $H_0: \gamma = 0$ (não-estacionária)
Hipótese alternativa: $H_1: \gamma < 0$ (estacionária)

---

### 5.3 Spectral Analysis

**Fourier Transform:**
$$X(f) = \int_{-\infty}^{\infty} x(t) e^{-2\pi i f t} dt$$

**Discrete Fourier Transform (DFT):**
$$X_k = \sum_{n=0}^{N-1} x_n e^{-2\pi i k n / N}$$

**Power Spectral Density:**
$$S(f) = \lim_{T \to \infty} \frac{1}{2T} \left| \int_{-T}^{T} x(t) e^{-2\pi i f t} dt \right|^2$$

---

## 🎯 6. SUPPLY CHAIN OPTIMIZATION

### 6.1 Economic Order Quantity (EOQ)

**EOQ Clássico:**
$$Q^* = \sqrt{\frac{2DS}{H}}$$

onde:
- $D$ = Demanda anual
- $S$ = Custo de pedido
- $H$ = Custo de armazenamento por unidade

**Total Cost:**
$$TC = \frac{DS}{Q} + \frac{HQ}{2}$$

**EOQ com Descontos (quantity discounts):**

Para cada faixa de preço $i$:
$$Q_i^* = \sqrt{\frac{2DS}{H}}$$

Mas se $Q_i^*$ não está na faixa $i$, usar o limite da faixa.

---

### 6.2 Multi-Item Optimization

**Knapsack Problem (budget constraint):**
$$\max \sum_{i=1}^{n} v_i x_i$$
$$\text{subject to: } \sum_{i=1}^{n} c_i x_i \leq B$$
$$x_i \in \{0, 1\}$$

onde:
- $v_i$ = valor do item $i$
- $c_i$ = custo do item $i$
- $B$ = orçamento total
- $x_i$ = escolher item $i$ (0 ou 1)

---

### 6.3 Newsvendor Problem

**Critical Fractile:**
$$F(q^*) = \frac{c_u}{c_u + c_o}$$

onde:
- $c_u$ = custo de sub-stock (underage)
- $c_o$ = custo de super-stock (overage)
- $F$ = CDF da demanda

**Quantidade Ótima:**
$$q^* = F^{-1}\left(\frac{c_u}{c_u + c_o}\right)$$

---

## 📊 7. PROBABILIDADE E ESTATÍSTICA

### 7.1 Distribuições

**Normal/Gaussiana:**
$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

**Log-Normal:**
$$f(x) = \frac{1}{x\sigma\sqrt{2\pi}} e^{-\frac{(\ln x - \mu)^2}{2\sigma^2}}$$

**Poisson (para demanda discreta):**
$$P(k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

**Gamma (para lead time):**
$$f(x) = \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}$$

---

### 7.2 Confidence Intervals

**Confidence Interval para Média:**
$$\bar{x} \pm z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$$

**Confidence Interval para Previsão:**
$$\hat{D}_{t+h} \pm z_{\alpha/2} \sqrt{\hat{\sigma}^2 + \hat{Var}(\hat{D}_{t+h})}$$

---

## 📐 8. MATRIZES E LINEAR ALGEBRA

### 8.1 Representação de Séries Temporais

**Vetor de Demanda:**
$$\mathbf{D} = [D_1, D_2, ..., D_n]^T$$

**Matriz de Features:**
$$\mathbf{X} = \begin{pmatrix}
1 & x_{1,1} & x_{1,2} & ... & x_{1,p} \\
1 & x_{2,1} & x_{2,2} & ... & x_{2,p} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_{n,1} & x_{n,2} & ... & x_{n,p}
\end{pmatrix}$$

**Regressão Linear:**
$$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$

**Least Squares Estimate:**
$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

---

### 8.2 Eigenvalue Decomposition

**Decomposição:**
$$\mathbf{A} = \mathbf{Q} \boldsymbol{\Lambda} \mathbf{Q}^T$$

onde:
- $\mathbf{Q}$ = Matriz de autovetores
- $\boldsymbol{\Lambda}$ = Matriz diagonal de autovalores

---

## ✅ CONCLUSÃO

Este documento contém **fórmulas matemáticas avançadas** para:
1. ✅ Demanda e Estoque
2. ✅ Modelos ML (ARIMA, SARIMAX, Prophet, LSTM)
3. ✅ Ensemble Methods
4. ✅ Métricas de Avaliação
5. ✅ Otimização (Bayesian, Gradient Descent)
6. ✅ Análise de Séries Temporais
7. ✅ Supply Chain Optimization
8. ✅ Probabilidade e Estatística

**Total:** 100+ fórmulas matemáticas detalhadas

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

