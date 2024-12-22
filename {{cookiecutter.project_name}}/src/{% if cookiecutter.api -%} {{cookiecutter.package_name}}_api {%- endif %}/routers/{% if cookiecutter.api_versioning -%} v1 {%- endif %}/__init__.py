"""API v1 router module.

This module aggregates all v1 API endpoints under a common /v1 prefix.
Add your versioned routes by importing routers and including them here.

Usage:
    # In your router module (e.g., routers/v1/items.py):
    from fastapi import APIRouter
    router = APIRouter(prefix="/items", tags=["items"])

    @router.get("/")
    async def list_items():
        return {"items": []}

    # Then in this file, add:
    from {{cookiecutter.package_name}}_api.routers.v1 import items
    router.include_router(items.router)
"""

from fastapi import APIRouter

from {{cookiecutter.package_name}}_api.routers.v1 import example

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(example.router)
