"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
{%- if cookiecutter.api_pagination %}
from fastapi_pagination import add_pagination
{%- endif %}

from {{cookiecutter.package_name}}.logging import get_logger
from {{cookiecutter.package_name}}.sentry import init_sentry
from {{cookiecutter.package_name}}_api.config import settings
from {{cookiecutter.package_name}}_api.exceptions import configure_exception_handlers
from {{cookiecutter.package_name}}_api.middleware.logging import LoggingMiddleware
from {{cookiecutter.package_name}}_api.middleware.request_id import RequestIdMiddleware
{%- if cookiecutter.api_auth %}
from {{cookiecutter.package_name}}_api.routers import auth, health
{%- else %}
from {{cookiecutter.package_name}}_api.routers import health
{%- endif %}
{%- if cookiecutter.api_versioning %}
from {{cookiecutter.package_name}}_api.routers.v1 import router as v1_router
{%- endif %}

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager.

    Handles startup and shutdown events.

    Args:
        app: The FastAPI application instance.

    Yields:
        None during application lifetime.
    """
    logger.info("Starting {{cookiecutter.friendly_name}} API...")
    init_sentry()
    yield
    logger.info("Shutting down {{cookiecutter.friendly_name}} API...")


app = FastAPI(
    title="{{cookiecutter.friendly_name}}",
    description="{{cookiecutter.description}}",
    version="{{cookiecutter.version}}",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware (order matters: first added = outermost)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIdMiddleware)

# Configure exception handlers
configure_exception_handlers(app)

# Include routers
app.include_router(health.router, tags=["Health"])
{%- if cookiecutter.api_auth %}
app.include_router(auth.router)
{%- endif %}
{%- if cookiecutter.api_versioning %}
app.include_router(v1_router)
{%- endif %}
{%- if cookiecutter.api_pagination %}

# Enable pagination
add_pagination(app)
{%- endif %}
