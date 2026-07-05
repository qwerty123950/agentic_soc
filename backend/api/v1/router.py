"""V1 API Router assembly.

Includes and prefixes endpoints under /api/v1 namespace.
"""

from fastapi import APIRouter
from backend.api.v1.endpoints import health, root

v1_router = APIRouter()

# Root endpoints at version namespace
v1_router.include_router(root.router, tags=["System Root"])
v1_router.include_router(health.router, tags=["System Health"])
