"""Tests for the authentication middleware."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from mcp_starter.middleware.auth import AuthMiddleware


def create_test_app() -> FastAPI:
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

    app.add_middleware(AuthMiddleware)

    return app


def test_middleware_passes_requests():
    """Test that the middleware passes requests through."""
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/protected")
    assert response.status_code == 200
    assert response.json() == {"message": "protected"}


def test_middleware_health_endpoint():
    """Test that health endpoint is accessible."""
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_middleware_public_endpoint():
    """Test that public endpoint is accessible."""
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "public"}
