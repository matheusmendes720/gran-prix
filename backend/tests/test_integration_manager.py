"""
Tests for Integration Manager
Tests the central coordinator for all services and external APIs
"""
import sys
from pathlib import Path
import pytest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

# Add backend to path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.integration_manager import integration_manager, IntegrationManager


class TestIntegrationManager:
    """Test Integration Manager functionality"""
    
    def test_integration_manager_exists(self):
        """Test integration manager instance exists"""
        assert integration_manager is not None
        assert isinstance(integration_manager, IntegrationManager)
    
    @pytest.mark.asyncio
    async def test_initialize_all(self):
        """Test initialization of all services (NO external clients in deployment)"""
        result = await integration_manager.initialize_all()
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'status' in result
        assert 'services' in result
        # ❌ REMOVED: external_clients (not used in deployment)
        assert 'timestamp' in result
    
    @pytest.mark.asyncio
    async def test_get_service(self):
        """Test getting a service by name"""
        # Initialize first
        await integration_manager.initialize_all()
        
        # Try to get database service
        db_service = integration_manager.get_service('database')
        # Should either be the service or None if not initialized
        assert db_service is None or hasattr(db_service, 'test_connection')
    
    # ❌ REMOVED: test_get_external_client (external clients not used in deployment)
    # ❌ REMOVED: test_refresh_all_external_data (external APIs disabled in deployment)


class TestServiceInitialization:
    """Test individual service initialization"""
    
    @pytest.mark.asyncio
    async def test_database_service_initialization(self):
        """Test database service initialization"""
        await integration_manager.initialize_all()
        
        result = integration_manager.services
        # Check if database service was attempted
        assert 'database' in result or 'database' in str(result)
    
    # ❌ REMOVED: test_external_services_initialization (external clients not used in deployment)


# ❌ REMOVED: TestExternalClientInitialization class (external clients not used in deployment)
# All external API client tests removed as they are disabled in deployment


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

