"""Authentication module."""

from {{cookiecutter.package_name}}_api.auth.dependencies import CurrentUserDep, get_current_user
from {{cookiecutter.package_name}}_api.auth.jwt import create_access_token, verify_token

__all__ = [
    "CurrentUserDep",
    "create_access_token",
    "get_current_user",
    "verify_token",
]
