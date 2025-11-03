"""
System monitoring and health check script.
Monitors forecasting system health and performance.
"""
import sys
from pathlib import Path
from datetime import datetime
import json
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demand_forecasting.utils.config import Config
from demand_forecasting.utils.model_persistence import ModelPersistence
from demand_forecasting.data.loader import DataLoader
import warnings
warnings.filterwarnings('ignore')


class SystemMonitor:
    """Monitor system health and performance."""
    
    def __init__(self):
        """Initialize monitor."""
        self.config = Config()
        self.model_persistence = ModelPersistence()
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
    
    def check_data_availability(self):
        """Check if data files are available."""
        data_path = self.config.get('data.path', 'data/nova_corrente_demand.csv')
        data_file = Path(data_path)
        
        return {
            'available': data_file.exists(),
            'path': str(data_file),
            'size_mb': data_file.stat().st_size / (1024 * 1024) if data_file.exists() else 0
        }
    
    def check_models(self):
        """Check trained models."""
        models = self.model_persistence.list_models()
        
        return {
            'count': len(models),
            'models': [Path(m).stem for m in models[:10]]  # First 10
        }
    
    def check_system_health(self):
        """Perform complete health check."""
        health = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'checks': {}
        }
        
        # Check data
        data_check = self.check_data_availability()
        health['checks']['data'] = data_check
        if not data_check['available']:
            health['status'] = 'degraded'
        
        # Check models
        models_check = self.check_models()
        health['checks']['models'] = models_check
        if models_check['count'] == 0:
            health['status'] = 'warning'
        
        # Check directories
        dirs_check = {
            'reports': Path('reports').exists(),
            'models': Path('models').exists(),
            'data': Path('data').exists(),
            'logs': Path('logs').exists()
        }
        health['checks']['directories'] = dirs_check
        
        # Overall status
        if health['status'] == 'healthy' and not all(dirs_check.values()):
            health['status'] = 'warning'
        
        return health
    
    def generate_report(self):
        """Generate monitoring report."""
        health = self.check_system_health()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'health': health,
            'recommendations': []
        }
        
        # Add recommendations
        if not health['checks']['data']['available']:
            report['recommendations'].append(
                'Data file not found. Create sample data or provide data file.'
            )
        
        if health['checks']['models']['count'] == 0:
            report['recommendations'].append(
                'No trained models found. Run training script: python scripts/train_models.py'
            )
        
        if not health['checks']['directories']['reports']:
            report['recommendations'].append(
                'Reports directory missing. It will be created on first forecast run.'
            )
        
        return report
    
    def save_report(self, report):
        """Save monitoring report."""
        report_file = self.log_dir / f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def print_report(self, report):
        """Print monitoring report."""
        print("\n" + "="*60)
        print("System Health Check")
        print("="*60)
        print(f"\nTimestamp: {report['timestamp']}")
        print(f"Overall Status: {report['health']['status'].upper()}")
        
        print("\n--- Data Availability ---")
        data = report['health']['checks']['data']
        print(f"Available: {'Yes' if data['available'] else 'No'}")
        if data['available']:
            print(f"Path: {data['path']}")
            print(f"Size: {data['size_mb']:.2f} MB")
        
        print("\n--- Trained Models ---")
        models = report['health']['checks']['models']
        print(f"Count: {models['count']}")
        if models['count'] > 0:
            print(f"Examples: {', '.join(models['models'][:5])}")
        
        print("\n--- Directories ---")
        dirs = report['health']['checks']['directories']
        for name, exists in dirs.items():
            print(f"{name.capitalize()}: {'Exists' if exists else 'Missing'}")
        
        if report['recommendations']:
            print("\n--- Recommendations ---")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"{i}. {rec}")
        
        print("\n" + "="*60)


def main():
    """Main monitoring execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor system health')
    parser.add_argument('--continuous', action='store_true',
                       help='Run continuously (check every minute)')
    parser.add_argument('--interval', type=int, default=60,
                       help='Check interval in seconds (default: 60)')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor()
    
    if args.continuous:
        print(f"\nStarting continuous monitoring (interval: {args.interval}s)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                report = monitor.generate_report()
                monitor.print_report(report)
                report_file = monitor.save_report(report)
                print(f"\nReport saved: {report_file}")
                print(f"\nWaiting {args.interval} seconds until next check...\n")
                time.sleep(args.interval)
        
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
    
    else:
        # Single check
        report = monitor.generate_report()
        monitor.print_report(report)
        report_file = monitor.save_report(report)
        print(f"\nReport saved: {report_file}")


if __name__ == '__main__':
    main()









