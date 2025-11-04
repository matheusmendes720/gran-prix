#!/usr/bin/env python3
"""
Runtime ML Constraint Monitoring Script

This script runs periodically in deployed environment to check for ML dependencies
at runtime and alerts if ML frameworks are detected.
"""
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# ML package patterns to detect
ML_PACKAGES = [
    'torch',
    'tensorflow',
    'sklearn',
    'scikit-learn',
    'mlflow',
    'xgboost',
    'lightgbm',
    'prophet',
    'pmdarima',
]


def check_runtime_ml_dependencies() -> Dict[str, any]:
    """
    Check for ML dependencies at runtime.
    
    Returns:
        Dict with status, violations, and details
    """
    violations = []
    checked_packages = []
    
    for package in ML_PACKAGES:
        checked_packages.append(package)
        try:
            # Try to import the package
            __import__(package)
            violations.append(package)
        except ImportError:
            # Good - ML package not installed
            pass
        except Exception as e:
            # Unexpected error
            violations.append(f"{package} (error: {str(e)})")
    
    return {
        'timestamp': datetime.now().isoformat(),
        'status': 'compliant' if len(violations) == 0 else 'non_compliant',
        'violations': violations,
        'checked_packages': checked_packages,
        'message': 'No ML dependencies detected' if len(violations) == 0 else f'ML dependencies detected: {violations}'
    }


def main():
    """Main monitoring function"""
    import json
    
    print("=" * 80)
    print("RUNTIME ML CONSTRAINT MONITORING")
    print("=" * 80)
    print()
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    result = check_runtime_ml_dependencies()
    
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print()
    
    if result['violations']:
        print("❌ VIOLATIONS DETECTED:")
        for violation in result['violations']:
            print(f"  - {violation}")
        print()
        print("⚠️  ALERT: ML dependencies detected in runtime environment!")
        print("   This violates the 'NO ML OPS LOGIC IN DEPLOYMENT' constraint.")
        print("   Action required:")
        print("   1. Remove ML dependencies from deployment")
        print("   2. Use requirements_deployment.txt (NO ML)")
        print("   3. Rebuild Docker image")
        print("   4. Restart services")
        
        # Log to file if LOG_DIR is set
        log_dir = os.getenv('LOG_DIR', './logs')
        log_file = Path(log_dir) / 'ml_constraint_monitoring.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} | VIOLATION | {json.dumps(result)}\n")
        
        return 1
    else:
        print("✅ COMPLIANT: No ML dependencies detected")
        print(f"   Checked {len(result['checked_packages'])} packages")
        
        # Log to file if LOG_DIR is set
        log_dir = os.getenv('LOG_DIR', './logs')
        log_file = Path(log_dir) / 'ml_constraint_monitoring.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} | COMPLIANT | {json.dumps(result)}\n")
        
        return 0


if __name__ == "__main__":
    sys.exit(main())

