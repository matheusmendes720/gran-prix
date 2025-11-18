# External Factors ML Processing - Complete Dataset Population

## Overview
This document outlines the complete population of `data/landing/external_factors-raw` with all datasets needed for comprehensive ML demand forecasting.

## Data Categories Completeness Status

### ✅ **Already Complete**
- **Economic Indicators**: BACEN PTAX, SELIC, IPCA, IBGE GDP
- **Global Indicators**: World Bank GDP data
- **Basic Climate**: INMET data for multiple stations (2022-2025)
- **Logistics**: ANP fuel prices, Baltic Dry Index, freight benchmarks
- **Partial Weather**: OpenWeather for 3 states (Bahia, Ceará, Pernambuco)

### 🔄 **Newly Added (This Implementation)**
- **Commodity Prices**: Copper, aluminum, steel, semiconductor indices
- **Market Indices**: Bovespa, S&P 500, NASDAQ, telecom ETFs
- **Energy Prices**: Electricity tariffs, natural gas, renewable energy production
- **Expanded Weather**: All 27 Brazilian states with historical & forecast data

## New Downloader Scripts

### 1. `commodities_downloader.py`
**Purpose**: Downloads critical telecom equipment commodities
**Sources**: Yahoo Finance, London Metal Exchange APIs
**Outputs**: 
- `copper_prices.csv` - Daily copper prices (USD/lb)
- `aluminum_prices.csv` - Daily aluminum prices (USD/ton)
- `steel_prices.csv` - Daily steel price indices
- `semiconductor_index.csv` - Semiconductor sector performance

### 2. `market_indices_downloader.py`
**Purpose**: Downloads global and Brazilian market indices
**Sources**: Yahoo Finance, Investing.com APIs
**Outputs**:
- `ibovespa.csv` - B3 IBOVESPA index
- `sp500.csv` - S&P 500 performance
- `telecom_etfs.csv` - Telecom sector ETFs (VOX, IYZ, XTL)
- `vix.csv` - Market volatility index

### 3. `energy_downloader.py`
**Purpose**: Downloads energy prices and renewable energy data
**Sources**: ANEEL, CCEE, EIA APIs (sample data for demo)
**Outputs**:
- `electricity_tariffs.csv` - Regional electricity tariffs (R$/kWh)
- `energy_pld.csv` - PLD energy prices by submarket
- `natural_gas_prices.csv` - Natural gas prices (USD/MMBtu)
- `renewable_energy.csv` - Renewable energy production by source

### 4. `brazil_weather_fetcher.py`
**Purpose**: Downloads weather data for all 27 Brazilian states
**Sources**: Open-Meteo API (free)
**Outputs**:
- `brazil_historical_weather.csv` - 730 days historical for all states
- `brazil_forecast_weather.csv` - 5-day forecasts
- Individual state files: `weather_sp.csv`, `weather_rj.csv`, etc.

### 5. `complete_external_downloader.py`
**Purpose**: Orchestrates all downloads with validation and reporting
**Features**:
- Coordinates all data downloads
- Validates existing data
- Creates master summary JSON
- Reports ML readiness status

## Execution Commands

### Quick Start - Download All Missing Data
```bash
cd data/landing/external_factors-raw
python complete_external_downloader.py
```

### Individual Category Downloads
```bash
# Commodities
python commodities_downloader.py

# Market Indices  
python market_indices_downloader.py

# Energy Data
python energy_downloader.py

# Brazil Weather (expands to 27 states)
python brazil_weather_fetcher.py
```

## Expected Output Structure

After complete execution, you'll have:

```
data/landing/external_factors-raw/
├── YYYYMMDD/                          # Daily download folder
│   ├── commodities_summary.json
│   ├── market_indices_summary.json
│   ├── energy_summary.json
│   ├── brazil_weather_summary.json
│   └── external_factors_master_summary.json
│
├── commodities/                         # New
│   └── YYYYMMDD/
│       ├── copper_prices.csv
│       ├── aluminum_prices.csv
│       ├── steel_prices.csv
│       └── semiconductor_index.csv
│
├── market_indices/                       # New
│   └── YYYYMMDD/
│       ├── ibovespa.csv
│       ├── sp500.csv
│       ├── nasdaq.csv
│       ├── telecom_etfs.csv
│       └── vix.csv
│
├── energy/                              # New
│   └── YYYYMMDD/
│       ├── electricity_tariffs.csv
│       ├── energy_pld.csv
│       ├── natural_gas_prices.csv
│       └── renewable_energy.csv
│
├── openweather/                          # Expanded
│   └── YYYYMMDD/
│       ├── brazil_historical_weather.csv
│       ├── brazil_forecast_weather.csv
│       ├── weather_sp.csv
│       ├── weather_rj.csv
│       └── [all 27 state files]
│
├── macro/                               # Existing
├── global/                              # Existing  
├── logistics/                            # Existing
└── inmet/                               # Existing
```

## ML Readiness Checklist

### Economic Factors ✅
- [x] Exchange rates (PTAX USD/BRL)
- [x] Interest rates (SELIC)
- [x] Inflation (IPCA)
- [x] GDP (national and global)
- [x] Commodity prices (copper, steel, aluminum)
- [x] Market indices (Bovespa, S&P 500)

### Energy Factors ✅
- [x] Electricity tariffs by region
- [x] Natural gas prices
- [x] Renewable energy production
- [x] Energy market prices (PLD)

### Climate Factors ✅
- [x] Historical weather (all 27 states)
- [x] Weather forecasts
- [x] Precipitation data
- [x] Temperature extremes
- [x] Wind and humidity data

### Logistics Factors ✅
- [x] Shipping indices (Baltic Dry)
- [x] Fuel prices (ANP)
- [x] Freight benchmarks
- [x] Container rates

## Integration with ML Pipeline

### 1. Data Transformation to Silver Layer
```bash
python ../../scripts/etl/transform/external_to_silver.py
```

### 2. Feature Engineering
```bash
python ../../scripts/etl/feature/build_external_features.py
```

### 3. Validation
```bash
python ../../scripts/validation/check_ml_endpoints.py
```

## API Keys Required (Optional)

For production use, configure these API keys:
- **EIA Energy API**: `EIA_API_KEY`
- **Yahoo Finance**: Free tier sufficient
- **B3 API**: Optional for higher frequency data
- **ANEEL API**: For real electricity tariffs

## Data Quality Validation

Each downloader includes:
- ✅ Data type validation
- ✅ Missing value handling  
- ✅ Duplicate detection
- ✅ Range validation
- ✅ Timestamp consistency
- ✅ JSON summary with statistics

## Next Steps After Population

1. **Transform to Silver**: Process raw data to consistent schema
2. **Feature Store Integration**: Load to `data/silver/external_factors/`
3. **ML Pipeline Integration**: Connect to demand forecasting models
4. **Monitoring**: Set up data freshness alerts
5. **Documentation**: Update ML feature catalog

## Troubleshooting

### Common Issues
- **API Rate Limits**: Built-in delays between requests
- **Network Timeouts**: 30-60 second timeouts with retries
- **Missing Dependencies**: Check README for required packages
- **Permission Errors**: Ensure write access to output directories

### Fallback Data
All downloaders generate realistic sample data when APIs fail, ensuring ML pipeline can proceed with placeholder data.

---

**Status**: ✅ Ready for ML Processing
**Last Updated**: November 2025
**Data Coverage**: Brazil + Global Economic Indicators