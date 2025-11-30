"""Tests for the authentication middleware."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from mcp_starter.middleware.auth import AuthMiddleware


def create_test_app(token: str | None = None, exclude_paths: list[str] | None = None) -> FastAPI:
    """Create a test FastAPI app with AuthMiddleware."""
    app = FastAPI()

    @app.get("/public")
    async def public_route():
        return {"message": "public"}

    @app.get("/protected")
    async def protected_route():
        return {"message": "protected"}

    @app.get("/health")
    async def health_route():
        return {"status": "healthy"}

    exclude = exclude_paths if exclude_paths is not None else ["/health"]
    app.add_middleware(AuthMiddleware, token=token, exclude_paths=exclude)

    return app


class TestAuthMiddleware:
    """Tests for the AuthMiddleware class."""

    def test_no_token_configured_allows_all(self):
        """Test that requests pass through when no token is configured."""
        app = create_test_app(token=None)
        client = TestClient(app)

        response = client.get("/protected")
        assert response.status_code == 200
        assert response.json() == {"message": "protected"}

    def test_excluded_paths_skip_auth(self):
        """Test that excluded paths skip authentication."""
        app = create_test_app(token="secret-token", exclude_paths=["/health", "/public"])
        client = TestClient(app)

        # Health should be accessible without auth
        response = client.get("/health")
        assert response.status_code == 200

        # Public should be accessible without auth
        response = client.get("/public")
        assert response.status_code == 200

    def test_missing_auth_header_returns_401(self):
        """Test that missing auth header returns 401."""
        app = create_test_app(token="secret-token")
        client = TestClient(app)

        response = client.get("/protected")
        assert response.status_code == 401
        assert "Missing authentication header" in response.json()["error"]

    def test_invalid_header_format_returns_401(self):
        """Test that invalid auth header format returns 401."""
        app = create_test_app(token="secret-token")
        client = TestClient(app)

        # Missing Bearer prefix
        response = client.get("/protected", headers={"Authorization": "secret-token"})
        assert response.status_code == 401
        assert "Invalid authentication header format" in response.json()["error"]

        # Wrong prefix
        response = client.get("/protected", headers={"Authorization": "Basic secret-token"})
        assert response.status_code == 401

    def test_invalid_token_returns_403(self):
        """Test that invalid token returns 403."""
        app = create_test_app(token="secret-token")
        client = TestClient(app)

        response = client.get("/protected", headers={"Authorization": "Bearer wrong-token"})
        assert response.status_code == 403
        assert "Invalid authentication token" in response.json()["error"]

    def test_valid_token_allows_access(self):
        """Test that valid token allows access."""
        app = create_test_app(token="secret-token")
        client = TestClient(app)

        response = client.get("/protected", headers={"Authorization": "Bearer secret-token"})
        assert response.status_code == 200
        assert response.json() == {"message": "protected"}
