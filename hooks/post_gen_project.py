#!/usr/bin/env python3
"""Post-generation hook to clean up conditional files and directories."""

import os
import shutil
import stat
from pathlib import Path

PROJECT_DIR = Path.cwd()
SRC_DIR = PROJECT_DIR / "src"
TESTS_DIR = PROJECT_DIR / "tests"
ENVS_DIR = PROJECT_DIR / "envs"
DOCKER_DIR = PROJECT_DIR / "docker"


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
API_LAMBDA = to_bool("{{ cookiecutter.api_lambda }}")
API_VERSIONING = to_bool("{{ cookiecutter.api_versioning }}")
GITHUB_ACTIONS = to_bool("{{ cookiecutter.github_actions }}")


def remove_path(path: Path) -> None:
    """Remove a file or directory if it exists."""
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def make_executable(path: Path) -> None:
    """Make a file executable."""
    if path.is_file():
        current_mode = path.stat().st_mode
        path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def regenerate_root_conftest() -> None:
    """Regenerate the root tests/conftest.py using dotenv pattern."""
    base_content_without_os = '''"""Pytest configuration and fixtures."""

from pathlib import Path

from dotenv import load_dotenv

# Load environment files before any other imports
# This ensures env vars are available for module-level configuration
_envs_dir = Path(__file__).parent.parent / "envs"

# Load base environment (common settings)
if (_base := _envs_dir / "base.env").exists():
    load_dotenv(_base)

# Load test environment (overrides base settings)
if (_test := _envs_dir / "test.env").exists():
    load_dotenv(_test, override=True)
'''

    base_content_with_os = '''"""Pytest configuration and fixtures."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment files before any other imports
# This ensures env vars are available for module-level configuration
_envs_dir = Path(__file__).parent.parent / "envs"

# Load base environment (common settings)
if (_base := _envs_dir / "base.env").exists():
    load_dotenv(_base)

# Load test environment (overrides base settings)
if (_test := _envs_dir / "test.env").exists():
    load_dotenv(_test, override=True)
'''

    django_setup = f'''
# Configure Django before pytest-django tries to set up the test database
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{PACKAGE_NAME}_web.settings")

import django  # noqa: E402

django.setup()
'''

    if WEB:
        conftest_content = base_content_with_os + django_setup
    else:
        conftest_content = base_content_without_os

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
        "dependencies",
        "middleware",
        "routers",
        "schemas",
        "services",
        "v1",
    ]

    for filename in api_files:
        remove_path(SRC_DIR / filename)

    for dirname in api_dirs:
        remove_path(SRC_DIR / dirname)

    # Also clean up API test files that leaked to tests/unit/
    unit_dir = TESTS_DIR / "unit"
    api_test_files = [
        "test_config.py",
        "test_health.py",
        "test_auth.py",
        "test_lambda_handler.py",
        "conftest.py",
    ]
    api_test_dirs = [
        "auth",
        "routers",
        "v1",
    ]

    for filename in api_test_files:
        remove_path(unit_dir / filename)

    for dirname in api_test_dirs:
        remove_path(unit_dir / dirname)


def cleanup_leaked_cli_files() -> None:
    """Remove CLI files that leaked when cli=false."""
    # Remove leaked CLI source files
    remove_path(SRC_DIR / "__main__.py")

    # Remove leaked CLI test file (now in tests/unit/)
    remove_path(TESTS_DIR / "unit" / "test_cli.py")


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

    # Remove leaked web test file (now in tests/unit/)
    remove_path(TESTS_DIR / "unit" / "test_django.py")


def regenerate_api_init(package_name: str) -> None:
    """Regenerate API package __init__.py after auth __init__ leaked and overwrote it."""
    api_package = SRC_DIR / f"{package_name}_api"
    init_content = f'''"""API package for {package_name}."""

from {package_name}_api.main import app

__all__ = ["app"]
'''
    (api_package / "__init__.py").write_text(init_content)


def regenerate_routers_init(package_name: str) -> None:
    """Regenerate routers __init__.py after v1 __init__ leaked and overwrote it."""
    api_package = SRC_DIR / f"{package_name}_api"
    routers_dir = api_package / "routers"
    init_content = '''"""API routers package."""
'''
    (routers_dir / "__init__.py").write_text(init_content)


