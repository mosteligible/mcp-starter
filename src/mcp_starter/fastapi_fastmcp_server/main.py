"""FastAPI + FastMCP integrated server with configurable middleware.

This module provides a FastAPI application that integrates FastMCP's http_app,
allowing you to serve MCP endpoints alongside regular FastAPI routes with
full middleware support.

Example usage:
    ```python
    from mcp_starter.fastapi_fastmcp_server import create_app, run

    # Create app with authentication middleware
    app = create_app(auth_token="your-secret-token")

    # Run the server
    run()
    ```

    Or run from command line:
    ```bash
    mcp-fastapi
    ```
"""

import os
from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from mcp_starter.middleware.auth import AuthMiddleware
from mcp_starter.resources.config import get_config
from mcp_starter.resources.info import get_server_info
from mcp_starter.tools.calculator import add, divide, multiply, subtract
from mcp_starter.tools.greeting import greet


def create_mcp_server(
    name: str | None = None,
    instructions: str | None = None,
) -> FastMCP:
    """Create and configure a FastMCP server instance.

    Args:
        name: The name of the MCP server. Defaults to SERVER_NAME env var.
        instructions: Instructions for using the server.

    Returns:
        A configured FastMCP server instance.
    """
    server_name = name or os.environ.get("SERVER_NAME", "FastAPI + FastMCP Starter")
    server_instructions = instructions or "A starter MCP server with FastAPI integration."

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


def create_app(
    mcp: FastMCP | None = None,
    auth_token: str | None = None,
    enable_cors: bool = True,
    cors_origins: list[str] | None = None,
    additional_middleware: list[tuple[type, dict[str, Any]]] | None = None,
    lifespan: Callable | None = None,
) -> FastAPI:
    """Create a FastAPI application with FastMCP integration.

    This function creates a FastAPI application that mounts FastMCP's http_app
    at the /mcp endpoint, allowing MCP communication over HTTP. The application
    can be configured with authentication middleware and other middleware.

    Args:
        mcp: A pre-configured FastMCP instance. If None, creates a new one.
        auth_token: Authentication token for the AuthMiddleware.
            If None, uses AUTH_TOKEN env var. Set to empty string to disable auth.
        enable_cors: Whether to enable CORS middleware. Defaults to True.
        cors_origins: List of allowed CORS origins. Defaults to ["*"].
        additional_middleware: List of additional middleware to add.
            Each item is a tuple of (middleware_class, kwargs_dict).
        lifespan: Custom lifespan context manager for the FastAPI app.

    Returns:
        A configured FastAPI application.

    Example:
        ```python
        # Basic usage with authentication
        app = create_app(auth_token="secret-token")

        # With custom CORS origins
        app = create_app(
            auth_token="secret-token",
            cors_origins=["http://localhost:3000", "https://myapp.com"],
        )

        # With additional middleware
        from some_middleware import RateLimitMiddleware

        app = create_app(
            additional_middleware=[
                (RateLimitMiddleware, {"requests_per_minute": 60}),
            ],
        )

        # With custom MCP server
        mcp = create_mcp_server(name="Custom Server")
        app = create_app(mcp=mcp)
        ```
    """
    # Create MCP server if not provided
    if mcp is None:
        mcp = create_mcp_server()

    # Default lifespan that does nothing
    @asynccontextmanager
    async def default_lifespan(app: FastAPI):
        yield

    # Create FastAPI app
    app = FastAPI(
        title="FastAPI + FastMCP Server",
        description="A FastAPI application with MCP server integration",
        version="0.1.0",
        lifespan=lifespan or default_lifespan,
    )

    # Add CORS middleware if enabled
    if enable_cors:
        origins = cors_origins or ["*"]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add authentication middleware
    # Check if auth_token is explicitly set (including empty string)
    token = auth_token if auth_token is not None else os.environ.get("AUTH_TOKEN")
    if token:  # Only add auth middleware if token is non-empty
        app.add_middleware(
            AuthMiddleware,
            token=token,
            exclude_paths=["/health", "/docs", "/openapi.json", "/redoc"],
        )

    # Add any additional middleware
    if additional_middleware:
        for middleware_class, kwargs in additional_middleware:
            app.add_middleware(middleware_class, **kwargs)

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict:
        """Health check endpoint."""
        return {"status": "healthy"}

    # Mount the FastMCP http_app at /mcp
    app.mount("/mcp", mcp.http_app())

    return app


# Create the default app and MCP instances
mcp = create_mcp_server()
app = create_app(mcp=mcp)


def run(
    host: str | None = None,
    port: int | None = None,
    reload: bool = False,
) -> None:
    """Run the FastAPI server with FastMCP integration.

    Args:
        host: The host to bind to. Defaults to HOST env var or "0.0.0.0".
        port: The port to bind to. Defaults to PORT env var or 8000.
        reload: Whether to enable auto-reload. Defaults to False.

    Example:
        ```bash
        export HOST=0.0.0.0
        export PORT=8000
        export AUTH_TOKEN=my-secret-token
        mcp-fastapi
        ```
    """
    server_host = host or os.environ.get("HOST", "0.0.0.0")
    server_port = port or int(os.environ.get("PORT", "8000"))

    uvicorn.run(
        "mcp_starter.fastapi_fastmcp_server.main:app",
        host=server_host,
        port=server_port,
        reload=reload,
    )


if __name__ == "__main__":
    run()
