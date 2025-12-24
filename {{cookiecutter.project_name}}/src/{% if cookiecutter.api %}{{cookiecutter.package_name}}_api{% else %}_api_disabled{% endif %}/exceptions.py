"""Global exception handlers."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError

from {{cookiecutter.package_name}}.logging import get_logger

logger = get_logger()


class APIError(Exception):
    """Base API exception."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize API error.

        Args:
            message: Error message.
            status_code: HTTP status code.
            details: Additional error details.
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(APIError):
    """Resource not found error."""

    def __init__(self, message: str = "Resource not found", details: dict[str, Any] | None = None) -> None:
        """Initialize not found error.

        Args:
            message: Error message.
            details: Additional error details.
        """
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)


class BadRequestError(APIError):
    """Bad request error."""

    def __init__(self, message: str = "Bad request", details: dict[str, Any] | None = None) -> None:
        """Initialize bad request error.

        Args:
            message: Error message.
            details: Additional error details.
        """
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)
{%- if cookiecutter.api_auth %}


class UnauthorizedError(APIError):
    """Unauthorized error."""

    def __init__(self, message: str = "Unauthorized", details: dict[str, Any] | None = None) -> None:
        """Initialize unauthorized error.

        Args:
            message: Error message.
            details: Additional error details.
        """
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, details)


class ForbiddenError(APIError):
    """Forbidden error."""

    def __init__(self, message: str = "Forbidden", details: dict[str, Any] | None = None) -> None:
        """Initialize forbidden error.

        Args:
            message: Error message.
            details: Additional error details.
        """
        super().__init__(message, status.HTTP_403_FORBIDDEN, details)
{%- endif %}


def configure_exception_handlers(app: FastAPI) -> None:
    """Configure global exception handlers for the application.

    Args:
        app: The FastAPI application instance.
    """

    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> ORJSONResponse:
        """Handle API errors."""
        logger.warning(
            "API error",
            path=request.url.path,
            status_code=exc.status_code,
            message=exc.message,
        )
        return ORJSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message, "details": exc.details},
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError) -> ORJSONResponse:
        """Handle Pydantic validation errors."""
        logger.warning("Validation error", path=request.url.path, errors=exc.errors())
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "Validation error", "details": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
        """Handle unexpected exceptions."""
        logger.exception("Unhandled exception", path=request.url.path)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error"},
        )
