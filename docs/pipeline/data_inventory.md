# Data Inventory

## Overview
Complete inventory of all data layers in the ML pipeline.

## Landing Layer (2301 files, 0 records)
**Location**: `data/landing/external_factors-raw`
**Purpose**: Raw external data from APIs and downloads
**Format**: JSON, CSV
**Update Frequency**: Daily

### Categories Available:
- - economic: 18 files
- climatic: 2270 files
- global: 6 files
- logistics: 7 files
- commodities: 0 files
- market: 0 files
- energy: 0 files

**Data Freshness**: STALE

## Silver Layer (23 files, 75,189 records)
**Location**: `data/silver/external_factors`
**Purpose**: Cleaned, normalized external data
**Format**: Parquet
**Update Frequency**: Daily

### Tables:
- - climatic/inmet_historical.parquet: 0 records, N/A
- climatic/openmeteo_daily.parquet: 7,310 records, 2021-11-11 00:00:00 to 2025-11-11 00:00:00
- global/gdp_current_usd.parquet: 4 records, N/A
- global/gdp_growth_pct.parquet: 4 records, N/A
- global/gdp_ppp.parquet: 4 records, N/A
- global/worldbank_gdp.parquet: 0 records, N/A
- logistics/anp_fuel_daily.parquet: 1,079 records, 2021-01-01 00:00:00 to 2025-06-30 00:00:00
- logistics/anp_fuel_prices.parquet: 2,158 records, 2021-01-01 00:00:00 to 2025-06-30 00:00:00
- logistics/baltic_dry.parquet: 77 records, 2022-08-31 00:00:00 to 2025-02-21 00:00:00
- logistics/baltic_dry_index.parquet: 0 records, N/A
- logistics/freight_worldbank.parquet: 2 records, 2021-01-01 00:00:00 to 2022-01-01 00:00:00
- macro/cds_spread.parquet: 12 records, 2010-01-31 00:00:00 to 2021-01-31 00:00:00
- macro/inpc_monthly.parquet: 58 records, N/A
- macro/ipca15_monthly.parquet: 58 records, N/A
- macro/ipca_inflation.parquet: 259 records, 2015-01-01 00:00:00 to 2025-10-01 00:00:00
- macro/ipca_monthly.parquet: 58 records, N/A
- macro/pib_annual_value.parquet: 7 records, N/A
- macro/pib_quarterly_yoy.parquet: 42 records, N/A
- macro/ppp_conversion_factor.parquet: 1 records, 2010-12-31 00:00:00 to 2010-12-31 00:00:00
- macro/ptax_rates.parquet: 54,288 records, 2015-01-02 00:00:00 to 2025-11-11 00:00:00
- macro/selic_daily.parquet: 1,776 records, 2021-01-01 00:00:00 to 2025-11-11 00:00:00
- macro/selic_rates.parquet: 7,935 records, 2015-01-01 00:00:00 to 2025-11-11 00:00:00
- macro/unemployment_rate.parquet: 57 records, N/A

**Data Quality**: NEEDS ATTENTION (3 issues)

## Gold Layer (11 files, 1,296,502 records)
**Location**: `data/gold/ml_features`
**Purpose**: ML-ready features with time-series and lag variables
**Format**: Parquet
**Update Frequency**: Daily

### Feature Categories:
- - climatic: 0 features
- economic: 7 features
- global: 0 features
- logistics: 0 features
- master: 44 features
- ml_ready: 9 features

**Feature Types**: ['ipca', 'selic', 'sell', 'ptax', 'price', 'anp', 'buy']

## Total Pipeline Data
- **Total Files**: 2335
- **Total Records**: 1,371,691
- **Storage Size**: ~1.0 GB (estimated)
- **ML Ready**: READY

---

*Last Updated: 2025-11-11 13:46:25*
