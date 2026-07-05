"""Configuration management module for the Agentic SOC backend application.

This module defines the Settings class which loads configuration values from
environment variables and an optional .env file using Pydantic Settings.
"""

from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings class loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application Metadata
    APP_ENV: str = "development"
    APP_NAME: str = "Agentic SOC"
    API_V1_STR: str = "/api/v1"

    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Logging
    LOG_LEVEL: str = "INFO"

    # Security & Middleware Configuration
    ALLOWED_HOSTS: list[str] = ["*"]
    CORS_ORIGINS: list[str] = ["*"]

    @field_validator("ALLOWED_HOSTS", "CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_list(cls, v: Any) -> list[str]:
        """Convert a comma-separated string to a list of strings if necessary."""
        if isinstance(v, str):
            if not v or v.strip() == "*":
                return ["*"]
            return [item.strip() for item in v.split(",") if item.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]


# Instantiate settings to be imported across the application
settings = Settings()
