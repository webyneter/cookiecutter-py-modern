# Cookiecutter Python Modern

[![CI](https://github.com/webyneter/cookiecutter-py-modern/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/webyneter/cookiecutter-py-modern/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type%20checker-mypy-blue.svg)](https://mypy-lang.org/)
[![Safety](https://img.shields.io/badge/security-Safety-green.svg)](https://safetycli.com/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![License](https://img.shields.io/badge/license-MIT%20%7C%20Apache--2.0%20%7C%20GPL--3.0-blue.svg)](LICENSE)
[![Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg)](https://github.com/cookiecutter/cookiecutter)

A modern, batteries-included Cookiecutter template for Python and API projects.

Generate production-ready scaffolding with optional support for CLI applications, web backends, REST APIs, serverless
deployments, and more.

## Features

- **Python 3.12+** — Modern Python with full type hints and the latest language features
- **[FastAPI](https://fastapi.tiangolo.com/)** — High-performance async API framework with automatic OpenAPI docs,
  middleware, health checks, JWT authentication, and URL-prefix versioning
- **[Django](https://www.djangoproject.com/)** — Battle-tested web framework with security hardening (CSP, CORS, Axes)
  out of the box
- **[Typer](https://typer.tiangolo.com/)** — Build elegant CLIs with automatic help generation and shell completion
- **[Mangum](https://mangum.io/) + [AWS Lambda Powertools](https://docs.powertools.aws.dev/lambda/python/latest/)** —
  Deploy your FastAPI to AWS Lambda with structured logging, X-Ray tracing, and CloudWatch metrics
- **Async-First** — Full async support with uvloop and pytest-asyncio for blazing-fast concurrent workloads
- **Docker & Docker Compose** — Production-ready multi-stage builds for containerized deployments
- **[Sentry](https://sentry.io/)** — Error tracking and performance monitoring from day one
- **[uv](https://docs.astral.sh/uv/) + [Hatch](https://hatch.pypa.io/)** — Lightning-fast dependency management and
  modern build tooling
- **[Ruff](https://docs.astral.sh/ruff/)** — Linting and formatting at 10-100x the speed of traditional tools
- **[mypy](https://mypy-lang.org/)** — Strict type checking to catch bugs before they reach production
- **[pytest](https://docs.pytest.org/)** — Comprehensive testing with coverage, hypothesis, and parallel execution
- **[Structlog](https://www.structlog.org/)** — Structured logging that makes debugging a breeze
- **[pre-commit](https://pre-commit.com/)** — Automated hooks to enforce code quality on every commit
- **[Safety](https://safetycli.com/)** — Continuous vulnerability scanning for your dependencies
- **CI-Tested** — [11 template variants](variants.json) validated on every push for linting, type safety, and tests so you can rest assured your generated project works out of the box (aside from unknown unknowns, of course 😉)

## Quick Start

### Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html)

### Generate a Project

```shell
# From GitHub
cookiecutter gh:webyneter/cookiecutter-py-modern

# From local clone
cookiecutter /path/to/cookiecutter-py-modern
```

### Working with Generated Projects

```shell
cd my-project

# Install dependencies
uv sync

# Run linting
uv run ruff check .
uv run ruff format .

# Run type checking
uv run mypy .

# Run tests
uv run pytest

# Run CLI (if enabled)
uv run my-project --help

# Run Django server (if web enabled)
uv run python -m my_project_web runserver

# Run FastAPI server (if api enabled)
uv run uvicorn my_project_api.main:app --reload
```

## Template Options

| Option                          | Description                                            |
|---------------------------------|--------------------------------------------------------|
| `project_name`                  | Project name (used for package directory)              |
| `package_name`                  | Python package name (auto-generated from project_name) |
| `author`                        | Author name                                            |
| `email`                         | Author email                                           |
| `license`                       | License choice: MIT, Apache-2.0, or GPL-3.0            |
| `sentry`                        | Include Sentry SDK for error tracking                  |
| `async`                         | Enable async support (uvloop, pytest-asyncio)          |
| `cli`                           | Include Typer CLI package                              |
| `web`                           | Include Django web application                         |
| `api`                           | Include FastAPI application                            |
| `api_auth`                      | Add JWT authentication (requires api)                  |
| `api_lambda`                    | AWS Lambda support with Mangum (requires api)          |
| `api_lambda_powertools_tracing` | X-Ray tracing (requires api_lambda)                    |
| `api_lambda_powertools_metrics` | CloudWatch metrics (requires api_lambda)               |
| `api_pagination`                | Add fastapi-pagination (requires api)                  |
| `api_versioning`                | URL-prefix versioning /v1/ (requires api)              |
| `docker`                        | Include Dockerfile and docker configs                  |
| `pycharm`                       | Include PyCharm/IntelliJ configuration                 |

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** for your feature or fix
4. **Make your changes** and test them thoroughly
5. **Submit a pull request** with a clear description

### Development Setup

See [docs/development.md](docs/development.md) for local setup instructions and testing guidelines.

## Disclaimer

This project is maintained on a best-effort basis. No guarantees of any sort are made regarding functionality,
stability, or continued support. The community is welcome to contribute via issues and pull requests.

## License

This template is available under multiple license options. When generating a project, you can choose between:

- [MIT License](https://opensource.org/licenses/MIT)
- [Apache License 2.0](https://opensource.org/licenses/Apache-2.0)
- [GNU General Public License v3.0](https://opensource.org/licenses/GPL-3.0)