def cleanup_leaked_auth_files(package_name: str) -> None:
    """Remove auth files that leaked to _api package when api_auth=false."""
    api_package = SRC_DIR / f"{package_name}_api"
    if not api_package.exists():
        return

    auth_files = [
        "jwt.py",
        "schemas.py",
    ]

    # Remove leaked files in API package root
    for filename in auth_files:
        leaked_file = api_package / filename
        if leaked_file.exists():
            remove_path(leaked_file)

    # The auth/__init__.py leaks to api package root, overwriting it
    # Regenerate the clean API __init__.py
    regenerate_api_init(package_name)

    # Remove auth.py router if it leaked to routers/
    remove_path(api_package / "routers" / "auth.py")

    # Remove leaked auth test files (now in tests/unit/)
    api_test_dir = TESTS_DIR / "unit" / f"test_{package_name}_api"
    if api_test_dir.exists():
        remove_path(api_test_dir / "test_auth.py")


def cleanup_leaked_versioning_files(package_name: str) -> None:
    """Remove v1 files that leaked to routers/ when api_versioning=false."""
    api_package = SRC_DIR / f"{package_name}_api"
    if not api_package.exists():
        return

    routers_dir = api_package / "routers"
    if not routers_dir.exists():
        return

    # Remove leaked v1 files from routers/
    v1_files = ["example.py"]
    for filename in v1_files:
        remove_path(routers_dir / filename)

    # The v1/__init__.py leaks to routers/, overwriting it
    # Regenerate the clean routers __init__.py
    regenerate_routers_init(package_name)


def cleanup_leaked_sentry_files() -> None:
    """Remove sentry.py that leaked when sentry=false."""
    # sentry.py is inside core package with conditional filename
    # When sentry=false, it might leak as empty file
    remove_path(SRC_DIR / "sentry.py")


def cleanup_disabled_placeholder_dirs() -> None:
    """Remove placeholder directories created when features are disabled.

    Cookiecutter doesn't support truly optional directories, so we use
    placeholder names like '_api_disabled' that are always created,
    then cleaned up here based on the actual feature flags.
    """
    # Source package placeholders
    if not API:
        remove_path(SRC_DIR / "_api_disabled")

    if not CLI:
        remove_path(SRC_DIR / "_cli_disabled")

    if not WEB:
        remove_path(SRC_DIR / "_web_disabled")

    # Test package placeholders (now under tests/unit/)
    unit_dir = TESTS_DIR / "unit"
    if not API:
        remove_path(unit_dir / "_test_api_disabled")

    if not CLI:
        remove_path(unit_dir / "_test_cli_disabled")

    if not WEB:
        remove_path(unit_dir / "_test_web_disabled")

    # Lambda-related placeholders
    if not API_LAMBDA:
        remove_path(ENVS_DIR / "_docker_compose_disabled")
        remove_path(DOCKER_DIR / "_lambda_api_disabled")
        remove_path(TESTS_DIR / "_common_disabled")
        remove_path(TESTS_DIR / "_integration_disabled")
        remove_path(TESTS_DIR / "_smoke_disabled")

    # GitHub Actions placeholder
    if not GITHUB_ACTIONS:
        remove_path(PROJECT_DIR / "_.github_disabled")

    # Nested placeholders inside API package (only relevant when API is enabled)
    if API:
        api_package = SRC_DIR / f"{PACKAGE_NAME}_api"
        if not API_AUTH:
            remove_path(api_package / "_auth_disabled")
        if not API_VERSIONING:
            remove_path(api_package / "routers" / "_v1_disabled")


def cleanup_docker_files() -> None:
    """Clean up Docker-related files based on options."""
    docker_compose = PROJECT_DIR / "docker-compose.yaml"
    dockerignore = PROJECT_DIR / ".dockerignore"

    if not DOCKER:
        remove_path(DOCKER_DIR)
        remove_path(docker_compose)
        remove_path(dockerignore)
    else:
        if not WEB:
            remove_path(DOCKER_DIR / "web")

        # Standard API Dockerfile is only used when api=true and api_lambda=false
        if not API or API_LAMBDA:
            remove_path(DOCKER_DIR / "api")

        # Lambda API Dockerfile is only used when api_lambda=true
        if not API_LAMBDA:
            remove_path(DOCKER_DIR / "lambda-api")


def make_scripts_executable() -> None:
    """Make script files executable."""
    # Make test script executable
    test_script = PROJECT_DIR / "test"
    make_executable(test_script)


def main() -> None:
    """Clean up files and directories based on cookiecutter options."""
    # Clean up placeholder directories for disabled features
    cleanup_disabled_placeholder_dirs()

    # Regenerate conftest.py to ensure correct Django setup based on WEB option
    regenerate_root_conftest()

    # Clean up leaked files from conditional directories (legacy fallback)
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

    # Clean up versioning files if api=true but api_versioning=false
    if API and not API_VERSIONING:
        cleanup_leaked_versioning_files(PACKAGE_NAME)

    # Clean up Docker files
    cleanup_docker_files()

    # Make scripts executable
    make_scripts_executable()


if __name__ == "__main__":
    main()
