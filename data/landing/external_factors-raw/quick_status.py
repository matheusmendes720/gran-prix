#!/usr/bin/env python3
"""
Quick External Factors Status Check
Simple status monitoring without Unicode issues
"""

import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json

def quick_status_check():
    """Quick status check of external factors"""
    print("EXTERNAL FACTORS STATUS CHECK")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    base_dir = Path('.')
    
    # Check key data categories
    categories = {
        'Economic Data': {
            'files': ['macro/bacen/ptax/usd/ptax.json', 'macro/bacen/selic/selic.json', 'macro/ibge/ipca/ipca.json'],
            'status': 'Checking...'
        },
        'Market Data': {
            'files': ['global/worldbank/gdp_current_usd/*/gdp_current_usd.json'],
            'status': 'Checking...'
        },
        'Commodities': {
            'files': ['commodities/*/20251111/*.csv'],
            'status': 'Checking...'
        },
        'Logistics': {
            'files': ['logistics/anp_fuel/*/anp_fuel.csv', 'logistics/baltic_dry/*/baltic_dry.csv'],
            'status': 'Checking...'
        },
        'Climate': {
            'files': ['inmet/202*/INMET_*.CSV', 'openweather/20251111/brazil_weather_expanded.csv'],
            'status': 'Checking...'
        }
    }
    
    total_files = 0
    total_found = 0
    
    for category, info in categories.items():
        found = 0
        for file_pattern in info['files']:
            try:
                import glob
                matches = list(base_dir.glob(file_pattern))
                if matches:
                    found += len(matches)
            except:
                pass
        total_files += len(info['files'])
        total_found += found
        
        if found == len(info['files']):
            status = "✅ COMPLETE"
        elif found > 0:
            status = f"🟡 PARTIAL ({found}/{len(info['files'])})"
        else:
            status = "❌ MISSING"
        
        categories[category]['status'] = status
        categories[category]['found'] = found
        categories[category]['total'] = len(info['files'])
        
        print(f"{category: {status}")
    
    print()
    print("SUMMARY:")
    print(f"Total Files: {total_found}/{total_files}")
    print(f"Overall Coverage: {(total_found/total_files)*100:.1f}%")
    
    # ML Readiness assessment
    critical_categories = ['Economic Data', 'Commodities', 'Climate']
    critical_found = sum(1 for cat in critical_categories if categories[cat]['found'] > 0)
    critical_total = len(critical_categories)
    
    ml_readiness = (critical_found / critical_total) * 100
    if ml_readiness >= 75:
        readiness_status = "✅ READY FOR ML"
    elif ml_readiness >= 50:
        readiness_status = "🟡 MOSTLY READY"
    else:
        readiness_status = "❌ NEEDS WORK"
    
    print()
    print(f"ML Readiness: {readiness_status}")
    print(f"Critical Coverage: {critical_found}/{critical_total}")
    
    # Recent data activity
    print()
    print("RECENT ACTIVITY:")
    today_dir = base_dir / datetime.now().strftime('%Y%m%d')
    if today_dir.exists():
        csv_files = list(today_dir.glob('*.csv'))
        json_files = list(today_dir.glob('*.json'))
        
        total_activity = len(csv_files) + len(json_files)
        if total_activity > 0:
            print(f"✅ Today's activity: {total_activity} files")
        else:
            print("- No new files today")
    
    # Quick recommendations
    print()
    print("QUICK ACTIONS:")
    if total_found < total_files * 0.8:
        print("1. Run missing data downloaders")
        print("2. Check API availability")
        print("3. Validate data quality")
    else:
        print("1. Data is current")
        print("2. ML pipeline ready")
        print("3. Monitor for updates")
    
    # Save simple status
    status_data = {
        'timestamp': datetime.now().isoformat(),
        'categories': categories,
        'summary': {
            'total_files': total_files,
            'total_found': total_found,
            'coverage_percent': (total_found/total_files)*100,
            'ml_readiness': ml_readiness,
            'critical_found': critical_found,
            'critical_total': critical_total
        }
    }
    
    status_file = base_dir / 'quick_status.json'
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, indent=2)
    
    print(f"Status saved to: {status_file}")
    print()
    print("EXTERNAL FACTORS CHECK COMPLETED")
    print("=" * 50)
    
    return status_data

if __name__ == "__main__":
    quick_status_check()