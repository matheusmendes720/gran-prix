"""
Configuration and credentials management
"""

import os
import json
from pathlib import Path

class FreightDataConfig:
    def __init__(self, config_file='.env.freight'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file or environment"""
        config = {
            'trading_economics_key': os.getenv('TRADING_ECONOMICS_API_KEY', 'guest:guest'),
            'output_dir': os.getenv('FREIGHT_DATA_DIR', 'data/manual'),
            'log_level': os.getenv('FREIGHT_LOG_LEVEL', 'INFO'),
            'download_schedule': {
                'bdi': 'daily at 2:00 AM',
                'drewry': 'manual (contact supplychain@drewry.co.uk)',
                'scfi': 'manual (visit investing.com)',
                'unctad': 'manual (unctadstat.unctad.org)',
                'imf': 'weekly Monday 3:00 AM',
                'fbx': 'on demand (partial free access)'
            },
            'data_sources': {
                'bdi': {
                    'type': 'api',
                    'provider': 'trading_economics',
                    'ticker': 'BDIY',
                    'frequency': 'daily'
                },
                'drewry': {
                    'type': 'manual',
                    'url': 'https://www.drewry.co.uk/supply-chain-advisors/world-container-index',
                    'contact': 'supplychain@drewry.co.uk',
                    'frequency': 'weekly'
                },
                'scfi': {
                    'type': 'scraping',
                    'url': 'https://www.investing.com/indices/shanghai-containerized-freight-index',
                    'method': 'selenium',
                    'frequency': 'weekly'
                },
                'unctad': {
                    'type': 'manual',
                    'url': 'https://unctadstat.unctad.org/wds/TableViewer/tableView.aspx?ReportId=92',
                    'frequency': 'quarterly'
                },
                'imf': {
                    'type': 'api',
                    'provider': 'world_bank',
                    'endpoint': '/v2/country/WLD/indicator/IM.fs.sp_cons.sh',
                    'frequency': 'annual'
                },
                'fbx': {
                    'type': 'api',
                    'provider': 'trading_economics',
                    'access': 'limited (free tier)',
                    'symbols': ['MEX:FBX', 'NZL:FBX', 'SWE:FBX', 'THA:FBX']
                }
            }
        }

        return config

    def get(self, key, default=None):
        """Get config value"""
        parts = key.split('.')
        value = self.config
        for part in parts:
            value = value.get(part, {}) if isinstance(value, dict) else default
        return value

    def print_config(self):
        """Pretty print configuration"""
        print("\n" + "="*60)
        print("FREIGHT DATA CONFIGURATION")
        print("="*60)
        print(json.dumps(self.config, indent=2))
        print("="*60 + "\n")

if __name__ == "__main__":
    config = FreightDataConfig()
    config.print_config()
