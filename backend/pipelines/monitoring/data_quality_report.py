#!/usr/bin/env python3
"""
Data Quality Report Generator for Nova Corrente Demand Forecasting System
Generates comprehensive data quality reports with statistics and visualizations
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict
import warnings
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOTTING = True
except ImportError:
    HAS_PLOTTING = False
    warnings.warn("Matplotlib/Seaborn not available. Visualizations will be skipped.")

warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataQualityReporter:
    """Generate data quality reports"""
    
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
        self.reports_dir = project_root / "data" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def generate_statistics(self, df: pd.DataFrame) -> Dict:
        """Generate descriptive statistics"""
        logger.info("Generating statistics...")
        
        stats = {
            'basic': {
                'total_records': len(df),
                'total_columns': len(df.columns),
                'date_range': {
                    'start': str(df['date'].min()) if 'date' in df.columns else None,
                    'end': str(df['date'].max()) if 'date' in df.columns else None,
                    'days': int((df['date'].max() - df['date'].min()).days) if 'date' in df.columns else None
                }
            }
        }
        
        # Item statistics
        if 'item_id' in df.columns:
            stats['items'] = {
                'unique_items': int(df['item_id'].nunique()),
                'items_with_data': int((df.groupby('item_id')['quantity'].sum() > 0).sum())
            }
        
        # Quantity statistics
        if 'quantity' in df.columns:
            stats['quantity'] = {
                'total': float(df['quantity'].sum()),
                'mean': float(df['quantity'].mean()),
                'median': float(df['quantity'].median()),
                'std': float(df['quantity'].std()),
                'min': float(df['quantity'].min()),
                'max': float(df['quantity'].max()),
                'zero_count': int((df['quantity'] == 0).sum()),
                'negative_count': int((df['quantity'] < 0).sum())
            }
        
        # Cost statistics
        if 'cost' in df.columns:
            stats['cost'] = {
                'total': float(df['cost'].sum()),
                'mean': float(df['cost'].mean()),
                'median': float(df['cost'].median()),
                'std': float(df['cost'].std())
            }
        
        # Site statistics
        if 'site_id' in df.columns:
            stats['sites'] = {
                'unique_sites': int(df['site_id'].nunique()),
                'sites_with_data': int((df.groupby('site_id')['quantity'].sum() > 0).sum())
            }
        
        # Dataset source distribution
        if 'dataset_source' in df.columns:
            stats['sources'] = df['dataset_source'].value_counts().to_dict()
        
        return stats
    
    def generate_report_text(self, df: pd.DataFrame, stats: Dict) -> str:
        """Generate text report"""
        report_lines = []
        report_lines.append("="*70)
        report_lines.append("DATA QUALITY REPORT - NOVA CORRENTE")
        report_lines.append("="*70)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("="*70)
        
        # Basic statistics
        basic = stats.get('basic', {})
        report_lines.append("\nBASIC STATISTICS")
        report_lines.append("-"*70)
        report_lines.append(f"Total Records: {basic.get('total_records', 'N/A'):,}")
        report_lines.append(f"Total Columns: {basic.get('total_columns', 'N/A')}")
        
        if 'date_range' in basic and basic['date_range']['start']:
            report_lines.append(f"\nDate Range:")
            report_lines.append(f"  Start: {basic['date_range']['start']}")
            report_lines.append(f"  End: {basic['date_range']['end']}")
            report_lines.append(f"  Days: {basic['date_range']['days']:,}")
        
        # Item statistics
        if 'items' in stats:
            items = stats['items']
            report_lines.append("\nITEM STATISTICS")
            report_lines.append("-"*70)
            report_lines.append(f"Unique Items: {items.get('unique_items', 'N/A'):,}")
            report_lines.append(f"Items with Data: {items.get('items_with_data', 'N/A'):,}")
        
        # Quantity statistics
        if 'quantity' in stats:
            qty = stats['quantity']
            report_lines.append("\nQUANTITY STATISTICS")
            report_lines.append("-"*70)
            report_lines.append(f"Total Quantity: {qty.get('total', 0):,.2f}")
            report_lines.append(f"Mean: {qty.get('mean', 0):.2f}")
            report_lines.append(f"Median: {qty.get('median', 0):.2f}")
            report_lines.append(f"Std Dev: {qty.get('std', 0):.2f}")
            report_lines.append(f"Min: {qty.get('min', 0):.2f}")
            report_lines.append(f"Max: {qty.get('max', 0):,.2f}")
            report_lines.append(f"Zero Count: {qty.get('zero_count', 0):,}")
            report_lines.append(f"Negative Count: {qty.get('negative_count', 0):,}")
        
        # Cost statistics
        if 'cost' in stats:
            cost = stats['cost']
            report_lines.append("\nCOST STATISTICS")
            report_lines.append("-"*70)
            report_lines.append(f"Total Cost: R$ {cost.get('total', 0):,.2f}")
            report_lines.append(f"Mean Cost: R$ {cost.get('mean', 0):.2f}")
            report_lines.append(f"Median Cost: R$ {cost.get('median', 0):.2f}")
        
        # Source distribution
        if 'sources' in stats:
            report_lines.append("\nDATASET SOURCE DISTRIBUTION")
            report_lines.append("-"*70)
            for source, count in stats['sources'].items():
                pct = (count / basic.get('total_records', 1)) * 100
                report_lines.append(f"  {source}: {count:,} records ({pct:.1f}%)")
        
        # Missing values
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        high_missing = missing_pct[missing_pct > 0]
        
        if len(high_missing) > 0:
            report_lines.append("\nMISSING VALUES")
            report_lines.append("-"*70)
            for col, pct in high_missing.items():
                report_lines.append(f"  {col}: {missing[col]:,} ({pct}%)")
        
        report_lines.append("\n" + "="*70)
        
        return "\n".join(report_lines)
    
    def generate_visualizations(self, df: pd.DataFrame, stats: Dict):
        """Generate visualization plots"""
        if not HAS_PLOTTING:
            logger.warning("Matplotlib not available. Skipping visualizations.")
            return
        
        logger.info("Generating visualizations...")
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
        # 1. Time series plot
        if 'date' in df.columns and 'quantity' in df.columns:
            fig, ax = plt.subplots()
            df_ts = df.groupby('date')['quantity'].sum().reset_index()
            ax.plot(df_ts['date'], df_ts['quantity'], linewidth=1.5)
            ax.set_title('Total Daily Demand Over Time', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Quantity', fontsize=12)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(self.reports_dir / 'daily_demand_timeseries.png', dpi=150)
            plt.close()
            logger.info("  ✓ Saved: daily_demand_timeseries.png")
        
        # 2. Top items by quantity
        if 'item_id' in df.columns and 'quantity' in df.columns:
            top_items = df.groupby('item_id')['quantity'].sum().sort_values(ascending=False).head(20)
            
            fig, ax = plt.subplots()
            top_items.plot(kind='barh', ax=ax)
            ax.set_title('Top 20 Items by Total Quantity', fontsize=14, fontweight='bold')
            ax.set_xlabel('Total Quantity', fontsize=12)
            ax.set_ylabel('Item ID', fontsize=12)
            ax.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            plt.savefig(self.reports_dir / 'top_items_quantity.png', dpi=150)
            plt.close()
            logger.info("  ✓ Saved: top_items_quantity.png")
        
        # 3. Quantity distribution
        if 'quantity' in df.columns:
            fig, ax = plt.subplots()
            df['quantity'].hist(bins=50, ax=ax, edgecolor='black')
            ax.set_title('Quantity Distribution', fontsize=14, fontweight='bold')
            ax.set_xlabel('Quantity', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.savefig(self.reports_dir / 'quantity_distribution.png', dpi=150)
            plt.close()
            logger.info("  ✓ Saved: quantity_distribution.png")
        
        # 4. Dataset source distribution
        if 'dataset_source' in df.columns:
            source_counts = df['dataset_source'].value_counts()
            
            fig, ax = plt.subplots()
            source_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%')
            ax.set_title('Records by Dataset Source', fontsize=14, fontweight='bold')
            ax.set_ylabel('')
            plt.tight_layout()
            plt.savefig(self.reports_dir / 'source_distribution.png', dpi=150)
            plt.close()
            logger.info("  ✓ Saved: source_distribution.png")
    
    def generate_report(self, dataset_path: Path = None):
        """Generate complete quality report"""
        if dataset_path is None:
            dataset_path = self.processed_data_dir / "unified_dataset_with_factors.csv"
        
        if not dataset_path.exists():
            logger.error(f"Dataset not found: {dataset_path}")
            return
        
        logger.info(f"\n{'='*70}")
        logger.info("GENERATING DATA QUALITY REPORT")
        logger.info(f"{'='*70}")
        logger.info(f"Dataset: {dataset_path}")
        
        # Load dataset
        df = pd.read_csv(dataset_path, low_memory=False)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Generate statistics
        stats = self.generate_statistics(df)
        
        # Generate text report
        report_text = self.generate_report_text(df, stats)
        
        # Save text report
        report_path = self.reports_dir / "data_quality_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        logger.info(f"✓ Text report saved to: {report_path}")
        
        # Generate visualizations
        self.generate_visualizations(df, stats)
        
        # Save JSON statistics
        stats_path = self.reports_dir / "statistics.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, default=str)
        logger.info(f"✓ Statistics saved to: {stats_path}")
        
        # Print summary
        print("\n" + report_text)
        
        logger.info(f"\n✓ Quality report generation completed!")
        logger.info(f"Reports directory: {self.reports_dir}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate data quality report for Nova Corrente demand forecasting'
    )
    parser.add_argument(
        '--dataset',
        default='data/processed/unified_dataset_with_factors.csv',
        help='Path to dataset'
    )
    
    args = parser.parse_args()
    
    reporter = DataQualityReporter()
    reporter.generate_report(dataset_path=Path(args.dataset))

if __name__ == "__main__":
    main()



