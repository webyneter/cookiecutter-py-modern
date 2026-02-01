"""Logging configuration using structlog."""

import logging
import os
from typing import cast

import structlog


def _is_debug_enabled() -> bool:
    """Check if debug mode is enabled via environment variable.

    Returns:
        True if DEBUG environment variable is set to a truthy value.
    """
    return os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")


def get_logger() -> structlog.typing.FilteringBoundLogger:
    """Configure and return a structured logger.

    The log level is determined by the DEBUG environment variable:
    - DEBUG=true/1/yes: DEBUG level
    - Otherwise: INFO level

    Returns:
        A configured structlog bound logger with console rendering.
    """
    log_level = logging.DEBUG if _is_debug_enabled() else logging.INFO

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.CallsiteParameterAdder(
                parameters={
                    structlog.processors.CallsiteParameter.PATHNAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                },
            ),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return cast(structlog.typing.FilteringBoundLogger, structlog.get_logger())
