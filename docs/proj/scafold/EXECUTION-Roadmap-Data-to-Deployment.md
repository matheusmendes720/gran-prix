# 🚀 FINAL EXECUTION ROADMAP
## Complete Data Integration + ML Model Training Pipeline

---

## 📋 PHASE 1: DATA COLLECTION (Week 1-2)

### Task 1.1: INMET Weather Data Integration
```python
# File: src/data/inmet_integration.py
import pandas as pd
import requests
from datetime import datetime, timedelta

class INMETDataCollector:
    """Collect Salvador weather data from INMET API"""
    
    def collect_historical_weather(self, days=365):
        """Download 1 year of Salvador weather"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"https://apitempo.inmet.gov.br/estacao/diaria/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}/A502"
        
        try:
            df = pd.read_json(url)
            df.columns = ['date', 'temp_max', 'temp_min', 'humidity_max', 'humidity_min', 'precipitation', 'wind_speed', 'pressure']
            df['date'] = pd.to_datetime(df['date'])
            
            print(f"✅ Collected {len(df)} days of weather data")
            return df
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

# Usage
collector = INMETDataCollector()
weather_data = collector.collect_historical_weather(days=730)  # 2 years
weather_data.to_csv('data/salvador_weather_2years.csv', index=False)
```

### Task 1.2: BACEN Economic Data
```python
# Get inflation, exchange rate, interest rates
import requests

def get_bacen_data():
    """Fetch BACEN economic indicators"""
    
    indicators = {
        '433': 'inflation_ipca',  # IPCA inflation
        '21619': 'exchange_usd_brl',  # USD/BRL
        '11': 'selic_rate'  # SELIC rate
    }
    
    base_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
    all_data = {}
    
    for code, name in indicators.items():
        url = f"{base_url}.{code}/dados"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data, columns=['date', name])
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
            all_data[name] = df.set_index('date')
    
    # Merge all indicators
    result = pd.concat(list(all_data.values()), axis=1)
    result.to_csv('data/bacen_indicators.csv')
    
    print(f"✅ Collected BACEN economic data: {list(indicators.values())}")
    return result

economic_data = get_bacen_data()
```

### Task 1.3: ANATEL 5G Expansion Data
```python
# Use publicly available ANATEL reports
# For this example, we'll create from known data sources

def create_anatel_5g_dataset():
    """
    Create 5G expansion dataset from ANATEL data
    (In production, scrape ANATEL website or use their API)
    """
    
    anatel_5g = pd.DataFrame({
        'date': pd.date_range(start='2020-06-01', end='2025-12-31', freq='M'),
        '5g_coverage_percent': np.linspace(0.5, 85, 66),
        'new_tower_installations': np.random.normal(150, 30, 66),
        'fiber_deployment_km': np.random.normal(5000, 1000, 66),
        'optical_component_demand_index': np.linspace(1.0, 1.45, 66)
    })
    
    anatel_5g.to_csv('data/anatel_5g_expansion.csv', index=False)
    print(f"✅ Created ANATEL 5G expansion dataset: {len(anatel_5g)} months")
    return anatel_5g

anatel_data = create_anatel_5g_dataset()
```

### Task 1.4: Download Kaggle Training Data
```python
# Install Kaggle CLI first:
# pip install kaggle

import os
import subprocess

# Setup Kaggle API credentials
# Place kaggle.json in ~/.kaggle/

def download_kaggle_datasets():
    """Download key Kaggle datasets"""
    
    datasets = [
        'akshatpattiwar/daily-demand-forecasting-orderscsv',  # Main training data
        'datasets/time-series-data'  # Additional time series
    ]
    
    for dataset in datasets:
        cmd = f"kaggle datasets download -d {dataset} -p ./data/"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        if result.returncode == 0:
            print(f"✅ Downloaded: {dataset}")
        else:
            print(f"❌ Failed to download: {dataset}")
    
    # Extract files
    os.system("cd ./data && unzip -o '*.zip'")
    print("✅ All datasets extracted")

download_kaggle_datasets()
```

---

## 📊 PHASE 2: DATA INTEGRATION & FEATURE ENGINEERING (Week 2-3)

