#!/usr/bin/env python3
"""
Simple External Factors Quick Status
Minimal status without Unicode complications
"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json

def quick_status():
    """Quick status without Unicode issues"""
    print("EXTERNAL FACTORS QUICK STATUS")
    print("=" * 50)
    
    base_dir = Path('.')
    
    # Check key data sources
    data_sources = {
        'Economic': {
            'files': ['macro/bacen/ptax/usd', 'macro/bacen/selic', 'macro/ibge/ipca'],
            'found': 0
        },
        'Global': {
            'files': ['global/worldbank/gdp_current_usd'],
            'found': 0
        },
        'Commodities': {
            'files': ['commodities/20251111/*.csv'],
            'found': 0
        },
        'Market': {
            'files': ['market_indices/20251111/*.csv'],
            'found': 0
        },
        'Energy': {
            'files': ['energy/20251111/*.csv'],
            'found': 0
        },
        'Climate': {
            'files': ['inmet/2025/INMET_*.CSV', 'openweather/20251111/brazil_weather_expanded.csv'],
            'found': 0
        },
        'Logistics': {
            'files': ['logistics/anp_fuel/*/anp_fuel.csv', 'logistics/baltic_dry/*/baltic_dry.csv'],
            'found': 0
        }
    }
    
    total_files = 0
    total_found = 0
    
    print("CHECKING DATA SOURCES...")
    
    for category, info in data_sources.items():
        found = 0
        for file_pattern in info['files']:
            try:
                import glob
                matches = list(base_dir.glob(file_pattern))
                if matches:
                    found += len(matches)
            except:
                pass
        
        info['found'] = found
        total_files += len(info['files'])
        total_found += found
        
        if found == len(info['files']):
            status = "COMPLETE"
        elif found > 0:
            status = f"PARTIAL ({found}/{len(info['files'])})"
        else:
            status = "MISSING"
        
        print(f"{status:10} {category}: {status}")
    
    print()
    print(f"SUMMARY:")
    print(f"Total Sources: {total_found}/{total_files}")
    print(f"Coverage: {(total_found/total_files)*100:.1f}%")
    
    # ML readiness check
    critical_categories = ['Economic', 'Commodities', 'Market', 'Climate']
    critical_found = sum(1 for cat in critical_categories if data_sources[cat]['found'] > 0)
    critical_total = len(critical_categories)
    
    ml_ready = (critical_found / critical_total) * 100
    if ml_ready >= 75:
        readiness = "READY FOR ML"
        emoji = "✅"
    elif ml_ready >= 50:
        readiness = "MOSTLY READY"
        emoji = "🟡"
    else:
        readiness = "NEEDS WORK"
        emoji = "❌"
    
    print()
    print(f"ML READINESS: {readiness}")
    print(f"Critical Coverage: {critical_found}/{critical_total}")
    
    # Today's data
    today = datetime.now().strftime("%Y%m%d")
    today_dir = base_dir / today
    if today_dir.exists():
        csv_files = list(today_dir.glob("*.csv"))
        if csv_files:
            print(f"TODAY'S DATA: {len(csv_files)} files")
        else:
            print("TODAY'S DATA: No new files")
    else:
        print(f"TODAY'S DATA: Directory {today} not found")
    
    # Quick actions
    print()
    print("QUICK ACTIONS:")
    if total_found < total_files * 0.8:
        print("1. Run missing data downloaders")
        print("2. Check API availability")
        print("3. Validate data quality")
    else:
        print("1. Run transformation scripts")
        print("2. Start ML integration")
        print("3. Monitor for updates")
    
    # Save status
    status_data = {
        'timestamp': datetime.now().isoformat(),
        'sources': data_sources,
        'summary': {
            'total_files': total_files,
            'total_found': total_found,
            'coverage_percent': (total_found/total_files)*100,
            'ml_ready': ml_ready,
            'critical_found': critical_found,
            'critical_total': critical_total
        }
    }
    
    status_file = base_dir / 'quick_status.json'
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"Status saved to: {status_file}")
    print("QUICK STATUS CHECK COMPLETED")
    
    return status_data

if __name__ == "__main__":
    quick_status()