
# Create quick reference and example notebook

quickref = '''# Freight Data Automation - Quick Reference

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
'''

with open('QUICKREF.md', 'w') as f:
    f.write(quickref)

print("✓ QUICKREF.md created")

# Example notebook in Python format
example_notebook = '''"""
Freight Data Automation Example Notebook
Run with: python or jupyter notebook
"""

import pandas as pd
from datetime import datetime, timedelta
import os

print("="*60)
print("FREIGHT DATA AUTOMATION - EXAMPLE NOTEBOOK")
print("="*60)

# Step 1: One-time download
print("\\n[Step 1] Downloading freight data...")
print("-" * 60)

try:
    from freight_data_automation import FreightAutomationOrchestrator
    
    orchestrator = FreightAutomationOrchestrator(output_dir="data/manual")
    results = orchestrator.download_all(skip_manual=True)
    orchestrator.print_status()
except Exception as e:
    print(f"Error: {e}")
    print("Note: Ensure Trading Economics API key is set")
    print("export TRADING_ECONOMICS_API_KEY='your_key'")

# Step 2: Load and inspect data
print("\\n[Step 2] Loading and inspecting downloaded data...")
print("-" * 60)

data_files = [
    'data/manual/bdi_historical.csv',
    'data/manual/imf_shipping_cost_index.csv'
]

loaded_data = {}
for filepath in data_files:
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            name = os.path.basename(filepath).replace('.csv', '')
            loaded_data[name] = df
            
            print(f"\\n✓ {name}")
            print(f"  Shape: {df.shape}")
            print(f"  Columns: {', '.join(df.columns)}")
            print(f"  Date range: {df.iloc[-1, 0]} to {df.iloc[0, 0]}")
            print(f"  Records: {len(df)}")
        except Exception as e:
            print(f"✗ {filepath}: {e}")

# Step 3: Data quality checks
print("\\n[Step 3] Data quality analysis...")
print("-" * 60)

for name, df in loaded_data.items():
    print(f"\\n{name}:")
    print(f"  Missing values: {df.isnull().sum().sum()}")
    print(f"  Data types: {dict(df.dtypes)}")
    if 'value' in df.columns:
        print(f"  Value range: {df['value'].min():.2f} - {df['value'].max():.2f}")
        print(f"  Mean: {df['value'].mean():.2f}")

# Step 4: Combine indices
print("\\n[Step 4] Combining indices for feature engineering...")
print("-" * 60)

if len(loaded_data) >= 2:
    try:
        # Get BDI
        bdi = loaded_data.get('bdi_historical', None)
        if bdi is not None:
            bdi['date'] = pd.to_datetime(bdi['date'])
            bdi_indexed = bdi.set_index('date')[['value']].rename(columns={'value': 'bdi'})
            
            # Get IMF SCI
            imf = loaded_data.get('imf_shipping_cost_index', None)
            if imf is not None:
                imf['date'] = pd.to_datetime(imf['date'].astype(str))
                imf_indexed = imf.set_index('date')[['value']].rename(columns={'value': 'imf_sci'})
                
                # Merge
                merged = bdi_indexed.join(imf_indexed, how='inner')
                print(f"\\nMerged dataset:")
                print(f"  Shape: {merged.shape}")
                print(f"  Date range: {merged.index[0].date()} to {merged.index[-1].date()}")
                print(f"  Common records: {len(merged)}")
                
                # Save combined
                merged.to_csv('data/manual/freight_indices_combined.csv')
                print(f"✓ Saved to data/manual/freight_indices_combined.csv")
                
                # Show sample
                print(f"\\nSample data (first 5 rows):")
                print(merged.head())
    except Exception as e:
        print(f"Error combining: {e}")

# Step 5: Visualization prep
print("\\n[Step 5] Visualization data preparation...")
print("-" * 60)

try:
    if 'bdi' in locals():
        # Resample to weekly for smoother visualization
        bdi_weekly = bdi_indexed.resample('W').mean()
        print(f"✓ BDI resampled to weekly: {len(bdi_weekly)} points")
        
        # Calculate rolling statistics
        bdi_weekly['ma_4w'] = bdi_weekly['bdi'].rolling(4).mean()
        bdi_weekly['volatility_4w'] = bdi_weekly['bdi'].rolling(4).std()
        
        print("✓ Added 4-week moving average and volatility")
        print(f"\\nSample with indicators (last 5 rows):")
        print(bdi_weekly.tail())
        
        bdi_weekly.to_csv('data/manual/bdi_with_indicators.csv')
        print(f"✓ Saved to data/manual/bdi_with_indicators.csv")
except Exception as e:
    print(f"Error: {e}")

# Step 6: Ready for ML/BI
print("\\n[Step 6] Ready for downstream processing...")
print("-" * 60)

print("""
Your data is ready for:
✓ Time series forecasting (ARIMA, Prophet)
✓ Demand prediction models
✓ Feature engineering for demand/inventory optimization
✓ Dashboard visualization (Plotly, Streamlit)
✓ Machine learning pipelines

Next steps:
1. Normalize/standardize the indices
2. Create lag features for forecasting
3. Combine with your internal telco data
4. Train models on combined dataset
""")

print("\\n" + "="*60)
print("EXAMPLE COMPLETE")
print("="*60)
'''

