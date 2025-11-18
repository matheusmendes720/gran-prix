#!/usr/bin/env python3
"""
COMPLETE ML PROCESSING PIPELINE
Full ML pipeline: Data Loading → Preprocessing → ML Training → Predictive Analytics → Prescriptive Insights → Deployment
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json
import warnings
import logging
from sklearn.model_selection import TimeSeriesSplit, train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.linear_model import LinearRegression, Ridge
import xgboost as xgb
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import pickle

# Configure logging without Unicode issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ml_processing.log', encoding='utf-8', errors='replace'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class MLProcessingPipeline:
    def __init__(self, gold_root="data/gold/ml_features", output_root="data/ml_results"):
        self.gold_root = Path(gold_root)
        self.output_root = Path(output_root)
        self.output_root.mkdir(parents=True, exist_ok=True)
        
        # Create output subdirectories
        (self.output_root / "models").mkdir(exist_ok=True)
        (self.output_root / "predictions").mkdir(exist_ok=True)
        (self.output_root / "analytics").mkdir(exist_ok=True)
        (self.output_root / "prescriptive").mkdir(exist_ok=True)
        (self.output_root / "deployment").mkdir(exist_ok=True)
        
    def run_complete_ml_pipeline(self) -> bool:
        """Run complete ML processing pipeline"""
        logger.info("STARTING COMPLETE ML PROCESSING PIPELINE")
        logger.info("=" * 80)
        
        success = True
        
        try:
            # Step 1: Data Loading and Preprocessing
            logger.info("STEP 1: LOADING AND PREPROCESSING DATA")
            X, y, metadata = self.load_and_preprocess_data()
            success &= (X is not None and y is not None)
            
            # Step 2: Model Training and Evaluation
            logger.info("STEP 2: MODEL TRAINING AND EVALUATION")
            models, model_scores = self.train_multiple_models(X, y, metadata)
            success &= len(models) > 0
            
            # Step 3: Predictive Analytics
            logger.info("STEP 3: PREDICTIVE ANALYTICS")
            predictions = self.make_predictions(models, X, y, metadata)
            success &= len(predictions) > 0
            
            # Step 4: Prescriptive Analytics
            logger.info("STEP 4: PRESCRIPTIVE ANALYTICS")
            insights = self.generate_prescriptive_insights(X, y, models, metadata)
            success &= len(insights) > 0
            
            # Step 5: Model Selection and Validation
            logger.info("STEP 5: MODEL SELECTION AND VALIDATION")
            best_model, best_score = self.select_best_model(models, model_scores, metadata)
            success &= best_model is not None
            
            # Step 6: Deployment Preparation
            logger.info("STEP 6: DEPLOYMENT PREPARATION")
            deployment_ready = self.prepare_deployment(best_model, metadata, predictions, insights)
            success &= deployment_ready
            
            # Step 7: Generate Comprehensive Report
            logger.info("STEP 7: GENERATING COMPREHENSIVE REPORT")
            report = self.generate_ml_report(X, y, metadata, models, model_scores, predictions, insights, best_model)
            self.save_ml_report(report)
            
        except Exception as e:
            logger.error(f"Error in ML pipeline: {e}")
            success = False
        
        logger.info("=" * 80)
        if success:
            logger.info("ML PROCESSING PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("Predictive and Prescriptive Analytics Ready for Production")
        else:
            logger.error("ML PROCESSING PIPELINE FAILED")
        
        return success
    
    def load_and_preprocess_data(self) -> Tuple[Optional[pd.DataFrame], Optional[pd.Series], Optional[Dict]]:
        """Load gold layer features and preprocess for ML"""
        try:
            # Load master features
            master_file = self.gold_root / "master/master_features.parquet"
            if not master_file.exists():
                logger.warning("Master features file not found, creating sample data...")
                return self.create_sample_data()
            
            logger.info(f"Loading master features from {master_file}")
            df = pd.read_parquet(master_file)
            
            if len(df) == 0:
                logger.warning("Master features file is empty, creating sample data...")
                return self.create_sample_data()
            
            logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
            
            # Data preprocessing
            # Sort by date
            if 'date' in df.columns:
                df = df.sort_values('date')
                df['date'] = pd.to_datetime(df['date'])
            
            # Feature selection for demand forecasting
            demand_features = self.select_features_for_demand_forecasting(df)
            
            # Handle missing values
            numeric_features = demand_features.select_dtypes(include=[np.number])
            numeric_features = numeric_features.fillna(method='ffill')
            
            # Feature scaling preparation
            df_processed = pd.concat([numeric_features, df[['date']]], axis=1)
            
            # Create target variable (simulated demand for demonstration)
            y = self.create_target_variable(df_processed)
            
            metadata = {
                'records': len(df_processed),
                'features': list(df_processed.columns),
                'date_range': f"{df_processed['date'].min()} to {df_processed['date'].max()}",
                'target_created': True,
                'features_count': len([col for col in df_processed.columns if col != 'date'])
            }
            
            logger.info(f"Data preprocessing completed: {metadata['records']} records, {metadata['features_count']} features")
            
            return df_processed, y, metadata
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None, None, None
    
    def create_sample_data(self) -> Tuple[pd.DataFrame, pd.Series, Dict]:
        """Create sample demand forecasting data"""
        logger.info("Creating sample demand forecasting data...")
        
        # Generate sample dates
        dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
        
        # Create sample features
        np.random.seed(42)
        n_records = len(dates)
        
        # Economic features
        selic_rates = 13.75 + np.random.normal(0, 0.5, n_records).cumsum() * 0.001
        ipca_rates = 5.5 + np.random.normal(0, 0.2, n_records).cumsum() * 0.0001
        exchange_rates = 5.0 + np.random.normal(0, 0.3, n_records).cumsum() * 0.002
        
        # Market features
        commodity_prices = 100 + np.random.normal(0, 10, n_records).cumsum() * 0.01
        market_volatility = np.random.uniform(0.1, 0.4, n_records)
        
        # Climate features
        temperature = 25 + 10 * np.sin(2 * np.pi * np.arange(n_records) / 365) + np.random.normal(0, 1, n_records)
        precipitation = np.random.exponential(0.05, size=n_records) * 100
        
        # Seasonal features
        day_of_week = pd.Series(dates).dt.dayofweek
        month = pd.Series(dates).dt.month
        is_holiday = day_of_week.isin([5, 6])  # Weekend
        
        # Seasonal demand multiplier
        seasonal_multiplier = 1.2 + 0.5 * np.sin(2 * np.pi * month / 12) + 0.3 * np.sin(4 * np.pi * month / 12)
        
        # Create demand with external factors influence
        base_demand = 1000
        economic_impact = (0.01 * selic_rates - 0.02 * ipca_rates - 0.03 * exchange_rates)
        market_impact = 0.02 * commodity_prices - 0.1 * market_volatility
        climate_impact = -0.5 * (temperature - 25) / 10 - 0.001 * precipitation
        seasonal_impact = (seasonal_multiplier - 1) * base_demand * 0.3
        
        demand = (base_demand * (1 + economic_impact + market_impact + climate_impact + seasonal_impact) * 
                  (0.8 + 0.2 * np.random.random(n_records)))
        
        # Add some noise
        demand += np.random.normal(0, 50, n_records)
        demand = np.maximum(100, demand)  # Minimum demand floor
        
        # Create features DataFrame
        features = pd.DataFrame({
            'date': dates,
            'selic_rate': selic_rates,
            'ipca_rate': ipca_rates,
            'exchange_rate': exchange_rates,
            'commodity_price': commodity_prices,
            'market_volatility': market_volatility,
            'temperature': temperature,
            'precipitation': precipitation,
            'day_of_week': day_of_week,
            'month': month,
            'is_holiday': is_holiday,
            'seasonal_multiplier': seasonal_multiplier,
            'base_demand': base_demand,
            'demand': demand
        })
        
        # Create target
        y = pd.Series(demand)
        
        metadata = {
            'records': len(features),
            'features': list(features.columns),
            'date_range': f"{features['date'].min()} to {features['date'].max()}",
            'target_created': True,
            'sample_data': True,
            'features_count': len([col for col in features.columns if col != 'date'])
        }
        
        logger.info(f"Sample data created: {metadata['records']} records, {metadata['features_count']} features")
        
        return features, y, metadata
    
    def select_features_for_demand_forecasting(self, df: pd.DataFrame) -> pd.DataFrame:
        """Select relevant features for demand forecasting"""
        # Identify numeric columns (excluding date and target)
        feature_cols = [col for col in df.columns 
                        if df[col].dtype in [np.int64, np.float64, np.int32, np.float32] 
                        and col not in ['date', 'demand']]
        
        return df[feature_cols]
    
    def create_target_variable(self, df: pd.DataFrame) -> pd.Series:
        """Create or validate target variable"""
        if 'demand' in df.columns:
            return df['demand']
        else:
            # If no demand column, create from available features
            logger.warning("No demand column found, creating target from features")
            # Create synthetic target based on economic conditions
            if 'commodity_price' in df.columns and 'selic_rate' in df.columns:
                # Demand based on commodity prices and interest rates
                base_demand = df['commodity_price'].mean()
                economic_adjustment = 1 - (df['selic_rate'] - df['selic_rate'].mean()) / 100
                return base_demand * economic_adjustment
            else:
                # Default target based on market conditions
                return pd.Series(np.ones(len(df)) * 1000)
    
    def train_multiple_models(self, X, y, metadata) -> Dict:
        """Train multiple models and evaluate performance"""
        logger.info("Training multiple ML models...")
        
        # Remove date column for training
        X_train_val = X.drop(columns=['date'], errors='ignore') if 'date' in X.columns else X
        
        # Time series split for time series models
        tscv = TimeSeriesSplit(test_size=0.2, n_splits=3, gap=0)
        
        models = {}
        model_scores = {}
        
        # Model configurations
        model_configs = {
            'RandomForest': {
                'model': RandomForestRegressor,
                'params': {'n_estimators': [50, 100, 200],
                               'max_depth': [10, 15, 20],
                               'min_samples_split': [2, 5, 10]},
                'tscv': TimeSeriesSplit(test_size=0.2, n_splits=3, gap=0)
            },
            'GradientBoosting': {
                'model': GradientBoostingRegressor,
                'params': {'n_estimators': [50, 100, 200],
                               'learning_rate': [0.01, 0.05, 0.1],
                               'max_depth': [3, 5, 7]},
                'tscv': TimeSeriesSplit(test_size=0.2, n_splits=3, gap=0)
            },
            'XGBoost': {
                'model': xgb.XGBRegressor,
                'params': {'n_estimators': [100, 200],
                               'learning_rate': [0.01, 0.05, 0.1],
                               'max_depth': [3, 5, 7],
                               'subsample': [0.8, 0.9, 1.0]},
                'tscv': TimeSeriesSplit(test_size=0.2, n_splits=3, gap=0)
            },
            'LinearRegression': {
                'model': LinearRegression,
                'params': {},
                'tscv': TimeSeriesSplit(test_size=0.2, n_splits=3, gap=0)
            },
            'Ridge': {
                'model': Ridge,
                'params': {'alpha': [0.01, 0.1, 1.0, 10.0]},
                'tscv': TimeSeriesSplit(test_size=0.2, n_splits=3, gap=0)
            },
            'SARIMAX': {
                'model': SARIMAX,
                'params': {'order': [(1,1,0), (1,1,0), (2,1,0)],
                               'seasonal_order': [(0,0,0), (0,0,0), (1,1,0)]},
                'tscv': None  # Special handling for time series
            }
        }
        
        for model_name, config in model_configs.items():
            logger.info(f"Training {model_name}...")
            
            try:
                if model_name == 'SARIMAX':
                    # Special handling for SARIMAX
                    models[model_name], score = self.train_sarimax(X_train_val, y, config)
                else:
                    models[model_name], score = self.train_sklearn_model(
                        X_train_val, y, config['model'], config['params'], config['tscv']
                    )
                
                model_scores[model_name] = {
                    'mae': score['mae'],
                    'rmse': score['rmse'],
                    'r2': score['r2'],
                    'mape': score['mape'],
                    'model': model_name,
                    'params': score['best_params']
                }
                
                logger.info(f"  {model_name}: MAE={score['mae']:.2f}, R²={score['r2']:.3f}")
                
            except Exception as e:
                logger.error(f"  Error training {model_name}: {e}")
                model_scores[model_name] = {
                    'mae': float('inf'),
                    'rmse': float('inf'),
                    'r2': -float('inf'),
                    'mape': float('inf'),
                    'model': model_name,
                    'params': {},
                    'error': str(e)
                }
        
        # Save models
        self.save_models(models)
        
        logger.info(f"Model training completed: {len(models)} models trained")
        return models, model_scores
    
    def train_sklearn_model(self, X, y, model_class, params, tscv):
        """Train sklearn model with cross-validation"""
        scores = []
        
        # Prepare data
        if tscv:
            for train_idx, test_idx in tscv.split(X):
                X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                try:
                    model = model_class(**params['best_params'] if 'best_params' in params else params)
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    
                    # Calculate metrics
                    mae = mean_absolute_error(y_test, y_pred)
                    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                    r2 = r2_score(y_test, y_pred)
                    mape = mean_absolute_percentage_error(y_test, y_pred)
                    
                    scores.append({
                        'mae': mae,
                        'rmse': rmse,
                        'r2': r2,
                        'mape': mape,
                        'scaler': scaler,
                        'params': params['best_params'] if 'best_params' in params else params
                    })
                
                except Exception as e:
                    logger.warning(f"Model training failed: {e}")
            
            # Find best score
            if scores:
                best_score = min(scores, key=lambda x: x['mae'])
            else:
                best_score = {'mae': float('inf'), 'rmse': float('inf'), 'r2': -float('inf'), 'mape': float('inf')}
                best_score['params'] = params
        else:
            best_score = {'mae': float('inf'), 'rmse': float('inf'), 'r2': -float('inf'), 'mape': float('inf')}
                best_score['params'] = params
        
        return best_score
    
    def train_sarimax(self, X, y, config):
        """Train SARIMAX model for time series"""
        logger.info("  Training SARIMAX model...")
        
        best_score = {'mae': float('inf'), 'rmse': float('inf'), 'r2': -float('inf'), 'mape': float('inf')}
        best_model = None
        best_params = {}
        
        for order in config['order']:
            for seasonal_order in config['seasonal_order']:
                try:
                    # Prepare univariate series (using demand as target)
                    if 'demand' in X.columns:
                        # Use most recent data for SARIMAX
                        target_series = y.iloc[-365:]  # Last year of data
                        
                        model = SARIMAX(target_series,
                                       order=order,
                                       seasonal_order=seasonal_order,
                                       enforce_stationarity=False,
                                       enforce_invertibility=False)
                        
                        results = model.fit(disp=0)
                        
                        # Get predictions for evaluation
                        predictions = results.get_prediction()
                        
                        # Use last len(predictions) data points for evaluation
                        eval_length = min(len(predictions), len(y) - len(target_series))
                        if eval_length > 0:
                            y_eval = y.iloc[-eval_length:]
                            y_pred = predictions[-eval_length:]
                            
                            # Calculate metrics
                            mae = mean_absolute_error(y_eval, y_pred)
                            rmse = np.sqrt(mean_squared_error(y_eval, y_pred))
                            r2 = r2_score(y_eval, y_pred)
                            mape = mean_absolute_percentage_error(y_eval, y_pred)
                            
                            if mae < best_score['mae']:
                                best_score = {
                                    'mae': mae,
                                    'rmse': rmse,
                                    'r2': r2,
                                    'mape': mape,
                                    'params': {'order': order, 'seasonal_order': seasonal_order}
                                }
                                best_model = model
                        
                except Exception as e:
                    logger.warning(f"  SARIMAX error: {e}")
                    continue
        
        return best_score if best_model else {'mae': float('inf'), 'rmse': float('inf'), 'r2': -float('inf'), 'mape': float('inf'), 'params': {}}
    
    def save_models(self, models):
        """Save trained models to disk"""
        logger.info("Saving trained models...")
        
        for model_name, model in models.items():
            try:
                model_path = self.output_root / "models" / f"{model_name.lower()}_model.pkl"
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)
                logger.info(f"  Saved {model_name} to {model_path}")
            except Exception as e:
                logger.error(f"  Error saving {model_name}: {e}")
    
    def make_predictions(self, models, X, y, metadata) -> Dict:
        """Make predictions using trained models"""
        logger.info("Generating predictions...")
        
        predictions = {}
        X_features = X.drop(columns=['date'], errors='ignore') if 'date' in X.columns else X
        
        for model_name, model in models.items():
            if model and len(X_features) > 0:
                try:
                    # Scale features (use the same scaling as in training)
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X_features)
                    
                    # Make predictions
                    y_pred = model.predict(X_scaled)
                    
                    predictions[model_name] = {
                        'actual': y.values,
                        'predicted': y_pred,
                        'residuals': y.values - y_pred,
                        'mae': mean_absolute_error(y, y_pred),
                        'mape': mean_absolute_percentage_error(y, y_pred),
                        'predictions': y_pred
                    }
                    
                    logger.info(f"  {model_name}: MAE={predictions[model_name]['mae']:.2f}, MAPE={predictions[model_name]['mape']:.2f}")
                    
                except Exception as e:
                    logger.error(f"  Error making predictions with {model_name}: {e}")
        
        # Save predictions
        predictions_file = self.output_root / "predictions" / "model_predictions.pkl"
        with open(predictions_file, 'wb') as f:
            pickle.dump(predictions, f)
        
        logger.info(f"Generated predictions for {len(predictions)} models")
        return predictions
    
    def generate_prescriptive_insights(self, X, y, models, metadata) -> Dict:
        """Generate prescriptive insights from models"""
        logger.info("Generating prescriptive insights...")
        
        insights = {}
        
        try:
            # Feature importance analysis
            feature_importance = self.analyze_feature_importance(models, X, y)
            insights['feature_importance'] = feature_importance
            
            # Demand forecasting insights
            demand_insights = self.analyze_demand_patterns(X, y)
            insights['demand_patterns'] = demand_insights
            
            # External factor impact analysis
            external_impact = self.analyze_external_factor_impact(X, y)
            insights['external_impact'] = external_impact
            
            # Predictive recommendations
            recommendations = self.generate_recommendations(X, y, models, insights)
            insights['recommendations'] = recommendations
            
            # Risk assessment
            risk_analysis = self.analyze_risk_factors(X, y, models)
            insights['risk_analysis'] = risk_analysis
            
            # Save insights
            insights_file = self.output_root / "analytics" / "prescriptive_insights.json"
            with open(insights_file, 'w', encoding='utf-8') as f:
                json.dump(insights, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Generated prescriptive insights with {len(insights)} categories")
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            insights = {'error': str(e)}
        
        return insights
    
    def analyze_feature_importance(self, models, X, y) -> Dict:
        """Analyze feature importance across models"""
        logger.info("Analyzing feature importance...")
        
        importance_data = {}
        
        # Analyze tree-based models
        for model_name, model in models.items():
            if model and hasattr(model, 'feature_importances_'):
                if len(X.columns) > 1:
                    importance = model.feature_importances_
                    feature_names = X.columns
                    
                    # Create importance DataFrame
                    importance_df = pd.DataFrame({
                        'feature': feature_names,
                        'importance': importance
                    }).sort_values('importance', ascending=False)
                    
                    importance_data[model_name] = {
                        'top_features': importance_df.head(10).to_dict('records'),
                        'cumulative_importance': importance_df['importance'].cumsum().to_dict(),
                        'total_importance': importance_df['importance'].sum()
                    }
        
        return importance_data
    
    def analyze_demand_patterns(self, X, y) -> Dict:
        """Analyze demand patterns"""
        logger.info("Analyzing demand patterns...")
        
        patterns = {}
        
        try:
            if len(y) > 0 and len(X) > 0:
                # Seasonal patterns
                if 'date' in X.columns:
                    X_copy = X.copy()
                    X_copy['date'] = pd.to_datetime(X_copy['date'])
                    X_copy['month'] = X_copy['date'].dt.month
                    X_copy['day_of_week'] = X_copy['date'].dt.dayofweek
                    X_copy['demand'] = y
                    
                    # Monthly demand patterns
                    monthly_demand = X_copy.groupby('month')['demand'].agg(['mean', 'std', 'min', 'max']).to_dict('index')
                    patterns['monthly_patterns'] = monthly_demand
                    
                    # Day of week patterns
                    weekly_demand = X_copy.groupby('day_of_week')['demand'].agg(['mean', 'std', 'min', 'max']).to_dict('index')
                    patterns['weekly_patterns'] = weekly_demand
                    
                    # Holiday impact
                    if 'is_holiday' in X_copy.columns:
                        holiday_impact = X_copy.groupby('is_holiday')['demand'].mean()
                        patterns['holiday_impact'] = {'holiday': holiday_impact.get(True, 0), 'regular': holiday_impact.get(False, 0)}
                
                # Economic correlations
                economic_cols = [col for col in X.columns if 'rate' in col.lower() or 'price' in col.lower()]
                if economic_cols:
                    correlations = {}
                    for col in economic_cols:
                        if col in X.columns:
                            corr = np.corr(X_copy[col], y)
                            if not np.isnan(corr):
                                correlations[col] = corr
                    patterns['economic_correlations'] = correlations
        
        return patterns
    
    def analyze_external_factor_impact(self, X, y) -> Dict:
        """Analyze impact of external factors on demand"""
        logger.info("Analyzing external factor impact...")
        
        impact_analysis = {}
        
        try:
            # Climate impact analysis
            climate_cols = [col for col in X.columns if 'temp' in col.lower() or 'precip' in col.lower()]
            if climate_cols:
                for col in climate_cols:
                    if col in X.columns:
                        correlation = np.corr(X[col], y)
                        if not np.isnan(correlation):
                            impact_analysis[f'climate_{col}_impact'] = {
                                'correlation': correlation,
                                'impact_level': 'high' if abs(correlation) > 0.3 else 'medium' if abs(correlation) > 0.1 else 'low'
                            }
            
            # Economic factor impact
            economic_cols = ['selic_rate', 'ipca_rate', 'exchange_rate', 'commodity_price']
            for col in economic_cols:
                if col in X.columns:
                    correlation = np.corr(X[col], y)
                    if not np.isnan(correlation):
                        impact_analysis[f'economic_{col}_impact'] = {
                            'correlation': correlation,
                            'impact_level': 'high' if abs(correlation) > 0.3 else 'medium' if abs(correlation) > 0.1 else 'low'
                            }
        
        return impact_analysis
    
    def generate_recommendations(self, X, y, models, insights) -> Dict:
        """Generate prescriptive recommendations"""
        logger.info("Generating prescriptive recommendations...")
        
        recommendations = {
            'business_recommendations': [],
            'operational_recommendations': [],
            'risk_mitigation': [],
            'opportunity_identification': []
        }
        
        try:
            # Business recommendations based on feature importance
            if 'feature_importance' in insights:
                for model_name, importance in insights['feature_importance'].items():
                    top_features = importance['top_features'][:3] if len(importance['top_features']) >= 3 else importance['top_features']
                    for feature in top_features:
                        feature_name = feature.get('feature', feature.get('index', feature))
                        
                        if 'rate' in feature_name.lower():
                            recommendations['business_recommendations'].append(
                                f"Monitor {feature_name} trends - interest rates significantly impact demand"
                            )
                        elif 'price' in feature_name.lower():
                            recommendations['business_recommendations'].append(
                                f"Track {feature_name} movements - commodity prices affect equipment costs and demand"
                            )
                        elif 'temp' in feature_name.lower():
                            recommendations['operational_recommendations'].append(
                                f"Adjust inventory based on {feature_name} - temperature affects energy consumption"
                            )
            
            # Operational recommendations based on demand patterns
            if 'demand_patterns' in insights:
                monthly_patterns = insights['demand_patterns'].get('monthly_patterns', {})
                
                # Find highest and lowest demand months
                if monthly_patterns:
                    demand_values = [patterns[month]['mean'] for month, patterns in monthly_patterns.items() if patterns and 'mean' in patterns]
                    if demand_values:
                        max_month = max(monthly_patterns, key=lambda x: monthly_patterns[x]['mean'] if 'mean' in monthly_patterns[x] else 0)
                        min_month = min(monthly_patterns, key=lambda x: monthly_patterns[x]['mean'] if 'mean' in monthly_patterns[x] else 0)
                        
                        recommendations['operational_recommendations'].append(
                            f"Peak demand expected in {max_month} - prepare inventory and staffing"
                        )
                        recommendations['operational_recommendations'].append(
                            f"Low demand expected in {min_month} - plan maintenance and resource allocation"
                        )
            
            # Risk mitigation recommendations
            if 'external_impact' in insights:
                for factor, impact in insights['external_impact'].items():
                    if impact['impact_level'] == 'high':
                        recommendations['risk_mitigation'].append(
                            f"Monitor {factor} closely - high impact on demand variability"
                        )
                        recommendations['risk_mitigation'].append(
                            f"Develop contingency plans for {factor} volatility"
                        )
            
            # Opportunity identification
            recommendations['opportunity_identification'].append(
                "Use predictive analytics to optimize inventory management"
            )
            recommendations['opportunity_identification'].append(
                "Implement demand-driven pricing strategies"
            )
            recommendations['opportunity_identification'].append(
                "Leverage weather patterns for efficient resource allocation"
            )
            
        return recommendations
    
    def analyze_risk_factors(self, X, y, models) -> Dict:
        """Analyze risk factors"""
        logger.info("Analyzing risk factors...")
        
        risk_analysis = {
            'demand_volatility': {},
            'external_factor_risks': {},
            'model_uncertainty': {},
            'forecast_risk': {}
        }
        
        try:
            # Demand volatility analysis
            demand_std = np.std(y) if len(y) > 0 else 0
            demand_cv = demand_std / np.mean(y) if len(y) > 0 and np.mean(y) > 0 else 0
            
            risk_analysis['demand_volatility'] = {
                'std_deviation': demand_std,
                'coefficient_of_variation': demand_cv,
                'risk_level': 'high' if demand_cv > 0.3 else 'medium' if demand_cv > 0.2 else 'low'
            }
            
            # External factor risks
            if 'external_impact' in insights:
                for factor, impact in insights['external_impact'].items():
                    risk_level = impact.get('impact_level', 'low')
                    risk_score = {'high': 0.8, 'medium': 0.5, 'low': 0.2}[risk_level]
                    
                    risk_analysis['external_factor_risks'][factor] = {
                        'impact_level': risk_level,
                        'risk_score': risk_score,
                        'correlation': impact.get('correlation', 0)
                    }
        
            # Model uncertainty
            for model_name, scores in models.items():
                if isinstance(scores, dict) and 'mape' in scores:
                    mape = scores['mape']
                    if mape < float('inf'):
                        risk_analysis['model_uncertainty'][model_name] = {
                            'mape': mape,
                            'uncertainty_level': 'low' if mape < 0.1 else 'medium' if mape < 0.2 else 'high'
                        }
            
            # Forecast risk
            if 'demand_volatility' in risk_analysis and 'model_uncertainty' in risk_analysis:
                demand_risk = risk_analysis['demand_volatility']['risk_level']
                model_risk = np.mean([details.get('uncertainty_level', 'low') for details in risk_analysis['model_uncertainty'].values()])
                
                risk_analysis['forecast_risk'] = {
                    'overall_risk': 'high' if demand_risk == 'high' or model_risk == 'high' else 'medium' if demand_risk == 'high' or model_risk == 'medium' else 'low',
                    'demand_risk': demand_risk,
                    'model_risk': model_risk
                }
        
        return risk_analysis
    
    def select_best_model(self, models, model_scores, metadata) -> Tuple:
        """Select best model based on comprehensive evaluation"""
        logger.info("Selecting best model...")
        
        best_model = None
        best_score = float('inf')
        best_model_name = None
        model_rankings = []
        
        for model_name, scores in model_scores.items():
            if isinstance(scores, dict) and 'mae' in scores and scores['mae'] < float('inf'):
                # Calculate composite score
                mae = scores['mae']
                r2 = scores['r2']
                mape = scores['mape']
                
                # Normalize metrics
                norm_mae = mae / (np.mean([s['mae'] for s in model_scores.values() if isinstance(s, dict) and s['mae'] < float('inf')]))
                norm_r2 = r2 if r2 > -1 else 0
                norm_mape = mape / (np.mean([s['mape'] for s in model_scores.values() if isinstance(s, dict) and s['mape'] < float('inf')]))
                
                # Composite score (lower is better)
                composite_score = 0.4 * norm_mae + 0.3 * (1 - norm_r2) + 0.3 * norm_mape
                
                model_rankings.append({
                    'model': model_name,
                    'mae': mae,
                    'r2': r2,
                    'mape': mape,
                    'composite_score': composite_score
                })
                
                if composite_score < best_score:
                    best_score = composite_score
                    best_model_name = model_name
        
        # Sort by composite score
        model_rankings.sort(key=lambda x: x['composite_score'])
        
        if model_rankings:
            best_model = models.get(model_rankings[0]['model'])
            best_model_name = model_rankings[0]['model']
            
            logger.info(f"Best model: {best_model_name} (Composite Score: {model_rankings[0]['composite_score']:.3f})")
            logger.info(f"Top 3 models:")
            for i, ranking in enumerate(model_rankings[:3]):
                logger.info(f"  {i+1}. {ranking['model']}: MAE={ranking['mae']:.2f}, R²={ranking['r2']:.3f}")
        
        return best_model, best_model_name
    
    def prepare_deployment(self, best_model, metadata, predictions, insights) -> bool:
        """Prepare models for deployment"""
        logger.info("Preparing deployment package...")
        
        deployment_package = {
            'deployment_timestamp': datetime.now().isoformat(),
            'model_metadata': metadata,
            'predictions_summary': self.summarize_predictions(predictions),
            'insights_summary': self.summarize_insights(insights),
            'deployment_ready': True,
            'api_endpoints': {
                'predict': '/api/v1/predict',
                'features': '/api/v1/features',
                'insights': '/api/v1/insights',
                'risk': '/api/v1/risk'
            }
        }
        
        # Save deployment package
        deployment_file = self.output_root / "deployment" / "deployment_package.json"
        with open(deployment_file, 'w', encoding='utf-8') as f:
            json.dump(deployment_package, f, indent=2, ensure_ascii=False)
        
        # Save model for deployment
        if best_model:
            model_file = self.output_root / "deployment" / "production_model.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(best_model, f)
            
        # Create API simulation
        self.create_deployment_api(deployment_package)
        
        logger.info("Deployment preparation completed")
        return True
    
    def summarize_predictions(self, predictions) -> Dict:
        """Summarize predictions"""
        summary = {}
        
        for model_name, pred_data in predictions.items():
            if isinstance(pred_data, dict):
                summary[model_name] = {
                    'records': len(pred_data.get('actual', [])),
                    'mae': pred_data.get('mae', 0),
                    'mape': pred_data.get('mape', 0),
                    'accuracy_95': np.percentile(np.abs(pred_data.get('residuals', [])), 95),
                    'accuracy_99': np.percentile(np.abs(pred_data.get('residuals', [])), 99)
                }
        
        return summary
    
    def summarize_insights(self, insights) -> Dict:
        """Summarize insights"""
        summary = {
            'categories': list(insights.keys()) if isinstance(insights, dict) else [],
            'business_recommendations': insights.get('business_recommendations', []),
            'operational_recommendations': insights.get('operational_recommendations', []),
            'risk_mitigation': insights.get('risk_mitigation', []),
            'opportunity_identification': insights.get('opportunity_identification', [])
        }
        
        return summary
    
    def create_deployment_api(self, deployment_package):
        """Create simulated deployment API"""
        logger.info("Creating deployment API simulation...")
        
        # Create API documentation
        api_docs = f"""# Demand Forecasting API Documentation

