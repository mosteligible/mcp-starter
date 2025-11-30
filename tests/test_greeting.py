"""Tests for the greeting tools."""

from mcp_starter.tools.greeting import greet


def test_greet_default():
    """Test greeting with default greeting word."""
    assert greet("World") == "Hello, World!"


def test_greet_custom_greeting():
    """Test greeting with custom greeting word."""
    assert greet("Alice", "Hi") == "Hi, Alice!"


def test_greet_different_names():
    """Test greeting with different names."""
    assert greet("Bob") == "Hello, Bob!"
    assert greet("Charlie", "Welcome") == "Welcome, Charlie!"
