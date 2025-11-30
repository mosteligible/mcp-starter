"""Tests for the resources."""

import os
from unittest.mock import patch

from mcp_starter.resources.info import get_server_info


# Tests for the get_config function
def test_get_config_defaults():
    """Test get_config returns default values."""
    # Clear any existing env vars
    with patch.dict(os.environ, {}, clear=True):
        # Need to reimport to get fresh settings
        import importlib

        import mcp_starter.resources.config as config_module

        importlib.reload(config_module)
        config = config_module.get_config()
        assert config["server_name"] == "MCP Starter Server"
        assert config["version"] == "0.1.0"
        assert config["environment"] == "development"
        assert config["debug"] is False


def test_get_config_with_env_vars():
    """Test get_config uses environment variables."""
    env_vars = {
        "SERVER_NAME": "Test Server",
        "ENVIRONMENT": "production",
        "DEBUG": "true",
    }
    with patch.dict(os.environ, env_vars, clear=True):
        # Need to reimport to get fresh settings
        import importlib

        import mcp_starter.resources.config as config_module

        importlib.reload(config_module)
        config = config_module.get_config()
        assert config["server_name"] == "Test Server"
        assert config["environment"] == "production"
        assert config["debug"] is True


# Tests for the get_server_info function
def test_get_server_info_structure():
    """Test get_server_info returns expected structure."""
    info = get_server_info()
    assert "python_version" in info
    assert "platform" in info
    assert "platform_release" in info
    assert "timestamp" in info


def test_get_server_info_types():
    """Test get_server_info returns correct types."""
    info = get_server_info()
    assert isinstance(info["python_version"], str)
    assert isinstance(info["platform"], str)
    assert isinstance(info["timestamp"], str)
