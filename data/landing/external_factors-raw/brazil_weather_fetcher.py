#!/usr/bin/env python3
"""
Expanded OpenWeather Data Fetcher for All Brazilian States
Downloads historical weather data for all 27 Brazilian states for ML processing
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from pathlib import Path
from typing import Dict, List, Optional

class BrazilWeatherFetcher:
    def __init__(self, output_dir: str = "data/landing/external_factors-raw/openweather"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.today = datetime.now().strftime("%Y%m%d")
        
        # Create daily subdirectory
        self.daily_dir = self.output_dir / self.today
        self.daily_dir.mkdir(exist_ok=True)
        
        # All Brazilian states with their capital cities and coordinates
        self.brazilian_states = {
            'AC': {'name': 'Acre', 'capital': 'Rio Branco', 'lat': -9.974, 'lon': -67.824},
            'AL': {'name': 'Alagoas', 'capital': 'Maceió', 'lat': -9.665, 'lon': -35.735},
            'AP': {'name': 'Amapá', 'capital': 'Macapá', 'lat': 0.038, 'lon': -51.069},
            'AM': {'name': 'Amazonas', 'capital': 'Manaus', 'lat': -3.119, 'lon': -60.021},
            'BA': {'name': 'Bahia', 'capital': 'Salvador', 'lat': -12.971, 'lon': -38.501},
            'CE': {'name': 'Ceará', 'capital': 'Fortaleza', 'lat': -3.717, 'lon': -38.543},
            'DF': {'name': 'Distrito Federal', 'capital': 'Brasília', 'lat': -15.827, 'lon': -47.921},
            'ES': {'name': 'Espírito Santo', 'capital': 'Vitória', 'lat': -20.319, 'lon': -40.337},
            'GO': {'name': 'Goiás', 'capital': 'Goiânia', 'lat': -16.686, 'lon': -49.264},
            'MA': {'name': 'Maranhão', 'capital': 'São Luís', 'lat': -2.529, 'lon': -44.302},
            'MT': {'name': 'Mato Grosso', 'capital': 'Cuiabá', 'lat': -15.601, 'lon': -56.097},
            'MS': {'name': 'Mato Grosso do Sul', 'capital': 'Campo Grande', 'lat': -20.469, 'lon': -54.620},
            'MG': {'name': 'Minas Gerais', 'capital': 'Belo Horizonte', 'lat': -19.916, 'lon': -43.934},
            'PA': {'name': 'Pará', 'capital': 'Belém', 'lat': -1.455, 'lon': -48.490},
            'PB': {'name': 'Paraíba', 'capital': 'João Pessoa', 'lat': -7.119, 'lon': -34.843},
            'PR': {'name': 'Paraná', 'capital': 'Curitiba', 'lat': -25.428, 'lon': -49.273},
            'PE': {'name': 'Pernambuco', 'capital': 'Recife', 'lat': -8.047, 'lon': -34.877},
            'PI': {'name': 'Piauí', 'capital': 'Teresina', 'lat': -5.089, 'lon': -42.801},
            'RJ': {'name': 'Rio de Janeiro', 'capital': 'Rio de Janeiro', 'lat': -22.906, 'lon': -43.172},
            'RN': {'name': 'Rio Grande do Norte', 'capital': 'Natal', 'lat': -5.794, 'lon': -35.209},
            'RS': {'name': 'Rio Grande do Sul', 'capital': 'Porto Alegre', 'lat': -30.032, 'lon': -51.230},
            'RO': {'name': 'Rondônia', 'capital': 'Porto Velho', 'lat': -8.761, 'lon': -63.900},
            'RR': {'name': 'Roraima', 'capital': 'Boa Vista', 'lat': 2.819, 'lon': -60.673},
            'SC': {'name': 'Santa Catarina', 'capital': 'Florianópolis', 'lat': -27.595, 'lon': -48.548},
            'SP': {'name': 'São Paulo', 'capital': 'São Paulo', 'lat': -23.551, 'lon': -46.633},
            'SE': {'name': 'Sergipe', 'capital': 'Aracaju', 'lat': -10.909, 'lon': -37.074},
            'TO': {'name': 'Tocantins', 'capital': 'Palmas', 'lat': -10.175, 'lon': -48.332}
        }
        
    def fetch_historical_weather(self, lat: float, lon: float, state_code: str, 
                            days: int = 730) -> Optional[pd.DataFrame]:
        """Fetch historical weather data using Open-Meteo API (free alternative)"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Using Open-Meteo API (free, no API key required)
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                'latitude': lat,
                'longitude': lon,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'daily': [
                    'temperature_2m_mean',
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'precipitation_hours',
                    'wind_speed_10m_max',
                    'wind_direction_10m_dominant',
                    'relative_humidity_2m_mean',
                    'pressure_msl_mean',
                    'cloud_cover_mean',
                    'sunshine_duration',
                    'weather_code'
                ],
                'timezone': 'America/Sao_Paulo'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                
                if 'daily' in data:
                    daily_data = data['daily']
                    
                    df = pd.DataFrame({
                        'date': pd.to_datetime(daily_data['time']),
                        'state_code': state_code,
                        'state_name': self.brazilian_states[state_code]['name'],
                        'capital_city': self.brazilian_states[state_code]['capital'],
                        'latitude': lat,
                        'longitude': lon,
                        'temperature_mean_c': daily_data.get('temperature_2m_mean'),
                        'temperature_max_c': daily_data.get('temperature_2m_max'),
                        'temperature_min_c': daily_data.get('temperature_2m_min'),
                        'precipitation_mm': daily_data.get('precipitation_sum'),
                        'precipitation_hours': daily_data.get('precipitation_hours'),
                        'wind_speed_max_kmh': daily_data.get('wind_speed_10m_max'),
                        'wind_direction_deg': daily_data.get('wind_direction_10m_dominant'),
                        'humidity_percent': daily_data.get('relative_humidity_2m_mean'),
                        'pressure_hpa': daily_data.get('pressure_msl_mean'),
                        'cloud_cover_percent': daily_data.get('cloud_cover_mean'),
                        'sunshine_hours': daily_data.get('sunshine_duration'),
                        'weather_code': daily_data.get('weather_code')
                    })
                    
                    return df
            
            return None
        except Exception as e:
            print(f"Error fetching historical weather for {state_code}: {e}")
            return None
    
    def fetch_forecast_weather(self, lat: float, lon: float, state_code: str) -> Optional[pd.DataFrame]:
        """Fetch 5-day weather forecast"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'daily': [
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'wind_speed_10m_max',
                    'weather_code'
                ],
                'timezone': 'America/Sao_Paulo',
                'forecast_days': 5
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                if 'daily' in data:
                    daily_data = data['daily']
                    
                    df = pd.DataFrame({
                        'date': pd.to_datetime(daily_data['time']),
                        'state_code': state_code,
                        'state_name': self.brazilian_states[state_code]['name'],
                        'capital_city': self.brazilian_states[state_code]['capital'],
                        'latitude': lat,
                        'longitude': lon,
                        'temperature_max_c': daily_data.get('temperature_2m_max'),
                        'temperature_min_c': daily_data.get('temperature_2m_min'),
                        'precipitation_mm': daily_data.get('precipitation_sum'),
                        'wind_speed_max_kmh': daily_data.get('wind_speed_10m_max'),
                        'weather_code': daily_data.get('weather_code'),
                        'data_type': 'forecast'
                    })
                    
                    return df
            
            return None
        except Exception as e:
            print(f"Error fetching forecast weather for {state_code}: {e}")
            return None
    
    def download_all_states_weather(self, historical_days: int = 730) -> Dict[str, pd.DataFrame]:
        """Download weather data for all Brazilian states"""
        historical_data = []
        forecast_data = []
        
        total_states = len(self.brazilian_states)
        processed = 0
        
        for state_code, state_info in self.brazilian_states.items():
            processed += 1
            print(f"Processing {state_info['name']} ({processed}/{total_states})...")
            
            lat = state_info['lat']
            lon = state_info['lon']
            
            # Fetch historical data
            hist_df = self.fetch_historical_weather(lat, lon, state_code, historical_days)
            if hist_df is not None:
                historical_data.append(hist_df)
                print(f"  + Historical data: {len(hist_df)} records")
            else:
                print(f"  - Failed to fetch historical data")
            
            # Short delay to avoid rate limiting
            time.sleep(1)
            
            # Fetch forecast data
            forecast_df = self.fetch_forecast_weather(lat, lon, state_code)
            if forecast_df is not None:
                forecast_data.append(forecast_df)
                print(f"  + Forecast data: {len(forecast_df)} records")
            else:
                print(f"  - Failed to fetch forecast data")
            
            # Longer delay between states
            time.sleep(2)
        
        # Combine all data
        results = {}
        
        if historical_data:
            historical_combined = pd.concat(historical_data, ignore_index=True)
            results['historical'] = historical_combined
            print(f"Combined historical data: {len(historical_combined)} records")
        
        if forecast_data:
            forecast_combined = pd.concat(forecast_data, ignore_index=True)
            results['forecast'] = forecast_combined
            print(f"Combined forecast data: {len(forecast_combined)} records")
        
        return results
    
    def save_data(self, data: Dict[str, pd.DataFrame]):
        """Save data to files"""
        if 'historical' in data:
            hist_file = self.daily_dir / 'brazil_historical_weather.csv'
            data['historical'].to_csv(hist_file, index=False)
            print(f"Saved historical weather data to {hist_file}")
        
        if 'forecast' in data:
            forecast_file = self.daily_dir / 'brazil_forecast_weather.csv'
            data['forecast'].to_csv(forecast_file, index=False)
            print(f"Saved forecast weather data to {forecast_file}")
        
        # Save individual state files for easier processing
        if 'historical' in data:
            hist_data = data['historical']
            for state_code in hist_data['state_code'].unique():
                state_data = hist_data[hist_data['state_code'] == state_code]
                state_file = self.daily_dir / f'weather_{state_code.lower()}.csv'
                state_data.to_csv(state_file, index=False)
            
            print(f"Saved individual state weather files to {self.daily_dir}")
    
    def create_summary_json(self, data: Dict[str, pd.DataFrame]):
        """Create summary of downloaded weather data"""
        summary = {
            'download_date': datetime.now().isoformat(),
            'brazilian_states_covered': len(self.brazilian_states),
            'weather_data': {}
        }
        
        for data_type, df in data.items():
            if df is not None and len(df) > 0:
                summary['weather_data'][data_type] = {
                    'records': len(df),
                    'date_range': {
                        'start': df['date'].min().isoformat(),
                        'end': df['date'].max().isoformat()
                    },
                    'states': df['state_code'].unique().tolist(),
                    'columns': df.columns.tolist()
                }
        
        summary_file = self.daily_dir / 'brazil_weather_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Summary saved to {summary_file}")
        return summary
    
    def generate_sample_data(self, state_code: str, days: int = 730) -> pd.DataFrame:
        """Generate sample weather data when API fails"""
        start_date = datetime.now() - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=datetime.now(), freq='D')
        
        state_info = self.brazilian_states[state_code]
        base_temp = 25.0  # Base temperature for Brazil
        
        # Adjust base temperature by state (approximate climate zones)
        climate_adjustment = {
            'AC': 2, 'AM': 2, 'AP': 2, 'PA': 2, 'RO': 2, 'RR': 2, 'TO': 2,  # North
            'AL': 0, 'BA': 0, 'CE': 0, 'MA': 0, 'PB': 0, 'PE': 0, 'PI': 0, 
            'RN': 0, 'SE': 0,  # Northeast
            'DF': 1, 'GO': 1, 'MS': 1, 'MT': 1,  # Center-West
            'ES': 0, 'MG': 0, 'RJ': 0, 'SP': 0,  # Southeast
            'PR': -2, 'RS': -2, 'SC': -2  # South
        }
        
        temp_adjustment = climate_adjustment.get(state_code, 0)
        
        import random
        random.seed(42)
        
        data = []
        for i, date in enumerate(dates):
            # Seasonal variation
            day_of_year = date.timetuple().tm_yday
            seasonal_factor = 5 * (1 - abs((day_of_year - 180) / 180))
            
            # Random daily variation
            daily_variation = random.uniform(-3, 3)
            
            # Temperature calculation
            temp_mean = base_temp + temp_adjustment + seasonal_factor + daily_variation
            temp_max = temp_mean + random.uniform(2, 8)
            temp_min = temp_mean - random.uniform(2, 8)
            
            # Precipitation (seasonal)
            precip_prob = 0.3 if (day_of_year > 330 or day_of_year < 60) else 0.6  # Summer rains
            precipitation = random.uniform(0, 50) if random.random() < precip_prob else 0
            
            # Wind
            wind_speed = random.uniform(5, 25)
            wind_direction = random.uniform(0, 360)
            
            # Humidity
            humidity = random.uniform(50, 95)
            
            # Pressure
            pressure = random.uniform(1008, 1025)
            
            data.append({
                'date': date,
                'state_code': state_code,
                'state_name': state_info['name'],
                'capital_city': state_info['capital'],
                'latitude': state_info['lat'],
                'longitude': state_info['lon'],
                'temperature_mean_c': round(temp_mean, 1),
                'temperature_max_c': round(temp_max, 1),
                'temperature_min_c': round(temp_min, 1),
                'precipitation_mm': round(precipitation, 1),
                'precipitation_hours': random.uniform(0, 24),
                'wind_speed_max_kmh': round(wind_speed, 1),
                'wind_direction_deg': round(wind_direction, 0),
                'humidity_percent': round(humidity, 0),
                'pressure_hpa': round(pressure, 0),
                'cloud_cover_percent': random.uniform(0, 100),
                'sunshine_hours': random.uniform(0, 12),
                'weather_code': random.randint(0, 95)
            })
        
        return pd.DataFrame(data)

def main():
    """Main execution function"""
    print("Starting Brazilian weather data download...")
    print(f"Downloading data for all {27} Brazilian states")
    
    fetcher = BrazilWeatherFetcher()
    
    # Download all states weather data
    data = fetcher.download_all_states_weather(historical_days=730)
    
    # Save data
    fetcher.save_data(data)
    
    # Create summary
    summary = fetcher.create_summary_json(data)
    
    print("Brazilian weather data download completed!")
    print(f"States processed: {summary['brazilian_states_covered']}")
    
    for data_type, info in summary['weather_data'].items():
        print(f"{data_type.title()}: {info['records']} records")
    
    return data, summary

if __name__ == "__main__":
    main()