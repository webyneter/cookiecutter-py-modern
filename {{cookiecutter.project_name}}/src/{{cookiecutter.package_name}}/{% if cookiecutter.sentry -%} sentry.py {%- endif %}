"""Sentry error tracking integration."""

import sentry_sdk
from environ import Env
from sentry_sdk.integrations.asyncio import AsyncioIntegration

from {{cookiecutter.package_name}}.logging import get_logger

env = Env()

ENVIRONMENT = env("ENVIRONMENT")
SENTRY_DSN = env("SENTRY_DSN")

logger = get_logger()


def init_sentry() -> None:
    """Initialize Sentry SDK for error tracking.

    Requires SENTRY_DSN and ENVIRONMENT environment variables to be set.
    If either is missing, initialization is skipped with a warning.
    """
    if not SENTRY_DSN:
        logger.warning("SENTRY_DSN is unset, skipping Sentry initialization.")
        return
    if not ENVIRONMENT:
        logger.warning("ENVIRONMENT is unset, skipping Sentry initialization.")
        return

    logger.debug(f"Initializing Sentry for {ENVIRONMENT} environment...")
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        integrations=[
            AsyncioIntegration(),
        ],
    )
    logger.debug(f"Initialized Sentry for {ENVIRONMENT} environment.")
