# Freight & Shipping Indices Automation Guide

## Overview

Complete automation framework for downloading freight indices to replace restricted sources (Freightos FBX) with free and semi-free alternatives. This guide covers **Baltic Dry Index (BDI)**, **Drewry World Container Index (WCI)**, **Shanghai Containerized Freight Index (SCFI)**, **UNCTAD Liner Shipping Index (LSCI)**, **IMF Shipping Cost Index (SCI)**, and partial **Trading Economics FBX** access.

---

## Data Sources & Access Methods

| Index | Source | Frequency | Access | Automation |
|-------|--------|-----------|--------|-----------|
| **BDI** | Trading Economics API | Daily | Free (guest:guest) | ✓ Full API |
| **Drewry WCI** | Drewry.co.uk | Weekly | Manual + Email | Manual loader |
| **SCFI** | Investing.com | Weekly | Manual + Scrape | Selenium/Manual |
| **UNCTAD LSCI** | UNCTADstat Portal | Quarterly | Manual export | Manual loader |
| **IMF SCI** | World Bank API | Annual | Free API | ✓ Full API |
| **FBX** | Trading Economics | Daily | Limited free | ✓ Partial (4 lanes) |

---

## Installation

### Prerequisites
```bash
# Core requirements
pip install requests beautifulsoup4

# For Trading Economics (optional but recommended)
pip install tradingeconomics

# For Selenium scraping (for SCFI, optional)
pip install selenium webdriver-manager

# For scheduling (optional)
pip install schedule APScheduler

# For data processing
pip install pandas openpyxl
```

### Environment Setup
```bash
# Set API key (optional, defaults to guest:guest)
export TRADING_ECONOMICS_API_KEY="your_api_key_here"

# Set output directory
export FREIGHT_DATA_DIR="data/manual"

# Create data directory
mkdir -p data/manual
```

---

## Quick Start

### Option 1: Simple One-Time Download (Recommended for Testing)

```python
from freight_data_automation import FreightAutomationOrchestrator

# Initialize
orchestrator = FreightAutomationOrchestrator(output_dir="data/manual")

# Download all automated sources
results = orchestrator.download_all(skip_manual=True)

# Print status
orchestrator.print_status()
```

**Output:**
- `data/manual/bdi_historical.csv` - Baltic Dry Index (last 5+ years)
- `data/manual/imf_shipping_cost_index.csv` - IMF SCI proxy
- `data/manual/te_fbx_free_lanes.csv` - FBX for Mexico, New Zealand, Sweden, Thailand

### Option 2: Trading Economics API Only

```python
from trading_econ_fetcher import TradingEconomicsFreightFetcher

fetcher = TradingEconomicsFreightFetcher(
    api_key="your_api_key"  # or os.getenv('TRADING_ECONOMICS_API_KEY')
)

# Fetch BDI last 365 days
bdi_data = fetcher.get_historical_ticker(
    ticker='BDIY',
    start_date='2023-11-01'
)

# Save to CSV
fetcher.save_to_csv(bdi_data, 'bdi_data.csv')
```

### Option 3: World Bank IMF Fetcher

```python
from worldbank_freight_fetcher import WorldBankFreightFetcher

fetcher = WorldBankFreightFetcher()

# Fetch IMF Shipping Cost Index proxy (2000-2024)
data = fetcher.get_indicator(
    indicator_code='IM.fs.sp_cons.sh',
    start_year=2000,
    end_year=2024
)

fetcher.save_csv(data, 'imf_shipping_cost.csv')
```

---

## Manual Data Loading

### For Drewry World Container Index

1. **Visit:** https://www.drewry.co.uk/supply-chain-advisors/world-container-index
2. **Download:** Weekly CSV or request historical data
3. **Load in code:**
   ```python
   from freight_data_automation import DrewryWCI
   
   drewry = DrewryWCI(output_dir="data/manual")
   drewry.load_existing_csv("path/to/drewry_download.csv")
   ```

### For UNCTAD LSCI