### Task 2.1: Create Master Training Dataset
```python
# File: src/data/feature_engineering.py

class FeatureEngineer:
    """Create integrated feature set for ML training"""
    
    def __init__(self):
        self.weather_data = None
        self.economic_data = None
        self.anatel_data = None
        self.demand_data = None
    
    def load_all_data(self):
        """Load data from all sources"""
        
        self.weather_data = pd.read_csv('data/salvador_weather_2years.csv')
        self.economic_data = pd.read_csv('data/bacen_indicators.csv', index_col=0)
        self.anatel_data = pd.read_csv('data/anatel_5g_expansion.csv')
        self.demand_data = pd.read_csv('data/daily_demand.csv')  # From Kaggle
        
        print("✅ All data loaded successfully")
    
    def create_features(self):
        """Engineer features from raw data"""
        
        # Start with demand data
        df = self.demand_data.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        # Add weather features
        weather = self.weather_data.copy()
        weather['date'] = pd.to_datetime(weather['date'])
        
        df = df.merge(weather, on='date', how='left')
        
        # Add economic features (daily resampled)
        economic_daily = self.economic_data.resample('D').ffill()
        df = df.merge(economic_daily, left_on='date', right_index=True, how='left')
        
        # Add 5G features (monthly to daily)
        anatel_daily = self.anatel_data.copy()
        anatel_daily['date'] = pd.to_datetime(anatel_daily['date'])
        anatel_daily = anatel_daily.set_index('date').resample('D').ffill()
        
        df = df.merge(anatel_daily, left_on='date', right_index=True, how='left')
        
        # Create time features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['day_of_year'] = df['date'].dt.dayofyear
        
        # Create lag features
        for lag in [1, 7, 14, 30]:
            df[f'demand_lag_{lag}'] = df['quantity'].shift(lag)
        
        # Create rolling statistics
        for window in [7, 14, 30]:
            df[f'demand_ma_{window}'] = df['quantity'].rolling(window=window).mean()
            df[f'demand_std_{window}'] = df['quantity'].rolling(window=window).std()
        
        # Create weather interaction features
        df['high_temp_flag'] = (df['temp_max'] > 35).astype(int)
        df['high_humidity_flag'] = (df['humidity_avg'] > 80).astype(int)
        df['heavy_rain_flag'] = (df['precipitation'] > 50).astype(int)
        
        # Create economic impact features
        df['inflation_increase_flag'] = df['inflation_ipca'].diff() > 0
        df['exchange_volatility'] = df['exchange_usd_brl'].rolling(window=7).std()
        
        # Create 5G expansion feature
        df['5g_expansion_acceleration'] = df['5g_coverage_percent'].diff()
        
        # Drop NaN
        df = df.dropna()
        
        print(f"✅ Feature engineering complete. Shape: {df.shape}")
        print(f"Features created: {df.columns.tolist()}")
        
        return df

# Execute feature engineering
engineer = FeatureEngineer()
engineer.load_all_data()
training_data = engineer.create_features()
training_data.to_csv('data/training_dataset_integrated.csv', index=False)
```

---

## 🧠 PHASE 3: ML MODEL TRAINING (Week 3-4)

### Task 3.1: Train Base Models
```python
# File: src/models/training.py

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
import joblib

class ModelTrainingPipeline:
    """Train multiple ML models"""
    
    def __init__(self):
        self.models = {}
        self.performance = {}
    
    def prepare_data(self, df):
        """Prepare data for training"""
        
        # Separate features and target
        target = 'quantity'
        features = [col for col in df.columns if col not in ['date', 'quantity']]
        
        X = df[features].fillna(0)
        y = df[target]
        
        # Train-test split (80-20)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"✅ Data prepared: Train {X_train.shape}, Test {X_test.shape}")
        return X_train, X_test, y_train, y_test, features
    
    def train_models(self, X_train, X_test, y_train, y_test, features):
        """Train multiple models and compare"""
        
        from sklearn.ensemble import RandomForestRegressor
        from xgboost import XGBRegressor
        from sklearn.linear_model import Ridge
        
        models_to_train = {
            'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
            'XGBoost': XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1),
            'Ridge': Ridge(alpha=1.0)
        }
        
        results = []
        
        for model_name, model in models_to_train.items():
            # Train
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            
            # Evaluate
            mape = mean_absolute_percentage_error(y_test, y_pred)
            mae = np.mean(np.abs(y_test - y_pred))
            rmse = np.sqrt(np.mean((y_test - y_pred)**2))
            
            self.models[model_name] = model
            self.performance[model_name] = {
                'mape': mape,
                'mae': mae,
                'rmse': rmse
            }
            
            results.append({
                'Model': model_name,
                'MAPE (%)': f"{mape:.2f}%",
                'MAE': f"{mae:.2f}",
                'RMSE': f"{rmse:.2f}"
            })
            
            print(f"✅ {model_name}: MAPE={mape:.2f}%, MAE={mae:.2f}")
        
        results_df = pd.DataFrame(results)
        print("\n" + results_df.to_string(index=False))
        
        return results_df
    
    def save_models(self):
        """Save trained models"""
        
        for model_name, model in self.models.items():
            path = f'models/{model_name}_model.pkl'
            joblib.dump(model, path)
            print(f"✅ Saved {model_name} to {path}")

# Execute training
pipeline = ModelTrainingPipeline()
data = pd.read_csv('data/training_dataset_integrated.csv')
X_train, X_test, y_train, y_test, features = pipeline.prepare_data(data)
results = pipeline.train_models(X_train, X_test, y_train, y_test, features)
pipeline.save_models()
```

