#!/usr/bin/env python3
"""
Script de Validação para Deployment Simplificado
Nova Corrente - Verifica ausência de ML dependencies e APIs externas

Uso:
    python scripts/validation/validate_deployment_simplified.py
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple
import re
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# ML dependencies to check
ML_DEPENDENCIES = [
    'torch', 'tensorflow', 'keras', 'sklearn', 'scikit-learn',
    'mlflow', 'xgboost', 'lightgbm', 'prophet', 'pmdarima',
    'statsmodels', 'pytorch', 'theano', 'caffe', 'cntk'
]

# ML imports to check
ML_IMPORTS = [
    'model_registry', 'prediction_service', 'ml_models',
    'torch', 'tensorflow', 'sklearn', 'prophet', 'arima',
    'lstm', 'xgboost', 'lightgbm', 'mlflow'
]

# External API patterns to check
EXTERNAL_API_PATTERNS = [
    r'climate_etl\.run',
    r'economic_etl\.run',
    r'anatel_5g_etl\.run',
    r'external_data_service',
    r'external_apis_config',
    r'INMET_CONFIG',
    r'BACEN_CONFIG',
    r'ANATEL_CONFIG',
    r'ExpandedAPIIntegration',
    r'brazilian_apis_expanded',
    r'web_scrapers'
]


class DeploymentValidator:
    """Validator for deployment simplification"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_dir = project_root / 'backend'
        self.app_dir = self.backend_dir / 'app'
        self.api_dir = self.backend_dir / 'api'
        self.services_dir = self.backend_dir / 'services'
        self.pipelines_dir = self.backend_dir / 'pipelines'
        
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.info: List[Dict] = []
        
    def validate_ml_dependencies(self) -> Tuple[bool, List[Dict]]:
        """Validate absence of ML dependencies in deployment code"""
        print("\n[VALIDATING] ML Dependencies...")
        
        errors = []
        warnings = []
        
        # Check deployment requirements
        requirements_file = self.backend_dir / 'requirements_deployment.txt'
        if requirements_file.exists():
            content = requirements_file.read_text()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                # Skip commented lines
                if line.strip().startswith('#'):
                    continue
                
                # Check for ML dependencies in non-commented lines
                for ml_dep in ML_DEPENDENCIES:
                    # Check if it's an actual dependency (not just a mention)
                    if ml_dep.lower() in line.lower() and not line.strip().startswith('#'):
                        # Check if it's a real dependency line (has >= or ==)
                        if '>=' in line or '==' in line or line.strip().startswith(ml_dep.lower()):
                            errors.append({
                                'file': str(requirements_file.relative_to(self.project_root)),
                                'line': i,
                                'type': 'ML_DEPENDENCY_IN_REQUIREMENTS',
                                'message': f'ML dependency "{ml_dep}" found in deployment requirements: {line.strip()}'
                            })
        
        # Check deployment code files
        deployment_files = [
            self.app_dir / 'main.py',
            self.app_dir / 'core' / 'integration_manager.py',
            self.api_dir / 'enhanced_api.py' if (self.api_dir / 'enhanced_api.py').exists() else None,
        ]
        
        for file_path in deployment_files:
            if file_path is None or not file_path.exists():
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Skip commented lines
                    stripped = line.strip()
                    if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                        continue
                    
                    # Check for ML imports (only in non-commented code)
                    for ml_import in ML_IMPORTS:
                        if f'import {ml_import}' in line or f'from {ml_import}' in line:
                            # Make sure it's not commented out
                            if not line.strip().startswith('#'):
                                errors.append({
                                    'file': str(file_path.relative_to(self.project_root)),
                                    'line': i,
                                    'type': 'ML_IMPORT_FOUND',
                                    'message': f'ML import found: {line.strip()}'
                                })
                    
                    # Check for ML service initialization (only active code, not commented)
                    if 'prediction_service' in line and '=' in line and not line.strip().startswith('#'):
                        errors.append({
                            'file': str(file_path.relative_to(self.project_root)),
                            'line': i,
                            'type': 'ML_SERVICE_INIT',
                            'message': f'ML service initialization found: {line.strip()}'
                        })
                    
                    if 'model_registry' in line and 'import' in line and not line.strip().startswith('#'):
                        errors.append({
                            'file': str(file_path.relative_to(self.project_root)),
                            'line': i,
                            'type': 'ML_REGISTRY_IMPORT',
                            'message': f'Model registry import found: {line.strip()}'
                        })
            except Exception as e:
                warnings.append({
                    'file': str(file_path.relative_to(self.project_root)),
                    'type': 'READ_ERROR',
                    'message': f'Error reading file: {e}'
                })
        
        return len(errors) == 0, errors + warnings
    
    def validate_external_apis(self) -> Tuple[bool, List[Dict]]:
        """Validate absence of external API calls in deployment code"""
        print("\n[VALIDATING] External APIs...")
        
        errors = []
        warnings = []
        
        # Check integration manager
        integration_file = self.app_dir / 'core' / 'integration_manager.py'
        if integration_file.exists():
            try:
                content = integration_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for external API client initialization
                    for pattern in ['INMET_CONFIG', 'BACEN_CONFIG', 'ANATEL_CONFIG', 
                                   'OPENWEATHER_CONFIG', 'ExpandedAPIIntegration']:
                        if pattern in line and ('import' in line or '=' in line):
                            errors.append({
                                'file': str(integration_file.relative_to(self.project_root)),
                                'line': i,
                                'type': 'EXTERNAL_API_CLIENT',
                                'message': f'External API client initialization found: {line.strip()}'
                            })
                    
                    # Check for external data service
                    if 'external_data_service' in line and '=' in line:
                        errors.append({
                            'file': str(integration_file.relative_to(self.project_root)),
                            'line': i,
                            'type': 'EXTERNAL_DATA_SERVICE',
                            'message': f'External data service initialization found: {line.strip()}'
                        })
            except Exception as e:
                warnings.append({
                    'file': str(integration_file.relative_to(self.project_root)),
                    'type': 'READ_ERROR',
                    'message': f'Error reading file: {e}'
                })
        
        # Check orchestrator
        orchestrator_file = self.pipelines_dir / 'orchestrator_service.py'
        if orchestrator_file.exists():
            try:
                content = orchestrator_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for ETL pipeline calls
                    for pattern in EXTERNAL_API_PATTERNS:
                        if re.search(pattern, line):
                            if '.run(' in line and '#' not in line.split('.run(')[0]:
                                warnings.append({
                                    'file': str(orchestrator_file.relative_to(self.project_root)),
                                    'line': i,
                                    'type': 'ETL_PIPELINE_CALL',
                                    'message': f'ETL pipeline call found (should be disabled): {line.strip()}'
                                })
            except Exception as e:
                warnings.append({
                    'file': str(orchestrator_file.relative_to(self.project_root)),
                    'type': 'READ_ERROR',
                    'message': f'Error reading file: {e}'
                })
        
        return len(errors) == 0, errors + warnings
    
    def validate_dockerfile(self) -> Tuple[bool, List[Dict]]:
        """Validate Dockerfile doesn't include ML dependencies"""
        print("\n[VALIDATING] Dockerfile...")
        
        errors = []
        warnings = []
        
        dockerfile = self.project_root / 'infrastructure' / 'docker' / 'Dockerfile.backend.deployment'
        if dockerfile.exists():
            content = dockerfile.read_text(encoding='utf-8')
            
            # Check if it uses deployment requirements
            if 'requirements_deployment.txt' not in content:
                warnings.append({
                    'file': str(dockerfile.relative_to(self.project_root)),
                    'type': 'DOCKERFILE_REQUIREMENTS',
                    'message': 'Dockerfile may not be using deployment requirements'
                })
            
            # Check for ML dependency verification
            if 'grep -iE "(torch|tensorflow|sklearn|mlflow' not in content:
                warnings.append({
                    'file': str(dockerfile.relative_to(self.project_root)),
                    'type': 'DOCKERFILE_ML_CHECK',
                    'message': 'Dockerfile may not have ML dependency verification'
                })
        else:
            errors.append({
                'file': 'Dockerfile.backend.deployment',
                'type': 'DOCKERFILE_MISSING',
                'message': 'Deployment Dockerfile not found'
            })
        
        return len(errors) == 0, errors + warnings
    
    def validate_environment_variables(self) -> Tuple[bool, List[Dict]]:
        """Validate environment variables are correctly set"""
        print("\n[VALIDATING] Environment Variables...")
        
        errors = []
        warnings = []
        
        # Check docker-compose.yml
        compose_file = self.project_root / 'docker-compose.yml'
        if compose_file.exists():
            content = compose_file.read_text(encoding='utf-8')
            
            # Check for ENABLE_EXTERNAL_APIS
            if 'ENABLE_EXTERNAL_APIS' not in content:
                warnings.append({
                    'file': str(compose_file.relative_to(self.project_root)),
                    'type': 'ENV_VAR_MISSING',
                    'message': 'ENABLE_EXTERNAL_APIS environment variable not found in docker-compose.yml'
                })
            
            # Check for ML_RESULTS_PATH
            if 'ML_RESULTS_PATH' not in content:
                warnings.append({
                    'file': str(compose_file.relative_to(self.project_root)),
                    'type': 'ENV_VAR_MISSING',
                    'message': 'ML_RESULTS_PATH environment variable not found in docker-compose.yml'
                })
        
        return len(errors) == 0, errors + warnings
    
    def run_all_validations(self) -> Dict:
        """Run all validations"""
        print("=" * 80)
        print("DEPLOYMENT VALIDATION - NOVA CORRENTE")
        print("=" * 80)
        print(f"Project Root: {self.project_root}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'validations': {}
        }
        
        # Run validations
        ml_ok, ml_issues = self.validate_ml_dependencies()
        results['validations']['ml_dependencies'] = {
            'passed': ml_ok,
            'issues': ml_issues
        }
        
        api_ok, api_issues = self.validate_external_apis()
        results['validations']['external_apis'] = {
            'passed': api_ok,
            'issues': api_issues
        }
        
        docker_ok, docker_issues = self.validate_dockerfile()
        results['validations']['dockerfile'] = {
            'passed': docker_ok,
            'issues': docker_issues
        }
        
        env_ok, env_issues = self.validate_environment_variables()
        results['validations']['environment_variables'] = {
            'passed': env_ok,
            'issues': env_issues
        }
        
        # Calculate overall status
        all_passed = ml_ok and api_ok and docker_ok and env_ok
        total_errors = sum(len(v['issues']) for v in results['validations'].values() 
                          if any(issue.get('type', '').startswith(('ML_', 'EXTERNAL_', 'DOCKERFILE_MISSING')) 
                                for issue in v['issues']))
        total_warnings = sum(len(v['issues']) for v in results['validations'].values()) - total_errors
        
        results['summary'] = {
            'all_passed': all_passed,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'status': '[PASS]' if all_passed and total_errors == 0 else '[FAIL]'
        }
        
        # Print summary
        print("\n" + "=" * 80)
        print("[SUMMARY] VALIDATION SUMMARY")
        print("=" * 80)
        print(f"Status: {results['summary']['status']}")
        print(f"Total Errors: {total_errors}")
        print(f"Total Warnings: {total_warnings}")
        print("=" * 80)
        
        if total_errors > 0:
            print("\n[ERROR] ERRORS FOUND:")
            for validation_name, validation_result in results['validations'].items():
                for issue in validation_result['issues']:
                    if issue.get('type', '').startswith(('ML_', 'EXTERNAL_', 'DOCKERFILE_MISSING')):
                        print(f"  - {validation_name}: {issue.get('message', 'Unknown error')}")
        
        if total_warnings > 0:
            print("\n[WARNING] WARNINGS:")
            for validation_name, validation_result in results['validations'].items():
                for issue in validation_result['issues']:
                    if not issue.get('type', '').startswith(('ML_', 'EXTERNAL_', 'DOCKERFILE_MISSING')):
                        print(f"  - {validation_name}: {issue.get('message', 'Unknown warning')}")
        
        # Save results
        results_file = self.project_root / 'reports' / 'deployment_validation_results.json'
        results_file.parent.mkdir(parents=True, exist_ok=True)
        results_file.write_text(json.dumps(results, indent=2), encoding='utf-8')
        print(f"\n[INFO] Results saved to: {results_file.relative_to(self.project_root)}")
        
        return results


def main():
    """Main function"""
    project_root = Path(__file__).parent.parent.parent
    
    validator = DeploymentValidator(project_root)
    results = validator.run_all_validations()
    
    # Exit with error code if validation failed
    if not results['summary']['all_passed'] or results['summary']['total_errors'] > 0:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()

