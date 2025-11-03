# Dataset Download and Preprocessing System
## Nova Corrente Demand Forecasting - Grand Prix SENAI

This system downloads, preprocesses, merges, and enriches datasets from multiple sources to create a unified dataset for training predictive demand forecasting models.

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure Kaggle API (optional, for Kaggle datasets)
# Copy config/kaggle_config.json.template to config/kaggle_config.json
# Add your Kaggle username and API key
```

### 2. Run Complete Pipeline

```bash
# Download all datasets, preprocess, merge, and add external factors
python run_pipeline.py
```

### 3. Run Individual Steps

```bash
# Step 1: Download datasets
python download_datasets.py

# Step 2: Preprocess datasets
python preprocess_datasets.py

# Step 3: Merge datasets
python merge_datasets.py

# Step 4: Add external factors
python add_external_factors.py
```

## Dataset Sources

| Dataset ID | Source | Description | Relevance |
|------------|--------|-------------|-----------|
| `kaggle_daily_demand` | Kaggle | 60 days daily demand, MVP ready | ⭐⭐⭐⭐⭐ |
| `kaggle_logistics_warehouse` | Kaggle | 3,204 logistics records with lead times | ⭐⭐⭐⭐ |
| `kaggle_retail_inventory` | Kaggle | 73,000+ inventory records | ⭐⭐⭐⭐ |
| `kaggle_supply_chain` | Kaggle | Large-scale supply chain data | ⭐⭐⭐⭐ |
| `zenodo_milan_telecom` | Zenodo | Telecom + weather data | ⭐⭐⭐⭐ |
| `mit_telecom_parts` | MIT | 3 years, 2,058 sites (similar to Nova Corrente) | ⭐⭐⭐⭐⭐ |

## Output Files

- **Raw Data**: `data/raw/{dataset_id}/`
- **Preprocessed**: `data/processed/{dataset_id}_preprocessed.csv`
- **Unified Dataset**: `data/processed/unified_dataset.csv`
- **Final Dataset**: `data/processed/unified_dataset_with_factors.csv`

## Configuration

Edit `config/datasets_config.json` to:
- Add new datasets
- Modify column mappings
- Adjust preprocessing parameters
- Customize unified schema

## Pipeline Options

```bash
# Run for specific datasets only
python run_pipeline.py --datasets kaggle_daily_demand kaggle_logistics_warehouse

# Skip download step (use existing data)
python run_pipeline.py --skip-download

# Only add external factors to existing unified dataset
python run_pipeline.py --skip-download --skip-preprocess --skip-merge
```

## External Factors

The system adds placeholder columns for:
- **Climate**: temperature, precipitation, humidity, extreme weather flags
- **Economic**: exchange rate, inflation, GDP growth
- **Regulatory**: 5G coverage, compliance dates
- **Operational**: holidays, vacation periods, SLA renewal periods

**Note**: Placeholder values are used. For production, integrate with:
- INMET API (climate)
- BACEN API (economic)
- ANATEL reports (regulatory)
- Company calendars (operational)

## Data Schema

### Required Columns
- `date`: DateTime (YYYY-MM-DD)
- `item_id`: String (unique item identifier)
- `item_name`: String (item description)
- `quantity`: Float (consumption/demand quantity)
- `site_id`: String (tower/site identifier)
- `category`: String (material category)
- `cost`: Float (unit cost)
- `lead_time`: Integer (days)

### Optional Columns (External Factors)
- `temperature`, `precipitation`, `humidity`
- `exchange_rate_brl_usd`, `inflation_rate`, `gdp_growth`
- `5g_coverage`, `is_holiday`, `weekend`
- Impact scores: `climate_impact`, `economic_impact`, `operational_impact`

## Troubleshooting

### Kaggle API Issues
- Ensure `config/kaggle_config.json` exists and has valid credentials
- Check Kaggle account has access to datasets
- Verify internet connection

### Missing Data Files
- Check `data/raw/` directory for downloaded files
- Re-run download step if files are missing
- Some datasets may require manual download (MIT PDF)

### Memory Issues
- Process datasets individually using `--datasets` flag
- Use `--skip-download` and `--skip-preprocess` if raw/preprocessed data exists

## Next Steps

After running the pipeline:

1. **Validate Data Quality**
   - Check `data/processed/preprocessing_log.txt`
   - Review `data/processed/unified_dataset_with_factors.csv`

2. **Train ML Models**
   - Use unified dataset for ARIMA, Prophet, LSTM training
   - Reference: `script.py` for example forecasting code

3. **Integrate Real External Factors**
   - Replace placeholder values with API calls
   - Update `add_external_factors.py` with real data sources

4. **Model Training Pipeline**
   - Implement forecasting models (see `Grok-_27.md` for specs)
   - Calculate Reorder Points (PP)
   - Generate alerts and reports

## File Structure

```
gran_prix/
├── config/
│   ├── datasets_config.json          # Dataset configuration
│   └── kaggle_config.json.template   # Kaggle API template
├── data/
│   ├── raw/                           # Downloaded raw data
│   └── processed/                     # Preprocessed & unified data
├── scrapy_spiders/                    # Web scraping spiders
├── download_datasets.py               # Download script
├── preprocess_datasets.py             # Preprocessing script
├── merge_datasets.py                  # Merge script
├── add_external_factors.py            # External factors script
├── run_pipeline.py                    # Main orchestrator
└── requirements.txt                   # Dependencies
```

## Support

For issues or questions:
- Check log files in `data/` directory
- Review configuration in `config/datasets_config.json`
- Reference project documentation in `Solucao-Completa-Resumida-Final.md`



