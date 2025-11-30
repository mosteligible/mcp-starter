"""Configuration resource for MCP demonstration."""

import os


def get_config() -> dict:
    """Get the server configuration.

    Returns:
        A dictionary containing server configuration values.
    """
    return {
        "server_name": os.environ.get("SERVER_NAME", "MCP Starter Server"),
        "version": "0.1.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "debug": os.environ.get("DEBUG", "false").lower() == "true",
    }
