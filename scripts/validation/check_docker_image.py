#!/usr/bin/env python3
"""
Docker Image Validation Script
Validates Docker image has no ML dependencies.

This script builds the Docker image and checks installed packages.
"""
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

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

# Docker image name
DOCKER_IMAGE = 'nova-corrente-backend:deployment'
DOCKERFILE = 'infrastructure/docker/Dockerfile.backend.deployment'
MAX_IMAGE_SIZE_MB = 600


def check_docker_image() -> Tuple[bool, List[str]]:
    """
    Check Docker image for ML dependencies.
    
    Returns:
        Tuple of (is_compliant, violations)
    """
    violations = []
    
    try:
        # Build Docker image
        print("Building Docker image...")
        build_result = subprocess.run(
            ['docker', 'build', '-t', DOCKER_IMAGE, '-f', DOCKERFILE, '.'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if build_result.returncode != 0:
            violations.append(f"Docker build failed: {build_result.stderr}")
            return False, violations
        
        print("✅ Docker image built successfully")
        
        # Check installed packages
        print("Checking installed packages...")
        pip_list_result = subprocess.run(
            ['docker', 'run', '--rm', DOCKER_IMAGE, 'pip', 'list'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if pip_list_result.returncode != 0:
            violations.append(f"pip list failed: {pip_list_result.stderr}")
            return False, violations
        
        # Check for ML packages
        installed_packages = pip_list_result.stdout.lower()
        for ml_package in ML_PACKAGES:
            if ml_package.lower() in installed_packages:
                violations.append(f"ML package detected: {ml_package}")
        
        # Check image size
        print("Checking image size...")
        inspect_result = subprocess.run(
            ['docker', 'inspect', '--format={{.Size}}', DOCKER_IMAGE],
            capture_output=True,
            text=True,
            check=False
        )
        
        if inspect_result.returncode == 0:
            size_bytes = int(inspect_result.stdout.strip())
            size_mb = size_bytes / (1024 * 1024)
            if size_mb > MAX_IMAGE_SIZE_MB:
                violations.append(f"Image size too large: {size_mb:.2f} MB (max: {MAX_IMAGE_SIZE_MB} MB)")
        
    except FileNotFoundError:
        violations.append("Docker not found - please install Docker")
        return False, violations
    except Exception as e:
        violations.append(f"Error checking Docker image: {e}")
        return False, violations
    
    return len(violations) == 0, violations


def main():
    """Main validation function"""
    import os
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    print("=" * 80)
    print("DOCKER IMAGE VALIDATION")
    print("=" * 80)
    print()
    
    is_compliant, violations = check_docker_image()
    
    print()
    print("=" * 80)
    
    # Summary
    if violations:
        print("❌ VALIDATION FAILED")
        print(f"   Found {len(violations)} violation(s)")
        print()
        print("Violations:")
        for v in violations:
            print(f"  - {v}")
        print()
        print("Action required:")
        print("  1. Remove ML dependencies from Dockerfile")
        print("  2. Use requirements_deployment.txt (NO ML dependencies)")
        print("  3. Verify image size < 600 MB")
        return 1
    else:
        print("✅ VALIDATION PASSED")
        print("   Docker image has no ML dependencies")
        print("   Image size is within limits")
        return 0


if __name__ == "__main__":
    sys.exit(main())

