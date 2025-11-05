#!/usr/bin/env python3
"""
Script para verificar ausência de imports ML no código de deployment
Nova Corrente - Validação de constraint NO ML OPS IN DEPLOYMENT

Uso:
    python scripts/validation/check_no_ml_imports.py
"""

import sys
from pathlib import Path
import re
from typing import List, Dict

# ML imports to check
ML_IMPORTS = [
    'torch', 'tensorflow', 'keras', 'sklearn', 'scikit-learn',
    'mlflow', 'xgboost', 'lightgbm', 'prophet', 'pmdarima',
    'statsmodels', 'pytorch', 'model_registry', 'prediction_service',
    'ml_models', 'arima', 'lstm'
]

# Directories to check
DEPLOYMENT_DIRS = [
    'backend/app',
    'backend/api'  # Only if enhanced_api.py still exists
]

# Directories to exclude
EXCLUDE_DIRS = [
    'backend/ml',
    'backend/services/ml_models',  # Only if used in deployment
    'backend/data/collectors',
    '__pycache__',
    '.git'
]

# Files to exclude
EXCLUDE_FILES = [
    'requirements_ml.txt',
    'requirements.txt',  # Dev requirements (OK to have ML)
    'test_*.py',  # Test files (may have ML for testing)
    '*_test.py'
]


def is_excluded(file_path: Path) -> bool:
    """Check if file should be excluded from validation"""
    # Check if in exclude dirs
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in str(file_path):
            return True
    
    # Check if matches exclude files pattern
    for exclude_pattern in EXCLUDE_FILES:
        if re.search(exclude_pattern.replace('*', '.*'), file_path.name):
            return True
    
    return False


def check_file_for_ml_imports(file_path: Path) -> List[Dict]:
    """Check file for ML imports"""
    issues = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for ML imports
            for ml_import in ML_IMPORTS:
                # Check import statements
                if re.search(rf'import\s+{ml_import}|from\s+.*{ml_import}', line):
                    issues.append({
                        'file': str(file_path),
                        'line': i,
                        'type': 'ML_IMPORT',
                        'message': f'ML import found: {line.strip()}',
                        'severity': 'error'
                    })
                
                # Check for ML service initialization
                if 'prediction_service' in line and '=' in line:
                    issues.append({
                        'file': str(file_path),
                        'line': i,
                        'type': 'ML_SERVICE_INIT',
                        'message': f'ML service initialization: {line.strip()}',
                        'severity': 'error'
                    })
                
                if 'model_registry' in line and ('import' in line or 'from' in line):
                    issues.append({
                        'file': str(file_path),
                        'line': i,
                        'type': 'ML_REGISTRY',
                        'message': f'Model registry import: {line.strip()}',
                        'severity': 'error'
                    })
    except Exception as e:
        issues.append({
            'file': str(file_path),
            'line': 0,
            'type': 'READ_ERROR',
            'message': f'Error reading file: {e}',
            'severity': 'warning'
        })
    
    return issues


def main():
    """Main function"""
    project_root = Path(__file__).parent.parent.parent
    
    all_issues = []
    files_checked = 0
    
    print("=" * 80)
    print("[CHECKING] ML IMPORTS IN DEPLOYMENT CODE")
    print("=" * 80)
    
    # Check deployment directories
    for deployment_dir in DEPLOYMENT_DIRS:
        dir_path = project_root / deployment_dir
        if not dir_path.exists():
            print(f"⚠️  Directory not found: {deployment_dir}")
            continue
        
        print(f"\n[CHECKING] {deployment_dir}")
        
        # Find all Python files
        for py_file in dir_path.rglob('*.py'):
            if is_excluded(py_file):
                continue
            
            files_checked += 1
            issues = check_file_for_ml_imports(py_file)
            
            if issues:
                all_issues.extend(issues)
                print(f"  [ERROR] {py_file.relative_to(project_root)}: {len(issues)} issue(s)")
                for issue in issues:
                    if issue['severity'] == 'error':
                        print(f"     Line {issue['line']}: {issue['message']}")
            else:
                print(f"  [OK] {py_file.relative_to(project_root)}")
    
    # Summary
    print("\n" + "=" * 80)
    print("[SUMMARY]")
    print("=" * 80)
    print(f"Files checked: {files_checked}")
    print(f"Total issues: {len(all_issues)}")
    
    errors = [i for i in all_issues if i['severity'] == 'error']
    warnings = [i for i in all_issues if i['severity'] == 'warning']
    
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    
    if errors:
        print("\n[ERROR] ERRORS FOUND:")
        for error in errors:
            print(f"  - {error['file']}:{error['line']} - {error['message']}")
        sys.exit(1)
    else:
        print("\n[OK] NO ML IMPORTS FOUND IN DEPLOYMENT CODE")
        sys.exit(0)


if __name__ == '__main__':
    main()

