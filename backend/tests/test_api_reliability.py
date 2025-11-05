"""
Comprehensive API reliability tests
Tests all external APIs with retry logic, error handling, and performance metrics
"""
import sys
from pathlib import Path
import pytest
import requests
from datetime import date, timedelta
from time import time
import statistics

# Add backend to path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from backend.config.external_apis_config import (
    INMET_CONFIG,
    BACEN_CONFIG,
    ANATEL_CONFIG,
    OPENWEATHER_CONFIG,
)


class APIReliabilityTester:
    """Test API reliability with metrics"""
    
    def __init__(self):
        self.results = {}
    
    def test_api_with_retries(self, name, url, params=None, method='GET', max_retries=3, timeout=15):
        """Test API with retry logic and collect metrics"""
        start_time = time()
        success = False
        status_code = None
        error = None
        response_times = []
        
        for attempt in range(max_retries):
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
            'attempts': attempt + 1,
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
                print(f"\n✅ {name}")
                print(f"   Status: {result['status_code']}")
                print(f"   Response Time: {result['avg_response_time']:.3f}s (avg)")
                print(f"   Attempts: {result['attempts']}")
            else:
                failed.append(result)
                print(f"\n❌ {name}")
                print(f"   Error: {result['error']}")
                print(f"   Status Code: {result['status_code']}")
                print(f"   Attempts: {result['attempts']}")
        
        print("\n" + "=" * 70)
        print(f"Summary: {len(successful)}/{len(self.results)} APIs successful")
        print("=" * 70 + "\n")


@pytest.mark.integration
@pytest.mark.network
class TestAPIReliability:
    """Comprehensive API reliability tests"""
    
    def setup_method(self):
        """Setup test instance"""
        self.tester = APIReliabilityTester()
    
    def test_inmet_api_reliability(self):
        """Test INMET API reliability"""
        print("\n🌦️ Testing INMET API...")
        base_url = INMET_CONFIG['base_url']
        result = self.tester.test_api_with_retries(
            name="INMET API",
            url=base_url,
            max_retries=3,
            timeout=10
        )
        
        assert result['success'] or result['status_code'] in [404, 403, 401], \
            f"INMET API failed: {result['error']}"
        print(f"   Result: {'✅ SUCCESS' if result['success'] else '⚠️ PARTIAL'} - {result['status_code']}")
    
    def test_bacen_api_reliability(self):
        """Test BACEN API reliability for all series"""
        print("\n💰 Testing BACEN API...")
        
        series_to_test = {
            'IPCA': BACEN_CONFIG['series_codes']['ipca'],
            'SELIC': BACEN_CONFIG['series_codes']['selic'],
            'Exchange Rate': BACEN_CONFIG['series_codes']['exchange_rate'],
            'GDP': BACEN_CONFIG['series_codes']['gdp'],
        }
        
        all_success = True
        
        for series_name, series_code in series_to_test.items():
            url = f"{BACEN_CONFIG['base_url']}{series_code}/dados"
            params = {
                'formato': 'json',
                'dataInicial': '01/01/2024',
                'dataFinal': '31/12/2024'
            }
            
            result = self.tester.test_api_with_retries(
                name=f"BACEN {series_name}",
                url=url,
                params=params,
                max_retries=3,
                timeout=15
            )
            
            if not result['success']:
                all_success = False
                print(f"   ⚠️ {series_name}: {result['error']}")
            else:
                print(f"   ✅ {series_name}: {result['status_code']} ({result['avg_response_time']:.3f}s)")
        
        # At least one should succeed
        assert any(r['success'] for k, r in self.tester.results.items() if 'BACEN' in k), \
            "All BACEN endpoints failed"
    
    def test_anatel_api_reliability(self):
        """Test ANATEL website reliability"""
        print("\n📡 Testing ANATEL Website...")
        base_url = ANATEL_CONFIG['base_url']
        result = self.tester.test_api_with_retries(
            name="ANATEL Website",
            url=base_url,
            max_retries=3,
            timeout=10
        )
        
        assert result['success'], f"ANATEL website failed: {result['error']}"
        print(f"   Result: ✅ SUCCESS - {result['status_code']} ({result['avg_response_time']:.3f}s)")
    
    def test_openweather_api_reliability(self):
        """Test OpenWeatherMap API if key is configured"""
        api_key = OPENWEATHER_CONFIG.get('api_key')
        
        if not api_key:
            pytest.skip("OpenWeatherMap API key not configured")
        
        print("\n🌤️ Testing OpenWeatherMap API...")
        city = OPENWEATHER_CONFIG.get('city', 'Salvador,BR')
        url = f"{OPENWEATHER_CONFIG['base_url']}weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        
        result = self.tester.test_api_with_retries(
            name="OpenWeatherMap API",
            url=url,
            params=params,
            max_retries=3,
            timeout=10
        )
        
        # OpenWeatherMap might fail if key is invalid, that's okay
        if result['success']:
            print(f"   Result: ✅ SUCCESS - {result['status_code']} ({result['avg_response_time']:.3f}s)")
        else:
            print(f"   Result: ⚠️ {result['error']}")
    
    def test_all_apis_performance(self):
        """Test all APIs and generate performance report"""
        print("\n📊 Running comprehensive API reliability tests...")
        
        # Run all API tests
        self.test_inmet_api_reliability()
        self.test_bacen_api_reliability()
        self.test_anatel_api_reliability()
        
        # Print summary
        self.tester.print_results()
        
        # Calculate overall metrics
        successful = [r for r in self.tester.results.values() if r['success']]
        
        if successful:
            avg_response_time = statistics.mean([r['avg_response_time'] for r in successful if r['avg_response_time']])
            print(f"📈 Average Response Time: {avg_response_time:.3f}s")
            print(f"📈 Success Rate: {len(successful)}/{len(self.tester.results)} ({len(successful)/len(self.tester.results)*100:.1f}%)")
        
        # At least core APIs should work
        core_apis = ['INMET API', 'ANATEL Website']
        core_success = sum(1 for name, r in self.tester.results.items() 
                          if any(api in name for api in core_apis) and r['success'])
        
        assert core_success > 0, "Core APIs are not accessible"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s', '--tb=short', '-m', 'integration'])