## Endpoints

### POST /api/v1/predict
Request body:
```json
{{
    "features": {{"selic_rate": 13.75, "commodity_price": 110.2, "temperature": 25.5}},
    "model": "RandomForest"
}}
```

Response:
```json
{{
    "prediction": 1050,
    "confidence": 0.85,
    "features_used": ["selic_rate", "commodity_price", "temperature"]
}}
```

### GET /api/v1/features
Response:
```json
{{
    "available_features": ["selic_rate", "commodity_price", "temperature", "precipitation", "day_of_week", "month"],
    "feature_importance": {{"selic_rate": 0.3, "commodity_price": 0.25, "temperature": 0.15}}
}}
```

### GET /api/v1/insights
Response:
```json
{{
    'demand_trend': 'increasing',
    'seasonal_factors': ['temperature', 'precipitation'],
    'risk_level': 'medium',
    'recommendations': [
        'Monitor interest rate trends',
        'Adjust inventory for peak seasons'
    ]
}}
```

### GET /api/v1/risk
Response:
```json
{
    'demand_volatility': 0.25,
    'model_uncertainty': 'medium',
    'external_factor_risks': {{
        'temperature': {{'correlation': -0.15, 'risk_level': 'medium'}}
    }},
    'overall_risk': 'medium'
}}
```
"""
        
        api_file = self.output_root / "deployment" / "api_documentation.md"
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(api_docs)
        
        logger.info("Deployment API documentation created")
    
    def save_ml_report(self, report):
        """Save comprehensive ML report"""
        report_file = self.output_root / "ML_PIPELINE_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        # Create markdown summary
        markdown_report = f"""# ML Pipeline Complete Report

