"""Health check schemas."""

from {{cookiecutter.package_name}}_api.schemas.base import BaseSchema


class HealthResponse(BaseSchema):
    """Health check response."""

    status: str
    version: str
