"""Example v1 API endpoints.

This is a placeholder router demonstrating the versioned API structure.
Delete this file and create your own routers as needed.

Example usage:
    GET /v1/example -> {"message": "This is API v1", "version": "1.0.0"}
"""

from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["example"])


@router.get("/")
async def get_example() -> dict[str, str]:
    """Get example endpoint demonstrating v1 API.

    Returns:
        Example response with version information.
    """
    return {"message": "This is API v1", "version": "1.0.0"}
