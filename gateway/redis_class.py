import redis
import json
from typing import Any, Optional


def get_redis():
    return RedisClient()


class RedisClient:
    def __init__(self, host: str = 'redis', port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)

    def set_(self, key: str, value: Any, ttl: int = 30) -> None:
        """ Set a key-value pair in Redis with optional TTL """
        self.redis_client.set(key, json.dumps(value))
        if ttl:
            self.redis_client.expire(key, ttl)

    def get_(self, key: str) -> Optional[Any]:

        """ Get a value from Redis by key """
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def delete(self, key: str) -> None:
        """ Delete a key from Redis """
        self.redis_client.delete(key)

    def expire(self, key: str, ttl: int) -> bool:
        """ Set expiration (TTL) for a key in seconds """
        return self.redis_client.expire(key, ttl)

    def ttl(self, key: str) -> Optional[int]:
        """ Get time-to-live (TTL) of a key in seconds """
        return self.redis_client.ttl(key)