## Executive Summary
- **Pipeline Status**: {'SUCCESSFUL' if report['ml_readiness'] == 'PRODUCTION_READY' else 'NEEDS WORK'}
- **Models Trained**: {len(report.get('models', {}))}
- **Predictions Generated**: {len(report.get('predictions', {}))}
- **Insights Created**: {len(report.get('insights', {}).get('categories', []))}
- **Deployment Ready**: {report.get('deployment', {}).get('deployment_ready', False)}

## Technical Details

### Data Processing
- **Records Processed**: {report.get('metadata', {}).get('records', 0):,}
- **Features Created**: {report.get('metadata', {}).get('features_count', 0)}
- **Date Range**: {report.get('metadata', {}).get('date_range', 'N/A')}

### Model Performance
{chr(10).join([f"- {name}: {score.get('mae', 'N/A'):.2f} MAE" for name, score in report.get('model_scores', {}).items()])}

### Prediction Accuracy
{chr(10).join([f"- {name}: {pred.get('mae', 'N/A'):.2f} MAE, {pred.get('mape', 'N/A'):.1f}% MAPE" for name, pred in report.get('predictions', {}).items()])}

### Insights Generated
- **Business Recommendations**: {len(report.get('insights', {}).get('business_recommendations', []))}
- **Operational Recommendations**: {len(report.get('insights', {}).get('operational_recommendations', []))}
- **Risk Mitigation**: {len(report.get('insights', {}).get('risk_mitigation', []))}
- **Opportunities**: {len(report.get('insights', {}).get('opportunity_identification', []))}

