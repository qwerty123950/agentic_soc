"""Global API router orchestrator.

Integrates the versioned APIs under the configurable endpoint prefix.
"""

from fastapi import APIRouter
from backend.api.v1.router import v1_router
from backend.core.config import settings

api_router = APIRouter()

# Register v1 router under the configured API version string (e.g. /api/v1)
api_router.include_router(v1_router, prefix=settings.API_V1_STR)
