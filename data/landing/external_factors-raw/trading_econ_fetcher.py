"""
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
