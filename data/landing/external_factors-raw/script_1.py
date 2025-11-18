
# Create specialized scripts for different scenarios

# 1. Trading Economics API Script
trading_econ_script = '''"""
Trading Economics Freight Data Fetcher
Handles BDI, FBX, and other shipping indices via Trading Economics API
"""

import os
from datetime import datetime, timedelta
import csv

# Using requests for broader compatibility
try:
    import requests
except ImportError:
    raise ImportError("Install: pip install requests")

class TradingEconomicsFreightFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('TRADING_ECONOMICS_API_KEY', 'guest:guest')
        self.base_url = "https://api.tradingeconomics.com"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    def get_historical_ticker(self, ticker, start_date=None, end_date=None):
        """
        Fetch historical data for a ticker
        Common shipping tickers:
        - BDIY: Baltic Dry Index
        - BDI: Baltic Dry Index (alternative)
        - FBXINDEX: Freightos FBX
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/historical/ticker/{ticker}/{start_date}?c={self.api_key}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None
    
    def save_to_csv(self, data, filename):
        if not data or not isinstance(data, list):
            print(f"No valid data for {filename}")
            return False
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'close', 'ticker'])
                writer.writeheader()
                
                for record in data:
                    writer.writerow({
                        'date': record.get('date', '').split('T')[0],
                        'close': record.get('close', ''),
                        'ticker': record.get('ticker', '')
                    })
            
            print(f"✓ Saved {len(data)} records to {filename}")
            return True
        except Exception as e:
            print(f"Error saving CSV: {e}")
            return False

# Usage
if __name__ == "__main__":
    fetcher = TradingEconomicsFreightFetcher()
    
    # Fetch BDI
    print("Fetching Baltic Dry Index...")
    bdi_data = fetcher.get_historical_ticker('BDIY')
    if bdi_data:
        fetcher.save_to_csv(bdi_data, 'data/manual/bdi_history.csv')
    
    # Note: FBX may require paid access
    # fbx_data = fetcher.get_historical_ticker('FBXINDEX')
'''

with open('trading_econ_fetcher.py', 'w') as f:
    f.write(trading_econ_script)

print("✓ trading_econ_fetcher.py created")

# 2. Selenium-based scraper for dynamic sites
selenium_script = '''"""
Selenium-based scraper for Investing.com and other JS-heavy sites
Requires: pip install selenium webdriver-manager
"""

from datetime import datetime, timedelta
import csv
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    raise ImportError("Install: pip install selenium webdriver-manager")

class InvestingComScraper:
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 10)
    
    def scrape_scfi_historical(self, output_file='scfi_data.csv'):
        """
        Scrape Shanghai Containerized Freight Index from Investing.com
        URL: https://www.investing.com/indices/shanghai-containerized-freight-index
        """
        url = "https://www.investing.com/indices/shanghai-containerized-freight-index"
        
        try:
            print(f"Navigating to {url}...")
            self.driver.get(url)
            
            # Wait for table to load
            time.sleep(3)
            
            # Click on download/export button (may vary by page structure)
            # Look for table data in page source
            page_source = self.driver.page_source
            
            # Extract data using regex or BeautifulSoup on rendered content
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find table rows
            rows = soup.find_all('tr')
            data = []
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    try:
                        date_text = cols[0].text.strip()
                        value_text = cols[1].text.strip().replace(',', '')
                        value = float(value_text)
                        
                        data.append({
                            'date': date_text,
                            'value': value,
                            'index': 'SCFI'
                        })
                    except (ValueError, IndexError):
                        continue
            
            # Save to CSV
            if data:
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['date', 'value', 'index'])
                    writer.writeheader()
                    writer.writerows(data)
                print(f"✓ Scraped {len(data)} SCFI records to {output_file}")
            
            return data
            
        except Exception as e:
            print(f"Scraping error: {e}")
            return None
        finally:
            self.driver.quit()

# Usage
if __name__ == "__main__":
    scraper = InvestingComScraper(headless=True)
    scraper.scrape_scfi_historical('data/manual/scfi_scraped.csv')
'''

with open('selenium_freight_scraper.py', 'w') as f:
    f.write(selenium_script)

print("✓ selenium_freight_scraper.py created")

# 3. World Bank/IMF API Fetcher
worldbank_script = '''"""
World Bank API fetcher for IMF Shipping Cost Index
"""

import requests
import csv
from datetime import datetime

class WorldBankFreightFetcher:
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"
        self.session = requests.Session()
    
    def get_indicator(self, indicator_code, start_year=2000, end_year=2024):
        """
        Fetch World Bank indicator data
        
        Common freight-related indicators:
        - IM.fs.sp_cons.sh: Shipping cost as % of imports (IMF SCI proxy)
        - NY.GDP.FCST.CD: GDP forecast (proxy for demand)
        """
        url = f"{self.base_url}/country/WLD/indicator/{indicator_code}"
        
        params = {
            'format': 'json',
            'date': f'{start_year}:{end_year}',
            'per_page': 500
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if len(data) < 2:
                return None
            
            records = data[1]
            parsed = []
            
            for record in records:
                if record.get('value'):
                    parsed.append({
                        'date': record['date'],
                        'value': record['value'],
                        'indicator': indicator_code,
                        'country': record['country']['value']
                    })
            
            return parsed
        
        except Exception as e:
            print(f"Error fetching {indicator_code}: {e}")
            return None
    
    def save_csv(self, data, filename):
        if not data:
            print(f"No data to save")
            return False
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'value', 'indicator', 'country'])
                writer.writeheader()
                writer.writerows(sorted(data, key=lambda x: x['date'], reverse=True))
            
            print(f"✓ Saved {len(data)} records to {filename}")
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False

# Usage
if __name__ == "__main__":
    fetcher = WorldBankFreightFetcher()
    
    # Fetch IMF Shipping Cost Index proxy
    print("Fetching IMF Shipping Cost Index (World Bank proxy)...")
    data = fetcher.get_indicator('IM.fs.sp_cons.sh')
    if data:
        fetcher.save_csv(data, 'data/manual/imf_shipping_cost.csv')
'''

