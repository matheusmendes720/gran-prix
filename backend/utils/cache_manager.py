"""
Cache manager for Nova Corrente services
Supports both Redis and file-based caching
"""
import os
import json
import pickle
from pathlib import Path
from typing import Any, Optional, Callable
from datetime import datetime, timedelta
import hashlib

# Try to import Redis, fall back to file cache if not available
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.cache')


class CacheManager:
    """
    Unified cache manager supporting Redis and file-based caching
    """
    def __init__(self, use_redis: bool = True):
        self.use_redis = use_redis and REDIS_AVAILABLE
        self.cache_dir = Path(os.getenv('CACHE_DIR', 'cache'))
        self.cache_dir.mkdir(exist_ok=True)
        
        if self.use_redis:
            try:
                self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'),
                    port=int(os.getenv('REDIS_PORT', 6379)),
                    db=int(os.getenv('REDIS_DB', 0)),
                    decode_responses=False  # Use bytes for pickle
                )
                # Test connection
                self.redis_client.ping()
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.warning(f"Redis unavailable, falling back to file cache: {e}")
                self.use_redis = False
                self.redis_client = None
        else:
            self.redis_client = None
            logger.info("Using file-based cache")
    
    def _get_key_hash(self, key: str) -> str:
        """Generate hash for cache key"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_file_path(self, key: str) -> Path:
        """Get file path for cache key"""
        key_hash = self._get_key_hash(key)
        return self.cache_dir / f"{key_hash}.cache"
    
    def get(self, key: str, default: Any = None) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            default: Default value if not found
        
        Returns:
            Cached value or default
        """
        try:
            if self.use_redis:
                cached = self.redis_client.get(key)
                if cached:
                    return pickle.loads(cached)
            else:
                file_path = self._get_file_path(key)
                if file_path.exists():
                    with open(file_path, 'rb') as f:
                        cache_data = pickle.load(f)
                        # Check expiration
                        if cache_data.get('expires_at') and datetime.now() > cache_data['expires_at']:
                            file_path.unlink()
                            return default
                        return cache_data['value']
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return default
        
        return default
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache with optional TTL
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None for no expiration)
        
        Returns:
            True if successful
        """
        try:
            if self.use_redis:
                if ttl:
                    self.redis_client.setex(key, ttl, pickle.dumps(value))
                else:
                    self.redis_client.set(key, pickle.dumps(value))
            else:
                file_path = self._get_file_path(key)
                cache_data = {
                    'value': value,
                    'created_at': datetime.now(),
                    'expires_at': datetime.now() + timedelta(seconds=ttl) if ttl else None
                }
                with open(file_path, 'wb') as f:
                    pickle.dump(cache_data, f)
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        
        Args:
            key: Cache key
        
        Returns:
            True if deleted
        """
        try:
            if self.use_redis:
                return bool(self.redis_client.delete(key))
            else:
                file_path = self._get_file_path(key)
                if file_path.exists():
                    file_path.unlink()
                    return True
            return False
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def clear(self, pattern: str = None) -> int:
        """
        Clear cache entries matching pattern
        
        Args:
            pattern: Optional pattern to match (None for all)
        
        Returns:
            Number of entries deleted
        """
        try:
            count = 0
            if self.use_redis:
                if pattern:
                    keys = self.redis_client.keys(pattern)
                    if keys:
                        count = self.redis_client.delete(*keys)
                else:
                    count = self.redis_client.flushdb()
            else:
                if pattern:
                    for file_path in self.cache_dir.glob("*.cache"):
                        # Could implement pattern matching here
                        file_path.unlink()
                        count += 1
                else:
                    for file_path in self.cache_dir.glob("*.cache"):
                        file_path.unlink()
                        count += 1
            logger.info(f"Cleared {count} cache entries")
            return count
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return 0
    
    def get_or_set(
        self,
        key: str,
        default_factory: Callable[[], Any],
        ttl: Optional[int] = None
    ) -> Any:
        """
        Get value from cache or set using factory function
        
        Args:
            key: Cache key
            default_factory: Function to generate value if not cached
            ttl: Time to live in seconds
        
        Returns:
            Cached or newly generated value
        """
        value = self.get(key)
        if value is None:
            value = default_factory()
            self.set(key, value, ttl)
        return value
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache
        
        Args:
            key: Cache key
        
        Returns:
            True if exists
        """
        try:
            if self.use_redis:
                return bool(self.redis_client.exists(key))
            else:
                return self._get_file_path(key).exists()
        except Exception as e:
            logger.error(f"Cache exists check error for key {key}: {e}")
            return False


# Singleton instance
cache_manager = CacheManager(use_redis=REDIS_AVAILABLE)

