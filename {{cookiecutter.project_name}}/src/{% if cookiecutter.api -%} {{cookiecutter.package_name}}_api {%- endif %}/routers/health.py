"""Health check endpoint."""

from fastapi import APIRouter

from {{cookiecutter.package_name}}_api.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check application health.

    Returns:
        Health status response.
    """
    return HealthResponse(status="healthy", version="{{cookiecutter.version}}")
