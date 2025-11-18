# External Factors Daily Runner
# Cross-platform automation for external factors maintenance

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_command(description, command, cwd=None):
    """Run a command with proper error handling"""
    print(f"\n=== {description} ===")
    try:
        if cwd:
            result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Errors:\n{result.stderr}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Main daily automation runner"""
    print("EXTERNAL FACTORS DAILY AUTOMATION RUNNER")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    # Step 1: Status check
    success = run_command(
        "STATUS CHECK",
        [sys.executable, "quick_status.py"]
    )
    
    # Step 2: Generate fresh data if needed
    today_dir = base_dir / datetime.now().strftime("%Y%m%d")
    csv_files = list(today_dir.glob("*.csv")) if today_dir.exists() else []
    
    if len(csv_files) < 10:  # Need fresh data
        success &= run_command(
            "DATA REFRESH",
            [sys.executable, "complete_external_downloader.py"]
        )
    else:
        print("DATA REFRESH: Already sufficient data")
    
    # Step 3: Quality validation
    success &= run_command(
        "QUALITY VALIDATION", 
        ["python", "-c", """
import pandas as pd
from pathlib import Path
from datetime import datetime

base_dir = Path('.')
today_dir = base_dir / datetime.now().strftime('%Y%m%d')

if today_dir.exists():
    csv_files = list(today_dir.glob('*.csv'))
    total_nulls = 0
    total_records = 0
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            total_nulls += df.isnull().sum().sum()
            total_records += len(df)
            print(f'✅ {csv_file.name}: {len(df)} records, {total_nulls} nulls')
        except Exception as e:
            print(f'❌ {csv_file.name}: Error {e}')
    
    null_rate = (total_nulls / (total_records * len(csv_files))) * 100 if csv_files else 0
    print(f'\\nQUALITY: {null_rate:.1f}% null rate ({total_nulls}/{total_records * len(csv_files)} cells)')
else:
    print('NO DATA FOR QUALITY CHECK')
"""]
    )
    
    # Step 4: Generate daily report
    success &= run_command(
        "DAILY REPORT",
        ["python", "-c", f"""
import json
from datetime import datetime
from pathlib import Path

base_dir = Path('.')
today_dir = base_dir / datetime.now().strftime('%Y%m%d')

report = {{
    'maintenance_date': datetime.now().isoformat(),
    'status': 'COMPLETED',
    'csv_files': len(list(today_dir.glob('*.csv'))) if today_dir.exists() else 0,
    'quality_status': 'CHECKED',
    'next_run': (datetime.now().replace(hour=9, minute=0)).isoformat()
}}

report_file = base_dir / 'daily_report.json'
with open(report_file, 'w', encoding='utf-8', errors='replace') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f'Daily report saved to: {{report_file.name}}')
print(f'Next maintenance: {{report[\"next_run\"]}}')
"""]
    )
    
    # Step 5: Schedule next run
    tomorrow_9am = datetime.now().replace(hour=9, minute=0, second=0)
    if tomorrow_9am <= datetime.now():
        tomorrow_9am = tomorrow_9am + timedelta(days=1)
    
    print(f"\n=== SCHEDULING ===")
    print(f"Next run scheduled for: {tomorrow_9am.strftime('%Y-%m-%d %H:%M')}")
    
    print("\n=== DAILY AUTOMATION COMPLETED ===")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Next run: {tomorrow_9am.strftime('%Y-%m-%d %H:%M')}")
    
    return success

if __name__ == "__main__":
    main()