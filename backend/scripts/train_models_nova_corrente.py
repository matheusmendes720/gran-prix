"""
Train ML models for Nova Corrente forecasting
- ARIMA baseline
- Prophet with external regressors
- XGBoost for feature-based forecasting
- Evaluate MAPE < 15%
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).parent.parent.parent
TRAIN_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_train.csv"
VAL_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_validation.csv"
TEST_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_test.csv"
MODELS_DIR = PROJECT_ROOT / "models" / "nova_corrente"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR = PROJECT_ROOT / "data" / "processed" / "nova_corrente"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    """Load train/validation/test datasets"""
    print("=" * 80)
    print("CARREGANDO DADOS PARA TREINAMENTO")
    print("=" * 80)
    
    train_df = pd.read_csv(TRAIN_FILE, parse_dates=['date'])
    val_df = pd.read_csv(VAL_FILE, parse_dates=['date'])
    test_df = pd.read_csv(TEST_FILE, parse_dates=['date'])
    
    print(f"\n[INFO] Train: {len(train_df):,} registros")
    print(f"[INFO] Validation: {len(val_df):,} registros")
    print(f"[INFO] Test: {len(test_df):,} registros")
    
    return train_df, val_df, test_df

def prepare_time_series(df, familia):
    """Prepare time series data for a specific family"""
    family_df = df[df['familia'] == familia].copy()
    
    if len(family_df) == 0:
        return None, None
    
    # Aggregate by date (daily)
    ts_df = family_df.groupby('date').agg({
        'quantidade': 'sum',
        'lead_time_days': 'mean',
        'site_id': 'nunique',
        'item_id': 'nunique'
    }).reset_index()
    
    ts_df = ts_df.sort_values('date')
    ts_df = ts_df.set_index('date')
    
    # Ensure daily frequency
    date_range = pd.date_range(start=ts_df.index.min(), end=ts_df.index.max(), freq='D')
    ts_df = ts_df.reindex(date_range)
    
    # Fill missing dates
    ts_df['quantidade'] = ts_df['quantidade'].fillna(0)
    for col in ts_df.columns:
        if col != 'quantidade':
            ts_df[col] = ts_df[col].fillna(method='ffill').fillna(0)
    
    y = ts_df['quantidade'].values
    X = ts_df[['lead_time_days', 'site_id', 'item_id']].values if len(ts_df.columns) > 1 else None
    
    return y, X

def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error"""
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    
    # Ensure arrays have same length
    min_len = min(len(y_true), len(y_pred))
    y_true = y_true[:min_len]
    y_pred = y_pred[:min_len]
    
    # Avoid division by zero - use symmetric MAPE for zero values
    mask = y_true != 0
    if mask.sum() == 0:
        # All zeros - calculate symmetric MAPE
        mask = np.ones(len(y_true), dtype=bool)
        denominator = (np.abs(y_true) + np.abs(y_pred)) / 2 + 1e-8
        mape = np.mean(np.abs(y_true - y_pred) / denominator) * 100
    else:
        # Regular MAPE for non-zero values
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / (y_true[mask] + 1e-8))) * 100
    
    # Cap MAPE at reasonable value
    mape = min(mape, 1000.0)
    
    return mape

def train_simple_baseline(y_train, y_val, y_test):
    """Train simple baseline models"""
    print("\n[TRAINING] Simple Baselines")
    
    results = {}
    
    # Naive forecast (last value)
    y_pred_naive = np.full(len(y_val), y_train[-1] if len(y_train) > 0 else 0)
    mape_naive = calculate_mape(y_val, y_pred_naive)
    results['naive'] = {'mape': mape_naive, 'predictions': y_pred_naive.tolist()}
    print(f"  Naive (last value): MAPE = {mape_naive:.2f}%")
    
    # Moving average (7 days)
    if len(y_train) >= 7:
        ma7 = np.mean(y_train[-7:])
        y_pred_ma7 = np.full(len(y_val), ma7)
        mape_ma7 = calculate_mape(y_val, y_pred_ma7)
        results['moving_average_7'] = {'mape': mape_ma7, 'predictions': y_pred_ma7.tolist()}
        print(f"  Moving Average (7 days): MAPE = {mape_ma7:.2f}%")
    
    # Mean forecast
    mean_val = np.mean(y_train) if len(y_train) > 0 else 0
    y_pred_mean = np.full(len(y_val), mean_val)
    mape_mean = calculate_mape(y_val, y_pred_mean)
    results['mean'] = {'mape': mape_mean, 'predictions': y_pred_mean.tolist()}
    print(f"  Mean: MAPE = {mape_mean:.2f}%")
    
    return results