1. **Visit:** https://unctadstat.unctad.org/wds/TableViewer/tableView.aspx?ReportId=92
2. **Export:** CSV or Excel format
3. **Load in code:**
   ```python
   from freight_data_automation import UNCTADLinnerShippingIndex
   
   unctad = UNCTADLinnerShippingIndex(output_dir="data/manual")
   unctad.load_existing_csv("path/to/unctad_lsci.csv")
   ```

### For SCFI (Shanghai Containerized Freight Index)

**Option A: Manual Download from Investing.com**
1. Visit: https://www.investing.com/indices/shanghai-containerized-freight-index
2. Click "Download Data" button
3. Select date range and download CSV
4. Place in `data/manual/scfi_historical.csv`

**Option B: Selenium Automation**
```python
from selenium_freight_scraper import InvestingComScraper

scraper = InvestingComScraper(headless=True)
scraper.scrape_scfi_historical('data/manual/scfi_scraped.csv')
```

---

## Automated Scheduling

### Option 1: Simple Schedule (Development)

```python
from freight_data_scheduler import FreightDataScheduler

scheduler = FreightDataScheduler()
scheduler.setup_daily_schedule()
scheduler.run_continuous()  # Blocks - runs indefinitely
```

**Schedule:**
- Daily at 2:00 AM - BDI download
- Weekly Monday 3:00 AM - IMF SCI download

### Option 2: APScheduler (Production)

```python
from freight_data_scheduler import setup_apscheduler

# Setup background scheduler
scheduler = setup_apscheduler()

# Your app continues running
# Scheduler runs in background threads
```

### Option 3: System Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add these lines:
# BDI daily at 2 AM
0 2 * * * cd /path/to/project && python -c "from trading_econ_fetcher import *; TradingEconomicsFreightFetcher().save_to_csv(TradingEconomicsFreightFetcher().get_historical_ticker('BDIY'), 'data/manual/bdi_\$(date +\\%Y\\%m\\%d).csv')"

# IMF weekly Monday 3 AM
0 3 * * 1 cd /path/to/project && python -c "from worldbank_freight_fetcher import *; WorldBankFreightFetcher().save_csv(WorldBankFreightFetcher().get_indicator('IM.fs.sp_cons.sh'), 'data/manual/imf_sci_\$(date +\\%Y\\%m\\%d).csv')"
```

### Option 4: Task Scheduler (Windows)

**Create batch file `fetch_freight.bat`:**
```batch
@echo off
cd C:\path\to\project
python -m freight_data_automation
```

**Schedule via Task Scheduler:**
- Action: Start a program
- Program: `C:\path\to\project\fetch_freight.bat`
- Trigger: Daily at 2:00 AM

---

## Data Structure & CSV Format

### BDI Historical
```
date,value,symbol
2024-11-10,2084.00,BDI
2024-11-09,2104.00,BDI
2024-11-08,2090.50,BDI
```

### IMF Shipping Cost Index
```
date,value,country,indicator
2024,5.2,World,IM.fs.sp_cons.sh
2023,4.8,World,IM.fs.sp_cons.sh
2022,6.1,World,IM.fs.sp_cons.sh
```

### SCFI (Shanghai Container Freight)
```
date,value,index
2024-11-10,1456.23,SCFI
2024-11-03,1465.80,SCFI
2024-10-27,1482.15,SCFI
```

---

## API Credentials & Rate Limiting

### Trading Economics

**Free API:**
- Credentials: `guest:guest`
- Rate limit: 100 requests/hour
- Data lag: 1-2 days

**Paid API:**
- Full FBX access
- Real-time data
- Unlimited requests
- Sign up: https://tradingeconomics.com/subscribe

### World Bank

**IMF Shipping Cost Index**
- No authentication required
- Rate limit: Generous (1000s/hour)
- Data lag: 6-12 months
- Endpoint: `https://api.worldbank.org/v2/country/WLD/indicator/IM.fs.sp_cons.sh`

---

## Integration with Feature Store

### Combining Multiple Indices

