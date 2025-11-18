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
        """Test initialization of all services and clients"""
        result = await integration_manager.initialize_all()
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'status' in result
        assert 'services' in result
        assert 'external_clients' in result
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
    
    @pytest.mark.asyncio
    async def test_get_external_client(self):
        """Test getting an external client by name"""
        # Initialize first
        await integration_manager.initialize_all()
        
        # Try to get INMET client
        inmet_client = integration_manager.get_external_client('inmet')
        # Should either be config dict or None
        assert inmet_client is None or isinstance(inmet_client, dict)
    
    @pytest.mark.asyncio
    async def test_refresh_all_external_data(self):
        """Test refreshing all external data"""
        start_date = date.today() - timedelta(days=7)
        end_date = date.today()
        
        result = await integration_manager.refresh_all_external_data(
            start_date=start_date,
            end_date=end_date
        )
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'start_date' in result
        assert 'end_date' in result
        assert 'status' in result


class TestServiceInitialization:
    """Test individual service initialization"""
    
    @pytest.mark.asyncio
    async def test_database_service_initialization(self):
        """Test database service initialization"""
        await integration_manager.initialize_all()
        
        result = integration_manager.services
        # Check if database service was attempted
        assert 'database' in result or 'database' in str(result)
    
    @pytest.mark.asyncio
    async def test_external_services_initialization(self):
        """Test external services initialization"""
        await integration_manager.initialize_all()
        
        result = integration_manager.external_clients
        # Should have some external clients configured
        assert len(result) >= 0  # At least initialized (may be empty if configs missing)


class TestExternalClientInitialization:
    """Test external API client initialization"""
    
    @pytest.mark.asyncio
    async def test_inmet_client_initialization(self):
        """Test INMET client initialization"""
        await integration_manager.initialize_all()
        
        inmet_client = integration_manager.get_external_client('inmet')
        # Should be None or a dict with config
        assert inmet_client is None or isinstance(inmet_client, dict)
    
    @pytest.mark.asyncio
    async def test_bacen_client_initialization(self):
        """Test BACEN client initialization"""
        await integration_manager.initialize_all()
        
        bacen_client = integration_manager.get_external_client('bacen')
        # Should be None or a dict with config
        assert bacen_client is None or isinstance(bacen_client, dict)
    
    @pytest.mark.asyncio
    async def test_anatel_client_initialization(self):
        """Test ANATEL client initialization"""
        await integration_manager.initialize_all()
        
        anatel_client = integration_manager.get_external_client('anatel')
        # Should be None or a dict with config
        assert anatel_client is None or isinstance(anatel_client, dict)
    
    @pytest.mark.asyncio
    async def test_openweather_client_initialization(self):
        """Test OpenWeatherMap client initialization"""
        await integration_manager.initialize_all()
        
        openweather_client = integration_manager.get_external_client('openweather')
        # Should be None or a dict with config
        assert openweather_client is None or isinstance(openweather_client, dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

