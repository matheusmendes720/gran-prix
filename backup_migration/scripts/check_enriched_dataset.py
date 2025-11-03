#!/usr/bin/env python3
"""Check enriched Nova Corrente dataset"""

import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
dataset_file = BASE_DIR / 'data' / 'processed' / 'unified_brazilian_telecom_nova_corrente_enriched.csv'
summary_file = BASE_DIR / 'data' / 'processed' / 'nova_corrente_enrichment_summary.json'

if dataset_file.exists():
    df = pd.read_csv(dataset_file)
    print("="*80)
    print("NOVA CORRENTE ENRICHED DATASET")
    print("="*80)
    print(f"\nRecords: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    
    # Find new columns
    new_cols = [c for c in df.columns if any(x in c.lower() for x in [
        'sla', 'climate', '5g', 'lead', 'tower', 'contract', 'penalty', 
        'corrosion', 'coastal', 'availability', 'downtime', 'humidity', 
        'precipitation', 'wind', 'expansion', 'investment', 'milestone'
    ])]
    
    print(f"\nNew enrichment columns: {len(new_cols)}")
    print("\nSample new columns:")
    for i, col in enumerate(new_cols[:20], 1):
        print(f"  {i:2d}. {col}")
    
    if summary_file.exists():
        summary = json.load(open(summary_file))
        print(f"\nEnrichment Summary:")
        print(f"  Original columns: {summary.get('original_columns', 'N/A')}")
        print(f"  Enriched columns: {summary.get('enriched_columns', 'N/A')}")
        print(f"  New features added: {summary.get('new_features_added', 'N/A')}")
        print(f"  Factors included: {len(summary.get('factors_included', []))}")
        print(f"\nFactors:")
        for factor in summary.get('factors_included', []):
            print(f"  - {factor}")
    
    print(f"\nSample data:")
    print(df[['date', 'sla_penalty_brl', '5g_coverage_pct', 'total_lead_time_days', 
              'corrosion_risk', 'sla_violation_risk']].head(10))
else:
    print(f"Dataset not found: {dataset_file}")

