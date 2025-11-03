"""
Retrain all models with enhanced Brazilian dataset (56 features).

Compares performance before/after Brazilian feature integration.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Model imports
from demand_forecasting.models.arima_model import ARIMAForecaster
from demand_forecasting.models.prophet_model import ProphetForecaster
from demand_forecasting.models.lstm_model import LSTMForecaster
from demand_forecasting.models.ensemble import EnsembleForecaster

# Evaluation metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "models" / "trained"
RESULTS_DIR = BASE_DIR / "results"

# Create directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_enhanced_dataset() -> pd.DataFrame:
    """Load unified dataset with Brazilian factors."""
    file_path = DATA_DIR / "unified_dataset_with_brazilian_factors.csv"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Enhanced dataset not found: {file_path}")
    
    print(f"[+] Loading enhanced dataset: {file_path}")
    df = pd.read_csv(file_path, low_memory=False)
    
    # Convert date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='ISO8601', errors='coerce')
        df = df.set_index('date')
    
    print(f"[OK] Loaded {len(df):,} rows × {len(df.columns)} columns")
    return df


def prepare_features(df: pd.DataFrame, target_col: str = 'quantity') -> tuple:
    """
    Prepare features and target for model training.
    
    Returns:
        X: Feature matrix (excluding target and metadata)
        y: Target series
        feature_names: List of feature names
    """
    # Identify target column
    if target_col not in df.columns:
        # Try common alternatives
        alternatives = ['Quantity_Consumed', 'order_demand', 'Order_Demand', 
                       'demand', 'units_sold', 'Units_Sold']
        for alt in alternatives:
            if alt in df.columns:
                target_col = alt
                break
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found. Available: {list(df.columns)[:10]}")
    
    # Get target
    y = df[target_col].copy()
    
    # Exclude target and metadata columns from features
    exclude_cols = [
        target_col, 'item_id', 'item_name', 'site_id', 'dataset_source',
        'date', 'timestamp', 'id', 'UID', 'Product ID', 'SKU_ID'
    ]
    
    # Get feature columns
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    # Select features
    X = df[feature_cols].copy()
    
    # Handle missing values (forward fill for time series)
    X = X.ffill().bfill()  # Forward fill then backward fill
    X = X.fillna(0)  # Fill any remaining NaN with 0
    
    # Remove any infinite values
    X = X.replace([np.inf, -np.inf], 0)
    
    print(f"[+] Prepared {len(feature_cols)} features")
    print(f"[+] Feature categories:")
    print(f"    - Climate: {len([c for c in feature_cols if 'temp' in c.lower() or 'precip' in c.lower() or 'humid' in c.lower()])}")
    print(f"    - Economic: {len([c for c in feature_cols if 'inflation' in c.lower() or 'exchange' in c.lower() or 'economic' in c.lower()])}")
    print(f"    - IoT: {len([c for c in feature_cols if 'iot' in c.lower()])}")
    print(f"    - Fiber: {len([c for c in feature_cols if 'fiber' in c.lower()])}")
    print(f"    - Operators: {len([c for c in feature_cols if 'market' in c.lower() or 'operator' in c.lower() or '5g' in c.lower()])}")
    print(f"    - Temporal: {len([c for c in feature_cols if 'month' in c.lower() or 'year' in c.lower() or 'holiday' in c.lower() or 'weekend' in c.lower()])}")
    print(f"    - Other: {len([c for c in feature_cols if not any(k in c.lower() for k in ['temp', 'precip', 'humid', 'inflation', 'exchange', 'economic', 'iot', 'fiber', 'market', 'operator', '5g', 'month', 'year', 'holiday', 'weekend'])])}")
    
    return X, y, feature_cols


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate evaluation metrics."""
    # Remove any NaN or infinite values
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    y_true_clean = y_true[mask]
    y_pred_clean = y_pred[mask]
    
    if len(y_true_clean) == 0:
        return {
            'rmse': np.inf,
            'mae': np.inf,
            'mape': np.inf,
            'r2': -np.inf,
            'n_samples': 0
        }
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_true_clean, y_pred_clean))
    mae = mean_absolute_error(y_true_clean, y_pred_clean)
    
    # MAPE (Mean Absolute Percentage Error)
    with np.errstate(divide='ignore', invalid='ignore'):
        mape = np.mean(np.abs((y_true_clean - y_pred_clean) / (y_true_clean + 1e-8))) * 100
    
    # R²
    r2 = r2_score(y_true_clean, y_pred_clean)
    
    return {
        'rmse': float(rmse),
        'mae': float(mae),
        'mape': float(mape),
        'r2': float(r2),
        'n_samples': int(len(y_true_clean))
    }


