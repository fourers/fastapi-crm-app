import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)


async def access_log(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start
    user_id = getattr(request.state, "user_id", "")

    logger.info(
        "%s %s %s user_id=%s %.3fs",
        request.method,
        request.url.path,
        response.status_code,
        user_id,
        duration,
    )

    return response
