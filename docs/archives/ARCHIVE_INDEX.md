# 📚 Archive Index

## Nova Corrente - Reports & Documentation Archive

This archive contains all reports, success summaries, changelogs, benchmarks, and analysis documents organized by topic and subject.

## 📁 Archive Structure

### Archive Types

- **reports/** - Detailed analysis and status reports
- **success/** - Success summaries and milestone reports  
- **changelogs/** - Change logs and version history
- **benchmarks/** - Performance benchmarks and comparisons
- **analysis/** - Deep dive analysis documents
- **screenshots/** - Visual documentation and UI screenshots
- **exports/** - Exported data and results

### Topics & Subjects

#### Pipeline
- `data_ingestion/`
- `data_processing/`
- `data_validation/`
- `feature_engineering/`

#### Datasets
- `kaggle/`
- `zenodo/`
- `github/`
- `api_fetched/`
- `scraped/`
- `enrichment/`
- `merging/`

#### Models
- `arima/`
- `prophet/`
- `lstm/`
- `xgboost/`
- `ensemble/`
- `training/`
- `evaluation/`
- `comparison/`

#### Dashboard
- `ui/`
- `visualizations/`
- `charts/`
- `metrics/`
- `alerts/`
- `user_experience/`

#### Api
- `endpoints/`
- `integration/`
- `performance/`
- `documentation/`
- `testing/`

#### Deployment
- `docker/`
- `kubernetes/`
- `infrastructure/`
- `ci_cd/`
- `monitoring/`

#### Visualization
- `charts/`
- `maps/`
- `analytics/`
- `reports/`
- `exports/`

#### Integration
- `brazilian_data/`
- `external_apis/`
- `third_party/`
- `system_integration/`

#### Performance
- `optimization/`
- `benchmarks/`
- `scalability/`
- `resource_usage/`

#### Benchmarks
- `model_comparison/`
- `accuracy/`
- `speed/`
- `resource_usage/`
- `cost_analysis/`

#### Documentation
- `architecture/`
- `guides/`
- `tutorials/`
- `api_docs/`
- `changelog/`

#### Testing
- `unit_tests/`
- `integration_tests/`
- `e2e_tests/`
- `performance_tests/`

#### Errors
- `bug_reports/`
- `fixes/`
- `investigations/`
- `solutions/`

#### Enhancements
- `features/`
- `improvements/`
- `optimizations/`
- `new_capabilities/`

## 📅 Timeline Organization

Reports are also organized by:
- **by_year/** - 2024, 2025, etc.
- **by_month/** - Monthly archives
- **by_quarter/** - Quarterly archives

## 🔍 Quick Navigation

Use this index to quickly find reports by:
1. **Topic** - What subject area (pipeline, models, dashboard, etc.)
2. **Archive Type** - What kind of document (report, success, benchmark, etc.)
3. **Timeline** - When it was created

## 📝 Naming Convention

Files should follow this naming pattern:
- `REPORT_{TOPIC}_{SUBTOPIC}_{DATE}.md`
- `SUCCESS_{TOPIC}_{DESCRIPTION}_{DATE}.md`
- `BENCHMARK_{METRIC}_{DATE}.md`

Example: `REPORT_models_lstm_training_2025-11-01.md`

## 🚀 Organizing Reports

To organize existing reports into this archive structure:

```bash
# Organize all reports
python backend/scripts/organize_reports.py

# Organize from specific directory
python backend/scripts/organize_reports.py --source ./docs

# Dry run (preview only)
python backend/scripts/organize_reports.py --dry-run
```

The script will:
1. Detect topic from filename and content
2. Extract date from filename
3. Copy report to appropriate archive location
4. Organize by topic, subtopic, and timeline

---
*Last updated: 2025-11-01*
