"""
Redis cache service for caching AI responses.
"""
import json
import hashlib
from typing import Optional, Any
import redis.asyncio as redis
from app.core.config import settings


class CacheService:
    """Service for caching AI responses using Redis."""

    def __init__(self):
        """Initialize Redis connection."""
        self.redis: Optional[redis.Redis] = None
        self.enabled = settings.REDIS_ENABLED

    async def connect(self):
        """Connect to Redis."""
        if not self.enabled:
            return

        try:
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
            await self.redis.ping()
            print("✅ Connected to Redis cache")
        except Exception as e:
            print(f"⚠️  Redis connection failed: {e}")
            self.enabled = False

    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()

    def _generate_key(self, prefix: str, **kwargs) -> str:
        """
        Generate a cache key from parameters.

        Args:
            prefix: Key prefix (e.g., 'generate', 'explain')
            **kwargs: Parameters to include in the key

        Returns:
            Cache key string
        """
        # Sort kwargs for consistent hashing
        sorted_params = sorted(kwargs.items())
        param_str = json.dumps(sorted_params, sort_keys=True)

        # Create hash of parameters
        param_hash = hashlib.sha256(param_str.encode()).hexdigest()[:16]

        return f"{settings.CACHE_PREFIX}:{prefix}:{param_hash}"

    async def get(self, prefix: str, **kwargs) -> Optional[dict]:
        """
        Get cached value.

        Args:
            prefix: Cache key prefix
            **kwargs: Parameters for cache key

        Returns:
            Cached value or None if not found
        """
        if not self.enabled or not self.redis:
            return None

        try:
            key = self._generate_key(prefix, **kwargs)
            cached = await self.redis.get(key)

            if cached:
                return json.loads(cached)

            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    async def set(
        self, prefix: str, value: Any, ttl: Optional[int] = None, **kwargs
    ) -> bool:
        """
        Set cached value.

        Args:
            prefix: Cache key prefix
            value: Value to cache
            ttl: Time to live in seconds (default from settings)
            **kwargs: Parameters for cache key

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.redis:
            return False

        try:
            key = self._generate_key(prefix, **kwargs)
            ttl = ttl or settings.CACHE_TTL

            await self.redis.setex(
                key, ttl, json.dumps(value, ensure_ascii=False)
            )

            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    async def delete(self, prefix: str, **kwargs) -> bool:
        """
        Delete cached value.

        Args:
            prefix: Cache key prefix
            **kwargs: Parameters for cache key

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.redis:
            return False

        try:
            key = self._generate_key(prefix, **kwargs)
            await self.redis.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False

    async def clear_all(self) -> bool:
        """
        Clear all cache entries with the app prefix.

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.redis:
            return False

        try:
            pattern = f"{settings.CACHE_PREFIX}:*"
            cursor = 0

            while True:
                cursor, keys = await self.redis.scan(
                    cursor, match=pattern, count=100
                )

                if keys:
                    await self.redis.delete(*keys)

                if cursor == 0:
                    break

            return True
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False

    async def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        if not self.enabled or not self.redis:
            return {"enabled": False}

        try:
            info = await self.redis.info()
            pattern = f"{settings.CACHE_PREFIX}:*"

            # Count keys with our prefix
            cursor = 0
            key_count = 0

            while True:
                cursor, keys = await self.redis.scan(
                    cursor, match=pattern, count=100
                )
                key_count += len(keys)

                if cursor == 0:
                    break

            return {
                "enabled": True,
                "keys": key_count,
                "memory_used": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "uptime_days": info.get("uptime_in_days", 0),
            }
        except Exception as e:
            print(f"Cache stats error: {e}")
            return {"enabled": True, "error": str(e)}


# Singleton instance
cache_service = CacheService()
