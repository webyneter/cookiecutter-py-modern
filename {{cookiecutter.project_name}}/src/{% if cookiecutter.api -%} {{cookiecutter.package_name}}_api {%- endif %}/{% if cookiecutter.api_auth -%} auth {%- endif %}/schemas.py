"""Authentication schemas."""

from {{cookiecutter.package_name}}_api.schemas.base import BaseSchema


class Token(BaseSchema):
    """OAuth2 token response."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105


class TokenData(BaseSchema):
    """Data extracted from JWT token."""

    sub: str
