"""
Generate synthetic demo data for Nova Corrente PostgreSQL database
Creates dimensions and facts for demonstration purposes
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import os
import json

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente')
engine = create_engine(DATABASE_URL)

print("🚀 Starting demo data generation...")

# ===== 1. Generate Calendar Dimension (3 years) =====
print("\n📅 Generating calendar dimension...")

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
    'is_holiday': False,  # Can enhance with holidays library
    'fiscal_year': dates.year,
    'fiscal_quarter': dates.quarter
})

calendar.to_sql('dim_calendar', engine, schema='core', if_exists='append', index=False)
print(f"✅ Generated {len(calendar)} calendar dates")

# ===== 2. Generate Regions =====
print("\n🌎 Generating regions...")

regions = pd.DataFrame({
    'name': ['Southeast', 'South', 'Northeast', 'North', 'Midwest'],
    'state_code': ['SP', 'RS', 'BA', 'AM', 'DF'],
    'economic_zone': ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5']
})

regions.to_sql('dim_region', engine, schema='core', if_exists='append', index=False)
print(f"✅ Generated {len(regions)} regions")

# ===== 3. Generate Sites =====
print("\n🏪 Generating sites...")

sites = pd.DataFrame({
    'code': [f'SITE-{i:03d}' for i in range(1, 11)],
    'name': [f'Site {i}' for i in range(1, 11)],
    'region_id': np.random.choice([1, 2, 3, 4, 5], 10),
    'latitude': np.random.uniform(-30, -5, 10),
    'longitude': np.random.uniform(-60, -35, 10),
    'site_type': np.random.choice(['WAREHOUSE', 'STORE', 'DISTRIBUTION_CENTER'], 10),
    'active': True
})

sites.to_sql('dim_site', engine, schema='core', if_exists='append', index=False)
print(f"✅ Generated {len(sites)} sites")

# ===== 4. Generate Suppliers =====
print("\n🚚 Generating suppliers...")

suppliers = pd.DataFrame({
    'code': [f'SUP-{i:04d}' for i in range(1, 51)],
    'name': [f'Supplier {i}' for i in range(1, 51)],
    'supplier_type': np.random.choice(['DOMESTIC', 'IMPORT', 'HYBRID'], 50),
    'reliability_score': np.random.uniform(70, 100, 50),
    'avg_lead_time_days': np.random.randint(5, 60, 50),
    'on_time_delivery_rate': np.random.uniform(80, 99, 50),
    'active': True
})

suppliers.to_sql('dim_supplier', engine, schema='core', if_exists='append', index=False)
print(f"✅ Generated {len(suppliers)} suppliers")

# ===== 5. Generate Items (500 SKUs) =====
print("\n📦 Generating items...")

families = ['ELECTRICAL', 'TELECOM', 'HARDWARE', 'CABLE', 'CONNECTOR']
categories = {
    'ELECTRICAL': ['SWITCHES', 'OUTLETS', 'BREAKERS'],
    'TELECOM': ['ROUTERS', 'MODEMS', 'ANTENNAS'],
    'HARDWARE': ['SCREWS', 'BOLTS', 'TOOLS'],
    'CABLE': ['FIBER', 'COPPER', 'COAXIAL'],
    'CONNECTOR': ['RJ45', 'USB', 'HDMI']
}

items_data = []
for i in range(1, 501):
    family = np.random.choice(families)
    category = np.random.choice(categories[family])
    
    items_data.append({
        'sku': f'{family[:3]}-{i:05d}',
        'name': f'{family} Product {i}',
        'description': f'Description for {family} product {i}',
        'family': family,
        'category': category,
        'subcategory': f'{category}_SUB',
        'unit_measure': 'UN',
        'abc_class': np.random.choice(['A', 'B', 'C'], p=[0.2, 0.3, 0.5]),
        'criticality': np.random.randint(1, 11),
        'active': True,
        'min_order_qty': np.random.randint(10, 100),
        'max_order_qty': np.random.randint(1000, 5000),
        'extra_attributes': json.dumps({'voltage': '220V', 'warranty': '12m'})
    })

items = pd.DataFrame(items_data)
items.to_sql('dim_item', engine, schema='core', if_exists='append', index=False)
print(f"✅ Generated {len(items)} items")

# ===== 6. Generate Demand Facts (Last 90 days) =====
print("\n📊 Generating demand facts...")

last_90_days = pd.date_range(datetime.now() - timedelta(days=90), datetime.now(), freq='D')
site_ids = list(range(1, 11))
item_ids = list(range(1, 501))

demand_rows = []
batch_size = 10000

for date in last_90_days:
    for item_id in np.random.choice(item_ids, 100, replace=False):  # Random 100 items per day
        for site_id in np.random.choice(site_ids, 3, replace=False):  # Random 3 sites per item
            # Simulate demand with seasonality + noise
            day_of_year = date.timetuple().tm_yday
            base_demand = 50 + 20 * np.sin(2 * np.pi * day_of_year / 365)
            demand = max(0, base_demand + np.random.normal(0, 10))
            
            demand_rows.append({
                'full_date': date.date(),
                'item_id': item_id,
                'site_id': site_id,
                'supplier_id': np.random.choice(list(range(1, 51))),
                'quantity': round(demand, 2),
                'unit_cost': round(np.random.uniform(5, 50), 2),
                'lead_time_days': np.random.randint(5, 45)
            })
            
            # Batch insert every 10,000 rows
            if len(demand_rows) >= batch_size:
                demand_df = pd.DataFrame(demand_rows)
                demand_df.to_sql('fact_demand_daily', engine, schema='core', if_exists='append', index=False)
                print(f"  ✅ Inserted {len(demand_rows)} demand records...")
                demand_rows = []

# Insert remaining rows
if demand_rows:
    demand_df = pd.DataFrame(demand_rows)
    demand_df.to_sql('fact_demand_daily', engine, schema='core', if_exists='append', index=False)

print(f"✅ Generated demand facts")

# ===== 7. Generate Inventory Facts =====
print("\n📦 Generating inventory facts...")

inventory_rows = []

for date in last_90_days:
    for item_id in np.random.choice(item_ids, 100, replace=False):
        for site_id in np.random.choice(site_ids, 3, replace=False):
            current_stock = max(0, np.random.normal(500, 150))
            safety_stock = current_stock * 0.3
            reorder_point = current_stock * 0.4
            days_to_rupture = int(current_stock / max(1, np.random.normal(15, 5)))
            
            inventory_rows.append({
                'full_date': date.date(),
                'item_id': item_id,
                'site_id': site_id,
                'current_stock': round(current_stock, 2),
                'safety_stock': round(safety_stock, 2),
                'reorder_point': round(reorder_point, 2),
                'days_to_rupture': max(0, days_to_rupture)
            })
            
            if len(inventory_rows) >= batch_size:
                inventory_df = pd.DataFrame(inventory_rows)
                inventory_df.to_sql('fact_inventory_daily', engine, schema='core', if_exists='append', index=False)
                print(f"  ✅ Inserted {len(inventory_rows)} inventory records...")
                inventory_rows = []

if inventory_rows:
    inventory_df = pd.DataFrame(inventory_rows)
    inventory_df.to_sql('fact_inventory_daily', engine, schema='core', if_exists='append', index=False)

print(f"✅ Generated inventory facts")

# ===== 8. Generate Sample KPIs =====
print("\n📈 Generating sample KPIs...")

kpis_rows = []
for date in pd.date_range(datetime.now() - timedelta(days=30), datetime.now(), freq='D'):
    kpis_rows.append({
        'full_date': date.date(),
        'total_demand': round(np.random.uniform(10000, 50000), 2),
        'stockout_rate': round(np.random.uniform(0.02, 0.08), 4),
        'abc_a_share': round(np.random.uniform(0.75, 0.85), 4),
        'delayed_orders_pct': round(np.random.uniform(0.03, 0.10), 4),
        'forecast_mape': round(np.random.uniform(0.10, 0.20), 4),
        'avg_inventory_value': round(np.random.uniform(500000, 1500000), 2),
        'computed_at': datetime.now()
    })

kpis_df = pd.DataFrame(kpis_rows)
kpis_df.to_sql('kpis_daily', engine, schema='analytics', if_exists='append', index=False)
print(f"✅ Generated {len(kpis_df)} KPI records")

# ===== 9. Generate Sample Recommendations =====
print("\n💡 Generating sample recommendations...")

rec_types = ['REORDER', 'PROMO', 'REALLOCATE', 'HOLD', 'EXPEDITE']
priorities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

recommendations = []
for i in range(50):
    rec_type = np.random.choice(rec_types)
    priority = np.random.choice(priorities)
    item_id = np.random.choice(item_ids)
    site_id = np.random.choice(site_ids)
    
    messages = {
        'REORDER': f'Stock below safety level. Reorder recommended.',
        'EXPEDITE': f'Critical item - expedite delivery.',
        'REALLOCATE': f'Excess stock - consider reallocation.',
        'PROMO': f'Slow-moving item - promotion recommended.',
        'HOLD': f'Hold ordering - sufficient stock.'
    }
    
    recommendations.append({
        'item_id': item_id,
        'site_id': site_id,
        'type': rec_type,
        'priority': priority,
        'message': messages[rec_type],
        'quantity_recommended': round(np.random.uniform(100, 1000), 2),
        'action_date': (datetime.now() + timedelta(days=np.random.randint(1, 30))).date()
    })

rec_df = pd.DataFrame(recommendations)
rec_df.to_sql('recommendations', engine, schema='analytics', if_exists='append', index=False)
print(f"✅ Generated {len(rec_df)} recommendations")

# ===== 10. Generate Sample Alerts =====
print("\n🚨 Generating sample alerts...")

alert_levels = ['NORMAL', 'WARNING', 'CRITICAL']
categories = ['STOCKOUT_IMMINENT', 'LOW_STOCK', 'DELAYED_ORDER', 'QUALITY_ISSUE']

alerts = []
for i in range(30):
    level = np.random.choice(alert_levels, p=[0.3, 0.4, 0.3])
    category = np.random.choice(categories)
    item_id = np.random.choice(item_ids)
    site_id = np.random.choice(site_ids)
    
    messages = {
        'STOCKOUT_IMMINENT': f'Item will stock out in {np.random.randint(1, 5)} days',
        'LOW_STOCK': f'Stock below reorder point',
        'DELAYED_ORDER': f'Order delayed by {np.random.randint(3, 15)} days',
        'QUALITY_ISSUE': f'Quality issue reported'
    }
    
    alerts.append({
        'item_id': item_id,
        'site_id': site_id,
        'level': level,
        'category': category,
        'message': messages[category],
        'created_at': datetime.now() - timedelta(hours=np.random.randint(1, 72))
    })

alerts_df = pd.DataFrame(alerts)
alerts_df.to_sql('alerts', engine, schema='analytics', if_exists='append', index=False)
print(f"✅ Generated {len(alerts_df)} alerts")

# ===== 11. Create Admin User =====
print("\n👤 Creating admin user...")

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

admin_user = pd.DataFrame([{
    'username': 'admin',
    'email': 'admin@novacorrente.com',
    'password_hash': pwd_context.hash('admin123'),  # Change this in production!
    'role': 'ADMIN',
    'active': True
}])

admin_user.to_sql('users', engine, schema='support', if_exists='append', index=False)
print(f"✅ Created admin user (username: admin, password: admin123)")

print("\n" + "="*60)
print("✅ Demo data generation complete!")
print("="*60)
print("\nDatabase Summary:")
print(f"  📅 Calendar dates: {len(calendar)}")
print(f"  🌎 Regions: {len(regions)}")
print(f"  🏪 Sites: {len(sites)}")
print(f"  🚚 Suppliers: {len(suppliers)}")
print(f"  📦 Items: {len(items)}")
print(f"  📊 Demand records: ~{len(last_90_days) * 100 * 3:,}")
print(f"  📦 Inventory records: ~{len(last_90_days) * 100 * 3:,}")
print(f"  📈 KPIs: {len(kpis_df)}")
print(f"  💡 Recommendations: {len(rec_df)}")
print(f"  🚨 Alerts: {len(alerts_df)}")
print("\n🎉 You can now start the Flask API and explore the data!")
