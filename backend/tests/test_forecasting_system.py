"""
Test Script for Nova Corrente Demand Forecasting System
Validates all components and integration
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add demand_forecasting to path
sys.path.insert(0, str(Path(__file__).parent))

from demand_forecasting.data_loader import DataLoader
from demand_forecasting.models.arima_model import ARIMAForecaster
from demand_forecasting.models.prophet_model import ProphetForecaster
from demand_forecasting.models.lstm_model import LSTMForecaster
from demand_forecasting.pp_calculator import PPCalculator
from demand_forecasting.pipeline import DemandForecastingPipeline


def test_data_loader():
    """Test DataLoader component."""
    print("\n" + "=" * 60)
    print("TEST 1: Data Loader")
    print("=" * 60)
    
    try:
        # Create sample data
        np.random.seed(42)
        dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
        df = pd.DataFrame({
            'date': dates,
            'Item_ID': ['TEST-001'] * len(dates),
            'Quantity_Consumed': np.random.poisson(8, len(dates)),
            'Site_ID': ['SITE-001'] * len(dates),
            'Lead_Time': [14] * len(dates)
        })
        
        # Save sample
        test_file = 'test_demand_data.csv'
        df.to_csv(test_file, index=False)
        
        # Test loader
        loader = DataLoader(external_features=True)
        data_dict = loader.load_and_preprocess(test_file)
        
        # Validate
        assert len(data_dict) > 0, "Data dict should not be empty"
        assert 'TEST-001' in data_dict, "Item ID should be present"
        
        # Check features
        item_df = data_dict['TEST-001']
        expected_features = ['year', 'month', 'weekend', 'holiday', 'temperature']
        for feature in expected_features:
            assert feature in item_df.columns, f"Feature {feature} should be present"
        
        print("✅ Data Loader test passed")
        return True
        
    except Exception as e:
        print(f"❌ Data Loader test failed: {e}")
        return False


def test_arima_model():
    """Test ARIMA model component."""
    print("\n" + "=" * 60)
    print("TEST 2: ARIMA Model")
    print("=" * 60)
    
    try:
        # Create sample series
        np.random.seed(42)
        dates = pd.date_range(start='2022-01-01', end='2024-06-30', freq='D')
        series = pd.Series(
            np.random.poisson(8, len(dates)) + 2 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365),
            index=dates
        )
        
        # Split train/test
        train_size = int(len(series) * 0.8)
        train_series = series.iloc[:train_size]
        test_series = series.iloc[train_size:]
        
        # Test ARIMA
        forecaster = ARIMAForecaster(seasonal=True, m=7)
        model_info = forecaster.fit(train_series)
        
        # Validate
        assert forecaster.fitted_model is not None, "Model should be fitted"
        assert 'order' in model_info, "Model info should contain order"
        
        # Forecast
        forecast_df = forecaster.forecast(steps=len(test_series))
        assert len(forecast_df) == len(test_series), "Forecast length should match test"
        
        # Evaluate
        metrics = forecaster.evaluate(test_series, forecast_df['forecast'])
        assert 'RMSE' in metrics, "Metrics should contain RMSE"
        assert 'MAE' in metrics, "Metrics should contain MAE"
        assert 'MAPE' in metrics, "Metrics should contain MAPE"
        
        print(f"✅ ARIMA test passed (RMSE: {metrics['RMSE']:.2f}, MAPE: {metrics['MAPE']:.2f}%)")
        return True
        
    except Exception as e:
        print(f"❌ ARIMA test failed: {e}")
        return False


def test_prophet_model():
    """Test Prophet model component."""
    print("\n" + "=" * 60)
    print("TEST 3: Prophet Model")
    print("=" * 60)
    
    try:
        # Create sample data
        np.random.seed(42)
        dates = pd.date_range(start='2022-01-01', end='2024-06-30', freq='D')
        df = pd.DataFrame({
            'date': dates,
            'Quantity_Consumed': np.random.poisson(8, len(dates)) + 
                                2 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365),
            'temperature': np.random.uniform(15, 40, len(dates))
        })
        df.set_index('date', inplace=True)
        
        # Split train/test
        train_size = int(len(df) * 0.8)
        train_df = df.iloc[:train_size]
        test_df = df.iloc[train_size:]
        
        # Test Prophet
        forecaster = ProphetForecaster()
        model_info = forecaster.fit(train_df, target_col='Quantity_Consumed')
        
        # Validate
        assert forecaster.model is not None, "Model should be fitted"
        
        # Forecast
        forecast_df = forecaster.forecast(periods=len(test_df))
        assert len(forecast_df) == len(test_df), "Forecast length should match test"
        
        # Evaluate
        metrics = forecaster.evaluate(test_df, forecast_df, target_col='Quantity_Consumed')
        assert 'RMSE' in metrics, "Metrics should contain RMSE"
        assert metrics['MAPE'] < 100, "MAPE should be reasonable"
        
        print(f"✅ Prophet test passed (RMSE: {metrics['RMSE']:.2f}, MAPE: {metrics['MAPE']:.2f}%)")
        return True
        
    except Exception as e:
        print(f"❌ Prophet test failed: {e}")
        return False


def test_lstm_model():
    """Test LSTM model component (if TensorFlow available)."""
    print("\n" + "=" * 60)
    print("TEST 4: LSTM Model")
    print("=" * 60)
    
    try:
        # Create sample series
        np.random.seed(42)
        dates = pd.date_range(start='2022-01-01', end='2024-06-30', freq='D')
        series = pd.Series(
            np.random.poisson(8, len(dates)) + 2 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365),
            index=dates
        )
        
        # Test LSTM
        forecaster = LSTMForecaster(look_back=30, epochs=10, verbose=0)
        forecaster.fit(series, validation_split=0.2)
        
        # Validate
        assert forecaster.fitted, "Model should be fitted"
        assert forecaster.model is not None, "Model should exist"
        
        # Forecast
        forecast = forecaster.forecast(series, steps=30)
        assert len(forecast) == 30, "Forecast length should be 30"
        
        print(f"✅ LSTM test passed (Forecast: {forecast.mean():.2f})")
        return True
        
    except ImportError:
        print("⚠️  LSTM test skipped (TensorFlow not available)")
        return True  # Not a failure, just optional
    except Exception as e:
        print(f"❌ LSTM test failed: {e}")
        return False


def test_pp_calculator():
    """Test PP Calculator component."""
    print("\n" + "=" * 60)
    print("TEST 5: PP Calculator")
    print("=" * 60)
    
    try:
        # Create sample forecast
        forecast = pd.DataFrame({
            'forecast': np.random.poisson(8, 30),
            'lower': np.random.poisson(6, 30),
            'upper': np.random.poisson(10, 30)
        })
        
        # Test calculator
        calculator = PPCalculator(service_level=0.95)
        pp_info = calculator.calculate_reorder_point(
            forecast=forecast,
            lead_time=14,
            current_stock=100,
            std_demand=2.5
        )
        
        # Validate
        assert 'reorder_point' in pp_info, "PP info should contain reorder_point"
        assert 'safety_stock' in pp_info, "PP info should contain safety_stock"
        assert pp_info['reorder_point'] > 0, "PP should be positive"
        assert pp_info['safety_stock'] > 0, "Safety stock should be positive"
        
        # Test alert
        alert = calculator.check_alert(pp_info)
        if pp_info['current_stock'] <= pp_info['reorder_point']:
            assert alert is not None, "Alert should be generated"
        
        print(f"✅ PP Calculator test passed (PP: {pp_info['reorder_point']:.2f}, SS: {pp_info['safety_stock']:.2f})")
        return True
        
    except Exception as e:
        print(f"❌ PP Calculator test failed: {e}")
        return False


def test_pipeline():
    """Test complete pipeline."""
    print("\n" + "=" * 60)
    print("TEST 6: Complete Pipeline")
    print("=" * 60)
    
    try:
        # Create sample data
        np.random.seed(42)
        dates = pd.date_range(start='2022-01-01', end='2024-06-30', freq='D')
        df = pd.DataFrame({
            'date': dates,
            'Item_ID': ['TEST-001'] * len(dates),
            'Quantity_Consumed': np.random.poisson(8, len(dates)),
            'Site_ID': ['SITE-001'] * len(dates),
            'Lead_Time': [14] * len(dates)
        })
        
        # Save sample
        test_file = 'test_pipeline_data.csv'
        df.to_csv(test_file, index=False)
        
        # Configuration
        config = {
            'service_level': 0.95,
            'ensemble_weights': {'ARIMA': 0.5, 'Prophet': 0.5},
            'forecast_horizon': 30,
            'use_ensemble': True
        }
        
        # Test pipeline
        pipeline = DemandForecastingPipeline(config=config)
        results = pipeline.run(
            data_file=test_file,
            lead_times={'TEST-001': 14},
            current_stocks={'TEST-001': 100},
            output_dir='test_output'
        )
        
        # Validate
        assert 'forecasts' in results, "Results should contain forecasts"
        assert 'pp_results' in results, "Results should contain pp_results"
        assert 'reports' in results, "Results should contain reports"
        
        # Check reports exist
        for report_type, file_path in results['reports'].items():
            assert Path(file_path).exists(), f"Report {report_type} should exist"
        
        print("✅ Pipeline test passed")
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Nova Corrente Demand Forecasting System - Tests")
    print("=" * 60)
    
    tests = [
        test_data_loader,
        test_arima_model,
        test_prophet_model,
        test_lstm_model,
        test_pp_calculator,
        test_pipeline
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

