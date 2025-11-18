# Feature Catalog

## Overview
Complete catalog of ML-ready features available in the gold layer.

## Economic Features

### Rate-Based Features
- **ptax_rate**: Exchange rate (BRL/USD)
  - `ptax_rate_change`: Day-over-day change
  - `ptax_rate_ma7`: 7-day moving average
  - `ptax_rate_ma30`: 30-day moving average
  - `ptax_rate_volatility`: 30-day rolling standard deviation

- **selic_rate**: SELIC interest rate
  - `selic_rate_change`: Daily change
  - `selic_rate_ma7`: 7-day average
  - `selic_rate_ma30`: 30-day average

- **ipca_index**: Inflation index
  - `ipca_index_mom`: Month-over-month change
  - `ipca_index_mom_ma12`: 12-month moving average

## Climatic Features

### Temperature Features
- **temperature_c**: Daily temperature (°C)
  - `temperature_c_lag7`: 7-day lag
  - `temperature_c_ma7`: 7-day moving average
  - `temperature_c_ma30`: 30-day moving average

### Precipitation Features
- **precipitation_mm**: Daily precipitation (mm)
  - `precipitation_rolling7`: 7-day rolling sum
  - `precipitation_rolling30`: 30-day rolling sum

## Logistics Features

### Fuel Price Features
- **fuel_price**: Fuel price (BRL/liter)
  - `fuel_price_change`: Daily change
  - `fuel_price_ma7`: 7-day average
  - `fuel_price_ma30`: 30-day average

### Shipping Index Features
- **shipping_index**: Baltic Dry Index
  - `shipping_index_change`: Daily change
  - **shipping_index_ma30**: 30-day moving average

## Market Features

### Commodity Features
- **commodity_price**: Commodity price (USD)
  - **commodity_price_change**: Daily change
  - **commodity_price_ma7**: 7-day average
  - **commodity_price_ma30**: 30-day average

### Market Index Features
- **market_index**: Stock market index
  - **market_index_change**: Daily change
  - **market_index_ma7**: 7-day average
  - `market_index_ma30`: 30-day average

## Cross-Features

### Correlation Features
- **selic_commodity_correlation**: 30-day rolling correlation
- **market_rate_correlation**: Market vs rate correlations
- **inflation_adjusted_returns**: Real returns adjusted for inflation

### Lagged Features
- **rate_lag_1d/7d/30d**: Historical rates at different lags
- **price_lag_1d/7d/30d**: Historical prices at different lags

## Feature Engineering Principles

### Time-Series Features
- **Rate of Change**: Daily percentage changes
- **Moving Averages**: 7-day, 30-day rolling averages
- **Volatility**: Rolling standard deviations
- **Trend Analysis**: Longer-term moving averages

### Lag Features
- **Short Lag**: 1-7 days (immediate impact)
- **Medium Lag**: 8-30 days (medium-term trends)
- **Seasonal Patterns**: Historical values from same period

### Correlation Features
- **Cross-Asset**: Correlations between different asset classes
- **Leading Indicators**: Economic vs market correlations
- **Risk Metrics**: Volatility and correlation measures

## Feature Quality
- **Null Rate**: < 5% for all features
- **Outlier Handling**: Winsorization at 1%/99% percentiles
- **Consistency**: Regular validation of feature ranges
- **Freshness**: Daily updates with < 24h latency

## Usage in ML Models
- **Demand Forecasting**: Primary predictors for Nova Corrente
- **Risk Modeling**: Volatility and correlation features
- **Trend Analysis**: Moving averages and lagged values
- **Scenario Planning**: Historical patterns for stress testing

---

*Feature Catalog Last Updated: 2025-11-11 13:46:25*
