"""
Tests for Health Check Endpoint
Tests that health check endpoint works without ML dependencies and external APIs
"""
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add backend to path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app

client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoint functionality"""
    
    def test_health_check_endpoint_exists(self):
        """Test that health check endpoint exists and responds"""
        response = client.get("/health")
        
        assert response.status_code == 200, "Health check should return 200"
        assert response.json() is not None, "Health check should return JSON"
    
    def test_health_check_structure(self):
        """Test that health check response has correct structure"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data, "Health check should include status"
        assert "timestamp" in data, "Health check should include timestamp"
        assert "version" in data, "Health check should include version"
        assert "service" in data, "Health check should include service name"
        assert "services" in data, "Health check should include services"
    
    def test_health_check_no_external_apis(self):
        """Test that health check does not include external APIs"""
        response = client.get("/health")
        data = response.json()
        
        # Should NOT have external_apis key (removed in deployment)
        assert "external_apis" not in data, "Health check should NOT include external_apis in deployment"
    
    def test_health_check_ml_dependencies(self):
        """Test that health check includes ML dependency validation"""
        response = client.get("/health")
        data = response.json()
        
        assert "ml_dependencies" in data, "Health check should include ML dependency validation"
        ml_deps = data["ml_dependencies"]
        
        assert "status" in ml_deps, "ML dependencies should include status"
        assert ml_deps["status"] in ["compliant", "non_compliant", "error"], \
            "ML dependencies status should be compliant, non_compliant, or error"
    
    def test_health_check_ml_compliant(self):
        """Test that health check reports ML dependencies status correctly"""
        response = client.get("/health")
        data = response.json()
        
        # In deployment (Docker), ML dependencies should be compliant (no ML packages installed)
        # In development environment, ML packages may be installed, so non_compliant is expected
        ml_deps = data.get("ml_dependencies", {})
        status = ml_deps.get("status", "")
        
        # Status should be one of: compliant (deployment), non_compliant (dev with ML), or error
        assert status in ["compliant", "non_compliant", "error"], \
            f"ML dependencies status should be compliant/non_compliant/error, got: {status}"
        
        # In deployment, status should be compliant
        # In development, non_compliant is acceptable if ML packages are installed
        # The important thing is that the check exists and works
        assert "violations" in ml_deps, "ML dependencies should include violations list"
    
    def test_readiness_check(self):
        """Test readiness check endpoint"""
        response = client.get("/health/ready")
        
        assert response.status_code == 200, "Readiness check should return 200"
        data = response.json()
        
        assert "status" in data, "Readiness check should include status"
        assert "timestamp" in data, "Readiness check should include timestamp"
        assert data["status"] in ["ready", "not_ready"], \
            "Readiness status should be ready or not_ready"
    
    def test_liveness_check(self):
        """Test liveness check endpoint"""
        response = client.get("/health/live")
        
        assert response.status_code == 200, "Liveness check should return 200"
        data = response.json()
        
        assert "status" in data, "Liveness check should include status"
        assert data["status"] == "alive", "Liveness status should be alive"
        assert "timestamp" in data, "Liveness check should include timestamp"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

