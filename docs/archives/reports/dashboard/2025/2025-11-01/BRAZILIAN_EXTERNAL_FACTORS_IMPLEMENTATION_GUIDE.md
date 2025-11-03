# 🇧🇷 Brazilian External Factors Integration Guide

## Nova Corrente Demand Forecasting System - Grand Prix SENAI

**Status:** 📋 **IMPLEMENTATION PLAN**  
**Priority:** High - Integrate real Brazilian data sources for accurate forecasting

---

## 📊 Overview

This guide provides implementation details for integrating **real Brazilian external factors** into the demand forecasting system, replacing placeholder data with actual data from Brazilian regulatory agencies and data providers.

**Current State:**
- ✅ External factors structure implemented (22 factors)
- ⚠️ Using placeholder/simulated data
- 🎯 **Goal:** Replace with real Brazilian data sources

**Impact:**
- Improve forecasting accuracy by 20-30% (based on research)
- Enable scenario planning for Brazilian-specific events
- Support long-tail demand forecasting in rural areas
- Reduce inventory stockouts by 50-60%

---

## 🌦️ Climate Data Integration (INMET)

### Data Source

**Instituto Nacional de Meteorologia (INMET)**  
**URL:** https://www.inmet.gov.br/  
**Data Portal:** https://portal.inmet.gov.br/

### Implementation Strategy

#### Option 1: INMET API (Recommended if Available)

```python
# src/pipeline/brazilian_apis.py

import requests
from datetime import datetime, timedelta
import pandas as pd

class INMETClimateDataFetcher:
    """Fetch climate data from INMET for Brazilian regions"""
    
    def __init__(self, station_code: str):
        self.station_code = station_code  # e.g., "A601" for Salvador
        self.base_url = "https://portal.inmet.gov.br/"
    
    def fetch_hourly_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch hourly climate data for date range"""
        # Implementation depends on INMET API structure
        # May need to use web scraping or portal downloads
        pass
    
    def fetch_daily_summary(self, date: str) -> dict:
        """Fetch daily climate summary"""
        # Temperature, precipitation, humidity
        pass

# Example usage for Salvador, Bahia
salvador_fetcher = INMETClimateDataFetcher("A601")  # Salvador station
climate_data = salvador_fetcher.fetch_daily_summary("2024-01-15")
```

#### Option 2: Direct CSV Download

If API is not available, use web scraping to download CSV files:

```python
# Alternative: Web scraping from INMET portal
from bs4 import BeautifulSoup

def download_inmet_csv(station_code: str, year: int) -> pd.DataFrame:
    """Download INMET data as CSV from portal"""
    url = f"https://portal.inmet.gov.br/uploads/dadoshistoricos/{year}.zip"
    # Download and extract CSV files
    # Parse station-specific data
    pass
```

### Stations for Nova Corrente Operations

| Region | Station Code | Coverage Area |
|--------|--------------|---------------|
| Salvador, BA | A601 | Main operations center |
| São Paulo, SP | A701 | Metro operations |
| Rio de Janeiro, RJ | A603 | Secondary operations |

### Data Fields to Extract

- **Temperature** (min, max, average) - Celsius
- **Precipitation** (mm/day)
- **Humidity** (%)
- **Wind Speed** (km/h)
- **Extreme Weather Flags** (storms, floods, heatwaves)

### Integration Points

**File:** `src/pipeline/add_external_factors.py`  
**Method:** `add_climate_factors()`

```python
def add_climate_factors(self, df: pd.DataFrame) -> pd.DataFrame:
    """Add climate factors from INMET"""
    from src.pipeline.brazilian_apis import INMETClimateDataFetcher
    
    logger.info("Fetching climate data from INMET...")
    
    # Map site_id to INMET station codes
    station_map = {
        'SALVADOR': 'A601',
        'SAO_PAULO': 'A701',
        'RIO': 'A603'
    }
    
    # Fetch real data for each region
    for site_id, station_code in station_map.items():
        fetcher = INMETClimateDataFetcher(station_code)
        # Fetch and merge data
        climate_df = fetcher.fetch_daily_summary(df['date'])
        df = df.merge(climate_df, on='date', how='left')
    
    return df
```

---

## 💰 Economic Data Integration (BACEN / IBGE)

### Data Sources

**Banco Central do Brasil (BACEN)**  
**URL:** https://www.bcb.gov.br/  
**Economic Data API:** https://www.bcb.gov.br/en/htms/publicsdin/pxweb_internet.asp

**Instituto Brasileiro de Geografia e Estatística (IBGE)**  
**URL:** https://www.ibge.gov.br/  
**API:** https://servicodados.ibge.gov.br/api/docs

### Implementation Strategy

