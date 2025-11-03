#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone script to run external API reliability tests
Tests all public APIs with retry logic and error handling
"""
import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import requests
from datetime import date, timedelta
from time import time
import statistics
from typing import Dict, List, Any

# Import configs directly
try:
    from config.external_apis_config import (
        INMET_CONFIG,
        BACEN_CONFIG,
        ANATEL_CONFIG,
        OPENWEATHER_CONFIG,
    )
except ImportError:
    # Try backend prefix
    from backend.config.external_apis_config import (
        INMET_CONFIG,
        BACEN_CONFIG,
        ANATEL_CONFIG,
        OPENWEATHER_CONFIG,
    )


class APIReliabilityTester:
    """Test API reliability with metrics"""
    
    def __init__(self):
        self.results: Dict[str, Any] = {}
    
    def test_api_with_retries(self, name: str, url: str, params: Dict = None, 
                              method: str = 'GET', max_retries: int = 3, timeout: int = 15) -> Dict:
        """Test API with retry logic and collect metrics"""
        start_time = time()
        success = False
        status_code = None
        error = None
        response_times = []
        attempts = 0
        
        for attempt in range(max_retries):
            attempts = attempt + 1
            try:
                request_start = time()
                
                if method == 'GET':
                    response = requests.get(url, params=params, timeout=timeout)
                else:
                    response = requests.post(url, json=params, timeout=timeout)
                
                request_time = time() - request_start
                response_times.append(request_time)
                status_code = response.status_code
                
                # Check if successful (200-299)
                if 200 <= status_code < 300:
                    success = True
                    break
                elif status_code in [400, 401, 403, 404]:
                    # Client errors - don't retry
                    error = f"Client error: {status_code}"
                    break
                else:
                    # Server errors - retry
                    if attempt < max_retries - 1:
                        print(f"  ⚠️ {name} returned {status_code}, retrying ({attempt + 1}/{max_retries})...")
                        continue
                    error = f"Server error: {status_code}"
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"  ⚠️ {name} timeout, retrying ({attempt + 1}/{max_retries})...")
                    continue
                error = "Timeout"
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    print(f"  ⚠️ {name} connection error, retrying ({attempt + 1}/{max_retries})...")
                    continue
                error = f"Connection error: {str(e)}"
            except requests.exceptions.RequestException as e:
                error = f"Request error: {str(e)}"
                break
        
        total_time = time() - start_time
        
        result = {
            'name': name,
            'url': url,
            'success': success,
            'status_code': status_code,
            'error': error,
            'total_time': total_time,
            'avg_response_time': statistics.mean(response_times) if response_times else None,
            'min_response_time': min(response_times) if response_times else None,
            'max_response_time': max(response_times) if response_times else None,
            'attempts': attempts,
        }
        
        self.results[name] = result
        return result
    
    def print_results(self):
        """Print test results summary"""
        print("\n" + "=" * 70)
        print("API RELIABILITY TEST RESULTS")
        print("=" * 70)
        
        successful = []
        failed = []
        
        for name, result in self.results.items():
            if result['success']:
                successful.append(result)
                print(f"\n[PASS] {name}")
                print(f"   Status: {result['status_code']}")
                if result['avg_response_time']:
                    print(f"   Response Time: {result['avg_response_time']:.3f}s (avg)")
                print(f"   Attempts: {result['attempts']}")
            else:
                failed.append(result)
                print(f"\n[FAIL] {name}")
                print(f"   Error: {result['error']}")
                if result['status_code']:
                    print(f"   Status Code: {result['status_code']}")
                print(f"   Attempts: {result['attempts']}")
        
        print("\n" + "=" * 70)
        print(f"Summary: {len(successful)}/{len(self.results)} APIs successful")
        
        if successful:
            avg_response_time = statistics.mean([r['avg_response_time'] for r in successful if r['avg_response_time']])
            print(f"Average Response Time: {avg_response_time:.3f}s")
        
        print("=" * 70 + "\n")


def test_all_apis():
    """Test all external APIs"""
    tester = APIReliabilityTester()
    
    print("Starting External API Reliability Tests...")
    print("=" * 70)
    
    # Test INMET API
    print("\n[INMET] Testing INMET API...")
    base_url = INMET_CONFIG['base_url']
    # Try different INMET endpoints
    inmet_endpoints = [
        (base_url, "INMET Base URL"),
        (f"{base_url}condicoesEstacao/", "INMET Station Conditions"),
        (f"{base_url}estacao/", "INMET Stations"),
        ("https://tempo.inmet.gov.br/", "INMET Weather Portal"),
    ]
    
    for url, name in inmet_endpoints:
        result = tester.test_api_with_retries(
            name=name,
            url=url,
            max_retries=2,
            timeout=10
        )
        # If any endpoint works, consider INMET working
        if result['success']:
            break
    
    # Test BACEN API - all series
    print("\n[BACEN] Testing BACEN API...")
    series_to_test = {
        'IPCA': BACEN_CONFIG['series_codes']['ipca'],
        'SELIC': BACEN_CONFIG['series_codes']['selic'],
        'Exchange Rate': BACEN_CONFIG['series_codes']['exchange_rate'],
        'GDP': BACEN_CONFIG['series_codes']['gdp'],
    }
    
    for series_name, series_code in series_to_test.items():
        url = f"{BACEN_CONFIG['base_url']}{series_code}/dados"
        params = {
            'formato': 'json',
            'dataInicial': '01/01/2024',
            'dataFinal': '31/12/2024'
        }
        
        tester.test_api_with_retries(
            name=f"BACEN {series_name}",
            url=url,
            params=params,
            max_retries=3,
            timeout=15
        )
    
    # Test ANATEL Website
    print("\n[ANATEL] Testing ANATEL Website...")
    base_url = ANATEL_CONFIG['base_url']
    tester.test_api_with_retries(
        name="ANATEL Website",
        url=base_url,
        max_retries=3,
        timeout=10
    )
    
    # Test OpenWeatherMap if key is configured
    api_key = OPENWEATHER_CONFIG.get('api_key')
    if api_key:
        print("\n[OpenWeatherMap] Testing OpenWeatherMap API...")
        city = OPENWEATHER_CONFIG.get('city', 'Salvador,BR')
        url = f"{OPENWEATHER_CONFIG['base_url']}weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        
        tester.test_api_with_retries(
            name="OpenWeatherMap API",
            url=url,
            params=params,
            max_retries=3,
            timeout=10
        )
    else:
        print("\n[OpenWeatherMap] API: Skipped (API key not configured)")
    
    # Print results
    tester.print_results()
    
    # Return success count
    successful = [r for r in tester.results.values() if r['success']]
    return len(successful), len(tester.results)


if __name__ == '__main__':
    try:
        successful, total = test_all_apis()
        print(f"\n[SUCCESS] Test Complete: {successful}/{total} APIs successful")
        
        # Exit with appropriate code
        if successful == 0:
            sys.exit(1)
        elif successful < total:
            sys.exit(2)  # Partial success
        else:
            sys.exit(0)  # All successful
            
    except KeyboardInterrupt:
        print("\n\n[WARNING] Tests interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERROR] Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

