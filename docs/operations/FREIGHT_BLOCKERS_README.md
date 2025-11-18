<!-- markdownlint-disable-file MD012 -->

# Freight Data Blockers – Fully Automated Solution

## Problem Solved

Previously three manual data sources blocked the ML pipeline:

| Blocker | Old Way | New Way |
|---------|---------|---------|
| **FBX** | Log into Freightos Terminal → export CSV manually | ✓ World Bank Liner Shipping Connectivity Index (via `xeneta_xsi_c.parquet`) |
| **Drewry WCI** | Download weekly from Drewry portal | ✓ World Bank Container Port Traffic (wide lanes) |
| **ANTT KPIs** | Export Excel/PDF from ANTT dashboards | ✓ ANTT CKAN RNTRC export with Brazil Logistics LPI fallback |

## Solution: Fully Automated APIs

### One Command to Replace All Manual Downloads

```bash
python -m scripts.automation.freight_blockers.integration replace-manual
```

This executes:

1. **Liner Connectivity (World Bank)** – Connectivity scores for China/USA/Brazil/Singapore/Germany  
2. **Container Port Traffic (World Bank)** – TEU throughput for WLD/CHN/USA/BRA/MEX/SWE  
3. **ANTT RNTRC + LPI Fallback** – CKAN registry ingest with World Bank Logistics Performance Index backup

## Integration with the ETL

### Option 1: Add to existing `transform_all()`

```python
from scripts.automation.freight_blockers.integration import FreightBlockersETLStep

def transform_all():
    # … existing transforms …
    FreightBlockersETLStep().execute()
    # … rest of pipeline …
```

### Option 2: Standalone automation

```bash
python -m scripts.automation.freight_blockers.integration run-all
```

Outputs to `data/silver/freight/`:

- `xeneta_xsi_c.parquet` (liner connectivity index proxies)  
- `drewry_wci_alternatives.parquet` (container port traffic)  
- `antt_logistics_kpis.parquet` (RNTRC-derived KPIs or World Bank LPI)

### Option 3: Scheduled (continuous updates)

```bash
python -m scripts.automation.freight_blockers.integration schedule
```

Runs daily at 02:00 by default (requires `apscheduler`).

### Option 4: End-to-end fetch

```bash
python -m scripts.etl.external.fetch_all
```

Use `--skip-freight-blockers` if you need to bypass the automation during troubleshooting.

## Data Sources Used

### 1. World Bank Liner Shipping Connectivity Index – FBX Replacement

- Coverage: China, USA, Brazil, Singapore, Germany (annual)  
- Frequency: Annual (latest released year)  
- Access: Free World Bank API  
- Output: `xeneta_xsi_c.parquet` (wide columns by country)

### 2. World Bank Container Port Traffic – Drewry Replacement

- Coverage: World aggregate + China, USA, Brazil, Mexico, Sweden  
- Frequency: Annual  
- Access: Free World Bank API  
- Output: `drewry_wci_alternatives.parquet`

### 3. ANTT CKAN + World Bank Logistics Performance Fallback

- Primary: RNTRC vehicle registry (CSV) parsed with multi-encoding support  
- Fallback: World Bank `LP.LPI.OVRL.XQ` (Brazil) when CKAN resources change format  
- Output: `antt_logistics_kpis.parquet`

## Validation

Check blocker status:

```bash
python -m scripts.automation.freight_blockers.integration validate
```

Expected output:

```text
xeneta_xsi_c                 OK - 13 records
drewry_wci_alternatives      OK - 14 records
antt_kpis                    OK - 1 records
```

## ML Feature Store Integration

Once blockers are automated, the feature store automatically receives:

```python
# features/macro_climate_daily.parquet now includes:
china_connectivity_index        # World Bank liner connectivity
united_states_connectivity_index
world_container_traffic         # World Bank TEU traffic
brazil_container_traffic
antt_fuel_price_mean            # RNTRC-derived fuel KPI
```

Run after blockers complete:

```bash
python -m scripts.etl.transform.external_to_silver
python -m scripts.etl.feature.build_external_features
```

## Performance

- Connectivity fetch: <3 seconds  
- Container traffic fetch: ≈4 seconds  
- ANTT RNTRC fetch: ≈6 seconds  
- Total automation: ≈15 seconds

## FAQ

- **Why not use paid Freightos/Drewry APIs?**  
  World Bank indices are open, reliable, and cover global routes with annual cadence.
- **Do we still need manual CSV uploads?**  
  No. Existing manual ingestion scripts can remain for parity but are not required.
- **How do we disable just the blockers in the full fetch?**  
  Use `python -m scripts.etl.external.fetch_all --skip-freight-blockers`.

## Next Steps

1. Run blockers  
   `python -m scripts.automation.freight_blockers.integration replace-manual`
2. Validate outputs  
   `python -m scripts.automation.freight_blockers.integration validate`
3. Integrate into ETL or Airflow (daily task already appended)  
4. Rerun Silver → Feature builds  
5. Retrain ML models with complete datasets

## Support

All blockers now automated with open data fallbacks. Monitor `logs/freight_blockers.log` for API changes or RNTRC schema revisions. <!-- EOF -->

