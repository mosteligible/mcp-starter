"""Base middleware class for MCP servers."""

from abc import ABC, abstractmethod
from typing import Any, Callable


class BaseMiddleware(ABC):
    """Abstract base class for middleware components.

    Middleware can be used to intercept and process requests before they reach
    the MCP server handlers, enabling authentication, logging, rate limiting,
    and other cross-cutting concerns.
    """

    @abstractmethod
    async def __call__(
        self,
        request: Any,
        call_next: Callable[..., Any],
    ) -> Any:
        """Process the request through the middleware.

        Args:
            request: The incoming request object.
            call_next: The next handler in the middleware chain.

        Returns:
            The response from the next handler or an error response.
        """
        pass

    @abstractmethod
    async def process_request(self, request: Any) -> tuple[bool, Any | None]:
        """Process and validate the incoming request.

        Args:
            request: The incoming request object.

        Returns:
            A tuple of (is_valid, error_response).
            If is_valid is True, error_response should be None.
            If is_valid is False, error_response contains the error to return.
        """
        pass