#### BACEN - Exchange Rate & Inflation

```python
class BACENEconomicDataFetcher:
    """Fetch economic data from BACEN"""
    
    def __init__(self):
        self.base_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs."
    
    def fetch_exchange_rate(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch USD/BRL exchange rate"""
        # Series code: 1 (USD exchange rate)
        series_id = "1"
        url = f"{self.base_url}{series_id}/dados?formato=json&dataInicial={start_date}&dataFinal={end_date}"
        
        response = requests.get(url)
        data = response.json()
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df.rename(columns={'valor': 'exchange_rate_brl_usd'}, inplace=True)
        
        return df[['date', 'exchange_rate_brl_usd']]
    
    def fetch_inflation_ipca(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch IPCA inflation data"""
        # Series code: 433 (IPCA acumulado 12 meses)
        series_id = "433"
        url = f"{self.base_url}{series_id}/dados?formato=json&dataInicial={start_date}&dataFinal={end_date}"
        
        response = requests.get(url)
        data = response.json()
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df.rename(columns={'valor': 'inflation_rate'}, inplace=True)
        
        return df[['date', 'inflation_rate']]

# Example usage
bacen_fetcher = BACENEconomicDataFetcher()
exchange_data = bacen_fetcher.fetch_exchange_rate('2024-01-01', '2024-12-31')
inflation_data = bacen_fetcher.fetch_inflation_ipca('2024-01-01', '2024-12-31')
```

#### IBGE - Regional GDP & Economic Indicators

```python
class IBGEEconomicDataFetcher:
    """Fetch regional economic data from IBGE"""
    
    def __init__(self):
        self.base_url = "https://servicodados.ibge.gov.br/api/v1"
    
    def fetch_regional_gdp(self, state_code: str, year: int) -> dict:
        """Fetch regional GDP growth data"""
        # State codes: 29=Bahia, 35=São Paulo, 33=Rio de Janeiro
        url = f"{self.base_url}/economia/pib/v2/{state_code}/{year}"
        
        response = requests.get(url)
        data = response.json()
        
        return data
    
    def fetch_employment_rate(self, state_code: str) -> pd.DataFrame:
        """Fetch employment data"""
        pass

# Example usage for Bahia (Nova Corrente headquarters)
ibge_fetcher = IBGEEconomicDataFetcher()
bahia_gdp = ibge_fetcher.fetch_regional_gdp('29', 2024)  # Bahia code
```

### Integration Points

**File:** `src/pipeline/add_external_factors.py`  
**Method:** `add_economic_factors()`

```python
def add_economic_factors(self, df: pd.DataFrame) -> pd.DataFrame:
    """Add economic factors from BACEN/IBGE"""
    from src.pipeline.brazilian_apis import BACENEconomicDataFetcher, IBGEEconomicDataFetcher
    
    logger.info("Fetching economic data from BACEN/IBGE...")
    
    bacen_fetcher = BACENEconomicDataFetcher()
    ibge_fetcher = IBGEEconomicDataFetcher()
    
    # Fetch exchange rate and inflation
    min_date = df['date'].min().strftime('%d/%m/%Y')
    max_date = df['date'].max().strftime('%d/%m/%Y')
    
    exchange_df = bacen_fetcher.fetch_exchange_rate(min_date, max_date)
    inflation_df = bacen_fetcher.fetch_inflation_ipca(min_date, max_date)
    
    # Merge with main dataset
    df = df.merge(exchange_df, on='date', how='left')
    df = df.merge(inflation_df, on='date', how='left')
    
    # Add economic flags
    df['high_inflation'] = (df['inflation_rate'] > 5).astype(int)
    df['currency_devaluation'] = (df['exchange_rate_brl_usd'] > 5.3).astype(int)
    
    return df
```

---

## 📡 Regulatory Data Integration (Anatel)

### Data Source

**Agência Nacional de Telecomunicações (Anatel)**  
**URL:** https://www.anatel.gov.br/  
**Open Data Portal:** https://dadosabertos.anatel.gov.br/

### Implementation Strategy

#### Anatel 5G Expansion Data

```python
class AnatelRegulatoryDataFetcher:
    """Fetch regulatory data from Anatel"""
    
    def __init__(self):
        self.base_url = "https://dadosabertos.anatel.gov.br"
    
    def fetch_5g_coverage(self, city: str, state: str) -> pd.DataFrame:
        """Fetch 5G coverage data by city"""
        # Anatel open data API or CSV download
        url = f"{self.base_url}/dataset/5g-coverage"
        
        # Download CSV or use API
        # Parse 5G coverage percentage by city/date
        pass
    
    def fetch_compliance_deadlines(self) -> pd.DataFrame:
        """Fetch regulatory compliance deadlines"""
        # Dates when 5G must be deployed in specific cities
        # Based on Anatel auction results
        pass
    
    def fetch_subscriber_growth(self, region: str) -> pd.DataFrame:
        """Fetch mobile subscriber growth data"""
        # Monthly subscriber counts by technology (4G, 5G)
        pass

# Example: 5G expansion timeline
anatel_fetcher = AnatelRegulatoryDataFetcher()
salvador_5g = anatel_fetcher.fetch_5g_coverage("Salvador", "BA")
```

