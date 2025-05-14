import json
from typing import Optional, Any
import redis
from app.core.config import get_settings

settings = get_settings()


class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.default_ttl = 3600  # 1 hour

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        ttl = ttl or self.default_ttl
        self.redis_client.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        self.redis_client.delete(key)

    async def clear(self) -> None:
        """Clear all cache"""
        self.redis_client.flushdb()
