"""Integration tests for Lambda API endpoints."""

from common.http import ApiClient


class TestHealthEndpoint:
    """Tests for the /health endpoint via Lambda RIE."""

    def test_health_check_returns_healthy(self, lambda_client: ApiClient) -> None:
        """Test health endpoint returns healthy status."""
        response = lambda_client.health_check()

        assert response["status_code"] == 200
        assert response["body"]["status"] == "healthy"

    def test_health_check_returns_json(self, lambda_client: ApiClient) -> None:
        """Test health endpoint returns JSON content type."""
        response = lambda_client.health_check()

        content_type = response["headers"].get("content-type", "")
        assert "application/json" in content_type


class TestApiErrorHandling:
    """Tests for API error handling."""

    def test_not_found_returns_404(self, lambda_client: ApiClient) -> None:
        """Test unknown paths return 404."""
        response = lambda_client.get("/nonexistent/path")

        assert response["status_code"] == 404
