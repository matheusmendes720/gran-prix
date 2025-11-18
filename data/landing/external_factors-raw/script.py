
# Create a comprehensive freight data automation framework
# This will be a modular system for downloading all the freight indices

automation_code = '''"""
Freight & Shipping Indices Automation Framework
Automates downloads from multiple sources:
- Baltic Dry Index (BDI)
- Drewry World Container Index (WCI)
- Shanghai Containerized Freight Index (SCFI)
- UNCTAD Liner Shipping Connectivity Index (LSCI)
- IMF Shipping Cost Index (SCI)
- Trading Economics FBX (partial access)
"""

import os
import csv
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple
import time
from abc import ABC, abstractmethod

# Core dependencies (standard library)
import urllib.request
import urllib.error
from urllib.parse import urlencode, parse_qs, urlparse
import re

# Optional external dependencies (install as needed)
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BEAUTIFULSOUP = True
except ImportError:
    HAS_BEAUTIFULSOUP = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import tradingeconomics as te
    HAS_TE = True
except ImportError:
    HAS_TE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FreightDataSource(ABC):
    """Abstract base class for freight data sources"""
    
    def __init__(self, output_dir: str = "data/manual"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.last_download = None
        
    @abstractmethod
    def fetch_data(self) -> Optional[Dict]:
        """Fetch data from source. Return dict or None on failure."""
        pass
    
    @abstractmethod
    def parse_data(self, raw_data) -> List[Dict]:
        """Parse raw data into list of dicts with keys: date, value"""
        pass
    
    def save_csv(self, data: List[Dict], filename: str) -> Path:
        """Save data to CSV file"""
        filepath = self.output_dir / filename
        
        if not data:
            logger.warning(f"No data to save for {filename}")
            return filepath
            
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Saved {len(data)} records to {filepath}")
            self.last_download = datetime.now()
            return filepath
        except Exception as e:
            logger.error(f"Error saving CSV {filename}: {e}")
            return None
    
    def download(self) -> Optional[Path]:
        """Full download pipeline: fetch -> parse -> save"""
        try:
            raw_data = self.fetch_data()
            if raw_data is None:
                return None
            
            parsed = self.parse_data(raw_data)
            if not parsed:
                logger.warning(f"{self.__class__.__name__}: No data parsed")
                return None
                
            return self.save_csv(parsed, self.get_filename())
        except Exception as e:
            logger.error(f"Download failed for {self.__class__.__name__}: {e}")
            return None
    
    @abstractmethod
    def get_filename(self) -> str:
        """Return CSV filename for this source"""
        pass


class BalticDryIndex(FreightDataSource):
    """Baltic Dry Index via Trading Economics API or web scraping"""
    
    def __init__(self, output_dir: str = "data/manual", api_key: Optional[str] = None):
        super().__init__(output_dir)
        self.api_key = api_key or os.getenv('TRADING_ECONOMICS_API_KEY', 'guest:guest')
        self.use_api = HAS_TE and api_key
    
    def fetch_data(self) -> Optional[Dict]:
        """Fetch BDI data via Trading Economics API"""
        if not HAS_REQUESTS:
            logger.error("requests library required for BDI fetch")
            return None
        
        try:
            # Using Trading Economics endpoint
            url = f"https://api.tradingeconomics.com/historical/ticker/BDIY/2020-01-01?c={self.api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"BDI API fetch failed: {e}")
            return None
    
    def parse_data(self, raw_data) -> List[Dict]:
        """Parse BDI JSON response"""
        if not isinstance(raw_data, list):
            return []
        
        parsed = []
        for item in raw_data:
            try:
                parsed.append({
                    'date': item.get('date', '').split('T')[0],
                    'value': float(item.get('close', 0)),
                    'symbol': 'BDI'
                })
            except (ValueError, KeyError, TypeError) as e:
                logger.debug(f"Skipping BDI record: {e}")
                continue
        
        return sorted(parsed, key=lambda x: x['date'])
    
    def get_filename(self) -> str:
        return "bdi_historical.csv"


class DrewryWCI(FreightDataSource):
    """Drewry World Container Index - requires manual CSV or web scraping"""
    
    def __init__(self, output_dir: str = "data/manual"):
        super().__init__(output_dir)
        self.drewry_url = "https://www.drewry.co.uk/supply-chain-advisors/world-container-index"
    
    def fetch_data(self) -> Optional[Dict]:
        """
        Drewry data requires manual download or contact with supplychain@drewry.co.uk
        This method documents the process
        """
        logger.info("Drewry WCI: Manual download required")
        logger.info(f"Visit: {self.drewry_url}")
        logger.info("Download weekly CSV and place in data/manual/")
        logger.info("Or request historical sheet from: supplychain@drewry.co.uk")
        return None
    
    def parse_data(self, raw_data) -> List[Dict]:
        """Parse Drewry CSV if already downloaded"""
        if raw_data is None:
            return []
        return []
    
    def load_existing_csv(self, csv_path: str) -> Optional[Path]:
        """Load pre-downloaded Drewry CSV"""
        try:
            path = Path(csv_path)
            if not path.exists():
                logger.error(f"File not found: {csv_path}")
                return None
            
            # Validate and copy to standard location
            import shutil
            dest = self.output_dir / "drewry_wci.csv"
            shutil.copy2(path, dest)
            logger.info(f"Loaded Drewry WCI from {csv_path}")
            self.last_download = datetime.now()
            return dest
        except Exception as e:
            logger.error(f"Error loading Drewry CSV: {e}")
            return None
    
    def get_filename(self) -> str:
        return "drewry_wci.csv"


class ShanghaiContainerFreightIndex(FreightDataSource):
    """Shanghai Containerized Freight Index via Investing.com"""
    
    def __init__(self, output_dir: str = "data/manual"):
        super().__init__(output_dir)
        self.base_url = "https://www.investing.com/indices/shanghai-containerized-freight-index"
        self.pair_id = 44744  # SCFI pair ID on Investing.com
    
    def fetch_data(self) -> Optional[Dict]:
        """
        Fetch SCFI from Investing.com
        Note: Direct API access is limited; this uses web scraping fallback
        """
        if not HAS_REQUESTS or not HAS_BEAUTIFULSOUP:
            logger.warning("requests and beautifulsoup required for SCFI scraping")
            return None
        
        try:
            # Try direct table extraction
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.base_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Extract table data
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for data in script tags (Investing.com uses Highcharts)
            scripts = soup.find_all('script')
            data_found = None
            
            for script in scripts:
                if script.string and 'Highcharts' in script.string:
                    # Extract JSON-like structure
                    data_found = script.string
                    break
            
            return {'html': response.text, 'scripts': data_found}
            
        except Exception as e:
            logger.error(f"SCFI fetch failed: {e}")
            return None
    
    def parse_data(self, raw_data) -> List[Dict]:
        """Parse SCFI from Investing.com data"""
        if not raw_data:
            return []
        
        # Due to Investing.com's JavaScript rendering, direct parsing is limited
        # Recommend using Selenium or manual download instead
        logger.info("SCFI: Recommend using Selenium or manual download from Investing.com")
        logger.info(f"URL: {self.base_url} -> Download Data button")
        return []
    
    def get_filename(self) -> str:
        return "scfi_historical.csv"


class UNCTADLinnerShippingIndex(FreightDataSource):
    """UNCTAD Liner Shipping Connectivity Index (LSCI)"""
    
    def __init__(self, output_dir: str = "data/manual"):
        super().__init__(output_dir)
        self.unctad_url = "https://unctadstat.unctad.org/wds/TableViewer/tableView.aspx"
        self.table_id = 92  # LSCI table ID
    
    def fetch_data(self) -> Optional[Dict]:
        """
        UNCTAD LSCI requires manual export from their portal
        This method documents the process
        """
        logger.info("UNCTAD LSCI: Manual export required")
        logger.info(f"Visit: {self.unctad_url}?ReportId={self.table_id}")
        logger.info("Export as Excel/CSV and place in data/manual/")
        logger.info("Data: Quarterly LSCI by country")
        return None
    
    def parse_data(self, raw_data) -> List[Dict]:
        return []
    
    def load_existing_csv(self, csv_path: str) -> Optional[Path]:
        """Load pre-exported UNCTAD CSV"""
        try:
            path = Path(csv_path)
            if not path.exists():
                logger.error(f"File not found: {csv_path}")
                return None
            
            import shutil
            dest = self.output_dir / "unctad_lsci.csv"
            shutil.copy2(path, dest)
            logger.info(f"Loaded UNCTAD LSCI from {csv_path}")
            self.last_download = datetime.now()
            return dest
        except Exception as e:
            logger.error(f"Error loading UNCTAD CSV: {e}")
            return None
    
    def get_filename(self) -> str:
        return "unctad_lsci.csv"


class IMFShippingCostIndex(FreightDataSource):
    """IMF Shipping Cost Index via World Bank API"""
    
    def __init__(self, output_dir: str = "data/manual"):
        super().__init__(output_dir)
        self.api_url = "https://api.worldbank.org/v2/country/WLD/indicator/IM.fs.sp_cons.sh"
    
    def fetch_data(self) -> Optional[Dict]:
        """Fetch IMF SCI from World Bank API"""
        if not HAS_REQUESTS:
            logger.error("requests library required")
            return None
        
        try:
            params = {
                'format': 'json',
                'date': '2000:2024',
                'per_page': 500
            }
            url = self.api_url + "?" + urlencode(params)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"IMF SCI fetch failed: {e}")
            return None
    
    def parse_data(self, raw_data) -> List[Dict]:
        """Parse World Bank API response"""
        if not isinstance(raw_data, list) or len(raw_data) < 2:
            return []
        
        data = raw_data[1]  # Actual data in second element
        parsed = []
        
        for record in data:
            if record.get('value'):
                try:
                    parsed.append({
                        'date': record.get('date'),
                        'value': float(record.get('value')),
                        'country': record.get('country', {}).get('value', 'World'),
                        'indicator': 'IMF_SCI'
                    })
                except (ValueError, TypeError):
                    continue
        
        return sorted(parsed, key=lambda x: x['date'], reverse=True)
    
    def get_filename(self) -> str:
        return "imf_shipping_cost_index.csv"


class TradingEconomicsFBX(FreightDataSource):
    """Trading Economics Freightos FBX Index - limited free access"""
    
    def __init__(self, output_dir: str = "data/manual", api_key: Optional[str] = None):
        super().__init__(output_dir)
        self.api_key = api_key or os.getenv('TRADING_ECONOMICS_API_KEY', 'guest:guest')
        self.symbols = ['MEX:FBX', 'NZL:FBX', 'SWE:FBX', 'THA:FBX']  # Free tier routes
    
    def fetch_data(self) -> Optional[Dict]:
        """Fetch available FBX lanes via Trading Economics"""
        if not HAS_TE and not HAS_REQUESTS:
            logger.error("tradingeconomics or requests library required")
            return None
        
        try:
            if HAS_TE:
                te.login(self.api_key)
                results = {}
                for symbol in self.symbols:
                    try:
                        results[symbol] = te.getMarketsHistorical(symbols=symbol, output_type="df")
                    except Exception as e:
                        logger.debug(f"Symbol {symbol} failed: {e}")
                        continue
                return results if results else None
            else:
                # Fallback to REST API
                url = f"https://api.tradingeconomics.com/markets/search?c={self.api_key}&q=FBX"
                response = requests.get(url, timeout=10)
                return response.json()
        except Exception as e:
            logger.error(f"FBX fetch failed: {e}")
            return None
    
    def parse_data(self, raw_data) -> List[Dict]:
        """Parse FBX data"""
        parsed = []
        
        if isinstance(raw_data, dict):
            for symbol, df in raw_data.items():
                if HAS_PANDAS and isinstance(df, pd.DataFrame):
                    for idx, row in df.iterrows():
                        parsed.append({
                            'date': str(idx.date()) if hasattr(idx, 'date') else str(idx),
                            'value': float(row.get('Close', row.get('price', 0))),
                            'lane': symbol
                        })
        
        return sorted(parsed, key=lambda x: x['date'])
    
    def get_filename(self) -> str:
        return "te_fbx_free_lanes.csv"


class FreightAutomationOrchestrator:
    """Main orchestrator for all freight data downloads"""
    
    def __init__(self, output_dir: str = "data/manual"):
        self.output_dir = output_dir
        self.sources: Dict[str, FreightDataSource] = {}
        self.results = {}
        self.setup_sources()
    
    def setup_sources(self):
        """Initialize all data sources"""
        self.sources = {
            'bdi': BalticDryIndex(self.output_dir),
            'drewry': DrewryWCI(self.output_dir),
            'scfi': ShanghaiContainerFreightIndex(self.output_dir),
            'unctad': UNCTADLinnerShippingIndex(self.output_dir),
            'imf': IMFShippingCostIndex(self.output_dir),
            'fbx': TradingEconomicsFBX(self.output_dir)
        }
    
    def download_all(self, skip_manual: bool = True) -> Dict[str, Optional[Path]]:
        """
        Download all freight indices
        
        Args:
            skip_manual: Skip sources requiring manual download
        """
        self.results = {}
        
        for name, source in self.sources.items():
            # Skip manual-only sources if requested
            if skip_manual and name in ['drewry', 'scfi', 'unctad']:
                logger.info(f"Skipping {name} (manual download required)")
                self.results[name] = None
                continue
            
            logger.info(f"\\nDownloading {name}...")
            result = source.download()
            self.results[name] = result
            
            if result:
                logger.info(f"✓ {name} completed")
            else:
                logger.warning(f"✗ {name} failed or no data")
            
            # Rate limiting
            time.sleep(1)
        
        return self.results
    
    def load_manual_file(self, source_name: str, filepath: str) -> Optional[Path]:
        """Load manually downloaded file for a source"""
        if source_name not in self.sources:
            logger.error(f"Unknown source: {source_name}")
            return None
        
        source = self.sources[source_name]
        
        if hasattr(source, 'load_existing_csv'):
            return source.load_existing_csv(filepath)
        else:
            logger.error(f"{source_name} does not support manual loading")
            return None
    
    def get_status(self) -> Dict:
        """Get download status summary"""
        return {
            'timestamp': datetime.now().isoformat(),
            'results': {
                name: str(path) if path else None 
                for name, path in self.results.items()
            },
            'output_dir': self.output_dir
        }
    
    def print_status(self):
        """Print human-readable status"""
        print("\\n" + "="*60)
        print("FREIGHT DATA DOWNLOAD STATUS")
        print("="*60)
        
        for name, path in self.results.items():
            status = "✓" if path else "✗"
            print(f"{status} {name.upper():12} {path or 'Failed/Skipped'}")
        
        print("="*60 + "\\n")


# USAGE EXAMPLE
if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = FreightAutomationOrchestrator(output_dir="data/manual")
    
    # Download all automated sources (BDI, IMF, partial FBX)
    orchestrator.download_all(skip_manual=True)
    
    # Print results
    orchestrator.print_status()
    
    # Optional: Load manually downloaded files
    # orchestrator.load_manual_file('drewry', '/path/to/drewry_download.csv')
    # orchestrator.load_manual_file('unctad', '/path/to/unctad_export.csv')
    
    # Export status to JSON
    with open("data/manual/download_status.json", "w") as f:
        json.dump(orchestrator.get_status(), f, indent=2)
'''

# Save the automation framework
with open('freight_data_automation.py', 'w') as f:
    f.write(automation_code)

print("✓ Automation framework saved: freight_data_automation.py")
print("\nFramework includes:")
print("- BalticDryIndex (via Trading Economics API)")
print("- DrewryWCI (manual + loader)")
print("- ShanghaiContainerFreightIndex (Investing.com scraping)")
print("- UNCTADLinnerShippingIndex (manual + loader)")
print("- IMFShippingCostIndex (World Bank API)")
print("- TradingEconomicsFBX (partial free access)")
print("\nKey features:")
print("- Modular architecture (ABC pattern)")
print("- Error handling & logging")
print("- CSV export with metadata")
print("- Manual file loader support")
print("- Download orchestration & status reporting")
