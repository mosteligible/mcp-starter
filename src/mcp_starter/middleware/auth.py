"""Authentication middleware for MCP servers."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for FastAPI/Starlette applications.

    This is a base middleware class that can be extended to add
    authentication logic. Currently provides a simple pass-through
    dispatch method.

    Example usage with FastAPI:
        ```python
        from fastapi import FastAPI
        from mcp_starter.middleware import AuthMiddleware

        app = FastAPI()
        app.add_middleware(AuthMiddleware)
        ```
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """Dispatch method for the middleware.

        Override this method to add custom authentication logic.

        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.

        Returns:
            The response from the next handler.
        """
        # TODO: Add authentication logic here
        # Example: validate settings.AUTH_TOKEN against request headers
        response = await call_next(request)
        return response
