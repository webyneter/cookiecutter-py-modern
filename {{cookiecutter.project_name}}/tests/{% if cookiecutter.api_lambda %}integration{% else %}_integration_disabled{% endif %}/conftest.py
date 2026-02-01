"""Integration test fixtures."""

from collections.abc import Generator

import pytest
from common.http import ApiClient


@pytest.fixture
def lambda_client() -> Generator[ApiClient, None, None]:
    """Create an API client for Lambda integration tests.

    Uses Lambda invoke mode to call the Lambda function via Docker Compose's
    Runtime Interface Emulator.

    Yields:
        ApiClient configured for Lambda RIE.
    """
    with ApiClient(lambda_mode=True) as client:
        yield client
