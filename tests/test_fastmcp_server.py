"""Tests for the FastMCP standalone server."""

from mcp_starter.fastmcp_server.main import create_mcp_server


class TestCreateMcpServer:
    """Tests for the create_mcp_server function."""

    def test_create_mcp_server_default(self):
        """Test creating MCP server with default settings."""
        mcp = create_mcp_server()
        assert mcp is not None
        assert mcp.name == "FastMCP Starter"

    def test_create_mcp_server_custom_name(self):
        """Test creating MCP server with custom name."""
        mcp = create_mcp_server(name="Custom Server")
        assert mcp.name == "Custom Server"

    def test_create_mcp_server_custom_instructions(self):
        """Test creating MCP server with custom instructions."""
        mcp = create_mcp_server(instructions="Custom instructions")
        assert mcp.instructions == "Custom instructions"
