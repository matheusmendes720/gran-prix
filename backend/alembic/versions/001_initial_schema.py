"""Initial schema core analytics support

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-11-05 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
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

    # Calendar Dimension
    op.create_table('dim_calendar',
        sa.Column('date_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('full_date', sa.Date(), nullable=False),
        sa.Column('year', sa.SmallInteger(), nullable=False),
        sa.Column('month', sa.SmallInteger(), nullable=False),
        sa.Column('quarter', sa.SmallInteger(), nullable=False),
        sa.Column('weekday', sa.SmallInteger(), nullable=False),
        sa.Column('day_of_month', sa.SmallInteger(), nullable=False),
        sa.Column('week_of_year', sa.SmallInteger(), nullable=False),
        sa.Column('is_weekend', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_holiday', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('holiday_name', sa.Text(), nullable=True),
        sa.Column('fiscal_year', sa.SmallInteger(), nullable=True),
        sa.Column('fiscal_quarter', sa.SmallInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('date_id'),
        sa.UniqueConstraint('full_date'),
        schema='core'
    )

    # Create indexes for dim_calendar
    op.create_index('ix_dim_calendar_date', 'dim_calendar', ['full_date'], unique=False, schema='core')
    op.create_index('ix_dim_calendar_year_month', 'dim_calendar', ['year', 'month'], unique=False, schema='core')

    # Item/Material Dimension
    op.create_table('dim_item',
        sa.Column('item_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sku', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('family', sa.Text(), nullable=True),
        sa.Column('category', sa.Text(), nullable=True),
        sa.Column('subcategory', sa.Text(), nullable=True),
        sa.Column('unit_measure', sa.Text(), nullable=False, server_default='UN'),
        sa.Column('abc_class', sa.CHAR(length=1), nullable=True),
        sa.Column('criticality', sa.SmallInteger(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('min_order_qty', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('max_order_qty', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('extra_attributes', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="'{}'::jsonb"),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('item_id'),
        sa.UniqueConstraint('sku'),
        schema='core'
    )

    # Create indexes for dim_item
    op.create_index('ix_dim_item_sku', 'dim_item', ['sku'], unique=False, schema='core')
    op.create_index('ix_dim_item_family', 'dim_item', ['family'], unique=False, schema='core')
    op.create_index('ix_dim_item_abc', 'dim_item', ['abc_class'], unique=False, schema='core')
    op.create_index('gin_dim_item_attrs', 'dim_item', ['extra_attributes'], unique=False, postgresql_using='gin', schema='core')

    # Region Dimension
    op.create_table('dim_region',
        sa.Column('region_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('state_code', sa.CHAR(length=2), nullable=True),
        sa.Column('economic_zone', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('region_id'),
        sa.UniqueConstraint('name'),
        schema='core'
    )

    # Site/Location Dimension
    op.create_table('dim_site',
        sa.Column('site_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('region_id', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column('longitude', sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column('site_type', sa.Text(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['region_id'], ['core.dim_region.region_id'], ),
        sa.PrimaryKeyConstraint('site_id'),
        sa.UniqueConstraint('code'),
        schema='core'
    )

    # Create indexes for dim_site
    op.create_index('ix_dim_site_region', 'dim_site', ['region_id'], unique=False, schema='core')

    # Supplier Dimension
    op.create_table('dim_supplier',
        sa.Column('supplier_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('supplier_type', sa.Text(), nullable=True),
        sa.Column('reliability_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('avg_lead_time_days', sa.Integer(), nullable=True),
        sa.Column('on_time_delivery_rate', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('supplier_id'),
        sa.UniqueConstraint('code'),
        schema='core'
    )

    # Create indexes for dim_supplier
    op.create_index('ix_dim_supplier_type', 'dim_supplier', ['supplier_type'], unique=False, schema='core')

    # Demand Fact (partitioned by month) - Initial table without partitioning for compatibility
    op.create_table('fact_demand_daily',
        sa.Column('demand_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('full_date', sa.Date(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('site_id', sa.Integer(), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column('unit_cost', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('total_cost', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('lead_time_days', sa.Integer(), nullable=True),
        sa.Column('extra_attributes', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="'{}'::jsonb"),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['full_date'], ['core.dim_calendar.full_date'], ),
        sa.ForeignKeyConstraint(['item_id'], ['core.dim_item.item_id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['core.dim_site.site_id'], ),
        sa.ForeignKeyConstraint(['supplier_id'], ['core.dim_supplier.supplier_id'], ),
        sa.PrimaryKeyConstraint('demand_id', 'full_date'),
        schema='core'
    )

    # Create indexes for fact_demand_daily
    op.create_index('ix_fact_demand_date', 'fact_demand_daily', ['full_date'], unique=False, schema='core')
    op.create_index('ix_fact_demand_item', 'fact_demand_daily', ['item_id'], unique=False, schema='core')
    op.create_index('ix_fact_demand_site', 'fact_demand_daily', ['site_id'], unique=False, schema='core')
    op.create_index('ix_fact_demand_composite', 'fact_demand_daily', ['item_id', 'site_id', 'full_date'], unique=False, schema='core')

    # Inventory Fact (partitioned by month) - Initial table without partitioning for compatibility
    op.create_table('fact_inventory_daily',
        sa.Column('inventory_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('full_date', sa.Date(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('site_id', sa.Integer(), nullable=False),
        sa.Column('current_stock', sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column('safety_stock', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('reorder_point', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('days_to_rupture', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['full_date'], ['core.dim_calendar.full_date'], ),
        sa.ForeignKeyConstraint(['item_id'], ['core.dim_item.item_id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['core.dim_site.site_id'], ),
        sa.PrimaryKeyConstraint('inventory_id', 'full_date'),
        schema='core'
    )

    # Create indexes for fact_inventory_daily
    op.create_index('ix_fact_inventory_date', 'fact_inventory_daily', ['full_date'], unique=False, schema='core')
    op.create_index('ix_fact_inventory_item_site', 'fact_inventory_daily', ['item_id', 'site_id'], unique=False, schema='core')

    # Orders Fact (partitioned by month) - Initial table without partitioning for compatibility
    op.create_table('fact_orders',
        sa.Column('order_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('order_date', sa.Date(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=False),
        sa.Column('site_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('status', sa.Text(), nullable=False),
        sa.Column('expected_delivery_date', sa.Date(), nullable=True),
        sa.Column('actual_delivery_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['order_date'], ['core.dim_calendar.full_date'], ),
        sa.ForeignKeyConstraint(['item_id'], ['core.dim_item.item_id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['core.dim_site.site_id'], ),
        sa.ForeignKeyConstraint(['supplier_id'], ['core.dim_supplier.supplier_id'], ),
        sa.PrimaryKeyConstraint('order_id', 'order_date'),
        schema='core'
    )

    # Create indexes for fact_orders
    op.create_index('ix_fact_orders_date', 'fact_orders', ['order_date'], unique=False, schema='core')
    op.create_index('ix_fact_orders_status', 'fact_orders', ['status'], unique=False, schema='core')

    # Forecasts Table
    op.create_table('forecasts',
        sa.Column('forecast_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('full_date', sa.Date(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('site_id', sa.Integer(), nullable=False),
        sa.Column('horizon_days', sa.SmallInteger(), nullable=False),
        sa.Column('yhat', sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column('yhat_lower', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('yhat_upper', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('model_tag', sa.Text(), nullable=False),
        sa.Column('confidence_level', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('computed_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['full_date'], ['core.dim_calendar.full_date'], ),
        sa.ForeignKeyConstraint(['item_id'], ['core.dim_item.item_id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['core.dim_site.site_id'], ),
        sa.PrimaryKeyConstraint('forecast_id'),
        schema='analytics'
    )

    # Create indexes for forecasts
    op.create_index('ix_forecasts_item_site_date', 'forecasts', ['item_id', 'site_id', 'full_date'], unique=False, schema='analytics')
    op.create_index('ix_forecasts_horizon', 'forecasts', ['horizon_days'], unique=False, schema='analytics')
    op.create_index('ix_forecasts_computed', 'forecasts', ['computed_at'], unique=False, schema='analytics')

    # Features Store (flexible JSONB)
    op.create_table('features_store',
        sa.Column('feature_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('full_date', sa.Date(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('site_id', sa.Integer(), nullable=True),
        sa.Column('features', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('schema_version', sa.Text(), nullable=False, server_default='v1.0'),
        sa.Column('computed_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['full_date'], ['core.dim_calendar.full_date'], ),
        sa.ForeignKeyConstraint(['item_id'], ['core.dim_item.item_id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['core.dim_site.site_id'], ),
        sa.PrimaryKeyConstraint('feature_id'),
        schema='analytics'
    )

    # Create indexes for features_store
    op.create_index('ix_features_item_date', 'features_store', ['item_id', 'full_date'], unique=False, schema='analytics')
    op.create_index('gin_features_jsonb', 'features_store', ['features'], unique=False, postgresql_using='gin', schema='analytics')

    # KPIs Daily (aggregated metrics)
    op.create_table('kpis_daily',
        sa.Column('kpi_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('full_date', sa.Date(), nullable=False),
        sa.Column('total_demand', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('stockout_rate', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('abc_a_share', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('delayed_orders_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('forecast_mape', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('avg_inventory_value', sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column('computed_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['full_date'], ['core.dim_calendar.full_date'], ),
        sa.PrimaryKeyConstraint('kpi_id'),
        sa.UniqueConstraint('full_date', 'computed_at'),
        schema='analytics'
    )

    # Create indexes for kpis_daily
    op.create_index('ix_kpis_date', 'kpis_daily', ['full_date'], unique=False, schema='analytics')

    # Recommendations Table
    op.create_table('recommendations',
        sa.Column('recommendation_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=True),
        sa.Column('site_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.Text(), nullable=False),
        sa.Column('priority', sa.Text(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('action_date', sa.Date(), nullable=True),
        sa.Column('quantity_recommended', sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(), nullable=True),
        sa.Column('acknowledged_by', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['item_id'], ['core.dim_item.item_id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['core.dim_site.site_id'], ),
        sa.PrimaryKeyConstraint('recommendation_id'),
        schema='analytics'
    )

    # Create indexes for recommendations
    op.create_index('ix_recommendations_priority', 'recommendations', ['priority', 'created_at'], unique=False, schema='analytics')
    op.create_index('ix_recommendations_item', 'recommendations', ['item_id'], unique=False, schema='analytics')

    # Alerts Table
    op.create_table('alerts',
        sa.Column('alert_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=True),
        sa.Column('site_id', sa.Integer(), nullable=True),
        sa.Column('level', sa.Text(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['item_id'], ['core.dim_item.item_id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['core.dim_site.site_id'], ),
        sa.PrimaryKeyConstraint('alert_id'),
        schema='analytics'
    )

    # Create indexes for alerts
    op.create_index('ix_alerts_level_date', 'alerts', ['level', 'created_at'], unique=False, schema='analytics')
    op.create_index('ix_alerts_unread', 'alerts', ['read_at'], unique=False, schema='analytics', postgresql_where=sa.text('read_at IS NULL'))

    # Audit Logs
    op.create_table('audit_logs',
        sa.Column('audit_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('actor', sa.Text(), nullable=False),
        sa.Column('action', sa.Text(), nullable=False),
        sa.Column('entity_type', sa.Text(), nullable=True),
        sa.Column('entity_id', sa.BigInteger(), nullable=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="'{}'::jsonb"),
        sa.Column('ip_address', postgresql.INET(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('audit_id'),
        schema='support'
    )

    # Create indexes for audit_logs
    op.create_index('ix_audit_actor', 'audit_logs', ['actor'], unique=False, schema='support')
    op.create_index('ix_audit_timestamp', 'audit_logs', ['timestamp'], unique=False, schema='support')
    op.create_index('gin_audit_details', 'audit_logs', ['details'], unique=False, postgresql_using='gin', schema='support')

    # User Management (simple RBAC)
    op.create_table('users',
        sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.Text(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('password_hash', sa.Text(), nullable=False),
        sa.Column('role', sa.Text(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
        schema='support'
    )

    # Create indexes for users
    op.create_index('ix_users_username', 'users', ['username'], unique=False, schema='support')

    # Insert some basic region data
    op.execute("""
        INSERT INTO core.dim_region (name, state_code, economic_zone) VALUES
        ('São Paulo', 'SP', 'Sudeste'),
        ('Minas Gerais', 'MG', 'Sudeste'),
        ('Rio de Janeiro', 'RJ', 'Sudeste'),
        ('Espírito Santo', 'ES', 'Sudeste'),
        ('Rio Grande do Sul', 'RS', 'Sul'),
        ('Santa Catarina', 'SC', 'Sul'),
        ('Paraná', 'PR', 'Sul'),
        ('Bahia', 'BA', 'Nordeste'),
        ('Pernambuco', 'PE', 'Nordeste'),
        ('Ceará', 'CE', 'Nordeste'),
        ('Pará', 'PA', 'Norte'),
        ('Amazonas', 'AM', 'Norte'),
        ('Rondônia', 'RO', 'Norte'),
        ('Mato Grosso', 'MT', 'Centro-Oeste'),
        ('Goiás', 'GO', 'Centro-Oeste'),
        ('Mato Grosso do Sul', 'MS', 'Centro-Oeste'),
        ('Distrito Federal', 'DF', 'Centro-Oeste'),
        ('Acre', 'AC', 'Norte'),
        ('Amapá', 'AP', 'Norte'),
        ('Maranhão', 'MA', 'Nordeste'),
        ('Paraíba', 'PB', 'Nordeste'),
        ('Piauí', 'PI', 'Nordeste'),
        ('Rio Grande do Norte', 'RN', 'Nordeste'),
        ('Alagoas', 'AL', 'Nordeste'),
        ('Sergipe', 'SE', 'Nordeste'),
        ('Tocantins', 'TO', 'Norte'),
        ('Roraima', 'RR', 'Norte')
    """)


def downgrade():
    # Reverse the operations in reverse order
    op.drop_index('ix_users_username', table_name='users', schema='support')
    op.drop_table('users', schema='support')
    
    op.drop_index('gin_audit_details', table_name='audit_logs', schema='support', postgresql_using='gin')
    op.drop_index('ix_audit_timestamp', table_name='audit_logs', schema='support')
    op.drop_index('ix_audit_actor', table_name='audit_logs', schema='support')
    op.drop_table('audit_logs', schema='support')
    
    op.drop_index('ix_alerts_unread', table_name='alerts', schema='analytics', postgresql_where=sa.text('read_at IS NULL'))
    op.drop_index('ix_alerts_level_date', table_name='alerts', schema='analytics')
    op.drop_table('alerts', schema='analytics')
    
    op.drop_index('ix_recommendations_item', table_name='recommendations', schema='analytics')
    op.drop_index('ix_recommendations_priority', table_name='recommendations', schema='analytics')
    op.drop_table('recommendations', schema='analytics')
    
    op.drop_index('ix_kpis_date', table_name='kpis_daily', schema='analytics')
    op.drop_table('kpis_daily', schema='analytics')
    
    op.drop_index('gin_features_jsonb', table_name='features_store', schema='analytics', postgresql_using='gin')
    op.drop_index('ix_features_item_date', table_name='features_store', schema='analytics')
    op.drop_table('features_store', schema='analytics')
    
    op.drop_index('ix_forecasts_computed', table_name='forecasts', schema='analytics')
    op.drop_index('ix_forecasts_horizon', table_name='forecasts', schema='analytics')
    op.drop_index('ix_forecasts_item_site_date', table_name='forecasts', schema='analytics')
    op.drop_table('forecasts', schema='analytics')
    
    op.drop_index('ix_fact_orders_status', table_name='fact_orders', schema='core')
    op.drop_index('ix_fact_orders_date', table_name='fact_orders', schema='core')
    op.drop_table('fact_orders', schema='core')
    
    op.drop_index('ix_fact_inventory_item_site', table_name='fact_inventory_daily', schema='core')
    op.drop_index('ix_fact_inventory_date', table_name='fact_inventory_daily', schema='core')
    op.drop_table('fact_inventory_daily', schema='core')
    
    op.drop_index('ix_fact_demand_composite', table_name='fact_demand_daily', schema='core')
    op.drop_index('ix_fact_demand_site', table_name='fact_demand_daily', schema='core')
    op.drop_index('ix_fact_demand_item', table_name='fact_demand_daily', schema='core')
    op.drop_index('ix_fact_demand_date', table_name='fact_demand_daily', schema='core')
    op.drop_table('fact_demand_daily', schema='core')
    
    op.drop_index('ix_dim_supplier_type', table_name='dim_supplier', schema='core')
    op.drop_table('dim_supplier', schema='core')
    
    op.drop_index('ix_dim_site_region', table_name='dim_site', schema='core')
    op.drop_table('dim_site', schema='core')
    
    op.drop_table('dim_region', schema='core')
    
    op.drop_index('gin_dim_item_attrs', table_name='dim_item', schema='core', postgresql_using='gin')
    op.drop_index('ix_dim_item_abc', table_name='dim_item', schema='core')
    op.drop_index('ix_dim_item_family', table_name='dim_item', schema='core')
    op.drop_index('ix_dim_item_sku', table_name='dim_item', schema='core')
    op.drop_table('dim_item', schema='core')
    
    op.drop_index('ix_dim_calendar_year_month', table_name='dim_calendar', schema='core')
    op.drop_index('ix_dim_calendar_date', table_name='dim_calendar', schema='core')
    op.drop_table('dim_calendar', schema='core')
    
    # Drop schemas (in reverse order)
    op.execute('DROP SCHEMA IF EXISTS staging')
    op.execute('DROP SCHEMA IF EXISTS support')
    op.execute('DROP SCHEMA IF EXISTS analytics')
    op.execute('DROP SCHEMA IF EXISTS core')