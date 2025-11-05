# etl/load_ml_outputs.py (runs on-demand or via cron)
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os
import json
import numpy as np

def load_ml_outputs():
    print("Starting ML Output Loading Process...")
    
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente')
    engine = create_engine(DATABASE_URL)

    # 1. Load forecasts from the database (in this case, we'll generate some sample data)
    print("1. Loading forecasts...")
    
    # Generate sample forecast data
    sample_forecasts = []
    for item_id in range(1, 51):  # First 50 items
        for site_id in range(1, 3):  # First 2 sites
            for horizon in [7, 14, 30, 60, 90]:
                for day_offset in range(5):  # 5 days of forecasts
                    forecast_date = datetime.now().date() + timedelta(days=day_offset*7 + horizon)
                    
                    sample_forecasts.append({
                        'full_date': forecast_date,
                        'item_id': item_id,
                        'site_id': site_id,
                        'horizon_days': horizon,
                        'yhat': max(0, 100 + (item_id % 20) + (site_id % 5) + (horizon / 10) + (day_offset * 2) + np.random.normal(0, 10)),
                        'yhat_lower': max(0, 80 + (item_id % 20) + (site_id % 5) + (horizon / 10) + (day_offset * 2) + np.random.normal(0, 5)),
                        'yhat_upper': max(0, 120 + (item_id % 20) + (site_id % 5) + (horizon / 10) + (day_offset * 2) + np.random.normal(0, 15)),
                        'model_tag': 'prophet_v2.1',
                        'confidence_level': 0.95,
                        'computed_at': datetime.now()
                    })

    forecast_df = pd.DataFrame(sample_forecasts)
    
    # Truncate old forecasts (optional: keep history)
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE analytics.forecasts;")
        conn.commit()

    # Bulk insert via pandas to_sql
    forecast_df.to_sql('forecasts', engine, schema='analytics', if_exists='append', index=False, method='multi', chunksize=10000)

    print(f"Loaded {len(forecast_df)} forecasts into PostgreSQL")

    # 2. Load features (JSONB transformation)
    print("2. Loading features...")
    
    # Generate sample features data
    sample_features = []
    for item_id in range(1, 51):  # First 50 items
        for date_offset in range(30):  # Last 30 days
            feature_date = datetime.now().date() - timedelta(days=date_offset)
            
            # Generate feature JSON
            features_json = {
                'lag_7d': 90 + (item_id % 20) + np.random.normal(0, 5),
                'rolling_mean_30d': 100 + (item_id % 20) + np.random.normal(0, 5),
                'holiday_effect': 1.0 + np.random.uniform(-0.2, 0.3),
                'seasonality_factor': 1.0 + np.random.uniform(-0.1, 0.2),
                'trend_factor': 1.0 + np.random.uniform(-0.05, 0.1)
            }
            
            sample_features.append({
                'full_date': feature_date,
                'item_id': item_id,
                'site_id': 1,  # Default to site 1
                'features': json.dumps(features_json),
                'schema_version': 'v1.0',
                'computed_at': datetime.now()
            })

    features_df = pd.DataFrame(sample_features)
    
    # Truncate old features (optional: keep history)
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE analytics.features_store;")
        conn.commit()
    
    # Bulk insert features
    features_df.to_sql('features_store', engine, schema='analytics', if_exists='append', index=False)

    print(f"Loaded {len(features_df)} feature rows")

    # 3. Calculate recommendations based on forecasts and current inventory
    print("3. Generating recommendations...")
    
    # Fetch current inventory levels
    inventory_query = """
        SELECT 
            item_id, 
            site_id, 
            current_stock,
            safety_stock,
            reorder_point
        FROM core.fact_inventory_daily 
        WHERE full_date = (SELECT MAX(full_date) FROM core.fact_inventory_daily)
    """
    
    current_inventory = pd.read_sql(inventory_query, engine)
    
    recommendations = []
    for _, inv_row in current_inventory.iterrows():
        item_id = inv_row['item_id']
        site_id = inv_row['site_id']
        current_stock = inv_row['current_stock'] or 0
        safety_stock = inv_row['safety_stock'] or 0
        reorder_point = inv_row['reorder_point'] or 0
        
        # Check if we should generate a recommendation
        if current_stock <= safety_stock:
            # Need to reorder
            avg_demand = 100 + (item_id % 20)  # Simplified average demand
            reorder_qty = max(100, avg_demand * 14)  # Order enough for 14 days
            
            recommendations.append({
                'item_id': item_id,
                'site_id': site_id,
                'type': 'REORDER',
                'priority': 'HIGH' if current_stock == 0 else 'MEDIUM',
                'message': f'Reorder {reorder_qty} units. Current stock: {current_stock}',
                'action_date': datetime.now().date() + timedelta(days=2),  # Suggest reorder in 2 days
                'quantity_recommended': reorder_qty,
                'created_at': datetime.now()
            })
        elif current_stock <= reorder_point:
            # Below reorder point, monitor
            recommendations.append({
                'item_id': item_id,
                'site_id': site_id,
                'type': 'MONITOR',
                'priority': 'LOW',
                'message': f'Monitor stock. Current stock: {current_stock}, Reorder point: {reorder_point}',
                'action_date': None,
                'quantity_recommended': 0,
                'created_at': datetime.now()
            })
    
    recommendations_df = pd.DataFrame(recommendations)
    
    # Clear old recommendations
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE analytics.recommendations;")
        conn.commit()
    
    # Insert new recommendations
    recommendations_df.to_sql('recommendations', engine, schema='analytics', if_exists='append', index=False)
    
    print(f"Generated {len(recommendations_df)} recommendations")
    
    # 4. Generate alerts based on current state
    print("4. Generating alerts...")
    
    alerts = []
    for _, inv_row in current_inventory.iterrows():
        item_id = inv_row['item_id']
        site_id = inv_row['site_id']
        current_stock = inv_row['current_stock'] or 0
        safety_stock = inv_row['safety_stock'] or 0
        
        if current_stock == 0:
            alerts.append({
                'item_id': item_id,
                'site_id': site_id,
                'level': 'CRITICAL',
                'category': 'STOCKOUT',
                'message': f'Item {item_id} is out of stock at site {site_id}',
                'created_at': datetime.now()
            })
        elif current_stock < safety_stock:
            alerts.append({
                'item_id': item_id,
                'site_id': site_id,
                'level': 'WARNING',
                'category': 'LOW_STOCK',
                'message': f'Item {item_id} stock level ({current_stock}) below safety stock ({safety_stock}) at site {site_id}',
                'created_at': datetime.now()
            })
    
    alerts_df = pd.DataFrame(alerts)
    
    # Clear old alerts
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE analytics.alerts;")
        conn.commit()
    
    # Insert new alerts
    alerts_df.to_sql('alerts', engine, schema='analytics', if_exists='append', index=False)
    
    print(f"Generated {len(alerts_df)} alerts")
    
    # 5. Refresh materialized views
    print("5. Refreshing materialized views...")
    with engine.connect() as conn:
        conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.mv_kpis_latest;")
        conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.mv_forecasts_latest;")
        conn.commit()

    print("ML Output Loading Process completed successfully!")
    
    return {
        'forecasts_loaded': len(forecast_df),
        'features_loaded': len(features_df),
        'recommendations_generated': len(recommendations_df),
        'alerts_generated': len(alerts_df)
    }

if __name__ == "__main__":
    import numpy as np
    from datetime import timedelta
    results = load_ml_outputs()
    print(f"Loading Results: {results}")