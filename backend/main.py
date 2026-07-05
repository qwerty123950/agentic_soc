"""Main application initialization module for the Agentic SOC backend.

Constructs the FastAPI application instance, configures custom lifespan hooks,
registers standard and custom middlewares, binds centralized error handlers,
and mounts API versioned routing paths.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from backend.api.router import api_router
from backend.core.config import settings
from backend.core.logging import setup_logging
from backend.middleware.errors import register_error_handlers
from backend.middleware.logging_middleware import LoggingMiddleware
from backend.middleware.request_id import RequestIdMiddleware
from backend.schemas.responses import RootResponse

# Initialize logging configuration before building the FastAPI app
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages application startup and shutdown lifecycles."""
    logger.info("Initializing Agentic SOC application foundation...")
    yield
    logger.info("Shutting down Agentic SOC application foundation...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise-grade Security Operations Center (SOC) platform backend skeleton.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Apply middlewares (order matters: executed from bottom to top for incoming request)
# 1. Custom HTTP logging (inner middleware)
app.add_middleware(LoggingMiddleware)

# 2. Request tracing identifier injection
app.add_middleware(RequestIdMiddleware)

# 3. Allowed CORS Origins configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Security Trusted Host middleware (applied if hosts are explicitly restricted)
if settings.ALLOWED_HOSTS and "*" not in settings.ALLOWED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS
    )

# Register centralized error handlers
register_error_handlers(app)

# Register versioned API router (/api/v1/...)
app.include_router(api_router)


# Root endpoint of the application redirecting/returning system index
@app.get(
    "/",
    response_model=RootResponse,
    tags=["System Root"],
    summary="Get API root metadata",
)
def get_app_root() -> RootResponse:
    """Return top-level application metadata for the SOC backend system."""
    return RootResponse(
        app_name=settings.APP_NAME,
        version="0.1.0",
        environment=settings.APP_ENV,
        docs_url="/docs",
    )
