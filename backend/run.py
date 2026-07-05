"""Startup launcher script for the Agentic SOC FastAPI application.

Configures and executes the Uvicorn server, enabling live reload during
local development and loading options from settings.
"""

import uvicorn
from backend.core.config import settings


def main() -> None:
    """Launch the Uvicorn server programmatically."""
    # We set log_config=None to prevent Uvicorn from resetting our custom log configuration
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.APP_ENV == "development",
        log_config=None,
    )


if __name__ == "__main__":
    main()
