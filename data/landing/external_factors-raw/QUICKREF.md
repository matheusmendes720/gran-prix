# Freight Data Automation - Quick Reference

## Installation (30 seconds)
```bash
pip install requests beautifulsoup4 tradingeconomics pandas
mkdir -p data/manual
```

## One-Line Download
```python
from freight_data_automation import FreightAutomationOrchestrator
FreightAutomationOrchestrator().download_all()
```

## Manual Downloads

| Source | Link | Format | Frequency |
|--------|------|--------|-----------|
| **Drewry WCI** | https://www.drewry.co.uk/supply-chain-advisors/world-container-index | CSV | Weekly |
| **UNCTAD LSCI** | https://unctadstat.unctad.org/wds/TableViewer/tableView.aspx?ReportId=92 | Excel/CSV | Quarterly |
| **SCFI** | https://www.investing.com/indices/shanghai-containerized-freight-index | Manual or Selenium | Weekly |

## Docker Quick Start
```bash
# Build
docker build -t freight-automation .

# Run once
docker run --rm -v $(pwd)/data:/app/data freight-automation

# Run scheduled (background)
docker-compose up -d
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| API returns no data | Check credentials; try guest:guest |
| Selenium timeout | Increase wait time or use manual download |
| Permission denied | chmod +x docker-run.sh |
| No output files | Check output_dir permissions |

## Data Format Quick Check
```python
import pandas as pd
df = pd.read_csv('data/manual/bdi_historical.csv')
print(df.head())
print(df.dtypes)
print(df.describe())
```

## API Response Sizes
- BDI: ~500KB (5 years daily)
- IMF SCI: ~5KB (25 years)
- SCFI: ~300KB (5 years weekly)

## Rate Limits
- Trading Economics: 100 req/hr (free)
- World Bank: 1000+ req/hr
- Investing.com: No official limits (use Selenium sparingly)