### Integration Points

**File:** `src/pipeline/add_external_factors.py`  
**Method:** `add_regulatory_factors()`

```python
def add_regulatory_factors(self, df: pd.DataFrame) -> pd.DataFrame:
    """Add regulatory factors from Anatel"""
    from src.pipeline.brazilian_apis import AnatelRegulatoryDataFetcher
    
    logger.info("Fetching regulatory data from Anatel...")
    
    anatel_fetcher = AnatelRegulatoryDataFetcher()
    
    # Fetch 5G coverage by city
    cities = df['site_id'].unique()
    for city in cities:
        # Parse city and state from site_id
        state = self._get_state_from_site(city)
        coverage_df = anatel_fetcher.fetch_5g_coverage(city, state)
        
        # Merge 5G coverage data
        df = df.merge(coverage_df, on=['date', 'site_id'], how='left')
    
    # Add 5G expansion flags based on dates
    df['5g_coverage'] = df['date'].apply(lambda x: 1 if x >= pd.Timestamp('2024-01-01') else 0)
    
    return df
```

---

## 📅 Operational Data Integration

### Brazilian Holidays & Events

```python
class BrazilianOperationalDataFetcher:
    """Fetch operational factors (holidays, events)"""
    
    def __init__(self):
        import holidays
        
        self.holidays_br = holidays.Brazil()
    
    def fetch_holidays(self, year: int) -> list:
        """Get Brazilian holidays for year"""
        return list(self.holidays_br[y:f"{year}-12-31"])
    
    def fetch_carnival_dates(self, year: int) -> tuple:
        """Get Carnival dates (major telecom traffic event)"""
        # Carnival typically in Feb/Mar - lookup specific dates
        # Carnaval Salvador 2024: Feb 8-13
        pass
    
    def fetch_economic_events(self) -> pd.DataFrame:
        """Get economic events that might impact supply chain"""
        # e.g., trucker strikes, port blockades
        pass

# Example
operational_fetcher = BrazilianOperationalDataFetcher()
br_holidays_2024 = operational_fetcher.fetch_holidays(2024)
carnival_2024 = operational_fetcher.fetch_carnival_dates(2024)
```

---

## 🚀 Implementation Steps

### Phase 1: API Integration Setup (Week 1)

1. **Create Brazilian APIs Module**
   ```bash
   touch src/pipeline/brazilian_apis.py
   ```

2. **Install Required Libraries**
   ```bash
   pip install requests beautifulsoup4 holidays pandas
   ```

3. **Implement BACEN Fetcher** (Highest priority - most reliable API)
   - Exchange rate
   - Inflation (IPCA)
   - Test with real API calls

### Phase 2: Climate Data Integration (Week 2)

1. **Explore INMET Portal**
   - Test CSV downloads
   - Check for API availability
   - Identify station codes for Nova Corrente regions

2. **Implement INMET Fetcher**
   - Daily climate data
   - Fallback to web scraping if needed

3. **Update Climate Factors**
   - Replace placeholders with real data
   - Test integration in pipeline

### Phase 3: Regulatory Data Integration (Week 3)

1. **Explore Anatel Open Data**
   - 5G coverage datasets
   - Subscriber growth data
   - Compliance deadlines

2. **Implement Anatel Fetcher**
   - Web scraping or CSV download
   - Parse regulatory data

3. **Update Regulatory Factors**
   - Real 5G expansion dates
   - Subscriber-driven demand adjustments

### Phase 4: Operational Data Integration (Week 4)

1. **Brazilian Holidays Calendar**
   - Integrate `holidays` library
   - Add custom events (Carnival, etc.)

2. **Economic Event Database**
   - Create database of past events
   - Track supply chain impacts

3. **Test Full Integration**
   - Run complete pipeline with real data
   - Validate forecast accuracy improvements

### Phase 5: Validation & Optimization (Week 5)

1. **Data Quality Checks**
   - Validate API data consistency
   - Handle missing data gracefully
   - Implement caching

2. **Performance Optimization**
   - Cache API responses
   - Batch downloads
   - Error handling & retries

3. **Documentation**
   - API usage documentation
   - Data freshness policies
   - Monitoring setup

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/test_brazilian_apis.py

