"""HTTP client utilities for integration and smoke tests."""

import base64
import contextlib
import json
from typing import Any, Final

import httpx


class ApiClient:
    """HTTP client for testing Lambda API endpoints.

    Supports two modes:
    - Lambda invoke mode: Calls Lambda via Docker Compose's Runtime Interface Emulator
    - Direct HTTP mode: Calls deployed Lambda via API Gateway/Function URL

    Attributes:
        base_url: The base URL of the API endpoint.
        lambda_mode: Whether to use Lambda invoke format (for Docker Compose testing).
    """

    # Default Lambda RIE endpoint in Docker Compose
    LAMBDA_RIE_URL: Final[str] = "http://localhost:9000/2015-03-31/functions/function/invocations"

    def __init__(
        self,
        base_url: str | None = None,
        lambda_mode: bool = True,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the API client.

        Args:
            base_url: The base URL for direct HTTP mode. Ignored in lambda_mode.
            lambda_mode: If True, use Lambda invoke format via RIE.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url or self.LAMBDA_RIE_URL
        self.lambda_mode = lambda_mode
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "ApiClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.close()

    @staticmethod
    def create_alb_event(
        method: str,
        path: str,
        body: dict[str, Any] | str | None = None,
        headers: dict[str, str] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create an ALB (Application Load Balancer) event for Lambda invocation.

        Args:
            method: HTTP method (GET, POST, etc.).
            path: Request path (e.g., /health).
            body: Request body (dict will be JSON-encoded).
            headers: HTTP headers.
            query_params: Query string parameters.

        Returns:
            ALB event dictionary suitable for Lambda invocation.
        """
        default_headers = {
            "host": "localhost",
            "user-agent": "ApiClient/1.0",
            "accept": "application/json",
            "content-type": "application/json",
        }
        merged_headers = {**default_headers, **(headers or {})}

        # Encode body if dict
        encoded_body = ""
        is_base64 = False
        if body is not None:
            encoded_body = json.dumps(body) if isinstance(body, dict) else body

        target_group_arn = "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/test/1234567890123456"
        return {
            "requestContext": {"elb": {"targetGroupArn": target_group_arn}},
            "httpMethod": method.upper(),
            "path": path,
            "queryStringParameters": query_params or {},
            "headers": merged_headers,
            "body": encoded_body,
            "isBase64Encoded": is_base64,
        }

    def _invoke_lambda(self, event: dict[str, Any]) -> httpx.Response:
        """Invoke Lambda via RIE.

        Args:
            event: Lambda event payload.

        Returns:
            HTTP response from the Lambda function.
        """
        return self._client.post(
            self.LAMBDA_RIE_URL,
            json=event,
        )

    def _parse_lambda_response(self, response: httpx.Response) -> dict[str, Any]:
        """Parse Lambda invocation response.

        Args:
            response: HTTP response from Lambda RIE.

        Returns:
            Parsed response with statusCode, headers, and body.
        """
        lambda_result = response.json()

        # Lambda response format
        status_code = lambda_result.get("statusCode", 500)
        headers = lambda_result.get("headers", {})
        body = lambda_result.get("body", "")

        # Decode base64 body if needed
        if lambda_result.get("isBase64Encoded", False):
            body = base64.b64decode(body).decode("utf-8")

        # Parse JSON body if applicable
        content_type = headers.get("content-type", "")
        if "application/json" in content_type and body:
            with contextlib.suppress(json.JSONDecodeError):
                body = json.loads(body)

        return {
            "status_code": status_code,
            "headers": headers,
            "body": body,
            "raw_response": lambda_result,
        }

    def request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | str | None = None,
        headers: dict[str, str] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.).
            path: Request path (e.g., /health).
            body: Request body (dict will be JSON-encoded).
            headers: HTTP headers.
            query_params: Query string parameters.

        Returns:
            Response dictionary with status_code, headers, and body.
        """
        if self.lambda_mode:
            event = self.create_alb_event(
                method=method,
                path=path,
                body=body,
                headers=headers,
                query_params=query_params,
            )
            response = self._invoke_lambda(event)
            return self._parse_lambda_response(response)
        else:
            # Direct HTTP mode for deployed Lambda
            url = f"{self.base_url.rstrip('/')}{path}"
            response = self._client.request(
                method=method,
                url=url,
                json=body if isinstance(body, dict) else None,
                content=body if isinstance(body, str) else None,
                headers=headers,
                params=query_params,
            )
            content_type = response.headers.get("content-type", "")
            body = response.json() if content_type.startswith("application/json") else response.text
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": body,
                "raw_response": response,
            }

    def get(
        self,
        path: str,
        headers: dict[str, str] | None = None,
        query_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a GET request."""
        return self.request("GET", path, headers=headers, query_params=query_params)

    def post(
        self,
        path: str,
        body: dict[str, Any] | str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a POST request."""
        return self.request("POST", path, body=body, headers=headers)

    def health_check(self) -> dict[str, Any]:
        """Check the /health endpoint.

        Returns:
            Health check response.
        """
        return self.get("/health")
