#!/usr/bin/env python3
"""
ML Endpoint Validation Script
Checks API routes for ML endpoints (inference, training, etc.).

This script validates that deployment API has NO ML endpoints.
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ML endpoint patterns to detect
ML_ENDPOINT_PATTERNS = [
    r'/predict',
    r'/forecast',
    r'/inference',
    r'/train',
    r'/retrain',
    r'/optimize',
    r'/model',
    r'/mlflow',
    r'/ml/',
    r'/inference/',
    r'/training/',
]

# API route files to check
API_ROUTE_FILES = [
    'backend/api/*.py',
    'backend/routes/*.py',
    'backend/app/routes/*.py',
]


def check_file_for_ml_endpoints(file_path: Path) -> Tuple[bool, List[dict]]:
    """
    Check a file for ML endpoints.
    
    Args:
        file_path: Path to file to check
    
    Returns:
        Tuple of (is_compliant, violations)
    """
    if not file_path.exists():
        return True, []  # File doesn't exist, not a violation
    
    violations = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        for pattern in ML_ENDPOINT_PATTERNS:
            # Case-insensitive search
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
    import glob
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    all_violations = []
    files_checked = []
    
    print("=" * 80)
    print("ML ENDPOINT VALIDATION")
    print("=" * 80)
    print()
    
    # Find all API route files
    api_files = []
    for pattern in API_ROUTE_FILES:
        api_files.extend(glob.glob(str(project_root / pattern), recursive=True))
    
    # Also check common API locations
    api_dirs = [
        project_root / 'backend' / 'api',
        project_root / 'backend' / 'routes',
        project_root / 'backend' / 'app' / 'routes',
    ]
    
    for api_dir in api_dirs:
        if api_dir.exists():
            api_files.extend(api_dir.glob('*.py'))
    
    # Remove duplicates
    api_files = list(set(api_files))
    
    print(f"Checking {len(api_files)} API route file(s)...")
    for file_path_str in api_files:
        file_path = Path(file_path_str)
        is_compliant, violations = check_file_for_ml_endpoints(file_path)
        
        if file_path.exists():
            files_checked.append(str(file_path))
            if violations:
                all_violations.extend(violations)
                print(f"  ❌ {file_path.relative_to(project_root)}: {len(violations)} violation(s) found")
                for v in violations:
                    print(f"     Line {v['line']}: {v['content']}")
            else:
                print(f"  ✅ {file_path.relative_to(project_root)}: No ML endpoints found")
    
    print()
    print("=" * 80)
    
    # Summary
    if all_violations:
        print("❌ VALIDATION FAILED")
        print(f"   Found {len(all_violations)} ML endpoint violation(s)")
        print()
        print("Violations:")
        for v in all_violations:
            print(f"  - {v['file']}:{v['line']}: {v['pattern']} - {v['content']}")
        print()
        print("Action required:")
        print("  1. Remove ML endpoints from API routes")
        print("  2. Only read operations for precomputed data allowed")
        print("  3. Data refresh endpoint is allowed (manual trigger only)")
        return 1
    else:
        print("✅ VALIDATION PASSED")
        print(f"   Checked {len(files_checked)} API route file(s)")
        print(f"   No ML endpoints found")
        return 0


if __name__ == "__main__":
    sys.exit(main())

