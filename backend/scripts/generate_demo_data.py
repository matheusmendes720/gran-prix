import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os
import hashlib
from werkzeug.security import generate_password_hash

# Create database engine
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente')
engine = create_engine(DATABASE_URL)

def generate_demo_data():
    print("Generating demo data...")
    
    # 1. Generate calendar dimension (3 years: 2023, 2024, 2025)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')

    calendar = pd.DataFrame({
        'full_date': dates,
        'year': dates.year,
        'month': dates.month,
        'quarter': dates.quarter,
        'weekday': dates.weekday,
        'day_of_month': dates.day,
        'week_of_year': dates.isocalendar().week,
        'is_weekend': dates.weekday >= 5,
        'is_holiday': False  # Can enhance with holidays library
    })

    # Insert calendar data
    calendar.to_sql('dim_calendar', engine, schema='core', if_exists='replace', index=False)
    print(f"Generated {len(calendar)} calendar dates")

    # 2. Generate items (500 SKUs)
    np.random.seed(42)  # For reproducible results
    items_data = {
        'sku': [f"ITEM-{i:05d}" for i in range(1, 501)],
        'name': [f"Product {i}" for i in range(1, 501)],
        'description': [f"Description for product {i}" for i in range(1, 501)],
        'family': np.random.choice(['ELECTRICAL', 'TELECOM', 'HARDWARE'], 500),
        'category': np.random.choice(['Connectors', 'Cables', 'Components', 'Tools'], 500),
        'subcategory': np.random.choice(['Small', 'Medium', 'Large'], 500),
        'unit_measure': 'UN',
        'abc_class': np.random.choice(['A', 'B', 'C'], 500, p=[0.2, 0.3, 0.5]),
        'criticality': np.random.randint(1, 11, 500),
        'active': True,
        'min_order_qty': np.random.randint(1, 10, 500),
        'max_order_qty': np.random.randint(10, 100, 500)
    }

    items = pd.DataFrame(items_data)
    items.to_sql('dim_item', engine, schema='core', if_exists='replace', index=False)
    print(f"Generated {len(items)} items")

    # 3. Generate sites (5 locations)
    sites_data = {
        'code': ['SP01', 'RJ01', 'MG01', 'BA01', 'PE01'],
        'name': ['São Paulo Distribution', 'Rio de Janeiro Warehouse', 'Belo Horizonte Center', 'Salvador Hub', 'Recife Depot'],
        'region_id': [1, 3, 2, 8, 9],  # SP, RJ, MG, BA, PE
        'latitude': [-23.5505, -22.9068, -19.9173, -12.9714, -8.0466],
        'longitude': [-46.6333, -43.1729, -43.9347, -38.5014, -34.8770],
        'site_type': ['WAREHOUSE', 'DISTRIBUTION_CENTER', 'WAREHOUSE', 'STORE', 'DISTRIBUTION_CENTER'],
        'active': [True, True, True, True, True]
    }

    sites = pd.DataFrame(sites_data)
    sites.to_sql('dim_site', engine, schema='core', if_exists='replace', index=False)
    print(f"Generated {len(sites)} sites")

    # 4. Generate suppliers (50 suppliers)
    suppliers_data = {
        'code': [f"SUP-{i:04d}" for i in range(1, 51)],
        'name': [f"Supplier {i}" for i in range(1, 51)],
        'supplier_type': np.random.choice(['DOMESTIC', 'IMPORT', 'HYBRID'], 50),
        'reliability_score': np.random.uniform(70, 100, 50),
        'avg_lead_time_days': np.random.randint(5, 60, 50),
        'on_time_delivery_rate': np.random.uniform(0.7, 1.0, 50),
        'active': [True] * 50
    }

    suppliers = pd.DataFrame(suppliers_data)
    suppliers.to_sql('dim_supplier', engine, schema='core', if_exists='replace', index=False)
    print(f"Generated {len(suppliers)} suppliers")

    # 5. Generate demand facts (last 90 days, 500 items × 5 sites = 225K rows)
    print("Generating demand data...")
    item_ids = items['item_id'].tolist()
    site_ids = sites['site_id'].tolist()
    last_90_days = pd.date_range(datetime.now() - timedelta(days=90), datetime.now(), freq='D')

    demand_rows = []
    for date in last_90_days:
        for item_id in item_ids:
            for site_id in site_ids:
                # Simulate demand with seasonality + noise
                base_demand = 50 + 20 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365)
                demand = max(0, base_demand + np.random.normal(0, 10))
                
                demand_rows.append({
                    'full_date': date.date(),
                    'item_id': item_id,
                    'site_id': site_id,
                    'quantity': round(demand, 2),
                    'unit_cost': round(np.random.uniform(5, 50), 2),
                    'lead_time_days': np.random.randint(1, 15)
                })

    demand_df = pd.DataFrame(demand_rows)
    demand_df.to_sql('fact_demand_daily', engine, schema='core', if_exists='replace', index=False)
    print(f"Generated {len(demand_df)} demand records")

    # 6. Generate inventory data
    print("Generating inventory data...")
    inventory_rows = []
    for date in last_90_days:
        for item_id in item_ids:
            for site_id in site_ids:
                # Generate random inventory levels
                current_stock = np.random.uniform(0, 1000)
                safety_stock = np.random.uniform(50, 200)
                reorder_point = safety_stock * 1.5
                
                inventory_rows.append({
                    'full_date': date.date(),
                    'item_id': item_id,
                    'site_id': site_id,
                    'current_stock': round(current_stock, 2),
                    'safety_stock': round(safety_stock, 2),
                    'reorder_point': round(reorder_point, 2),
                    'days_to_rupture': np.random.randint(0, 30)
                })

    inventory_df = pd.DataFrame(inventory_rows)
    inventory_df.to_sql('fact_inventory_daily', engine, schema='core', if_exists='replace', index=False)
    print(f"Generated {len(inventory_df)} inventory records")

    # 7. Generate forecasts (for next 30 days)
    print("Generating forecast data...")
    forecast_rows = []
    future_dates = pd.date_range(datetime.now(), datetime.now() + timedelta(days=30), freq='D')[1:]  # Skip today
    
    for date in future_dates:
        for item_id in item_ids[:50]:  # Only use first 50 items to reduce data volume
            for site_id in site_ids:
                # Generate forecast values
                base_forecast = 50 + np.random.normal(0, 10)
                forecast_rows.append({
                    'full_date': date.date(),
                    'item_id': item_id,
                    'site_id': site_id,
                    'horizon_days': (date - datetime.now()).days,
                    'yhat': max(0, round(base_forecast, 2)),
                    'yhat_lower': max(0, round(base_forecast - 5, 2)),
                    'yhat_upper': max(0, round(base_forecast + 5, 2)),
                    'model_tag': 'prophet_v2.1',
                    'confidence_level': 0.95,
                    'computed_at': datetime.now()
                })

    forecast_df = pd.DataFrame(forecast_rows)
    forecast_df.to_sql('forecasts', engine, schema='analytics', if_exists='replace', index=False)
    print(f"Generated {len(forecast_df)} forecast records")

    # 8. Generate KPIs (for last 30 days)
    print("Generating KPI data...")
    kpi_rows = []
    kpi_dates = pd.date_range(datetime.now() - timedelta(days=30), datetime.now(), freq='D')
    
    for date in kpi_dates:
        # Generate random KPI values
        kpi_rows.append({
            'full_date': date.date(),
            'total_demand': round(np.random.uniform(10000, 50000), 2),
            'stockout_rate': round(np.random.uniform(0.01, 0.1), 4),  # 1% to 10% stockout rate
            'abc_a_share': round(np.random.uniform(0.70, 0.90), 4),  # 70% to 90% A-class share
            'delayed_orders_pct': round(np.random.uniform(0.02, 0.08), 4),  # 2% to 8% delayed
            'forecast_mape': round(np.random.uniform(0.05, 0.20), 4),  # 5% to 20% MAPE
            'avg_inventory_value': round(np.random.uniform(200000, 500000), 2),
            'computed_at': datetime.now()
        })

    kpi_df = pd.DataFrame(kpi_rows)
    kpi_df.to_sql('kpis_daily', engine, schema='analytics', if_exists='replace', index=False)
    print(f"Generated {len(kpi_df)} KPI records")

    # 9. Generate recommendations
    print("Generating recommendations...")
    rec_types = ['REORDER', 'PROMO', 'REALLOCATE', 'HOLD', 'EXPEDITE']
    rec_priorities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    rec_rows = []
    for i in range(100):  # Generate 100 recommendations
        rec_rows.append({
            'item_id': np.random.choice(item_ids),
            'site_id': np.random.choice(site_ids),
            'type': np.random.choice(rec_types),
            'priority': np.random.choice(rec_priorities),
            'message': f"Recommendation for item {i+1}",
            'action_date': datetime.now() + timedelta(days=np.random.randint(0, 30)),
            'quantity_recommended': round(np.random.uniform(10, 200), 2),
            'created_at': datetime.now()
        })

    rec_df = pd.DataFrame(rec_rows)
    rec_df.to_sql('recommendations', engine, schema='analytics', if_exists='replace', index=False)
    print(f"Generated {len(rec_df)} recommendations")

    # 10. Generate alerts
    print("Generating alerts...")
    alert_levels = ['NORMAL', 'WARNING', 'CRITICAL']
    alert_categories = ['STOCKOUT_IMMINENT', 'LOW_INVENTORY', 'HIGH_DEMAND', 'SUPPLIER_ISSUE']
    
    alert_rows = []
    for i in range(50):  # Generate 50 alerts
        alert_rows.append({
            'item_id': np.random.choice(item_ids),
            'site_id': np.random.choice(site_ids),
            'level': np.random.choice(alert_levels),
            'category': np.random.choice(alert_categories),
            'message': f"Alert for item {i+1}",
            'created_at': datetime.now()
        })

    alert_df = pd.DataFrame(alert_rows)
    alert_df.to_sql('alerts', engine, schema='analytics', if_exists='replace', index=False)
    print(f"Generated {len(alert_df)} alerts")

    # 11. Generate users
    print("Generating users...")
    user_rows = [
        {
            'username': 'admin',
            'email': 'admin@novacorrente.com',
            'password_hash': generate_password_hash('admin123'),
            'role': 'ADMIN',
            'active': True,
            'created_at': datetime.now()
        },
        {
            'username': 'analyst',
            'email': 'analyst@novacorrente.com',
            'password_hash': generate_password_hash('analyst123'),
            'role': 'ANALYST',
            'active': True,
            'created_at': datetime.now()
        },
        {
            'username': 'viewer',
            'email': 'viewer@novacorrente.com',
            'password_hash': generate_password_hash('viewer123'),
            'role': 'VIEWER',
            'active': True,
            'created_at': datetime.now()
        }
    ]

    user_df = pd.DataFrame(user_rows)
    user_df.to_sql('users', engine, schema='support', if_exists='replace', index=False)
    print(f"Generated {len(user_df)} users")

    # 12. Refresh materialized views (if they exist)
    try:
        with engine.connect() as conn:
            conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.mv_kpis_latest;")
            conn.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.mv_forecasts_latest;")
            conn.commit()
        print("Materialized views refreshed")
    except Exception as e:
        print(f"Could not refresh materialized views: {e}")

    print("Demo data generation complete!")

if __name__ == "__main__":
    generate_demo_data()