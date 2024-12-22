# Cookiecutter Python Modern

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

The `scripts/test-template.sh` script generates projects from the template and validates them.

### Generate a single variant

```shell
# Generate with defaults (async + cli)
./scripts/test-template.bash

# Generate async web project and install dependencies
./scripts/test-template.bash --web true --async true --install

# Clean output, generate, install deps, and run tests
./scripts/test-template.bash --clean --web true --test

# Custom project name and output directory
./scripts/test-template.bash --name my-test --output /tmp/test-output --install
```

### Test all variant combinations

```shell
# Generate and install deps for all 8 variant combinations
./scripts/test-template.bash --all-variants
```

This tests:
- `minimal` - no async, cli, or web
- `async-only` - async without cli or web
- `cli-only` - cli without async or web
- `web-only` - web without async or cli
- `async-cli` - async + cli
- `async-web` - async + web (uses uvicorn)
- `cli-web` - cli + web (uses gunicorn)
- `full` - all features enabled

### Script options

```
-h, --help          Show help message
-a, --async BOOL    Enable async support (default: true)
-c, --cli BOOL      Enable CLI support (default: true)
-w, --web BOOL      Enable web/Django support (default: false)
-d, --docker BOOL   Enable Docker support (default: true)
-p, --pycharm BOOL  Enable PyCharm support (default: false)
-o, --output DIR    Output directory (default: .test-output)
-n, --name NAME     Project name (default: test-project)
-i, --install       Install dependencies after generation
-t, --test          Run tests after generation (implies --install)
--clean             Remove output directory before generation
--all-variants      Generate and test all variant combinations
```

Generated projects are placed in `.test-output/` by default (gitignored).
