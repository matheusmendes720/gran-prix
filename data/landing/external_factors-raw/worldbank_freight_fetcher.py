"""
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
