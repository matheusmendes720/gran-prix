from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import datetime
from typing import Dict, Any, Optional
import jwt
from functools import wraps
from passlib.context import CryptContext
import hashlib

app = Flask(__name__)
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))

# Determine cache type - Redis if available, otherwise simple in-memory
if os.getenv('USE_REDIS_CACHE', 'false').lower() == 'true':
    # Redis cache configuration
    cache = Cache(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        'CACHE_DEFAULT_TIMEOUT': 300,  # Default 5 minutes
        'CACHE_KEY_PREFIX': 'nova_corrente_'
    })
else:
    # Simple cache configuration for development
    cache = Cache(app, config={
        'CACHE_TYPE': 'simple', 
        'CACHE_DEFAULT_TIMEOUT': 300,  # Default 5 minutes
        'CACHE_KEY_PREFIX': 'nova_corrente_'
    })

def make_cache_key(*args, **kwargs):
    """Create a cache key based on the request parameters"""
    path = request.path
    args = str(sorted(request.args.items()))
    return hashlib.md5((path + args).encode('utf-8')).hexdigest()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nova_corrente:strong_password@localhost:5432/nova_corrente')
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600    # Recycle connections every hour
)
SessionLocal = sessionmaker(bind=engine)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_token(user_id: int, role: str) -> str:
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def token_required(roles: Optional[list] = None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return jsonify({'error': 'No token provided'}), 401
            
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                if roles and payload['role'] not in roles:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                return f(payload, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
        return wrapper
    return decorator

def log_audit(actor: str, action: str, entity_type: str, entity_id: Optional[int], details: Dict[str, Any]):
    """Log audit event to database"""
    with SessionLocal() as session:
        session.execute(text("""
            INSERT INTO support.audit_logs (actor, action, entity_type, entity_id, details, ip_address, timestamp)
            VALUES (:actor, :action, :entity_type, :entity_id, :details, :ip, NOW())
        """), {
            'actor': actor,
            'action': action,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'details': details,
            'ip': request.remote_addr
        })
        session.commit()

@app.route('/health', methods=['GET'])
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'cache': 'configured',
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'version': '3.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'degraded',
            'database': 'disconnected',
            'error': str(e)
        }), 503

