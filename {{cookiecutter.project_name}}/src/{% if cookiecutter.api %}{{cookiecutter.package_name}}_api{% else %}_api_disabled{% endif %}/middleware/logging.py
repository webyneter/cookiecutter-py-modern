"""Logging middleware for request/response logging."""

import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from {{cookiecutter.package_name}}.logging import get_logger

logger = get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs request and response information."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process the request and log request/response details.

        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.

        Returns:
            The response from the route handler.
        """
        request_id = getattr(request.state, "request_id", "unknown")
        start_time = time.perf_counter()

        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query=str(request.query_params),
        )

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        logger.info(
            "Request completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(process_time * 1000, 2),
        )

        return response
