"""Global error handling middleware for the Agentic SOC application.

Registers custom handlers to translate exceptions into standardized API responses
conforming to the ErrorResponse schema definition.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from backend.core.exceptions import SOCException
from backend.schemas.responses import ErrorDetails, ErrorResponse

logger = logging.getLogger(__name__)


async def soc_exception_handler(
    request: Request, exc: SOCException
) -> JSONResponse:
    """Handle custom application SOCException errors."""
    error_response = ErrorResponse(
        success=False,
        error=ErrorDetails(
            code=exc.code, message=exc.message, details=exc.details
        ),
    )
    return JSONResponse(
        status_code=exc.status_code, content=error_response.model_dump()
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request payload validation errors (Pydantic / FastAPI)."""
    error_response = ErrorResponse(
        success=False,
        error=ErrorDetails(
            code="VALIDATION_ERROR",
            message="Request validation failed.",
            details=exc.errors(),
        ),
    )
    return JSONResponse(status_code=422, content=error_response.model_dump())


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle standard Starlette/FastAPI HTTPExceptions (e.g. 404 Not Found)."""
    error_response = ErrorResponse(
        success=False,
        error=ErrorDetails(
            code="HTTP_ERROR", message=str(exc.detail), details=None
        ),
    )
    return JSONResponse(
        status_code=exc.status_code, content=error_response.model_dump()
    )


async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle unexpected runtime exceptions and prevent traceback leaks."""
    logger.exception("Unhandled application error: %s", str(exc))
    error_response = ErrorResponse(
        success=False,
        error=ErrorDetails(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected internal server error occurred.",
            details=None,
        ),
    )
    return JSONResponse(status_code=500, content=error_response.model_dump())


def register_error_handlers(app: FastAPI) -> None:
    """Register exception handlers on the FastAPI application instance."""
    app.add_exception_handler(SOCException, soc_exception_handler)
    app.add_exception_handler(
        RequestValidationError, validation_exception_handler
    )
    app.add_exception_handler(
        StarletteHTTPException, http_exception_handler
    )
    app.add_exception_handler(Exception, general_exception_handler)
