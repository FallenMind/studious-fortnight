class CacheRep:
    def __init__(self, redis_loop):
        self.redis = redis_loop

    async def set(self, key, value, expire=3600):
        await self.redis.set(key, value, expire=expire)

    async def get(self, key):
        return await self.redis.get(key)

    async def delete(self, key):
        return await self.redis.delete(key)

    async def exists(self, key):
        return await self.redis.exists(key)
