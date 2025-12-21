"""Tests for the FastMCP standalone server."""

from mcp_starter.fastmcp_server.main import create_mcp_server


def test_create_mcp_server_default():
    """Test creating MCP server with default settings."""
    mcp = create_mcp_server()
    assert mcp is not None
    assert mcp.name == "MCP Starter Server"


def test_create_mcp_server_custom_name():
    """Test creating MCP server with custom name."""
    mcp = create_mcp_server(name="Custom Server")
    assert mcp.name == "Custom Server"


def test_create_mcp_server_custom_instructions():
    """Test creating MCP server with custom instructions."""
    mcp = create_mcp_server(instructions="Custom instructions")
    assert mcp.instructions == "Custom instructions"
