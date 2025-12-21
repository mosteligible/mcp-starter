"""Greeting tools for MCP demonstration."""


def greet(name: str, greeting: str = "Hello") -> str:
    """Generate a personalized greeting message.

    Args:
        name: The name of the person to greet.
        greeting: The greeting word to use. Defaults to "Hello".

    Returns:
        A personalized greeting message.
    """
    return f"{greeting}, {name}!"
