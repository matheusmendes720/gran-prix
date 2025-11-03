#!/usr/bin/env python3
"""
External Factors Integration Script for Nova Corrente Demand Forecasting System
Adds placeholder columns for external factors (climate, economic, regulatory, operational)
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Setup logging
project_root = Path(__file__).parent.parent.parent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(project_root / 'data' / 'processed' / 'external_factors_log.txt')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ExternalFactorsAdder:
    """Add external factors to unified dataset"""
    
    def __init__(self, config_path: str = None):
        # Get project root (2 levels up from src/pipeline)
        project_root = Path(__file__).parent.parent.parent
        if config_path is None:
            config_path = str(project_root / "config" / "datasets_config.json")
        else:
            # If relative path, make it relative to project root
            if not Path(config_path).is_absolute():
                config_path = str(project_root / config_path)
        self.config_path = config_path
        self.project_root = project_root
        self.processed_data_dir = project_root / "data" / "processed"
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def load_unified_dataset(self) -> Optional[pd.DataFrame]:
        """Load unified dataset"""
        dataset_path = self.processed_data_dir / "unified_dataset.csv"
        
        if not dataset_path.exists():
            logger.error(f"Unified dataset not found at {dataset_path}")
            logger.error("Please run merge_datasets.py first")
            return None
        
        logger.info(f"Loading unified dataset from {dataset_path}")
        df = pd.read_csv(dataset_path, low_memory=False)
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        logger.info(f"Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def add_climate_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add climate factors from INMET"""
        logger.info("Adding climate factors from INMET...")
        
        try:
            from src.pipeline.brazilian_apis import INMETClimateDataFetcher
            
            if 'date' in df.columns:
                # Get date range
                min_date = df['date'].min().strftime('%Y-%m-%d')
                max_date = df['date'].max().strftime('%Y-%m-%d')
                
                # Fetch climate data for Salvador (main operations)
                logger.info(f"  - Fetching climate data from {min_date} to {max_date}")
                inmet_fetcher = INMETClimateDataFetcher("A601")  # Salvador station
                climate_df = inmet_fetcher.fetch_daily_climate_data(min_date, max_date)
                
                # Merge climate data
                if len(climate_df) > 0:
                    df = df.merge(climate_df, on='date', how='left', suffixes=('', '_climate'))
                    logger.info(f"  - Merged {len(climate_df)} climate records")
                else:
                    logger.warning("  - No climate data fetched, using fallback")
                    self._add_climate_placeholders(df)
            else:
                logger.warning("Date column missing, skipping climate factors")
                self._add_climate_placeholders(df)
        except Exception as e:
            logger.error(f"Error fetching climate data: {e}")
            logger.info("  - Falling back to placeholder data")
            self._add_climate_placeholders(df)
        
        return df
    
    def _add_climate_placeholders(self, df: pd.DataFrame) -> None:
        """Add placeholder climate data (fallback)"""
        np.random.seed(42)
        if 'date' in df.columns:
            df['temperature'] = np.random.uniform(22, 32, len(df))
            df['precipitation'] = np.random.exponential(5, len(df))
            df['humidity'] = np.random.uniform(70, 90, len(df))
            df['extreme_heat'] = (df['temperature'] > 32).astype(int)
            df['heavy_rain'] = (df['precipitation'] > 50).astype(int)
            df['high_humidity'] = (df['humidity'] > 80).astype(int)
            logger.info("  - Added placeholder climate data")
    
    def add_economic_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add economic factors from BACEN"""
        logger.info("Adding economic factors from BACEN...")
        
        try:
            from src.pipeline.brazilian_apis import BACENEconomicDataFetcher
            
            if 'date' in df.columns:
                # Get date range
                min_date = df['date'].min().strftime('%Y-%m-%d')
                max_date = df['date'].max().strftime('%Y-%m-%d')
                
                # Fetch economic data
                logger.info(f"  - Fetching economic data from {min_date} to {max_date}")
                bacen_fetcher = BACENEconomicDataFetcher()
                
                # Fetch exchange rate
                exchange_df = bacen_fetcher.fetch_exchange_rate_usd_brl(min_date, max_date)
                if len(exchange_df) > 0:
                    df = df.merge(exchange_df, on='date', how='left')
                    logger.info(f"  - Merged {len(exchange_df)} exchange rate records")
                else:
                    logger.warning("  - No exchange rate data fetched")
                
                # Fetch inflation
                inflation_df = bacen_fetcher.fetch_inflation_ipca(min_date, max_date)
                if len(inflation_df) > 0:
                    df = df.merge(inflation_df, on='date', how='left')
                    logger.info(f"  - Merged {len(inflation_df)} inflation records")
                else:
                    logger.warning("  - No inflation data fetched")
                
                # Fill missing with placeholders if needed
                if 'exchange_rate_brl_usd' not in df.columns:
                    df['exchange_rate_brl_usd'] = np.random.uniform(5.0, 5.5, len(df))
                if 'inflation_rate' not in df.columns:
                    df['inflation_rate'] = np.random.uniform(3.0, 6.0, len(df))
                
                # Economic flags
                df['high_inflation'] = (df['inflation_rate'] > 5).astype(int)
                df['currency_devaluation'] = (df['exchange_rate_brl_usd'] > 5.3).astype(int)
                
                logger.info("  - Added economic flags")
            else:
                logger.warning("Date column missing, skipping economic factors")
                self._add_economic_placeholders(df)
        except Exception as e:
            logger.error(f"Error fetching economic data: {e}")
            logger.info("  - Falling back to placeholder data")
            self._add_economic_placeholders(df)
        
        return df
    
    def _add_economic_placeholders(self, df: pd.DataFrame) -> None:
        """Add placeholder economic data (fallback)"""
        np.random.seed(42)
        df['exchange_rate_brl_usd'] = np.random.uniform(5.0, 5.5, len(df))
        df['inflation_rate'] = np.random.uniform(3.0, 6.0, len(df))
        df['high_inflation'] = (df['inflation_rate'] > 5).astype(int)
        df['currency_devaluation'] = (df['exchange_rate_brl_usd'] > 5.3).astype(int)
        logger.info("  - Added placeholder economic data")
    
    def add_regulatory_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add regulatory factor placeholder columns"""
        logger.info("Adding regulatory factors...")
        
        # Placeholder for Anatel 5G expansion data
        # These would come from ANATEL reports or regulatory databases
        df['5g_coverage'] = 0  # Placeholder: 0 or 1 based on 5G rollout dates
        df['regulatory_compliance_date'] = None  # Dates of compliance deadlines
        
        # Simulate 5G expansion timeline (2024-2026)
        if 'date' in df.columns:
            # Assume 5G rollout started accelerating in 2024
            df['5g_coverage'] = (
                (df['date'] >= pd.Timestamp('2024-01-01')).astype(int)
            )
            df['5g_expansion_rate'] = np.where(
                df['date'] >= pd.Timestamp('2024-01-01'),
                (df['date'] - pd.Timestamp('2024-01-01')).dt.days / 365.0 * 0.2,
                0
            )
        
        logger.info("  - Added 5g_coverage flag")
        logger.info("  - Added 5g_expansion_rate")
        logger.info("  - Added regulatory_compliance_date placeholder")
        
        return df
    
    def add_operational_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add operational factors from Brazilian calendars"""
        logger.info("Adding operational factors...")
        
        try:
            from src.pipeline.brazilian_apis import BrazilianOperationalDataFetcher
            
            if 'date' in df.columns:
                operational_fetcher = BrazilianOperationalDataFetcher()
                
                # Get unique years in dataset
                years = df['date'].dt.year.unique()
                
                # Initialize holiday flags
                df['is_holiday'] = 0
                df['is_carnival'] = 0
                df['is_vacation_period'] = 0
                
                # Add Brazilian public holidays
                logger.info("  - Adding Brazilian public holidays...")
                for year in years:
                    holidays_list = operational_fetcher.fetch_brazilian_holidays(int(year))
                    holiday_dates = pd.to_datetime(holidays_list, errors='coerce')
                    df.loc[df['date'].isin(holiday_dates), 'is_holiday'] = 1
                
                # Add Carnival dates (major telecom traffic event)
                logger.info("  - Adding Carnival dates...")
                for year in years:
                    carnival_start, carnival_end = operational_fetcher.get_carnival_dates(int(year))
                    carnival_dates = pd.date_range(carnival_start, carnival_end, freq='D')
                    df.loc[df['date'].isin(carnival_dates), 'is_carnival'] = 1
                    df.loc[df['date'].isin(carnival_dates), 'is_holiday'] = 1
                
                # July vacation period
                df.loc[df['date'].dt.month == 7, 'is_vacation_period'] = 1
                
                # SLA renewal periods (January and July)
                df['sla_renewal_period'] = (
                    (df['date'].dt.month == 1) | (df['date'].dt.month == 7)
                ).astype(int)
                
                # Weekend flag
                if 'weekend' not in df.columns:
                    df['weekend'] = (df['date'].dt.weekday >= 5).astype(int)
                
                logger.info("  - Added Brazilian holidays and events")
                logger.info("  - Added vacation periods")
                logger.info("  - Added SLA renewal periods")
        except Exception as e:
            logger.error(f"Error fetching operational data: {e}")
            logger.info("  - Falling back to placeholder data")
            self._add_operational_placeholders(df)
        
        return df
    
    def _add_operational_placeholders(self, df: pd.DataFrame) -> None:
        """Add placeholder operational data (fallback)"""
        if 'date' in df.columns:
            df['is_holiday'] = 0
            df['is_vacation_period'] = 0
            df.loc[df['date'].dt.month == 7, 'is_vacation_period'] = 1
            df.loc[(df['date'].dt.month == 12) | (df['date'].dt.month == 1), 'is_holiday'] = 1
            df['sla_renewal_period'] = ((df['date'].dt.month == 1) | (df['date'].dt.month == 7)).astype(int)
            if 'weekend' not in df.columns:
                df['weekend'] = (df['date'].dt.weekday >= 5).astype(int)
            logger.info("  - Added placeholder operational data")
    
    def add_factor_impact_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate impact scores based on external factors"""
        logger.info("Calculating external factor impact scores...")
        
        # Climate impact score (0-1 scale, higher = more demand)
        if all(col in df.columns for col in ['extreme_heat', 'heavy_rain', 'high_humidity']):
            df['climate_impact'] = (
                df['extreme_heat'] * 0.3 +
                df['heavy_rain'] * 0.4 +
                df['high_humidity'] * 0.2
            ).clip(0, 1)
        
        # Economic impact score (higher = potential supply chain delays)
        if all(col in df.columns for col in ['high_inflation', 'currency_devaluation']):
            df['economic_impact'] = (
                df['high_inflation'] * 0.5 +
                df['currency_devaluation'] * 0.5
            ).clip(0, 1)
        
        # Operational impact score
        if all(col in df.columns for col in ['is_holiday', 'is_vacation_period', 'sla_renewal_period']):
            df['operational_impact'] = (
                df['sla_renewal_period'] * 0.5 -  # Increases demand
                df['is_vacation_period'] * 0.25 -  # Decreases demand
                df['is_holiday'] * 0.25
            ).clip(-1, 1)
        
        # Combined impact score for demand adjustment
        if 'climate_impact' in df.columns:
            df['demand_adjustment_factor'] = 1.0 + (
                df.get('climate_impact', 0) * 0.3 +
                df.get('economic_impact', 0) * 0.1 +
                df.get('operational_impact', 0).clip(0, 1) * 0.2
            )
        
        logger.info("  - Calculated climate_impact score")
        logger.info("  - Calculated economic_impact score")
        logger.info("  - Calculated operational_impact score")
        logger.info("  - Calculated demand_adjustment_factor")
        
        return df
    
    def add_external_factors(self, save_output: bool = True) -> Optional[pd.DataFrame]:
        """Add all external factors to unified dataset"""
        logger.info(f"\n{'='*70}")
        logger.info("ADDING EXTERNAL FACTORS")
        logger.info(f"{'='*70}\n")
        
        # Load unified dataset
        df = self.load_unified_dataset()
        if df is None:
            return None
        
        logger.info(f"Initial dataset shape: {df.shape}")
        
        # Add external factors
        df = self.add_climate_factors(df)
        df = self.add_economic_factors(df)
        df = self.add_regulatory_factors(df)
        df = self.add_operational_factors(df)
        
        # Calculate impact scores
        df = self.add_factor_impact_scores(df)
        
        logger.info(f"\nFinal dataset shape: {df.shape}")
        logger.info(f"New columns added: {len(df.columns) - len(self.load_unified_dataset().columns)}")
        
        # Save enriched dataset
        if save_output:
            output_path = self.processed_data_dir / "unified_dataset_with_factors.csv"
            df.to_csv(output_path, index=False)
            logger.info(f"\nSaved enriched dataset to: {output_path}")
        
        # Summary
        logger.info("\n" + "="*70)
        logger.info("EXTERNAL FACTORS SUMMARY")
        logger.info("="*70)
        logger.info("\nNote: External factors are currently placeholder values.")
        logger.info("To integrate real data:")
        logger.info("  - Climate: INMET API (https://www.inmet.gov.br/)")
        logger.info("  - Economic: BACEN API (https://www.bcb.gov.br/)")
        logger.info("  - Regulatory: ANATEL reports")
        logger.info("  - Operational: Company calendars/historical patterns")
        
        return df

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Add external factors to unified dataset for Nova Corrente demand forecasting'
    )
    parser.add_argument(
        '--config',
        default='config/datasets_config.json',
        help='Path to datasets configuration file'
    )
    
    args = parser.parse_args()
    
    adder = ExternalFactorsAdder(config_path=args.config)
    enriched_df = adder.add_external_factors()
    
    if enriched_df is None:
        logger.error("Failed to add external factors!")
        exit(1)
    
    logger.info("\n✅ External factors integration completed successfully!")

if __name__ == "__main__":
    main()