with open('example_notebook.py', 'w') as f:
    f.write(example_notebook)

print("✓ example_notebook.py created")

# Create a Makefile for common tasks
makefile = '''# Freight Data Automation Makefile

.PHONY: help install download clean docker-build docker-run schedule test

help:
	@echo "Freight Data Automation Commands"
	@echo "================================"
	@echo "make install       - Install dependencies"
	@echo "make download      - Download freight data (one-time)"
	@echo "make schedule      - Start scheduled downloads"
	@echo "make docker-build  - Build Docker image"
	@echo "make docker-run    - Run in Docker container"
	@echo "make clean         - Clean up generated files"
	@echo "make test          - Run tests"
	@echo "make example       - Run example notebook"

install:
	pip install -r requirements.txt
	mkdir -p data/manual

download:
	python -c "from freight_data_automation import FreightAutomationOrchestrator; orchestrator = FreightAutomationOrchestrator(); orchestrator.download_all(); orchestrator.print_status()"

schedule:
	python -c "from freight_data_scheduler import FreightDataScheduler; scheduler = FreightDataScheduler(); scheduler.setup_daily_schedule(); scheduler.run_continuous()"

docker-build:
	docker build -t freight-data-automation:latest .

docker-run:
	docker run --rm -v $$(pwd)/data:/app/data freight-data-automation:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

clean:
	rm -rf data/manual/*.csv
	rm -rf __pycache__
	rm -rf *.pyc
	find . -type d -name __pycache__ -delete

test:
	python -m pytest tests/ -v

example:
	python example_notebook.py

status:
	@echo "Files in data/manual:"
	@ls -lh data/manual/ 2>/dev/null || echo "No data directory yet"

logs:
	docker logs -f freight-fetcher-scheduled 2>/dev/null || echo "Container not running"

update:
	git pull
	pip install -r requirements.txt

.PHONY: help install download clean docker-build docker-run schedule test
'''

with open('Makefile', 'w') as f:
    f.write(makefile)

print("✓ Makefile created")

