# Operations Manual

## Overview
Complete manual for operating and maintaining the external factors ML pipeline.

## Daily Operations

### Automated Scripts
```bash
# Run complete pipeline
cd scripts/etl/transform
python complete_pipeline_push.py

# Run individual components
python build_silver_fixed.py      # Silver layer
python build_gold_layer.py          # Gold layer
```

### Monitoring Commands
```bash
# Quick status check
cd data/landing/external_factors-raw
python simple_status.py

# Daily maintenance
cd data/landing/external_factors-raw
python maintain_external_factors.py
```

### Data Freshness Checks
- **Economic Data**: Daily (PTAX, SELIC, IPCA)
- **Climate Data**: Daily (INMET, OpenWeather)
- **Market Data**: Daily (indices, commodities)
- **Logistics Data**: Weekly (fuel, shipping)

## Data Quality Monitoring

### Automated Quality Checks
```python
# Run quality validation
cd scripts/etl/transform
python validate_external_factors.py

# Key metrics to monitor:
# - Null rate (< 5%)
# - Date range consistency
# - Value range validation
# - Duplicate detection
```

### Alerting System
- **Failed Downloads**: Immediate notification
- **High Null Rates**: Alert when > 10%
- **Data Freshness**: Alert when data > 48h old
- **Pipeline Failures**: Immediate error notifications

## Weekly Operations

### Data Review
```bash
# Review weekly data quality
cd data/landing/external_factors-raw
python weekly_quality_report.py
```

### Performance Monitoring
- **Pipeline Runtime**: Track execution time
- **Storage Usage**: Monitor disk space
- **API Rate Limits**: Track usage and limits
- **Error Rates**: Monitor success/failure ratios

## Monthly Operations

### Full Data Refresh
```bash
# Complete monthly refresh
cd scripts/etl/external
python fetch_all.py --full-refresh

# Rebuild all layers
cd scripts/etl/transform
python complete_pipeline_push.py --force-rebuild
```

### Model Retraining
```bash
# Monthly model update with new features
cd models
python retrain_demand_model.py --use-external-features
```

### Documentation Updates
- Update feature catalog with new features
- Review and update data schemas
- Update operations manual with new procedures
- Archive monthly reports

## Troubleshooting

### Common Issues
1. **API Rate Limits**
   - Add delays between API calls
   - Implement retry mechanisms with exponential backoff
   - Monitor API usage and limits

2. **Data Quality Issues**
   - Run validation scripts
   - Check for null values and outliers
   - Verify date ranges and consistency

3. **Pipeline Failures**
   - Check logs for specific error messages
   - Verify input data format and structure
   - Run individual components to isolate issues

4. **Performance Issues**
   - Monitor memory usage during large data processing
   - Optimize SQL queries and data loading
   - Consider data sampling for development

### Error Resolution
```python
# Example: Handling missing data
def handle_missing_data(df, strategy='interpolate'):
    '''
    Handle missing data in DataFrame
    
    Args:
        df: Input DataFrame
        strategy: 'interpolate', 'forward_fill', 'drop'
    
    Returns:
        DataFrame: Cleaned DataFrame
    '''
    if strategy == 'interpolate':
        return df.interpolate(method='time')
    elif strategy == 'forward_fill':
        return df.fillna(method='ffill')
    elif strategy == 'drop':
        return df.dropna()
    else:
        return df
```

## Backup and Recovery

### Automated Backups
```bash
# Daily backup of all data layers
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf external_factors_backup_$DATE.tar.gz     data/landing/external_factors-raw     data/silver/external_factors     data/gold/ml_features
```

### Recovery Procedures
1. **Data Corruption**: Restore from latest backup
2. **Pipeline Failure**: Rebuild from silver layer
3. **Feature Issues**: Regenerate from silver layer
4. **Complete Failure**: Restore entire pipeline from backup

## Security Considerations

### API Keys Management
- Store API keys in environment variables
- Rotate keys regularly
- Use different keys for different environments
- Monitor API key usage and access

### Data Privacy
- Anonymize personal data
- Follow GDPR and LGPD guidelines
- Implement data access controls
- Regular security audits

## Performance Optimization

### Data Processing
- Use Parquet format for efficient storage
- Implement incremental updates
- Parallel process multiple categories
- Cache frequently accessed data

### ML Pipeline
- Use feature selection to reduce dimensionality
- Implement model versioning
- Optimize hyperparameter tuning
- Use appropriate model complexity

---

*Operations Manual Last Updated: 2025-11-11 13:46:25*