import unittest
from src.pipeline.brazilian_apis import *

class TestBrazilianAPIs(unittest.TestCase):
    
    def test_bacen_exchange_rate(self):
        fetcher = BACENEconomicDataFetcher()
        data = fetcher.fetch_exchange_rate('2024-01-01', '2024-01-31')
        self.assertGreater(len(data), 0)
        self.assertIn('exchange_rate_brl_usd', data.columns)
    
    def test_inmet_climate_data(self):
        fetcher = INMETClimateDataFetcher('A601')
        data = fetcher.fetch_daily_summary('2024-01-15')
        self.assertIn('temperature', data)
        self.assertIn('precipitation', data)
    
    def test_anatel_5g_coverage(self):
        fetcher = AnatelRegulatoryDataFetcher()
        data = fetcher.fetch_5g_coverage('Salvador', 'BA')
        self.assertGreater(len(data), 0)
```

### Integration Tests

```python
# tests/test_external_factors_integration.py

def test_full_pipeline_with_real_data():
    """Test complete pipeline with Brazilian APIs"""
    from src.pipeline.add_external_factors import ExternalFactorsAdder
    
    adder = ExternalFactorsAdder()
    df = adder.add_external_factors()
    
    # Validate real data was fetched
    assert df['exchange_rate_brl_usd'].notna().sum() > 0
    assert df['temperature'].notna().sum() > 0
    assert df['5g_coverage'].notna().sum() > 0
```

---

## 📊 Expected Impact

### Before (Placeholder Data)
- Simulated values with no real-world correlation
- No seasonal patterns from actual climate
- Missing economic context for Brazil
- Generic regulatory timelines

### After (Real Brazilian Data)
- **20-30% improvement** in forecast accuracy (based on research)
- **50-60% reduction** in stockouts (models account for real factors)
- **Scenario planning** for Brazilian-specific events:
  - Carnival traffic spikes
  - Rainy season infrastructure stress
  - USD/BRL volatility impacts
  - 5G rollout driven demand

### Metrics to Track

| Metric | Baseline | Target | Tracking |
|--------|----------|--------|----------|
| MAPE (forecast accuracy) | 25% | <15% | Weekly |
| Stockout incidents | 10/month | <4/month | Weekly |
| Safety stock optimization | Baseline | -20% | Monthly |
| API uptime | N/A | >99% | Daily |

---

## 🔐 Security & Compliance

### Data Privacy
- Brazilian General Data Protection Law (LGPD) compliance
- No personal data collection
- Aggregated/anonymous data only

### API Security
- Store API credentials in `config/secrets.json` (git-ignored)
- Use environment variables for sensitive data
- Implement rate limiting for API calls
- Cache responses to minimize external calls

### Data Retention
- Keep API data cached for 30 days
- Archive historical data for trend analysis
- Comply with Anatel/INMET/BACEN data policies

---

## 📚 Resources & References

### Official Sources
- [INMET Portal](https://www.inmet.gov.br/)
- [BACEN Economic Data](https://www.bcb.gov.br/en/htms/publicsdin/pxweb_internet.asp)
- [Anatel Open Data](https://dadosabertos.anatel.gov.br/)
- [IBGE Statistics](https://www.ibge.gov.br/)

### APIs & Libraries
- [Brazil Holidays Python](https://github.com/dr-prodigy/python-holidays)
- [Requests Library](https://requests.readthedocs.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

### Documentation
- `docs/Grok-_27.md` - Detailed external factors analysis
- `docs/BRAZILIAN_TELECOM_DATASETS_GUIDE.md` - Brazilian datasets overview
- `src/pipeline/add_external_factors.py` - Current implementation

---

## ✅ Next Actions

**Immediate (This Week):**
1. ✅ Create `src/pipeline/brazilian_apis.py`
2. ⬜ Implement `BACENEconomicDataFetcher` (start with exchange rate)
3. ⬜ Test BACEN API with sample calls
4. ⬜ Update `add_economic_factors()` to use real data

**Short-term (Next 2 Weeks):**
5. ⬜ Implement INMET climate data fetcher
6. ⬜ Implement Anatel regulatory data fetcher
7. ⬜ Full pipeline integration test
8. ⬜ Performance optimization & caching

**Long-term (Next Month):**
9. ⬜ Monitoring dashboard for API health
10. ⬜ Automated alerts for data freshness issues
11. ⬜ Historical data archive system
12. ⬜ Documentation & training for team

---

**Status:** 🚀 **READY FOR IMPLEMENTATION**  
**Last Updated:** 2025-01-01  
**Nova Corrente Grand Prix SENAI - Demand Forecasting System**


