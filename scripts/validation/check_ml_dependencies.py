#!/usr/bin/env python3
"""
ML Dependency Validation Script
Checks requirements files and Dockerfiles for ML dependencies.

This script validates that deployment requirements have NO ML dependencies.
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ML dependency patterns to detect
ML_DEPENDENCIES = [
    r'torch',
    r'tensorflow',
    r'sklearn|scikit-learn',
    r'mlflow',
    r'xgboost',
    r'lightgbm',
    r'prophet',
    r'pmdarima',
    r'statsmodels',  # For ML usage (basic stats OK, but flag for review)
]

# Deployment requirements files to check
DEPLOYMENT_FILES = [
    'backend/requirements_deployment.txt',
    'infrastructure/docker/Dockerfile.backend.deployment',
]

# ML requirements files (allowed to have ML dependencies)
ML_FILES = [
    'backend/requirements_ml.txt',
    'infrastructure/docker/Dockerfile.backend.ml',
]


def check_file_for_ml_dependencies(file_path: Path, allowed: bool = False) -> Tuple[bool, List[str]]:
    """
    Check a file for ML dependencies.
    
    Args:
        file_path: Path to file to check
        allowed: If True, ML dependencies are allowed (for ML files)
    
    Returns:
        Tuple of (is_compliant, violations)
    """
    if not file_path.exists():
        return True, []  # File doesn't exist, not a violation
    
    violations = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        for pattern in ML_DEPENDENCIES:
            # Case-insensitive search
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = content.split('\n')[line_num - 1].strip()
                
                # Skip if in comments
                if line_content.startswith('#'):
                    continue
                
                # Skip if in allowed ML files
                if allowed:
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
    deployment_files_checked = []
    ml_files_checked = []
    
    print("=" * 80)
    print("ML DEPENDENCY VALIDATION")
    print("=" * 80)
    print()
    
    # Check deployment files (NO ML allowed)
    print("Checking deployment files (NO ML dependencies allowed)...")
    for file_path_str in DEPLOYMENT_FILES:
        file_path = project_root / file_path_str
        is_compliant, violations = check_file_for_ml_dependencies(file_path, allowed=False)
        
        if file_path.exists():
            deployment_files_checked.append(str(file_path))
            if violations:
                all_violations.extend(violations)
                print(f"  ❌ {file_path_str}: {len(violations)} violation(s) found")
                for v in violations:
                    print(f"     Line {v['line']}: {v['content']}")
            else:
                print(f"  ✅ {file_path_str}: No ML dependencies found")
        else:
            print(f"  ⚠️  {file_path_str}: File not found (skipping)")
    
    print()
    
    # Check ML files (ML allowed - just verify they exist)
    print("Checking ML files (ML dependencies allowed)...")
    for file_path_str in ML_FILES:
        file_path = project_root / file_path_str
        if file_path.exists():
            ml_files_checked.append(str(file_path))
            print(f"  ✅ {file_path_str}: Found (ML dependencies allowed)")
        else:
            print(f"  ⚠️  {file_path_str}: File not found (optional)")
    
    print()
    print("=" * 80)
    
    # Summary
    if all_violations:
        print("❌ VALIDATION FAILED")
        print(f"   Found {len(all_violations)} ML dependency violation(s) in deployment files")
        print()
        print("Violations:")
        for v in all_violations:
            print(f"  - {v['file']}:{v['line']}: {v['pattern']} - {v['content']}")
        print()
        print("Action required:")
        print("  1. Remove ML dependencies from deployment files")
        print("  2. Use requirements_deployment.txt for deployment (NO ML)")
        print("  3. Use requirements_ml.txt for ML processing (separate environment)")
        return 1
    else:
        print("✅ VALIDATION PASSED")
        print(f"   Checked {len(deployment_files_checked)} deployment file(s)")
        print(f"   No ML dependencies found in deployment files")
        return 0


if __name__ == "__main__":
    import os
    sys.exit(main())

