# 📈 BREAKDOWN COMPLETO: ARIMA
## Análise Profunda Passo a Passo - Modelo ARIMA

---

**Data:** Novembro 2025  
**Versão:** ARIMA Breakdown v1.0  
**Status:** ✅ Breakdown Completo Expandido

---

## 📋 ÍNDICE EXPANDIDO

### Parte I: Fundamentos Teóricos
1. [O que é ARIMA?](#1-o-que-é-arima)
2. [Derivação Completa das Equações](#2-derivação-completa)
3. [Condições de Estacionariedade](#3-estacionariedade)
4. [Seleção de Parâmetros (p,d,q)](#4-seleção-parâmetros)
5. [Propriedades Estatísticas](#5-propriedades-estatísticas)

### Parte II: Matemática Profunda
6. [Polinômio Característico](#6-polinômio-característico)
7. [Função de Autocorrelação (ACF)](#7-acf)
8. [Função de Autocorrelação Parcial (PACF)](#8-pacf)
9. [Likelihood Function](#9-likelihood)
10. [Método de Máxima Verossimilhança](#10-mle)

### Parte III: Implementação e Algoritmos
11. [Algoritmo de Estimação](#11-estimação)
12. [Forecasting com Erro](#12-forecasting)
13. [Intervalos de Confiança](#13-confidence-intervals)
14. [Diagnóstico do Modelo](#14-diagnóstico)
15. [Seleção Automática de Ordem](#15-auto-seleção)

### Parte IV: Aplicações Nova Corrente
16. [Demanda de Materiais](#16-aplicação-demanda)
17. [Previsão com Fatores Externos](#17-fatores-externos)
18. [Casos Práticos Resolvidos](#18-casos-práticos)
19. [Otimização de Hiperparâmetros](#19-otimização)
20. [Validação e Métricas](#20-validação)

---

# 1. O QUE É ARIMA?

## 1.1 Definição Formal

**ARIMA(p,d,q)** = AutoRegressive Integrated Moving Average

**Equação Geral:**
$$\Phi(B)(1-B)^d Y_t = \Theta(B) \epsilon_t$$

onde:
- $\Phi(B) = 1 - \phi_1 B - \phi_2 B^2 - ... - \phi_p B^p$ (AR parte)
- $\Theta(B) = 1 - \theta_1 B - \theta_2 B^2 - ... - \theta_q B^q$ (MA parte)
- $(1-B)^d$: diferenciação $d$ vezes
- $B$: operador backshift ($BY_t = Y_{t-1}$)
- $\epsilon_t \sim \mathcal{N}(0, \sigma^2)$: ruído branco

## 1.2 Componentes do ARIMA

### AutoRegressive (AR)
**Modelo AR(p):**
$$Y_t = c + \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + ... + \phi_p Y_{t-p} + \epsilon_t$$

**Forma compacta:**
$$\Phi(B) Y_t = c + \epsilon_t$$

### Integrated (I)
**Diferenciação de ordem d:**
$$W_t = (1-B)^d Y_t$$

**Para d=1:**
$$W_t = Y_t - Y_{t-1}$$

**Para d=2:**
$$W_t = (Y_t - Y_{t-1}) - (Y_{t-1} - Y_{t-2}) = Y_t - 2Y_{t-1} + Y_{t-2}$$

### Moving Average (MA)
**Modelo MA(q):**
$$Y_t = \mu + \epsilon_t + \theta_1 \epsilon_{t-1} + \theta_2 \epsilon_{t-2} + ... + \theta_q \epsilon_{t-q}$$

**Forma compacta:**
$$Y_t = \mu + \Theta(B) \epsilon_t$$

## 1.3 Breakdown Passo a Passo

### Passo 1: Verificar Estacionariedade
**Teste ADF (Augmented Dickey-Fuller):**
$$H_0: \text{Série é não-estacionária}$$
$$H_1: \text{Série é estacionária}$$

**Estatística:**
$$ADF = \frac{\hat{\rho} - 1}{SE(\hat{\rho})}$$

**Critério:** Se $p < 0.05$, rejeita $H_0$ → série estacionária.

### Passo 2: Diferenciação (se necessário)
Se não estacionária, diferencia:
$$W_t = (1-B) Y_t = Y_t - Y_{t-1}$$

**Repete até estacionária.**

### Passo 3: Identificar p e q
**Usa ACF e PACF:**

**ACF (Autocorrelation Function):**
$$\rho_k = \frac{\gamma_k}{\gamma_0} = \frac{\text{Cov}(Y_t, Y_{t-k})}{\text{Var}(Y_t)}$$

**PACF (Partial Autocorrelation):**
$$\phi_{kk} = \text{Corr}(Y_t, Y_{t-k} | Y_{t-1}, ..., Y_{t-k+1})$$

### Passo 4: Estimação de Parâmetros
**Método de Máxima Verossimilhança (MLE):**
$$\hat{\boldsymbol{\phi}}, \hat{\boldsymbol{\theta}} = \arg\max_{\phi, \theta} \mathcal{L}(\phi, \theta | \mathbf{Y})$$

---

# 2. DERIVAÇÃO COMPLETA DAS EQUAÇÕES

## 2.1 Derivação do AR(1)

### Modelo AR(1)
$$Y_t = \phi Y_{t-1} + \epsilon_t$$

### Substituição Recursiva

**Iteração 1:**
$$Y_t = \phi Y_{t-1} + \epsilon_t$$

**Iteração 2:**
$$Y_t = \phi (\phi Y_{t-2} + \epsilon_{t-1}) + \epsilon_t$$
$$Y_t = \phi^2 Y_{t-2} + \phi \epsilon_{t-1} + \epsilon_t$$

**Iteração 3:**
$$Y_t = \phi^3 Y_{t-3} + \phi^2 \epsilon_{t-2} + \phi \epsilon_{t-1} + \epsilon_t$$

### Solução Geral (k iterações)
$$Y_t = \phi^k Y_{t-k} + \sum_{i=0}^{k-1} \phi^i \epsilon_{t-i}$$

### Limite quando $k \to \infty$
**Se $|\phi| < 1$ (estacionário):**
$$Y_t = \sum_{i=0}^{\infty} \phi^i \epsilon_{t-i}$$

**Propriedades:**
- $\mathbb{E}[Y_t] = 0$
- $\text{Var}(Y_t) = \frac{\sigma^2}{1-\phi^2}$
- $\text{Cov}(Y_t, Y_{t-k}) = \phi^k \frac{\sigma^2}{1-\phi^2}$

## 2.2 Derivação do AR(2)

### Modelo AR(2)
$$Y_t = \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \epsilon_t$$

### Forma Vetorial (State Space)
$$\begin{pmatrix} Y_t \\ Y_{t-1} \end{pmatrix} = \begin{pmatrix} \phi_1 & \phi_2 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} Y_{t-1} \\ Y_{t-2} \end{pmatrix} + \begin{pmatrix} \epsilon_t \\ 0 \end{pmatrix}$$

### Condições de Estacionariedade
**Raízes do polinômio característico:**
$$1 - \phi_1 z - \phi_2 z^2 = 0$$

**Condição:** Raízes fora do círculo unitário ($|z| > 1$)

### Autocorrelação AR(2)
$$\rho_1 = \frac{\phi_1}{1-\phi_2}$$
$$\rho_k = \phi_1 \rho_{k-1} + \phi_2 \rho_{k-2}, \quad k \geq 2$$

## 2.3 Derivação do MA(1)

### Modelo MA(1)
$$Y_t = \epsilon_t + \theta \epsilon_{t-1}$$

### Propriedades Estatísticas

**Média:**
$$\mathbb{E}[Y_t] = \mathbb{E}[\epsilon_t] + \theta \mathbb{E}[\epsilon_{t-1}] = 0$$

**Variância:**
$$\text{Var}(Y_t) = \text{Var}(\epsilon_t) + \theta^2 \text{Var}(\epsilon_{t-1}) = \sigma^2(1 + \theta^2)$$

**Autocovariância:**
$$\gamma_1 = \text{Cov}(Y_t, Y_{t-1}) = \text{Cov}(\epsilon_t + \theta \epsilon_{t-1}, \epsilon_{t-1} + \theta \epsilon_{t-2})$$
$$= \theta \text{Var}(\epsilon_{t-1}) = \theta \sigma^2$$

**Autocovariância para $k > 1$:**
$$\gamma_k = 0 \quad \text{para } k > 1$$

### Função de Autocorrelação
$$\rho_1 = \frac{\theta}{1+\theta^2}$$
$$\rho_k = 0 \quad \text{para } k > 1$$

## 2.4 Derivação do ARMA(1,1)

### Modelo ARMA(1,1)
$$Y_t = \phi Y_{t-1} + \epsilon_t + \theta \epsilon_{t-1}$$

### Equação de Diferenças
$$Y_t - \phi Y_{t-1} = \epsilon_t + \theta \epsilon_{t-1}$$

### Solução usando Operador Backshift
$$(1 - \phi B) Y_t = (1 + \theta B) \epsilon_t$$

$$Y_t = \frac{1 + \theta B}{1 - \phi B} \epsilon_t$$

### Expansão em Série
**Se $|\phi| < 1$:**
$$\frac{1}{1 - \phi B} = \sum_{i=0}^{\infty} \phi^i B^i$$

$$Y_t = (1 + \theta B) \sum_{i=0}^{\infty} \phi^i B^i \epsilon_t$$

$$Y_t = \sum_{i=0}^{\infty} \psi_i \epsilon_{t-i}$$

onde:
$$\psi_0 = 1$$
$$\psi_1 = \phi + \theta$$
$$\psi_k = \phi^{k-1}(\phi + \theta), \quad k \geq 2$$

### Autocorrelação ARMA(1,1)
$$\rho_1 = \frac{(1 + \phi \theta)(\phi + \theta)}{1 + 2\phi\theta + \theta^2}$$
$$\rho_k = \phi \rho_{k-1}, \quad k \geq 2$$

---

# 3. ESTACIONARIEDADE

## 3.1 Definição

**Estacionariedade Forte (Strict Stationarity):**
Distribuição conjunta de $(Y_{t_1}, ..., Y_{t_n})$ é igual à de $(Y_{t_1+k}, ..., Y_{t_n+k})$ para todo $k$.

**Estacionariedade Fraca (Weak Stationarity):**
1. $\mathbb{E}[Y_t] = \mu$ (constante)
2. $\text{Var}(Y_t) = \sigma^2$ (constante)
3. $\text{Cov}(Y_t, Y_{t-k}) = \gamma_k$ (só depende de $k$, não de $t$)

## 3.2 Condições AR(p)

**Polinômio Característico:**
$$\Phi(z) = 1 - \phi_1 z - \phi_2 z^2 - ... - \phi_p z^p = 0$$

**Condição:** Todas as raízes de $\Phi(z) = 0$ devem estar **fora** do círculo unitário ($|z| > 1$).

### Exemplo AR(1)
$$\Phi(z) = 1 - \phi z = 0$$
$$z = \frac{1}{\phi}$$

**Condição:** $|\phi| < 1$

### Exemplo AR(2)
$$\Phi(z) = 1 - \phi_1 z - \phi_2 z^2 = 0$$

**Solução:**
$$z = \frac{\phi_1 \pm \sqrt{\phi_1^2 + 4\phi_2}}{2\phi_2}$$

**Condições:**
- $\phi_2 + \phi_1 < 1$
- $\phi_2 - \phi_1 < 1$
- $|\phi_2| < 1$

## 3.3 Condições MA(q)

**Invertibilidade:** Todas as raízes de $\Theta(z) = 0$ devem estar **fora** do círculo unitário.

**Observação:** MA(q) é sempre estacionário, mas precisa ser invertível para identificação única.

---

# 4. SELEÇÃO DE PARÂMETROS (p,d,q)

## 4.1 Critérios de Informação

### AIC (Akaike Information Criterion)
$$AIC = -2 \log(\mathcal{L}) + 2(p + q + 1)$$

**Penaliza complexidade:** Quanto menor, melhor.

### AICc (AIC Corrigido)
$$AICc = AIC + \frac{2(p+q+1)(p+q+2)}{T-p-q-2}$$

**Usa quando:** $T < 50$ (amostra pequena).

### BIC (Bayesian Information Criterion)
$$BIC = -2 \log(\mathcal{L}) + (p + q + 1) \log(T)$$

**Penalização maior** que AIC para complexidade.

### HQIC (Hannan-Quinn Information Criterion)
$$HQIC = -2 \log(\mathcal{L}) + 2(p + q + 1) \log(\log(T))$$

**Intermediário entre AIC e BIC.**

## 4.2 Método Automático (auto.arima)

**Algoritmo:**
1. **Teste de Estacionariedade:** ADF test
2. **Diferenciação:** Se necessário, diferencia até estacionária
3. **Grid Search:** Testa combinações de (p,q)
4. **Seleção:** Escolhe modelo com menor AICc

**Python (pmdarima):**
```python
from pmdarima import auto_arima

model = auto_arima(
    series,
    start_p=0, max_p=5,
    start_q=0, max_q=5,
    d=None,  # Auto-select
    seasonal=False,
    stepwise=True,
    information_criterion='aicc'
)
```

---

# 5. PROPRIEDADES ESTATÍSTICAS

## 5.1 Função de Autocovariância

### AR(1)
$$\gamma_k = \frac{\phi^k \sigma^2}{1-\phi^2}, \quad k \geq 0$$

### AR(2)
$$\gamma_0 = \frac{(1-\phi_2)\sigma^2}{(1+\phi_2)[(1-\phi_2)^2 - \phi_1^2]}$$

$$\gamma_1 = \frac{\phi_1 \sigma^2}{(1+\phi_2)[(1-\phi_2)^2 - \phi_1^2]}$$

$$\gamma_k = \phi_1 \gamma_{k-1} + \phi_2 \gamma_{k-2}, \quad k \geq 2$$

### MA(1)
$$\gamma_0 = \sigma^2(1 + \theta^2)$$
$$\gamma_1 = \theta \sigma^2$$
$$\gamma_k = 0, \quad k > 1$$

## 5.2 Função de Autocorrelação (ACF)

### AR(p)
**Decai exponencialmente** (pode oscilar se raízes complexas).

$$\rho_k = \sum_{i=1}^{p} c_i z_i^{-k}$$

onde $z_i$ são raízes do polinômio característico.

### MA(q)
**Corta após lag q:**
$$\rho_k = 0, \quad k > q$$

### ARMA(p,q)
**Decai exponencialmente após lag q** (comporta-se como AR após lag inicial).

## 5.3 Função de Autocorrelação Parcial (PACF)

### AR(p)
**Corta após lag p:**
$$\phi_{kk} = 0, \quad k > p$$

### MA(q)
**Decai exponencialmente** (comporta-se como AR após transformação).

---

# 6. POLINÔMIO CARACTERÍSTICO

## 6.1 Forma Geral

Para ARIMA(p,d,q) estacionário:
$$\Phi(B)(1-B)^d Y_t = \Theta(B) \epsilon_t$$

**Polinômio AR:**
$$\Phi(z) = 1 - \phi_1 z - ... - \phi_p z^p$$

**Polinômio MA:**
$$\Theta(z) = 1 + \theta_1 z + ... + \theta_q z^q$$

## 6.2 Fatoração

**Fatoração em raízes:**
$$\Phi(z) = \prod_{i=1}^{p} (1 - \lambda_i z)$$

onde $\lambda_i$ são inversos das raízes.

**Condição de estacionariedade:**
$$|\lambda_i| < 1 \quad \forall i$$

---

# 7. ACF (AUTOCORRELATION FUNCTION)

## 7.1 Definição

$$\rho_k = \frac{\gamma_k}{\gamma_0} = \frac{\mathbb{E}[(Y_t - \mu)(Y_{t-k} - \mu)]}{\text{Var}(Y_t)}$$

## 7.2 Estimador Amostral

$$\hat{\rho}_k = \frac{\sum_{t=k+1}^{T} (Y_t - \bar{Y})(Y_{t-k} - \bar{Y})}{\sum_{t=1}^{T} (Y_t - \bar{Y})^2}$$

## 7.3 Propriedades

- $\rho_0 = 1$
- $\rho_k = \rho_{-k}$ (simetria)
- $|\rho_k| \leq 1$

---

# 8. PACF (PARTIAL AUTOCORRELATION)

## 8.1 Definição

**Correlação parcial entre $Y_t$ e $Y_{t-k}$ após remover efeito de $Y_{t-1}, ..., Y_{t-k+1}$:**

$$\phi_{kk} = \text{Corr}(Y_t, Y_{t-k} | Y_{t-1}, ..., Y_{t-k+1})$$

## 8.2 Cálculo via Regressão

**Regressão:**
$$Y_t = \phi_{k1} Y_{t-1} + \phi_{k2} Y_{t-2} + ... + \phi_{kk} Y_{t-k} + \epsilon_t$$

**PACF = coeficiente $\phi_{kk}$.**

## 8.3 Propriedades

- $\phi_{11} = \rho_1$
- Para AR(p): $\phi_{kk} = 0$ para $k > p$
- Para MA(q): $\phi_{kk}$ decai exponencialmente

---

# 9. LIKELIHOOD FUNCTION

## 9.1 Distribuição Conjunta

**Para ARIMA(p,d,q), assumindo normalidade:**

$$\mathbf{Y} = (Y_1, ..., Y_T)^T \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$$

onde:
- $\boldsymbol{\mu} = (\mu, ..., \mu)^T$
- $\boldsymbol{\Sigma}_{ij} = \gamma_{|i-j|}$ (matriz de covariância)

## 9.2 Log-Likelihood

$$\log \mathcal{L}(\boldsymbol{\phi}, \boldsymbol{\theta}, \sigma^2 | \mathbf{Y}) = -\frac{T}{2}\log(2\pi) - \frac{1}{2}\log(|\boldsymbol{\Sigma}|) - \frac{1}{2}(\mathbf{Y} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1}(\mathbf{Y} - \boldsymbol{\mu})$$

## 9.3 Método de Máxima Verossimilhança (MLE)

**Estimadores:**
$$\hat{\boldsymbol{\phi}}, \hat{\boldsymbol{\theta}}, \hat{\sigma^2} = \arg\max_{\phi, \theta, \sigma^2} \log \mathcal{L}(\boldsymbol{\phi}, \boldsymbol{\theta}, \sigma^2 | \mathbf{Y})$$

**Resolve numericamente** (ex: método de Newton-Raphson).

---

# 10. MÉTODO DE MÁXIMA VEROSSIMILHANÇA

## 10.1 Algoritmo Iterativo

### Passo 1: Inicialização
**Valores iniciais:**
- $\boldsymbol{\phi}^{(0)} = 0$ (ou ACF/PACF)
- $\boldsymbol{\theta}^{(0)} = 0$
- $\sigma^{2(0)} = \text{Var}(\mathbf{Y})$

### Passo 2: Calcular Residuals
$$\hat{\epsilon}_t = Y_t - \hat{\mu} - \sum_{i=1}^{p} \hat{\phi}_i Y_{t-i} - \sum_{j=1}^{q} \hat{\theta}_j \hat{\epsilon}_{t-j}$$

### Passo 3: Atualizar Parâmetros
**Newton-Raphson:**
$$\boldsymbol{\theta}^{(k+1)} = \boldsymbol{\theta}^{(k)} - [\mathbf{H}(\boldsymbol{\theta}^{(k)})]^{-1} \nabla \log \mathcal{L}(\boldsymbol{\theta}^{(k)})$$

onde:
- $\nabla \log \mathcal{L}$: gradiente
- $\mathbf{H}$: Hessiana (segunda derivada)

### Passo 4: Verificar Convergência
$$\|\boldsymbol{\theta}^{(k+1)} - \boldsymbol{\theta}^{(k)}\| < \epsilon$$

## 10.2 Estimador de Variância

$$\hat{\sigma}^2 = \frac{1}{T} \sum_{t=1}^{T} \hat{\epsilon}_t^2$$

---

# 11. ALGORITMO DE ESTIMAÇÃO

## 11.1 Métodos Disponíveis

### Conditional Sum of Squares (CSS)
**Minimiza:**
$$S(\boldsymbol{\phi}, \boldsymbol{\theta}) = \sum_{t=1}^{T} \hat{\epsilon}_t^2$$

**Vantagem:** Mais rápido
**Desvantagem:** Menos eficiente que MLE

### Maximum Likelihood Estimation (MLE)
**Maximiza likelihood (preferível para amostras grandes).**

### Exact Maximum Likelihood
**Usa Kalman Filter** para likelihood exata.

## 11.2 Algoritmo Completo

```python
def estimate_arima(y, p, d, q):
    """
    Estima parâmetros ARIMA usando MLE.
    """
    # 1. Diferenciação
    if d > 0:
        y_diff = y.diff(d).dropna()
    else:
        y_diff = y
    
    # 2. Inicialização
    phi_init = np.zeros(p)
    theta_init = np.zeros(q)
    sigma2_init = y_diff.var()
    
    # 3. Otimização (Newton-Raphson)
    params = optimize.arima_params(
        y_diff, phi_init, theta_init, sigma2_init
    )
    
    # 4. Calcular residuals
    residuals = calculate_residuals(y_diff, params)
    
    # 5. Estimar variância
    sigma2 = np.mean(residuals**2)
    
    return {
        'phi': params['phi'],
        'theta': params['theta'],
        'sigma2': sigma2,
        'aic': calculate_aic(params, len(y_diff)),
        'log_likelihood': calculate_loglik(params, y_diff)
    }
```

---

# 12. FORECASTING COM ERRO

## 12.1 Previsão 1 Passo à Frente

**Para ARIMA(p,d,q):**

$$\hat{Y}_{T+1|T} = \mathbb{E}[Y_{T+1} | \mathcal{F}_T]$$

onde $\mathcal{F}_T$ é informação até tempo $T$.

### AR(1) Example
$$Y_t = \phi Y_{t-1} + \epsilon_t$$

$$\hat{Y}_{T+1|T} = \phi Y_T$$

**Erro de previsão:**
$$e_{T+1} = Y_{T+1} - \hat{Y}_{T+1|T} = \epsilon_{T+1}$$

**Variância do erro:**
$$\text{Var}(e_{T+1}) = \sigma^2$$

### ARMA(1,1) Example
$$Y_t = \phi Y_{t-1} + \epsilon_t + \theta \epsilon_{t-1}$$

$$\hat{Y}_{T+1|T} = \phi Y_T + \theta \hat{\epsilon}_T$$

## 12.2 Previsão h Passos à Frente

### AR(1) Generalizado
$$\hat{Y}_{T+h|T} = \phi^h Y_T$$

**Erro:**
$$e_{T+h} = \sum_{i=0}^{h-1} \phi^i \epsilon_{T+h-i}$$

**Variância:**
$$\text{Var}(e_{T+h}) = \sigma^2 \sum_{i=0}^{h-1} \phi^{2i} = \frac{\sigma^2(1-\phi^{2h})}{1-\phi^2}$$

**Quando $h \to \infty$:**
$$\lim_{h \to \infty} \hat{Y}_{T+h|T} = 0 \quad \text{(média incondicional)}$$
$$\lim_{h \to \infty} \text{Var}(e_{T+h}) = \frac{\sigma^2}{1-\phi^2} \quad \text{(variância incondicional)}$$

## 12.3 Método Geral (MA Representation)

**Representação MA($\infty$):**
$$Y_t = \sum_{i=0}^{\infty} \psi_i \epsilon_{t-i}$$

**Forecast h passos:**
$$\hat{Y}_{T+h|T} = \sum_{i=h}^{\infty} \psi_i \epsilon_{T+h-i}$$

**Erro:**
$$e_{T+h} = \sum_{i=0}^{h-1} \psi_i \epsilon_{T+h-i}$$

**Variância:**
$$\text{Var}(e_{T+h}) = \sigma^2 \sum_{i=0}^{h-1} \psi_i^2$$

---

# 13. INTERVALOS DE CONFIANÇA

## 13.1 Intervalo Assintótico

**Para forecast h passos à frente:**

$$\hat{Y}_{T+h|T} \pm z_{\alpha/2} \sqrt{\text{Var}(e_{T+h})}$$

onde $z_{\alpha/2}$ é quantil normal padrão (ex: 1.96 para 95% CI).

### AR(1) Example
$$\hat{Y}_{T+h|T} \pm 1.96 \sigma \sqrt{\frac{1-\phi^{2h}}{1-\phi^2}}$$

## 13.2 Cálculo da Variância

**Usando MA representation:**
$$\text{Var}(e_{T+h}) = \sigma^2 \sum_{i=0}^{h-1} \psi_i^2$$

**Coeficientes MA ($\psi_i$):**
- Resolve recursivamente usando $\phi$ e $\theta$
- Ou obtém via expansão: $Y_t = \frac{\Theta(B)}{\Phi(B)} \epsilon_t$

---

# 14. DIAGNÓSTICO DO MODELO

## 14.1 Teste de Residuals

### Ljung-Box Test
$$Q = T(T+2) \sum_{k=1}^{m} \frac{\hat{\rho}_k^2}{T-k}$$

onde $\hat{\rho}_k$ é ACF dos residuals.

**Hipótese:** Residuals são não-correlacionados (ruído branco).

**Distribuição:** $Q \sim \chi^2(m-p-q)$ sob $H_0$.

### Teste de Normalidade
**Jarque-Bera:**
$$JB = \frac{T}{6} \left(S^2 + \frac{(K-3)^2}{4}\right)$$

onde:
- $S$: assimetria (skewness)
- $K$: curtose (kurtosis)

**Distribuição:** $JB \sim \chi^2(2)$ sob $H_0$ (normalidade).

## 14.2 Análise de Residuals

### Residuals Devem Ser:
- ✅ Não-correlacionados (ACF dos residuals ≈ 0)
- ✅ Normalmente distribuídos
- ✅ Média zero
- ✅ Variância constante (homocedasticidade)

---

# 15. SELEÇÃO AUTOMÁTICA DE ORDEM

## 15.1 Algoritmo Stepwise

**auto.arima algoritmo:**

```python
def auto_arima_stepwise(series, max_p=5, max_q=5, max_d=2):
    """
    Seleção automática ARIMA.
    """
    best_model = None
    best_aicc = float('inf')
    
    # Teste de diferenciação
    d = 0
    for d_candidate in range(max_d + 1):
        diff_series = series.diff(d_candidate).dropna()
        if adf_test(diff_series) < 0.05:  # Estacionária
            d = d_candidate
            break
    
    # Grid search (p, q)
    for p in range(max_p + 1):
        for q in range(max_q + 1):
            try:
                model = ARIMA(series, order=(p, d, q))
                fitted = model.fit()
                
                if fitted.aicc < best_aicc:
                    best_aicc = fitted.aicc
                    best_model = (p, d, q)
            except:
                continue
    
    return best_model
```

---

# 16. APLICAÇÃO: DEMANDA DE MATERIAIS

## 16.1 Modelagem de Demanda

**Dados:** Consumo diário de materiais (ex: conectores)

**Modelo ARIMA:**
$$D_t = \text{ARIMA}(p, d, q) + \text{Regressores}$$

### Exemplo: ARIMA(1,1,1) + Exógenos
$$(1-B) D_t = \phi (1-B) D_{t-1} + \epsilon_t + \theta \epsilon_{t-1} + \beta_1 \text{Temp}_t + \beta_2 \text{Holiday}_t$$

### Features Exógenas
- Temperatura
- Feriados
- Dia da semana
- Sazonalidade

---

# 17. FATORES EXTERNOS

## 17.1 ARIMAX (ARIMA com Exógenos)

**Modelo:**
$$\Phi(B)(1-B)^d Y_t = \sum_{i=1}^{k} \beta_i X_{i,t} + \Theta(B) \epsilon_t$$

### Estimação
**Usa regressão linear com erros ARIMA:**

1. **Estima ARIMA** dos residuals da regressão inicial
2. **Atualiza** coeficientes $\beta_i$ considerando estrutura ARIMA
3. **Itera** até convergência

---

# 18. CASOS PRÁTICOS RESOLVIDOS

## 18.1 Exemplo 1: Demanda Diária de Conectores

**Dados:**
- 730 dias de consumo histórico
- Item: CONN-001
- Média: 8 unidades/dia
- Std: 2.5 unidades

**Passo 1: Verificar Estacionariedade**
```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(demand_series)
p_value = result[1]  # p = 0.08 > 0.05 → não estacionária
```

**Passo 2: Diferenciação**
```python
demand_diff = demand_series.diff(1).dropna()
result = adfuller(demand_diff)
p_value = result[1]  # p = 0.001 < 0.05 → estacionária
# d = 1 ✓
```

**Passo 3: ACF/PACF**
- ACF: decai exponencialmente
- PACF: corta em lag 1
- **Conclusão:** AR(1) → ARIMA(1,1,0)

**Passo 4: Estimar**
```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(demand_series, order=(1,1,0))
fitted = model.fit()

# Resultados:
# phi = 0.65
# sigma2 = 6.25
# AIC = 1450.2
```

**Passo 5: Forecast**
```python
forecast = fitted.forecast(steps=30)
# Previsão 30 dias: 8.2 ± 2.5 unidades/dia
```

---

# 19. OTIMIZAÇÃO DE HIPERPARÂMETROS

## 19.1 Grid Search

**Testa todas combinações:**
```python
best_aic = float('inf')
best_order = None

for p in range(0, 6):
    for d in range(0, 3):
        for q in range(0, 6):
            try:
                model = ARIMA(series, order=(p,d,q))
                fitted = model.fit()
                if fitted.aic < best_aic:
                    best_aic = fitted.aic
                    best_order = (p, d, q)
            except:
                continue
```

## 19.2 Bayesian Optimization

**Usa Gaussian Process para otimizar:**
- Mais eficiente que grid search
- Foco em regiões promissoras do espaço de parâmetros

---

# 20. VALIDAÇÃO E MÉTRICAS

## 20.1 Walk-Forward Validation

**Dividir temporalmente:**
- Treino: 80% inicial
- Teste: 20% final

**Re-treinar periodicamente** (ex: mensalmente).

## 20.2 Métricas de Avaliação

### MAPE (Mean Absolute Percentage Error)
$$MAPE = \frac{100}{n} \sum_{i=1}^{n} \left|\frac{Y_i - \hat{Y}_i}{Y_i}\right|$$

### RMSE (Root Mean Squared Error)
$$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (Y_i - \hat{Y}_i)^2}$$

### MAE (Mean Absolute Error)
$$MAE = \frac{1}{n} \sum_{i=1}^{n} |Y_i - \hat{Y}_i|$$

---

# RESUMO FINAL

## Equações Principais

| Conceito | Fórmula |
|----------|---------|
| **ARIMA** | $\Phi(B)(1-B)^d Y_t = \Theta(B) \epsilon_t$ |
| **AR(1)** | $Y_t = \phi Y_{t-1} + \epsilon_t$ |
| **MA(1)** | $Y_t = \epsilon_t + \theta \epsilon_{t-1}$ |
| **Forecast** | $\hat{Y}_{T+h\|T} = \sum_{i=h}^{\infty} \psi_i \epsilon_{T+h-i}$ |
| **Erro Var** | $\text{Var}(e_{T+h}) = \sigma^2 \sum_{i=0}^{h-1} \psi_i^2$ |

---

**Nova Corrente Grand Prix SENAI**

**ARIMA COMPLETE BREAKDOWN - Version 1.0**

*Novembro 2025*

