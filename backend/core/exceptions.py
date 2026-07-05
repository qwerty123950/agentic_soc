"""Custom exception definitions for the Agentic SOC application.

Provides a unified base class to signal application-level errors
with HTTP status codes, error classification codes, and details.
"""

from typing import Any


class SOCException(Exception):
    """Base application exception for custom error states."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


class SOCNotFoundException(SOCException):
    """Exception raised when a requested resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            status_code=404, code=code, message=message, details=details
        )


class SOCBadRequestException(SOCException):
    """Exception raised for invalid payload arguments or bad requests."""

    def __init__(
        self,
        message: str = "Bad request parameters",
        code: str = "BAD_REQUEST",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            status_code=400, code=code, message=message, details=details
        )
