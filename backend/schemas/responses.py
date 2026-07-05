"""Response schema models for the Agentic SOC application.

Defines the structure for HTTP responses including standard root info,
health check parameters, and a unified error envelope format.
"""

from typing import Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Pydantic model representing the response schema of the health endpoint."""

    status: str = Field(default="healthy", description="Application health status.")
    service: str = Field(..., description="The name of the service.")
    version: str = Field(..., description="The current version of the application.")


class RootResponse(BaseModel):
    """Pydantic model representing the response schema of the root endpoint."""

    app_name: str = Field(..., description="Name of the application.")
    version: str = Field(..., description="Version of the application.")
    environment: str = Field(
        ..., description="Current running environment (e.g., development, production)."
    )
    docs_url: str = Field(
        ..., description="URL to the interactive OpenAPI documentation."
    )


class ErrorDetails(BaseModel):
    """Model representing granular error detail attributes."""

    code: str = Field(
        ..., description="Machine-readable string error code classification."
    )
    message: str = Field(
        ..., description="A clear, human-readable summary explaining the error."
    )
    details: Any | None = Field(
        default=None,
        description="Detailed contextual list or dictionary (e.g., validation issues).",
    )


class ErrorResponse(BaseModel):
    """Unified envelope model representing all failed API operations."""

    success: bool = Field(
        default=False,
        description="Boolean marker indicating failure status (always False).",
    )
    error: ErrorDetails = Field(..., description="The details containing the error.")
