#!/usr/bin/env python3
"""
SILVER LAYER BUILDER - Fixed Version
Builds silver layer from external factors without Unicode issues
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

# Configure logging without Unicode issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('silver_build.log', encoding='utf-8', errors='replace'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SilverBuilder:
    def __init__(self, landing_root="data/landing/external_factors-raw", 
                 silver_root="data/silver/external_factors"):
        self.landing_root = Path(landing_root)
        self.silver_root = Path(silver_root)
        self.silver_root.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        for subdir in ['macro', 'climatic', 'global', 'logistics', 'commodities', 'market', 'energy']:
            (self.silver_root / subdir).mkdir(exist_ok=True)
    
    def build_all(self):
        """Build all silver layer tables"""
        logger.info("Building silver layer from external factors")
        logger.info("=" * 50)
        
        tables_built = 0
        
        try:
            # Economic indicators
            if self._build_economic():
                tables_built += 1
                logger.info("  Economic: Built")
            
            # Climate data
            if self._build_climatic():
                tables_built += 1
                logger.info("  Climate: Built")
            
            # Global indicators
            if self._build_global():
                tables_built += 1
                logger.info("  Global: Built")
            
            # Logistics data
            if self._build_logistics():
                tables_built += 1
                logger.info("  Logistics: Built")
            
            # Commodities
            if self._build_commodities():
                tables_built += 1
                logger.info("  Commodities: Built")
            
            # Market indices
            if self._build_market():
                tables_built += 1
                logger.info("  Market: Built")
            
            # Energy data
            if self._build_energy():
                tables_built += 1
                logger.info("  Energy: Built")
            
            logger.info(f"Silver layer build completed. Tables: {tables_built}/8")
            
        except Exception as e:
            logger.error(f"Error building silver layer: {e}")
            return False
        
        return True
    
    def _build_economic(self):
        """Build economic indicators"""
        try:
            # PTAX data
            ptax_files = list(self.landing_root.glob("macro/bacen/ptax/**/*.json"))
            if ptax_files:
                ptax_df = self._process_ptax(ptax_files)
                ptax_df.to_parquet(self.silver_root / "macro/ptax_rates.parquet", index=False)
                logger.info(f"    PTAX: {len(ptax_df)} records")
            
            # SELIC data
            selic_files = list(self.landing_root.glob("macro/bacen/selic/**/*.json"))
            if selic_files:
                selic_df = self._process_selic(selic_files)
                selic_df.to_parquet(self.silver_root / "macro/selic_rates.parquet", index=False)
                logger.info(f"    SELIC: {len(selic_df)} records")
            
            # IPCA data
            ipca_files = list(self.landing_root.glob("macro/ibge/ipca/**/*.json"))
            if ipca_files:
                ipca_df = self._process_ipca(ipca_files)
                ipca_df.to_parquet(self.silver_root / "macro/ipca_inflation.parquet", index=False)
                logger.info(f"    IPCA: {len(ipca_df)} records")
            
            return True
        except Exception as e:
            logger.error(f"Error building economic: {e}")
            return False
    
    def _build_climatic(self):
        """Build climatic data"""
        try:
            # INMET data
            inmet_files = list(self.landing_root.glob("inmet/**/INMET_*.CSV"))
            if inmet_files:
                inmet_df = self._process_inmet(inmet_files[:20])  # Limit for performance
                inmet_df.to_parquet(self.silver_root / "climatic/inmet_historical.parquet", index=False)
                logger.info(f"    INMET: {len(inmet_df)} records")
            
            # OpenWeather data
            weather_files = list(self.landing_root.glob("openweather/**/*.csv"))
            if weather_files:
                weather_df = self._process_weather(weather_files)
                weather_df.to_parquet(self.silver_root / "climatic/openweather_current.parquet", index=False)
                logger.info(f"    Weather: {len(weather_df)} records")
            
            return True
        except Exception as e:
            logger.error(f"Error building climatic: {e}")
            return False
    
    def _build_global(self):
        """Build global indicators"""
        try:
            # World Bank data
            wb_files = list(self.landing_root.glob("global/worldbank/**/*.json"))
            if wb_files:
                wb_df = self._process_worldbank(wb_files)
                wb_df.to_parquet(self.silver_root / "global/worldbank_gdp.parquet", index=False)
                logger.info(f"    World Bank: {len(wb_df)} records")
            
            return True
        except Exception as e:
            logger.error(f"Error building global: {e}")
            return False
    
    def _build_logistics(self):
        """Build logistics data"""
        try:
            # ANP fuel data
            anp_files = list(self.landing_root.glob("logistics/anp_fuel/**/*.csv"))
            if anp_files:
                anp_df = self._process_anp(anp_files)
                anp_df.to_parquet(self.silver_root / "logistics/anp_fuel_prices.parquet", index=False)
                logger.info(f"    ANP Fuel: {len(anp_df)} records")
            
            # Baltic Dry data
            baltic_files = list(self.landing_root.glob("logistics/baltic_dry/**/*.csv"))
            if baltic_files:
                baltic_df = self._process_baltic(baltic_files)
                baltic_df.to_parquet(self.silver_root / "logistics/baltic_dry_index.parquet", index=False)
                logger.info(f"    Baltic: {len(baltic_df)} records")
            
            return True
        except Exception as e:
            logger.error(f"Error building logistics: {e}")
            return False
    
    def _build_commodities(self):
        """Build commodities data"""
        try:
            commodity_files = list(self.landing_root.glob("commodities/**/*.csv"))
            if commodity_files:
                commodity_df = self._process_commodities(commodity_files)
                commodity_df.to_parquet(self.silver_root / "commodities/prices.parquet", index=False)
                logger.info(f"    Commodities: {len(commodity_df)} records")
            
            return True
        except Exception as e:
            logger.error(f"Error building commodities: {e}")
            return False
    
    def _build_market(self):
        """Build market indices data"""
        try:
            market_files = list(self.landing_root.glob("market_indices/**/*.csv"))
            if market_files:
                market_df = self._process_market(market_files)
                market_df.to_parquet(self.silver_root / "market/indices.parquet", index=False)
                logger.info(f"    Market: {len(market_df)} records")
            
            return True
        except Exception as e:
            logger.error(f"Error building market: {e}")
            return False
    
    def _build_energy(self):
        """Build energy data"""
        try:
            energy_files = list(self.landing_root.glob("energy/**/*.csv"))
            if energy_files:
                energy_df = self._process_energy(energy_files)
                energy_df.to_parquet(self.silver_root / "energy/prices.parquet", index=False)
                logger.info(f"    Energy: {len(energy_df)} records")
            
            return True
        except Exception as e:
            logger.error(f"Error building energy: {e}")
            return False
    
    # Processing methods
    def _process_ptax(self, files):
        records = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    date = pd.to_datetime(data.get('data', ''), format='%d/%m/%Y')
                    for currency, rates in data.items():
                        if isinstance(rates, dict):
                            for period, info in rates.items():
                                if isinstance(info, dict):
                                    record = {
                                        'date': date,
                                        'currency': currency,
                                        'period': period,
                                        'buy_rate': float(info.get('buy', 0)),
                                        'sell_rate': float(info.get('sell', 0))
                                    }
                                    records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_selic(self, files):
        records = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    date = pd.to_datetime(data.get('data', ''), format='%d/%m/%Y')
                    rate = float(data.get('valor', 0))
                    record = {
                        'date': date,
                        'selic_rate': rate
                    }
                    records.append(record)
            except:
                continue
        df = pd.DataFrame(records)
        if len(df) > 1:
            df = df.sort_values('date')
            df['daily_rate'] = df['selic_rate'].interpolate()
        return df
    
    def _process_ipca(self, files):
        records = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    date = pd.to_datetime(data.get('data', ''), format='%d/%m/%Y')
                    value = float(data.get('valor', 0))
                    record = {
                        'date': date,
                        'ipca_index': value
                    }
                    records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_inmet(self, files):
        records = []
        for file in files[:10]:  # Limit to first 10
            try:
                df = pd.read_csv(file, encoding='latin1', sep=';')
                if len(df) > 0:
                    filename = file.stem
                    state = filename.split('_')[0].replace('INMET_', '')
                    for _, row in df.iterrows():
                        date_str = row.get('Data', '')
                        if date_str:
                            date = pd.to_datetime(date_str, format='%Y-%m-%d')
                            record = {
                                'date': date,
                                'state': state,
                                'temp_c': self._safe_float(row.get('TEMPERATURA DO AR (C)', 0)),
                                'humidity': self._safe_float(row.get('UMIDADE RELATIVA DO AR (%)', 0)),
                                'precip_mm': self._safe_float(row.get('PRECIPITACAO TOTAL, HORARIO (mm)', 0))
                            }
                            records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_weather(self, files):
        records = []
        for file in files:
            try:
                df = pd.read_csv(file)
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'state': row.get('state_code'),
                        'temp_c': row.get('temperature_mean_c', 0),
                        'precip_mm': row.get('precipitation_mm', 0),
                        'humidity': row.get('humidity_percent', 0)
                    }
                    records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_worldbank(self, files):
        records = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        for indicator, values in data.items():
                            if isinstance(values, dict) and len(values) > 0:
                                latest_year = max(values.keys())
                                latest_value = float(values.get(str(latest_year), 0))
                                record = {
                                    'indicator': indicator,
                                    'country': 'Brazil',
                                    'year': latest_year,
                                    'value': latest_value
                                }
                                records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_anp(self, files):
        records = []
        for file in files:
            try:
                df = pd.read_csv(file, encoding='utf-8')
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'fuel': row.get('product'),
                        'price': self._safe_float(row.get('mean_value', 0)),
                        'region': row.get('region')
                    }
                    records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_baltic(self, files):
        records = []
        for file in files:
            try:
                df = pd.read_csv(file)
                if 'Date' in df.columns and 'Price' in df.columns:
                    for _, row in df.iterrows():
                        record = {
                            'date': pd.to_datetime(row['Date']),
                            'index': self._safe_float(row['Price'])
                        }
                        records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_commodities(self, files):
        records = []
        for file in files:
            try:
                df = pd.read_csv(file)
                commodity = file.stem.split('_')[0] if '_' in file.stem else file.stem
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'commodity': commodity.upper(),
                        'price': self._safe_float(row.get('close', 0))
                    }
                    records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_market(self, files):
        records = []
        for file in files:
            try:
                df = pd.read_csv(file)
                index_name = file.stem.split('_')[0] if '_' in file.stem else file.stem
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'symbol': row.get('symbol', index_name),
                        'price': self._safe_float(row.get('close', 0))
                    }
                    records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _process_energy(self, files):
        records = []
        for file in files:
            try:
                df = pd.read_csv(file)
                energy_type = file.stem.split('_')[0] if '_' in file.stem else file.stem
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'type': energy_type.lower(),
                        'price': self._safe_float(row.get('price', 0))
                    }
                    records.append(record)
            except:
                continue
        return pd.DataFrame(records)
    
    def _safe_float(self, value):
        """Safely convert to float"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return 0.0
            return float(str(value).replace(',', '').replace('nan', ''))
        except:
            return 0.0

def main():
    """Main execution function"""
    builder = SilverBuilder()
    success = builder.build_all()
    
    if success:
        logger.info("Silver layer build completed successfully!")
    else:
        logger.error("Silver layer build failed!")
    
    return success

if __name__ == "__main__":
    main()