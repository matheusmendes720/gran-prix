#!/usr/bin/env python3
"""
Master Deployment Validation Script
Runs all validation scripts and generates comprehensive report.

This script validates that deployment has NO ML dependencies.
"""
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Validation scripts to run
VALIDATION_SCRIPTS = [
    'scripts/validation/check_ml_dependencies.py',
    'scripts/validation/check_ml_endpoints.py',
    'scripts/validation/check_ml_imports.py',
    'scripts/validation/check_docker_image.py',
]

# Script names for reporting
SCRIPT_NAMES = [
    'ML Dependencies Check',
    'ML Endpoints Check',
    'ML Imports Check',
    'Docker Image Check',
]


def run_validation_script(script_path: Path) -> Tuple[bool, str]:
    """
    Run a validation script.
    
    Args:
        script_path: Path to validation script
    
    Returns:
        Tuple of (success, output)
    """
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, f"Error running script: {e}"


def main():
    """Main validation function"""
    import os
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    print("=" * 80)
    print("DEPLOYMENT VALIDATION - COMPREHENSIVE CHECK")
    print("=" * 80)
    print()
    print(f"Started: {datetime.now().isoformat()}")
    print()
    
    results = []
    all_passed = True
    
    # Run all validation scripts
    for script_path_str, script_name in zip(VALIDATION_SCRIPTS, SCRIPT_NAMES):
        script_path = project_root / script_path_str
        
        if not script_path.exists():
            print(f"⚠️  {script_name}: Script not found - {script_path}")
            results.append({'name': script_name, 'passed': False, 'output': 'Script not found'})
            all_passed = False
            continue
        
        print(f"Running: {script_name}...")
        print("-" * 80)
        
        passed, output = run_validation_script(script_path)
        
        if passed:
            print(f"✅ {script_name}: PASSED")
        else:
            print(f"❌ {script_name}: FAILED")
            all_passed = False
        
        print(output)
        print()
        
        results.append({
            'name': script_name,
            'passed': passed,
            'output': output
        })
    
    # Summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print()
    
    for result in results:
        status = "✅ PASSED" if result['passed'] else "❌ FAILED"
        print(f"{status}: {result['name']}")
    
    print()
    print("=" * 80)
    
    if all_passed:
        print("✅ ALL VALIDATIONS PASSED")
        print("   Deployment is compliant with ML Ops constraint")
        print("   No ML dependencies detected in deployment")
        return 0
    else:
        print("❌ VALIDATION FAILED")
        print("   Some validations failed - see output above")
        print("   Deployment is NOT compliant with ML Ops constraint")
        print()
        print("Action required:")
        print("  1. Review failed validations above")
        print("  2. Fix violations in deployment code")
        print("  3. Remove ML dependencies from deployment")
        print("  4. Re-run validation")
        return 1


if __name__ == "__main__":
    sys.exit(main())

