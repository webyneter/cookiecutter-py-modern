"""Logging configuration using structlog."""

import logging
from typing import cast

import structlog


def get_logger() -> structlog.typing.FilteringBoundLogger:
    """Configure and return a structured logger.

    Returns:
        A configured structlog bound logger with console rendering.
    """
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
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return cast(structlog.typing.FilteringBoundLogger, structlog.get_logger())