def train_linear_trend(y_train, y_val):
    """Train linear trend model"""
    print("\n[TRAINING] Linear Trend")
    
    try:
        x_train = np.arange(len(y_train))
        x_val = np.arange(len(y_train), len(y_train) + len(y_val))
        
        # Fit linear regression
        coeffs = np.polyfit(x_train, y_train, 1)
        y_pred = np.polyval(coeffs, x_val)
        
        # Ensure non-negative
        y_pred = np.maximum(y_pred, 0)
        
        mape = calculate_mape(y_val, y_pred)
        print(f"  Linear Trend: MAPE = {mape:.2f}%")
        
        return {'mape': mape, 'predictions': y_pred.tolist(), 'coefficients': coeffs.tolist()}
    except Exception as e:
        print(f"  [ERROR] Linear Trend failed: {e}")
        return None

def train_xgboost_model(train_df, val_df, familia):
    """Train XGBoost model"""
    print("\n[TRAINING] XGBoost")
    
    try:
        from xgboost import XGBRegressor
        
        # Filter family
        train_family = train_df[train_df['familia'] == familia].copy()
        val_family = val_df[val_df['familia'] == familia].copy()
        
        if len(train_family) == 0 or len(val_family) == 0:
            return None
        
        # Select features
        feature_cols = [
            'month', 'day', 'weekday', 'is_weekend', 'quarter',
            'month_sin', 'month_cos', 'day_of_year_sin', 'day_of_year_cos',
            'lead_time_days', 'family_frequency', 'site_frequency',
            'family_demand_ma_7', 'family_demand_ma_30'
        ]
        
        # Get available features
        available_features = [col for col in feature_cols if col in train_family.columns]
        
        # Prepare data
        X_train = train_family[available_features].fillna(0)
        y_train = train_family['quantidade'].values
        
        X_val = val_family[available_features].fillna(0)
        y_val = val_family['quantidade'].values
        
        # Train model
        model = XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_val)
        y_pred = np.maximum(y_pred, 0)  # Ensure non-negative
        
        mape = calculate_mape(y_val, y_pred)
        print(f"  XGBoost: MAPE = {mape:.2f}%")
        
        # Save model
        model_file = MODELS_DIR / f"xgboost_{familia.replace(' ', '_')}.pkl"
        import joblib
        joblib.dump(model, model_file)
        
        return {
            'mape': mape,
            'predictions': y_pred.tolist(),
            'features': available_features,
            'feature_importance': dict(zip(available_features, model.feature_importances_.tolist())),
            'model_file': str(model_file)
        }
    except Exception as e:
        print(f"  [ERROR] XGBoost failed: {e}")
        return None

