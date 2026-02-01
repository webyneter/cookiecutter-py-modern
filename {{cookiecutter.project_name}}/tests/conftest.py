"""Pytest configuration and fixtures."""

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
{%- if cookiecutter.web %}

# Configure Django before pytest-django tries to set up the test database
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "{{ cookiecutter.package_name }}_web.settings"
)

import django  # noqa: E402

django.setup()
{%- endif %}