```python
import pandas as pd
from pathlib import Path

# Load all indices
bdi = pd.read_csv('data/manual/bdi_historical.csv')
imf = pd.read_csv('data/manual/imf_shipping_cost_index.csv')
scfi = pd.read_csv('data/manual/scfi_historical.csv')

# Merge on date
merged = bdi.set_index('date').join([
    imf.set_index('date')[['value']].rename(columns={'value': 'imf_sci'}),
    scfi.set_index('date')[['value']].rename(columns={'value': 'scfi'})
], how='outer')

# Fill missing values
merged_filled = merged.fillna(method='ffill').fillna(method='bfill')

# Save to feature store
merged_filled.to_csv('data/features/freight_indices_combined.csv')
```

### Standardization for ML Models

```python
# Normalize all indices to 0-1 scale
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
normalized = pd.DataFrame(
    scaler.fit_transform(merged_filled),
    columns=merged_filled.columns,
    index=merged_filled.index
)

normalized.to_csv('data/features/freight_indices_normalized.csv')
```

---

## Troubleshooting

### Issue: "guest:guest API access denied"
**Solution:** Get paid Trading Economics account or use World Bank API instead

### Issue: Selenium script hangs on page load
**Solution:** Increase timeout or use headless mode:
```python
scraper = InvestingComScraper(headless=True)
```

### Issue: Investing.com "Download Data" button not working
**Solution:** Page structure changes frequently. Alternative:
- Use manual download
- Check Drewry or SCFI mirrors
- Use trading volume/port statistics as proxy

### Issue: World Bank API returns empty data
**Solution:** Check indicator code and date range:
```python
# Available indicators
indicators = ['IM.fs.sp_cons.sh', 'NY.GDP.FCST.CD', 'TM.VAL.TRAD.WRD.CD']
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│        FreightAutomationOrchestrator (Main Controller)       │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
    ┌───────▼────────┐ ┌───▼──────────┐ ┌─▼────────────┐
    │ Automated APIs │ │ Manual Loaders│ │  Scrapers    │
    ├────────────────┤ ├──────────────┤ ├──────────────┤
    │ • BDI (TE)     │ │ • Drewry CSV │ │ • SCFI (Sel) │
    │ • IMF (WB)     │ │ • UNCTAD CSV │ │ • Custom     │
    │ • FBX (TE*)    │ │              │ │              │
    └────────────────┘ └──────────────┘ └──────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                    ┌───────▼────────┐
                    │  CSV Export    │
                    │  & Logging     │
                    └────────────────┘
                            │
                    ┌───────▼────────┐
                    │  Feature Store │
                    │  (data/manual) │
                    └────────────────┘
```

---

## Performance Metrics

**Typical execution times:**
- BDI fetch & parse: ~2-3 seconds
- IMF fetch & parse: ~2-3 seconds
- SCFI scrape (Selenium): ~15-20 seconds
- Full orchestration: ~30 seconds (with manual sources skipped)

**Data volume:**
- BDI: ~5 years = 1,250+ daily records
- IMF SCI: ~25 years = 25 annual records
- SCFI: ~5 years = 260+ weekly records
- Total CSV size: ~150 KB

---

## Extending the Framework

### Adding a New Data Source

```python
from freight_data_automation import FreightDataSource

class MyFreightSource(FreightDataSource):
    def fetch_data(self):
        # Your API/scraping logic
        return raw_data
    
    def parse_data(self, raw_data):
        # Return list of dicts: [{'date': ..., 'value': ...}, ...]
        return parsed_list
    
    def get_filename(self):
        return "my_index.csv"

# Register in orchestrator
orchestrator.sources['my_source'] = MyFreightSource()
```

### Using with Pandas/Polars

```python
import pandas as pd

# Load multiple indices
df = pd.concat([
    pd.read_csv(f'data/manual/{f}') 
    for f in ['bdi_historical.csv', 'imf_shipping_cost_index.csv']
], axis=1)

# Quick analysis
print(df.corr())
df.plot()
```

---

## References

- **Trading Economics API Docs:** https://docs.tradingeconomics.com
- **World Bank API:** https://data.worldbank.org/developers
- **UNCTAD Data Portal:** https://unctadstat.unctad.org
- **Investing.com:** https://www.investing.com
- **Drewry Supply Chain:** https://www.drewry.co.uk

---

## License & Attribution

Framework built for demand/inventory forecasting in telecommunications supply chains.
Data sourced from public APIs and approved channels.