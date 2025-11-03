"""
Deployment helper script.
Prepares system for production deployment with checks and setup.
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import subprocess
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demand_forecasting.utils.config import Config


class DeploymentHelper:
    """Helper for production deployment."""
    
    def __init__(self):
        """Initialize deployment helper."""
        self.config = Config()
        self.checklist = []
    
    def check_dependencies(self):
        """Check if all dependencies are installed."""
        required = [
            'pandas', 'numpy', 'statsmodels', 'prophet',
            'scikit-learn', 'holidays', 'pyyaml'
        ]
        
        optional = {
            'pmdarima': 'Auto ARIMA',
            'tensorflow': 'LSTM models',
            'flask': 'Web dashboard',
            'streamlit': 'Interactive dashboard',
            'reportlab': 'PDF reports'
        }
        
        missing_required = []
        missing_optional = []
        
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                missing_required.append(pkg)
        
        for pkg, desc in optional.items():
            try:
                __import__(pkg)
            except ImportError:
                missing_optional.append((pkg, desc))
        
        return {
            'required_missing': missing_required,
            'optional_missing': missing_optional,
            'all_ok': len(missing_required) == 0
        }
    
    def check_directories(self):
        """Check required directories exist."""
        required_dirs = ['data', 'models', 'reports', 'logs']
        missing = []
        existing = []
        
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                existing.append(dir_name)
            else:
                missing.append(dir_name)
                dir_path.mkdir(exist_ok=True, parents=True)
        
        return {
            'existing': existing,
            'missing': missing,
            'created': missing.copy()
        }
    
    def check_config(self):
        """Validate configuration file."""
        config_path = Path('config.yaml')
        
        if not config_path.exists():
            return {
                'valid': False,
                'error': 'config.yaml not found'
            }
        
        try:
            config = Config()
            # Basic validation
            required_keys = ['forecasting', 'models', 'data']
            
            for key in required_keys:
                if config.get(key) is None:
                    return {
                        'valid': False,
                        'error': f'Missing config section: {key}'
                    }
            
            return {
                'valid': True,
                'error': None
            }
        
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def create_env_file(self):
        """Create .env file template."""
        env_file = Path('.env.example')
        
        env_template = """# Environment Variables for Demand Forecasting System

# API Configuration
API_HOST=127.0.0.1
API_PORT=5000

# Dashboard Configuration
DASHBOARD_HOST=127.0.0.1
DASHBOARD_PORT=8080

# Email Configuration (for alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=alerts@novacorrente.com
SENDER_PASSWORD=your_password_here
ALERT_RECIPIENTS=manager@novacorrente.com

# Model Configuration
USE_LSTM=true
ENSEMBLE_WEIGHTS_ARIMA=0.4
ENSEMBLE_WEIGHTS_PROPHET=0.3
ENSEMBLE_WEIGHTS_LSTM=0.3

# Data Configuration
DATA_PATH=data/nova_corrente_demand.csv
CURRENT_STOCKS_PATH=data/current_stocks.json

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs

# Production Settings
DEBUG=false
"""
        
        with open(env_file, 'w') as f:
            f.write(env_template)
        
        return env_file
    
    def generate_deployment_report(self):
        """Generate deployment readiness report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'dependencies': self.check_dependencies(),
            'directories': self.check_directories(),
            'config': self.check_config(),
            'ready': False,
            'recommendations': []
        }
        
        # Overall readiness
        deps_ok = report['dependencies']['all_ok']
        config_ok = report['config']['valid']
        
        report['ready'] = deps_ok and config_ok
        
        # Recommendations
        if not deps_ok:
            report['recommendations'].append(
                'Install missing required dependencies: pip install -r requirements.txt'
            )
        
        if not config_ok:
            report['recommendations'].append(
                'Fix configuration file: config.yaml'
            )
        
        if not report['directories']['existing']:
            report['recommendations'].append(
                'Created missing directories. Ensure they have proper permissions.'
            )
        
        return report
    
    def print_report(self, report):
        """Print deployment report."""
        print("\n" + "="*60)
        print("Deployment Readiness Report")
        print("="*60)
        print(f"\nTimestamp: {report['timestamp']}")
        print(f"Ready for Deployment: {'YES' if report['ready'] else 'NO'}")
        
        print("\n--- Dependencies ---")
        deps = report['dependencies']
        if deps['all_ok']:
            print("[OK] All required dependencies installed")
        else:
            print("[ERROR] Missing required dependencies:")
            for pkg in deps['required_missing']:
                print(f"  - {pkg}")
        
        if deps['optional_missing']:
            print("\n[WARNING] Missing optional dependencies:")
            for pkg, desc in deps['optional_missing']:
                print(f"  - {pkg}: {desc}")
        
        print("\n--- Directories ---")
        dirs = report['directories']
        print(f"Existing: {', '.join(dirs['existing'])}")
        if dirs['created']:
            print(f"Created: {', '.join(dirs['created'])}")
        
        print("\n--- Configuration ---")
        config = report['config']
        if config['valid']:
            print("[OK] Configuration valid")
        else:
            print(f"[ERROR] Configuration invalid: {config['error']}")
        
        if report['recommendations']:
            print("\n--- Recommendations ---")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"{i}. {rec}")
        
        print("\n" + "="*60)


def main():
    """Main deployment check."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deployment readiness check')
    parser.add_argument('--create-env', action='store_true',
                       help='Create .env.example file')
    
    args = parser.parse_args()
    
    helper = DeploymentHelper()
    
    if args.create_env:
        env_file = helper.create_env_file()
        print(f"[OK] Created {env_file}")
    
    report = helper.generate_deployment_report()
    helper.print_report(report)
    
    # Save report
    report_file = Path('logs') / f"deployment_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved: {report_file}")
    
    if report['ready']:
        print("\n[SUCCESS] System is ready for deployment!")
        return 0
    else:
        print("\n[WARNING] System needs attention before deployment")
        return 1


if __name__ == '__main__':
    sys.exit(main())