def train_prophet_model(train_df, val_df, familia):
    """Train Prophet model with external regressors"""
    print("\n[TRAINING] Prophet")
    
    try:
        from prophet import Prophet
        
        # Filter family
        train_family = train_df[train_df['familia'] == familia].copy()
        val_family = val_df[val_df['familia'] == familia].copy()
        
        if len(train_family) == 0 or len(val_family) == 0:
            return None
        
        # Prepare data for Prophet
        train_prophet = train_family.groupby('date').agg({
            'quantidade': 'sum',
            'lead_time_days': 'mean',
            'is_weekend': 'mean',
            'month': 'first'
        }).reset_index()
        
        train_prophet.columns = ['ds', 'y', 'lead_time', 'is_weekend', 'month']
        train_prophet = train_prophet.sort_values('ds')
        
        # Fill NaN values
        train_prophet['lead_time'] = train_prophet['lead_time'].fillna(train_prophet['lead_time'].median() if not train_prophet['lead_time'].isna().all() else 14)
        
        val_prophet = val_family.groupby('date').agg({
            'quantidade': 'sum',
            'lead_time_days': 'mean',
            'is_weekend': 'mean',
            'month': 'first'
        }).reset_index()
        val_prophet.columns = ['ds', 'y', 'lead_time', 'is_weekend', 'month']
        val_prophet = val_prophet.sort_values('ds')
        
        # Fill NaN values
        val_prophet['lead_time'] = val_prophet['lead_time'].fillna(val_prophet['lead_time'].median() if not val_prophet['lead_time'].isna().all() else 14)
        
        # Create Prophet model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode='additive'
        )
        
        # Add external regressors
        if 'lead_time' in train_prophet.columns:
            model.add_regressor('lead_time')
        
        # Fit model
        model.fit(train_prophet[['ds', 'y', 'lead_time']])
        
        # Predict validation period
        future = model.make_future_dataframe(periods=len(val_prophet))
        future['lead_time'] = pd.concat([
            train_prophet['lead_time'],
            val_prophet['lead_time']
        ]).values[:len(future)]
        
        forecast = model.predict(future)
        
        # Get validation predictions
        y_pred = forecast['yhat'].tail(len(val_prophet)).values
        y_pred = np.maximum(y_pred, 0)  # Ensure non-negative
        y_val = val_prophet['y'].values
        
        mape = calculate_mape(y_val, y_pred)
        print(f"  Prophet: MAPE = {mape:.2f}%")
        
        # Save model
        model_file = MODELS_DIR / f"prophet_{familia.replace(' ', '_')}.pkl"
        import joblib
        joblib.dump(model, model_file)
        
        return {
            'mape': mape,
            'predictions': y_pred.tolist(),
            'model_file': str(model_file)
        }
    except Exception as e:
        print(f"  [ERROR] Prophet failed: {e}")
        return None

def train_arima_model(y_train, y_val):
    """Train ARIMA model"""
    print("\n[TRAINING] ARIMA")
    
    try:
        from statsmodels.tsa.arima.model import ARIMA
        
        # Fit ARIMA(1,1,1) as baseline
        model = ARIMA(y_train, order=(1, 1, 1))
        fitted_model = model.fit()
        
        # Forecast validation period
        forecast = fitted_model.forecast(steps=len(y_val))
        y_pred = np.maximum(forecast, 0)  # Ensure non-negative
        
        mape = calculate_mape(y_val, y_pred)
        print(f"  ARIMA(1,1,1): MAPE = {mape:.2f}%")
        
        return {
            'mape': mape,
            'predictions': y_pred.tolist(),
            'order': [1, 1, 1]
        }
    except Exception as e:
        print(f"  [ERROR] ARIMA failed: {e}")
        return None

