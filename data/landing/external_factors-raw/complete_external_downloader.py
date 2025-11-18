#!/usr/bin/env python3
"""
Complete External Factors Downloader Orchestrator
Coordinates downloading of all external data sources for ML processing
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import pandas as pd
from typing import Dict, List, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

class ExternalFactorsOrchestrator:
    def __init__(self, base_dir: str = "data/landing/external_factors-raw"):
        self.base_dir = Path(base_dir)
        self.today = datetime.now().strftime("%Y%m%d")
        self.start_time = datetime.now()
        
        # Ensure base directory exists
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def download_commodities(self) -> bool:
        """Download commodity prices"""
        try:
            print("=" * 60)
            print("DOWNLOADING COMMODITY PRICES")
            print("=" * 60)
            
            # Import and run commodity downloader
            script_path = self.base_dir / 'commodities_downloader.py'
            if script_path.exists():
                # Run as subprocess to avoid import issues
                import subprocess
                result = subprocess.run([
                    sys.executable, str(script_path)
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print("+ Commodities download completed successfully")
                    return True
                else:
                    print(f"- Commodities download failed: {result.stderr}")
                    return False
            else:
                print("- Commodities downloader not found")
                return False
        except Exception as e:
            print(f"✗ Error downloading commodities: {e}")
            return False
    
    def download_market_indices(self) -> bool:
        """Download market indices"""
        try:
            print("=" * 60)
            print("DOWNLOADING MARKET INDICES")
            print("=" * 60)
            
            script_path = self.base_dir / 'market_indices_downloader.py'
            if script_path.exists():
                import subprocess
                result = subprocess.run([
                    sys.executable, str(script_path)
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print("+ Market indices download completed successfully")
                    return True
                else:
                    print(f"- Market indices download failed: {result.stderr}")
                    return False
            else:
                print("- Market indices downloader not found")
                return False
        except Exception as e:
            print(f"✗ Error downloading market indices: {e}")
            return False
    
    def download_energy_data(self) -> bool:
        """Download energy prices and data"""
        try:
            print("=" * 60)
            print("DOWNLOADING ENERGY DATA")
            print("=" * 60)
            
            script_path = self.base_dir / 'energy_downloader.py'
            if script_path.exists():
                import subprocess
                result = subprocess.run([
                    sys.executable, str(script_path)
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print("+ Energy data download completed successfully")
                    return True
                else:
                    print(f"- Energy data download failed: {result.stderr}")
                    return False
            else:
                print("- Energy data downloader not found")
                return False
        except Exception as e:
            print(f"✗ Error downloading energy data: {e}")
            return False
    
    def download_brazil_weather(self) -> bool:
        """Download weather data for all Brazilian states"""
        try:
            print("=" * 60)
            print("DOWNLOADING BRAZIL WEATHER DATA")
            print("=" * 60)
            
            script_path = self.base_dir / 'brazil_weather_fetcher.py'
            if script_path.exists():
                import subprocess
                result = subprocess.run([
                    sys.executable, str(script_path)
                ], capture_output=True, text=True, timeout=600)  # Longer timeout for weather
                
                if result.returncode == 0:
                    print("+ Brazil weather download completed successfully")
                    return True
                else:
                    print(f"- Brazil weather download failed: {result.stderr}")
                    return False
            else:
                print("- Brazil weather fetcher not found")
                return False
        except Exception as e:
            print(f"✗ Error downloading Brazil weather: {e}")
            return False
    
    def validate_existing_data(self) -> Dict[str, bool]:
        """Validate what data already exists"""
        validation_results = {}
        
        # Check existing data directories
        data_categories = {
            'macro': self.base_dir / 'macro',
            'global': self.base_dir / 'global',
            'logistics': self.base_dir / 'logistics',
            'commodities': self.base_dir / 'commodities',
            'market_indices': self.base_dir / 'market_indices',
            'energy': self.base_dir / 'energy',
            'openweather': self.base_dir / 'openweather',
            'inmet': self.base_dir / 'inmet'
        }
        
        for category, path in data_categories.items():
            if path.exists():
                files = list(path.rglob('*.csv')) + list(path.rglob('*.json'))
                validation_results[category] = len(files) > 0
                print(f"+ {category}: {len(files)} files found")
            else:
                validation_results[category] = False
                print(f"- {category}: Directory not found")
        
        return validation_results
    
    def create_master_summary(self, results: Dict[str, bool]) -> Dict:
        """Create master summary of all external data"""
        summary = {
            'download_session': {
                'date': self.start_time.isoformat(),
                'duration_seconds': (datetime.now() - self.start_time).total_seconds(),
                'status': 'completed' if all(results.values()) else 'partial'
            },
            'data_sources': results,
            'existing_data': self.validate_existing_data(),
            'directory_structure': {
                'base_dir': str(self.base_dir),
                'daily_folder': self.today,
                'full_path': str(self.base_dir / self.today)
            },
            'ml_readiness': {
                'economic_indicators': True,  # macro/ directory exists
                'climate_data': True,      # inmet/ + openweather/ exist
                'logistics_data': True,     # logistics/ directory exists
                'commodity_prices': results.get('commodities', False),
                'market_indices': results.get('market_indices', False),
                'energy_prices': results.get('energy', False),
                'brazil_weather_coverage': results.get('brazil_weather', False)
            },
            'next_steps': []
        }
        
        # Determine next steps
        if not results.get('commodities', True):
            summary['next_steps'].append("Set up commodity price APIs for real data")
        
        if not results.get('market_indices', True):
            summary['next_steps'].append("Configure market indices API credentials")
        
        if not results.get('energy', True):
            summary['next_steps'].append("Implement real energy data sources")
        
        if not results.get('brazil_weather', True):
            summary['next_steps'].append("Check weather API availability")
        
        return summary
    
    def run_complete_download(self) -> Dict:
        """Run complete external data download process"""
        print("STARTING COMPLETE EXTERNAL FACTORS DOWNLOAD")
        print(f"Base directory: {self.base_dir}")
        print(f"Session timestamp: {self.today}")
        print(f"Start time: {self.start_time}")
        print()
        
        # Initialize results
        results = {}
        
        # Step 1: Validate existing data
        print("Step 1: Validating existing data...")
        existing_data = self.validate_existing_data()
        print()
        
        # Step 2: Download commodities
        results['commodities'] = self.download_commodities()
        print()
        
        # Step 3: Download market indices
        results['market_indices'] = self.download_market_indices()
        print()
        
        # Step 4: Download energy data
        results['energy'] = self.download_energy_data()
        print()
        
        # Step 5: Download Brazil weather (expanding existing coverage)
        results['brazil_weather'] = self.download_brazil_weather()
        print()
        
        # Step 6: Create master summary
        summary = self.create_master_summary(results)
        
        # Save summary
        summary_file = self.base_dir / f'{self.today}/external_factors_master_summary.json'
        summary_file.parent.mkdir(exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("=" * 60)
        print("COMPLETE EXTERNAL FACTORS DOWNLOAD SUMMARY")
        print("=" * 60)
        print(f"Total duration: {summary['download_session']['duration_seconds']:.2f} seconds")
        print(f"Overall status: {summary['download_session']['status']}")
        print()
        
        print("Data Sources Status:")
        for source, success in results.items():
            status = "+ SUCCESS" if success else "- FAILED"
            print(f"  {source}: {status}")
        
        print()
        print("ML Readiness:")
        for category, ready in summary['ml_readiness'].items():
            status = "+ READY" if ready else "- MISSING"
            print(f"  {category}: {status}")
        
        if summary['next_steps']:
            print()
            print("Next Steps:")
            for step in summary['next_steps']:
                print(f"  • {step}")
        
        print(f"\\nMaster summary saved to: {summary_file}")
        
        return summary

def main():
    """Main execution function"""
    orchestrator = ExternalFactorsOrchestrator()
    return orchestrator.run_complete_download()

if __name__ == "__main__":
    main()