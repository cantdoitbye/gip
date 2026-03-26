import redis.asyncio as redis

from app.config import settings


redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_client


async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None


async def redis_ping() -> bool:
    try:
        client = await get_redis()
        result = await client.ping()
        return result is True
    except Exception:
        return False
