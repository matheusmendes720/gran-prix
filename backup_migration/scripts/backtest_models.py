"""
Backtesting script for demand forecasting models.
Performs walk-forward validation and model comparison.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.arima_model import ARIMAForecaster
from demand_forecasting.models.prophet_model import ProphetForecaster
from demand_forecasting.models.lstm_model import LSTMForecaster
from demand_forecasting.models.ensemble import EnsembleForecaster
from demand_forecasting.utils.backtesting import Backtester
from demand_forecasting.utils.config import Config
import pandas as pd
import argparse
import warnings
warnings.filterwarnings('ignore')


def main():
    """Main backtesting execution."""
    parser = argparse.ArgumentParser(description='Backtest demand forecasting models')
    parser.add_argument('--data', type=str, default='data/nova_corrente_demand.csv',
                       help='Path to data file')
    parser.add_argument('--item', type=str, default=None,
                       help='Backtest specific item only')
    parser.add_argument('--periods', type=int, default=None,
                       help='Maximum number of validation periods')
    parser.add_argument('--step', type=int, default=30,
                       help='Step size for walk-forward validation (days)')
    parser.add_argument('--compare', action='store_true',
                       help='Compare all models')
    
    args = parser.parse_args()
    
    config = Config()
    
    # Load data
    loader = DataLoader(args.data)
    data_dict = loader.preprocess(
        external_features=config.get('data.external_features', True),
        min_years=config.get('data.min_years', 2)
    )
    
    # Select items to backtest
    items_to_test = [args.item] if args.item else list(data_dict.keys())
    
    if args.item and args.item not in data_dict:
        print(f"Error: Item {args.item} not found in data")
        return
    
    backtester = Backtester(step_size=args.step)
    
    for item_id in items_to_test:
        print(f"\n{'='*80}")
        print(f"Backtesting: {item_id}")
        print(f"{'='*80}")
        
        df = data_dict[item_id]
        
        # Get quantity column
        quantity_col = None
        for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
            if col in df.columns:
                quantity_col = col
                break
        
        if quantity_col is None:
            quantity_col = df.select_dtypes(include=['number']).columns[0]
        
        series = df[quantity_col]
        
        # External regressors
        exog = None
        exog_cols = ['temperature', 'holiday']
        available_exog = [col for col in exog_cols if col in df.columns]
        if available_exog:
            exog = df[available_exog]
        
        if args.compare:
            # Compare all models
            forecasters = {
                'ARIMA': ARIMAForecaster(seasonal=True),
                'Prophet': ProphetForecaster(),
            }
            
            # Add LSTM if available
            try:
                forecasters['LSTM'] = LSTMForecaster()
            except ImportError:
                print("Warning: LSTM not available (TensorFlow required)")
            
            # Add ensemble
            forecasters['Ensemble'] = EnsembleForecaster(
                weights=config.get('models.ensemble.weights'),
                use_lstm=config.get('models.ensemble.use_lstm', True)
            )
            
            comparison = backtester.compare_models(series, forecasters, exog)
            
            # Save comparison results
            output_path = f"backtest_comparison_{item_id}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv"
            comparison.to_csv(output_path, index=False)
            print(f"\n✓ Comparison saved: {output_path}")
        
        else:
            # Test ensemble only
            print("\nTesting Ensemble Model...")
            ensemble = EnsembleForecaster(
                weights=config.get('models.ensemble.weights'),
                use_lstm=config.get('models.ensemble.use_lstm', True)
            )
            
            results = backtester.walk_forward_validation(
                series, ensemble, exog, max_periods=args.periods
            )
            
            # Save results
            if 'overall_metrics' in results:
                output_path = f"backtest_results_{item_id}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv"
                results_df = pd.DataFrame(results['period_results'])
                results_df.to_csv(output_path, index=False)
                print(f"\n✓ Results saved: {output_path}")


if __name__ == '__main__':
    main()

