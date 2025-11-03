#!/usr/bin/env python3
"""
Master Dataset Integration Script
Integrates all datasets into one comprehensive ML-ready dataset

Combines:
- unified_brazilian_telecom_ml_ready.csv (2,880 records, 30 columns)
- unified_brazilian_telecom_nova_corrente_enriched.csv (2,880 records, 74 columns)
- unified_comprehensive_ml_ready.csv (1,676 records, 36 columns)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging
import json

# Setup paths
BASE_DIR = Path(__file__).parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'data' / 'master_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MasterDatasetIntegrator:
    """Integrates all datasets into one comprehensive ML-ready dataset"""
    
    def __init__(self):
        self.datasets = {}
        self.integrated_df = None
        
    def load_all_datasets(self):
        """Load all available datasets"""
        logger.info("="*80)
        logger.info("LOADING ALL DATASETS")
        logger.info("="*80)
        
        dataset_files = {
            'brazilian_telecom': PROCESSED_DATA_DIR / 'unified_brazilian_telecom_ml_ready.csv',
            'nova_corrente_enriched': PROCESSED_DATA_DIR / 'unified_brazilian_telecom_nova_corrente_enriched.csv',
            'comprehensive': PROCESSED_DATA_DIR / 'unified_comprehensive_ml_ready.csv'
        }
        
        for name, file_path in dataset_files.items():
            if file_path.exists():
                try:
                    logger.info(f"\nLoading: {name}")
                    df = pd.read_csv(file_path)
                    
                    # Convert date column
                    if 'date' in df.columns:
                        df['date'] = pd.to_datetime(df['date'], errors='coerce')
                    
                    self.datasets[name] = df
                    logger.info(f"  [OK] Loaded {len(df):,} records, {len(df.columns)} columns")
                    
                    # Log sample columns
                    logger.info(f"  Sample columns: {list(df.columns[:10])}...")
                except Exception as e:
                    logger.error(f"  [FAILED] Could not load {name}: {e}")
            else:
                logger.warning(f"  [SKIP] File not found: {file_path}")
        
        logger.info(f"\nTotal datasets loaded: {len(self.datasets)}")
        return len(self.datasets) > 0
    
    def merge_datasets(self):
        """Merge all datasets intelligently"""
        logger.info("\n" + "="*80)
        logger.info("MERGING ALL DATASETS")
        logger.info("="*80)
        
        if not self.datasets:
            logger.error("No datasets loaded!")
            return None
        
        # Start with the largest/most complete dataset
        if 'nova_corrente_enriched' in self.datasets:
            base_df = self.datasets['nova_corrente_enriched'].copy()
            logger.info(f"Starting with Nova Corrente enriched: {len(base_df):,} records")
        elif 'brazilian_telecom' in self.datasets:
            base_df = self.datasets['brazilian_telecom'].copy()
            logger.info(f"Starting with Brazilian telecom: {len(base_df):,} records")
        else:
            base_df = list(self.datasets.values())[0].copy()
            logger.info(f"Starting with first dataset: {len(base_df):,} records")
        
        # Merge comprehensive dataset on date
        if 'comprehensive' in self.datasets:
            logger.info("\nMerging comprehensive dataset...")
            comp_df = self.datasets['comprehensive'].copy()
            
            # Convert dates for merging
            if 'date' in comp_df.columns:
                comp_df['date'] = pd.to_datetime(comp_df['date'], errors='coerce')
            
            # Merge on date (left join to keep base_df structure)
            merged_df = base_df.merge(
                comp_df,
                on='date',
                how='outer',
                suffixes=('', '_comp')
            )
            
            logger.info(f"  [OK] Merged: {len(merged_df):,} records, {len(merged_df.columns)} columns")
            base_df = merged_df
        
        # Handle duplicate columns intelligently
        logger.info("\nCleaning duplicate columns...")
        duplicate_cols = []
        for col in base_df.columns:
            if col.endswith('_comp') or col.endswith('_x') or col.endswith('_y'):
                # Check if original column exists
                original_col = col.replace('_comp', '').replace('_x', '').replace('_y', '')
                if original_col in base_df.columns:
                    duplicate_cols.append(col)
        
        # Remove duplicate columns, keep originals
        if duplicate_cols:
            base_df = base_df.drop(columns=duplicate_cols)
            logger.info(f"  [OK] Removed {len(duplicate_cols)} duplicate columns")
        
        self.integrated_df = base_df
        logger.info(f"\n[OK] Final integrated dataset: {len(base_df):,} records, {len(base_df.columns)} columns")
        
        return base_df
    
    def enrich_with_metadata(self):
        """Add metadata and derived features"""
        logger.info("\n" + "="*80)
        logger.info("ENRICHING WITH METADATA")
        logger.info("="*80)
        
        if self.integrated_df is None:
            logger.error("No integrated dataset!")
            return None
        
        df = self.integrated_df.copy()
        
        # Add date features if date column exists
        if 'date' in df.columns:
            logger.info("Adding date features...")
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['quarter'] = df['date'].dt.quarter
            df['day_of_year'] = df['date'].dt.dayofyear
            df['weekday'] = df['date'].dt.weekday
            df['is_weekend'] = df['weekday'] >= 5
            df['is_quarter_end'] = df['date'].dt.is_quarter_end
            df['is_year_end'] = df['date'].dt.is_year_end
            
            logger.info(f"  [OK] Added {9} date features")
        
        # Add derived features
        logger.info("Adding derived features...")
        
        # Technology migration score
        if 'technology' in df.columns:
            tech_migration_map = {'2g': 0, '3g': 1, '4g': 2, '5g': 3}
            df['tech_migration_score'] = df['technology'].map(tech_migration_map).fillna(0)
        
        # Demand risk score (combining multiple factors)
        risk_factors = []
        if 'corrosion_risk' in df.columns:
            corrosion_risk_map = {'high': 3, 'medium': 2, 'low': 1}
            df['corrosion_risk_score'] = df['corrosion_risk'].map(corrosion_risk_map).fillna(1)
            risk_factors.append('corrosion_risk_score')
        
        if 'sla_violation_risk' in df.columns:
            sla_risk_map = {'high': 3, 'medium': 2, 'low': 1}
            df['sla_risk_score'] = df['sla_violation_risk'].map(sla_risk_map).fillna(1)
            risk_factors.append('sla_risk_score')
        
        if risk_factors:
            df['total_risk_score'] = df[risk_factors].sum(axis=1)
            logger.info(f"  [OK] Added risk scoring with {len(risk_factors)} factors")
        
        # Market concentration impact
        if 'market_concentration_hhi' in df.columns and 'competition_index' in df.columns:
            df['market_efficiency_score'] = (
                (1 - df['market_concentration_hhi'] / 10000) * 0.5 +
                df['competition_index'] * 0.5
            )
            logger.info(f"  [OK] Added market efficiency score")
        
        # Regional investment priority
        if 'investment_multiplier' in df.columns and 'coverage_pct' in df.columns:
            df['investment_priority_score'] = (
                df['investment_multiplier'] * 0.6 +
                (df['coverage_pct'] / 100) * 0.4
            )
            logger.info(f"  [OK] Added investment priority score")
        
        self.integrated_df = df
        logger.info(f"\n[OK] Enriched dataset: {len(df):,} records, {len(df.columns)} columns")
        
        return df
    
    def save_integrated_dataset(self) -> Path:
        """Save integrated dataset"""
        logger.info("\n" + "="*80)
        logger.info("SAVING INTEGRATED DATASET")
        logger.info("="*80)
        
        if self.integrated_df is None:
            logger.error("No integrated dataset to save!")
            return None
        
        # Save full dataset
        output_file = PROCESSED_DATA_DIR / 'unified_master_ml_ready.csv'
        self.integrated_df.to_csv(output_file, index=False)
        
        logger.info(f"[OK] Saved master dataset: {output_file}")
        logger.info(f"   Records: {len(self.integrated_df):,}")
        logger.info(f"   Columns: {len(self.integrated_df.columns)}")
        
        # Create summary statistics
        summary = {
            'integration_date': datetime.now().isoformat(),
            'total_records': int(len(self.integrated_df)),
            'total_columns': int(len(self.integrated_df.columns)),
            'datasets_integrated': list(self.datasets.keys()),
            'date_range': {
                'start': str(self.integrated_df['date'].min()) if 'date' in self.integrated_df.columns else None,
                'end': str(self.integrated_df['date'].max()) if 'date' in self.integrated_df.columns else None
            },
            'column_categories': {
                'temporal': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['date', 'year', 'month', 'quarter', 'day'])]),
                'economic': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['gdp', 'inflation', 'exchange', 'arpu', 'revenue'])]),
                'regulatory': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['sla', 'penalty', 'regulatory', 'competition', 'tax'])]),
                'technology': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['5g', 'technology', 'tech', 'spectrum'])]),
                'infrastructure': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['tower', 'coverage', 'investment', 'infrastructure'])]),
                'market': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['subscriber', 'operator', 'market', 'share'])]),
                'climate': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['temperature', 'humidity', 'precipitation', 'wind', 'corrosion'])]),
                'geographic': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['region', 'country', 'location', 'coastal', 'salvador'])]),
                'derived': len([c for c in self.integrated_df.columns if any(x in c.lower() for x in ['score', 'multiplier', 'priority', 'risk'])]),
            },
            'missing_data_pct': float((self.integrated_df.isnull().sum().sum() / (len(self.integrated_df) * len(self.integrated_df.columns))) * 100)
        }
        
        summary_file = PROCESSED_DATA_DIR / 'master_integration_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"[OK] Summary saved: {summary_file}")
        
        # Create feature importance preview (correlation with date if available)
        if 'date' in self.integrated_df.columns:
            numeric_cols = self.integrated_df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0:
                logger.info(f"\nFeature categories:")
                for category, count in summary['column_categories'].items():
                    logger.info(f"  {category}: {count} features")
        
        return output_file
    
    def run_complete_integration(self):
        """Run complete integration pipeline"""
        logger.info("="*80)
        logger.info("MASTER DATASET INTEGRATION PIPELINE")
        logger.info("="*80)
        
        # Step 1: Load all datasets
        if not self.load_all_datasets():
            logger.error("Failed to load datasets!")
            return None
        
        # Step 2: Merge datasets
        merged_df = self.merge_datasets()
        if merged_df is None:
            logger.error("Failed to merge datasets!")
            return None
        
        # Step 3: Enrich with metadata
        enriched_df = self.enrich_with_metadata()
        if enriched_df is None:
            logger.error("Failed to enrich dataset!")
            return None
        
        # Step 4: Save integrated dataset
        output_file = self.save_integrated_dataset()
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("INTEGRATION COMPLETE!")
        logger.info("="*80)
        logger.info(f"[OK] Master dataset: {output_file}")
        logger.info(f"   Records: {len(self.integrated_df):,}")
        logger.info(f"   Columns: {len(self.integrated_df.columns)}")
        logger.info(f"\nNext steps:")
        logger.info("1. Review master dataset")
        logger.info("2. Prepare train/test splits")
        logger.info("3. Train ML/DL models!")
        
        return output_file


def main():
    """Main entry point"""
    integrator = MasterDatasetIntegrator()
    integrator.run_complete_integration()


if __name__ == "__main__":
    main()

