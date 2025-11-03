"""
Performance benchmarking script.
Tests system performance and generates benchmarks.
"""
import sys
import time
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.arima_model import ARIMAForecaster
from demand_forecasting.models.prophet_model import ProphetForecaster
from demand_forecasting.models.lstm_model import LSTMForecaster
from demand_forecasting.models.ensemble import EnsembleForecaster
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


class PerformanceBenchmark:
    """Benchmark system performance."""
    
    def __init__(self):
        """Initialize benchmark."""
        self.results = []
    
    def benchmark_data_loading(self, data_path: str, iterations: int = 5):
        """Benchmark data loading performance."""
        times = []
        
        for i in range(iterations):
            start = time.time()
            loader = DataLoader(data_path)
            data_dict = loader.preprocess(external_features=True, min_years=1)
            elapsed = time.time() - start
            times.append(elapsed)
        
        return {
            'operation': 'data_loading',
            'iterations': iterations,
            'mean_time': np.mean(times),
            'std_time': np.std(times),
            'min_time': np.min(times),
            'max_time': np.max(times),
            'items_loaded': len(data_dict) if 'data_dict' in locals() else 0
        }
    
    def benchmark_model_training(self, series: pd.Series, model_type: str):
        """Benchmark model training performance."""
        times = []
        success = False
        
        try:
            start = time.time()
            
            if model_type == 'ARIMA':
                forecaster = ARIMAForecaster(seasonal=False)
                forecaster.auto_fit(series)
            
            elif model_type == 'Prophet':
                forecaster = ProphetForecaster()
                df = pd.DataFrame({'date': series.index, 'Quantity_Consumed': series.values})
                df.set_index('date', inplace=True)
                forecaster.fit(df, 'Quantity_Consumed')
            
            elif model_type == 'LSTM':
                forecaster = LSTMForecaster(epochs=10)  # Reduced for benchmark
                forecaster.fit(series)
            
            elapsed = time.time() - start
            times.append(elapsed)
            success = True
        
        except Exception as e:
            return {
                'operation': f'model_training_{model_type}',
                'success': False,
                'error': str(e)
            }
        
        return {
            'operation': f'model_training_{model_type}',
            'success': success,
            'training_time': elapsed,
            'data_points': len(series)
        }
    
    def benchmark_forecast_generation(self, forecaster, series: pd.Series, steps: int = 30):
        """Benchmark forecast generation."""
        times = []
        
        for _ in range(5):
            start = time.time()
            try:
                forecast = forecaster.forecast(series, steps)
                elapsed = time.time() - start
                times.append(elapsed)
            except Exception as e:
                return {
                    'operation': 'forecast_generation',
                    'success': False,
                    'error': str(e)
                }
        
        return {
            'operation': 'forecast_generation',
            'success': True,
            'mean_time': np.mean(times),
            'std_time': np.std(times),
            'steps': steps
        }
    
    def run_full_benchmark(self, data_path: str):
        """Run complete performance benchmark."""
        print("\n" + "="*60)
        print("Performance Benchmark")
        print("="*60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'benchmarks': []
        }
        
        # Load data
        print("\n[1/4] Benchmarking data loading...")
        try:
            load_result = self.benchmark_data_loading(data_path, iterations=3)
            results['benchmarks'].append(load_result)
            print(f"  Mean time: {load_result['mean_time']:.2f}s")
            print(f"  Items loaded: {load_result['items_loaded']}")
        except Exception as e:
            print(f"  [ERROR] {e}")
        
        # Load data for models
        try:
            loader = DataLoader(data_path)
            data_dict = loader.preprocess(min_years=1)
            item_id = list(data_dict.keys())[0]
            df = data_dict[item_id]
            
            # Get series
            quantity_col = None
            for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
                if col in df.columns:
                    quantity_col = col
                    break
            if quantity_col is None:
                quantity_col = df.select_dtypes(include=['number']).columns[0]
            
            series = df[quantity_col].tail(365)  # Last year for testing
            
        except Exception as e:
            print(f"[ERROR] Could not load data: {e}")
            return results
        
        # Benchmark ARIMA
        print("\n[2/4] Benchmarking ARIMA...")
        try:
            arima_result = self.benchmark_model_training(series, 'ARIMA')
            results['benchmarks'].append(arima_result)
            if arima_result.get('success'):
                print(f"  Training time: {arima_result['training_time']:.2f}s")
        except Exception as e:
            print(f"  [ERROR] {e}")
        
        # Benchmark Prophet
        print("\n[3/4] Benchmarking Prophet...")
        try:
            prophet_result = self.benchmark_model_training(series, 'Prophet')
            results['benchmarks'].append(prophet_result)
            if prophet_result.get('success'):
                print(f"  Training time: {prophet_result['training_time']:.2f}s")
        except Exception as e:
            print(f"  [ERROR] {e}")
        
        # Benchmark LSTM (if available)
        print("\n[4/4] Benchmarking LSTM...")
        try:
            lstm_result = self.benchmark_model_training(series, 'LSTM')
            results['benchmarks'].append(lstm_result)
            if lstm_result.get('success'):
                print(f"  Training time: {lstm_result['training_time']:.2f}s")
        except Exception as e:
            print(f"  [WARNING] LSTM not available: {e}")
        
        # Summary
        print("\n" + "="*60)
        print("Benchmark Summary")
        print("="*60)
        
        successful = [b for b in results['benchmarks'] if b.get('success', True)]
        print(f"Successful benchmarks: {len(successful)}/{len(results['benchmarks'])}")
        
        for bench in successful:
            if 'training_time' in bench:
                print(f"{bench['operation']}: {bench['training_time']:.2f}s")
            elif 'mean_time' in bench:
                print(f"{bench['operation']}: {bench['mean_time']:.2f}s")
        
        print("="*60)
        
        # Save results
        results_file = Path('logs') / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_file.parent.mkdir(exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved: {results_file}")
        
        return results


def main():
    """Main benchmark execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Performance benchmark')
    parser.add_argument('--data', type=str, default='data/nova_corrente_demand.csv',
                       help='Path to data file')
    
    args = parser.parse_args()
    
    benchmark = PerformanceBenchmark()
    results = benchmark.run_full_benchmark(args.data)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

