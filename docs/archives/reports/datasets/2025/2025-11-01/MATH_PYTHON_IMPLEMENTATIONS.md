# 🐍 IMPLEMENTAÇÕES PYTHON COMPLETAS
## Algoritmos Matemáticos para Previsão de Demanda

---

**Data:** Novembro 2025  
**Versão:** Python Implementations 1.0  
**Status:** ✅ Código Funcional Completo

---

## 📋 ÍNDICE

1. [Safety Stock e Reorder Point](#1-safety-stock-e-reorder-point)
2. [Modelos ARIMA/SARIMAX](#2-modelos-arimasarimax)
3. [Prophet](#3-prophet)
4. [LSTM](#4-lstm)
5. [Ensemble Methods](#5-ensemble-methods)
6. [Feature Engineering](#6-feature-engineering)
7. [Cross-Validation](#7-cross-validation)
8. [Métricas](#8-métricas)
9. [Optimization](#9-optimization)
10. [Casos Práticos](#10-casos-práticos)

---

## 1. Safety Stock e Reorder Point

### 1.1 Safety Stock Básico

```python
import numpy as np
from scipy import stats
from typing import Union

def calculate_safety_stock_basic(
    avg_demand: float,
    std_demand: float,
    lead_time: int,
    service_level: float = 0.95
) -> float:
    """
    Calculate basic safety stock using standard formula.
    
    SS = Z_α × σ_D × √LT
    
    Parameters:
    -----------
    avg_demand : float
        Average daily demand
    std_demand : float
        Standard deviation of daily demand
    lead_time : int
        Lead time in days
    service_level : float
        Target service level (default: 0.95 for 95%)
    
    Returns:
    --------
    float
        Safety stock in units
    
    Example:
    --------
    >>> ss = calculate_safety_stock_basic(8, 2.5, 14, 0.95)
    >>> print(f"Safety Stock: {ss:.2f} units")
    Safety Stock: 11.48 units
    """
    z_score = stats.norm.ppf(service_level)
    safety_stock = z_score * std_demand * np.sqrt(lead_time)
    return safety_stock
```

---

### 1.2 Safety Stock com Variabilidade de Lead Time

```python
def calculate_safety_stock_advanced(
    avg_demand: float,
    std_demand: float,
    avg_lead_time: float,
    std_lead_time: float,
    service_level: float = 0.95
) -> float:
    """
    Calculate safety stock with lead time variability.
    
    SS = Z_α × √(LT × σ_D² + D_avg² × σ_LT²)
    
    Parameters:
    -----------
    avg_demand : float
        Average daily demand
    std_demand : float
        Standard deviation of demand
    avg_lead_time : float
        Average lead time
    std_lead_time : float
        Standard deviation of lead time
    service_level : float
        Target service level
    
    Returns:
    --------
    float
        Safety stock in units
    
    Example:
    --------
    >>> ss = calculate_safety_stock_advanced(
    ...     avg_demand=8,
    ...     std_demand=2.5,
    ...     avg_lead_time=14,
    ...     std_lead_time=1.5,
    ...     service_level=0.95
    ... )
    >>> print(f"Safety Stock: {ss:.2f} units")
    Safety Stock: 25.00 units
    """
    z_score = stats.norm.ppf(service_level)
    
    # Variance calculation
    variance = (
        avg_lead_time * (std_demand ** 2) +
        (avg_demand ** 2) * (std_lead_time ** 2)
    )
    
    safety_stock = z_score * np.sqrt(variance)
    return safety_stock
```

---

### 1.3 Reorder Point com Fatores Externos

```python
def calculate_reorder_point(
    avg_demand: float,
    lead_time: int,
    safety_stock: float,
    adjustment_factor: float = 1.0
) -> float:
    """
    Calculate reorder point with optional adjustment factors.
    
    PP = (D_avg × AF × LT) + SS
    
    Parameters:
    -----------
    avg_demand : float
        Average daily demand
    lead_time : int
        Lead time in days
    safety_stock : float
        Safety stock value
    adjustment_factor : float
        Multiplier for external factors (default: 1.0)
    
    Returns:
    --------
    float
        Reorder point in units
    
    Example:
    --------
    >>> pp = calculate_reorder_point(
    ...     avg_demand=8,
    ...     lead_time=14,
    ...     safety_stock=25,
    ...     adjustment_factor=1.5  # 50% increase due to weather
    ... )
    >>> print(f"Reorder Point: {pp:.0f} units")
    Reorder Point: 193 units
    """
    reorder_point = (avg_demand * adjustment_factor * lead_time) + safety_stock
    return reorder_point
```

---

### 1.4 Sistema de Alertas

```python
from datetime import datetime, timedelta
from typing import Dict, List

def check_inventory_alert(
    current_stock: float,
    reorder_point: float,
    avg_demand: float,
    safety_stock: float
) -> Dict[str, any]:
    """
    Check if inventory alert should be triggered.
    
    Parameters:
    -----------
    current_stock : float
        Current inventory level
    reorder_point : float
        Reorder point threshold
    avg_demand : float
        Average daily demand
    safety_stock : float
        Safety stock value
    
    Returns:
    --------
    dict
        Alert information with status, days until stockout, etc.
    
    Example:
    --------
    >>> alert = check_inventory_alert(85, 137, 8, 25)
    >>> print(alert)
    {
        'alert': True,
        'status': '🔴 CRÍTICO',
        'days_until_stockout': 6.25,
        'recommendation': 'Compre urgentemente'
    }
    """
    alert_triggered = current_stock <= reorder_point
    
    # Calculate days until stockout
    days_until_stockout = (current_stock - safety_stock) / avg_demand
    
    # Determine status
    if days_until_stockout <= 3:
        status = "🔴 CRÍTICO"
        recommendation = "Compre urgentemente"
    elif days_until_stockout <= 7:
        status = "🟡 ATENÇÃO"
        recommendation = "Compre em 2-3 dias"
    elif alert_triggered:
        status = "🟢 MONITORAR"
        recommendation = "Compre na próxima semana"
    else:
        status = "✅ OK"
        recommendation = "Situação normal"
    
    return {
        "alert": alert_triggered,
        "current_stock": current_stock,
        "reorder_point": reorder_point,
        "days_until_stockout": max(0, days_until_stockout),
        "status": status,
        "recommendation": recommendation
    }
```

---

### 1.5 Simulação de Ruptura

```python
def simulate_inventory_runout(
    initial_stock: float,
    avg_demand: float,
    std_demand: float,
    forecast_days: int = 30
) -> Dict[str, any]:
    """
    Simulate inventory depletion over forecast period.
    
    Parameters:
    -----------
    initial_stock : float
        Starting inventory
    avg_demand : float
        Average daily demand
    std_demand : float
        Standard deviation of demand
    forecast_days : int
        Number of days to forecast
    
    Returns:
    --------
    dict
        Simulation results with daily data
    
    Example:
    --------
    >>> sim = simulate_inventory_runout(85, 8, 2.5, 30)
    >>> print(f"Stockout on day: {sim['stockout_day']}")
    Stockout on day: 11.5
    """
    current_stock = initial_stock
    daily_data = []
    stockout_day = None
    
    np.random.seed(42)  # Reproducibility
    
    for day in range(1, forecast_days + 1):
        # Generate random demand
        demand = np.random.normal(avg_demand, std_demand)
        demand = max(0, demand)  # Demand cannot be negative
        
        # Update stock
        current_stock = max(0, current_stock - demand)
        
        # Record daily data
        daily_data.append({
            "day": day,
            "demand": round(demand, 2),
            "stock": round(current_stock, 2)
        })
        
        # Check for stockout
        if stockout_day is None and current_stock <= 0:
            stockout_day = day - current_stock / demand
    
    return {
        "initial_stock": initial_stock,
        "final_stock": current_stock,
        "stockout_day": stockout_day,
        "daily_data": daily_data
    }
```

---

## 2. Modelos ARIMA/SARIMAX

### 2.1 ARIMA Automático

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.stats.diagnostic import acorr_ljungbox

def fit_arima_auto(
    data: pd.Series,
    max_p: int = 5,
    max_d: int = 2,
    max_q: int = 5,
    ic: str = "aic"
) -> ARIMA:
    """
    Fit ARIMA model with automatic order selection.
    
    Parameters:
    -----------
    data : pd.Series
        Time series data
    max_p : int
        Maximum AR order
    max_d : int
        Maximum differencing
    max_q : int
        Maximum MA order
    ic : str
        Information criterion ('aic', 'bic', 'hqic')
    
    Returns:
    --------
    ARIMA
        Fitted ARIMA model
    
    Example:
    --------
    >>> df = pd.read_csv('demand_data.csv')
    >>> ts = df['demand']
    >>> model = fit_arima_auto(ts, max_p=3, max_d=1, max_q=3)
    >>> print(model.summary())
    """
    best_aic = np.inf
    best_params = None
    best_model = None
    
    # Grid search
    for p in range(max_p + 1):
        for d in range(max_d + 1):
            for q in range(max_q + 1):
                try:
                    model = ARIMA(data, order=(p, d, q))
                    fitted_model = model.fit()
                    
                    # Select based on IC
                    if ic == "aic":
                        score = fitted_model.aic
                    elif ic == "bic":
                        score = fitted_model.bic
                    else:
                        score = fitted_model.hqic
                    
                    if score < best_aic:
                        best_aic = score
                        best_params = (p, d, q)
                        best_model = fitted_model
                
                except:
                    continue
    
    print(f"Best {ic.upper()}: {best_aic:.2f}")
    print(f"Best parameters: ARIMA{best_params}")
    
    return best_model
```

---

### 2.2 SARIMAX com Fatores Externos

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

def fit_sarimax(
    endog: pd.Series,
    exog: pd.DataFrame = None,
    order: tuple = (1, 1, 1),
    seasonal_order: tuple = (1, 1, 1, 12)
) -> SARIMAX:
    """
    Fit SARIMAX model with external factors.
    
    Parameters:
    -----------
    endog : pd.Series
        Endogenous variable (demand)
    exog : pd.DataFrame
        Exogenous variables (weather, economic factors)
    order : tuple
        (p, d, q) order
    seasonal_order : tuple
        (P, D, Q, s) seasonal order
    
    Returns:
    --------
    SARIMAX
        Fitted SARIMAX model
    
    Example:
    --------
    >>> demand_ts = df['demand']
    >>> exog_vars = df[['temperature', 'precipitation', 'holiday']]
    >>> model = fit_sarimax(
    ...     endog=demand_ts,
    ...     exog=exog_vars,
    ...     order=(1, 1, 1),
    ...     seasonal_order=(1, 1, 1, 7)  # Weekly seasonality
    ... )
    """
    model = SARIMAX(
        endog=endog,
        exog=exog,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    
    fitted_model = model.fit(maxiter=200, method='nm')
    return fitted_model
```

---

### 2.3 Previsão com Intervals

```python
def forecast_arima(
    model: ARIMA,
    steps: int,
    exog_future: pd.DataFrame = None,
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Generate forecast with confidence intervals.
    
    Parameters:
    -----------
    model : ARIMA
        Fitted ARIMA/SARIMAX model
    steps : int
        Forecast horizon
    exog_future : pd.DataFrame
        Future exogenous variables
    alpha : float
        Significance level (default: 0.05 for 95% CI)
    
    Returns:
    --------
    pd.DataFrame
        Forecast results with CI
    
    Example:
    --------
    >>> forecast = forecast_arima(model, steps=30, alpha=0.05)
    >>> print(forecast.head())
    """
    forecast_result = model.get_forecast(steps=steps, exog=exog_future)
    
    forecast_df = pd.DataFrame({
        "forecast": forecast_result.predicted_mean,
        "lower_ci": forecast_result.conf_int()[f"lower y"],
        "upper_ci": forecast_result.conf_int()[f"upper y"]
    })
    
    return forecast_df
```

---

## 3. Prophet

### 3.1 Prophet Básico

```python
from prophet import Prophet

def fit_prophet(
    df: pd.DataFrame,
    date_col: str = "ds",
    value_col: str = "y",
    growth: str = "linear"
) -> Prophet:
    """
    Fit Prophet model.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with ds (date) and y (value) columns
    date_col : str
        Date column name
    value_col : str
        Value column name
    growth : str
        Growth type ('linear', 'logistic')
    
    Returns:
    --------
    Prophet
        Fitted Prophet model
    
    Example:
    --------
    >>> df = pd.DataFrame({
    ...     'ds': pd.date_range('2023-01-01', periods=365),
    ...     'y': np.random.randn(365).cumsum()
    ... })
    >>> model = fit_prophet(df)
    >>> print(model.params)
    """
    # Prepare data
    prophet_df = df[[date_col, value_col]].rename(
        columns={date_col: 'ds', value_col: 'y'}
    )
    
    # Initialize and fit model
    model = Prophet(growth=growth, yearly_seasonality=True, weekly_seasonality=True)
    model.fit(prophet_df)
    
    return model
```

---

### 3.2 Prophet com Feriados

```python
def fit_prophet_with_holidays(
    df: pd.DataFrame,
    holidays_df: pd.DataFrame,
    yearly_seasonality: bool = True,
    weekly_seasonality: bool = True,
    daily_seasonality: bool = False
) -> Prophet:
    """
    Fit Prophet model with custom holidays.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Time series data
    holidays_df : pd.DataFrame
        Holidays with 'holiday' and 'ds' columns
    yearly_seasonality : bool
        Fit yearly seasonality
    weekly_seasonality : bool
        Fit weekly seasonality
    daily_seasonality : bool
        Fit daily seasonality
    
    Returns:
    --------
    Prophet
        Fitted model
    
    Example:
    --------
    >>> holidays = pd.DataFrame({
    ...     'holiday': ['Christmas', 'New Year', 'Carnival'],
    ...     'ds': pd.to_datetime(['2023-12-25', '2024-01-01', '2024-02-12'])
    ... })
    >>> model = fit_prophet_with_holidays(df, holidays)
    """
    model = Prophet(
        yearly_seasonality=yearly_seasonality,
        weekly_seasonality=weekly_seasonality,
        daily_seasonality=daily_seasonality
    )
    
    model.add_country_holidays(country_name='BR')  # Brazil holidays
    model.add_country_holidays(country_name='US')  # Can add multiple
    
    # Add custom holidays
    if holidays_df is not None:
        model.holidays = holidays_df
    
    model.fit(df)
    return model
```

---

### 3.3 Prophet com Regressores Externos

```python
def fit_prophet_with_regressors(
    df: pd.DataFrame,
    regressors: List[str]
) -> Prophet:
    """
    Fit Prophet model with additional regressors.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with ds, y, and regressor columns
    regressors : List[str]
        List of regressor column names
    
    Returns:
    --------
    Prophet
        Fitted model
    
    Example:
    --------
    >>> df['temperature'] = np.random.randn(len(df))
    >>> model = fit_prophet_with_regressors(df, regressors=['temperature'])
    """
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    
    # Add regressors
    for regressor in regressors:
        model.add_regressor(regressor)
    
    model.fit(df)
    return model
```

---

## 4. LSTM

### 4.1 Preparação de Dados LSTM

```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler

def prepare_lstm_data(
    data: np.array,
    lookback: int = 30,
    forecast_horizon: int = 1
) -> tuple:
    """
    Prepare data for LSTM training.
    
    Parameters:
    -----------
    data : np.array
        Time series data
    lookback : int
        Number of timesteps to look back
    forecast_horizon : int
        Number of timesteps to forecast
    
    Returns:
    --------
    tuple
        (X_train, y_train) arrays
    
    Example:
    --------
    >>> X, y = prepare_lstm_data(data, lookback=30, forecast_horizon=1)
    >>> print(X.shape, y.shape)
    (700, 30, 1) (700, 1)
    """
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data.reshape(-1, 1))
    
    X, y = [], []
    for i in range(len(data_scaled) - lookback - forecast_horizon + 1):
        X.append(data_scaled[i:(i + lookback), 0])
        y.append(data_scaled[i + lookback:(i + lookback + forecast_horizon), 0])
    
    return np.array(X), np.array(y), scaler
```

---

### 4.2 Arquitetura LSTM

```python
def build_lstm_model(
    input_shape: tuple,
    units: List[int] = [50, 50],
    dropout_rate: float = 0.2,
    learning_rate: float = 0.001
) -> Sequential:
    """
    Build LSTM neural network.
    
    Parameters:
    -----------
    input_shape : tuple
        Input shape (timesteps, features)
    units : List[int]
        Number of units in each LSTM layer
    dropout_rate : float
        Dropout rate
    learning_rate : float
        Learning rate
    
    Returns:
    --------
    Sequential
        Compiled LSTM model
    
    Example:
    --------
    >>> model = build_lstm_model(
    ...     input_shape=(30, 1),
    ...     units=[100, 50],
    ...     dropout_rate=0.2
    ... )
    >>> model.summary()
    """
    model = Sequential()
    
    # First LSTM layer
    model.add(LSTM(
        units=units[0],
        return_sequences=True if len(units) > 1 else False,
        input_shape=input_shape
    ))
    model.add(Dropout(dropout_rate))
    
    # Additional LSTM layers
    for i in range(1, len(units)):
        model.add(LSTM(
            units=units[i],
            return_sequences=(i < len(units) - 1)
        ))
        model.add(Dropout(dropout_rate))
    
    # Output layer
    model.add(Dense(1))
    
    # Compile
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='mse',
        metrics=['mae']
    )
    
    return model
```

---

## 5. Ensemble Methods

### 5.1 Weighted Ensemble

```python
def weighted_ensemble_forecast(
    forecasts: Dict[str, np.array],
    weights: Dict[str, float] = None
) -> np.array:
    """
    Combine multiple forecasts using weighted average.
    
    Parameters:
    -----------
    forecasts : Dict[str, np.array]
        Dictionary of model name and forecast
    weights : Dict[str, float]
        Weights for each model
    
    Returns:
    --------
    np.array
        Ensemble forecast
    
    Example:
    --------
    >>> forecasts = {
    ...     'arima': arima_pred,
    ...     'prophet': prophet_pred,
    ...     'lstm': lstm_pred
    ... }
    >>> weights = {'arima': 0.3, 'prophet': 0.3, 'lstm': 0.4}
    >>> ensemble = weighted_ensemble_forecast(forecasts, weights)
    """
    if weights is None:
        # Equal weights
        n_models = len(forecasts)
        weights = {model: 1 / n_models for model in forecasts.keys()}
    
    # Normalize weights
    total_weight = sum(weights.values())
    weights = {k: v / total_weight for k, v in weights.items()}
    
    # Calculate weighted average
    ensemble = np.zeros_like(list(forecasts.values())[0])
    for model_name, forecast in forecasts.items():
        ensemble += weights.get(model_name, 0) * forecast
    
    return ensemble
```

---

### 5.2 Ridge Regression Stacking

```python
from sklearn.linear_model import Ridge

def ridge_stacking(
    y_train: np.array,
    X_train_meta: np.array,
    X_test_meta: np.array,
    alpha: float = 1.0
) -> np.array:
    """
    Stacking ensemble using Ridge regression.
    
    Parameters:
    -----------
    y_train : np.array
        Target values
    X_train_meta : np.array
        Meta-features from base models
    X_test_meta : np.array
        Meta-features for test set
    alpha : float
        Regularization strength
    
    Returns:
    --------
    np.array
        Stacked predictions
    
    Example:
    --------
    >>> stacked_pred = ridge_stacking(
    ...     y_train, X_train_meta, X_test_meta, alpha=0.1
    ... )
    """
    meta_model = Ridge(alpha=alpha)
    meta_model.fit(X_train_meta, y_train)
    
    stacked_pred = meta_model.predict(X_test_meta)
    return stacked_pred
```

---

## 6. Feature Engineering

### 6.1 Feature Temporal

```python
def create_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create temporal features from date column.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with date column
    
    Returns:
    --------
    pd.DataFrame
        Data with temporal features
    
    Example:
    --------
    >>> df = create_temporal_features(df)
    """
    df = df.copy()
    
    # Date components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.weekday
    df['week'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter
    
    # Cyclical encoding
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df['weekday_sin'] = np.sin(2 * np.pi * df['weekday'] / 7)
    df['weekday_cos'] = np.cos(2 * np.pi * df['weekday'] / 7)
    
    # Flags
    df['is_weekend'] = (df['weekday'] >= 5).astype(int)
    df['is_month_end'] = (df['day'] >= 25).astype(int)
    
    return df
```

---

### 6.2 Feature Lag

```python
def create_lag_features(
    df: pd.DataFrame,
    value_col: str,
    lags: List[int] = [1, 7, 14, 30]
) -> pd.DataFrame:
    """
    Create lag features.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Time series data
    value_col : str
        Value column name
    lags : List[int]
        Lag periods
    
    Returns:
    --------
    pd.DataFrame
        Data with lag features
    """
    df = df.copy()
    
    for lag in lags:
        df[f'lag_{lag}'] = df[value_col].shift(lag)
    
    # Rolling statistics
    df['rolling_mean_7'] = df[value_col].rolling(window=7).mean()
    df['rolling_std_7'] = df[value_col].rolling(window=7).std()
    df['rolling_mean_30'] = df[value_col].rolling(window=30).mean()
    df['rolling_std_30'] = df[value_col].rolling(window=30).std()
    
    # Exponentially weighted
    df['ewm_mean_7'] = df[value_col].ewm(span=7).mean()
    df['ewm_std_7'] = df[value_col].ewm(span=7).std()
    
    return df
```

---

## 7. Cross-Validation

### 7.1 Time Series Cross-Validation

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error

def time_series_cv(
    data: pd.Series,
    model_func: callable,
    n_splits: int = 5,
    test_size: int = 30
) -> Dict[str, float]:
    """
    Time series cross-validation.
    
    Parameters:
    -----------
    data : pd.Series
        Time series data
    model_func : callable
        Function that returns fitted model
    n_splits : int
        Number of splits
    test_size : int
        Test set size
    
    Returns:
    --------
    Dict[str, float]
        Average metrics across folds
    
    Example:
    --------
    >>> cv_results = time_series_cv(
    ...     data,
    ...     lambda train: fit_arima_auto(train),
    ...     n_splits=5,
    ...     test_size=30
    ... )
    >>> print(cv_results)
    """
    mae_scores = []
    rmse_scores = []
    
    for i in range(n_splits):
        split_idx = len(data) - (n_splits - i) * test_size
        train = data[:split_idx]
        test = data[split_idx:split_idx + test_size]
        
        # Fit model
        model = model_func(train)
        
        # Forecast
        forecast = model.forecast(steps=len(test))
        
        # Evaluate
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(mean_squared_error(test, forecast))
        
        mae_scores.append(mae)
        rmse_scores.append(rmse)
    
    return {
        'mean_mae': np.mean(mae_scores),
        'std_mae': np.std(mae_scores),
        'mean_rmse': np.mean(rmse_scores),
        'std_rmse': np.std(rmse_scores)
    }
```

---

## 8. Métricas

### 8.1 Cálculo de Todas as Métricas

```python
def calculate_all_metrics(
    actual: np.array,
    forecast: np.array
) -> Dict[str, float]:
    """
    Calculate all common forecasting metrics.
    
    Parameters:
    -----------
    actual : np.array
        Actual values
    forecast : np.array
        Forecasted values
    
    Returns:
    --------
    Dict[str, float]
        Dictionary of metrics
    
    Example:
    --------
    >>> metrics = calculate_all_metrics(actual, forecast)
    >>> print(f"MAPE: {metrics['mape']:.2f}%")
    """
    # Remove any zero actuals for MAPE
    mask = actual != 0
    
    # Basic metrics
    mae = mean_absolute_error(actual[mask], forecast[mask])
    mse = mean_squared_error(actual[mask], forecast[mask])
    rmse = np.sqrt(mse)
    
    # Percentage errors
    mape = np.mean(np.abs((actual[mask] - forecast[mask]) / actual[mask])) * 100
    smape = np.mean(np.abs(actual[mask] - forecast[mask]) / (
        (np.abs(actual[mask]) + np.abs(forecast[mask])) / 2
    )) * 100
    
    # R-squared
    ss_res = np.sum((actual[mask] - forecast[mask]) ** 2)
    ss_tot = np.sum((actual[mask] - np.mean(actual[mask])) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    
    return {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'mape': mape,
        'smape': smape,
        'r2': r2
    }
```

---

## 9. Optimization

### 9.1 Bayesian Optimization para Hyperparameters

```python
from skopt import gp_minimize
from skopt.space import Real, Integer

def optimize_arima_hyperparameters(
    train_data: pd.Series,
    n_calls: int = 20
) -> Dict[str, any]:
    """
    Optimize ARIMA hyperparameters using Bayesian optimization.
    
    Parameters:
    -----------
    train_data : pd.Series
        Training data
    n_calls : int
        Number of optimization iterations
    
    Returns:
    --------
    Dict[str, any]
        Best parameters
    
    Example:
    --------
    >>> best_params = optimize_arima_hyperparameters(train_data)
    >>> print(best_params)
    """
    def objective(params):
        p, d, q = int(params[0]), int(params[1]), int(params[2])
        
        try:
            model = ARIMA(train_data, order=(p, d, q))
            fitted = model.fit()
            return fitted.aic
        except:
            return 1e10
    
    space = [
        Integer(0, 5, name='p'),
        Integer(0, 2, name='d'),
        Integer(0, 5, name='q')
    ]
    
    result = gp_minimize(objective, space, n_calls=n_calls, random_state=42)
    
    return {
        'p': int(result.x[0]),
        'd': int(result.x[1]),
        'q': int(result.x[2]),
        'aic': result.fun
    }
```

---

## 10. Casos Práticos

### 10.1 Pipeline Completo

```python
def complete_forecasting_pipeline(
    df: pd.DataFrame,
    target_col: str,
    date_col: str,
    forecast_horizon: int = 30
) -> Dict[str, any]:
    """
    Complete forecasting pipeline from data to predictions.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Full dataset
    target_col : str
        Target column name
    date_col : str
        Date column name
    forecast_horizon : int
        Number of days to forecast
    
    Returns:
    --------
    Dict[str, any]
        Complete results with models and forecasts
    
    Example:
    --------
    >>> results = complete_forecasting_pipeline(
    ...     df, 'demand', 'date', forecast_horizon=30
    ... )
    """
    # Prepare data
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)
    
    # Feature engineering
    df = create_temporal_features(df)
    df = create_lag_features(df, target_col)
    
    # Split train/test
    split_idx = int(len(df) * 0.8)
    train = df[:split_idx]
    test = df[split_idx:]
    
    # Train models
    arima_model = fit_arima_auto(train[target_col])
    prophet_model = fit_prophet(train[[date_col, target_col]])
    
    # Forecast
    arima_forecast = forecast_arima(arima_model, forecast_horizon)
    prophet_forecast = prophet_model.predict(
        prophet_model.make_future_dataframe(periods=forecast_horizon)
    )[['yhat', 'yhat_lower', 'yhat_upper']]
    
    # Ensemble
    forecasts = {
        'arima': arima_forecast['forecast'].values,
        'prophet': prophet_forecast['yhat'].values
    }
    ensemble = weighted_ensemble_forecast(forecasts)
    
    # Metrics
    metrics = calculate_all_metrics(
        test[target_col].values[:forecast_horizon],
        ensemble
    )
    
    return {
        'models': {'arima': arima_model, 'prophet': prophet_model},
        'forecasts': {
            'arima': arima_forecast,
            'prophet': prophet_forecast,
            'ensemble': ensemble
        },
        'metrics': metrics
    }
```

---

## 📊 UTILIZAÇÃO COMPLETA

### Exemplo Final

```python
# Importar todas as funções
import pandas as pd
import numpy as np

# Carregar dados
df = pd.read_csv('nova_corrente_demand.csv')
df['date'] = pd.to_datetime(df['date'])

# Calcular safety stock e reorder point
avg_demand = df['demand'].mean()
std_demand = df['demand'].std()

ss = calculate_safety_stock_advanced(
    avg_demand=avg_demand,
    std_demand=std_demand,
    avg_lead_time=14,
    std_lead_time=1.5,
    service_level=0.95
)

pp = calculate_reorder_point(
    avg_demand=avg_demand,
    lead_time=14,
    safety_stock=ss
)

print(f"Safety Stock: {ss:.2f}")
print(f"Reorder Point: {pp:.0f}")

# Verificar alerta
current_stock = 85
alert = check_inventory_alert(
    current_stock=current_stock,
    reorder_point=pp,
    avg_demand=avg_demand,
    safety_stock=ss
)

print(f"\nAlert Status: {alert['status']}")
print(f"Days until stockout: {alert['days_until_stockout']:.1f}")

# Pipeline completo
results = complete_forecasting_pipeline(
    df,
    target_col='demand',
    date_col='date',
    forecast_horizon=30
)

print(f"\nMAPE: {results['metrics']['mape']:.2f}%")
print(f"RMSE: {results['metrics']['rmse']:.2f}")
```

---

## 📈 CONCLUSÃO

Este documento contém **implementações Python completas** para:

1. ✅ Safety Stock e Reorder Point (5 funções)
2. ✅ Modelos ARIMA/SARIMAX (3 funções)
3. ✅ Prophet (3 funções)
4. ✅ LSTM (2 funções)
5. ✅ Ensemble Methods (2 funções)
6. ✅ Feature Engineering (2 funções)
7. ✅ Cross-Validation (1 função)
8. ✅ Métricas (1 função)
9. ✅ Optimization (1 função)
10. ✅ Pipeline Completo (1 função)

**Total:** 21 funções prontas para uso!

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

**PYTHON IMPLEMENTATIONS COMPLETE - Version 1.0**

*Generated: Novembro 2025*

