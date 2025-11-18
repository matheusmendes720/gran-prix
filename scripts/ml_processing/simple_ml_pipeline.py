#!/usr/bin/env python3
"""
Simplified ML Pipeline for Nova Corrente Demand Forecasting
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json

# Machine Learning imports
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleMLPipeline:
    """Simplified ML pipeline for demand forecasting"""
    
    def __init__(self):
        self.data_dir = Path('data/outputs/nova_corrente')
        self.models_dir = Path('models/nova_corrente')
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        """Load processed Nova Corrente data"""
        try:
            # Try to load the enriched data
            data_file = self.data_dir / 'nova_corrente_enriched.csv'
            if data_file.exists():
                df = pd.read_csv(data_file)
                logger.info(f"Loaded enriched data: {len(df)} records")
            else:
                # Generate synthetic data for testing
                logger.warning("No data found, generating synthetic dataset")
                df = self.generate_synthetic_data()
            
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            # Generate synthetic data as fallback
            logger.info("Generating synthetic data as fallback")
            return self.generate_synthetic_data()
    
    def generate_synthetic_data(self):
        """Generate synthetic demand data for testing"""
        np.random.seed(42)
        
        # Generate 2 years of daily data
        dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
        n_records = len(dates)
        
        # Base demand with seasonality
        base_demand = 100 + 50 * np.sin(2 * np.pi * np.arange(n_records) / 365.25)
        base_demand += np.random.normal(0, 20, n_records)
        
        # External factors
        economic_impact = np.random.normal(0, 10, n_records)
        market_impact = np.random.normal(0, 5, n_records)
        climate_impact = np.random.normal(0, 3, n_records)
        logistic_impact = np.random.normal(0, 7, n_records)
        
        # Seasonal multiplier
        seasonal_multiplier = 1 + 0.3 * np.sin(2 * np.pi * np.arange(n_records) / 365.25)
        
        # Final demand
        demand = base_demand * seasonal_multiplier + economic_impact + market_impact + climate_impact + logistic_impact
        demand = np.maximum(demand, 10)  # Ensure positive demand
        
        df = pd.DataFrame({
            'date': dates,
            'year': pd.Series(dates).dt.year,
            'month': pd.Series(dates).dt.month,
            'day': pd.Series(dates).dt.day,
            'dayofweek': pd.Series(dates).dt.dayofweek,
            'is_weekend': (pd.Series(dates).dt.dayofweek >= 5).astype(int),
            'seasonal_multiplier': seasonal_multiplier,
            'base_demand': base_demand,
            'external_impact': economic_impact + market_impact + climate_impact + logistic_impact,
            'demand': demand,
            'family': np.random.choice(['EPI', 'FERRAMENTAS_E_EQUIPAMENTOS', 'FERRO_E_AÇO', 'MATERIAL_CIVIL', 'MATERIAL_ELETRICO'], n_records),
            'sku_id': [f'SKU_{i:04d}' for i in range(n_records)],
            'client_id': np.random.choice(['CLIENT_A', 'CLIENT_B', 'CLIENT_C'], n_records)
        })
        
        return df
    
    def prepare_features(self, df):
        """Prepare features for ML modeling"""
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        # Create lag features (use 'familia' instead of 'family')
        for lag in [1, 7, 30]:
            df[f'demand_lag_{lag}'] = df.groupby('familia')['quantidade'].shift(lag)
        
        # Create rolling window features
        for window in [7, 30]:
            df[f'demand_mean_{window}'] = df.groupby('familia')['quantidade'].transform(
                lambda x: x.rolling(window=window).mean()
            )
            df[f'demand_std_{window}'] = df.groupby('familia')['quantidade'].transform(
                lambda x: x.rolling(window=window).std()
            )
        
        # Drop rows with NaN values (from lag features)
        df = df.dropna()
        
        # Define feature columns based on actual data
        feature_cols = [
            'year', 'month', 'day', 'is_weekend',
            'temperature_avg_c', 'precipitation_mm', 'humidity_percent',
            'inflation_rate', 'exchange_rate_brl_usd', 'gdp_growth_rate',
            '5g_coverage_pct', 'lead_time_days', 'sla_penalty_brl',
            'is_holiday', 'is_weekend', 'is_drought', 'is_flood_risk'
        ]
        
        # Filter to only columns that exist
        feature_cols = [col for col in feature_cols if col in df.columns]
        
        X = df[feature_cols]
        y = df['quantidade']
        
        return X, y, df
    
    def train_models(self, X, y):
        """Train multiple models and return the best one"""
        # Define models to try
        model_configs = {
            'LinearRegression': {
                'model': LinearRegression,
                'params': {}
            },
            'RandomForest': {
                'model': RandomForestRegressor,
                'params': {'n_estimators': 100, 'random_state': 42}
            },
            'GradientBoosting': {
                'model': GradientBoostingRegressor,
                'params': {'n_estimators': 100, 'learning_rate': 0.1, 'random_state': 42}
            }
        }
        
        # Time series cross-validation
        tscv = TimeSeriesSplit(n_splits=5)
        models = {}
        model_scores = {}
        
        for model_name, config in model_configs.items():
            logger.info(f"Training {model_name}")
            fold_scores = []
            
            # Time series cross-validation
            for train_idx, test_idx in tscv.split(X):
                try:
                    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
                    
                    # Scale features
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    
                    # Train model
                    model = config['model'](**config['params'])
                    model.fit(X_train_scaled, y_train)
                    
                    # Predict
                    y_pred = model.predict(X_test_scaled)
                    
                    # Calculate metrics
                    mae = mean_absolute_error(y_test, y_pred)
                    mse = mean_squared_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                    
                    fold_scores.append({
                        'mae': mae,
                        'mse': mse,
                        'rmse': np.sqrt(mse),
                        'r2': r2
                    })
                
                except Exception as e:
                    logger.warning(f"Fold error in {model_name}: {e}")
                    continue
            
            # Average scores across folds
            if fold_scores:
                avg_scores = {
                    'mae': np.mean([s['mae'] for s in fold_scores]),
                    'mse': np.mean([s['mse'] for s in fold_scores]),
                    'rmse': np.mean([s['rmse'] for s in fold_scores]),
                    'r2': np.mean([s['r2'] for s in fold_scores])
                }
                
                # Train final model on full dataset
                try:
                    full_scaler = StandardScaler()
                    X_scaled = full_scaler.fit_transform(X)
                    
                    final_model = config['model'](**config['params'])
                    final_model.fit(X_scaled, y)
                    
                    avg_scores['model'] = final_model
                    avg_scores['scaler'] = full_scaler
                    
                    logger.info(f"  {model_name}: MAE={avg_scores['mae']:.2f}, R²={avg_scores['r2']:.3f}")
                    
                except Exception as e:
                    logger.error(f"Error training final {model_name}: {e}")
                    continue
                
                models[model_name] = avg_scores
                model_scores[model_name] = avg_scores
            else:
                logger.warning(f"No valid folds for {model_name}")
        
        return models, model_scores
    
    def save_models(self, models, model_scores):
        """Save trained models and scores"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save model scores
        scores_file = self.models_dir / f'model_scores_{timestamp}.json'
        
        # Convert numpy types to Python types for JSON serialization
        serializable_scores = {}
        for model_name, scores in model_scores.items():
            serializable_scores[model_name] = {
                'mae': float(scores['mae']),
                'mse': float(scores['mse']),
                'rmse': float(scores['rmse']),
                'r2': float(scores['r2'])
            }
            
            # Save the actual model
            if 'model' in scores and scores['model'] is not None:
                model_file = self.models_dir / f'{model_name}_{timestamp}.pkl'
                joblib.dump(scores['model'], model_file)
                serializable_scores[model_name]['model_file'] = str(model_file)
                
                # Save scaler
                if 'scaler' in scores and scores['scaler'] is not None:
                    scaler_file = self.models_dir / f'{model_name}_scaler_{timestamp}.pkl'
                    joblib.dump(scores['scaler'], scaler_file)
                    serializable_scores[model_name]['scaler_file'] = str(scaler_file)
        
        # Save scores to JSON
        with open(scores_file, 'w') as f:
            json.dump(serializable_scores, f, indent=2)
        
        logger.info(f"Models and scores saved with timestamp {timestamp}")
        return timestamp
    
    def run_pipeline(self):
        """Run the complete ML pipeline"""
        logger.info("Starting Nova Corrente ML Pipeline")
        
        # Load data
        df = self.load_data()
        
        # Prepare features
        X, y, processed_df = self.prepare_features(df)
        logger.info(f"Features prepared: {X.shape}, Target: {y.shape}")
        
        # Train models
        models, model_scores = self.train_models(X, y)
        
        # Save models
        timestamp = self.save_models(models, model_scores)
        
        # Print summary
        logger.info("\\n" + "="*50)
        logger.info("MODEL TRAINING SUMMARY")
        logger.info("="*50)
        
        best_model = None
        best_mae = float('inf')
        
        for model_name, scores in model_scores.items():
            mae = scores['mae']
            r2 = scores['r2']
            logger.info(f"{model_name}: MAE={mae:.2f}, R²={r2:.3f}")
            
            if mae < best_mae:
                best_mae = mae
                best_model = model_name
        
        logger.info(f"\\nBEST MODEL: {best_model} (MAE={best_mae:.2f})")
        
        # Generate insights
        insights = []
        
        if best_mae < 50:
            insights.append("EXCELLENT: High accuracy achieved")
        elif best_mae < 100:
            insights.append("GOOD: Model performance is acceptable")
        elif best_mae < 200:
            insights.append("MEDIUM: Model accuracy needs improvement")
        else:
            insights.append("POOR: Consider additional features or data")
        
        insights.append(f"Recommendation: Retrain monthly with new data")
        insights.append(f"Monitor model drift and performance degradation")
        
        logger.info("\\nINSIGHTS:")
        for insight in insights:
            logger.info(f"  - {insight}")
        
        # Create summary report
        report = {
            'timestamp': timestamp,
            'data_shape': df.shape,
            'feature_shape': X.shape,
            'best_model': best_model,
            'best_mae': best_mae,
            'models_trained': list(model_scores.keys()),
            'insights': insights,
            'model_scores': {
                name: {
                    'mae': float(scores['mae']),
                    'r2': float(scores['r2'])
                }
                for name, scores in model_scores.items()
            }
        }
        
        report_file = self.data_dir / f'ml_training_report_{timestamp}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\\nTraining report saved to: {report_file}")
        logger.info("Pipeline completed successfully! 🚀")
        
        return report

def main():
    """Main execution function"""
    pipeline = SimpleMLPipeline()
    return pipeline.run_pipeline()

if __name__ == "__main__":
    main()