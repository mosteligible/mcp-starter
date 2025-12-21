"""Configuration resource for MCP demonstration."""

import os


class Settings:
    """Application settings loaded from environment variables.

    All environment variables should be read through this class.
    """

    # Server settings
    SERVER_NAME: str = os.getenv("SERVER_NAME", "MCP Starter Server")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # FastMCP transport settings
    # Options: "sse", "stateless_http" (default)
    MCP_TRANSPORT: str = os.getenv("MCP_TRANSPORT", "stateless_http")

    # Authentication settings
    AUTH_TOKEN: str | None = os.getenv("AUTH_TOKEN")

    # Server binding settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Application version (constant)
    VERSION: str = "0.1.0"


# Singleton instance for easy access
settings = Settings()


def get_config() -> dict:
    """Get the server configuration.

    Returns:
        A dictionary containing server configuration values.
    """
    return {
        "server_name": settings.SERVER_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
    }
