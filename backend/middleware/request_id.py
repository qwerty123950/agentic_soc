"""Request ID middleware for tracing and debugging.

Generates or forwards a unique X-Request-ID header value for every incoming
HTTP request, setting it in the async context for logging purposes.
"""

import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from backend.core.context import request_id_ctx_var


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware to inject tracking request IDs into request and response lifecycles."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process incoming requests, assigning and managing the request ID context."""
        # Retrieve incoming Request ID or generate a new random UUID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Set request ID in context variables for logging
        token = request_id_ctx_var.set(request_id)

        try:
            # Store request ID in request state for endpoint handlers
            request.state.request_id = request_id

            # Proceed to next middleware/handler
            response = await call_next(request)

            # Return request ID in response header
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            # Reset context value for this task
            request_id_ctx_var.reset(token)
