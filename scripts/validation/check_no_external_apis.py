#!/usr/bin/env python3
"""
Script para verificar ausência de chamadas a APIs externas no código de deployment
Nova Corrente - Validação de constraint NO APIs externas em tempo real

Uso:
    python scripts/validation/check_no_external_apis.py
"""

import sys
from pathlib import Path
import re
from typing import List, Dict

# External API patterns to check
EXTERNAL_API_PATTERNS = [
    (r'climate_etl\.run\s*\(', 'climate_etl.run() call'),
    (r'economic_etl\.run\s*\(', 'economic_etl.run() call'),
    (r'anatel_5g_etl\.run\s*\(', 'anatel_5g_etl.run() call'),
    (r'external_data_service', 'external_data_service usage'),
    (r'external_apis_config', 'external_apis_config usage'),
    (r'INMET_CONFIG', 'INMET_CONFIG usage'),
    (r'BACEN_CONFIG', 'BACEN_CONFIG usage'),
    (r'ANATEL_CONFIG', 'ANATEL_CONFIG usage'),
    (r'ExpandedAPIIntegration', 'ExpandedAPIIntegration usage'),
    (r'brazilian_apis_expanded', 'brazilian_apis_expanded usage'),
    (r'web_scrapers', 'web_scrapers usage'),
]

# Directories to check
DEPLOYMENT_DIRS = [
    'backend/app',
    'backend/pipelines/orchestrator_service.py'
]

# Directories to exclude
EXCLUDE_DIRS = [
    'backend/data/collectors',
    'backend/pipelines/climate_etl.py',  # ETL files themselves (OK to have API code)
    'backend/pipelines/economic_etl.py',
    'backend/pipelines/anatel_5g_etl.py',
    '__pycache__',
    '.git'
]


def is_excluded(file_path: Path) -> bool:
    """Check if file should be excluded from validation"""
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in str(file_path):
            return True
    return False


def check_file_for_external_apis(file_path: Path) -> List[Dict]:
    """Check file for external API calls"""
    issues = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Skip commented lines
            if line.strip().startswith('#'):
                continue
            
            # Check for external API patterns
            for pattern, description in EXTERNAL_API_PATTERNS:
                if re.search(pattern, line):
                    # Check if it's a disabled call (commented out)
                    if '#' in line and line.split('#')[0].strip().endswith('#'):
                        # It's commented, OK
                        continue
                    
                    # Check if it's in a conditional for local processing
                    if 'ENABLE_EXTERNAL_APIS' in line or 'if not enable_external_apis' in line.lower():
                        # It's in a conditional, OK
                        continue
                    
                    issues.append({
                        'file': str(file_path),
                        'line': i,
                        'type': 'EXTERNAL_API_CALL',
                        'message': f'{description} found: {line.strip()}',
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
    print("[CHECKING] EXTERNAL API CALLS IN DEPLOYMENT CODE")
    print("=" * 80)
    
    # Check deployment directories
    for deployment_dir in DEPLOYMENT_DIRS:
        dir_path = project_root / deployment_dir
        
        if deployment_dir.endswith('.py'):
            # Single file
            file_path = dir_path
            if not file_path.exists():
                print(f"⚠️  File not found: {deployment_dir}")
                continue
            
            if is_excluded(file_path):
                continue
            
            files_checked += 1
            issues = check_file_for_external_apis(file_path)
            
            if issues:
                all_issues.extend(issues)
                print(f"  [ERROR] {file_path.relative_to(project_root)}: {len(issues)} issue(s)")
                for issue in issues:
                    if issue['severity'] == 'error':
                        print(f"     Line {issue['line']}: {issue['message']}")
            else:
                print(f"  [OK] {file_path.relative_to(project_root)}")
        else:
            # Directory
            if not dir_path.exists():
                print(f"⚠️  Directory not found: {deployment_dir}")
                continue
            
            print(f"\n[CHECKING] {deployment_dir}")
            
            # Find all Python files
            for py_file in dir_path.rglob('*.py'):
                if is_excluded(py_file):
                    continue
                
                files_checked += 1
                issues = check_file_for_external_apis(py_file)
                
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
        print("\n[OK] NO EXTERNAL API CALLS FOUND IN DEPLOYMENT CODE")
        sys.exit(0)


if __name__ == '__main__':
    main()

