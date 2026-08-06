from functools import cache

from redis import Redis

from app.config.redis import settings


@cache
def get_client():
    return Redis(
        host=settings.host,
        port=settings.port,
        password=settings.password,
    )
