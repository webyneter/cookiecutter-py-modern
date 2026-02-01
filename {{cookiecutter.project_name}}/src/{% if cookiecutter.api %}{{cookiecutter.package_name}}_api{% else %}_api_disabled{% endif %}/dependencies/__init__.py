"""Dependency injection utilities."""

from typing import Annotated

import structlog
from fastapi import Depends

from {{cookiecutter.package_name}}.logging import get_logger
from {{cookiecutter.package_name}}_api.config import Settings, get_settings


def get_request_logger() -> structlog.typing.FilteringBoundLogger:
    """Get a logger instance for request handling.

    Returns:
        A configured structlog bound logger.
    """
    return get_logger()


LoggerDep = Annotated[structlog.typing.FilteringBoundLogger, Depends(get_request_logger)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
