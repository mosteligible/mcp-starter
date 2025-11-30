"""Authentication middleware for MCP servers."""

import os
from typing import Any, Callable

from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware:
    """Authentication middleware for FastAPI/Starlette applications.

    This middleware validates authentication tokens before allowing requests
    to proceed to the MCP server handlers.

    Example usage with FastAPI:
        ```python
        from fastapi import FastAPI
        from mcp_starter.middleware import AuthMiddleware

        app = FastAPI()
        app.add_middleware(AuthMiddleware, token="your-secret-token")
        ```
    """

    def __init__(
        self,
        app: Any,
        token: str | None = None,
        header_name: str = "Authorization",
        token_prefix: str = "Bearer",
        exclude_paths: list[str] | None = None,
    ):
        """Initialize the authentication middleware.

        Args:
            app: The ASGI application to wrap.
            token: The expected authentication token. If None, uses AUTH_TOKEN env var.
            header_name: The header name to look for the token. Defaults to "Authorization".
            token_prefix: The prefix before the token (e.g., "Bearer"). Defaults to "Bearer".
            exclude_paths: List of paths to exclude from authentication. Defaults to ["/health"].
        """
        self.app = app
        self.token = token or os.environ.get("AUTH_TOKEN")
        self.header_name = header_name
        self.token_prefix = token_prefix
        self.exclude_paths = exclude_paths or ["/health"]

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        """ASGI interface for the middleware."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        path = request.url.path

        # Skip authentication for excluded paths
        if path in self.exclude_paths:
            await self.app(scope, receive, send)
            return

        # Skip authentication if no token is configured
        if not self.token:
            await self.app(scope, receive, send)
            return

        # Validate the authentication token
        is_valid, error_response = await self._validate_token(request)
        if not is_valid and error_response:
            await error_response(scope, receive, send)
            return

        await self.app(scope, receive, send)

    async def _validate_token(self, request: Request) -> tuple[bool, Any | None]:
        """Validate the authentication token from the request.

        Args:
            request: The incoming request.

        Returns:
            A tuple of (is_valid, error_response).
        """
        auth_header = request.headers.get(self.header_name)

        if not auth_header:
            return False, JSONResponse(
                status_code=401,
                content={"error": "Missing authentication header"},
            )

        # Parse the token from the header
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.token_prefix:
            error_msg = (
                f"Invalid authentication header format. Expected: {self.token_prefix} <token>"
            )
            return False, JSONResponse(
                status_code=401,
                content={"error": error_msg},
            )

        token = parts[1]
        if token != self.token:
            return False, JSONResponse(
                status_code=403,
                content={"error": "Invalid authentication token"},
            )

        return True, None


async def bearer_token_auth(
    token: str | None = None,
    header_name: str = "Authorization",
    token_prefix: str = "Bearer",
) -> Callable:
    """Create a bearer token authentication dependency for FastAPI.

    This can be used as a FastAPI dependency to validate bearer tokens.

    Example usage:
        ```python
        from fastapi import FastAPI, Depends
        from mcp_starter.middleware import bearer_token_auth

        app = FastAPI()

        @app.get("/protected")
        async def protected_route(auth=Depends(bearer_token_auth(token="secret"))):
            return {"message": "Authenticated!"}
        ```

    Args:
        token: The expected authentication token. If None, uses AUTH_TOKEN env var.
        header_name: The header name to look for the token.
        token_prefix: The prefix before the token.

    Returns:
        A dependency function for FastAPI.
    """
    expected_token = token or os.environ.get("AUTH_TOKEN")

    async def verify_token(request: Request) -> bool:
        if not expected_token:
            return True

        auth_header = request.headers.get(header_name)
        if not auth_header:
            from fastapi import HTTPException

            raise HTTPException(status_code=401, detail="Missing authentication header")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != token_prefix:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=401,
                detail=f"Invalid authentication header format. Expected: {token_prefix} <token>",
            )

        if parts[1] != expected_token:
            from fastapi import HTTPException

            raise HTTPException(status_code=403, detail="Invalid authentication token")

        return True

    return verify_token
