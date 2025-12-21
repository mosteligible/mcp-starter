"""Server info resource for MCP demonstration."""

import platform
from datetime import datetime, timezone


def get_server_info() -> dict:
    """Get information about the server.

    Returns:
        A dictionary containing server information.
    """
    return {
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
