"""HTTP request and response logging middleware.

Logs request arrival and request completion stats, including method, path, client
host, status code, and latency in milliseconds.
"""

import logging
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP request metadata and durations."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Log incoming request data and track the processing time."""
        start_time = time.perf_counter()
        client_host = request.client.host if request.client else "unknown"

        logger.info(
            "Incoming request - Method: %s - Path: %s - Client: %s",
            request.method,
            request.url.path,
            client_host,
        )

        try:
            response = await call_next(request)
            duration = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Request processed - Method: %s - Path: %s - Status: %d - Duration: %.2fms",
                request.method,
                request.url.path,
                response.status_code,
                duration,
            )
            return response
        except Exception as exc:
            duration = (time.perf_counter() - start_time) * 1000
            logger.error(
                "Request error - Method: %s - Path: %s - Duration: %.2fms - Error: %s",
                request.method,
                request.url.path,
                duration,
                str(exc),
            )
            raise
