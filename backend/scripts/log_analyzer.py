"""
Log analyzer for forecasting system.
Analyzes logs and generates insights.
"""
import sys
from pathlib import Path
from datetime import datetime
import json
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class LogAnalyzer:
    """Analyze system logs."""
    
    def __init__(self, log_dir='logs'):
        """Initialize analyzer."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
    
    def analyze_forecast_logs(self):
        """Analyze forecast execution logs."""
        log_files = list(self.log_dir.glob('forecast_run_*.json'))
        
        if not log_files:
            return {'error': 'No forecast logs found'}
        
        # Analyze latest log
        latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
        
        with open(latest_log, 'r') as f:
            log_data = json.load(f)
        
        analysis = {
            'latest_run': latest_log.stem,
            'timestamp': log_data.get('timestamp'),
            'items_processed': log_data.get('items_processed', 0),
            'items_with_alerts': log_data.get('items_with_alerts', 0),
            'total_alerts': log_data.get('total_alerts', 0),
            'training_performed': log_data.get('training_performed', False)
        }
        
        return analysis
    
    def analyze_all_logs(self):
        """Analyze all available logs."""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'forecast_logs': len(list(self.log_dir.glob('forecast_run_*.json'))),
            'health_checks': len(list(self.log_dir.glob('health_check_*.json'))),
            'latest_forecast': None,
            'latest_health': None
        }
        
        forecast_logs = list(self.log_dir.glob('forecast_run_*.json'))
        if forecast_logs:
            latest = max(forecast_logs, key=lambda p: p.stat().st_mtime)
            with open(latest, 'r') as f:
                analysis['latest_forecast'] = json.load(f)
        
        health_logs = list(self.log_dir.glob('health_check_*.json'))
        if health_logs:
            latest = max(health_logs, key=lambda p: p.stat().st_mtime)
            with open(latest, 'r') as f:
                analysis['latest_health'] = json.load(f)
        
        return analysis
    
    def print_summary(self, analysis):
        """Print analysis summary."""
        print("\n" + "="*60)
        print("Log Analysis Summary")
        print("="*60)
        print(f"\nTimestamp: {analysis['timestamp']}")
        print(f"\nForecast Logs: {analysis['forecast_logs']}")
        print(f"Health Checks: {analysis['health_checks']}")
        
        if analysis['latest_forecast']:
            latest = analysis['latest_forecast']
            print("\n--- Latest Forecast Run ---")
            print(f"Items Processed: {latest.get('items_processed', 0)}")
            print(f"Items with Alerts: {latest.get('items_with_alerts', 0)}")
            print(f"Total Alerts: {latest.get('total_alerts', 0)}")
        
        if analysis['latest_health']:
            health = analysis['latest_health']
            print("\n--- Latest Health Check ---")
            print(f"Status: {health['health']['status'].upper()}")
        
        print("\n" + "="*60)


def main():
    """Main execution."""
    analyzer = LogAnalyzer()
    analysis = analyzer.analyze_all_logs()
    analyzer.print_summary(analysis)
    
    # Save analysis
    output_file = analyzer.log_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\nAnalysis saved: {output_file}")


if __name__ == '__main__':
    main()

