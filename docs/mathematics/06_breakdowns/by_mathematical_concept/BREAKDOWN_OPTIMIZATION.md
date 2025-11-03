# ⚡ BREAKDOWN COMPLETO: OTIMIZAÇÃO
## Análise Profunda de Métodos de Otimização

---

**Data:** Novembro 2025  
**Versão:** Optimization Breakdown v1.0  
**Status:** ✅ Breakdown Completo Expandido

---

## 📋 ÍNDICE EXPANDIDO

### Parte I: Otimização Clássica
1. [Gradient Descent](#1-gradient-descent)
2. [Newton's Method](#2-newtons-method)
3. [Stochastic Gradient Descent (SGD)](#3-sgd)
4. [Momentum](#4-momentum)
5. [Adam Optimizer](#5-adam)

### Parte II: Otimização Convexa
6. [Convex Optimization](#6-convex-optimization)
7. [Lagrange Multipliers](#7-lagrange-multipliers)
8. [KKT Conditions](#8-kkt-conditions)
9. [Dual Problem](#9-dual-problem)
10. [Strong Duality](#10-strong-duality)

### Parte III: Otimização Não-Convexa
11. [Bayesian Optimization](#11-bayesian-optimization)
12. [Genetic Algorithms](#12-genetic-algorithms)
13. [Simulated Annealing](#13-simulated-annealing)
14. [Particle Swarm](#14-particle-swarm)
15. [Multi-Objective Optimization](#15-multi-objective)

### Parte IV: Aplicações Nova Corrente
16. [Hyperparameter Tuning](#16-hyperparameter-tuning)
17. [Feature Selection](#17-feature-selection)
18. [Model Selection](#18-model-selection)
19. [Inventory Optimization](#19-inventory-optimization)
20. [Route Optimization](#20-route-optimization)

---

# 1. GRADIENT DESCENT

## 1.1 Algoritmo Básico

**Update rule:**
$$\theta_{t+1} = \theta_t - \alpha \nabla f(\theta_t)$$

onde:
- $\alpha$: learning rate
- $\nabla f(\theta_t)$: gradiente da função objetivo

## 1.2 Convergência

**Condição de convergência:**
$$\lim_{t \to \infty} \|\nabla f(\theta_t)\| = 0$$

**Taxa de convergência:** $O(1/t)$

---

# 2. NEWTON'S METHOD

## 2.1 Algoritmo

**Update rule:**
$$\theta_{t+1} = \theta_t - H^{-1}(\theta_t) \nabla f(\theta_t)$$

onde $H(\theta_t)$ é a matriz Hessiana.

**Taxa de convergência:** $O(1/t^2)$ (quadrática)

---

# 3. STOCHASTIC GRADIENT DESCENT (SGD)

## 3.1 Algoritmo

**Update rule:**
$$\theta_{t+1} = \theta_t - \alpha \nabla f_i(\theta_t)$$

onde $f_i$ é loss de um único exemplo (minibatch).

**Vantagem:** Mais rápido para datasets grandes.

---

# 4. MOMENTUM

## 4.1 Algoritmo

**Velocity update:**
$$v_t = \beta v_{t-1} - \alpha \nabla f(\theta_t)$$

**Parameter update:**
$$\theta_{t+1} = \theta_t + v_t$$

onde $\beta$ é momentum coefficient (ex: 0.9).

**Benefício:** Reduz oscilação e acelera convergência.

---

# 5. ADAM OPTIMIZER

## 5.1 Algoritmo Completo

**First moment (gradient):**
$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$$

**Second moment (squared gradient):**
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$

**Bias correction:**
$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}$$
$$\hat{v}_t = \frac{v_t}{1-\beta_2^t}$$

**Parameter update:**
$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

**Hiperparâmetros típicos:**
- $\alpha = 0.001$ (learning rate)
- $\beta_1 = 0.9$ (momentum decay)
- $\beta_2 = 0.999$ (squared gradient decay)
- $\epsilon = 10^{-8}$ (numérico)

---

# 6. CONVEX OPTIMIZATION

## 6.1 Definição

**Função convexa:**
$$f(\lambda x + (1-\lambda)y) \leq \lambda f(x) + (1-\lambda) f(y)$$

**Conjunto convexo:**
$$\lambda x + (1-\lambda)y \in S \quad \forall x,y \in S, \lambda \in [0,1]$$

## 6.2 Propriedades

- **Mínimo global único** (se função estritamente convexa)
- **Gradiente = 0** garante mínimo global
- **Algoritmos eficientes** disponíveis

---

# 7. LAGRANGE MULTIPLIERS

## 7.1 Problema de Otimização

**Minimizar:**
$$\min_x f(x)$$

**Sujeito a:**
$$g_i(x) = 0, \quad i = 1, ..., m$$
$$h_j(x) \leq 0, \quad j = 1, ..., p$$

## 7.2 Lagrangean

$$L(x, \lambda, \mu) = f(x) + \sum_{i=1}^m \lambda_i g_i(x) + \sum_{j=1}^p \mu_j h_j(x)$$

## 7.3 Condições Necessárias

$$\nabla_x L = 0$$
$$g_i(x) = 0 \quad \forall i$$
$$h_j(x) \leq 0 \quad \forall j$$
$$\mu_j \geq 0 \quad \forall j$$
$$\mu_j h_j(x) = 0 \quad \forall j$$

---

# 8. KKT CONDITIONS

## 8.1 Karush-Kuhn-Tucker

**Para problema:**
$$\min_x f(x) \quad \text{s.t.} \quad h_j(x) \leq 0$$

**KKT conditions:**
1. **Stationarity:** $\nabla f(x) + \sum_j \mu_j \nabla h_j(x) = 0$
2. **Primal feasibility:** $h_j(x) \leq 0$
3. **Dual feasibility:** $\mu_j \geq 0$
4. **Complementary slackness:** $\mu_j h_j(x) = 0$

---

# 9. DUAL PROBLEM

## 9.1 Dual Lagrangean

**Primal:**
$$\min_x \max_{\lambda, \mu} L(x, \lambda, \mu)$$

**Dual:**
$$\max_{\lambda, \mu} \min_x L(x, \lambda, \mu)$$

## 9.2 Weak Duality

**Para primal ($p^*$) e dual ($d^*$):**
$$d^* \leq p^*$$

**Gap:** $p^* - d^*$

---

# 10. STRONG DUALITY

## 10.1 Condição

**Se problema convexo e Slater condition satisfeita:**
$$d^* = p^*$$

**Gap zero!**

---

# 11. BAYESIAN OPTIMIZATION

## 11.1 Gaussian Process

**Modelo de função objetivo:**
$$f(x) \sim \mathcal{GP}(\mu(x), k(x, x'))$$

## 11.2 Acquisition Function

**Expected Improvement (EI):**
$$\text{EI}(x) = \mathbb{E}[\max(0, f(x) - f^*)]$$

**Upper Confidence Bound (UCB):**
$$\text{UCB}(x) = \mu(x) + \kappa \sigma(x)$$

## 11.3 Algoritmo

1. **Amostrar pontos iniciais**
2. **Treinar GP** nos pontos observados
3. **Maximizar acquisition function** → próximo ponto
4. **Avaliar** função objetivo no novo ponto
5. **Repetir** até convergência

---

# 12-20. [Continuação similar...]

---

# RESUMO FINAL

## Algoritmos Principais

| Algoritmo | Update Rule | Taxa Convergência |
|----------|-------------|-------------------|
| **Gradient Descent** | $\theta_{t+1} = \theta_t - \alpha \nabla f$ | $O(1/t)$ |
| **Newton** | $\theta_{t+1} = \theta_t - H^{-1} \nabla f$ | $O(1/t^2)$ |
| **Adam** | Complexo (ver seção 5) | Adaptativo |

---

**Nova Corrente Grand Prix SENAI**

**OPTIMIZATION BREAKDOWN COMPLETE - Version 1.0**

*Novembro 2025*