def train_arima_model(X: pd.DataFrame, y: pd.Series, train_size: float = 0.8) -> Dict:
    """Train ARIMA model."""
    print("\n" + "="*60)
    print("TRAINING ARIMA MODEL")
    print("="*60)
    
    try:
        # ARIMA works with time series, so we use the target series directly
        series = y.sort_index()
        
        # Split data
        split_idx = int(len(series) * train_size)
        train_series = series[:split_idx]
        test_series = series[split_idx:]
        
        print(f"[+] Training on {len(train_series):,} samples")
        print(f"[+] Testing on {len(test_series):,} samples")
        
        # Initialize and fit
        model = ARIMAForecaster()
        fitted_model = model.auto_fit(train_series)
        
        # Forecast
        print("[+] Generating forecasts...")
        forecast = model.forecast(len(test_series))
        
        # Evaluate
        metrics = evaluate_model(test_series.values, forecast.values if isinstance(forecast, pd.Series) else forecast)
        
        print(f"[OK] ARIMA Results:")
        print(f"    RMSE: {metrics['rmse']:.4f}")
        print(f"    MAE:  {metrics['mae']:.4f}")
        print(f"    MAPE: {metrics['mape']:.2f}%")
        print(f"    R²:   {metrics['r2']:.4f}")
        
        return {
            'model': 'ARIMA',
            'fitted': True,
            'metrics': metrics,
            'model_obj': model
        }
    except Exception as e:
        print(f"[!] ARIMA training failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            'model': 'ARIMA',
            'fitted': False,
            'error': str(e),
            'metrics': None
        }


def train_prophet_model(X: pd.DataFrame, y: pd.Series, feature_cols: List[str], 
                        train_size: float = 0.8) -> Dict:
    """Train Prophet model with Brazilian features."""
    print("\n" + "="*60)
    print("TRAINING PROPHET MODEL")
    print("="*60)
    
    try:
        # Prepare Prophet format
        df = pd.DataFrame({'y': y.values, 'ds': y.index})
        df = df.sort_values('ds')
        
        # Add external regressors (select top features)
        # Select numerical features only
        numerical_features = X.select_dtypes(include=[np.number]).columns
        
        # Limit to top 20 features to avoid overfitting
        if len(numerical_features) > 20:
            # Calculate correlation with target
            correlations = abs(X[numerical_features].corrwith(y))
            top_features = correlations.nlargest(20).index.tolist()
        else:
            top_features = numerical_features.tolist()
        
        # Add selected features
        for feat in top_features:
            if feat in X.columns:
                df[feat] = X[feat].values
        
        # Split data
        split_idx = int(len(df) * train_size)
        train_df = df[:split_idx].copy()
        test_df = df[split_idx:].copy()
        
        print(f"[+] Training on {len(train_df):,} samples")
        print(f"[+] Testing on {len(test_df):,} samples")
        print(f"[+] Using {len(top_features)} external regressors")
        
        # Initialize and fit
        model = ProphetForecaster(country='BR')
        fitted_model = model.fit(train_df, quantity_col='y', regressors=top_features)
        
        # Prepare future dataframe with regressors
        future_df = model.model.make_future_dataframe(periods=len(test_df))
        
        # Add regressors to future
        for feat in top_features:
            if feat in test_df.columns:
                # Extend last known value for future periods
                last_value = train_df[feat].iloc[-1]
                future_df[feat] = last_value
        
        # Forecast
        print("[+] Generating forecasts...")
        forecast_df = model.model.predict(future_df)
        
        # Get test predictions
        test_forecast = forecast_df['yhat'].iloc[-len(test_df):].values
        test_actual = test_df['y'].values
        
        # Evaluate
        metrics = evaluate_model(test_actual, test_forecast)
        
        print(f"[OK] Prophet Results:")
        print(f"    RMSE: {metrics['rmse']:.4f}")
        print(f"    MAE:  {metrics['mae']:.4f}")
        print(f"    MAPE: {metrics['mape']:.2f}%")
        print(f"    R²:   {metrics['r2']:.4f}")
        
        return {
            'model': 'Prophet',
            'fitted': True,
            'metrics': metrics,
            'model_obj': model,
            'regressors_used': top_features
        }
    except Exception as e:
        print(f"[!] Prophet training failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            'model': 'Prophet',
            'fitted': False,
            'error': str(e),
            'metrics': None
        }


