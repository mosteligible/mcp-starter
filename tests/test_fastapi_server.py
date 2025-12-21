"""Tests for the FastAPI + FastMCP integrated server."""

from fastapi.testclient import TestClient

from mcp_starter.fastapi_fastmcp_server.main import create_app, create_mcp_server


# Tests for the create_mcp_server function
def test_create_mcp_server_default():
    """Test creating MCP server with default settings."""
    mcp = create_mcp_server()
    assert mcp is not None
    assert mcp.name == "MCP Starter Server"


def test_create_mcp_server_custom_name():
    """Test creating MCP server with custom name."""
    mcp = create_mcp_server(name="Custom Server")
    assert mcp.name == "Custom Server"


# Tests for the create_app function
def test_create_app_default():
    """Test creating FastAPI app with default settings."""
    app = create_app()
    assert app is not None
    client = TestClient(app)

    # Health endpoint should be accessible
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_app_cors_enabled():
    """Test that CORS is enabled by default."""
    app = create_app()
    client = TestClient(app)

    # Check CORS headers
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" in response.headers


def test_create_app_mcp_endpoint():
    """Test that MCP endpoint is mounted."""
    app = create_app()
    # Verify the app has the /mcp mount registered
    # The MCP endpoint is mounted as a sub-application
    routes = [route for route in app.routes if hasattr(route, "path")]
    mcp_routes = [route for route in routes if "/mcp" in str(route.path)]
    assert len(mcp_routes) > 0, "MCP endpoint should be mounted"


def test_create_app_custom_mcp():
    """Test creating FastAPI app with custom MCP server."""
    mcp = create_mcp_server(name="Custom MCP")
    app = create_app(mcp=mcp)
    assert app is not None
