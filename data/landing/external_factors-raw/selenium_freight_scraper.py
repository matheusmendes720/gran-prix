"""
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