def train_lstm_model(X: pd.DataFrame, y: pd.Series, train_size: float = 0.8) -> Dict:
    """Train LSTM model."""
    print("\n" + "="*60)
    print("TRAINING LSTM MODEL")
    print("="*60)
    
    try:
        # LSTM works with time series, so we use the target series directly
        series = y.sort_index()
        
        print(f"[+] Training on {int(len(series) * train_size):,} samples")
        print(f"[+] Testing on {int(len(series) * (1 - train_size)):,} samples")
        
        # Initialize and fit
        model = LSTMForecaster(look_back=30, units=50, epochs=50, batch_size=32, verbose=1)
        fitted_model = model.fit(series, validation_split=1 - train_size)
        
        # Forecast on test set
        split_idx = int(len(series) * train_size)
        test_series = series[split_idx:]
        
        print("[+] Generating forecasts...")
        forecast = model.forecast(series[:split_idx], steps=len(test_series))
        
        # Evaluate
        metrics = evaluate_model(test_series.values, forecast)
        
        print(f"[OK] LSTM Results:")
        print(f"    RMSE: {metrics['rmse']:.4f}")
        print(f"    MAE:  {metrics['mae']:.4f}")
        print(f"    MAPE: {metrics['mape']:.2f}%")
        print(f"    R²:   {metrics['r2']:.4f}")
        
        return {
            'model': 'LSTM',
            'fitted': True,
            'metrics': metrics,
            'model_obj': model
        }
    except Exception as e:
        print(f"[!] LSTM training failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            'model': 'LSTM',
            'fitted': False,
            'error': str(e),
            'metrics': None
        }


def train_ensemble_model(X: pd.DataFrame, y: pd.Series, feature_cols: List[str],
                         train_size: float = 0.8) -> Dict:
    """Train Ensemble model."""
    print("\n" + "="*60)
    print("TRAINING ENSEMBLE MODEL")
    print("="*60)
    
    try:
        # Prepare data
        df = pd.DataFrame({'Quantity_Consumed': y.values}, index=y.index)
        
        # Add external regressors
        numerical_features = X.select_dtypes(include=[np.number]).columns
        if len(numerical_features) > 20:
            correlations = abs(X[numerical_features].corrwith(y))
            top_features = correlations.nlargest(20).index.tolist()
        else:
            top_features = numerical_features.tolist()
        
        exog_df = X[top_features].copy()
        
        # Split data
        split_idx = int(len(df) * train_size)
        train_df = df[:split_idx].copy()
        train_exog = exog_df[:split_idx].copy()
        test_df = df[split_idx:].copy()
        test_exog = exog_df[split_idx:].copy()
        
        print(f"[+] Training on {len(train_df):,} samples")
        print(f"[+] Testing on {len(test_df):,} samples")
        
        # Initialize and fit
        model = EnsembleForecaster(use_lstm=True)
        fit_results = model.fit(train_df, quantity_col='Quantity_Consumed', exog=train_exog)
        
        print(f"[+] Fit results: {fit_results}")
        
        # Forecast
        print("[+] Generating forecasts...")
        forecast = model.forecast(
            steps=len(test_df),
            df=train_df,
            exog=test_exog,
            quantity_col='Quantity_Consumed'
        )
        
        # Evaluate
        metrics = evaluate_model(test_df['Quantity_Consumed'].values, forecast.values)
        
        print(f"[OK] Ensemble Results:")
        print(f"    RMSE: {metrics['rmse']:.4f}")
        print(f"    MAE:  {metrics['mae']:.4f}")
        print(f"    MAPE: {metrics['mape']:.2f}%")
        print(f"    R²:   {metrics['r2']:.4f}")
        
        return {
            'model': 'Ensemble',
            'fitted': True,
            'metrics': metrics,
            'model_obj': model,
            'fit_results': fit_results
        }
    except Exception as e:
        print(f"[!] Ensemble training failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            'model': 'Ensemble',
            'fitted': False,
            'error': str(e),
            'metrics': None
        }


