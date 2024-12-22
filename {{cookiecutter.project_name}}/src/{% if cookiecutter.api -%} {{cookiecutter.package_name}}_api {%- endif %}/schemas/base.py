"""Base schema models."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class ErrorResponse(BaseSchema):
    """Standard error response."""

    error: str
    details: dict[str, Any] | None = None


class MessageResponse(BaseSchema):
    """Standard message response."""

    message: str
