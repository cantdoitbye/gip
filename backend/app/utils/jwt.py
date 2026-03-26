from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.config import settings
from app.utils.cache import get_redis


ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    return payload


async def is_token_blacklisted(token: str) -> bool:
    redis = await get_redis()
    key = f"blacklist:{token}"
    return await redis.exists(key) > 0


async def blacklist_token(token: str) -> None:
    redis = await get_redis()
    key = f"blacklist:{token}"
    try:
        payload = decode_token(token)
        exp = payload.get("exp", 0)
        now = datetime.now(timezone.utc).timestamp()
        ttl = int(exp - now)
        if ttl > 0:
            await redis.setex(key, ttl, "1")
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass
