"""
Model training script with advanced features.
Supports incremental training, model persistence, and performance tracking.
"""
import sys
import os
import pickle
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demand_forecasting.data.loader import DataLoader
from demand_forecasting.models.ensemble import EnsembleForecaster
from demand_forecasting.models.arima_model import ARIMAForecaster
from demand_forecasting.models.prophet_model import ProphetForecaster
from demand_forecasting.models.lstm_model import LSTMForecaster
from demand_forecasting.validation.metrics import ValidationMetrics
from demand_forecasting.utils.config import Config
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    """Advanced model training with persistence and tracking."""
    
    def __init__(self, config_path: str = None):
        """Initialize model trainer."""
        self.config = Config(config_path)
        self.models_dir = Path('models')
        self.models_dir.mkdir(exist_ok=True)
        self.training_history = []
    
    def train_item_model(self, item_id: str, df: pd.DataFrame, quantity_col: str,
                        save_model: bool = True) -> dict:
        """
        Train models for a specific item.
        
        Args:
            item_id: Item identifier
            df: Historical data DataFrame
            quantity_col: Name of quantity column
            save_model: Whether to save trained models
        
        Returns:
            Dictionary with training results
        """
        print(f"\n{'='*60}")
        print(f"Training models for {item_id}")
        print(f"{'='*60}")
        
        # Split data
        split_idx = int(len(df) * 0.8)
        train = df.iloc[:split_idx]
        test = df.iloc[split_idx:]
        
        print(f"Training data: {len(train)} days")
        print(f"Test data: {len(test)} days")
        
        results = {
            'item_id': item_id,
            'train_size': len(train),
            'test_size': len(test),
            'training_date': datetime.now().isoformat(),
            'models': {}
        }
        
        # External regressors
        exog = None
        exog_cols = ['temperature', 'holiday']
        available_exog = [col for col in exog_cols if col in df.columns]
        if available_exog:
            exog = df[available_exog]
            train_exog = exog.loc[train.index]
            test_exog = exog.loc[test.index]
        else:
            train_exog = None
            test_exog = None
        
        series = train[quantity_col] if quantity_col in train.columns else train.iloc[:, 0]
        test_series = test[quantity_col] if quantity_col in test.columns else test.iloc[:, 0]
        
        metrics = ValidationMetrics()
        
        # Train and evaluate ARIMA
        print("\n[1/3] Training ARIMA model...")
        try:
            arima = ARIMAForecaster(seasonal=True)
            arima.auto_fit(series, train_exog)
            
            # Generate test forecast
            arima_fc = arima.forecast(len(test), test_exog)
            arima_metrics = metrics.calculate_all(test_series, arima_fc)
            
            results['models']['ARIMA'] = {
                'status': 'success',
                'order': arima.order,
                'metrics': arima_metrics
            }
            
            print(f"  ✓ ARIMA - MAPE: {arima_metrics['MAPE_percent']:.2f}%")
            
            # Save model
            if save_model:
                model_path = self.models_dir / f"{item_id}_arima.pkl"
                with open(model_path, 'wb') as f:
                    pickle.dump(arima, f)
        
        except Exception as e:
            print(f"  ✗ ARIMA failed: {e}")
            results['models']['ARIMA'] = {'status': 'failed', 'error': str(e)}
        
        # Train and evaluate Prophet
        print("\n[2/3] Training Prophet model...")
        try:
            prophet = ProphetForecaster()
            prophet.fit(train, quantity_col, available_exog)
            
            # Generate test forecast
            prophet_fc_df = prophet.forecast(len(test), regressors=test_exog)
            prophet_fc = prophet_fc_df['yhat'].values
            prophet_metrics = metrics.calculate_all(test_series, pd.Series(prophet_fc))
            
            results['models']['Prophet'] = {
                'status': 'success',
                'metrics': prophet_metrics
            }
            
            print(f"  ✓ Prophet - MAPE: {prophet_metrics['MAPE_percent']:.2f}%")
            
            # Save model
            if save_model:
                model_path = self.models_dir / f"{item_id}_prophet.pkl"
                with open(model_path, 'wb') as f:
                    pickle.dump(prophet, f)
        
        except Exception as e:
            print(f"  ✗ Prophet failed: {e}")
            results['models']['Prophet'] = {'status': 'failed', 'error': str(e)}
        
        # Train and evaluate LSTM
        print("\n[3/3] Training LSTM model...")
        try:
            lstm = LSTMForecaster(
                look_back=self.config.get('models.lstm.look_back', 30),
                units=self.config.get('models.lstm.units', 50),
                epochs=self.config.get('models.lstm.epochs', 50)
            )
            lstm.fit(series)
            
            # Generate test forecast
            lstm_fc = lstm.forecast(series, len(test))
            lstm_metrics = metrics.calculate_all(test_series, pd.Series(lstm_fc))
            
            results['models']['LSTM'] = {
                'status': 'success',
                'metrics': lstm_metrics
            }
            
            print(f"  ✓ LSTM - MAPE: {lstm_metrics['MAPE_percent']:.2f}%")
            
            # Save model
            if save_model:
                model_path = self.models_dir / f"{item_id}_lstm.pkl"
                with open(model_path, 'wb') as f:
                    pickle.dump(lstm, f)
        
        except Exception as e:
            print(f"  ✗ LSTM failed: {e}")
            results['models']['LSTM'] = {'status': 'failed', 'error': str(e)}
        
        # Train ensemble
        print("\n[4/4] Training ensemble...")
        try:
            ensemble = EnsembleForecaster(
                weights=self.config.get('models.ensemble.weights'),
                use_lstm=self.config.get('models.ensemble.use_lstm', True)
            )
            ensemble.fit(train, quantity_col, train_exog)
            
            # Generate test forecast
            ensemble_fc = ensemble.forecast(len(test), train, test_exog, quantity_col)
            ensemble_metrics = metrics.calculate_all(test_series, ensemble_fc)
            
            results['models']['Ensemble'] = {
                'status': 'success',
                'metrics': ensemble_metrics
            }
            
            print(f"  ✓ Ensemble - MAPE: {ensemble_metrics['MAPE_percent']:.2f}%")
            
            # Save ensemble
            if save_model:
                model_path = self.models_dir / f"{item_id}_ensemble.pkl"
                with open(model_path, 'wb') as f:
                    pickle.dump(ensemble, f)
        
        except Exception as e:
            print(f"  ✗ Ensemble failed: {e}")
            results['models']['Ensemble'] = {'status': 'failed', 'error': str(e)}
        
        # Summary
        print(f"\n{'-'*60}")
        print("Training Summary:")
        print(f"{'-'*60}")
        for model_name, model_result in results['models'].items():
            if model_result.get('status') == 'success':
                mape = model_result['metrics']['MAPE_percent']
                print(f"{model_name:15s} MAPE: {mape:6.2f}%")
        print(f"{'-'*60}")
        
        return results
    
    def train_all_items(self, data_path: str, save_models: bool = True) -> list:
        """
        Train models for all items in dataset.
        
        Args:
            data_path: Path to data file
            save_models: Whether to save trained models
        
        Returns:
            List of training results
        """
        # Load data
        loader = DataLoader(data_path)
        data_dict = loader.preprocess(
            external_features=self.config.get('data.external_features', True),
            min_years=self.config.get('data.min_years', 2)
        )
        
        print(f"\n{'='*60}")
        print(f"Training models for {len(data_dict)} items")
        print(f"{'='*60}")
        
        results = []
        
        for item_id, df in data_dict.items():
            # Get quantity column
            quantity_col = None
            for col in ['Quantity_Consumed', 'quantity', 'demand', 'sales']:
                if col in df.columns:
                    quantity_col = col
                    break
            
            if quantity_col is None:
                quantity_col = df.select_dtypes(include=['number']).columns[0]
            
            item_results = self.train_item_model(item_id, df, quantity_col, save_models)
            results.append(item_results)
            
            # Save training history
            self.training_history.append(item_results)
        
        # Save training summary
        self._save_training_summary(results)
        
        return results
    
    def _save_training_summary(self, results: list):
        """Save training summary to JSON."""
        summary_path = self.models_dir / 'training_summary.json'
        
        summary = {
            'training_date': datetime.now().isoformat(),
            'items': len(results),
            'results': results
        }
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Training summary saved: {summary_path}")


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Train demand forecasting models')
    parser.add_argument('--data', type=str, default='data/nova_corrente_demand.csv',
                       help='Path to data file')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to config file')
    parser.add_argument('--item', type=str, default=None,
                       help='Train specific item only')
    parser.add_argument('--no-save', action='store_true',
                       help='Do not save trained models')
    
    args = parser.parse_args()
    
    trainer = ModelTrainer(args.config)
    
    if args.item:
        # Train single item
        loader = DataLoader(args.data)
        data_dict = loader.preprocess()
        
        if args.item not in data_dict:
            print(f"Error: Item {args.item} not found in data")
            return
        
        df = data_dict[args.item]
        quantity_col = df.select_dtypes(include=['number']).columns[0]
        
        trainer.train_item_model(args.item, df, quantity_col, not args.no_save)
    else:
        # Train all items
        trainer.train_all_items(args.data, not args.no_save)


if __name__ == '__main__':
    main()









