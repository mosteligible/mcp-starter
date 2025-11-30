"""FastMCP standalone server with configurable middleware.

This module provides a FastMCP server implementation that can be run
standalone with configurable middleware for authentication and other
processing needs.

Example usage:
    ```python
    from mcp_starter.fastmcp_server import create_mcp_server, run

    # Create server with default configuration
    mcp = create_mcp_server()

    # Run the server
    run()
    ```

    Or run from command line:
    ```bash
    mcp-fastmcp
    ```

Environment Variables:
    MCP_TRANSPORT: Transport mode - "sse" or "stateless_http" (default: "stateless_http")
"""

from fastmcp import FastMCP

from mcp_starter.resources.config import get_config, settings
from mcp_starter.resources.info import get_server_info
from mcp_starter.tools.calculator import add, divide, multiply, subtract
from mcp_starter.tools.greeting import greet


def create_mcp_server(
    name: str | None = None,
    instructions: str | None = None,
) -> FastMCP:
    """Create and configure a FastMCP server instance.

    This function creates a FastMCP server with sample tools and resources.
    The server can be customized by passing configuration parameters.

    Args:
        name: The name of the MCP server. Defaults to SERVER_NAME env var or "FastMCP Starter".
        instructions: Instructions for using the server.

    Returns:
        A configured FastMCP server instance.

    Example:
        ```python
        mcp = create_mcp_server(
            name="My MCP Server",
            instructions="Use the calculator tools to perform math operations.",
        )
        ```
    """
    server_name = name or settings.SERVER_NAME
    server_instructions = instructions or "A starter MCP server with sample tools and resources."

    mcp = FastMCP(
        name=server_name,
        instructions=server_instructions,
    )

    # Register calculator tools
    mcp.tool()(add)
    mcp.tool()(subtract)
    mcp.tool()(multiply)
    mcp.tool()(divide)

    # Register greeting tool
    mcp.tool()(greet)

    # Register resources
    @mcp.resource("config://server")
    def config_resource() -> dict:
        """Get the server configuration."""
        return get_config()

    @mcp.resource("info://server")
    def info_resource() -> dict:
        """Get server information."""
        return get_server_info()

    return mcp


# Create the default server instance
mcp = create_mcp_server()


def run() -> None:
    """Run the FastMCP server.

    This function starts the FastMCP server using the configured transport.
    The transport mode can be configured via the MCP_TRANSPORT environment variable:
        - "sse": Server-Sent Events transport
        - "stateless_http": Stateless HTTP transport (default)

    The server can be configured using environment variables:
        - SERVER_NAME: The name of the server
        - MCP_TRANSPORT: Transport mode ("sse" or "stateless_http")

    Example:
        ```bash
        export SERVER_NAME="My MCP Server"
        export MCP_TRANSPORT="stateless_http"
        mcp-fastmcp
        ```
    """
    transport = settings.MCP_TRANSPORT
    if transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run(transport="streamable-http")


if __name__ == "__main__":
    run()
