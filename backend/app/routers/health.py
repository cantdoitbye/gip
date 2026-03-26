from fastapi import APIRouter
from sqlalchemy import text

from app.schemas.health import HealthResponse, DetailedHealthResponse, ServicesHealth

router = APIRouter(prefix="/health", tags=["health"])

VERSION = "1.0.0"


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="healthy", version=VERSION)


@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check() -> DetailedHealthResponse:
    from app.database import engine
    from app.utils.cache import redis_ping

    db_status = "healthy"
    redis_status = "healthy"

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        print(f"Database health check failed: {e}")
        db_status = "unhealthy"

    try:
        redis_healthy = await redis_ping()
        if not redis_healthy:
            redis_status = "unhealthy"
    except Exception as e:
        print(f"Redis health check failed: {e}")
        redis_status = "unhealthy"

    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"

    return DetailedHealthResponse(
        status=overall_status,
        version=VERSION,
        services=ServicesHealth(database=db_status, redis=redis_status),
    )
