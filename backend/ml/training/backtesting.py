"""
Backtesting module for demand forecasting models.
Implements walk-forward validation and performance analysis.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from demand_forecasting.validation.metrics import ValidationMetrics
import warnings
warnings.filterwarnings('ignore')


class Backtester:
    """Backtesting framework for demand forecasting models."""
    
    def __init__(self, initial_train_size: float = 0.7, step_size: int = 30):
        """
        Initialize backtester.
        
        Args:
            initial_train_size: Initial training set proportion (default: 0.7)
            step_size: Number of days to step forward each iteration (default: 30)
        """
        self.initial_train_size = initial_train_size
        self.step_size = step_size
        self.metrics = ValidationMetrics()
        self.results = []
    
    def walk_forward_validation(self, series: pd.Series, forecaster,
                               exog: Optional[pd.DataFrame] = None,
                               max_periods: Optional[int] = None) -> Dict:
        """
        Perform walk-forward validation.
        
        Args:
            series: Time series data
            forecaster: Forecaster object with fit() and forecast() methods
            exog: External regressors (optional)
            max_periods: Maximum number of validation periods (None = all)
        
        Returns:
            Dictionary with backtesting results
        """
        print(f"\n{'='*60}")
        print("Walk-Forward Validation")
        print(f"{'='*60}")
        
        # Initialize
        n = len(series)
        initial_train_size = int(n * self.initial_train_size)
        
        all_predictions = []
        all_actuals = []
        period_results = []
        
        # Walk forward
        current_train_end = initial_train_size
        period = 1
        
        while current_train_end < n:
            # Train/test split
            train_end = min(current_train_end, n)
            test_start = train_end
            test_end = min(test_start + self.step_size, n)
            
            if test_start >= test_end:
                break
            
            train_series = series.iloc[:train_end]
            test_series = series.iloc[test_start:test_end]
            
            # External regressors
            train_exog = None
            test_exog = None
            if exog is not None:
                train_exog = exog.iloc[:train_end] if len(exog) >= train_end else None
                test_exog = exog.iloc[test_start:test_end] if len(exog) >= test_end else None
            
            print(f"\nPeriod {period}: Training on {len(train_series)} days, "
                  f"Testing on {len(test_series)} days")
            
            try:
                # Fit model
                if hasattr(forecaster, 'auto_fit'):
                    forecaster.auto_fit(train_series, train_exog)
                elif hasattr(forecaster, 'fit'):
                    forecaster.fit(train_series, train_exog)
                
                # Generate forecast
                forecast_steps = len(test_series)
                if hasattr(forecaster, 'forecast'):
                    if test_exog is not None:
                        fc = forecaster.forecast(forecast_steps, test_exog)
                    else:
                        fc = forecaster.forecast(forecast_steps)
                    
                    # Convert to Series if needed
                    if isinstance(fc, np.ndarray):
                        fc = pd.Series(fc, index=test_series.index[:len(fc)])
                    elif isinstance(fc, pd.DataFrame):
                        fc = fc['yhat'] if 'yhat' in fc.columns else fc.iloc[:, 0]
                    
                    # Align indices
                    fc = fc.reindex(test_series.index)
                    fc = fc.fillna(method='ffill').fillna(method='bfill')
                    
                    # Calculate metrics
                    metrics = self.metrics.calculate_all(test_series, fc)
                    
                    # Store results
                    period_results.append({
                        'period': period,
                        'train_end': train_end,
                        'test_start': test_start,
                        'test_end': test_end,
                        'train_size': len(train_series),
                        'test_size': len(test_series),
                        'metrics': metrics
                    })
                    
                    all_predictions.append(fc)
                    all_actuals.append(test_series)
                    
                    print(f"  MAPE: {metrics['MAPE_percent']:.2f}%, "
                          f"RMSE: {metrics['RMSE']:.2f}, "
                          f"MAE: {metrics['MAE']:.2f}")
                
            except Exception as e:
                print(f"  ✗ Error in period {period}: {e}")
                period_results.append({
                    'period': period,
                    'train_end': train_end,
                    'test_start': test_start,
                    'test_end': test_end,
                    'error': str(e)
                })
            
            # Move forward
            current_train_end += self.step_size
            period += 1
            
            if max_periods and period > max_periods:
                break
        
        # Aggregate results
        if all_predictions:
            combined_predictions = pd.concat(all_predictions)
            combined_actuals = pd.concat(all_actuals)
            
            # Align indices
            common_index = combined_actuals.index.intersection(combined_predictions.index)
            combined_predictions = combined_predictions.loc[common_index]
            combined_actuals = combined_actuals.loc[common_index]
            
            overall_metrics = self.metrics.calculate_all(combined_actuals, combined_predictions)
            
            # Period-wise statistics
            period_mape = [r['metrics']['MAPE_percent'] 
                          for r in period_results if 'metrics' in r]
            period_rmse = [r['metrics']['RMSE'] 
                          for r in period_results if 'metrics' in r]
            
            results = {
                'overall_metrics': overall_metrics,
                'period_results': period_results,
                'period_count': len(period_results),
                'successful_periods': len([r for r in period_results if 'metrics' in r]),
                'mean_mape': np.mean(period_mape) if period_mape else None,
                'std_mape': np.std(period_mape) if period_mape else None,
                'mean_rmse': np.mean(period_rmse) if period_rmse else None,
                'std_rmse': np.std(period_rmse) if period_rmse else None,
                'predictions': combined_predictions,
                'actuals': combined_actuals
            }
            
            print(f"\n{'-'*60}")
            print("Overall Backtesting Results:")
            print(f"{'-'*60}")
            print(f"Periods: {results['period_count']} ({results['successful_periods']} successful)")
            print(f"Overall MAPE: {overall_metrics['MAPE_percent']:.2f}%")
            print(f"Overall RMSE: {overall_metrics['RMSE']:.2f}")
            print(f"Overall MAE: {overall_metrics['MAE']:.2f}")
            print(f"Mean Period MAPE: {results['mean_mape']:.2f}% ± {results['std_mape']:.2f}%")
            print(f"{'-'*60}")
            
            self.results.append(results)
            
            return results
        
        else:
            print("\n⚠️  No successful forecasts generated")
            return {
                'period_results': period_results,
                'period_count': len(period_results),
                'successful_periods': 0
            }
    
    def compare_models(self, series: pd.Series, forecasters: Dict[str, any],
                      exog: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Compare multiple models using walk-forward validation.
        
        Args:
            series: Time series data
            forecasters: Dictionary of {model_name: forecaster_object}
            exog: External regressors (optional)
        
        Returns:
            DataFrame with comparison results
        """
        print(f"\n{'='*60}")
        print("Model Comparison")
        print(f"{'='*60}")
        
        comparison_results = []
        
        for model_name, forecaster in forecasters.items():
            print(f"\nTesting {model_name}...")
            
            # Create fresh forecaster instance
            if hasattr(forecaster, '__class__'):
                forecaster_instance = forecaster.__class__(**forecaster.__dict__)
            else:
                forecaster_instance = forecaster
            
            results = self.walk_forward_validation(series, forecaster_instance, exog)
            
            if 'overall_metrics' in results:
                comparison_results.append({
                    'Model': model_name,
                    'MAPE (%)': results['overall_metrics']['MAPE_percent'],
                    'RMSE': results['overall_metrics']['RMSE'],
                    'MAE': results['overall_metrics']['MAE'],
                    'R²': results['overall_metrics']['R2'],
                    'Periods': results['successful_periods'],
                    'Mean MAPE': results.get('mean_mape'),
                    'Std MAPE': results.get('std_mape')
                })
        
        # Create comparison DataFrame
        if comparison_results:
            comparison_df = pd.DataFrame(comparison_results)
            comparison_df = comparison_df.sort_values('MAPE (%)')
            
            print(f"\n{'-'*60}")
            print("Model Comparison Summary:")
            print(f"{'-'*60}")
            print(comparison_df.to_string(index=False))
            print(f"{'-'*60}")
            
            return comparison_df
        
        else:
            print("⚠️  No comparison results available")
            return pd.DataFrame()

