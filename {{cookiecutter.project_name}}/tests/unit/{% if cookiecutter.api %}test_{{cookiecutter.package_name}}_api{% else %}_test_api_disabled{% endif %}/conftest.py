"""API test fixtures."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from {{cookiecutter.package_name}}_api.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client
