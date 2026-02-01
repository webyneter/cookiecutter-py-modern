"""Smoke test fixtures."""

import os
from collections.abc import Generator

import pytest
from common.http import ApiClient


def get_smoke_test_url() -> str:
    """Get the URL for smoke tests from environment.

    Returns:
        The Lambda function URL or API Gateway URL.

    Raises:
        pytest.skip: If SMOKE_TEST_URL is not set.
    """
    url = os.getenv("SMOKE_TEST_URL")
    if not url:
        pytest.skip("SMOKE_TEST_URL environment variable not set")
    return url


@pytest.fixture
def smoke_client() -> Generator[ApiClient, None, None]:
    """Create an API client for smoke tests against deployed Lambda.

    Uses direct HTTP mode to call the deployed Lambda function via its
    Function URL or API Gateway endpoint.

    Requires SMOKE_TEST_URL environment variable to be set.

    Yields:
        ApiClient configured for direct HTTP mode.
    """
    url = get_smoke_test_url()
    with ApiClient(base_url=url, lambda_mode=False) as client:
        yield client
