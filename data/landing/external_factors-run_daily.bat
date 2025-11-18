# Daily Automation Runner
# Schedules and maintains external factors dataset

echo "EXTERNAL FACTORS DAILY AUTOMATION RUNNER"
echo "======================================"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Set directory
cd "D:\codex\datamaster\senai\gran_prix\data\landing\external_factors-raw"

# Step 1: Run quick status check
echo "STEP 1: STATUS CHECK"
python quick_status.py
echo ""

# Step 2: Generate fresh data if needed
echo "STEP 2: DATA REFRESH"
echo "Checking if fresh data needed..."

# Check today's folder
TODAY=$(date +%Y%m%d)
if [ ! -d "$TODAY" ] || [ $(find "$TODAY" -name "*.csv" | wc -l) -lt 5 ]; then
    echo "Running complete external downloader..."
    python complete_external_downloader.py
else
    echo "Today's data exists ($(find "$TODAY" -name "*.csv" | wc -l) files)"
fi
echo ""

# Step 3: Validate data quality
echo "STEP 3: QUALITY VALIDATION"
python -c "
import pandas as pd
from pathlib import Path
import json

today = '$TODAY'
base_dir = Path('.')
today_dir = base_dir / today

if today_dir.exists():
    csv_files = list(today_dir.glob('*.csv'))
    print(f'Validating {len(csv_files)} files...')
    
    quality_issues = 0
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            if null_pct > 10:
                print(f'  ! {csv_file.name}: HIGH NULLS ({null_pct:.1f}%)')
                quality_issues += 1
            elif null_pct > 5:
                print(f'  ~ {csv_file.name}: SOME NULLS ({null_pct:.1f}%)')
            else:
                print(f'  + {csv_file.name}: GOOD QUALITY')
        except:
            print(f'  x {csv_file.name}: ERROR READING')
            quality_issues += 1
    
    if quality_issues == 0:
        print('✅ All files have good quality')
    elif quality_issues < len(csv_files) / 2:
        print('~ Most files have good quality')
    else:
        print('! Multiple quality issues detected')
else:
    print('No data to validate')
"
echo ""

# Step 4: Update status documentation
echo "STEP 4: UPDATE STATUS"
cat > STATUS_UPDATE.md << EOF
# External Factors Daily Status Update
**Date:** $(date '+%Y-%m-%d')
**Time:** $(date '+%H:%M:%S')
**Status:** MAINTENANCE RUNNING

## Recent Activity
- Daily automation executed
- Data quality validation performed
- Fresh data generation if needed

## Current Dataset Health
$(python quick_status.py 2>/dev/null | tail -10)

## Next Actions
- Monitor data quality metrics
- Check API rate limits
- Prepare ML integration refresh

---

*Automated update by maintenance runner*
EOF

echo "Status documentation updated"
echo ""

# Step 5: Schedule next run
echo "STEP 5: SCHEDULING NEXT RUN"
NEXT_RUN=$(date -d "tomorrow 09:00" '+%Y-%m-%d %H:%M')
echo "Next scheduled run: $NEXT_RUN"

# Create tomorrow's task file (for demonstration)
cat > schedule_next.txt << EOF
# Tomorrow's Maintenance Schedule
# Date: $(date -d "tomorrow" '+%Y-%m-%d')
# Time: 09:00
# Tasks:
# 1. Run complete external downloader
# 2. Validate all data sources
# 3. Check API rate limits
# 4. Generate quality report
# 5. Update ML integration pipeline

echo "Next maintenance scheduled for $NEXT_RUN"
echo ""

echo "DAILY AUTOMATION COMPLETED"
echo "======================================"
echo "Finished: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Next run: $NEXT_RUN"
echo ""