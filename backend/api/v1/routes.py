"""
API v1 Routes - Read-only Analytics Endpoints
PostgreSQL-powered REST API for Nova Corrente
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
from functools import wraps

# Create blueprint
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nova_corrente:password@localhost:5432/nova_corrente')
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)


# ===== UTILITY FUNCTIONS =====

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass


def handle_errors(f):
    """Error handling decorator"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 500
    return wrapper


# ===== ENDPOINTS =====

@api_v1.route('/items', methods=['GET'])
@handle_errors
def get_items():
    """
    Get items/materials catalog
    Query params: family, abc_class, limit, offset
    """
    family = request.args.get('family')
    abc_class = request.args.get('abc_class')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    query = """
        SELECT item_id, sku, name, family, category, abc_class, criticality, active
        FROM core.dim_item
        WHERE active = true
    """
    
    params = {}
    
    if family:
        query += " AND family = :family"
        params['family'] = family
    
    if abc_class:
        query += " AND abc_class = :abc_class"
        params['abc_class'] = abc_class
    
    query += " ORDER BY item_id LIMIT :limit OFFSET :offset"
    params['limit'] = limit
    params['offset'] = offset
    
    with SessionLocal() as session:
        result = session.execute(text(query), params)
        items = [dict(row._mapping) for row in result]
        
        # Get total count
        count_query = "SELECT COUNT(*) FROM core.dim_item WHERE active = true"
        count_params = {}
        if family:
            count_query += " AND family = :family"
            count_params['family'] = family
        if abc_class:
            count_query += " AND abc_class = :abc_class"
            count_params['abc_class'] = abc_class
        
        total = session.execute(text(count_query), count_params).scalar()
    
    return jsonify({
        'status': 'success',
        'data': items,
        'metadata': {
            'total_count': total,
            'limit': limit,
            'offset': offset
        }
    })


@api_v1.route('/items/<int:item_id>', methods=['GET'])
@handle_errors
def get_item(item_id):
    """Get single item details"""
    query = """
        SELECT item_id, sku, name, description, family, category, subcategory,
               unit_measure, abc_class, criticality, active, extra_attributes
        FROM core.dim_item
        WHERE item_id = :item_id
    """
    
    with SessionLocal() as session:
        result = session.execute(text(query), {'item_id': item_id})
        row = result.fetchone()
        
        if not row:
            return jsonify({'status': 'error', 'error': 'Item not found'}), 404
        
        item = dict(row._mapping)
    
    return jsonify(item)


