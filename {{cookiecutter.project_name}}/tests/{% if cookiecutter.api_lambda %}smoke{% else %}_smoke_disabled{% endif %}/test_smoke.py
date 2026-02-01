"""Smoke tests for deployed Lambda API.

These tests verify the deployed Lambda function is working correctly.
Set SMOKE_TEST_URL environment variable to the Lambda Function URL or API Gateway endpoint.
"""

from common.http import ApiClient


class TestDeployedApi:
    """Smoke tests for deployed Lambda API."""

    def test_health_endpoint_is_healthy(self, smoke_client: ApiClient) -> None:
        """Test deployed API health endpoint returns healthy."""
        response = smoke_client.health_check()

        assert response["status_code"] == 200
        assert response["body"]["status"] == "healthy"

    def test_health_endpoint_returns_version(self, smoke_client: ApiClient) -> None:
        """Test health endpoint includes version information."""
        response = smoke_client.health_check()

        assert "version" in response["body"]
