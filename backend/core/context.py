"""Context storage utilities for request-scoped variables using ContextVars.

This module provides thread-safe, async-safe storage for variables like Request ID.
"""

from contextvars import ContextVar

# Context variable to hold the request ID for the current async execution context
request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="-")
