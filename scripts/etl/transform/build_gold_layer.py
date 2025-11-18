#!/usr/bin/env python3
"""
GOLD LAYER BUILDER - ML Feature Engineering
Creates comprehensive ML-ready features from silver layer data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gold_build.log', encoding='utf-8', errors='replace'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GoldLayerBuilder:
    def __init__(self, silver_root="data/silver/external_factors", 
                 gold_root="data/gold/ml_features"):
        self.silver_root = Path(silver_root)
        self.gold_root = Path(gold_root)
        self.gold_root.mkdir(parents=True, exist_ok=True)
        
        # Create feature categories
        for category in ['economic', 'climatic', 'global', 'logistics', 'commodities', 'market', 'energy']:
            (self.gold_root / category).mkdir(exist_ok=True)
    
    def build_all_gold_features(self):
        """Build comprehensive gold layer ML features"""
        logger.info("Building gold layer ML features")
        logger.info("=" * 60)
        
        success = True
        features_built = []
        
        try:
            # Economic features
            if self._build_economic_features():
                features_built.append('economic')
                logger.info("✅ Economic features built")
            
            # Climate features
            if self._build_climatic_features():
                features_built.append('climatic')
                logger.info("✅ Climate features built")
            
            # Global features
            if self._build_global_features():
                features_built.append('global')
                logger.info("✅ Global features built")
            
            # Logistics features
            if self._build_logistics_features():
                features_built.append('logistics')
                logger.info("✅ Logistics features built")
            
            # Commodities features
            if self._build_commodities_features():
                features_built.append('commodities')
                logger.info("✅ Commodities features built")
            
            # Market features
            if self._build_market_features():
                features_built.append('market')
                logger.info("✅ Market features built")
            
            # Energy features
            if self._build_energy_features():
                features_built.append('energy')
                logger.info("✅ Energy features built")
            
            # Cross-features
            if self._build_cross_features():
                features_built.append('cross_features')
                logger.info("✅ Cross-features built")
            
            # Master feature table
            if self._build_master_features():
                features_built.append('master')
                logger.info("✅ Master features built")
            
            logger.info(f"Gold layer completed! Features built: {len(features_built)}")
            
        except Exception as e:
            logger.error(f"Error building gold layer: {e}")
            success = False
        
        # Create final report
        self._create_final_report(features_built, success)
        return success
    
    def _build_economic_features(self):
        """Build economic ML features"""
        try:
            # Load PTAX data
            ptax_file = self.silver_root / "macro/ptax_rates.parquet"
            if ptax_file.exists():
                ptax_df = pd.read_parquet(ptax_file)
                if "dataHoraCotacao" in ptax_df.columns:
                    ptax_df = ptax_df.copy()
                    ptax_df["date"] = pd.to_datetime(ptax_df["dataHoraCotacao"], errors="coerce").dt.date
                    if "currency" in ptax_df.columns:
                        # Prioritise USD but fall back to first currency available
                        usd_rows = ptax_df[ptax_df["currency"].str.upper() == "USD"]
                        ptax_df = usd_rows if not usd_rows.empty else ptax_df
                    ptax_df = ptax_df.rename(
                        columns={
                            "cotacaoCompra": "buy_rate",
                            "cotacaoVenda": "sell_rate",
                            "paridadeCompra": "parity_buy",
                            "paridadeVenda": "parity_sell",
                        }
                    )
                ptax_features = self._create_rate_features(ptax_df, "ptax")
                if not ptax_features.empty:
                    self._save_gold_features(ptax_features, "economic/ptax_features.parquet")

            # Load SELIC data
            selic_file = self.silver_root / "macro/selic_daily.parquet"
            if selic_file.exists():
                selic_df = pd.read_parquet(selic_file)
                selic_features = self._create_rate_features(selic_df, "selic")
                if not selic_features.empty:
                    self._save_gold_features(selic_features, "economic/selic_features.parquet")

            # Load IPCA data
            ipca_file = self.silver_root / "macro/ipca_monthly.parquet"
            if ipca_file.exists():
                ipca_df = pd.read_parquet(ipca_file)
                if "period" in ipca_df.columns:
                    ipca_df = ipca_df.copy()
                    ipca_df["date"] = pd.to_datetime(ipca_df["period"], errors="coerce")
                ipca_features = self._create_inflation_features(ipca_df)
                if not ipca_features.empty:
                    self._save_gold_features(ipca_features, "economic/ipca_features.parquet")

            return True
            
        except Exception as e:
            logger.error(f"Error building economic features: {e}")
            return False
    
    def _build_climatic_features(self):
        """Build climate ML features"""
        try:
            # Load INMET data
            inmet_file = self.silver_root / "climatic/inmet_historical.parquet"
            if inmet_file.exists():
                inmet_df = pd.read_parquet(inmet_file)
                inmet_features = self._create_climate_features(inmet_df)
                self._save_gold_features(inmet_features, 'climatic/inmet_features.parquet')
            
            # Load weather data
            weather_file = self.silver_root / "climatic/openweather_current.parquet"
            if weather_file.exists():
                weather_df = pd.read_parquet(weather_file)
                weather_features = self._create_climate_features(weather_df)
                self._save_gold_features(weather_features, 'climatic/weather_features.parquet')
            
            return True
            
        except Exception as e:
            logger.error(f"Error building climatic features: {e}")
            return False
    
    def _build_global_features(self):
        """Build global ML features"""
        try:
            global_file = self.silver_root / "global/worldbank_gdp.parquet"
            if global_file.exists():
                global_df = pd.read_parquet(global_file)
                global_features = self._create_global_features(global_df)
                self._save_gold_features(global_features, 'global/global_features.parquet')
            
            return True
            
        except Exception as e:
            logger.error(f"Error building global features: {e}")
            return False
    
    def _build_logistics_features(self):
        """Build logistics ML features"""
        try:
            # Load fuel prices
            fuel_file = self.silver_root / "logistics/anp_fuel_prices.parquet"
            if fuel_file.exists():
                fuel_df = pd.read_parquet(fuel_file)
                fuel_features = self._create_fuel_features(fuel_df)
                self._save_gold_features(fuel_features, 'logistics/fuel_features.parquet')
            
            # Load Baltic Dry index
            baltic_file = self.silver_root / "logistics/baltic_dry_index.parquet"
            if baltic_file.exists():
                baltic_df = pd.read_parquet(baltic_file)
                baltic_features = self._create_shipping_features(baltic_df)
                self._save_gold_features(baltic_features, 'logistics/shipping_features.parquet')
            
            return True
            
        except Exception as e:
            logger.error(f"Error building logistics features: {e}")
            return False
    
    def _build_commodities_features(self):
        """Build commodities ML features"""
        try:
            commodity_file = self.silver_root / "commodities/prices.parquet"
            if commodity_file.exists():
                commodity_df = pd.read_parquet(commodity_file)
                commodity_features = self._create_commodity_features(commodity_df)
                self._save_gold_features(commodity_features, 'commodities/commodity_features.parquet')
            
            return True
            
        except Exception as e:
            logger.error(f"Error building commodities features: {e}")
            return False
    
    def _build_market_features(self):
        """Build market ML features"""
        try:
            market_file = self.silver_root / "market/indices.parquet"
            if market_file.exists():
                market_df = pd.read_parquet(market_file)
                market_features = self._create_market_features(market_df)
                self._save_gold_features(market_features, 'market/market_features.parquet')
            
            return True
            
        except Exception as e:
            logger.error(f"Error building market features: {e}")
            return False
    
    def _build_energy_features(self):
        """Build energy ML features"""
        try:
            energy_file = self.silver_root / "energy/prices.parquet"
            if energy_file.exists():
                energy_df = pd.read_parquet(energy_file)
                energy_features = self._create_energy_features(energy_df)
                self._save_gold_features(energy_features, 'energy/energy_features.parquet')
            
            return True
            
        except Exception as e:
            logger.error(f"Error building energy features: {e}")
            return False
    
    def _build_cross_features(self):
        """Build cross-category ML features"""
        try:
            # Correlation features
            self._build_correlation_features()
            
            # Composite features
            self._build_composite_features()
            
            # Lagged cross-features
            self._build_cross_lagged_features()
            
            return True
            
        except Exception as e:
            logger.error(f"Error building cross-features: {e}")
            return False
    
    def _build_master_features(self):
        """Build master feature table for ML"""
        try:
            # Load all gold features
            master_df = pd.DataFrame()

            for feature_file in self.gold_root.rglob("*.parquet"):
                # Skip master outputs and activation reports
                if "master" in feature_file.parts or feature_file.name.lower().endswith("_report.parquet"):
                    continue
                try:
                    df = pd.read_parquet(feature_file)
                    if len(df) > 0:
                        category = feature_file.parent.name
                        df['category'] = category
                        master_df = pd.concat([master_df, df], ignore_index=True)
                except Exception as e:
                    logger.warning(f"Error loading {feature_file}: {e}")
            
            if len(master_df) > 0:
                # Sort and ensure date column
                if 'date' in master_df.columns:
                    master_df = master_df.sort_values('date')
                    master_df['date'] = pd.to_datetime(master_df['date'])
                
                # Add feature metadata
                master_df['feature_type'] = 'numeric'
                master_df['data_source'] = 'gold_layer'
                master_df['created_timestamp'] = datetime.now()
                
                self._save_gold_features(master_df, 'master/master_features.parquet')
                logger.info(f"Master features: {len(master_df)} records")
            
            return True
            
        except Exception as e:
            logger.error(f"Error building master features: {e}")
            return False
    
    # Feature engineering methods
    def _create_rate_features(self, df, feature_name):
        """Create rate-based features"""
        if len(df) == 0:
            return pd.DataFrame()

        df = df.copy()

        if 'date' not in df.columns:
            # Attempt to infer date-like columns
            date_candidates = [col for col in df.columns if 'date' in col.lower() or 'period' in col.lower()]
            if date_candidates:
                df['date'] = pd.to_datetime(df[date_candidates[0]], errors='coerce')
            else:
                return pd.DataFrame()
        else:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        df = df.dropna(subset=['date']).sort_values('date')

        # Identify primary numeric column
        exclude_cols = {'date', 'run_date', 'currency', 'tipoBoletim', 'source_table'}
        numeric_cols = [
            col for col in df.columns
            if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])
        ]
        if not numeric_cols:
            return pd.DataFrame()

        value_col = numeric_cols[0]
        feature_df = df[['date', value_col]].rename(columns={value_col: f'{feature_name}_current'})

        feature_df[f'{feature_name}_ma7'] = feature_df[f'{feature_name}_current'].rolling(7, min_periods=1).mean()
        feature_df[f'{feature_name}_ma30'] = feature_df[f'{feature_name}_current'].rolling(30, min_periods=1).mean()
        feature_df[f'{feature_name}_volatility_30'] = feature_df[f'{feature_name}_current'].rolling(30, min_periods=5).std()
        feature_df[f'{feature_name}_pct_change_7'] = feature_df[f'{feature_name}_current'].pct_change(7)
        feature_df[f'{feature_name}_pct_change_30'] = feature_df[f'{feature_name}_current'].pct_change(30)

        return feature_df.dropna(subset=[f'{feature_name}_current'])
    
    def _create_inflation_features(self, df):
        """Create inflation features"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date')
        
        if 'ipca_index' in df.columns:
            df['inflation_mom'] = df['ipca_index'].pct_change()
            df['inflation_mom_ma12'] = df['inflation_mom'].rolling(12).mean()
            df['inflation_trend'] = df['inflation_mom'].rolling(90).mean()
        elif 'ipca' in df.columns:
            df = df.rename(columns={'ipca': 'ipca_index'})
            df['inflation_mom'] = df['ipca_index'].pct_change()
            df['inflation_mom_ma12'] = df['inflation_mom'].rolling(12, min_periods=1).mean()
            df['inflation_trend'] = df['inflation_mom'].rolling(12 * 3, min_periods=3).mean()

        return df
    
    def _create_climate_features(self, df):
        """Create climate features"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date')
        
        # Temperature features
        temp_col = 'temp_c' if 'temp_c' in df.columns else 'temperature_c'
        if temp_col in df.columns:
            df[f'{temp_col}_lag7'] = df[temp_col].shift(7)
            df[f'{temp_col}_ma7'] = df[temp_col].rolling(7).mean()
            df[f'{temp_col}_ma30'] = df[temp_col].rolling(30).mean()
        
        # Precipitation features
        precip_col = 'precip_mm' if 'precip_mm' in df.columns else 'precipitation_mm'
        if precip_col in df.columns:
            df[f'{precip_col}_rolling7'] = df[precip_col].rolling(7).sum()
            df[f'{precip_col}_rolling30'] = df[precip_col].rolling(30).sum()
        
        return df
    
    def _create_global_features(self, df):
        """Create global economic features"""
        if len(df) == 0:
            return pd.DataFrame()
        
        # GDP growth rate
        if 'year' in df.columns:
            df = df.sort_values('year')
            df['gdp_growth_rate'] = df['value'].pct_change()
        
        return df
    
    def _create_fuel_features(self, df):
        """Create fuel price features"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date')
        
        if 'price' in df.columns:
            df['fuel_price_change'] = df['price'].pct_change()
            df['fuel_price_ma7'] = df['price'].rolling(7).mean()
            df['fuel_price_ma30'] = df['price'].rolling(30).mean()
        
        return df
    
    def _create_shipping_features(self, df):
        """Create shipping index features"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date')
        
        if 'baltic_index' in df.columns:
            df['shipping_index_change'] = df['baltic_index'].pct_change()
            df['shipping_index_ma30'] = df['baltic_index'].rolling(30).mean()
        
        return df
    
    def _create_commodity_features(self, df):
        """Create commodity price features"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date')
        
        if 'price' in df.columns:
            df['commodity_price_change'] = df['price'].pct_change()
            df['commodity_price_ma7'] = df['price'].rolling(7).mean()
            df['commodity_price_ma30'] = df['price'].rolling(30).mean()
            
            # Commodity-specific features
            if 'commodity' in df.columns:
                # Separate features per commodity
                for commodity in df['commodity'].unique():
                    mask = df['commodity'] == commodity
                    commodity_col = f'{commodity.lower()}_price'
                    df.loc[mask, f'{commodity_col}_ma7'] = (
                        df.loc[mask, 'price'].rolling(7).mean()
                    )
                    df.loc[mask, f'{commodity_col}_ma30'] = (
                        df.loc[mask, 'price'].rolling(30).mean()
                    )
        
        return df
    
    def _create_market_features(self, df):
        """Create market index features"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date')
        
        if 'close' in df.columns:
            df['market_index_change'] = df['close'].pct_change()
            df['market_index_ma7'] = df['close'].rolling(7).mean()
            df['market_index_ma30'] = df['close'].rolling(30).mean()
            
            # Market volatility (VIX if available)
            if 'symbol' in df.columns:
                for symbol in df['symbol'].unique():
                    if symbol.upper() == 'VIX':
                        mask = df['symbol'] == symbol
                        df.loc[mask, 'volatility_ma30'] = (
                            df.loc[mask, 'close'].rolling(30).std()
                        )
        
        return df
    
    def _create_energy_features(self, df):
        """Create energy price features"""
        if len(df) == 0 or 'date' not in df.columns:
            return pd.DataFrame()
        
        df = df.sort_values('date')
        
        if 'price' in df.columns:
            df['energy_price_change'] = df['price'].pct_change()
            df['energy_price_ma7'] = df['price'].rolling(7).mean()
            df['energy_price_ma30'] = df['price'].rolling(30).mean()
        
        return df
    
    def _build_correlation_features(self):
        """Build correlation features"""
        try:
            # Load specific datasets for correlation
            rates_file = self.silver_root / "macro/selic_rates.parquet"
            commodities_file = self.silver_root / "commodities/prices.parquet"
            
            if rates_file.exists() and commodities_file.exists():
                selic_df = pd.read_parquet(rates_file)
                commodity_df = pd.read_parquet(commodities_file)
                
                if len(selic_df) > 0 and len(commodity_df) > 0:
                    # Align by date
                    merged = pd.merge(
                        selic_df[['date', 'selic_rate']],
                        commodity_df[['date', 'price']],
                        on='date',
                        how='inner'
                    )
                    
                    # Rolling correlations
                    merged['selic_commodity_correlation'] = (
                        merged['selic_rate'].rolling(30).corr(merged['price'])
                    )
                    
                    self._save_gold_features(merged, 'cross_features/selic_commodity_correlation.parquet')
                    logger.info("✅ Correlation features built")
            
            return True
            
        except Exception as e:
            logger.error(f"Error building correlation features: {e}")
            return False
    
    def _build_composite_features(self):
        """Build composite features"""
        try:
            # Load economic and commodity data
            selic_file = self.silver_root / "macro/selic_rates.parquet"
            commodity_file = self.silver_root / "commodities/prices.parquet"
            
            if selic_file.exists() and commodity_file.exists():
                selic_df = pd.read_parquet(selic_file)
                commodity_df = pd.read_parquet(commodity_file)
                
                if len(selic_df) > 0 and len(commodity_df) > 0:
                    merged = pd.merge(
                        selic_df[['date', 'selic_rate']],
                        commodity_df[['date', 'commodity', 'price']],
                        on='date',
                        how='inner'
                    )
                    
                    # Real commodity cost adjusted by inflation
                    merged['real_price_index'] = merged['price'] / (1 + merged['selic_rate'] / 100)
                    
                    # Inflation-adjusted returns
                    merged['real_price_return'] = merged.groupby('commodity')['real_price_index'].pct_change()
                    
                    self._save_gold_features(merged, 'cross_features/inflation_adjusted_returns.parquet')
                    logger.info("✅ Composite features built")
            
            return True
            
        except Exception as e:
            logger.error(f"Error building composite features: {e}")
            return False
    
    def _build_cross_lagged_features(self):
        """Build cross-category lagged features"""
        try:
            # Load economic and market data
            selic_file = self.silver_root / "macro/selic_rates.parquet"
            market_file = self.silver_root / "market/indices.parquet"
            
            if selic_file.exists() and market_file.exists():
                selic_df = pd.read_parquet(selic_file)
                market_df = pd.read_parquet(market_file)
                
                if len(selic_df) > 0 and len(market_df) > 0:
                    merged = pd.merge(
                        selic_df[['date', 'selic_rate']],
                        market_df[['date', 'close']],
                        on='date',
                        how='inner'
                    )
                    
                    # Cross-correlation with lag
                    merged['market_selic_lag7'] = merged['selic_rate'].shift(7)
                    merged['market_selic_correlation'] = (
                        merged['close'].rolling(30).corr(merged['market_selic_lag7'].fillna(method='ffill'))
                    )
                    
                    self._save_gold_features(merged, 'cross_features/market_selic_lag_correlation.parquet')
                    logger.info("✅ Cross-lagged features built")
            
            return True
            
        except Exception as e:
            logger.error(f"Error building cross-lagged features: {e}")
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
            logger.error(f"Error saving gold features {path}: {e}")
    
    def _create_final_report(self, features_built, success):
        """Create final comprehensive report"""
        try:
            report = {
                'gold_layer_build_timestamp': datetime.now().isoformat(),
                'overall_success': success,
                'features_built': features_built,
                'features_count': len(features_built),
                'gold_root': str(self.gold_root),
                'silver_root': str(self.silver_root),
                'categories': {
                    'economic': 'economic' in features_built,
                    'climatic': 'climatic' in features_built,
                    'global': 'global' in features_built,
                    'logistics': 'logistics' in features_built,
                    'commodities': 'commodities' in features_built,
                    'market': 'market' in features_built,
                    'energy': 'energy' in features_built,
                    'cross_features': 'cross_features' in features_built,
                    'master': 'master' in features_built
                },
                'total_parquet_files': len(list(self.gold_root.rglob("*.parquet"))),
                'ml_readiness': {
                    'time_series_features': success,
                    'lagged_features': success,
                    'rolling_features': success,
                    'correlation_features': success,
                    'composite_features': success,
                    'master_dataset': success
                },
                'next_steps': [
                    'ML models can now use gold layer features',
                    'Start model training with feature engineered data',
                    'Set up model monitoring and retraining pipeline',
                    'Integrate with Nova Corrente demand forecasting'
                ]
            }
            
            # Save report
            report_file = Path("GOLD_LAYER_REPORT.json")
            with open(report_file, 'w', encoding='utf-8', errors='replace') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Gold layer report saved: {report_file}")
            
            return report
            
        except Exception as e:
            logger.error(f"Error creating final report: {e}")
            return None

def main():
    """Main execution function"""
    logger.info("Starting gold layer build")
    
    builder = GoldLayerBuilder()
    success = builder.build_all_gold_features()
    
    if success:
        logger.info("✅ Gold layer build completed successfully!")
    else:
        logger.error("❌ Gold layer build failed!")
    
    return success

if __name__ == "__main__":
    main()