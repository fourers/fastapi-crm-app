import asyncio
import logging
from typing import Literal

import httpx
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text

from app.config.keycloak import settings
from app.database.admin import provide_db
from app.utils.redis import get_client

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


class LivenessResponse(BaseModel):
    status: Literal["alive"]


@router.get("/health/live", response_model=LivenessResponse)
async def liveness():
    return {"status": "alive"}


class ReadinessResponse(BaseModel):
    status: Literal["ready"]
    database: Literal["healthy", "unhealthy"]
    redis: Literal["healthy", "unhealthy"]
    keycloak: Literal["healthy", "unhealthy"]


async def check_database() -> bool:
    try:
        with provide_db() as db:
            db.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.warning("Database healthcheck failed", exc_info=True)
        return False


async def check_redis() -> bool:
    try:
        get_client().ping()
        return True
    except Exception:
        logger.warning("Redis healthcheck failed", exc_info=True)
        return False


async def check_keycloak() -> bool:
    try:
        response = httpx.get(
            f"{settings.server_url}/realms/{settings.realm}/.well-known/openid-configuration"
        )
        response.raise_for_status()
        return True
    except Exception:
        logger.warning("Keycloak healthcheck failed", exc_info=True)
        return False


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Application is not ready",
        },
    },
)
async def readiness():
    db_healthy, redis_healthy, keycloak_healthy = await asyncio.gather(
        check_database(),
        check_redis(),
        check_keycloak(),
    )
    details = {
        "database": "healthy" if db_healthy else "unhealthy",
        "redis": "healthy" if redis_healthy else "unhealthy",
        "keycloak": "healthy" if keycloak_healthy else "unhealthy",
    }
    if not db_healthy or not redis_healthy or not keycloak_healthy:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "database": "healthy" if db_healthy else "unhealthy",
                "redis": "healthy" if redis_healthy else "unhealthy",
                "keycloak": "healthy" if keycloak_healthy else "unhealthy",
            },
        )
    return {"status": "ready"} | details
