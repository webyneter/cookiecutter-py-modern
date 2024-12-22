# Documentation

Welcome to the {{ cookiecutter.friendly_name }} documentation.

## Dependency Guides

- [Core Dependencies](core-dependencies-overview.md) - Essential libraries (structlog, Sentry, Pydantic, HTTPX, orjson, Rich)
{%- if cookiecutter.cli %}
- [CLI Dependencies](cli-dependencies-overview.md) - Command-line interface tools (Typer)
{%- endif %}
{%- if cookiecutter.web %}
- [Web Dependencies](web-dependencies-overview.md) - Django and related packages
{%- endif %}
{%- if cookiecutter.api %}
- [API Dependencies](api-dependencies-overview.md) - FastAPI and related packages
{%- endif %}
- [Development Dependencies](dev-dependencies-overview.md) - Testing and code quality tools (pytest, Ruff, mypy, Hypothesis)

## Quick Links

- [README](../README.md) - Project overview, setup instructions, and usage
- [Contributing](../CONTRIBUTING.md) - Guidelines for contributing to this project
- [License](../LICENSE) - Project license information
