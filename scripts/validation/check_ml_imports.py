#!/usr/bin/env python3
"""
ML Import Validation Script
Checks deployment code for ML imports.

This script validates that deployment code has NO ML imports.
ML code should be in separate directories (backend/ml/, backend/scripts/train_*.py).
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ML import patterns to detect
ML_IMPORT_PATTERNS = [
    r'import torch',
    r'from torch',
    r'import tensorflow',
    r'from tensorflow',
    r'import tf',
    r'from tf',
    r'import sklearn',
    r'from sklearn',
    r'import mlflow',
    r'from mlflow',
    r'import xgboost',
    r'from xgboost',
    r'import lightgbm',
    r'from lightgbm',
    r'import prophet',
    r'from prophet',
    r'import pmdarima',
    r'from pmdarima',
]

# Directories to exclude (ML code only)
EXCLUDED_DIRS = [
    'backend/ml/',
    'backend/scripts/train_',
    'backend/scripts/scheduled_forecast',
]

# Deployment code directories to check
DEPLOYMENT_CODE_DIRS = [
    'backend/api/',
    'backend/services/',
    'backend/app/',
    'backend/routes/',
]


def is_excluded(file_path: Path) -> bool:
    """Check if file should be excluded from validation"""
    file_str = str(file_path)
    for excluded in EXCLUDED_DIRS:
        if excluded in file_str:
            return True
    return False


def check_file_for_ml_imports(file_path: Path) -> Tuple[bool, List[dict]]:
    """
    Check a file for ML imports.
    
    Args:
        file_path: Path to file to check
    
    Returns:
        Tuple of (is_compliant, violations)
    """
    if not file_path.exists():
        return True, []  # File doesn't exist, not a violation
    
    if is_excluded(file_path):
        return True, []  # File is in excluded directory (ML code only)
    
    violations = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        for pattern in ML_IMPORT_PATTERNS:
            # Case-sensitive search for imports
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = content.split('\n')[line_num - 1].strip()
                
                # Skip if in comments
                if line_content.startswith('#'):
                    continue
                
                # Skip if in docstrings
                if '"""' in line_content or "'''" in line_content:
                    continue
                
                violations.append({
                    'pattern': pattern,
                    'line': line_num,
                    'content': line_content,
                    'file': str(file_path)
                })
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return False, [{'error': str(e), 'file': str(file_path)}]
    
    return len(violations) == 0, violations


def main():
    """Main validation function"""
    import os
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    all_violations = []
    files_checked = []
    
    print("=" * 80)
    print("ML IMPORT VALIDATION")
    print("=" * 80)
    print()
    
    # Find all deployment code files
    deployment_files = []
    for pattern in DEPLOYMENT_CODE_DIRS:
        code_dir = project_root / pattern
        if code_dir.exists():
            deployment_files.extend(code_dir.rglob('*.py'))
    
    # Remove excluded files
    deployment_files = [f for f in deployment_files if not is_excluded(f)]
    
    print(f"Checking {len(deployment_files)} deployment code file(s)...")
    for file_path in deployment_files:
        is_compliant, violations = check_file_for_ml_imports(file_path)
        
        if file_path.exists():
            files_checked.append(str(file_path))
            if violations:
                all_violations.extend(violations)
                print(f"  ❌ {file_path.relative_to(project_root)}: {len(violations)} violation(s) found")
                for v in violations:
                    print(f"     Line {v['line']}: {v['content']}")
    
    if not all_violations:
        print(f"  ✅ All {len(files_checked)} file(s) compliant - No ML imports found")
    
    print()
    print("=" * 80)
    
    # Summary
    if all_violations:
        print("❌ VALIDATION FAILED")
        print(f"   Found {len(all_violations)} ML import violation(s)")
        print()
        print("Violations:")
        for v in all_violations:
            print(f"  - {v['file']}:{v['line']}: {v['pattern']} - {v['content']}")
        print()
        print("Action required:")
        print("  1. Remove ML imports from deployment code")
        print("  2. ML code should be in separate directories (backend/ml/, backend/scripts/train_*.py)")
        print("  3. Deployment code should only read precomputed results")
        return 1
    else:
        print("✅ VALIDATION PASSED")
        print(f"   Checked {len(files_checked)} deployment code file(s)")
        print(f"   No ML imports found")
        return 0


if __name__ == "__main__":
    sys.exit(main())

