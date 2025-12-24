#!/usr/bin/env python3
"""Post-generation hook to clean up conditional files and directories."""

import shutil
from pathlib import Path

PROJECT_DIR = Path.cwd()
SRC_DIR = PROJECT_DIR / "src"
TESTS_DIR = PROJECT_DIR / "tests"

def to_bool(value: str) -> bool:
    """Convert string to boolean, handling various formats."""
    return value.lower() in ("true", "1", "yes")


PACKAGE_NAME = "{{ cookiecutter.package_name }}"
DOCKER = to_bool("{{ cookiecutter.docker }}")
SENTRY = to_bool("{{ cookiecutter.sentry }}")
CLI = to_bool("{{ cookiecutter.cli }}")
WEB = to_bool("{{ cookiecutter.web }}")
API = to_bool("{{ cookiecutter.api }}")
API_AUTH = to_bool("{{ cookiecutter.api_auth }}")
API_VERSIONING = to_bool("{{ cookiecutter.api_versioning }}")


def remove_path(path: Path) -> None:
    """Remove a file or directory if it exists."""
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def regenerate_root_conftest() -> None:
    """Regenerate the root tests/conftest.py after API conftest leaked and overwrote it."""
    conftest_content = '''"""Pytest configuration and fixtures."""

import os

import pytest

# Set environment variables before any imports
os.environ.setdefault("ENVIRONMENT", "test")
'''

    if SENTRY:
        conftest_content += 'os.environ.setdefault("SENTRY_DSN", "")\n'

    if WEB:
        conftest_content += f'''os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{PACKAGE_NAME}_web.settings")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("DATABASE_URL", "sqlite:///test.sqlite3")
'''

    conftest_content += '''

@pytest.fixture(autouse=True)
def set_test_env_vars() -> None:
    """Set required environment variables for testing."""
    os.environ.setdefault("ENVIRONMENT", "test")
'''

    if SENTRY:
        conftest_content += '    os.environ.setdefault("SENTRY_DSN", "")\n'

    if WEB:
        conftest_content += f'    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{PACKAGE_NAME}_web.settings")\n'

    conftest_path = TESTS_DIR / "conftest.py"
    conftest_path.write_text(conftest_content)


def cleanup_leaked_api_files() -> None:
    """Remove API files that leaked to src/ when api=false.

    When cookiecutter conditional directory evaluates to empty string,
    files end up in the parent directory instead of being skipped.
    """
    api_files = [
        "__init__.py",
        "py.typed",
        "config.py",
        "dependencies.py",
        "exceptions.py",
        "main.py",
        "pagination.py",
        "lambda_handler.py",
        "auth.py",
        "schemas.py",
        "jwt.py",
    ]
    api_dirs = [
        "auth",
        "middleware",
        "routers",
        "schemas",
        "v1",
    ]

    for filename in api_files:
        remove_path(SRC_DIR / filename)

    for dirname in api_dirs:
        remove_path(SRC_DIR / dirname)

    # Also clean up API test files that leaked
    api_test_files = [
        "test_config.py",
        "test_health.py",
        "test_auth.py",
        "test_lambda_handler.py",
    ]

    # The API conftest.py leaks to tests/conftest.py, overwriting the root conftest
    # Remove it and regenerate a clean root conftest
    leaked_conftest = TESTS_DIR / "conftest.py"
    if leaked_conftest.exists():
        remove_path(leaked_conftest)
        regenerate_root_conftest()
    api_test_dirs = [
        "auth",
        "routers",
        "v1",
    ]

    for filename in api_test_files:
        remove_path(TESTS_DIR / filename)

    for dirname in api_test_dirs:
        remove_path(TESTS_DIR / dirname)


def cleanup_leaked_cli_files() -> None:
    """Remove CLI files that leaked when cli=false."""
    # Remove leaked CLI source files
    remove_path(SRC_DIR / "__main__.py")

    # Remove leaked CLI test file
    remove_path(TESTS_DIR / "test_cli.py")


def cleanup_leaked_web_files() -> None:
    """Remove web files that leaked when web=false."""
    web_files = [
        "__init__.py",
        "py.typed",
        "asgi.py",
        "settings.py",
        "urls.py",
        "wsgi.py",
    ]
    web_dirs = [
        "templates",
    ]

    for filename in web_files:
        remove_path(SRC_DIR / filename)

    for dirname in web_dirs:
        remove_path(SRC_DIR / dirname)

    # Remove leaked web test file
    remove_path(TESTS_DIR / "test_django.py")


def cleanup_leaked_auth_files(package_name: str) -> None:
    """Remove auth files that leaked to _api package when api_auth=false."""
    api_package = SRC_DIR / f"{package_name}_api"
    if not api_package.exists():
        return

    auth_files = [
        "__init__.py",  # From auth package
        "dependencies.py",
        "jwt.py",
        "schemas.py",
    ]

    # Remove leaked files in API package root
    for filename in auth_files:
        leaked_file = api_package / filename
        # Don't remove __init__.py since API package needs it
        if filename != "__init__.py":
            # Check if the file exists at package root (leaked) vs in auth/ subdir
            if leaked_file.exists() and not (api_package / "auth" / filename).exists():
                remove_path(leaked_file)

    # Remove auth.py router if it leaked to routers/
    remove_path(api_package / "routers" / "auth.py")


def cleanup_leaked_sentry_files() -> None:
    """Remove sentry.py that leaked when sentry=false."""
    # sentry.py is inside core package with conditional filename
    # When sentry=false, it might leak as empty file
    remove_path(SRC_DIR / "sentry.py")


def main() -> None:
    """Clean up files and directories based on cookiecutter options."""
    # Clean up leaked files from conditional directories
    if not API:
        cleanup_leaked_api_files()

    if not CLI:
        cleanup_leaked_cli_files()

    if not WEB:
        cleanup_leaked_web_files()

    if not SENTRY:
        cleanup_leaked_sentry_files()

    # Clean up auth files if api=true but api_auth=false
    if API and not API_AUTH:
        cleanup_leaked_auth_files(PACKAGE_NAME)

    # Clean up Docker files
    docker_dir = PROJECT_DIR / "docker"
    docker_compose = PROJECT_DIR / "docker-compose.yaml"
    dockerignore = PROJECT_DIR / ".dockerignore"

    if not DOCKER:
        remove_path(docker_dir)
        remove_path(docker_compose)
        remove_path(dockerignore)
    else:
        if not WEB:
            remove_path(docker_dir / "web")

        if not API:
            remove_path(docker_dir / "api")


if __name__ == "__main__":
    main()