with open('worldbank_freight_fetcher.py', 'w') as f:
    f.write(worldbank_script)

print("✓ worldbank_freight_fetcher.py created")

# 4. Scheduler/Cron configuration
scheduler_script = '''"""
Scheduling script for automated daily/weekly downloads
Requires: pip install schedule APScheduler
"""

import schedule
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FreightDataScheduler:
    def __init__(self):
        self.schedule = schedule.Scheduler()
    
    def run_bdi_download(self):
        """Run BDI download via Trading Economics"""
        logger.info("Starting BDI download...")
        try:
            from trading_econ_fetcher import TradingEconomicsFreightFetcher
            fetcher = TradingEconomicsFreightFetcher()
            data = fetcher.get_historical_ticker('BDIY')
            if data:
                fetcher.save_to_csv(data, f"data/manual/bdi_{datetime.now().strftime('%Y%m%d')}.csv")
                logger.info("✓ BDI download completed")
        except Exception as e:
            logger.error(f"BDI download failed: {e}")
    
    def run_imf_download(self):
        """Run IMF Shipping Cost Index download"""
        logger.info("Starting IMF SCI download...")
        try:
            from worldbank_freight_fetcher import WorldBankFreightFetcher
            fetcher = WorldBankFreightFetcher()
            data = fetcher.get_indicator('IM.fs.sp_cons.sh')
            if data:
                fetcher.save_csv(data, f"data/manual/imf_sci_{datetime.now().strftime('%Y%m%d')}.csv")
                logger.info("✓ IMF SCI download completed")
        except Exception as e:
            logger.error(f"IMF download failed: {e}")
    
    def setup_daily_schedule(self):
        """Setup daily download tasks"""
        # Daily at 2 AM
        self.schedule.every().day.at("02:00").do(self.run_bdi_download)
        
        # Weekly on Monday at 3 AM (Drewry publishes weekly)
        self.schedule.every().monday.at("03:00").do(self.run_imf_download)
        
        logger.info("Schedule configured")
    
    def run_continuous(self):
        """Run scheduler in continuous loop"""
        logger.info("Scheduler started. Press Ctrl+C to stop.")
        
        while True:
            self.schedule.run_pending()
            time.sleep(60)

# Alternative: APScheduler for production use
def setup_apscheduler():
    """Setup with APScheduler for production (background service)"""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        
        scheduler = BackgroundScheduler()
        
        # BDI daily at 2 AM
        scheduler.add_job(
            FreightDataScheduler().run_bdi_download,
            CronTrigger(hour=2, minute=0),
            id='bdi_daily'
        )
        
        # IMF weekly Monday 3 AM
        scheduler.add_job(
            FreightDataScheduler().run_imf_download,
            CronTrigger(day_of_week='mon', hour=3, minute=0),
            id='imf_weekly'
        )
        
        scheduler.start()
        logger.info("APScheduler started in background")
        return scheduler
    
    except ImportError:
        logger.warning("APScheduler not installed")
        return None

# Usage examples
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['once', 'schedule', 'apscheduler'], 
                       default='once',
                       help='Run mode: single execution, schedule loop, or background')
    args = parser.parse_args()
    
    scheduler = FreightDataScheduler()
    
    if args.mode == 'once':
        scheduler.run_bdi_download()
        scheduler.run_imf_download()
    
    elif args.mode == 'schedule':
        scheduler.setup_daily_schedule()
        scheduler.run_continuous()
    
    elif args.mode == 'apscheduler':
        setup_apscheduler()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
'''

with open('freight_data_scheduler.py', 'w') as f:
    f.write(scheduler_script)

print("✓ freight_data_scheduler.py created")

# 5. Configuration file
config_script = '''"""
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
        print("\\n" + "="*60)
        print("FREIGHT DATA CONFIGURATION")
        print("="*60)
        print(json.dumps(self.config, indent=2))
        print("="*60 + "\\n")

if __name__ == "__main__":
    config = FreightDataConfig()
    config.print_config()
'''

with open('freight_config.py', 'w') as f:
    f.write(config_script)

print("✓ freight_config.py created")

print("\\n" + "="*60)
print("AUTOMATION SCRIPTS CREATED")
print("="*60)
print("\\nAll scripts saved to current directory:")
print("1. freight_data_automation.py      - Main orchestrator (recommended)")
print("2. trading_econ_fetcher.py         - Trading Economics API wrapper")
print("3. selenium_freight_scraper.py     - Selenium scraper for JS sites")
print("4. worldbank_freight_fetcher.py    - World Bank/IMF API fetcher")
print("5. freight_data_scheduler.py       - Scheduling & automation")
print("6. freight_config.py               - Configuration management")
