"""
Test Suite for Deployment ML Ops Constraint Validation

This test suite validates that deployment code has NO ML dependencies,
ML imports, or ML endpoints.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.validation.check_ml_dependencies import check_file_for_ml_dependencies
from scripts.validation.check_ml_endpoints import check_file_for_ml_endpoints
from scripts.validation.check_ml_imports import check_file_for_ml_imports


class TestMLDependencies:
    """Test ML dependencies validation"""
    
    def test_requirements_deployment_no_ml(self):
        """Test that requirements_deployment.txt has no ML dependencies"""
        req_file = project_root / 'backend' / 'requirements_deployment.txt'
        
        if not req_file.exists():
            pytest.skip("requirements_deployment.txt not found")
        
        is_compliant, violations = check_file_for_ml_dependencies(req_file, allowed=False)
        
        assert is_compliant, f"ML dependencies found in requirements_deployment.txt: {violations}"
    
    def test_dockerfile_deployment_no_ml(self):
        """Test that Dockerfile.backend.deployment has no ML dependencies"""
        dockerfile = project_root / 'infrastructure' / 'docker' / 'Dockerfile.backend.deployment'
        
        if not dockerfile.exists():
            pytest.skip("Dockerfile.backend.deployment not found")
        
        is_compliant, violations = check_file_for_ml_dependencies(dockerfile, allowed=False)
        
        assert is_compliant, f"ML dependencies found in Dockerfile: {violations}"


class TestMLEndpoints:
    """Test ML endpoints validation"""
    
    def test_api_routes_no_ml_endpoints(self):
        """Test that API routes have no ML endpoints"""
        api_dir = project_root / 'backend' / 'api'
        
        if not api_dir.exists():
            pytest.skip("backend/api directory not found")
        
        violations_found = []
        for py_file in api_dir.glob('*.py'):
            is_compliant, violations = check_file_for_ml_endpoints(py_file)
            if not is_compliant:
                violations_found.extend(violations)
        
        assert len(violations_found) == 0, f"ML endpoints found in API routes: {violations_found}"
    
    def test_data_refresh_endpoint_exists(self):
        """Test that data refresh endpoint exists (manual trigger only)"""
        data_refresh_file = project_root / 'backend' / 'api' / 'routes' / 'data_refresh.py'
        
        if not data_refresh_file.exists():
            pytest.skip("data_refresh.py not found")
        
        content = data_refresh_file.read_text()
        
        # Should have POST /refresh endpoint
        assert '/refresh' in content or '/data/refresh' in content, "Data refresh endpoint not found"
        
        # Should require auth
        assert 'verify_api_key' in content or 'Depends' in content, "Data refresh endpoint should require auth"


class TestMLImports:
    """Test ML imports validation"""
    
    def test_deployment_code_no_ml_imports(self):
        """Test that deployment code has no ML imports"""
        deployment_dirs = [
            project_root / 'backend' / 'api',
            project_root / 'backend' / 'app',
        ]
        
        violations_found = []
        for deploy_dir in deployment_dirs:
            if not deploy_dir.exists():
                continue
            
            for py_file in deploy_dir.rglob('*.py'):
                # Skip ML code directories
                if 'ml' in str(py_file) or 'train' in str(py_file):
                    continue
                
                is_compliant, violations = check_file_for_ml_imports(py_file)
                if not is_compliant:
                    violations_found.extend(violations)
        
        assert len(violations_found) == 0, f"ML imports found in deployment code: {violations_found}"


class TestConfig:
    """Test configuration validation"""
    
    def test_config_no_ml_settings(self):
        """Test that config.py has no ML-related settings"""
        config_file = project_root / 'backend' / 'app' / 'config.py'
        
        if not config_file.exists():
            pytest.skip("config.py not found")
        
        content = config_file.read_text()
        
        # Should NOT have these ML-related settings
        ml_settings = [
            'MODELS_DIR',
            'MODEL_CACHE_ENABLED',
            'MODEL_CACHE_TTL',
            'MLFLOW_TRACKING_URI',
        ]
        
        violations = []
        for setting in ml_settings:
            # Check if it's commented out or in a comment
            if setting in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if setting in line and not line.strip().startswith('#'):
                        violations.append(f"Line {i+1}: {line.strip()}")
        
        # Should have ML_RESULTS_PATH (read-only path)
        assert 'ML_RESULTS_PATH' in content, "ML_RESULTS_PATH should be in config"
        
        # Should have DATA_REFRESH_ENABPOINT_ENABLED
        assert 'DATA_REFRESH' in content, "DATA_REFRESH_ENABPOINT_ENABLED should be in config"


class TestDockerCompose:
    """Test Docker Compose validation"""
    
    def test_docker_compose_no_scheduler(self):
        """Test that docker-compose.yml has no scheduler service"""
        compose_file = project_root / 'docker-compose.yml'
        
        if not compose_file.exists():
            pytest.skip("docker-compose.yml not found")
        
        content = compose_file.read_text()
        
        # Should NOT have scheduler service
        assert 'scheduler:' not in content or '# NOTE: Scheduler service REMOVED' in content, \
            "Scheduler service should be removed from docker-compose.yml"
    
    def test_docker_compose_has_minio(self):
        """Test that docker-compose.yml has MinIO service"""
        compose_file = project_root / 'docker-compose.yml'
        
        if not compose_file.exists():
            pytest.skip("docker-compose.yml not found")
        
        content = compose_file.read_text()
        
        # Should have MinIO service
        assert 'minio:' in content.lower(), "MinIO service should be in docker-compose.yml"
    
    def test_docker_compose_uses_deployment_dockerfile(self):
        """Test that docker-compose.yml uses deployment Dockerfile"""
        compose_file = project_root / 'docker-compose.yml'
        
        if not compose_file.exists():
            pytest.skip("docker-compose.yml not found")
        
        content = compose_file.read_text()
        
        # Should use Dockerfile.backend.deployment
        assert 'Dockerfile.backend.deployment' in content, \
            "docker-compose.yml should use Dockerfile.backend.deployment"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

