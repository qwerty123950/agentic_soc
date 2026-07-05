"""Health check endpoint router for the Agentic SOC.

Returns basic health status of the application including service name and version.
"""

from fastapi import APIRouter
from backend.core.config import settings
from backend.schemas.responses import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check backend service health",
)
def get_health() -> HealthResponse:
    """Get the running status and identity of the SOC backend service."""
    return HealthResponse(
        status="healthy", service=settings.APP_NAME, version="0.1.0"
    )
