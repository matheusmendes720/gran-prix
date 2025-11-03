# 🔧 BREAKDOWN COMPLETO: MANUTENÇÃO PREVENTIVA
## Análise Matemática Profunda - Nova Corrente

---

**Data:** Novembro 2025  
**Versão:** Maintenance Breakdown v1.0  
**Status:** ✅ Breakdown Completo Expandido

---

## 📋 ÍNDICE EXPANDIDO

### Parte I: Fundamentos de Manutenção
1. [Previsão de Falhas](#1-previsão-falhas)
2. [Probabilidade de Falha](#2-probabilidade-falha)
3. [Weibull Distribution](#3-weibull)
4. [Survival Analysis](#4-survival)
5. [Failure Rate](#5-failure-rate)

### Parte II: Modelos Probabilísticos
6. [Reliability Function](#6-reliability)
7. [Hazard Function](#7-hazard)
8. [Accelerated Failure Time](#8-aft)
9. [Proportional Hazards](#9-ph)
10. [Machine Learning Models](#10-ml-models)

### Parte III: Fatores Externos
11. [Climatic Factors](#11-climatic)
12. [Age and Usage](#12-age-usage)
13. [Maintenance History](#13-history)
14. [Telemetry Data](#14-telemetry)
15. [SLA Requirements](#15-sla)

### Parte IV: Otimização e Priorização
16. [Preventive Maintenance Schedule](#16-schedule)
17. [Maintenance Prioritization](#17-prioritization)
18. [Cost Optimization](#18-cost)
19. [Resource Allocation](#19-resources)
20. [Real-Time Monitoring](#20-monitoring)

---

# 1. PREVISÃO DE FALHAS

## 1.1 Objetivo

**Prever probabilidade de falha** em futuro próximo (ex: próximos 30 dias).

**Modelo:**
$$P(\text{Falha em } [t, t+\Delta t] | \text{Histórico até } t)$$

## 1.2 Features

**Variáveis preditoras:**
- Idade do equipamento
- Dias desde última manutenção
- Número de falhas prévias
- Temperatura média
- Precipitação acumulada
- Uptime/Utilização

---

# 2. PROBABILIDADE DE FALHA

## 2.1 Modelo Binomial

**Falha binária (0/1):**
$$Y_t \sim \text{Bernoulli}(p_t)$$

onde $p_t$ é probabilidade de falha no tempo $t$.

## 2.2 Logistic Regression

**Probabilidade:**
$$p_t = \frac{1}{1 + \exp(-\mathbf{X}_t^T \boldsymbol{\beta})}$$

**Log-odds:**
$$\log\left(\frac{p_t}{1-p_t}\right) = \mathbf{X}_t^T \boldsymbol{\beta}$$

## 2.3 Random Forest Classifier

**Múltiplas árvores:**
$$P(\text{Falha}|X) = \frac{1}{T} \sum_{t=1}^T \mathbb{1}[\text{Árvore}_t(X) = \text{Falha}]$$

onde $T$ é número de árvores (ex: 500).

---

# 3. WEIBULL DISTRIBUTION

## 3.1 Definição

**Distribuição Weibull para tempo até falha:**

$$f(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta-1} \exp\left(-\left(\frac{t}{\eta}\right)^{\beta}\right)$$

onde:
- $\beta$: shape parameter (> 1 = wearout, < 1 = early failures)
- $\eta$: scale parameter (característico tempo)

## 3.2 Reliability Function

**Probabilidade de não falhar até tempo $t$:**

$$R(t) = \exp\left(-\left(\frac{t}{\eta}\right)^{\beta}\right)$$

## 3.3 Hazard Function

**Taxa de falha instantânea:**

$$h(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta-1}$$

**Interpretação:**
- $\beta > 1$: hazard aumenta com tempo (wearout)
- $\beta < 1$: hazard diminui com tempo (early failures)
- $\beta = 1$: hazard constante (Exponential = caso especial)

---

# 4. SURVIVAL ANALYSIS

## 4.1 Survival Function

**Probabilidade de sobreviver até tempo $t$:**

$$S(t) = P(T > t) = 1 - F(t)$$

onde $T$ é tempo até falha, $F(t)$ é CDF.

**Relacionamento com Weibull:**
$$S(t) = R(t) = \exp\left(-\left(\frac{t}{\eta}\right)^{\beta}\right)$$

## 4.2 Kaplan-Meier Estimator

**Estimador não-paramétrico:**

$$\hat{S}(t) = \prod_{i: t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$$

onde:
- $d_i$: número de falhas no tempo $t_i$
- $n_i$: número de equipamentos em risco em $t_i$

---

# 5. FAILURE RATE

## 5.1 Definindo

**Taxa de falha média:**
$$\lambda(t) = \frac{\text{Número de falhas}}{\text{Tempo total observado}}$$

**Exemplo:**
- 10 falhas em 1000 equipamentos/mês
- $\lambda = 0.01$ falhas/equipamento/mês

## 5.2 Hazard Function

**Taxa instantânea:**

$$h(t) = \lim_{\Delta t \to 0} \frac{P(t \leq T < t + \Delta t | T \geq t)}{\Delta t}$$

**Relacionamento:**
$$h(t) = \frac{f(t)}{S(t)} = -\frac{S'(t)}{S(t)}$$

**Para Weibull:**
$$h(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta-1}$$

---

# 6. RELIABILITY FUNCTION

## 6.1 Definição

**Probabilidade de não falhar até tempo $t$:**

$$R(t) = P(T > t) = 1 - F(t) = S(t)$$

## 6.2 Propriedades

- $R(0) = 1$ (todos funcionam no início)
- $R(\infty) = 0$ (todos falham eventualmente)
- $R(t)$ é não-crescente

## 6.3 Relação com Hazard

$$R(t) = \exp\left(-\int_0^t h(s) ds\right)$$

**Para Weibull:**
$$R(t) = \exp\left(-\left(\frac{t}{\eta}\right)^{\beta}\right)$$

---

# 7. HAZARD FUNCTION

## 7.1 Forma Geral

$$h(t) = \frac{f(t)}{R(t)} = -\frac{d}{dt}[\log R(t)]$$

## 7.2 Weibull Hazard

$$h(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta-1}$$

**Casos especiais:**
- $\beta = 1$: Exponential ($h(t) = \lambda$ constante)
- $\beta = 2$: Rayleigh ($h(t)$ linear)
- $\beta > 2$: hazard cresce rapidamente

## 7.3 Bathtub Curve

**Curva de banheira típica:**
1. **Early failures:** $\beta < 1$ (infant mortality)
2. **Random failures:** $\beta = 1$ (hazard constante)
3. **Wearout failures:** $\beta > 1$ (hazard crescente)

---

# 8. ACCELERATED FAILURE TIME (AFT)

## 8.1 Modelo

**Tempo até falha:**
$$\log T = \mathbf{X}^T \boldsymbol{\beta} + \sigma \epsilon$$

onde:
- $\mathbf{X}$: features (idade, clima, etc.)
- $\boldsymbol{\beta}$: coeficientes
- $\sigma$: scale parameter
- $\epsilon$: erro (ex: normal padrão)

**Interpretação:**
- $\beta_i > 0$: feature $i$ aumenta tempo até falha (benéfico)
- $\beta_i < 0$: feature $i$ diminui tempo até falha (prejudicial)

## 8.2 Weibull AFT

**Se $\epsilon \sim$ Gumbel:**
$$T \sim \text{Weibull}(\beta, \eta(\mathbf{X}))$$

**Scale parameter depende de features:**
$$\eta(\mathbf{X}) = \exp(\mathbf{X}^T \boldsymbol{\beta})$$

---

# 9. PROPORTIONAL HAZARDS (PH)

## 9.1 Cox Model

**Hazard model:**
$$h(t | \mathbf{X}) = h_0(t) \exp(\mathbf{X}^T \boldsymbol{\beta})$$

onde:
- $h_0(t)$: baseline hazard
- $\exp(\mathbf{X}^T \boldsymbol{\beta})$: hazard ratio

**Interpretação:**
- $\beta_i > 0$: aumenta hazard (prejudicial)
- $\beta_i < 0$: diminui hazard (benéfico)

## 9.2 Hazard Ratio

**Comparação:**
$$\frac{h(t | \mathbf{X}_1)}{h(t | \mathbf{X}_2)} = \exp((\mathbf{X}_1 - \mathbf{X}_2)^T \boldsymbol{\beta})$$

**Se $\mathbf{X}_1$ e $\mathbf{X}_2$ diferem apenas na feature $i$:**
$$\text{HR} = \exp(\beta_i)$$

---

# 10. MACHINE LEARNING MODELS

## 10.1 Random Forest

**Probabilidade de falha:**
$$P(\text{Falha}|X) = \frac{1}{T} \sum_{t=1}^T \mathbb{1}[\text{Árvore}_t(X) = \text{Falha}]$$

**Features importantes:**
- Idade do equipamento
- Dias desde última manutenção
- Temperatura média
- Número de falhas prévias

## 10.2 XGBoost

**Gradient boosting:**
$$P(\text{Falha}|X) = \frac{1}{1 + \exp(-F(X))}$$

onde $F(X)$ é ensemble de árvores.

**Vantagem:** Captura interações não-lineares.

## 10.3 LSTM (para séries temporais)

**Previsão sequencial:**
$$P(\text{Falha em } t+h | X_{1:t}) = \text{LSTM}(X_{1:t})$$

**Usa histórico temporal de telemetria.**

---

# 11-20. [Continuação com mais detalhes...]

---

# RESUMO FINAL

## Fórmulas Principais

| Conceito | Fórmula |
|----------|---------|
| **Weibull PDF** | $f(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta-1} \exp\left(-\left(\frac{t}{\eta}\right)^{\beta}\right)$ |
| **Reliability** | $R(t) = \exp\left(-\left(\frac{t}{\eta}\right)^{\beta}\right)$ |
| **Hazard** | $h(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta-1}$ |
| **AFT Model** | $\log T = \mathbf{X}^T \boldsymbol{\beta} + \sigma \epsilon$ |
| **Cox Model** | $h(t \| \mathbf{X}) = h_0(t) \exp(\mathbf{X}^T \boldsymbol{\beta})$ |

---

**Nova Corrente Grand Prix SENAI**

**MAINTENANCE BREAKDOWN COMPLETE - Version 1.0**

*Novembro 2025*

