# ML Integration Guide
 
 ## Overview
 Guide for integrating the external factors pipeline with Nova Corrente demand forecasting models.
 
 ## Data Access
 
 ### Feature Store Location
 ```python
 from pathlib import Path
 
 gold_root = Path("data/gold/ml_features")
 master_features = gold_root / "master/master_features.parquet"
 ```
 
 ### Loading Features
 ```python
 import pandas as pd
 
 # Load all features
 df = pd.read_parquet(master_features)
 
 # Load specific categories
 economic_features = pd.read_parquet(gold_root / "economic/ptax_features.parquet")
 climatic_features = pd.read_parquet(gold_root / "climatic/inmet_features.parquet")
 ```
 
 ## Model Integration
 
 ### Feature Selection
 ```python
 # Select features for demand forecasting
 feature_columns = [
     'ptax_rate_ma7',      # Exchange rate (7-day avg)
     'selic_rate_ma7',     # Interest rate (7-day avg)
     'ipca_index_mom_ma12', # Inflation (12-month avg)
     'temperature_c_ma7',   # Temperature (7-day avg)
     'precipitation_rolling30', # Precipitation (30-day sum)
     'commodity_price_ma7', # Commodity prices (7-day avg)
     'market_index_ma7'    # Market indices (7-day avg)
 ]
 
 X = df[feature_columns].fillna(method='ffill')
 y = df['nova_corrente_demand']  # Target variable
 ```
 
 ### Time Series Split
 ```python
 # Chronological split for time series data
 split_date = '2024-01-01'
 train_mask = df['date'] < split_date
 test_mask = df['date'] >= split_date
 
 X_train = X[train_mask]
 X_test = X[test_mask]
 y_train = y[train_mask]
 y_test = y[test_mask]
 ```
 
 ### Feature Engineering for Models
 ```python
 # Create lagged features
 def create_lagged_features(df, columns, lags=[1, 7, 30]):
     lagged_df = df.copy()
     df_sorted = df.sort_values('date')
     
     for col in columns:
         for lag in lags:
             lagged_df[f"{{col}}_lag_{{lag}}d"] = df_sorted[col].shift(lag)
     
     return lagged_df
 
 # Create rolling features
 def create_rolling_features(df, columns, windows=[7, 30]):
     rolling_df = df.copy()
     df_sorted = df.sort_values('date')
     
     for col in columns:
         for window in windows:
             rolling_df[f"{{col}}_ma_{{window}}d"] = df_sorted[col].rolling(window).mean()
             rolling_df[f"{{col}}_std_{{window}}d"] = df_sorted[col].rolling(window).std()
     
     return rolling_df
 ```
 
 ## Model Training
 
 ### Data Preparation
 ```python
 from sklearn.preprocessing import StandardScaler
 from sklearn.model_selection import TimeSeriesSplit
 
 # Scale features
 scaler = StandardScaler()
 X_scaled = scaler.fit_transform(X)
 
 # Time series cross-validation
 tscv = TimeSeriesSplit(n_splits=5, test_size=30)
 ```
 
 ### Model Examples
 ```python
 # Random Forest for demand forecasting
 from sklearn.ensemble import RandomForestRegressor
 
 model_rf = RandomForestRegressor(
     n_estimators=100,
     max_depth=10,
     random_state=42
 )
 
 # XGBoost for time series
 import xgboost as xgb
 
 model_xgb = xgb.XGBRegressor(
     n_estimators=100,
     max_depth=6,
     learning_rate=0.1,
     random_state=42
 )
 
 # LSTM for sequence data
 from tensorflow.keras.models import Sequential
 from tensorflow.keras.layers import LSTM, Dense
 
 model_lstm = Sequential([
     LSTM(50, activation='relu', input_shape=(30, X.shape[1])),
     Dense(1)
 ])
 ```
 
 ## Model Evaluation
 
 ### Metrics
 ```python
 from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
 
 def evaluate_model(model, X_test, y_test):
     y_pred = model.predict(X_test)
     
     mae = mean_absolute_error(y_test, y_pred)
     mse = mean_squared_error(y_test, y_pred)
     r2 = r2_score(y_test, y_pred)
     
     return {'mae': mae, 'mse': mse, 'r2': r2}
 ```
 
 ### Feature Importance
 ```python
 # Get feature importance from tree models
 import matplotlib.pyplot as plt
 
 if hasattr(model, 'feature_importances_'):
     importance = model.feature_importances_
     features = X.columns
     
     plt.figure(figsize=(10, 6))
     plt.barh(features, importance)
     plt.title('Feature Importance')
     plt.xlabel('Importance')
     plt.ylabel('Features')
     plt.tight_layout()
     plt.show()
 ```
 
 ## Production Integration
 
 ### Model Deployment
 ```python
 import joblib
 
 # Save model and scaler
 joblib.dump(model, 'demand_model.joblib')
 joblib.dump(scaler, 'feature_scaler.joblib')
 
 # Load for inference
 model = joblib.load('demand_model.joblib')
 scaler = joblib.load('feature_scaler.joblib')
 ```
 
 ### Real-Time Inference
 ```python
 def predict_demand(model, scaler, latest_features):
     '''
     Predict demand using latest external features
     
     Args:
         model: Trained ML model
         scaler: Fitted feature scaler
         latest_features: Dictionary of latest feature values
     
     Returns:
         float: Predicted demand
     '''
     # Convert to DataFrame and scale
     df = pd.DataFrame([latest_features])
     X_scaled = scaler.transform(df)
     
     # Make prediction
     prediction = model.predict(X_scaled)[0]
     
     return prediction
 ```
 
 ## Monitoring
 
 ### Data Drift Detection
 ```python
 def detect_data_drift(historical_features, current_features, threshold=0.1):
     '''
     Detect data drift between historical and current features
     
     Args:
         historical_features: Historical feature distribution
         current_features: Current feature distribution
         threshold: Drift detection threshold
     
     Returns:
         bool: True if drift detected
     '''
     from scipy import stats
     
     drift_scores = []
     
     for col in historical_features.columns:
         if col in current_features.columns:
             hist_col = historical_features[col]
             curr_col = current_features[col]
             
             # Kolmogorov-Smirnov test
             ks_stat, p_value = stats.ks_2samp(hist_col.dropna(), curr_col.dropna())
             drift_scores.append(ks_stat)
     
     avg_drift = np.mean(drift_scores)
     
     return avg_drift > threshold
 ```
 
 ---
 
 *ML Integration Guide Last Updated: 2025-11-11 13:46:25*
 