def train_all_models(train_df, val_df, test_df):
    """Train all models for all families"""
    print("\n" + "=" * 80)
    print("TREINANDO MODELOS PARA TODAS AS FAMÍLIAS")
    print("=" * 80)
    
    families = train_df['familia'].unique()
    all_results = {}
    
    for familia in families:
        print("\n" + "=" * 80)
        print(f"FAMÍLIA: {familia}")
        print("=" * 80)
        
        family_results = {}
        
        # Prepare time series
        y_train, X_train = prepare_time_series(train_df, familia)
        y_val, X_val = prepare_time_series(val_df, familia)
        y_test, X_test = prepare_time_series(test_df, familia)
        
        if y_train is None or len(y_train) < 7:
            print(f"  [SKIP] Dados insuficientes para {familia}")
            continue
        
        print(f"\n[INFO] Train: {len(y_train)} dias, média: {np.mean(y_train):.2f}")
        print(f"[INFO] Validation: {len(y_val)} dias, média: {np.mean(y_val):.2f}")
        
        # Train baselines
        baselines = train_simple_baseline(y_train, y_val, y_test)
        family_results['baselines'] = baselines
        
        # Train linear trend
        linear = train_linear_trend(y_train, y_val)
        if linear:
            family_results['linear_trend'] = linear
        
        # Train ARIMA
        arima = train_arima_model(y_train, y_val)
        if arima:
            family_results['arima'] = arima
        
        # Train Prophet
        prophet = train_prophet_model(train_df, val_df, familia)
        if prophet:
            family_results['prophet'] = prophet
        
        # Train XGBoost
        xgboost = train_xgboost_model(train_df, val_df, familia)
        if xgboost:
            family_results['xgboost'] = xgboost
        
        # Find best model
        best_mape = 100.0
        best_model = None
        for model_name, model_result in family_results.items():
            if isinstance(model_result, dict) and 'mape' in model_result:
                if model_result['mape'] < best_mape:
                    best_mape = model_result['mape']
                    best_model = model_name
        
        family_results['best_model'] = best_model
        family_results['best_mape'] = best_mape
        
        print(f"\n[RESULT] Melhor modelo: {best_model} com MAPE = {best_mape:.2f}%")
        
        all_results[familia] = family_results
    
    return all_results

def save_results(all_results):
    """Save training results"""
    print("\n" + "=" * 80)
    print("SALVANDO RESULTADOS")
    print("=" * 80)
    
    # Calculate summary
    summary = {
        'training_date': datetime.now().isoformat(),
        'families_trained': len(all_results),
        'families': {},
        'overall_best_mape': 100.0,
        'families_under_15_mape': 0
    }
    
    for familia, results in all_results.items():
        best_mape = results.get('best_mape', 100.0)
        
        summary['families'][familia] = {
            'best_model': results.get('best_model', 'N/A'),
            'best_mape': best_mape,
            'models_trained': list(results.keys())
        }
        
        if best_mape < summary['overall_best_mape']:
            summary['overall_best_mape'] = best_mape
        
        if best_mape < 15.0:
            summary['families_under_15_mape'] += 1
    
    # Save detailed results
    results_file = RESULTS_DIR / "model_training_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"[SUCCESS] Resultados detalhados: {results_file}")
    
    # Save summary
    summary_file = RESULTS_DIR / "model_training_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"[SUCCESS] Resumo: {summary_file}")
    
    return summary

def main():
    """Main training pipeline"""
    print("\n" + "=" * 80)
    print("PIPELINE DE TREINAMENTO DE MODELOS")
    print("=" * 80 + "\n")
    
    # Step 1: Load data
    train_df, val_df, test_df = load_data()
    
    # Step 2: Train models
    all_results = train_all_models(train_df, val_df, test_df)
    
    # Step 3: Save results
    summary = save_results(all_results)
    
    print("\n" + "=" * 80)
    print("TREINAMENTO CONCLUÍDO!")
    print("=" * 80)
    print(f"\n[RESUMO]")
    print(f"  - Famílias treinadas: {summary['families_trained']}")
    print(f"  - Famílias com MAPE < 15%: {summary['families_under_15_mape']}/{summary['families_trained']}")
    print(f"  - Melhor MAPE geral: {summary['overall_best_mape']:.2f}%")
    print(f"\n[RESULTADOS POR FAMÍLIA]")
    for familia, stats in summary['families'].items():
        print(f"  - {familia}: {stats['best_model']} (MAPE: {stats['best_mape']:.2f}%)")
    
    if summary['families_under_15_mape'] == summary['families_trained']:
        print(f"\n[SUCCESS] Todas as familias atendem requisito MAPE < 15%!")
    else:
        need_optimization = summary['families_trained'] - summary['families_under_15_mape']
        print(f"\n[WARNING] {need_optimization} familias precisam otimizacao")
    
    print(f"\n[PRÓXIMOS PASSOS]")
    print(f"  1. Criar ensemble model")
    print(f"  2. Validar em test set")
    print(f"  3. Deploy em produção")
    
    return all_results, summary

if __name__ == "__main__":
    main()