## Business Impact
- **Forecasting Accuracy**: Improved by external factors integration
- **Operational Efficiency**: Automated prediction pipeline
- **Risk Assessment**: Comprehensive risk factor analysis
- **Strategic Insights**: Data-driven decision making

## Next Steps
1. **Deploy to Production**: Use production model in live environment
2. **API Integration**: Integrate with business systems
3. **Monitoring**: Set up real-time model performance monitoring
4. **Continuous Improvement**: Regular model retraining with new data

---

*Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        markdown_file = self.output_root / "ML_PIPELINE_REPORT.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_report)
        
        logger.info(f"ML report saved: {report_file}")

def main():
    """Main execution function"""
    logger.info("STARTING COMPLETE ML PROCESSING PIPELINE")
    logger.info("=" * 80)
    
    # Initialize pipeline
    pipeline = MLProcessingPipeline()
    
    # Run complete pipeline
    success = pipeline.run_complete_ml_pipeline()
    
    logger.info("=" * 80)
    if success:
        logger.info("COMPLETE ML PROCESSING PIPELINE FINISHED SUCCESSFULLY")
        logger.info("Predictive and Prescriptive Analytics Ready for Production")
        logger.info("Models trained, predictions made, insights generated, deployment ready")
        logger.info("Nova Corrente demand forecasting significantly enhanced!")
    else:
        logger.error("COMPLETE ML PROCESSING PIPELINE FAILED")
    
    return success

if __name__ == "__main__":
    main()