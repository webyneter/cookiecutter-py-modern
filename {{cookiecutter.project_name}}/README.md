# {{ cookiecutter.friendly_name }}

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![License](https://img.shields.io/pypi/l/{{cookiecutter.project_name}})][license]

## Features

[//]: # (TODO: )

## Prerequisites

* [`git`](https://git-scm.com/downloads)
* [`pipx`](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
* [`uv`](https://docs.astral.sh/uv/getting-started/installation/)

[//]: # (TODO: Docker, if docker: true)

## Initialization

Create a virtualenv, install dependencies, generate a dependency lock file--all via a single `uv` command:

```shell
uv sync
```

Next up, install [`pre-commit`](https://pre-commit.com/) hooks:

```shell
pipx install pre-commit

pre-commit install
```

Initialize `git` repository:

```shell
git init
git remote add origin <your remote url>
```

Stage, commit, and push: 

```shell
git add .
git commit -m "Scaffold the project using webyneter/cookiecutter-py-modern"
git push --set-upstream origin main
```

## Usage
{%- if cookiecutter.cli %}

### CLI

```shell
uv run {{cookiecutter.project_name}} --help
```
{%- endif %}
{%- if cookiecutter.web %}

### Running the web server

Development:

```shell
{%- if cookiecutter.async %}
uv run uvicorn {{cookiecutter.package_name}}_web.asgi:application --reload
{%- else %}
uv run gunicorn {{cookiecutter.package_name}}_web.wsgi:application
{%- endif %}
```
{%- endif %}
{%- if cookiecutter.api %}

### Running the API server

Development:

```shell
uv run uvicorn {{cookiecutter.package_name}}_api.main:app --reload
```

Production:

```shell
uv run uvicorn {{cookiecutter.package_name}}_api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

API documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when running in debug mode.
{%- endif %}

### Testing

```shell
uv run pytest
```

### Linting and formatting

```shell
uv run ruff check .
uv run ruff format .
```

### Type checking

```shell
uv run mypy src/
```

## Documentation

For detailed documentation, see the [docs](docs/index.md) directory, which includes:

- [Core Dependencies](docs/core-dependencies-overview.md) - Essential libraries (structlog, {% if cookiecutter.sentry %}Sentry, {% endif %}Pydantic, HTTPX)
{%- if cookiecutter.cli %}
- [CLI Dependencies](docs/cli-dependencies-overview.md) - Command-line interface tools (Typer)
{%- endif %}
{%- if cookiecutter.web %}
- [Web Dependencies](docs/web-dependencies-overview.md) - Django and related packages
{%- endif %}
{%- if cookiecutter.api %}
- [API Dependencies](docs/api-dependencies-overview.md) - FastAPI and related packages
{%- endif %}
- [Development Dependencies](docs/dev-dependencies-overview.md) - Testing and code quality tools

## Contributing

Contributions are very welcome. To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [{{cookiecutter.license.replace("-", " ")}} license][license], _{{cookiecutter.friendly_name}}_ is free and open source software.

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

## Credits

This project was generated from [@webyneter]'s [Py-Modern Cookiecutter] template.

[@webyneter]: https://github.com/webyneter
[Py-Modern Cookiecutter]: https://github.com/webyneter/cookiecutter-py-modern
[file an issue]: https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/issues

<!-- github-only -->

[license]: https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/blob/main/LICENSE
[contributor guide]: https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/blob/main/CONTRIBUTING.md
[command-line reference]: https://{{cookiecutter.project_name}}.readthedocs.io/en/latest/usage.html
