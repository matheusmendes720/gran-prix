#!/usr/bin/env python3
"""
Data Validation Script for Nova Corrente Demand Forecasting System
Validates data quality, completeness, and schema compliance
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')

# Setup logging
project_root = Path(__file__).parent.parent.parent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(project_root / 'data' / 'validation_report.txt')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataValidator:
    """Validate dataset quality and schema compliance"""
    
    def __init__(self, config_path: str = None):
        # Get project root (3 levels up from src/validation)
        project_root = Path(__file__).parent.parent.parent
        if config_path is None:
            config_path = str(project_root / "config" / "datasets_config.json")
        else:
            if not Path(config_path).is_absolute():
                config_path = str(project_root / config_path)
        self.config_path = config_path
        self.project_root = project_root
        self.processed_data_dir = project_root / "data" / "processed"
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.unified_schema = self.config.get('unified_schema', {})
        self.validation_results = {
            'schema': {},
            'quality': {},
            'completeness': {},
            'consistency': {}
        }
    
    def validate_schema(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validate dataset schema against unified schema"""
        logger.info("\n" + "="*70)
        logger.info("SCHEMA VALIDATION")
        logger.info("="*70)
        
        results = {}
        required_cols = self.unified_schema.get('required_columns', [])
        optional_cols = self.unified_schema.get('optional_columns', [])
        data_types = self.unified_schema.get('data_types', {})
        
        # Check required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            results['required_columns'] = False
        else:
            logger.info(f"All required columns present: {required_cols}")
            results['required_columns'] = True
        
        # Check data types
        type_errors = []
        for col, expected_type in data_types.items():
            if col not in df.columns:
                continue
            
            actual_type = str(df[col].dtype)
            
            # Special handling for datetime
            if expected_type == 'datetime64[ns]' and not pd.api.types.is_datetime64_any_dtype(df[col]):
                type_errors.append(f"{col}: expected {expected_type}, got {actual_type}")
            elif expected_type != 'datetime64[ns]' and actual_type != expected_type:
                # More lenient check for numeric types
                if expected_type in ['float64', 'int64']:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        type_errors.append(f"{col}: expected numeric, got {actual_type}")
                else:
                    type_errors.append(f"{col}: expected {expected_type}, got {actual_type}")
        
        if type_errors:
            logger.warning(f"Data type mismatches: {type_errors}")
            results['data_types'] = False
        else:
            logger.info("All data types correct")
            results['data_types'] = True
        
        # Check optional columns (informational)
        available_optional = [col for col in optional_cols if col in df.columns]
        logger.info(f"Available optional columns: {len(available_optional)}/{len(optional_cols)}")
        logger.info(f"  {available_optional}")
        
        results['optional_columns_count'] = len(available_optional)
        self.validation_results['schema'] = results
        
        return results
    
    def validate_quality(self, df: pd.DataFrame) -> Dict[str, any]:
        """Validate data quality metrics"""
        logger.info("\n" + "="*70)
        logger.info("DATA QUALITY VALIDATION")
        logger.info("="*70)
        
        results = {}
        
        # Missing values
        missing_counts = df.isnull().sum()
        missing_pct = (missing_counts / len(df) * 100).round(2)
        
        high_missing = missing_pct[missing_pct > 10]
        if len(high_missing) > 0:
            logger.warning(f"Columns with >10% missing values:")
            for col, pct in high_missing.items():
                logger.warning(f"  {col}: {pct}%")
            results['high_missing'] = high_missing.to_dict()
        else:
            logger.info("OK No columns with excessive missing values (>10%)")
            results['high_missing'] = {}
        
        # Duplicate records
        if 'date' in df.columns and 'item_id' in df.columns:
            dup_key = ['date', 'item_id']
            if 'site_id' in df.columns:
                dup_key.append('site_id')
            
            duplicates = df.duplicated(subset=dup_key).sum()
            if duplicates > 0:
                logger.warning(f"Found {duplicates} duplicate records")
                results['duplicates'] = duplicates
            else:
                logger.info("No duplicate records found")
                results['duplicates'] = 0
        
        # Outliers in quantity
        if 'quantity' in df.columns:
            Q1 = df['quantity'].quantile(0.25)
            Q3 = df['quantity'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((df['quantity'] < lower_bound) | (df['quantity'] > upper_bound)).sum()
            outlier_pct = (outliers / len(df) * 100).round(2)
            
            if outlier_pct > 5:
                logger.warning(f"Found {outliers} outliers ({outlier_pct}%) in quantity")
            else:
                logger.info(f"Outliers in quantity: {outliers} ({outlier_pct}%)")
            
            results['outliers'] = {
                'count': int(outliers),
                'percentage': float(outlier_pct),
                'bounds': {'lower': float(lower_bound), 'upper': float(upper_bound)}
            }
        
        # Negative values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        negative_cols = {}
        for col in numeric_cols:
            if col == 'quantity' or col == 'cost':
                negatives = (df[col] < 0).sum()
                if negatives > 0:
                    negative_cols[col] = int(negatives)
        
        if negative_cols:
            logger.warning(f"Found negative values: {negative_cols}")
            results['negative_values'] = negative_cols
        else:
            logger.info("No negative values in quantity/cost columns")
            results['negative_values'] = {}
        
        self.validation_results['quality'] = results
        return results
    
    def validate_completeness(self, df: pd.DataFrame) -> Dict[str, any]:
        """Validate data completeness"""
        logger.info("\n" + "="*70)
        logger.info("COMPLETENESS VALIDATION")
        logger.info("="*70)
        
        results = {}
        
        # Date range completeness
        if 'date' in df.columns:
            df_sorted = df.sort_values('date')
            date_range = df_sorted['date'].max() - df_sorted['date'].min()
            unique_dates = df_sorted['date'].nunique()
            
            logger.info(f"Date range: {df_sorted['date'].min()} to {df_sorted['date'].max()}")
            logger.info(f"Total days: {date_range.days}")
            logger.info(f"Unique dates: {unique_dates}")
            
            # Check for gaps
            expected_days = date_range.days + 1
            coverage = round(unique_dates / expected_days * 100, 2)
            
            if coverage < 80:
                logger.warning(f"Date coverage: {coverage}% (missing {expected_days - unique_dates} days)")
            else:
                logger.info(f"Date coverage: {coverage}%")
            
            results['date_coverage'] = {
                'percentage': float(coverage),
                'expected_days': int(expected_days),
                'actual_days': int(unique_dates),
                'missing_days': int(expected_days - unique_dates)
            }
        
        # Item completeness
        if 'item_id' in df.columns:
            unique_items = df['item_id'].nunique()
            items_with_data = (df.groupby('item_id')['quantity'].sum() > 0).sum()
            
            logger.info(f"Unique items: {unique_items}")
            logger.info(f"Items with consumption data: {items_with_data}")
            
            if items_with_data < unique_items * 0.9:
                logger.warning(f"Only {items_with_data}/{unique_items} items have consumption data")
            else:
                logger.info(f"OK {items_with_data}/{unique_items} items have consumption data")
            
            results['item_coverage'] = {
                'total_items': int(unique_items),
                'items_with_data': int(items_with_data),
                'coverage': float(items_with_data / unique_items * 100)
            }
        
        # Minimum historical data requirement
        if 'date' in df.columns:
            months_of_data = (df['date'].max() - df['date'].min()).days / 30.44
            min_months = self.config.get('preprocessing', {}).get('min_historical_months', 24)
            
            if months_of_data < min_months:
                logger.warning(f"Only {months_of_data:.1f} months of data (minimum: {min_months})")
            else:
                logger.info(f"OK {months_of_data:.1f} months of data available (minimum: {min_months})")
            
            results['historical_coverage'] = {
                'months': float(months_of_data),
                'minimum_required': int(min_months),
                'meets_requirement': months_of_data >= min_months
            }
        
        self.validation_results['completeness'] = results
        return results
    
    def validate_consistency(self, df: pd.DataFrame) -> Dict[str, any]:
        """Validate data consistency"""
        logger.info("\n" + "="*70)
        logger.info("CONSISTENCY VALIDATION")
        logger.info("="*70)
        
        results = {}
        
        # Date consistency
        if 'date' in df.columns:
            future_dates = (df['date'] > pd.Timestamp.now()).sum()
            if future_dates > 0:
                logger.warning(f"Found {future_dates} records with future dates")
                results['future_dates'] = int(future_dates)
            else:
                logger.info("OK No future dates found")
                results['future_dates'] = 0
        
        # Quantity consistency
        if 'quantity' in df.columns:
            zero_quantity = (df['quantity'] == 0).sum()
            zero_pct = (zero_quantity / len(df) * 100).round(2)
            
            if zero_pct > 20:
                logger.warning(f"High percentage of zero quantities: {zero_pct}%")
            else:
                logger.info(f"OK Zero quantities: {zero_pct}%")
            
            results['zero_quantities'] = {
                'count': int(zero_quantity),
                'percentage': float(zero_pct)
            }
        
        # Cost consistency
        if 'cost' in df.columns and 'quantity' in df.columns:
            # Check if cost makes sense relative to quantity
            total_cost = (df['cost'] * df['quantity']).sum()
            if total_cost <= 0:
                logger.warning("Total cost is zero or negative")
                results['cost_consistency'] = False
            else:
                logger.info(f"OK Total cost: R$ {total_cost:,.2f}")
                results['cost_consistency'] = True
        
        self.validation_results['consistency'] = results
        return results
    
    def generate_report(self, output_path: Path = None) -> str:
        """Generate validation report"""
        if output_path is None:
            output_path = self.processed_data_dir / "validation_report.txt"
        
        report_lines = []
        report_lines.append("="*70)
        report_lines.append("DATA VALIDATION REPORT")
        report_lines.append("="*70)
        report_lines.append(f"\nGenerated: {pd.Timestamp.now()}")
        report_lines.append("\n" + "="*70)
        
        # Schema validation
        report_lines.append("\nSCHEMA VALIDATION:")
        for key, value in self.validation_results.get('schema', {}).items():
            if isinstance(value, bool):
                status = "OK PASS" if value else "FAIL FAIL"
                report_lines.append(f"  {key}: {status}")
            else:
                report_lines.append(f"  {key}: {value}")
        
        # Quality validation
        report_lines.append("\nQUALITY VALIDATION:")
        quality = self.validation_results.get('quality', {})
        if quality.get('high_missing'):
            report_lines.append("  High missing values detected")
        if quality.get('duplicates', 0) > 0:
            report_lines.append(f"  Duplicates: {quality.get('duplicates')}")
        if quality.get('negative_values'):
            report_lines.append(f"  Negative values: {quality.get('negative_values')}")
        
        # Completeness
        report_lines.append("\nCOMPLETENESS VALIDATION:")
        completeness = self.validation_results.get('completeness', {})
        if 'date_coverage' in completeness:
            report_lines.append(f"  Date coverage: {completeness['date_coverage']['percentage']}%")
        if 'item_coverage' in completeness:
            report_lines.append(f"  Item coverage: {completeness['item_coverage']['coverage']:.1f}%")
        
        # Consistency
        report_lines.append("\nCONSISTENCY VALIDATION:")
        consistency = self.validation_results.get('consistency', {})
        if consistency.get('future_dates', 0) > 0:
            report_lines.append(f"  Future dates: {consistency['future_dates']}")
        if consistency.get('zero_quantities'):
            report_lines.append(f"  Zero quantities: {consistency['zero_quantities']['percentage']}%")
        
        report = "\n".join(report_lines)
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"\nOK Validation report saved to: {output_path}")
        
        return report
    
    def validate_dataset(self, dataset_path: Path = None) -> bool:
        """Run complete validation"""
        if dataset_path is None:
            dataset_path = self.processed_data_dir / "unified_dataset_with_factors.csv"
        
        if not dataset_path.exists():
            logger.error(f"Dataset not found: {dataset_path}")
            return False
        
        logger.info(f"\n{'='*70}")
        logger.info("VALIDATING DATASET")
        logger.info(f"{'='*70}")
        logger.info(f"Dataset: {dataset_path}")
        
        # Load dataset
        df = pd.read_csv(dataset_path, low_memory=False)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        logger.info(f"Dataset shape: {df.shape}")
        
        # Run validations
        schema_ok = all(self.validate_schema(df).values())
        self.validate_quality(df)
        self.validate_completeness(df)
        self.validate_consistency(df)
        
        # Generate report
        self.generate_report()
        
        # Overall status
        if schema_ok:
            logger.info("\nOK Dataset validation completed")
            logger.info("Check validation_report.txt for details")
            return True
        else:
            logger.warning("\nWARN Dataset validation completed with warnings")
            logger.info("Check validation_report.txt for details")
            return False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate dataset for Nova Corrente demand forecasting'
    )
    parser.add_argument(
        '--dataset',
        default='data/processed/unified_dataset_with_factors.csv',
        help='Path to dataset to validate'
    )
    
    args = parser.parse_args()
    
    validator = DataValidator()
    success = validator.validate_dataset(dataset_path=Path(args.dataset))
    
    exit(0 if success else 1)

if __name__ == "__main__":
    main()

