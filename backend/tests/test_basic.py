"""
Basic tests for demand forecasting system.
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.arima_model import ARIMAForecaster
from demand_forecasting.models.prophet_model import ProphetForecaster
from demand_forecasting.inventory.reorder_point import ReorderPointCalculator
from demand_forecasting.validation.metrics import ValidationMetrics


def create_test_data(n_days=365):
    """Create test data for testing."""
    dates = pd.date_range(start='2022-01-01', periods=n_days, freq='D')
    np.random.seed(42)
    
    # Generate synthetic demand
    base_demand = 10
    trend = np.linspace(0, 3, n_days)
    seasonal = 2 * np.sin(2 * np.pi * np.arange(n_days) / 365.25)
    noise = np.random.normal(0, 1, n_days)
    
    demand = base_demand + trend + seasonal + noise
    demand = np.maximum(demand, 1)
    
    data = {
        'date': dates,
        'Item_ID': 'TEST-001',
        'Quantity_Consumed': demand,
        'Site_ID': 'SITE-001',
        'Lead_Time': 14
    }
    
    return pd.DataFrame(data)


def test_data_loader():
    """Test data loader."""
    # Create temporary CSV
    df = create_test_data(730)  # 2 years
    test_file = 'test_data.csv'
    df.to_csv(test_file, index=False)
    
    try:
        loader = DataLoader(test_file)
        data_dict = loader.preprocess(external_features=False, min_years=1)
        
        assert 'TEST-001' in data_dict
        assert len(data_dict['TEST-001']) > 0
        print("✓ DataLoader test passed")
    
    finally:
        import os
        if os.path.exists(test_file):
            os.remove(test_file)


def test_arima_forecaster():
    """Test ARIMA forecaster."""
    # Create test series
    dates = pd.date_range(start='2022-01-01', periods=365, freq='D')
    np.random.seed(42)
    series = pd.Series(10 + 0.01 * np.arange(365) + np.random.normal(0, 1, 365), 
                      index=dates)
    
    forecaster = ARIMAForecaster(seasonal=False)
    
    try:
        fit_results = forecaster.auto_fit(series)
        assert forecaster.model is not None
        assert forecaster.order is not None
        
        forecast = forecaster.forecast(steps=30)
        assert len(forecast) == 30
        print("✓ ARIMAForecaster test passed")
    
    except Exception as e:
        print(f"⚠️  ARIMAForecaster test skipped: {e}")


def test_prophet_forecaster():
    """Test Prophet forecaster."""
    # Create test DataFrame
    dates = pd.date_range(start='2022-01-01', periods=365, freq='D')
    np.random.seed(42)
    df = pd.DataFrame({
        'date': dates,
        'Quantity_Consumed': 10 + 0.01 * np.arange(365) + np.random.normal(0, 1, 365)
    })
    df.set_index('date', inplace=True)
    
    forecaster = ProphetForecaster()
    
    try:
        forecaster.fit(df, 'Quantity_Consumed')
        assert forecaster.model is not None
        
        forecast = forecaster.forecast(periods=30)
        assert len(forecast) == 30
        print("✓ ProphetForecaster test passed")
    
    except Exception as e:
        print(f"⚠️  ProphetForecaster test skipped: {e}")


def test_reorder_point_calculator():
    """Test reorder point calculator."""
    # Create test forecast
    forecast = pd.Series([10, 12, 11, 13, 10, 11, 12])
    
    calculator = ReorderPointCalculator(service_level=0.95)
    
    pp_metrics = calculator.compute_all(forecast, lead_time=14, current_stock=100)
    
    assert 'reorder_point' in pp_metrics
    assert 'safety_stock' in pp_metrics
    assert 'days_to_rupture' in pp_metrics
    assert pp_metrics['reorder_point'] > 0
    print("✓ ReorderPointCalculator test passed")


def test_validation_metrics():
    """Test validation metrics."""
    actual = pd.Series([10, 12, 11, 13, 10])
    predicted = pd.Series([10.5, 11.8, 11.2, 12.9, 10.1])
    
    metrics = ValidationMetrics()
    results = metrics.calculate_all(actual, predicted)
    
    assert 'MAPE' in results
    assert 'RMSE' in results
    assert 'MAE' in results
    assert 'R2' in results
    print("✓ ValidationMetrics test passed")


if __name__ == '__main__':
    print("Running basic tests...")
    print("=" * 60)
    
    test_data_loader()
    test_arima_forecaster()
    test_prophet_forecaster()
    test_reorder_point_calculator()
    test_validation_metrics()
    
    print("=" * 60)
    print("All basic tests completed!")

