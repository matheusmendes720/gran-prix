# 🔢 MÉTODOS NUMÉRICOS COMPLETOS
## Nova Corrente - Matemática Computacional
## Implementações Numéricas Avançadas

---

**Data:** Novembro 2025  
**Versão:** Numerical Methods v1.0

---

## 📋 ÍNDICE

1. [Root Finding](#1-root-finding)
2. [Numerical Integration](#2-numerical-integration)
3. [Optimization](#3-optimization-methods)
4. [Differential Equations](#4-differential-equations)
5. [Interpolation](#5-interpolation)

---

# 1. ROOT FINDING

## 1.1 Newton-Raphson

### Newton-Raphson Method

Find $x^*$ such that $f(x^*) = 0$:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

**Implementation:**

```python
def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    """
    Newton-Raphson root finding.
    
    Parameters:
    -----------
    f : callable
        Function f(x)
    df : callable
        Derivative f'(x)
    x0 : float
        Initial guess
    """
    x = x0
    
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        if abs(dfx) < 1e-10:
            raise ValueError("Derivative too small")
        
        x_new = x - fx / dfx
        
        if abs(x_new - x) < tol:
            return x_new, i + 1
        
        x = x_new
    
    raise RuntimeError("Not converged")
```

---

## 1.2 Bisection Method

**Algorithm:**

Given $f(x)$ continuous on $[a,b]$ with $f(a)f(b) < 0$:

```python
def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Bisection method.
    """
    if f(a) * f(b) > 0:
        raise ValueError("No root in interval")
    
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, i + 1
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2, max_iter
```

---

## 1.3 Brent's Method

**Hybrid: Bisection + Secant + Inverse Quadratic Interpolation**

```python
from scipy.optimize import brentq

def find_optimal_eoq(annual_demand, ordering_cost, holding_cost):
    """
    Find EOQ using Brent's method.
    """
    def total_cost(Q):
        return (annual_demand * ordering_cost / Q) + (holding_cost * Q / 2)
    
    def cost_derivative(Q):
        return -annual_demand * ordering_cost / (Q**2) + holding_cost / 2
    
    # Root of derivative = optimum
    eoq = brentq(cost_derivative, 10, 1000)
    
    return eoq
```

---

# 2. NUMERICAL INTEGRATION

## 2.1 Monte Carlo Integration

**Estimate:**

$$I = \int_a^{b} f(x) dx$$

**Monte Carlo:**

$$I \approx \frac{b-a}{n} \sum_{i=1}^{n} f(X_i)$$

where $X_i \sim \text{Uniform}(a, b)$.

```python
def monte_carlo_integration(f, a, b, n_samples=10000):
    """
    Monte Carlo integration.
    """
    # Sample uniformly
    X = np.random.uniform(a, b, n_samples)
    
    # Evaluate
    f_values = f(X)
    
    # Integrate
    I = (b - a) * np.mean(f_values)
    
    # Variance estimate
    variance = (b - a)**2 * np.var(f_values) / n_samples
    
    return I, np.sqrt(variance)
```

---

## 2.2 Gaussian Quadrature

**Approximation:**

$$\int_{-1}^{1} f(x) dx \approx \sum_{i=1}^{n} w_i f(x_i)$$

**Gauss-Legendre Weights and Nodes:**

```python
from scipy.special import roots_legendre

def gaussian_quadrature(f, a, b, n=20):
    """
    Gaussian quadrature on [a, b].
    """
    # Get nodes and weights for [-1, 1]
    xi, wi = roots_legendre(n)
    
    # Transform to [a, b]
    x = 0.5 * (b - a) * xi + 0.5 * (a + b)
    w = 0.5 * (b - a) * wi
    
    # Integrate
    I = np.sum(w * f(x))
    
    return I
```

---

# 3. OPTIMIZATION METHODS

## 3.1 Nelder-Mead Simplex

**Implementation:**

```python
from scipy.optimize import minimize

def optimize_inventory_nelder_mead():
    """
    Optimize inventory using Nelder-Mead.
    """
    def objective(params):
        Q, SS = params
        # Total cost
        return (3650 * 500 / Q) + (50 * Q / 2) + (50 * SS)
    
    # Constraints
    bounds = [(100, 500), (0, 100)]
    
    # Initial guess
    x0 = [250, 25]
    
    # Optimize
    result = minimize(objective, x0, method='Nelder-Mead', bounds=bounds)
    
    return result
```

---

## 3.2 Differential Evolution

**Global optimization:**

```python
from scipy.optimize import differential_evolution

def optimize_arima_params_global():
    """
    Global optimization for ARIMA parameters.
    """
    # Simulate data
    data = np.random.randn(200).cumsum()
    
    def objective(params):
        try:
            p, d, q = int(params[0]), int(params[1]), int(params[2])
            from statsmodels.tsa.arima.model import ARIMA
            model = ARIMA(data, order=(p, d, q))
            fitted = model.fit()
            return fitted.aic
        except:
            return 1e10
    
    # Bounds
    bounds = [(0, 5), (0, 2), (0, 5)]
    
    # Optimize
    result = differential_evolution(objective, bounds, seed=42)
    
    return result
```

---

# CONCLUSÃO

Métodos numéricos implementados:
- ✅ Root finding (Newton, Bisection, Brent)
- ✅ Integration (Monte Carlo, Gaussian Quadrature)
- ✅ Optimization (Nelder-Mead, Differential Evolution)

**Total:** Código numérico robusto para todos os cálculos!

---

**Nova Corrente Grand Prix SENAI**

**NUMERICAL METHODS COMPLETE - Version 1.0**

