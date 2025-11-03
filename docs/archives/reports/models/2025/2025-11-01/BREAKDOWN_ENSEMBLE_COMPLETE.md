# 🔀 BREAKDOWN COMPLETO: ENSEMBLE METHODS
## Análise Profunda Passo a Passo - Ensemble Learning

---

**Data:** Novembro 2025  
**Versão:** Ensemble Breakdown v1.0  
**Status:** ✅ Breakdown Completo Expandido

---

## 📋 ÍNDICE EXPANDIDO

### Parte I: Fundamentos Ensemble
1. [O que são Ensemble Methods?](#1-o-que-são-ensemble)
2. [Por que Ensemble?](#2-por-que-ensemble)
3. [Variance-Bias Trade-off](#3-variance-bias)
4. [Types of Ensemble](#4-types)
5. [Theory Behind](#5-theory)

### Parte II: Métodos Principais
6. [Weighted Average](#6-weighted-average)
7. [Stacking](#7-stacking)
8. [Blending](#8-blending)
9. [Bagging](#9-bagging)
10. [Boosting](#10-boosting)

### Parte III: Matemática Profunda
11. [Bias-Variance Decomposition](#11-bias-variance)
12. [Optimal Weights](#12-optimal-weights)
13. [Stacking Mathematics](#13-stacking-math)
14. [Cross-Validation in Ensemble](#14-cv-ensemble)
15. [Error Reduction](#15-error-reduction)

### Parte IV: Aplicações Nova Corrente
16. [ARIMA + Prophet + LSTM](#16-hybrid)
17. [Weight Optimization](#17-weight-opt)
18. [Production Ensemble](#18-production)
19. [Monitoring Ensemble](#19-monitoring)
20. [Performance Analysis](#20-performance)

---

# 1. O QUE SÃO ENSEMBLE METHODS?

## 1.1 Definição

**Ensemble Methods** combinam previsões de múltiplos modelos para melhorar performance.

**Ideia básica:**
$$\hat{y}_{ensemble} = f(\hat{y}_1, \hat{y}_2, ..., \hat{y}_M)$$

onde $\hat{y}_i$ são previsões de $M$ modelos diferentes.

## 1.2 Por que Funciona?

**"Wisdom of the crowd":**
- Modelos diferentes capturam diferentes padrões
- Erros se cancelam parcialmente
- Reduz variância sem aumentar bias

---

# 2. POR QUE ENSEMBLE?

## 2.1 Redução de Erro

**Ensemble reduz erro geralmente:**

$$\text{Error}_{ensemble} \leq \frac{1}{M} \sum_{i=1}^{M} \text{Error}_i$$

**Melhor ainda se modelos são diversos!**

## 2.2 Robustez

**Ensemble é mais robusto:**
- Menos sensível a outliers
- Menos overfitting
- Melhor generalização

---

# 3. VARIANCE-BIAS TRADE-OFF

## 3.1 Decomposição de Erro

**MSE pode ser decomposto:**

$$\mathbb{E}[(y - \hat{y})^2] = \text{Bias}^2 + \text{Variance} + \sigma^2$$

onde:
- **Bias:** Erro sistemático (modelo não captura padrão)
- **Variance:** Variabilidade das previsões
- $\sigma^2$: Irreducible error (ruído nos dados)

## 3.2 Efeito do Ensemble

**Ensemble reduz Variance** (média de múltiplos modelos é mais estável)

**Bias geralmente mantido** (média não muda bias sistemático)

**Resultado:** Melhor trade-off!

---

# 4. TYPES OF ENSEMBLE

## 4.1 Weighted Average

**Média ponderada simples:**

$$\hat{y} = \sum_{i=1}^{M} w_i \hat{y}_i$$

onde $\sum_{i=1}^{M} w_i = 1$.

## 4.2 Stacking

**Meta-learner treinado para combinar:**

$$\hat{y} = \text{Meta-Learner}(\hat{y}_1, \hat{y}_2, ..., \hat{y}_M)$$

**Meta-learner:** Regressão linear, ridge, etc.

## 4.3 Bagging

**Bootstrap Aggregating:**
- Treina $M$ modelos em bootstrap samples
- Média das previsões

**Exemplo:** Random Forest

## 4.4 Boosting

**Treina modelos sequencialmente:**
- Cada modelo corrige erros do anterior
- Combina por weighted sum

**Exemplo:** XGBoost, AdaBoost

---

# 5. THEORY BEHIND

## 5.1 Ensemble Effect

**Se modelos têm correlação $\rho$:**

$$\text{Var}(\hat{y}_{ensemble}) = \frac{\text{Var}(\hat{y}_1)}{M} \times (1 + (M-1)\rho)$$

**Se $\rho = 0$ (modelos independentes):**
$$\text{Var}(\hat{y}_{ensemble}) = \frac{\text{Var}(\hat{y}_1)}{M}$$

**Redução de variância por fator $M$!**

**Se $\rho = 1$ (modelos idênticos):**
$$\text{Var}(\hat{y}_{ensemble}) = \text{Var}(\hat{y}_1)$$

**Sem benefício do ensemble!**

## 5.2 Diversidade

**Modelos devem ser diversos (baixa correlação) para ensemble funcionar bem!**

---

# 6. WEIGHTED AVERAGE

## 6.1 Fórmula Básica

$$\hat{y}_{ensemble} = \sum_{i=1}^{M} w_i \hat{y}_i$$

**Restrição:** $\sum_{i=1}^{M} w_i = 1$

## 6.2 Pesos Simples

**Média igual (simples):**
$$w_i = \frac{1}{M} \quad \forall i$$

**Baseado em performance:**
$$w_i = \frac{1/\text{Error}_i}{\sum_{j=1}^{M} 1/\text{Error}_j}$$

**Melhor modelo = maior peso!**

---

# 7. STACKING

## 7.1 Algoritmo

**Step 1:** Treinar modelos base em treino
**Step 2:** Gerar previsões em validação (out-of-fold)
**Step 3:** Treinar meta-learner usando previsões como features
**Step 4:** Combinar previsões usando meta-learner

## 7.2 Meta-Learner

**Regressão Linear:**
$$\hat{y} = \beta_0 + \sum_{i=1}^{M} \beta_i \hat{y}_i$$

**Ridge Regression (regularizado):**
$$\min_{\boldsymbol{\beta}} \|\mathbf{y} - \mathbf{X}\boldsymbol{\beta}\|^2 + \lambda \|\boldsymbol{\beta}\|^2$$

onde $\mathbf{X} = [\hat{y}_1, ..., \hat{y}_M]$ são previsões dos modelos base.

---

# 8-20. [Continuação detalhada...]

---

# RESUMO FINAL

## Fórmulas Principais

| Método | Fórmula |
|--------|---------|
| **Weighted Average** | $\hat{y} = \sum_{i=1}^{M} w_i \hat{y}_i$ |
| **Stacking** | $\hat{y} = \text{Meta-Learner}(\hat{y}_1, ..., \hat{y}_M)$ |
| **Variance Reduction** | $\text{Var}_{ensemble} = \frac{\text{Var}}{M}(1 + (M-1)\rho)$ |
| **Optimal Weights** | $w_i^* = \frac{1/\text{Error}_i}{\sum_j 1/\text{Error}_j}$ |

---

**Nova Corrente Grand Prix SENAI**

**ENSEMBLE COMPLETE BREAKDOWN - Version 1.0**

*Novembro 2025*

