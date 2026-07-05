"""Root metadata endpoint router for the Agentic SOC.

Provides top-level system info such as application name, current version,
environment type, and API documentation references.
"""

from fastapi import APIRouter
from backend.core.config import settings
from backend.schemas.responses import RootResponse

router = APIRouter()


@router.get("/", response_model=RootResponse, summary="Get API Metadata")
def get_root() -> RootResponse:
    """Retrieve top-level info and documentation links for the SOC API."""
    return RootResponse(
        app_name=settings.APP_NAME,
        version="0.1.0",
        environment=settings.APP_ENV,
        docs_url="/docs",
    )
