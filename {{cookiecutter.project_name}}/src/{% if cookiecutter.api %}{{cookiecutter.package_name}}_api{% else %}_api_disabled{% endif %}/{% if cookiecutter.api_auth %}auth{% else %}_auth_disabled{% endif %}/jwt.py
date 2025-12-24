"""JWT token utilities."""

from datetime import UTC, datetime, timedelta
from typing import Any, cast

from jose import JWTError, jwt

from {{cookiecutter.package_name}}_api.auth.schemas import TokenData
from {{cookiecutter.package_name}}_api.config import settings
from {{cookiecutter.package_name}}_api.exceptions import UnauthorizedError


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token.

    Args:
        data: Data to encode in the token.
        expires_delta: Optional custom expiration time.

    Returns:
        Encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return cast(
        str,
        jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        ),
    )


def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token.

    Args:
        token: JWT token to verify.

    Returns:
        Decoded token data.

    Raises:
        UnauthorizedError: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        subject: str | None = payload.get("sub")
        if subject is None:
            raise UnauthorizedError("Invalid token: missing subject")
        return TokenData(sub=subject)
    except JWTError as e:
        raise UnauthorizedError(f"Invalid token: {e}") from e
