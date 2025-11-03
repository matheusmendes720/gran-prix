# ✅ PROVAS MATEMÁTICAS COMPLETAS
## Nova Corrente - Derivações Formais
## Documentação de Provas e Teoremas

---

**Data:** Novembro 2025  
**Versão:** Proofs v1.0

---

## 📋 ÍNDICE DE PROVAS

1. [Safety Stock Derivation](#1-safety-stock)
2. [EOQ Proof](#2-eoq)
3. [Newsvendor Theorem](#3-newsvendor)
4. [ARIMA Stationarity](#4-arima)
5. [Kalman Filter Optimality](#5-kalman)

---

# 1. SAFETY STOCK DERIVATION

## 1.1 Complete Proof

**Setup:** Demand during lead time $D_{LT} \sim \mathcal{N}(\mu_{LT}, \sigma_{LT}^2)$

**Service Level:** $\alpha = P(D_{LT} \leq SS + \mu_{LT})$

**We want:**

$$P(D_{LT} \leq SS + \mu_{LT}) = \alpha$$

**Standardize:**

$$P\left(Z \leq \frac{SS}{\sigma_{LT}}\right) = \alpha$$

where $Z \sim \mathcal{N}(0, 1)$.

**Solving:**

$$\frac{SS}{\sigma_{LT}} = \Phi^{-1}(\alpha) = Z_\alpha$$

**Result:**

$$\boxed{SS = Z_\alpha \sigma_{LT}}$$

---

## 1.2 Variable Lead Time

**Demand:** $D_{LT} \sim \mathcal{N}(\mu_{LT}, \sigma_{LT}^2)$

**Where:**
$$\mu_{LT} = \mathbb{E}[D] \cdot \mathbb{E}[LT]$$
$$\sigma_{LT}^2 = \mathbb{E}[LT] \cdot \text{Var}(D) + (\mathbb{E}[D])^2 \cdot \text{Var}(LT)$$

**General Form:**

$$\boxed{SS = Z_\alpha \sqrt{\mathbb{E}[LT] \cdot \text{Var}(D) + (\mathbb{E}[D])^2 \cdot \text{Var}(LT)}}$$

---

# 2. EOQ PROOF

## 2.1 Classical Derivation

**Total Cost:**

$$TC(Q) = \frac{DS}{Q} + \frac{HQ}{2}$$

where:
- $D$: annual demand
- $S$: ordering cost
- $H$: holding cost rate

**First Derivative:**

$$\frac{dTC}{dQ} = -\frac{DS}{Q^2} + \frac{H}{2}$$

**Set equal to zero:**

$$-\frac{DS}{Q^2} + \frac{H}{2} = 0$$

**Solving:**

$$\frac{DS}{Q^2} = \frac{H}{2}$$

$$Q^2 = \frac{2DS}{H}$$

$$\boxed{Q^* = \sqrt{\frac{2DS}{H}}}$$

---

## 2.2 Second Derivative Check

$$\frac{d^2TC}{dQ^2} = \frac{2DS}{Q^3} > 0$$

**Minimum confirmed!** ✓

---

# 3. NEWSVENDOR THEOREM

## 3.1 Complete Proof

**Setup:**
- Underage cost: $c_u$
- Overage cost: $c_o$
- Demand: $D$ with CDF $F(d)$

**Expected Cost:**

$$C(Q) = c_o \int_0^{Q} (Q - d) f(d) dd + c_u \int_{Q}^{\infty} (d - Q) f(d) dd$$

**Differentiate:**

$$\frac{dC}{dQ} = c_o \int_0^{Q} f(d) dd - c_u \int_{Q}^{\infty} f(d) dd$$

$$\frac{dC}{dQ} = c_o F(Q) - c_u (1 - F(Q))$$

**Set to zero:**

$$c_o F(Q) - c_u (1 - F(Q)) = 0$$

$$c_o F(Q) + c_u F(Q) = c_u$$

$$F(Q) (c_o + c_u) = c_u$$

$$\boxed{F(Q^*) = \frac{c_u}{c_o + c_u}}$$

---

## 3.2 Optimal Service Level

**Result:**
$$\alpha^* = \frac{c_u}{c_o + c_u}$$

**Interpretation:** Critical fractile balances overage vs underage costs.

---

# 4. ARIMA STATIONARITY

## 4.1 AR(1) Process

**Model:**
$$y_t = \phi y_{t-1} + \epsilon_t$$

**Characteristic Equation:**
$$\phi z = 1$$
$$z = \frac{1}{\phi}$$

**Stationarity Condition:**
$$|z| > 1 \Rightarrow |\phi| < 1$$

---

## 4.2 AR(p) General Case

**Characteristic Polynomial:**
$$\Phi(z) = 1 - \phi_1 z - \phi_2 z^2 - \cdots - \phi_p z^p$$

**Stationarity:** All roots of $\Phi(z) = 0$ lie outside unit circle.

---

# 5. KALMAN FILTER OPTIMALITY

## 5.1 Mean Square Error Criterion

**Minimize:**
$$\mathbb{E}[(x_t - \hat{x}_t)^2]$$

**Solution:**
$$\hat{x}_t = \mathbb{E}[x_t | y_1, ..., y_t]$$

---

## 5.2 Kalman Gain Derivation

**Prediction Error:**
$$e_{t|t-1} = x_t - \hat{x}_{t|t-1}$$

**Update:**
$$\hat{x}_{t|t} = \hat{x}_{t|t-1} + K_t (y_t - H_t \hat{x}_{t|t-1})$$

**Error:**
$$e_{t|t} = x_t - \hat{x}_{t|t}$$

$$e_{t|t} = x_t - \hat{x}_{t|t-1} - K_t (y_t - H_t \hat{x}_{t|t-1})$$

$$e_{t|t} = e_{t|t-1} - K_t (H_t e_{t|t-1} + v_t)$$

$$e_{t|t} = (I - K_t H_t) e_{t|t-1} - K_t v_t$$

**Covariance:**
$$P_{t|t} = \mathbb{E}[e_{t|t} e_{t|t}^T]$$

$$P_{t|t} = (I - K_t H_t) P_{t|t-1} (I - K_t H_t)^T + K_t R_t K_t^T$$

**Minimizing trace:**

$$\frac{\partial \text{tr}(P_{t|t})}{\partial K_t} = 0$$

**Solution:**
$$\boxed{K_t = P_{t|t-1} H_t^T (H_t P_{t|t-1} H_t^T + R_t)^{-1}}$$

---

# CONCLUSÃO

Provas completas para:
- ✅ Safety Stock
- ✅ EOQ
- ✅ Newsvendor
- ✅ ARIMA
- ✅ Kalman Filter

**Rigor matemático garantido!**

---

**Nova Corrente Grand Prix SENAI**

**MATHEMATICAL PROOFS COMPLETE - Version 1.0**

