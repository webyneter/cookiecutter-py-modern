"""Authentication dependencies."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from {{cookiecutter.package_name}}_api.auth.jwt import verify_token
from {{cookiecutter.package_name}}_api.auth.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    """Get current authenticated user from JWT token.

    Args:
        token: JWT token from Authorization header.

    Returns:
        Token data containing user information.

    Raises:
        UnauthorizedError: If token is invalid.
    """
    return verify_token(token)


CurrentUserDep = Annotated[TokenData, Depends(get_current_user)]
