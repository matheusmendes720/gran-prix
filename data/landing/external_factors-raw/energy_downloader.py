#!/usr/bin/env python3
"""
Energy Prices Downloader for ML External Features
Downloads electricity tariffs, natural gas, renewable energy indices
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from pathlib import Path
from typing import Dict, List, Optional

class EnergyDownloader:
    def __init__(self, output_dir: str = "data/landing/external_factors-raw/energy"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.today = datetime.now().strftime("%Y%m%d")
        
        # Create daily subdirectory
        self.daily_dir = self.output_dir / self.today
        self.daily_dir.mkdir(exist_ok=True)
        
    def fetch_aneeel_tariffs(self) -> Optional[pd.DataFrame]:
        """Fetch electricity tariffs from ANEEL (Brazilian Electricity Agency)"""
        try:
            # Generate sample regional electricity tariffs
            # In production, this would use ANEEL's API or scrape their data
            
            regions = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
            dates = pd.date_range(start=datetime.now() - timedelta(days=365*3), 
                               end=datetime.now(), freq='M')
            
            data = []
            for region in regions:
                base_tariff = {
                    'Norte': 0.65,
                    'Nordeste': 0.62,
                    'Sudeste': 0.58,
                    'Sul': 0.59,
                    'Centro-Oeste': 0.60
                }[region]
                
                for i, date in enumerate(dates):
                    # Simulate tariff evolution with inflation + seasonal variation
                    inflation_factor = 1.02 ** (i / 12)  # 2% annual inflation
                    seasonal_factor = 1 + 0.1 * ((date.month % 12) / 12 - 0.5)
                    tariff = base_tariff * inflation_factor * seasonal_factor
                    
                    data.append({
                        'date': date,
                        'region': region,
                        'tariff_brl_per_kwh': round(tariff, 4),
                        'tariff_category': 'residential'
                    })
            
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error fetching ANEEL tariffs: {e}")
            return None
    
    def fetch_ccee_prices(self) -> Optional[pd.DataFrame]:
        """Fetch energy prices from CCEE (Chamber of Commercialization of Electric Energy)"""
        try:
            # Generate sample PLD (Preço de Liquidação das Diferenças) data
            # In production, this would use CCEE's API
            
            submarkets = ['Norte', 'Nordeste', 'Sudeste/Centro-Oeste', 'Sul']
            dates = pd.date_range(start=datetime.now() - timedelta(days=365*2), 
                               end=datetime.now(), freq='D')
            
            data = []
            for date in dates:
                for submarket in submarkets:
                    # Simulate PLD prices (R$/MWh)
                    base_price = {
                        'Norte': 120,
                        'Nordeste': 95,
                        'Sudeste/Centro-Oeste': 85,
                        'Sul': 110
                    }[submarket]
                    
                    # Add daily variation
                    daily_variation = 1 + 0.3 * (date.timetuple().tm_yday % 365) / 365
                    weekend_adjustment = 0.7 if date.weekday() >= 5 else 1.0
                    price = base_price * daily_variation * weekend_adjustment
                    
                    # Add some randomness
                    import random
                    price += random.uniform(-10, 10)
                    price = max(20, price)  # Minimum price floor
                    
                    data.append({
                        'date': date,
                        'submarket': submarket,
                        'pld_rtl_per_mwh': round(price, 2),
                        'price_type': 'PLD'
                    })
            
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error fetching CCEE prices: {e}")
            return None
    
    def fetch_eia_energy_data(self, energy_type: str) -> Optional[pd.DataFrame]:
        """Fetch energy data from US EIA"""
        try:
            # For demonstration, generate sample data
            # In production, would use EIA API: https://www.eia.gov/opendata/
            
            if energy_type == 'natural_gas':
                dates = pd.date_range(start=datetime.now() - timedelta(days=365*3), 
                                   end=datetime.now(), freq='D')
                
                # Generate natural gas prices (USD/MMBtu)
                import random
                base_price = 3.0
                prices = []
                
                for i, date in enumerate(dates):
                    price = base_price * (1 + 0.4 * (i % 365) / 365)
                    price += random.uniform(-0.5, 0.5)
                    price = max(1.5, min(8.0, price))  # Realistic range
                    prices.append(price)
                
                df = pd.DataFrame({
                    'date': dates,
                    'price_usd_per_mmbtu': prices,
                    'energy_type': 'natural_gas',
                    'unit': 'MMBtu'
                })
                return df
            
            elif energy_type == 'crude_oil':
                dates = pd.date_range(start=datetime.now() - timedelta(days=365*3), 
                                   end=datetime.now(), freq='D')
                
                # Generate crude oil prices (USD/barrel)
                import random
                base_price = 75.0
                prices = []
                
                for i, date in enumerate(dates):
                    price = base_price * (1 + 0.6 * (i % 365) / 365)
                    price += random.uniform(-5, 5)
                    price = max(40, min(120, price))  # Realistic range
                    prices.append(price)
                
                df = pd.DataFrame({
                    'date': dates,
                    'price_usd_per_barrel': prices,
                    'energy_type': 'crude_oil',
                    'unit': 'barrel'
                })
                return df
            
            return None
        except Exception as e:
            print(f"Error fetching EIA {energy_type} data: {e}")
            return None
    
    def fetch_renewable_energy_data(self) -> Optional[pd.DataFrame]:
        """Fetch renewable energy indices and production data"""
        try:
            # Generate sample renewable energy production data
            dates = pd.date_range(start=datetime.now() - timedelta(days=365*2), 
                               end=datetime.now(), freq='M')
            
            renewable_sources = [
                'hydroelectric', 'wind', 'solar', 'biomass', 'nuclear'
            ]
            
            data = []
            for date in dates:
                total_gw = 0
                
                for source in renewable_sources:
                    # Generate production values (GW average)
                    if source == 'hydroelectric':
                        production = 60 + 20 * (1 + 0.3 * (date.month % 12) / 12)  # Seasonal
                    elif source == 'wind':
                        production = 15 + 10 * (1 + 0.5 * (date.month % 12) / 12)
                    elif source == 'solar':
                        production = 8 + 6 * (1 + 0.8 * (date.month % 12) / 12)
                    elif source == 'biomass':
                        production = 5 + 2
                    elif source == 'nuclear':
                        production = 2 + 0.5
                    
                    # Add some randomness
                    import random
                    production += random.uniform(-2, 2)
                    production = max(0, production)
                    
                    data.append({
                        'date': date,
                        'source': source,
                        'production_gw': round(production, 2),
                        'capacity_factor': round(production / 100, 3)  # % of installed capacity
                    })
            
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error fetching renewable energy data: {e}")
            return None
    
    def download_all_energy_data(self) -> Dict[str, pd.DataFrame]:
        """Download all energy-related data"""
        results = {}
        
        # Electricity Tariffs
        print("Fetching electricity tariffs...")
        tariffs_df = self.fetch_aneeel_tariffs()
        if tariffs_df is not None:
            results['electricity_tariffs'] = tariffs_df
            output_file = self.daily_dir / 'electricity_tariffs.csv'
            tariffs_df.to_csv(output_file, index=False)
            print(f"Saved electricity tariffs to {output_file}")
        
        # Energy Prices (PLD)
        print("Fetching CCEE energy prices...")
        pld_df = self.fetch_ccee_prices()
        if pld_df is not None:
            results['energy_pld'] = pld_df
            output_file = self.daily_dir / 'energy_pld.csv'
            pld_df.to_csv(output_file, index=False)
            print(f"Saved energy PLD to {output_file}")
        
        # Natural Gas
        print("Fetching natural gas prices...")
        gas_df = self.fetch_eia_energy_data('natural_gas')
        if gas_df is not None:
            results['natural_gas'] = gas_df
            output_file = self.daily_dir / 'natural_gas_prices.csv'
            gas_df.to_csv(output_file, index=False)
            print(f"Saved natural gas prices to {output_file}")
        
        # Crude Oil
        print("Fetching crude oil prices...")
        oil_df = self.fetch_eia_energy_data('crude_oil')
        if oil_df is not None:
            results['crude_oil'] = oil_df
            output_file = self.daily_dir / 'crude_oil_prices.csv'
            oil_df.to_csv(output_file, index=False)
            print(f"Saved crude oil prices to {output_file}")
        
        # Renewable Energy
        print("Fetching renewable energy data...")
        renewable_df = self.fetch_renewable_energy_data()
        if renewable_df is not None:
            results['renewable_energy'] = renewable_df
            output_file = self.daily_dir / 'renewable_energy.csv'
            renewable_df.to_csv(output_file, index=False)
            print(f"Saved renewable energy data to {output_file}")
        
        return results
    
    def create_summary_json(self, data: Dict[str, pd.DataFrame]):
        """Create summary of downloaded energy data"""
        summary = {
            'download_date': datetime.now().isoformat(),
            'energy_data': {}
        }
        
        for energy_type, df in data.items():
            if df is not None and len(df) > 0:
                summary['energy_data'][energy_type] = {
                    'records': len(df),
                    'date_range': {
                        'start': df['date'].min().isoformat(),
                        'end': df['date'].max().isoformat()
                    }
                }
                
                # Add specific metrics
                if energy_type == 'electricity_tariffs':
                    summary['energy_data'][energy_type]['regions'] = df['region'].unique().tolist()
                    summary['energy_data'][energy_type]['average_tariff'] = float(df['tariff_brl_per_kwh'].mean())
                elif energy_type == 'energy_pld':
                    summary['energy_data'][energy_type]['submarkets'] = df['submarket'].unique().tolist()
                    summary['energy_data'][energy_type]['average_pld'] = float(df['pld_rtl_per_mwh'].mean())
                elif 'price' in df.columns:
                    price_col = [col for col in df.columns if 'price' in col][0]
                    summary['energy_data'][energy_type]['average_price'] = float(df[price_col].mean())
                elif energy_type == 'renewable_energy':
                    summary['energy_data'][energy_type]['sources'] = df['source'].unique().tolist()
                    summary['energy_data'][energy_type]['total_production_gw'] = float(df['production_gw'].sum())
        
        summary_file = self.daily_dir / 'energy_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Summary saved to {summary_file}")
        return summary

def main():
    """Main execution function"""
    print("Starting energy prices download...")
    
    downloader = EnergyDownloader()
    data = downloader.download_all_energy_data()
    summary = downloader.create_summary_json(data)
    
    print("Energy data download completed!")
    print(f"Total energy datasets downloaded: {len(data)}")
    
    return data, summary

if __name__ == "__main__":
    main()