def save_results(results: Dict, feature_count: int):
    """Save training results to JSON."""
    results_file = RESULTS_DIR / f"model_retraining_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    summary = {
        'timestamp': datetime.now().isoformat(),
        'dataset': 'unified_dataset_with_brazilian_factors',
        'feature_count': feature_count,
        'models': {}
    }
    
    for result in results:
        model_name = result['model']
        summary['models'][model_name] = {
            'fitted': result['fitted'],
            'metrics': result.get('metrics'),
            'error': result.get('error')
        }
    
    with open(results_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n[OK] Results saved to: {results_file}")
    return results_file


def generate_comparison_report(results: Dict):
    """Generate comparison report."""
    print("\n" + "="*80)
    print("MODEL COMPARISON SUMMARY")
    print("="*80)
    
    # Create comparison table
    comparison = []
    for result in results:
        if result['fitted'] and result.get('metrics'):
            metrics = result['metrics']
            comparison.append({
                'Model': result['model'],
                'RMSE': f"{metrics['rmse']:.4f}",
                'MAE': f"{metrics['mae']:.4f}",
                'MAPE': f"{metrics['mape']:.2f}%",
                'R²': f"{metrics['r2']:.4f}",
                'N_Samples': metrics['n_samples']
            })
    
    if comparison:
        comparison_df = pd.DataFrame(comparison)
        print("\n" + comparison_df.to_string(index=False))
        
        # Save to CSV
        report_file = RESULTS_DIR / f"model_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        comparison_df.to_csv(report_file, index=False)
        print(f"\n[OK] Comparison report saved to: {report_file}")
    
    return comparison


def main():
    """Main retraining pipeline."""
    print("="*80)
    print("MODEL RETRAINING WITH BRAZILIAN DATA")
    print("Nova Corrente - Demand Forecasting System")
    print("="*80)
    
    # Load data
    df = load_enhanced_dataset()
    
    # Prepare features
    X, y, feature_cols = prepare_features(df)
    
    print(f"\n[+] Total features: {len(feature_cols)}")
    print(f"[+] Dataset shape: {df.shape}")
    print(f"[+] Date range: {df.index.min()} to {df.index.max()}")
    
    # Train models
    results = []
    
    # 1. ARIMA
    arima_result = train_arima_model(X, y)
    results.append(arima_result)
    
    # 2. Prophet
    prophet_result = train_prophet_model(X, y, feature_cols)
    results.append(prophet_result)
    
    # 3. LSTM
    lstm_result = train_lstm_model(X, y)
    results.append(lstm_result)
    
    # 4. Ensemble
    ensemble_result = train_ensemble_model(X, y, feature_cols)
    results.append(ensemble_result)
    
    # Save results
    results_file = save_results(results, len(feature_cols))
    
    # Generate comparison
    comparison = generate_comparison_report(results)
    
    print("\n" + "="*80)
    print("[SUCCESS] MODEL RETRAINING COMPLETE")
    print("="*80)
    print(f"\n[INFO] Results saved to: {RESULTS_DIR}")
    print(f"[INFO] Models trained with {len(feature_cols)} features")
    
    return results, comparison


if __name__ == "__main__":
    main()

