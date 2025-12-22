"""Pytest configuration and fixtures."""

import os

import pytest

# Set environment variables before any imports
os.environ.setdefault("ENVIRONMENT", "test")
{%- if cookiecutter.sentry %}
os.environ.setdefault("SENTRY_DSN", "")
{%- endif %}
{%- if cookiecutter.web %}
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.package_name}}_web.settings")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("DATABASE_URL", "sqlite:///test.sqlite3")
{%- endif %}
{%- if cookiecutter.api %}
os.environ.setdefault("DEBUG", "True")
{%- if cookiecutter.api_auth %}
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-not-for-production")
{%- endif %}
{%- endif %}


@pytest.fixture(autouse=True)
def set_test_env_vars() -> None:
    """Set required environment variables for testing."""
    os.environ.setdefault("ENVIRONMENT", "test")
    {%- if cookiecutter.sentry %}
    os.environ.setdefault("SENTRY_DSN", "")
    {%- endif %}
    {%- if cookiecutter.web %}
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.package_name}}_web.settings")
    {%- endif %}
