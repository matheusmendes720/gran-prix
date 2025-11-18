#!/usr/bin/env python3
"""
ACTIVATE GOLD LAYER - Final Step
Activates all gold layer features and creates master ML dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class GoldLayerActivator:
    def __init__(self, silver_root="data/silver/external_factors", 
                 gold_root="data/gold/ml_features"):
        self.silver_root = Path(silver_root)
        self.gold_root = Path(gold_root)
        self.gold_root.mkdir(parents=True, exist_ok=True)
        
        # Create all feature directories
        for category in ['economic', 'climatic', 'global', 'logistics', 'commodities', 'market', 'energy', 'cross_features', 'master']:
            (self.gold_root / category).mkdir(exist_ok=True)
    
    def activate_all_gold_features(self):
        """Activate all gold layer features"""
        logger.info("ACTIVATING ALL GOLD LAYER FEATURES")
        logger.info("=" * 60)
        
        success = True
        
        try:
            # Step 1: Activate basic category features
            self._activate_basic_features()
            
            # Step 2: Create correlation features
            self._activate_correlation_features()
            
            # Step 3: Create lagged features
            self._activate_lagged_features()
            
            # Step 4: Create rolling features
            self._activate_rolling_features()

            # Step 5: Create master dataset
            master_df = self._create_master_dataset()
            success = success and not master_df.empty
            
            # Step 6: Validate gold layer
            validation = self._validate_gold_layer()
            total_records = validation.get('total_records', 0)
            quality_status = validation.get('quality_status')
            if total_records == 0 or quality_status == 'NO DATA':
                success = False
            
            # Step 7: Create ML-ready dataset
            success = success and self._create_ml_ready_dataset()
            
        except Exception as e:
            logger.error(f"Error activating gold layer: {e}")
            success = False
        
        # Create final status report
        self._create_activation_report(success)
        
        logger.info("=" * 60)
        logger.info("GOLD LAYER ACTIVATION COMPLETED")
        logger.info(f"Success: {success}")
        
        return success
    
    def _activate_basic_features(self):
        """Activate basic ML features for each category"""
        logger.info("Step 1: Activating basic features...")
        
        categories = {
            'economic': ['ptax_rates.parquet', 'selic_rates.parquet', 'ipca_inflation.parquet'],
            'climatic': ['inmet_historical.parquet', 'openweather_current.parquet'],
            'global': ['worldbank_gdp.parquet'],
            'logistics': ['anp_fuel_prices.parquet', 'baltic_dry_index.parquet'],
            'commodities': ['prices.parquet'],
            'market': ['indices.parquet'],
            'energy': ['prices.parquet']
        }
        
        for category, files in categories.items():
            try:
                # Load silver data
                silver_dfs = {}
                for file_name in files:
                    file_path = self.silver_root / category / file_name
                    if file_path.exists():
                        df = pd.read_parquet(file_path)
                        silver_dfs[file_name.replace('.parquet', '')] = df
                
                # Create basic features
                if silver_dfs:
                    for key, df in silver_dfs.items():
                        if len(df) > 0:
                            basic_features = self._create_basic_features(df, category, key)
                            self._save_gold_features(basic_features, f"{category}/{key}_basic.parquet")
                            logger.info(f"  {category}/{key}_basic: {len(basic_features)} records")
                
            except Exception as e:
                logger.error(f"Error in {category}: {e}")
        
        logger.info("Basic features activation completed")
    
    def _create_basic_features(self, df, category, feature_name):
        """Create basic ML features for a DataFrame"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date').copy()
        
        # Identify value column
        value_col = None
        for col in df.columns:
            if any(x in col.lower() for x in ['rate', 'price', 'index', 'close', 'temp']):
                value_col = col
                break
        
        if not value_col:
            # If no clear value column, try to find a numeric column
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                value_col = numeric_cols[0]
        
        if value_col:
            # Rate of change features
            df[f'{feature_name}_roc'] = df[value_col].pct_change()
            
            # Moving averages
            df[f'{feature_name}_ma7'] = df[value_col].rolling(7, min_periods=1).mean()
            df[f'{feature_name}_ma30'] = df[value_col].rolling(30, min_periods=1).mean()
            df[f'{feature_name}_ma90'] = df[value_col].rolling(90, min_periods=1).mean()
            
            # Volatility features
            df[f'{feature_name}_volatility_7'] = df[value_col].rolling(7, min_periods=1).std()
            df[f'{feature_name}_volatility_30'] = df[value_col].rolling(30, min_periods=1).std()
            
            # Level features (normalized)
            df[f'{feature_name}_level'] = df[value_col] / df[value_col].rolling(252, min_periods=1).mean()
            
            # Year-over-year change
            df['year'] = df['date'].dt.year
            df[f'{feature_name}_yoy_change'] = df.groupby('year')[value_col].pct_change()
            df[f'{feature_name}_yoy_change'] = df.groupby('year')[f'{feature_name}_yoy_change'].ffill()
            
            # Add to feature set
            df[f'{feature_name}_current'] = df[value_col]
        
        return df
    
    def _activate_correlation_features(self):
        """Create cross-correlation features"""
        logger.info("Step 2: Creating correlation features...")
        
        try:
            # Load economic and market data for correlation
            economic_files = {
                'ptax': self.silver_root / "economic/ptax_rates.parquet",
                'selic': self.silver_root / "economic/selic_rates.parquet"
            }
            
            market_files = {
                'commodities': self.silver_root / "commodities/prices.parquet",
                'market': self.silver_root / "market/indices.parquet"
            }
            
            # Load data
            economic_dfs = {}
            for name, path in economic_files.items():
                if path.exists():
                    try:
                        df = pd.read_parquet(path)
                        if len(df) > 0:
                            economic_dfs[name] = df
                    except Exception as exc:  # noqa: BLE001
                        logger.warning("Failed to load economic dataset %s: %s", name, exc)
                        continue
            
            market_dfs = {}
            for name, path in market_files.items():
                if path.exists():
                    try:
                        df = pd.read_parquet(path)
                        if len(df) > 0:
                            market_dfs[name] = df
                    except Exception as exc:  # noqa: BLE001
                        logger.warning("Failed to load market dataset %s: %s", name, exc)
                        continue
            
            # Create correlation features
            if economic_dfs and market_dfs:
                self._create_economic_market_correlations(economic_dfs, market_dfs)
            
            # Create climatic-economic correlations
            climatic_file = self.silver_root / "climatic/inmet_historical.parquet"
            if climatic_file.exists():
                try:
                    climate_df = pd.read_parquet(climatic_file)
                    if economic_dfs:
                        self._create_climate_economic_correlations(climate_df, economic_dfs)
                except Exception as exc:  # noqa: BLE001
                    logger.warning("Failed to load climatic dataset for correlations: %s", exc)
            
            logger.info("Correlation features completed")
            
        except Exception as e:
            logger.error(f"Error creating correlation features: {e}")
    
    def _create_economic_market_correlations(self, economic_dfs, market_dfs):
        """Create economic-market correlation features"""
        try:
            # Focus on PTAX and market correlations
            if 'ptax' in economic_dfs:
                ptax_df = economic_dfs['ptax'].copy()
                
                # For each market data source
                for market_name, market_df in market_dfs.items():
                    if len(market_df) > 0:
                        # Merge by date
                        merged = pd.merge(
                            ptax_df[['date', 'buy_rate']],
                            market_df[['date', 'price', 'commodity', 'symbol']],
                            on='date',
                            how='inner'
                        )
                        
                        if len(merged) > 0:
                            # Calculate rolling correlations
                            merged['ptax_price_correlation_30'] = (
                                merged['buy_rate'].rolling(30).corr(merged['price'])
                            )
                            
                            # Lagged correlations (does PTAX predict market?)
                            for lag in [1, 7, 30]:
                                merged[f'ptax_price_lag_{lag}'] = merged['buy_rate'].shift(lag)
                            
                            # Save correlation features
                            self._save_gold_features(
                                merged, 
                                f"cross_features/ptax_{market_name}_correlations.parquet"
                            )
                            logger.info(f"  PTAX-{market_name} correlations: {len(merged)} records")
                
        except Exception as e:
            logger.error(f"Error in economic-market correlations: {e}")
    
    def _create_climate_economic_correlations(self, climate_df, economic_dfs):
        """Create climate-economic correlation features"""
        try:
            # Focus on temperature and economic indicators
            if 'temp_c' not in climate_df.columns:
                # Try alternative temperature column
                temp_col = [col for col in climate_df.columns if 'temp' in col.lower()]
                if temp_col:
                    climate_df = climate_df.rename(columns={temp_col[0]: 'temp_c'})
            
            if 'temp_c' in climate_df.columns:
                for econ_name, econ_df in economic_dfs.items():
                    if len(econ_df) > 0:
                        # Merge by date
                        merged = pd.merge(
                            climate_df[['date', 'temp_c', 'state']],
                            econ_df[['date']],
                            on='date',
                            how='inner'
                        )
                        
                        if len(merged) > 0:
                            # Temperature-economic correlations
                            for window in [7, 30, 90]:
                                for state in merged['state'].unique():
                                    state_mask = merged['state'] == state
                                    temp_series = merged.loc[state_mask, 'temp_c']
                                    econ_series = merged.loc[state_mask, econ_df.columns[-1]]
                                    
                                    correlation = temp_series.rolling(window).corr(econ_series)
                                    merged.loc[state_mask, f'temp_{state}_econ_{window}d_corr'] = correlation
                            
                            # Save climate-economic features
                            self._save_gold_features(
                                merged,
                                f"cross_features/climate_{econ_name}_correlations.parquet"
                            )
                            logger.info(f"  Climate-{econ_name} correlations: {len(merged)} records")
                
        except Exception as e:
            logger.error(f"Error in climate-economic correlations: {e}")
    
    def _activate_lagged_features(self):
        """Create lagged features"""
        logger.info("Step 3: Creating lagged features...")
        
        try:
            # Key lag configurations
            lag_configs = {
                'economic': {
                    'files': ['ptax_rates.parquet', 'selic_rates.parquet', 'ipca_inflation.parquet'],
                    'columns': ['buy_rate', 'selic_rate', 'ipca_index'],
                    'lags': [1, 7, 30, 90]
                },
                'market': {
                    'files': ['commodities/prices.parquet', 'market/indices.parquet'],
                    'columns': ['price', 'close'],
                    'lags': [1, 7, 30]
                },
                'climatic': {
                    'files': ['inmet_historical.parquet'],
                    'columns': ['temp_c'],
                    'lags': [1, 7, 30, 90]
                }
            }
            
            for category, config in lag_configs.items():
                for file_name in config['files']:
                    file_path = self.silver_root / category / file_name
                    if file_path.exists():
                        try:
                            df = pd.read_parquet(file_path)
                            if len(df) > 0:
                                # Create lagged features
                                lagged_df = self._create_lagged_features(df, config['columns'], config['lags'])
                                self._save_gold_features(
                                    lagged_df,
                                    f"{category}/{file_name.replace('.parquet', '')}_lagged.parquet"
                                )
                                logger.info(f"  {category}/{file_name} lagged: {len(lagged_df)} records")
                        except Exception as e:
                            logger.warning(f"Error lagging {file_name}: {e}")
            
            logger.info("Lagged features completed")
            
        except Exception as e:
            logger.error(f"Error creating lagged features: {e}")
    
    def _create_lagged_features(self, df, value_columns, lags):
        """Create lagged features for specified columns"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date').copy()
        
        # Ensure value columns exist
        available_cols = [col for col in value_columns if col in df.columns]
        
        if not available_cols:
            return df
        
        # Create lagged features
        for col in available_cols:
            for lag in lags:
                df[f'{col}_lag_{lag}d'] = df[col].shift(lag)
        
        return df
    
    def _activate_rolling_features(self):
        """Create rolling window features"""
        logger.info("Step 4: Creating rolling features...")
        
        try:
            # Rolling window configurations
            rolling_configs = {
                'market': {
                    'files': ['commodities/prices.parquet', 'market/indices.parquet'],
                    'columns': ['price', 'close'],
                    'windows': [7, 30, 90]
                },
                'energy': {
                    'files': ['logistics/anp_fuel_prices.parquet'],
                    'columns': ['price'],
                    'windows': [7, 30]
                },
                'climatic': {
                    'files': ['inmet_historical.parquet'],
                    'columns': ['temp_c', 'precip_mm'],
                    'windows': [7, 30, 90]
                }
            }
            
            for category, config in rolling_configs.items():
                for file_name in config['files']:
                    file_path = self.silver_root / category / file_name
                    if file_path.exists():
                        try:
                            df = pd.read_parquet(file_path)
                            if len(df) > 0:
                                # Create rolling features
                                rolling_df = self._create_rolling_features(df, config['columns'], config['windows'])
                                self._save_gold_features(
                                    rolling_df,
                                    f"{category}/{file_name.replace('.parquet', '')}_rolling.parquet"
                                )
                                logger.info(f"  {category}/{file_name} rolling: {len(rolling_df)} records")
                        except Exception as e:
                            logger.warning(f"Error rolling {file_name}: {e}")
            
            logger.info("Rolling features completed")
            
        except Exception as e:
            logger.error(f"Error creating rolling features: {e}")
    
    def _create_master_dataset(self):
        """Create master ML dataset with all features"""
        logger.info("Step 5: Creating master dataset...")
        
        try:
            all_features = []
            
            # Load all gold features
            for feature_file in self.gold_root.rglob("*.parquet"):
                try:
                    df = pd.read_parquet(feature_file)
                    if len(df) > 0:
                        # Add source information
                        df['source_table'] = feature_file.relative_to(self.gold_root).as_posix()
                        all_features.append(df)
                except Exception as e:
                    logger.warning(f"Error reading {feature_file}: {e}")
            
            if all_features:
                # Merge all features
                master_df = pd.concat(all_features, ignore_index=True)
                
                # Remove duplicate date columns
                date_cols = [col for col in master_df.columns if col == 'date']
                if len(date_cols) > 1:
                    # Keep first date column, drop others
                    master_df = master_df.drop(columns=date_cols[1:])
                
                # Sort by date
                if 'date' in master_df.columns:
                    master_df = master_df.sort_values('date')
                    master_df['date'] = pd.to_datetime(master_df['date'])
                
                # Add feature metadata
                master_df['feature_count'] = len(master_df.columns)
                master_df['record_created'] = datetime.now()
                
                # Save master dataset
                self._save_gold_features(master_df, 'master/master_features.parquet')
                logger.info(f"  Master dataset: {len(master_df)} records, {len(master_df.columns)} columns")
                
                return master_df
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error creating master dataset: {e}")
            return pd.DataFrame()
    
    def _validate_gold_layer(self):
        """Validate gold layer quality and completeness"""
        logger.info("Step 6: Validating gold layer...")
        
        validation_results = {
            'total_files': 0,
            'total_records': 0,
            'quality_issues': 0,
            'categories': {}
        }
        
        for parquet_file in self.gold_root.rglob("*.parquet"):
            try:
                df = pd.read_parquet(parquet_file)
                
                # Basic quality checks
                null_rate = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                
                category = parquet_file.parent.name
                if category not in validation_results['categories']:
                    validation_results['categories'][category] = {
                        'files': 0,
                        'records': 0,
                        'avg_null_rate': 0,
                        'max_null_rate': 0
                    }
                
                validation_results['categories'][category]['files'] += 1
                validation_results['categories'][category]['records'] += len(df)
                validation_results['categories'][category]['avg_null_rate'] += null_rate
                validation_results['categories'][category]['max_null_rate'] = max(
                    validation_results['categories'][category]['max_null_rate'], null_rate
                )
                
                if null_rate > 20:
                    validation_results['quality_issues'] += 1
                    logger.warning(f"  High null rate in {parquet_file.name}: {null_rate:.1f}%")
                
                validation_results['total_files'] += 1
                validation_results['total_records'] += len(df)
                
            except Exception as e:
                logger.error(f"  Error validating {parquet_file.name}: {e}")
                validation_results['quality_issues'] += 1
        
        # Calculate overall metrics
        total_files = validation_results['total_files']
        if total_files > 0:
            avg_null_rate = sum([
                cat['avg_null_rate'] for cat in validation_results['categories'].values()
            ]) / len(validation_results['categories'])
            
            if validation_results['quality_issues'] == 0:
                quality_status = "EXCELLENT"
            elif validation_results['quality_issues'] <= total_files * 0.1:
                quality_status = "GOOD"
            elif validation_results['quality_issues'] <= total_files * 0.2:
                quality_status = "FAIR"
            else:
                quality_status = "POOR"
        else:
            quality_status = "NO DATA"
        
        validation_results['quality_status'] = quality_status
        validation_results['avg_null_rate'] = avg_null_rate if total_files > 0 else 0
        
        logger.info(f"  Total files: {validation_results['total_files']}")
        logger.info(f"  Total records: {validation_results['total_records']:,}")
        logger.info(f"  Quality status: {quality_status}")
        logger.info(f"  Average null rate: {validation_results['avg_null_rate']:.1f}%")
        logger.info(f"  Quality issues: {validation_results['quality_issues']}")
        
        return validation_results
    
    def _create_ml_ready_dataset(self):
        """Create final ML-ready dataset"""
        logger.info("Step 7: Creating ML-ready dataset...")
        
        try:
            # Load master dataset
            master_file = self.gold_root / "master/master_features.parquet"
            if not master_file.exists():
                logger.warning("Master dataset not found, skipping ML-ready creation")
                return False
            
            master_df = pd.read_parquet(master_file)
            
            if len(master_df) == 0:
                logger.warning("Master dataset is empty, skipping ML-ready creation")
                return False
            
            # ML-ready preprocessing
            ml_df = master_df.copy()
            
            # Handle nulls
            numeric_cols = ml_df.select_dtypes(include=[np.number]).columns
            ml_df[numeric_cols] = ml_df[numeric_cols].ffill()
            
            # Remove duplicate features
            ml_df = ml_df.loc[:, ~ml_df.columns.duplicated()]
            
            # Add ML metadata
            ml_df['ml_ready'] = True
            ml_df['preprocessing_date'] = datetime.now()
            
            # Feature selection for demand forecasting
            demand_features = [
                # Economic features
                'ptax_current', 'ptax_ma7', 'ptax_ma30', 'ptax_volatility_30',
                'selic_current', 'selic_ma7', 'selic_ma30', 'selic_volatility_30',
                'ipca_current', 'ipca_level',
                
                # Market features
                'price_ma7', 'price_ma30', 'price_volatility_30',
                'price_lag_7d', 'price_lag_30d',
                
                # Climate features
                'temp_c_ma7', 'temp_c_ma30', 'temp_c_lag_7d',
                'precip_mm_rolling30',
                
                # Cross-correlation features
                'ptax_price_correlation_30',
                'temp_econ_correlation_30d'
            ]
            
            # Filter available demand features
            available_features = [f for f in demand_features if f in ml_df.columns]
            ml_ready_df = ml_df[['date'] + available_features].copy()
            
            # Save ML-ready dataset
            self._save_gold_features(ml_ready_df, 'ml_ready/demand_forecasting_features.parquet')
            logger.info(f"  ML-ready dataset: {len(ml_ready_df)} records, {len(ml_ready_df.columns)} features")
            logger.info(f"  Demand forecasting features: {len(available_features)} available")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating ML-ready dataset: {e}")
            return False
    
    def _save_gold_features(self, df, path):
        """Save DataFrame to gold layer"""
        try:
            full_path = self.gold_root / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            df.to_parquet(full_path, index=False)
            
        except Exception as e:
            logger.error(f"Error saving gold features to {path}: {e}")
    
    def _create_activation_report(self, success):
        """Create activation report"""
        logger.info("Creating activation report...")
        
        try:
            report = {
                'activation_timestamp': datetime.now().isoformat(),
                'overall_success': success,
                'gold_layer_root': str(self.gold_root),
                'feature_categories_created': self._count_feature_categories(),
                'total_feature_files': len(list(self.gold_root.rglob("*.parquet"))),
                'total_records': self._count_total_records(),
                'ml_readiness': self._assess_ml_readiness(),
                'next_steps': [
                    'ML models can now use gold layer features',
                    'Use master_features.parquet for comprehensive training',
                    'Use demand_forecasting_features.parquet for focused training',
                    'Set up model training and validation pipelines',
                    'Deploy to production environment'
                ]
            }
            
            # Save report
            report_file = self.gold_root / "GOLD_LAYER_ACTIVATION_REPORT.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"  Activation report saved: {report_file}")
            
            return report
            
        except Exception as e:
            logger.error(f"Error creating activation report: {e}")
            return None
    
    def _count_feature_categories(self):
        """Count feature categories"""
        categories = set()
        for parquet_file in self.gold_root.rglob("*.parquet"):
            categories.add(parquet_file.parent.name)
        return list(categories)
    
    def _count_total_records(self):
        """Count total records in gold layer"""
        total_records = 0
        for parquet_file in self.gold_root.rglob("*.parquet"):
            try:
                df = pd.read_parquet(parquet_file)
                total_records += len(df)
            except:
                continue
        return total_records
    
    def _assess_ml_readiness(self):
        """Assess ML readiness"""
        total_files = len(list(self.gold_root.rglob("*.parquet")))
        
        # Check for ML-ready features
        demand_features_file = self.gold_root / "ml_ready/demand_forecasting_features.parquet"
        master_features_file = self.gold_root / "master/master_features.parquet"
        
        if demand_features_file.exists() and master_features_file.exists():
            try:
                demand_df = pd.read_parquet(demand_features_file)
                master_df = pd.read_parquet(master_features_file)
                
                if len(demand_df) > 0 and len(master_df) > 0:
                    return "ML_READY"
            except:
                pass
        
        if total_files >= 50:  # Reasonable number of feature files
            return "FEATURES_AVAILABLE"
        elif total_files >= 20:
            return "PARTIALLY_READY"
        else:
            return "NEEDS_WORK"

def main():
    """Main execution function"""
    logger.info("STARTING GOLD LAYER ACTIVATION")
    
    activator = GoldLayerActivator()
    success = activator.activate_all_gold_features()
    
    if success:
        logger.info("✅ Gold layer activation completed successfully!")
        logger.info("✅ All ML features created and ready for use!")
    else:
        logger.error("❌ Gold layer activation failed!")
    
    return success

if __name__ == "__main__":
    main()