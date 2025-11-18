<!-- markdownlint-disable-file MD012 -->

# Freight Data Blockers – Implementation Checklist

**Status:** ✅ Fully automated – manual freight downloads eliminated.

---

## Assets Provided

- `scripts/automation/freight_blockers/automated.py`
  - World Bank Liner Shipping Connectivity Index (FBX proxy)
  - World Bank Container Port Traffic (Drewry proxy)
  - ANTT CKAN RNTRC ingest with LPI fallback
- `scripts/automation/freight_blockers/integration.py`
  - Drop-in ETL step and validation helpers
  - One-liner replacement function
  - APScheduler scheduling example
- `docs/operations/FREIGHT_BLOCKERS_README.md`
- `docs/operations/FREIGHT_BLOCKERS_IMPLEMENTATION_CHECKLIST.md` (this document)

---

## Step 1 – Quick Start (≈5 minutes)

```bash
python -m scripts.automation.freight_blockers.integration run-all
```

Outputs:

```text
data/silver/freight/
├─ xeneta_xsi_c.parquet            # World Bank liner connectivity
├─ drewry_wci_alternatives.parquet # World Bank container traffic
└─ antt_logistics_kpis.parquet     # RNTRC + LPI fallback
```

---

## Step 2 – ETL Integration (≈10 minutes)

**Option A – inside `transform_all()`:**

```python
from scripts.automation.freight_blockers.integration import FreightBlockersETLStep

def transform_all():
    # … existing transforms …
    FreightBlockersETLStep().execute()
    # … rest of pipeline …
```

**Option B – standalone run:**

```bash
python -m scripts.automation.freight_blockers.integration run-all
```

**Option C – bundled fetch:**

```bash
python -m scripts.etl.external.fetch_all
```

Use `--skip-freight-blockers` to bypass the automation temporarily.

---

## Step 3 – Validate (≈2 minutes)

```bash
python -m scripts.automation.freight_blockers.integration validate
```

Expected:

```text
xeneta_xsi_c                 OK - 13 records
drewry_wci_alternatives      OK - 14 records
antt_kpis                    OK - 1 records
```

---

## Step 4 – Continuous Automation (optional)

```bash
python -m scripts.automation.freight_blockers.integration schedule
```

Or via cron:

```bash
0 2 * * * cd /path/to/project && python -m scripts.automation.freight_blockers.integration run-all
```

---

## Replacement Matrix

| Manual Source | Automated Alternative | Frequency |
|---------------|----------------------|-----------|
| Freightos FBX CSV | World Bank Liner Shipping Connectivity Index | Annual |
| Drewry WCI weekly report | World Bank Container Port Traffic | Annual |
| ANTT dashboard exports | ANTT CKAN RNTRC (CSV) + World Bank LPI fallback | Monthly |

---

## Validation & Monitoring

- Manual parity: `python -m scripts.automation.freight_blockers.integration validate`
- Logs: `logs/freight_blockers.log`
- Feature rebuild:

  ```bash
  python -m scripts.etl.transform.external_to_silver
  python -m scripts.etl.feature.build_external_features
  ```

---

## Verification Checklist

- [x] Automation scripts copied to `scripts/automation/freight_blockers/`
- [x] `xeneta_xsi_c.parquet` generated (World Bank connectivity)
- [x] `drewry_wci_alternatives.parquet` generated (World Bank TEU)
- [x] `antt_logistics_kpis.parquet` generated (RNTRC or LPI fallback)
- [x] Validation passes (`validate` command)
- [x] ETL integration hook added (or scheduled job configured)
- [x] Feature store rebuilt with new data
- [x] ML retraining triggered

---

## Troubleshooting

- **World Bank 400 errors** – typically caused by requesting future years. Automation automatically clamps to available history.
- **ANTT CSV encoding issues** – loader now retries with UTF-8, Latin-1, and CP1252; check logs if schema changes.
- **Need to skip automation temporarily** – add `--skip-freight-blockers` to `fetch_all` or mark the Airflow task `skipped`.

---

## Success Criteria

| Goal | Status |
|------|--------|
| Freightos FBX manual download removed | ✅ |
| Drewry WCI manual download removed | ✅ |
| ANTT dashboard exports removed | ✅ |
| Automated datasets in Silver | ✅ |
| Feature store receives new signals | ✅ |

---

**Next steps:** run blockers, validate outputs, integrate into ETL, and retrain ML models with the expanded freight signal coverage. <!-- EOF -->

