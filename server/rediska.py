class CacheRep:
    def __init__(self, redis_loop):
        self.redis = redis_loop

    async def set(self, key, value, expire=3600):
        await self.redis.set(key, value)
        await self.redis.expire(key, expire)

    async def get(self, key):
        return await self.redis.get(key)

    async def delete(self, key):
        return await self.redis.delete(key)

    async def exists(self, key):
        return await self.redis.exists(key)

    async def flush_db(self):
        await self.redis.flushdb()

    async def delete_by_pattern(self, pattern: str):
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)
