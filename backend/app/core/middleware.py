import logging
import time
import uuid

from fastapi import Request

from app.core.request_context import request_id_context

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    # Generate a unique request ID for this request
    request_id = str(uuid.uuid4())[:8]
    request_id_context.set(request_id)

    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start

    # Expose the request ID in the response headers
    response.headers["X-Request-ID"] = request_id

    logger.info(
        "%s %s -> %s (%.3fs)",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response