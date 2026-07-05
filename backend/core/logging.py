"""Logging configuration module for the Agentic SOC backend.

Sets up a unified console logger format and integrates request-scoped tracking
using ContextVars. Intercepts third-party loggers (e.g., Uvicorn) to ensure
consistent output formatting.
"""

import logging
import sys
from typing import Any
from backend.core.config import settings
from backend.core.context import request_id_ctx_var


class RequestIdFilter(logging.Filter):
    """Logging filter to inject request_id context into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Inject the current request_id from the context variable into the record."""
        record.request_id = request_id_ctx_var.get()
        return True


def setup_logging() -> None:
    """Initialize and configure global logging handlers and formatters.

    This configures the root logger and redirects Uvicorn/FastAPI loggers to
    utilize our custom RequestIdFilter and formatting rules.
    """
    log_level_name = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    # Standardized format string containing request ID for debugging
    log_format = (
        "[%(asctime)s] [%(levelname)s] [%(request_id)s] "
        "[%(name)s:%(lineno)d] - %(message)s"
    )
    formatter = logging.Formatter(log_format)

    # Configure stdout stream handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIdFilter())

    # Configure the root logger
    root_logger = logging.getLogger()
    # Remove default handlers to prevent duplicated logs
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(log_level)

    # Override standard logger configurations to match application logging style
    intercepted_loggers: list[str] = [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
    ]

    for logger_name in intercepted_loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.addHandler(console_handler)
        logger.setLevel(log_level)
        logger.propagate = False