@app.route('/api/v1/analytics/kpis', methods=['GET'])
def get_kpis():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Create a custom cache key based on parameters
    cache_key = f"kpis_{start_date}_{end_date}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    query = text("""
        SELECT full_date, total_demand, stockout_rate, abc_a_share, 
               delayed_orders_pct, forecast_mape, computed_at
        FROM analytics.kpis_daily
        WHERE (:start_date IS NULL OR full_date >= :start_date)
          AND (:end_date IS NULL OR full_date <= :end_date)
        ORDER BY full_date DESC
    """)
    
    with SessionLocal() as session:
        result = session.execute(query, {'start_date': start_date, 'end_date': end_date})
        data = [dict(row._mapping) for row in result]
    
    response_data = {
        'status': 'success',
        'data': data,
        'metadata': {'total_count': len(data)}
    }
    
    # Cache for 10 minutes for KPIs since they update daily
    cache.set(cache_key, response_data, timeout=600)
    
    return jsonify(response_data)

@app.route('/api/v1/items', methods=['GET'])
def get_items():
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    family = request.args.get('family')
    abc_class = request.args.get('abc_class')
    
    # Create cache key based on parameters
    cache_key = f"items_{limit}_{offset}_{family}_{abc_class}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    base_query = "SELECT item_id, sku, name, family, category, abc_class, criticality FROM core.dim_item WHERE active = true"
    conditions = []
    params = {'limit': limit, 'offset': offset}
    
    if family:
        conditions.append("family = :family")
        params['family'] = family
    
    if abc_class:
        conditions.append("abc_class = :abc_class")
        params['abc_class'] = abc_class
    
    if conditions:
        base_query += " AND " + " AND ".join(conditions)
    
    base_query += " ORDER BY item_id LIMIT :limit OFFSET :offset"
    
    with SessionLocal() as session:
        result = session.execute(text(base_query), params)
        data = [dict(row._mapping) for row in result]
        
        # Get total count
        count_query = "SELECT COUNT(*) FROM core.dim_item WHERE active = true"
        if conditions:
            count_query += " AND " + " AND ".join(conditions)
        count_result = session.execute(text(count_query), params)
        total_count = count_result.scalar()
    
    response_data = {
        'status': 'success',
        'data': data,
        'metadata': {'total_count': total_count}
    }
    
    # Cache for 30 minutes for items since they don't change frequently
    cache.set(cache_key, response_data, timeout=1800)
    
    return jsonify(response_data)

@app.route('/api/v1/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # Create cache key for single item
    cache_key = f"item_{item_id}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    query = text("""
        SELECT item_id, sku, name, description, family, category, subcategory, 
               unit_measure, abc_class, criticality, active, min_order_qty, 
               max_order_qty, extra_attributes
        FROM core.dim_item
        WHERE item_id = :item_id
    """)
    
    with SessionLocal() as session:
        result = session.execute(query, {'item_id': item_id})
        item = result.fetchone()
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
    
    item_dict = dict(item._mapping)
    
    # Cache for 1 hour for individual items
    cache.set(cache_key, item_dict, timeout=3600)
    
    return jsonify(item_dict)

@app.route('/api/v1/demand/timeseries', methods=['GET'])
def get_demand_timeseries():
    item_id = request.args.get('item_id', type=int)
    site_id = request.args.get('site_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Create cache key
    cache_key = f"demand_ts_{item_id}_{site_id}_{start_date}_{end_date}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    query = text("""
        SELECT full_date, quantity
        FROM core.fact_demand_daily
        WHERE (:item_id IS NULL OR item_id = :item_id)
          AND (:site_id IS NULL OR site_id = :site_id)
          AND (:start_date IS NULL OR full_date >= :start_date)
          AND (:end_date IS NULL OR full_date <= :end_date)
        ORDER BY full_date
    """)
    
    params = {
        'item_id': item_id,
        'site_id': site_id,
        'start_date': start_date,
        'end_date': end_date
    }
    
    with SessionLocal() as session:
        result = session.execute(query, params)
        data = [dict(row._mapping) for row in result]
    
    response_data = {
        'status': 'success',
        'data': data,
        'metadata': {'item_id': item_id, 'site_id': site_id}
    }
    
    # Cache for 30 minutes for demand series
    cache.set(cache_key, response_data, timeout=1800)
    
    return jsonify(response_data)

@app.route('/api/v1/inventory/timeseries', methods=['GET'])
def get_inventory_timeseries():
    item_id = request.args.get('item_id', type=int)
    site_id = request.args.get('site_id', type=int)
    start_date = request.args.get('start_date')
    
    # Create cache key
    cache_key = f"inventory_ts_{item_id}_{site_id}_{start_date}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    query = text("""
        SELECT full_date, current_stock, safety_stock, reorder_point, days_to_rupture
        FROM core.fact_inventory_daily
        WHERE (:item_id IS NULL OR item_id = :item_id)
          AND (:site_id IS NULL OR site_id = :site_id)
          AND (:start_date IS NULL OR full_date >= :start_date)
        ORDER BY full_date
    """)
    
    params = {
        'item_id': item_id,
        'site_id': site_id,
        'start_date': start_date
    }
    
    with SessionLocal() as session:
        result = session.execute(query, params)
        data = [dict(row._mapping) for row in result]
    
    response_data = {
        'status': 'success',
        'data': data,
        'metadata': {'item_id': item_id, 'site_id': site_id}
    }
    
    # Cache for 15 minutes for inventory series
    cache.set(cache_key, response_data, timeout=900)
    
    return jsonify(response_data)

@app.route('/api/v1/forecasts', methods=['GET'])
def get_forecasts():
    item_id = request.args.get('item_id', type=int)
    site_id = request.args.get('site_id', type=int)
    horizon = request.args.get('horizon', type=int)
    start_date = request.args.get('start_date')
    
    # Create cache key based on parameters
    cache_key = f"forecasts_{item_id}_{site_id}_{horizon}_{start_date}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    query = text("""
        SELECT full_date, yhat, yhat_lower, yhat_upper, model_tag, horizon_days
        FROM analytics.forecasts
        WHERE (:item_id IS NULL OR item_id = :item_id)
          AND (:site_id IS NULL OR site_id = :site_id)
          AND (:horizon IS NULL OR horizon_days = :horizon)
          AND (:start_date IS NULL OR full_date >= :start_date)
        ORDER BY full_date
    """)
    
    params = {
        'item_id': item_id,
        'site_id': site_id,
        'horizon': horizon,
        'start_date': start_date
    }
    
    with SessionLocal() as session:
        result = session.execute(query, params)
        data = [dict(row._mapping) for row in result]
    
    response_data = {
        'status': 'success',
        'data': data,
        'metadata': {'computed_at': datetime.datetime.utcnow().isoformat() + 'Z'}
    }
    
    # Cache for 15 minutes for forecasts
    cache.set(cache_key, response_data, timeout=900)
    
    return jsonify(response_data)

@app.route('/api/v1/features', methods=['GET'])
def get_features():
    item_id = request.args.get('item_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Create cache key
    cache_key = f"features_{item_id}_{start_date}_{end_date}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    query = text("""
        SELECT full_date, features, schema_version, computed_at
        FROM analytics.features_store
        WHERE (:item_id IS NULL OR item_id = :item_id)
          AND (:start_date IS NULL OR full_date >= :start_date)
          AND (:end_date IS NULL OR full_date <= :end_date)
        ORDER BY full_date
    """)
    
    params = {
        'item_id': item_id,
        'start_date': start_date,
        'end_date': end_date
    }
    
    with SessionLocal() as session:
        result = session.execute(query, params)
        data = [dict(row._mapping) for row in result]
    
    response_data = {
        'status': 'success',
        'data': data
    }
    
    # Cache for 30 minutes for features
    cache.set(cache_key, response_data, timeout=1800)
    
    return jsonify(response_data)

@app.route('/api/v1/recommendations', methods=['GET'])
def get_recommendations():
    priority = request.args.get('priority')
    site_id = request.args.get('site_id', type=int)
    limit = int(request.args.get('limit', 20))
    
    # Create cache key
    cache_key = f"recoms_{priority}_{site_id}_{limit}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    query = text("""
        SELECT recommendation_id, item_id, site_id, type, priority, message,
               action_date, quantity_recommended, created_at, acknowledged_at, acknowledged_by
        FROM analytics.recommendations
        WHERE (:priority IS NULL OR priority = :priority)
          AND (:site_id IS NULL OR site_id = :site_id)
        ORDER BY 
            CASE priority
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
            END,
            created_at DESC
        LIMIT :limit
    """)
    
    params = {
        'priority': priority,
        'site_id': site_id,
        'limit': limit
    }
    
    with SessionLocal() as session:
        result = session.execute(query, params)
        data = [dict(row._mapping) for row in result]
    
    response_data = {
        'status': 'success',
        'data': data
    }
    
    # Cache for 5 minutes for recommendations (frequently changing)
    cache.set(cache_key, response_data, timeout=300)
    
    return jsonify(response_data)

@app.route('/api/v1/recommendations/<int:rec_id>/acknowledge', methods=['PATCH'])
@token_required(roles=['ADMIN', 'ANALYST'])
def acknowledge_recommendation(payload, rec_id):
    # Invalidate the recommendations cache after an update
    cache.delete_many([f"recoms_{priority}_{site_id}_{limit}" 
                      for priority in [None, 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
                      for site_id in range(1, 10)  # Assuming up to 10 sites
                      for limit in [20, 50, 100]])  # Common limits
    
    acknowledged_by = payload['user_id']
    
    query = text("""
        UPDATE analytics.recommendations
        SET acknowledged_at = NOW(), acknowledged_by = :acknowledged_by
        WHERE recommendation_id = :rec_id
        RETURNING recommendation_id
    """)
    
    with SessionLocal() as session:
        result = session.execute(query, {'rec_id': rec_id, 'acknowledged_by': acknowledged_by})
        row = result.fetchone()
        
        if not row:
            return jsonify({'error': 'Recommendation not found'}), 404
        
        session.commit()
        
        # Log the audit event
        log_audit(
            actor=payload['user_id'],
            action='ACKNOWLEDGE_RECOMMENDATION',
            entity_type='recommendation',
            entity_id=rec_id,
            details={'acknowledged_at': datetime.datetime.utcnow().isoformat()}
        )
    
    return jsonify({'status': 'success'})

@app.route('/api/v1/alerts', methods=['GET'])
def get_alerts():
    level = request.args.get('level')
    unread = request.args.get('unread', type=bool)
    
    # Create cache key
    cache_key = f"alerts_{level}_{unread}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    query = text("""
        SELECT alert_id, item_id, site_id, level, category, message, created_at, read_at, resolved_at
        FROM analytics.alerts
        WHERE (:level IS NULL OR level = :level)
          AND (:unread IS NULL OR (:unread = true AND read_at IS NULL) OR (:unread = false AND read_at IS NOT NULL))
        ORDER BY 
            CASE level
                WHEN 'CRITICAL' THEN 1
                WHEN 'WARNING' THEN 2
                WHEN 'NORMAL' THEN 3
            END,
            created_at DESC
    """)
    
    params = {
        'level': level,
        'unread': unread
    }
    
    with SessionLocal() as session:
        result = session.execute(query, params)
        data = [dict(row._mapping) for row in result]
    
    response_data = {
        'status': 'success',
        'data': data
    }
    
    # Cache for 2 minutes for alerts (very frequently changing)
    cache.set(cache_key, response_data, timeout=120)
    
    return jsonify(response_data)

@app.route('/api/v1/alerts/<int:alert_id>/mark-read', methods=['PATCH'])
@token_required(roles=['ADMIN', 'ANALYST', 'VIEWER'])
def mark_alert_read(payload, alert_id):
    # Invalidate the alerts cache after an update
    cache.delete_many([f"alerts_{level}_{unread}" 
                      for level in [None, 'CRITICAL', 'WARNING', 'NORMAL']
                      for unread in [None, True, False]])
    
    query = text("""
        UPDATE analytics.alerts
        SET read_at = NOW()
        WHERE alert_id = :alert_id
        RETURNING alert_id
    """)
    
    with SessionLocal() as session:
        result = session.execute(query, {'alert_id': alert_id})
        row = result.fetchone()
        
        if not row:
            return jsonify({'error': 'Alert not found'}), 404
        
        session.commit()
    
    return jsonify({'status': 'success'})

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Verify credentials against database
    query = text("SELECT user_id, username, role, password_hash FROM support.users WHERE username = :username AND active = true")
    
    with SessionLocal() as session:
        result = session.execute(query, {'username': username})
        user = result.fetchone()
        
        if not user or not verify_password(password, user.password_hash):
            return jsonify({'error': 'Invalid credentials'}), 401
    
    # Update last login time
    update_query = text("UPDATE support.users SET last_login = NOW() WHERE user_id = :user_id")
    session.execute(update_query, {'user_id': user.user_id})
    session.commit()
    
    # Create token
    token = create_token(user.user_id, user.role)
    
    return jsonify({
        'access_token': token,
        'expires_in': ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert minutes to seconds
        'token_type': 'bearer',
        'user': {
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role
        }
    })


@app.route('/api/v1/auth/refresh', methods=['POST'])
@token_required()  # Requires valid token
def refresh_token(payload):
    # Create new token with updated expiration
    new_token = create_token(payload['user_id'], payload['role'])
    
    return jsonify({
        'access_token': new_token,
        'expires_in': ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        'token_type': 'bearer'
    })


@app.route('/api/v1/auth/profile', methods=['GET'])
@token_required()
def get_profile(payload):
    # Get user profile information
    query = text("SELECT user_id, username, email, role, created_at FROM support.users WHERE user_id = :user_id")
    
    with SessionLocal() as session:
        result = session.execute(query, {'user_id': payload['user_id']})
        user = result.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat() if user.created_at else None
    })

@app.route('/api/v1/cache/clear', methods=['POST'])
@token_required(roles=['ADMIN'])
def clear_cache(payload):
    """Clear the entire cache - only for admin users"""
    try:
        cache.clear()
        log_audit(
            actor=payload['user_id'],
            action='CLEAR_CACHE',
            entity_type='cache',
            entity_id=None,
            details={'status': 'success'}
        )
        return jsonify({'status': 'success', 'message': 'Cache cleared successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/v1/cache/stats', methods=['GET'])
@token_required(roles=['ADMIN'])
def cache_stats(payload):
    """Get cache statistics - only for admin users"""
    try:
        # For simple cache, we can't get detailed stats, but we can return a message
        return jsonify({
            'status': 'success',
            'cache_type': 'simple' if cache.config['CACHE_TYPE'] == 'simple' else 'redis',
            'message': 'Cache is running. Detailed stats not available for simple cache backend.'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)