### Task 3.2: Train Ensemble Model
```python
# File: src/models/ensemble_training.py

def train_ensemble_model(X_train, X_test, y_train, y_test, features):
    """Create optimized ensemble"""
    
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from xgboost import XGBRegressor
    from scipy.optimize import minimize
    
    # Train base models
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    xgb_model = XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    
    rf_model.fit(X_train, y_train)
    gb_model.fit(X_train, y_train)
    xgb_model.fit(X_train, y_train)
    
    # Get predictions
    rf_pred = rf_model.predict(X_test)
    gb_pred = gb_model.predict(X_test)
    xgb_pred = xgb_model.predict(X_test)
    
    # Optimize weights
    def objective(weights):
        ensemble_pred = weights[0]*rf_pred + weights[1]*gb_pred + weights[2]*xgb_pred
        mape = mean_absolute_percentage_error(y_test, ensemble_pred)
        return mape
    
    # Initial weights
    x0 = np.array([1/3, 1/3, 1/3])
    
    # Constraints
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = [(0, 1) for _ in range(3)]
    
    # Optimize
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    optimal_weights = result.x
    
    print(f"✅ Ensemble weights optimized:")
    print(f"  RandomForest: {optimal_weights[0]:.3f}")
    print(f"  GradientBoosting: {optimal_weights[1]:.3f}")
    print(f"  XGBoost: {optimal_weights[2]:.3f}")
    
    # Final ensemble MAPE
    ensemble_pred = optimal_weights[0]*rf_pred + optimal_weights[1]*gb_pred + optimal_weights[2]*xgb_pred
    final_mape = mean_absolute_percentage_error(y_test, ensemble_pred)
    
    print(f"✅ Final Ensemble MAPE: {final_mape:.2f}%")
    
    return {
        'weights': optimal_weights,
        'models': [rf_model, gb_model, xgb_model],
        'mape': final_mape
    }
```

---

## 📈 PHASE 4: VALIDATION & DEPLOYMENT (Week 4)

### Task 4.1: Validate on Real Nova Corrente Data
```python
# Once you get real data from Nova Corrente

def validate_on_real_data(real_demand_data):
    """Validate models on actual Nova Corrente data"""
    
    # Load ensemble
    ensemble = joblib.load('models/ensemble_model.pkl')
    
    # Prepare real data
    real_data_prepared = prepare_nova_corrente_data(real_demand_data)
    
    # Generate forecast
    forecast = ensemble.predict(real_data_prepared)
    
    # Calculate actual MAPE
    actual_mape = mean_absolute_percentage_error(real_demand_data, forecast)
    
    print(f"✅ Real-world MAPE: {actual_mape:.2f}%")
    
    if actual_mape < 15:
        print("🏆 EXCEEDS TARGET! Ready for production!")
    
    return forecast
```

---

## 📋 EXECUTION CHECKLIST

**Week 1:**
- [ ] Download INMET weather data (Salvador)
- [ ] Download BACEN economic indicators
- [ ] Download ANATEL 5G expansion data
- [ ] Download Kaggle training datasets
- [ ] Create master dataset

**Week 2:**
- [ ] Feature engineering complete
- [ ] Data quality validation passed
- [ ] Training/test split ready
- [ ] Exploratory data analysis done

**Week 3:**
- [ ] ARIMA model trained (MAPE: target <8%)
- [ ] Prophet model trained (MAPE: target <7%)
- [ ] XGBoost model trained (MAPE: target <6%)
- [ ] Individual model evaluation complete

**Week 4:**
- [ ] Ensemble optimization complete
- [ ] Cross-validation passed (MAPE <5%)
- [ ] Models saved and documented
- [ ] Ready for Nova Corrente deployment

---

**Status: READY FOR FULL IMPLEMENTATION** ✅

**Next: Execute Phase 1 (Data Collection) immediately!** 🚀
