# Development

## Guidelines

- Follow existing code style and conventions
- Add tests for new functionality
- Update documentation as needed
- Keep pull requests focused and atomic

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html)
- [pre-commit](https://pre-commit.com/#install)

## Development

```shell
pip install pre-commit cookiecutter
pre-commit install
```

## Testing the Template

The `scripts/` directory contains modular scripts for testing:

| Script                   | Purpose                                       |
|--------------------------|-----------------------------------------------|
| `test-template.bash`     | Orchestration script (calls all of the below) |
| `generate.bash`          | Generate a project from the template          |
| `install.bash`           | Install dependencies (`uv sync`)              |
| `lint.bash`              | Run linting and type checks                   |
| `test.bash`              | Run tests with pytest                         |
| `test-all-variants.bash` | Test all variant combinations                 |

```shell
# Test all variant combinations (default behavior)
./scripts/test-template.bash

# Clean output and test all variants
./scripts/test-template.bash --clean

# Generate and test a single project with specific options
./scripts/test-template.bash --all-variants false --web true --api true --test

# Custom project name and output directory
./scripts/test-template.bash --all-variants false --name my-test --output /tmp/test-output --install

# Use individual scripts directly
./scripts/test-all-variants.bash --clean
```

Variants tested (11 total):

| Variant          | Features         | Use Case                 |
|------------------|------------------|--------------------------|
| `minimal`        | sentry           | Base case validation     |
| `cli-only`       | cli              | Standalone CLI tools     |
| `web-only`       | web              | Django web apps          |
| `api-only`       | api              | Simple FastAPI services  |
| `api-auth`       | api, auth        | APIs with authentication |
| `api-lambda`     | api, lambda      | Serverless deployments   |
| `async-web`      | async, web       | Async Django apps        |
| `async-api-auth` | async, api, auth | Async FastAPI with auth  |
| `full-no-api`    | all except api   | Django + CLI apps        |
| `full-no-web`    | all except web   | FastAPI + CLI apps       |
| `full`           | everything       | Full integration test    |

### Script Options (test-template.bash)

```
-h, --help                   Show help message
-s, --sentry BOOL            Enable Sentry integration (default: true)
-a, --async BOOL             Enable async support (default: true)
-c, --cli BOOL               Enable CLI support (default: true)
-w, --web BOOL               Enable web/Django support (default: true)
--api BOOL                   Enable FastAPI support (default: true)
--api-auth BOOL              Enable API auth support (default: true)
--api-lambda BOOL            Enable AWS Lambda hosting (default: true)
--api-lambda-tracing BOOL    Enable Powertools tracing (default: true)
--api-lambda-metrics BOOL    Enable Powertools metrics (default: true)
--api-pagination BOOL        Enable pagination utilities (default: true)
--api-versioning BOOL        Enable API versioning (default: true)
-d, --docker BOOL            Enable Docker support (default: true)
-p, --pycharm BOOL           Enable PyCharm support (default: true)
-o, --output DIR             Output directory (default: .test-output)
-n, --name NAME              Project name (default: test-project)
-i, --install                Install dependencies after generation
-t, --test                   Run tests after generation (implies --install)
-l, --lint                   Run linting after generation (implies --install)
--all-variants BOOL          Generate and test all variant combinations (default: true)
--clean                      Remove output directory before generation
```

Generated projects are placed in `.test-output/` by default (gitignored).
