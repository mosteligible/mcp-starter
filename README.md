# MCP Starter

A starter template for building MCP (Model Context Protocol) servers using FastMCP and the Python MCP SDK. This project provides two configurable server implementations with middleware support for authentication and other processing needs.

## Features

- **Two Server Implementations**:
  - **FastMCP Standalone Server**: A pure FastMCP server for stdio-based MCP communication
  - **FastAPI + FastMCP Server**: An HTTP-based server combining FastAPI with FastMCP's http_app

- **Configurable Middleware**:
  - Built-in authentication middleware with Bearer token support
  - Easy integration of custom middleware components
  - CORS support for the FastAPI server

- **Sample Tools and Resources**:
  - Calculator tools (add, subtract, multiply, divide)
  - Greeting tool
  - Server configuration and info resources

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/mosteligible/mcp-starter.git
cd mcp-starter

# Install in development mode
pip install -e ".[dev]"
```

### Using pip

```bash
pip install mcp-starter
```

## Quick Start

### FastMCP Standalone Server

The FastMCP standalone server uses stdio transport for MCP communication:

```python
from mcp_starter.fastmcp_server import create_mcp_server, run

# Create a server with default configuration
mcp = create_mcp_server()

# Or customize the server
mcp = create_mcp_server(
    name="My MCP Server",
    instructions="Use these tools to perform calculations.",
)

# Run the server
run()
```

Or run from the command line:

```bash
mcp-fastmcp
```

### FastAPI + FastMCP Server

The FastAPI server provides HTTP-based MCP communication with full middleware support:

```python
from mcp_starter.fastapi_fastmcp_server import create_app, run

# Create app with authentication
app = create_app(auth_token="your-secret-token")

# Or create app without authentication
app = create_app()

# Run the server
run(host="0.0.0.0", port=8000)
```

Or run from the command line:

```bash
# Without authentication
mcp-fastapi

# With authentication (using environment variable)
export AUTH_TOKEN=your-secret-token
mcp-fastapi
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_NAME` | Name of the MCP server | "FastMCP Starter" / "FastAPI + FastMCP Starter" |
| `AUTH_TOKEN` | Authentication token for middleware | None (auth disabled) |
| `HOST` | Host to bind the FastAPI server | "0.0.0.0" |
| `PORT` | Port for the FastAPI server | 8000 |
| `ENVIRONMENT` | Environment name (development/production) | "development" |
| `DEBUG` | Enable debug mode | "false" |

## Middleware Configuration

### Authentication Middleware

The built-in authentication middleware supports Bearer token authentication:

```python
from mcp_starter.fastapi_fastmcp_server import create_app
from mcp_starter.middleware import AuthMiddleware

# Using the create_app function
app = create_app(auth_token="secret-token")

# Or add middleware manually
from fastapi import FastAPI
app = FastAPI()
app.add_middleware(
    AuthMiddleware,
    token="secret-token",
    header_name="Authorization",
    token_prefix="Bearer",
    exclude_paths=["/health", "/docs"],
)
```

### Custom Middleware

You can add custom middleware to the FastAPI server:

```python
from mcp_starter.fastapi_fastmcp_server import create_app

# Add custom middleware using the additional_middleware parameter
app = create_app(
    auth_token="secret-token",
    additional_middleware=[
        (YourCustomMiddleware, {"param1": "value1"}),
        (AnotherMiddleware, {"setting": True}),
    ],
)
```

### CORS Configuration

CORS is enabled by default for the FastAPI server. You can customize it:

```python
from mcp_starter.fastapi_fastmcp_server import create_app

# Custom CORS origins
app = create_app(
    cors_origins=["http://localhost:3000", "https://myapp.com"],
)

# Disable CORS
app = create_app(enable_cors=False)
```

## API Endpoints (FastAPI Server)

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check endpoint |
| `/mcp/*` | FastMCP HTTP endpoints |
| `GET /docs` | Swagger UI documentation |
| `GET /redoc` | ReDoc documentation |

## Sample Tools

The starter includes sample tools for demonstration:

### Calculator Tools

```python
# Available operations
add(a: float, b: float) -> float
subtract(a: float, b: float) -> float
multiply(a: float, b: float) -> float
divide(a: float, b: float) -> float
```

### Greeting Tool

```python
greet(name: str, greeting: str = "Hello") -> str
```

## Sample Resources

### Server Configuration

```
config://server
```

Returns server configuration including name, version, environment, and debug status.

### Server Info

```
info://server
```

Returns server information including Python version, platform, and timestamp.

## Extending the Starter

### Adding Custom Tools

```python
from mcp_starter.fastmcp_server import create_mcp_server

mcp = create_mcp_server()

@mcp.tool()
def my_custom_tool(param: str) -> str:
    """My custom tool description."""
    return f"Result: {param}"
```

### Adding Custom Resources

```python
from mcp_starter.fastmcp_server import create_mcp_server

mcp = create_mcp_server()

@mcp.resource("custom://resource")
def my_resource() -> dict:
    """My custom resource."""
    return {"key": "value"}
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=mcp_starter
```

### Linting

```bash
# Run ruff linter
ruff check src tests

# Auto-fix issues
ruff check --fix src tests
```

## Project Structure

```
mcp-starter/
├── src/
│   └── mcp_starter/
│       ├── __init__.py
│       ├── fastmcp_server/          # FastMCP standalone server
│       │   ├── __init__.py
│       │   └── main.py
│       ├── fastapi_fastmcp_server/  # FastAPI + FastMCP server
│       │   ├── __init__.py
│       │   └── main.py
│       ├── middleware/              # Middleware components
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── auth.py
│       ├── tools/                   # Sample MCP tools
│       │   ├── __init__.py
│       │   ├── calculator.py
│       │   └── greeting.py
│       └── resources/               # Sample MCP resources
│           ├── __init__.py
│           ├── config.py
│           └── info.py
├── tests/
│   ├── __init__.py
│   ├── test_tools.py
│   ├── test_greeting.py
│   ├── test_resources.py
│   ├── test_middleware.py
│   ├── test_fastmcp_server.py
│   └── test_fastapi_server.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## License

MIT License - see [LICENSE](LICENSE) for details.
