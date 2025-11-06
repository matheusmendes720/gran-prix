"""Initial PostgreSQL schema with core, analytics, support schemas

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-11-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create schemas
    op.execute('CREATE SCHEMA IF NOT EXISTS core')
    op.execute('CREATE SCHEMA IF NOT EXISTS analytics')
    op.execute('CREATE SCHEMA IF NOT EXISTS support')
    op.execute('CREATE SCHEMA IF NOT EXISTS staging')
    
    # ===== CORE SCHEMA: DIMENSIONS =====
    
    # Calendar Dimension
    op.execute("""
        CREATE TABLE core.dim_calendar (
          date_id SERIAL PRIMARY KEY,
          full_date DATE UNIQUE NOT NULL,
          year SMALLINT NOT NULL,
          month SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
          quarter SMALLINT NOT NULL CHECK (quarter BETWEEN 1 AND 4),
          weekday SMALLINT NOT NULL CHECK (weekday BETWEEN 0 AND 6),
          day_of_month SMALLINT NOT NULL,
          week_of_year SMALLINT NOT NULL,
          is_weekend BOOLEAN NOT NULL DEFAULT false,
          is_holiday BOOLEAN NOT NULL DEFAULT false,
          holiday_name TEXT,
          fiscal_year SMALLINT,
          fiscal_quarter SMALLINT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_dim_calendar_date ON core.dim_calendar(full_date)')
    op.execute('CREATE INDEX ix_dim_calendar_year_month ON core.dim_calendar(year, month)')
    
    # Region Dimension
    op.execute("""
        CREATE TABLE core.dim_region (
          region_id SERIAL PRIMARY KEY,
          name TEXT UNIQUE NOT NULL,
          state_code CHAR(2),
          economic_zone TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Item/Material Dimension
    op.execute("""
        CREATE TABLE core.dim_item (
          item_id SERIAL PRIMARY KEY,
          sku TEXT UNIQUE NOT NULL,
          name TEXT NOT NULL,
          description TEXT,
          family TEXT,
          category TEXT,
          subcategory TEXT,
          unit_measure TEXT NOT NULL DEFAULT 'UN',
          abc_class CHAR(1) CHECK (abc_class IN ('A', 'B', 'C')),
          criticality SMALLINT CHECK (criticality BETWEEN 0 AND 10),
          active BOOLEAN NOT NULL DEFAULT true,
          min_order_qty NUMERIC(18,4),
          max_order_qty NUMERIC(18,4),
          extra_attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_dim_item_sku ON core.dim_item(sku)')
    op.execute('CREATE INDEX ix_dim_item_family ON core.dim_item(family)')
    op.execute('CREATE INDEX ix_dim_item_abc ON core.dim_item(abc_class)')
    op.execute('CREATE INDEX gin_dim_item_attrs ON core.dim_item USING GIN (extra_attributes)')
    
    # Site Dimension
    op.execute("""
        CREATE TABLE core.dim_site (
          site_id SERIAL PRIMARY KEY,
          code TEXT UNIQUE NOT NULL,
          name TEXT NOT NULL,
          region_id INT REFERENCES core.dim_region(region_id),
          latitude NUMERIC(9,6),
          longitude NUMERIC(9,6),
          site_type TEXT CHECK (site_type IN ('WAREHOUSE', 'STORE', 'DISTRIBUTION_CENTER')),
          active BOOLEAN NOT NULL DEFAULT true,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_dim_site_region ON core.dim_site(region_id)')
    
    # Supplier Dimension
    op.execute("""
        CREATE TABLE core.dim_supplier (
          supplier_id SERIAL PRIMARY KEY,
          code TEXT UNIQUE NOT NULL,
          name TEXT NOT NULL,
          supplier_type TEXT CHECK (supplier_type IN ('DOMESTIC', 'IMPORT', 'HYBRID')),
          reliability_score NUMERIC(5,2) CHECK (reliability_score BETWEEN 0 AND 100),
          avg_lead_time_days INTEGER,
          on_time_delivery_rate NUMERIC(5,2),
          active BOOLEAN NOT NULL DEFAULT true,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_dim_supplier_type ON core.dim_supplier(supplier_type)')
    
    # ===== CORE SCHEMA: FACTS (PARTITIONED) =====
    
    # Demand Fact (partitioned by month)
    op.execute("""
        CREATE TABLE core.fact_demand_daily (
          demand_id BIGSERIAL,
          full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
          item_id INT NOT NULL REFERENCES core.dim_item(item_id),
          site_id INT NOT NULL REFERENCES core.dim_site(site_id),
          supplier_id INT REFERENCES core.dim_supplier(supplier_id),
          quantity NUMERIC(18,4) NOT NULL CHECK (quantity >= 0),
          unit_cost NUMERIC(18,4),
          total_cost NUMERIC(18,4) GENERATED ALWAYS AS (quantity * unit_cost) STORED,
          lead_time_days INTEGER,
          extra_attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (demand_id, full_date)
        ) PARTITION BY RANGE (full_date)
    """)
    
    # Create 2025 monthly partitions
    for month in range(1, 13):
        month_str = f"{month:02d}"
        next_month = month + 1 if month < 12 else 1
        next_month_str = f"{next_month:02d}"
        year_next = 2025 if month < 12 else 2026
        
        op.execute(f"""
            CREATE TABLE core.fact_demand_daily_2025_{month_str} PARTITION OF core.fact_demand_daily
            FOR VALUES FROM ('2025-{month_str}-01') TO ('{year_next}-{next_month_str}-01')
        """)
    
    op.execute('CREATE INDEX ix_fact_demand_date ON core.fact_demand_daily(full_date)')
    op.execute('CREATE INDEX ix_fact_demand_item ON core.fact_demand_daily(item_id)')
    op.execute('CREATE INDEX ix_fact_demand_site ON core.fact_demand_daily(site_id)')
    op.execute('CREATE INDEX ix_fact_demand_composite ON core.fact_demand_daily(item_id, site_id, full_date)')
    
    # Inventory Fact (partitioned)
    op.execute("""
        CREATE TABLE core.fact_inventory_daily (
          inventory_id BIGSERIAL,
          full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
          item_id INT NOT NULL REFERENCES core.dim_item(item_id),
          site_id INT NOT NULL REFERENCES core.dim_site(site_id),
          current_stock NUMERIC(18,4) NOT NULL,
          safety_stock NUMERIC(18,4),
          reorder_point NUMERIC(18,4),
          days_to_rupture INTEGER,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (inventory_id, full_date)
        ) PARTITION BY RANGE (full_date)
    """)
    
    # Create 2025 inventory partitions
    for month in range(1, 13):
        month_str = f"{month:02d}"
        next_month = month + 1 if month < 12 else 1
        next_month_str = f"{next_month:02d}"
        year_next = 2025 if month < 12 else 2026
        
        op.execute(f"""
            CREATE TABLE core.fact_inventory_daily_2025_{month_str} PARTITION OF core.fact_inventory_daily
            FOR VALUES FROM ('2025-{month_str}-01') TO ('{year_next}-{next_month_str}-01')
        """)
    
    op.execute('CREATE INDEX ix_fact_inventory_date ON core.fact_inventory_daily(full_date)')
    op.execute('CREATE INDEX ix_fact_inventory_item_site ON core.fact_inventory_daily(item_id, site_id)')
    
    # ===== ANALYTICS SCHEMA =====
    
    # Forecasts Table
    op.execute("""
        CREATE TABLE analytics.forecasts (
          forecast_id BIGSERIAL PRIMARY KEY,
          full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
          item_id INT NOT NULL REFERENCES core.dim_item(item_id),
          site_id INT NOT NULL REFERENCES core.dim_site(site_id),
          horizon_days SMALLINT NOT NULL CHECK (horizon_days > 0),
          yhat NUMERIC(18,4) NOT NULL,
          yhat_lower NUMERIC(18,4),
          yhat_upper NUMERIC(18,4),
          model_tag TEXT NOT NULL,
          confidence_level NUMERIC(5,2),
          computed_at TIMESTAMP NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_forecasts_item_site_date ON analytics.forecasts(item_id, site_id, full_date)')
    op.execute('CREATE INDEX ix_forecasts_horizon ON analytics.forecasts(horizon_days)')
    op.execute('CREATE INDEX ix_forecasts_computed ON analytics.forecasts(computed_at)')
    
    # Features Store (JSONB)
    op.execute("""
        CREATE TABLE analytics.features_store (
          feature_id BIGSERIAL PRIMARY KEY,
          full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
          item_id INT NOT NULL REFERENCES core.dim_item(item_id),
          site_id INT REFERENCES core.dim_site(site_id),
          features JSONB NOT NULL,
          schema_version TEXT NOT NULL DEFAULT 'v1.0',
          computed_at TIMESTAMP NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_features_item_date ON analytics.features_store(item_id, full_date)')
    op.execute('CREATE INDEX gin_features_jsonb ON analytics.features_store USING GIN (features)')
    
    # KPIs Daily
    op.execute("""
        CREATE TABLE analytics.kpis_daily (
          kpi_id BIGSERIAL PRIMARY KEY,
          full_date DATE NOT NULL REFERENCES core.dim_calendar(full_date),
          total_demand NUMERIC(18,4),
          stockout_rate NUMERIC(10,4),
          abc_a_share NUMERIC(10,4),
          delayed_orders_pct NUMERIC(10,4),
          forecast_mape NUMERIC(10,4),
          avg_inventory_value NUMERIC(18,2),
          computed_at TIMESTAMP NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          UNIQUE (full_date, computed_at)
        )
    """)
    
    op.execute('CREATE INDEX ix_kpis_date ON analytics.kpis_daily(full_date DESC)')
    
    # Recommendations
    op.execute("""
        CREATE TABLE analytics.recommendations (
          recommendation_id BIGSERIAL PRIMARY KEY,
          item_id INT REFERENCES core.dim_item(item_id),
          site_id INT REFERENCES core.dim_site(site_id),
          type TEXT NOT NULL CHECK (type IN ('REORDER', 'PROMO', 'REALLOCATE', 'HOLD', 'EXPEDITE')),
          priority TEXT NOT NULL CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
          message TEXT NOT NULL,
          action_date DATE,
          quantity_recommended NUMERIC(18,4),
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          acknowledged_at TIMESTAMP,
          acknowledged_by TEXT
        )
    """)
    
    op.execute('CREATE INDEX ix_recommendations_priority ON analytics.recommendations(priority, created_at DESC)')
    op.execute('CREATE INDEX ix_recommendations_item ON analytics.recommendations(item_id)')
    
    # Alerts
    op.execute("""
        CREATE TABLE analytics.alerts (
          alert_id BIGSERIAL PRIMARY KEY,
          item_id INT REFERENCES core.dim_item(item_id),
          site_id INT REFERENCES core.dim_site(site_id),
          level TEXT NOT NULL CHECK (level IN ('NORMAL', 'WARNING', 'CRITICAL')),
          category TEXT NOT NULL,
          message TEXT NOT NULL,
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          read_at TIMESTAMP,
          resolved_at TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_alerts_level_date ON analytics.alerts(level, created_at DESC)')
    op.execute("CREATE INDEX ix_alerts_unread ON analytics.alerts(read_at) WHERE read_at IS NULL")
    
    # ===== SUPPORT SCHEMA =====
    
    # Audit Logs
    op.execute("""
        CREATE TABLE support.audit_logs (
          audit_id BIGSERIAL PRIMARY KEY,
          actor TEXT NOT NULL,
          action TEXT NOT NULL,
          entity_type TEXT,
          entity_id BIGINT,
          details JSONB NOT NULL DEFAULT '{}'::jsonb,
          ip_address INET,
          user_agent TEXT,
          timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_audit_actor ON support.audit_logs(actor)')
    op.execute('CREATE INDEX ix_audit_timestamp ON support.audit_logs(timestamp DESC)')
    op.execute('CREATE INDEX gin_audit_details ON support.audit_logs USING GIN (details)')
    
    # Users (simple RBAC)
    op.execute("""
        CREATE TABLE support.users (
          user_id SERIAL PRIMARY KEY,
          username TEXT UNIQUE NOT NULL,
          email TEXT UNIQUE NOT NULL,
          password_hash TEXT NOT NULL,
          role TEXT NOT NULL CHECK (role IN ('ADMIN', 'ANALYST', 'VIEWER')),
          active BOOLEAN NOT NULL DEFAULT true,
          last_login TIMESTAMP,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute('CREATE INDEX ix_users_username ON support.users(username)')
    
    print("✅ PostgreSQL schema created successfully!")


def downgrade():
    op.execute('DROP SCHEMA IF EXISTS core CASCADE')
    op.execute('DROP SCHEMA IF EXISTS analytics CASCADE')
    op.execute('DROP SCHEMA IF EXISTS support CASCADE')
    op.execute('DROP SCHEMA IF EXISTS staging CASCADE')
    
    print("✅ PostgreSQL schema dropped successfully!")