# .gitignore for the project
gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Data
data/manual/*.csv
data/manual/*.json
data/features/*.csv
logs/

# OS
.DS_Store
Thumbs.db

# Project specific
.env
.env.local
*.egg-info/
dist/
build/

# Docker
docker-compose.override.yml
'''

with open('.gitignore', 'w') as f:
    f.write(gitignore)

print("✓ .gitignore created")

# README
readme = '''# Freight & Shipping Indices Automation

Automated data pipeline for downloading and combining multiple freight indices for demand forecasting and supply chain optimization in telecommunications.

## Features

✓ **Daily Baltic Dry Index (BDI)** via Trading Economics API
✓ **Annual IMF Shipping Cost Index** via World Bank
✓ **Weekly Drewry World Container Index** (manual + auto-loader)
✓ **Quarterly UNCTAD Liner Shipping Index** (manual + auto-loader)
✓ **Weekly Shanghai Containerized Freight Index** (Selenium scraping)
✓ **Partial FBX access** via Trading Economics (4 free lanes)

## Quick Start

```bash
# Install
make install

# Download once
make download

# Run scheduled (continuous)
make schedule

# Or with Docker
make docker-build
make docker-compose-up
```

## Data Output

All data saved to `data/manual/`:
- `bdi_historical.csv` - Daily BDI data
- `imf_shipping_cost_index.csv` - Annual IMF SCI
- `drewry_wci.csv` - Weekly Drewry WCI (manual upload)
- `unctad_lsci.csv` - Quarterly LSCI (manual upload)
- `scfi_historical.csv` - Weekly SCFI
- `te_fbx_free_lanes.csv` - FBX partial access

## Integration

```python
from freight_data_automation import FreightAutomationOrchestrator

orchestrator = FreightAutomationOrchestrator()
orchestrator.download_all()
```

## Documentation

- [Comprehensive Guide](freight_automation_guide.md)
- [Quick Reference](QUICKREF.md)
- [Example Notebook](example_notebook.py)

## API Credentials

Trading Economics (free tier):
```bash
export TRADING_ECONOMICS_API_KEY="guest:guest"
```

Paid tier gives you full FBX access and higher rate limits.

## Scheduling Options

- **Linux/Mac:** `make schedule` or crontab
- **Windows:** Task Scheduler
- **Docker:** `make docker-compose-up`
- **GitHub Actions:** Push triggers `.github/workflows/`
- **Kubernetes:** `kubectl apply -f k8s/`

## Files

### Core Modules
- `freight_data_automation.py` - Main orchestrator
- `trading_econ_fetcher.py` - Trading Economics API
- `worldbank_freight_fetcher.py` - World Bank/IMF API
- `selenium_freight_scraper.py` - Investing.com scraper
- `freight_data_scheduler.py` - Scheduled automation
- `freight_config.py` - Configuration management

### Deployment
- `Dockerfile` - Container image
- `docker-compose.yml` - Multi-container setup
- `docker-run.sh` - Helper script
- `.github/workflows/` - GitHub Actions
- `k8s/` - Kubernetes manifests
- `Makefile` - Common commands

## License

MIT - See LICENSE file

## Support

For issues:
1. Check [freight_automation_guide.md](freight_automation_guide.md)
2. Review error logs in `logs/`
3. Verify API credentials
4. Check data format in `data/manual/`
'''

with open('README.md', 'w') as f:
    f.write(readme)

print("✓ README.md created")

print("\n" + "="*70)
print("COMPLETE AUTOMATION FRAMEWORK CREATED")
print("="*70)
print("\nCore Python modules:")
print("  ✓ freight_data_automation.py")
print("  ✓ trading_econ_fetcher.py")
print("  ✓ worldbank_freight_fetcher.py")
print("  ✓ selenium_freight_scraper.py")
print("  ✓ freight_data_scheduler.py")
print("  ✓ freight_config.py")
print("\nDocumentation:")
print("  ✓ freight_automation_guide.md (comprehensive)")
print("  ✓ QUICKREF.md (quick reference)")
print("  ✓ README.md (project overview)")
print("\nDeployment:")
print("  ✓ Dockerfile")
print("  ✓ docker-compose.yml")
print("  ✓ docker-run.sh")
print("  ✓ requirements.txt")
print("  ✓ .github/workflows/ (CI/CD)")
print("  ✓ k8s/freight-cronjob.yaml (Kubernetes)")
print("  ✓ Makefile (common tasks)")
print("\nExamples:")
print("  ✓ example_notebook.py (run with: python example_notebook.py)")
print("\nNext step: Make and run make download")
print("="*70)