@api_v1.route('/analytics/kpis', methods=['GET'])
@handle_errors
def get_kpis():
    """
    Get daily KPIs
    Query params: start_date, end_date (YYYY-MM-DD)
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = """
        SELECT full_date, total_demand, stockout_rate, abc_a_share,
               delayed_orders_pct, forecast_mape, avg_inventory_value, computed_at
        FROM analytics.kpis_daily
        WHERE 1=1
    """
    
    params = {}
    
    if start_date:
        query += " AND full_date >= :start_date"
        params['start_date'] = start_date
    
    if end_date:
        query += " AND full_date <= :end_date"
        params['end_date'] = end_date
    
    query += " ORDER BY full_date DESC LIMIT 90"
    
    with SessionLocal() as session:
        result = session.execute(text(query), params)
        kpis = [dict(row._mapping) for row in result]
    
    return jsonify({
        'status': 'success',
        'data': kpis,
        'metadata': {
            'total_count': len(kpis),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    })


@api_v1.route('/demand/timeseries', methods=['GET'])
@handle_errors
def get_demand_timeseries():
    """
    Get demand time series for an item
    Query params: item_id (required), site_id, start_date, end_date
    """
    item_id = request.args.get('item_id', type=int)
    site_id = request.args.get('site_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not item_id:
        return jsonify({'status': 'error', 'error': 'item_id is required'}), 400
    
    query = """
        SELECT full_date, SUM(quantity) as quantity
        FROM core.fact_demand_daily
        WHERE item_id = :item_id
    """
    
    params = {'item_id': item_id}
    
    if site_id:
        query += " AND site_id = :site_id"
        params['site_id'] = site_id
    
    if start_date:
        query += " AND full_date >= :start_date"
        params['start_date'] = start_date
    
    if end_date:
        query += " AND full_date <= :end_date"
        params['end_date'] = end_date
    
    query += " GROUP BY full_date ORDER BY full_date"
    
    with SessionLocal() as session:
        result = session.execute(text(query), params)
        data = [dict(row._mapping) for row in result]
    
    return jsonify({
        'status': 'success',
        'data': data,
        'metadata': {
            'item_id': item_id,
            'site_id': site_id
        }
    })


@api_v1.route('/inventory/timeseries', methods=['GET'])
@handle_errors
def get_inventory_timeseries():
    """
    Get inventory levels time series
    Query params: item_id (required), site_id (required), start_date, end_date
    """
    item_id = request.args.get('item_id', type=int)
    site_id = request.args.get('site_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not item_id or not site_id:
        return jsonify({'status': 'error', 'error': 'item_id and site_id are required'}), 400
    
    query = """
        SELECT full_date, current_stock, safety_stock, reorder_point, days_to_rupture
        FROM core.fact_inventory_daily
        WHERE item_id = :item_id AND site_id = :site_id
    """
    
    params = {'item_id': item_id, 'site_id': site_id}
    
    if start_date:
        query += " AND full_date >= :start_date"
        params['start_date'] = start_date
    
    if end_date:
        query += " AND full_date <= :end_date"
        params['end_date'] = end_date
    
    query += " ORDER BY full_date"
    
    with SessionLocal() as session:
        result = session.execute(text(query), params)
        data = [dict(row._mapping) for row in result]
    
    return jsonify({
        'status': 'success',
        'data': data
    })


@api_v1.route('/forecasts', methods=['GET'])
@handle_errors
def get_forecasts():
    """
    Get forecasts for an item
    Query params: item_id (required), site_id, horizon, start_date, end_date
    """
    item_id = request.args.get('item_id', type=int)
    site_id = request.args.get('site_id', type=int)
    horizon = request.args.get('horizon', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not item_id:
        return jsonify({'status': 'error', 'error': 'item_id is required'}), 400
    
    query = """
        SELECT full_date, yhat, yhat_lower, yhat_upper, horizon_days, model_tag, computed_at
        FROM analytics.forecasts
        WHERE item_id = :item_id
    """
    
    params = {'item_id': item_id}
    
    if site_id:
        query += " AND site_id = :site_id"
        params['site_id'] = site_id
    
    if horizon:
        query += " AND horizon_days = :horizon"
        params['horizon'] = horizon
    
    if start_date:
        query += " AND full_date >= :start_date"
        params['start_date'] = start_date
    
    if end_date:
        query += " AND full_date <= :end_date"
        params['end_date'] = end_date
    
    query += " ORDER BY full_date LIMIT 100"
    
    with SessionLocal() as session:
        result = session.execute(text(query), params)
        data = [dict(row._mapping) for row in result]
    
    return jsonify({
        'status': 'success',
        'data': data,
        'metadata': {
            'total_count': len(data)
        }
    })


@api_v1.route('/recommendations', methods=['GET'])
@handle_errors
def get_recommendations():
    """
    Get recommendations
    Query params: priority, site_id, limit
    """
    priority = request.args.get('priority')
    site_id = request.args.get('site_id', type=int)
    limit = request.args.get('limit', 20, type=int)
    
    query = """
        SELECT recommendation_id, item_id, site_id, type, priority, message,
               action_date, quantity_recommended, created_at, acknowledged_at
        FROM analytics.recommendations
        WHERE 1=1
    """
    
    params = {}
    
    if priority:
        query += " AND priority = :priority"
        params['priority'] = priority
    
    if site_id:
        query += " AND site_id = :site_id"
        params['site_id'] = site_id
    
    query += " ORDER BY priority DESC, created_at DESC LIMIT :limit"
    params['limit'] = limit
    
    with SessionLocal() as session:
        result = session.execute(text(query), params)
        data = [dict(row._mapping) for row in result]
    
    return jsonify({
        'status': 'success',
        'data': data
    })


@api_v1.route('/recommendations/<int:rec_id>/acknowledge', methods=['PATCH'])
@handle_errors
def acknowledge_recommendation(rec_id):
    """Mark recommendation as acknowledged"""
    data = request.get_json() or {}
    acknowledged_by = data.get('acknowledged_by', 'system')
    
    query = """
        UPDATE analytics.recommendations
        SET acknowledged_at = CURRENT_TIMESTAMP,
            acknowledged_by = :acknowledged_by
        WHERE recommendation_id = :rec_id
    """
    
    with SessionLocal() as session:
        session.execute(text(query), {'rec_id': rec_id, 'acknowledged_by': acknowledged_by})
        session.commit()
    
    return jsonify({'status': 'success'})


@api_v1.route('/alerts', methods=['GET'])
@handle_errors
def get_alerts():
    """
    Get alerts
    Query params: level, unread (bool), limit
    """
    level = request.args.get('level')
    unread = request.args.get('unread', 'false').lower() == 'true'
    limit = request.args.get('limit', 50, type=int)
    
    query = """
        SELECT alert_id, item_id, site_id, level, category, message,
               created_at, read_at, resolved_at
        FROM analytics.alerts
        WHERE 1=1
    """
    
    params = {}
    
    if level:
        query += " AND level = :level"
        params['level'] = level
    
    if unread:
        query += " AND read_at IS NULL"
    
    query += " ORDER BY level DESC, created_at DESC LIMIT :limit"
    params['limit'] = limit
    
    with SessionLocal() as session:
        result = session.execute(text(query), params)
        data = [dict(row._mapping) for row in result]
    
    return jsonify({
        'status': 'success',
        'data': data
    })


@api_v1.route('/alerts/<int:alert_id>/mark-read', methods=['PATCH'])
@handle_errors
def mark_alert_read(alert_id):
    """Mark alert as read"""
    query = """
        UPDATE analytics.alerts
        SET read_at = CURRENT_TIMESTAMP
        WHERE alert_id = :alert_id
    """
    
    with SessionLocal() as session:
        session.execute(text(query), {'alert_id': alert_id})
        session.commit()
    
    return jsonify({'status': 'success'})


@api_v1.route('/features', methods=['GET'])
@handle_errors
def get_features():
    """
    Get features for an item
    Query params: item_id (required), start_date, end_date
    """
    item_id = request.args.get('item_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not item_id:
        return jsonify({'status': 'error', 'error': 'item_id is required'}), 400
    
    query = """
        SELECT full_date, features, schema_version, computed_at
        FROM analytics.features_store
        WHERE item_id = :item_id
    """
    
    params = {'item_id': item_id}
    
    if start_date:
        query += " AND full_date >= :start_date"
        params['start_date'] = start_date
    
    if end_date:
        query += " AND full_date <= :end_date"
        params['end_date'] = end_date
    
    query += " ORDER BY full_date DESC LIMIT 90"
    
    with SessionLocal() as session:
        result = session.execute(text(query), params)
        data = [dict(row._mapping) for row in result]
    
    return jsonify({
        'status': 'success',
        'data': data
    })
