#!/usr/bin/env python3
"""
Build Silver Layer from External Factors
Transforms raw external data into clean, normalized parquet tables for ML
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('silver_transform.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SilverLayerBuilder:
    def __init__(self, landing_root: str = "data/landing/external_factors-raw", 
                 silver_root: str = "data/silver/external_factors"):
        self.landing_root = Path(landing_root)
        self.silver_root = Path(silver_root)
        self.silver_root.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.silver_root / "macro").mkdir(exist_ok=True)
        (self.silver_root / "climatic").mkdir(exist_ok=True)
        (self.silver_root / "global").mkdir(exist_ok=True)
        (self.silver_root / "logistics").mkdir(exist_ok=True)
        (self.silver_root / "commodities").mkdir(exist_ok=True)
        (self.silver_root / "market").mkdir(exist_ok=True)
        (self.silver_root / "energy").mkdir(exist_ok=True)
    
    def build_all_silver_layers(self) -> bool:
        """Build all silver layer tables"""
        logger.info("Starting silver layer transformation")
        
        success = True
        
        try:
            # Step 1: Transform economic indicators
            success &= self.transform_economic_indicators()
            
            # Step 2: Transform climatic data
            success &= self.transform_climatic_data()
            
            # Step 3: Transform global indicators
            success &= self.transform_global_indicators()
            
            # Step 4: Transform logistics data
            success &= self.transform_logistics_data()
            
            # Step 5: Transform commodities data
            success &= self.transform_commodities_data()
            
            # Step 6: Transform market indices
            success &= self.transform_market_indices()
            
            # Step 7: Transform energy data
            success &= self.transform_energy_data()
            
            # Step 8: Create master metadata
            success &= self.create_master_metadata()
            
        except Exception as e:
            logger.error(f"Error in silver layer transformation: {e}")
            success = False
        
        logger.info(f"Silver layer transformation completed. Success: {success}")
        return success
    
    def transform_economic_indicators(self) -> bool:
        """Transform Brazilian economic indicators to silver layer"""
        logger.info("Transforming economic indicators...")
        
        try:
            # PTAX Exchange Rates
            ptax_data = self.load_json_sources("macro/bacen/ptax")
            if ptax_data:
                ptax_df = self.transform_ptax_data(ptax_data)
                self.write_parquet(ptax_df, "macro/ptax_rates.parquet")
                logger.info(f"✅ PTAX: {len(ptax_df)} records")
            
            # SELIC Interest Rates
            selic_data = self.load_json_sources("macro/bacen/selic")
            if selic_data:
                selic_df = self.transform_selic_data(selic_data)
                self.write_parquet(selic_df, "macro/selic_rates.parquet")
                logger.info(f"✅ SELIC: {len(selic_df)} records")
            
            # IPCA Inflation
            ipca_data = self.load_json_sources("macro/ibge/ipca")
            if ipca_data:
                ipca_df = self.transform_ipca_data(ipca_data)
                self.write_parquet(ipca_df, "macro/ipca_inflation.parquet")
                logger.info(f"✅ IPCA: {len(ipca_df)} records")
            
            logger.info("Economic indicators transformation completed")
            return True
            
        except Exception as e:
            logger.error(f"Error transforming economic indicators: {e}")
            return False
    
    def load_json_sources(self, pattern: str) -> List[Dict]:
        """Load JSON data from pattern"""
        data = []
        json_files = list(self.landing_root.glob(f"{pattern}/**/*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    if isinstance(file_data, dict):
                        data.append(file_data)
                    elif isinstance(file_data, list):
                        data.extend(file_data)
            except Exception as e:
                logger.warning(f"Error loading {json_file}: {e}")
        
        return data
    
    def transform_ptax_data(self, data: List[Dict]) -> pd.DataFrame:
        """Transform PTAX data to normalized format"""
        records = []
        
        for item in data:
            if isinstance(item, dict):
                date_str = item.get('data', '')
                if date_str:
                    date = pd.to_datetime(date_str, format='%d/%m/%Y')
                    for currency, rates in item.items():
                        if currency not in ['data', 'id'] and isinstance(rates, dict):
                            for period, rate_info in rates.items():
                                if isinstance(rate_info, dict) and 'buy' in rate_info:
                                    record = {
                                        'date': date,
                                        'currency': currency.upper(),
                                        'period': period,
                                        'buy_rate': float(rate_info['buy']),
                                        'sell_rate': float(rate_info['sell']),
                                        'buy_date': pd.to_datetime(rate_info.get('buy_date'), format='%d/%m/%Y'),
                                        'sell_date': pd.to_datetime(rate_info.get('sell_date'), format='%d/%m/%Y'),
                                        'source': 'bacen'
                                    }
                                    records.append(record)
        
        return pd.DataFrame(records)
    
    def transform_selic_data(self, data: List[Dict]) -> pd.DataFrame:
        """Transform SELIC data to normalized format"""
        records = []
        
        for item in data:
            if isinstance(item, dict):
                date_str = item.get('data', '')
                value = item.get('valor', 0)
                
                if date_str and value:
                    date = pd.to_datetime(date_str, format='%d/%m/%Y')
                    record = {
                        'date': date,
                        'selic_rate': float(value),
                        'source': 'bacen'
                    }
                    records.append(record)
        
        df = pd.DataFrame(records)
        
        # Add daily interpolation if needed
        if len(df) > 1:
            df = df.sort_values('date').set_index('date')
            daily_df = df.resample('D').interpolate().reset_index()
            return daily_df
        
        return df
    
    def transform_ipca_data(self, data: List[Dict]) -> pd.DataFrame:
        """Transform IPCA data to normalized format"""
        records = []
        
        for item in data:
            if isinstance(item, dict):
                date_str = item.get('data', '')
                if 'valor' in item and date_str:
                    date = pd.to_datetime(date_str, format='%d/%m/%Y')
                    record = {
                        'date': date,
                        'ipca_index': float(item['valor']),
                        'variation': float(item.get('variacao', 0)),
                        'source': 'ibge'
                    }
                    records.append(record)
        
        return pd.DataFrame(records)
    
    def transform_climatic_data(self) -> bool:
        """Transform climatic data to silver layer"""
        logger.info("Transforming climatic data...")
        
        try:
            # INMET historical data
            inmet_files = list(self.landing_root.glob("inmet/**/INMET_*.CSV"))
            if inmet_files:
                inmet_df = self.process_inmet_files(inmet_files)
                self.write_parquet(inmet_df, "climatic/inmet_historical.parquet")
                logger.info(f"✅ INMET: {len(inmet_df)} records from {len(inmet_files)} stations")
            
            # OpenWeather data
            weather_files = list(self.landing_root.glob("openweather/**/*.csv"))
            if weather_files:
                weather_df = self.process_openweather_files(weather_files)
                self.write_parquet(weather_df, "climatic/openweather_current.parquet")
                logger.info(f"✅ OpenWeather: {len(weather_df)} records")
            
            logger.info("Climatic data transformation completed")
            return True
            
        except Exception as e:
            logger.error(f"Error transforming climatic data: {e}")
            return False
    
    def process_inmet_files(self, file_paths: List[Path]) -> pd.DataFrame:
        """Process INMET CSV files"""
        records = []
        
        for file_path in file_paths[:10]:  # Limit to first 10 files for performance
            try:
                df = pd.read_csv(file_path, encoding='latin1', sep=';')
                
                if len(df) > 0:
                    # Extract station info from filename
                    filename = file_path.stem
                    parts = filename.split('_')
                    if len(parts) >= 2:
                        state = parts[0].replace('INMET_', '')
                        station_code = parts[1].split('(')[0]
                        station_name = station_code.replace('_', ' ').title()
                    else:
                        continue
                    
                    # Process data
                    for _, row in df.iterrows():
                        try:
                            date_str = row.get('Data', '')
                            if date_str:
                                date = pd.to_datetime(date_str, format='%Y-%m-%d')
                                record = {
                                    'date': date,
                                    'state_code': state,
                                    'station_code': station_code,
                                    'station_name': station_name,
                                    'temperature_c': self.safe_float(row.get('TEMPERATURA DO AR (°C)', 0)),
                                    'temperature_max_c': self.safe_float(row.get('TEMPERATURA MÁX. NA HORA (°C)', 0)),
                                    'temperature_min_c': self.safe_float(row.get('TEMPERATURA MÍN. NA HORA (°C)', 0)),
                                    'humidity_percent': self.safe_float(row.get('UMIDADE RELATIVA DO AR (%)', 0)),
                                    'precipitation_mm': self.safe_float(row.get('PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', 0)),
                                    'wind_speed_kmh': self.safe_float(row.get('VELOCIDADE DO VENTO (m/s)', 0)),
                                    'source': 'inmet'
                                }
                                records.append(record)
                        except:
                            continue
            except Exception as e:
                logger.warning(f"Error processing INMET file {file_path}: {e}")
        
        return pd.DataFrame(records)
    
    def process_openweather_files(self, file_paths: List[Path]) -> pd.DataFrame:
        """Process OpenWeather CSV files"""
        records = []
        
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                
                if len(df) > 0:
                    for _, row in df.iterrows():
                        record = {
                            'date': pd.to_datetime(row['date']),
                            'state_code': row['state_code'],
                            'temperature_mean_c': row['temperature_c'],
                            'precipitation_mm': row['precipitation_mm'],
                            'humidity_percent': row['humidity_percent'],
                            'source': 'openweather'
                        }
                        records.append(record)
            except Exception as e:
                logger.warning(f"Error processing OpenWeather file {file_path}: {e}")
        
        return pd.DataFrame(records)
    
    def transform_global_indicators(self) -> bool:
        """Transform global economic indicators to silver layer"""
        logger.info("Transforming global indicators...")
        
        try:
            gdp_data = self.load_json_sources("global/worldbank")
            if gdp_data:
                gdp_df = self.transform_worldbank_data(gdp_data)
                self.write_parquet(gdp_df, "global/worldbank_indicators.parquet")
                logger.info(f"✅ World Bank GDP: {len(gdp_df)} records")
            
            logger.info("Global indicators transformation completed")
            return True
            
        except Exception as e:
            logger.error(f"Error transforming global indicators: {e}")
            return False
    
    def transform_worldbank_data(self, data: List[Dict]) -> pd.DataFrame:
        """Transform World Bank data"""
        records = []
        
        for item in data:
            if isinstance(item, dict):
                for indicator, values in item.items():
                    if isinstance(values, dict) and len(values) > 0:
                        latest_year = max(values.keys())
                        latest_value = values[str(latest_year)]
                        
                        record = {
                            'indicator': indicator,
                            'country': 'Brazil',
                            'year': latest_year,
                            'value': float(latest_value) if latest_value else 0,
                            'source': 'worldbank'
                        }
                        records.append(record)
        
        return pd.DataFrame(records)
    
    def transform_logistics_data(self) -> bool:
        """Transform logistics data to silver layer"""
        logger.info("Transforming logistics data...")
        
        try:
            # ANP Fuel Prices
            anp_files = list(self.landing_root.glob("logistics/anp_fuel/**/*.csv"))
            if anp_files:
                anp_df = self.process_anp_files(anp_files)
                self.write_parquet(anp_df, "logistics/anp_fuel_prices.parquet")
                logger.info(f"✅ ANP Fuel: {len(anp_df)} records")
            
            # Baltic Dry Index
            baltic_files = list(self.landing_root.glob("logistics/baltic_dry/**/*.csv"))
            if baltic_files:
                baltic_df = self.process_baltic_files(baltic_files)
                self.write_parquet(baltic_df, "logistics/baltic_dry_index.parquet")
                logger.info(f"✅ Baltic Dry: {len(baltic_df)} records")
            
            logger.info("Logistics data transformation completed")
            return True
            
        except Exception as e:
            logger.error(f"Error transforming logistics data: {e}")
            return False
    
    def process_anp_files(self, file_paths: List[Path]) -> pd.DataFrame:
        """Process ANP fuel price files"""
        records = []
        
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'fuel_type': row.get('product', ''),
                        'price_brl_per_liter': self.safe_float(row.get('mean_value', 0)),
                        'region': row.get('region', ''),
                        'source': 'anp'
                    }
                    records.append(record)
            except Exception as e:
                logger.warning(f"Error processing ANP file {file_path}: {e}")
        
        return pd.DataFrame(records)
    
    def process_baltic_files(self, file_paths: List[Path]) -> pd.DataFrame:
        """Process Baltic Dry Index files"""
        records = []
        
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                
                if 'Date' in df.columns and 'Price' in df.columns:
                    for _, row in df.iterrows():
                        record = {
                            'date': pd.to_datetime(row['Date']),
                            'baltic_index': self.safe_float(row['Price']),
                            'source': 'baltic'
                        }
                        records.append(record)
            except Exception as e:
                logger.warning(f"Error processing Baltic file {file_path}: {e}")
        
        return pd.DataFrame(records)
    
    def transform_commodities_data(self) -> bool:
        """Transform commodities data to silver layer"""
        logger.info("Transforming commodities data...")
        
        try:
            commodity_files = list(self.landing_root.glob("commodities/**/*.csv"))
            if commodity_files:
                commodities_df = self.process_commodity_files(commodity_files)
                self.write_parquet(commodities_df, "commodities/prices.parquet")
                logger.info(f"✅ Commodities: {len(commodities_df)} records")
            
            logger.info("Commodities data transformation completed")
            return True
            
        except Exception as e:
            logger.error(f"Error transforming commodities data: {e}")
            return False
    
    def process_commodity_files(self, file_paths: List[Path]) -> pd.DataFrame:
        """Process commodity price files"""
        records = []
        
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                commodity_type = file_path.stem.split('_')[0] if '_' in file_path.stem else file_path.stem
                
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'commodity': commodity_type.upper(),
                        'price_usd': self.safe_float(row.get('close', 0)),
                        'source': 'commodities'
                    }
                    records.append(record)
            except Exception as e:
                logger.warning(f"Error processing commodity file {file_path}: {e}")
        
        return pd.DataFrame(records)
    
    def transform_market_indices_data(self) -> bool:
        """Transform market indices data to silver layer"""
        logger.info("Transforming market indices data...")
        
        try:
            market_files = list(self.landing_root.glob("market_indices/**/*.csv"))
            if market_files:
                market_df = self.process_market_files(market_files)
                self.write_parquet(market_df, "market/indices.parquet")
                logger.info(f"✅ Market Indices: {len(market_df)} records")
            else:
                logger.warning("No market index files found")
            
            logger.info("Market indices transformation completed")
            return True
            
        except Exception as e:
            logger.error(f"Error transforming market indices data: {e}")
            return False
    
    def process_market_files(self, file_paths: List[Path]) -> pd.DataFrame:
        """Process market index files"""
        records = []
        
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                index_type = file_path.stem.split('_')[0] if '_' in file_path.stem else file_path.stem
                
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'symbol': row.get('symbol', index_type),
                        'close': self.safe_float(row.get('close', 0)),
                        'source': 'market_indices'
                    }
                    records.append(record)
            except Exception as e:
                logger.warning(f"Error processing market file {file_path}: {e}")
        
        return pd.DataFrame(records)
    
    def transform_energy_data(self) -> bool:
        """Transform energy data to silver layer"""
        logger.info("Transforming energy data...")
        
        try:
            energy_files = list(self.landing_root.glob("energy/**/*.csv"))
            if energy_files:
                energy_df = self.process_energy_files(energy_files)
                self.write_parquet(energy_df, "energy/energy_prices.parquet")
                logger.info(f"✅ Energy: {len(energy_df)} records")
            
            logger.info("Energy data transformation completed")
            return True
            
        except Exception as e:
            logger.error(f"Error transforming energy data: {e}")
            return False
    
    def process_energy_files(self, file_paths: List[Path]) -> pd.DataFrame:
        """Process energy price files"""
        records = []
        
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                energy_type = file_path.stem.split('_')[0] if '_' in file_path.stem else file_path.stem
                
                for _, row in df.iterrows():
                    record = {
                        'date': pd.to_datetime(row['date']),
                        'energy_type': energy_type.lower(),
                        'price_usd': self.safe_float(row.get('price', 0)),
                        'price_brl_per_unit': self.safe_float(row.get('price', 0)),
                        'source': 'energy'
                    }
                    records.append(record)
            except Exception as e:
                logger.warning(f"Error processing energy file {file_path}: {e}")
        
        return pd.DataFrame(records)
    
    def create_master_metadata(self) -> bool:
        """Create master metadata file for silver layer"""
        logger.info("Creating master metadata...")
        
        try:
            metadata = {
                'transformation_timestamp': datetime.now().isoformat(),
                'landing_root': str(self.landing_root),
                'silver_root': str(self.silver_root),
                'tables_created': [],
                'record_counts': {},
                'data_quality': {},
                'schema_version': '1.0'
            }
            
            # Count records in all parquet files
            for parquet_file in self.silver_root.rglob("*.parquet"):
                try:
                    df = pd.read_parquet(parquet_file)
                    table_name = parquet_file.relative_to(self.silver_root).as_posix()
                    metadata['tables_created'].append(table_name)
                    metadata['record_counts'][table_name] = len(df)
                    
                    # Basic quality checks
                    null_rate = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                    metadata['data_quality'][table_name] = {
                        'null_percentage': null_rate,
                        'columns': list(df.columns),
                        'date_range': f"{df['date'].min()} to {df['date'].max()}" if 'date' in df.columns else "N/A"
                    }
                except Exception as e:
                    logger.warning(f"Error processing {parquet_file}: {e}")
            
            # Save metadata
            metadata_file = self.silver_root / "metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"✅ Metadata created: {len(metadata['tables_created'])} tables, {sum(metadata['record_counts'].values())} total records")
            return True
            
        except Exception as e:
            logger.error(f"Error creating master metadata: {e}")
            return False
    
    def write_parquet(self, df: pd.DataFrame, path: str) -> None:
        """Write DataFrame to parquet file"""
        try:
            full_path = self.silver_root / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Ensure date column is datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            df.to_parquet(full_path, index=False)
            
        except Exception as e:
            logger.error(f"Error writing parquet {path}: {e}")
    
    def safe_float(self, value) -> float:
        """Safely convert to float"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return 0.0
            return float(str(value).replace(',', '').replace('nan', '').replace('null', ''))
        except:
            return 0.0

def main():
    """Main execution function"""
    logger.info("Starting silver layer transformation")
    
    builder = SilverLayerBuilder()
    success = builder.build_all_silver_layers()
    
    if success:
        logger.info("✅ Silver layer transformation completed successfully")
    else:
        logger.error("❌ Silver layer transformation failed")
    
    return success

if __name__ == "__main__":
    main()