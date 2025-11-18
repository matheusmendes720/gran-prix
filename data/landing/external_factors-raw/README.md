# Freight & Shipping Indices Automation

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
