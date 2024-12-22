# Core Dependencies Overview

This document covers the core dependencies included in all generated projects.

## Table of Contents

- [structlog](#structlog)
- [Sentry SDK](#sentry-sdk)
- [django-environ](#django-environ)
- [Pydantic](#pydantic)
- [HTTPX](#httpx)
- [orjson](#orjson)
- [Rich](#rich)

---

## structlog

Structured logging for Python that produces machine-readable log output.

**Documentation:** https://www.structlog.org/

**Usage:**

```python
from {{cookiecutter.package_name}}.logging import get_logger

logger = get_logger()

# Basic logging
logger.info("User logged in", user_id=123, ip_address="192.168.1.1")

# Bind context for subsequent logs
logger = logger.bind(request_id="abc-123")
logger.info("Processing request")
logger.warning("Rate limit approaching", current=95, limit=100)

# Log exceptions with context
try:
    risky_operation()
except Exception:
    logger.exception("Operation failed", operation="risky_operation")
```

**Output:**
```
2024-01-15T10:30:45.123456Z [info     ] User logged in                 user_id=123 ip_address=192.168.1.1
```

---

## Sentry SDK

Error tracking and performance monitoring.

**Documentation:** https://docs.sentry.io/platforms/python/

**Configuration:**

Set these environment variables:
```shell
SENTRY_DSN=https://your-key@sentry.io/project-id
ENVIRONMENT=production
```

**Usage:**

```python
import sentry_sdk

# Capture an exception manually
try:
    dangerous_operation()
except Exception as e:
    sentry_sdk.capture_exception(e)

# Add context to errors
sentry_sdk.set_user({"id": user.id, "email": user.email})
sentry_sdk.set_tag("feature", "checkout")
sentry_sdk.set_context("order", {"id": order.id, "total": order.total})

# Capture a message
sentry_sdk.capture_message("Something noteworthy happened")

# Create a performance transaction
with sentry_sdk.start_transaction(op="task", name="process_order"):
    with sentry_sdk.start_span(op="db", description="fetch order"):
        order = fetch_order()
    with sentry_sdk.start_span(op="http", description="charge payment"):
        charge_payment(order)
```

---

## django-environ

Environment variable parsing with type casting.

**Documentation:** https://django-environ.readthedocs.io/

**Usage:**

```python
from environ import Env

env = Env()

# Read environment variables with defaults and type casting
DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY")
DATABASE_URL = env.db("DATABASE_URL")  # Parses database URLs
REDIS_URL = env.cache_url("REDIS_URL")  # Parses cache URLs
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])
MAX_CONNECTIONS = env.int("MAX_CONNECTIONS", default=100)
API_TIMEOUT = env.float("API_TIMEOUT", default=30.0)

# Read from .env file
Env.read_env(".env")
```

**Example `.env` file:**
```shell
DEBUG=true
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
ALLOWED_HOSTS=example.com,www.example.com
```

---

## Pydantic

Data validation using Python type annotations.

**Documentation:** https://docs.pydantic.dev/

**Usage:**

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    created_at: datetime
    tags: list[str] = []

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.strip()

# Validation happens automatically
user = User(
    id=1,
    name="John Doe",
    email="john@example.com",
    created_at=datetime.now(),
)

# Convert to dict/JSON
user_dict = user.model_dump()
user_json = user.model_dump_json()

# Parse from dict/JSON
user = User.model_validate({"id": 1, "name": "Jane", "email": "jane@example.com", "created_at": "2024-01-15T10:00:00"})
user = User.model_validate_json('{"id": 1, "name": "Jane", "email": "jane@example.com", "created_at": "2024-01-15T10:00:00"}')
```

---

## HTTPX

Modern async-capable HTTP client.

**Documentation:** https://www.python-httpx.org/

**Usage:**

```python
import httpx

# Synchronous requests
response = httpx.get("https://api.example.com/users")
response.raise_for_status()
data = response.json()

# With parameters and headers
response = httpx.get(
    "https://api.example.com/search",
    params={"q": "python", "limit": 10},
    headers={"Authorization": "Bearer token"},
    timeout=30.0,
)

# POST with JSON body
response = httpx.post(
    "https://api.example.com/users",
    json={"name": "John", "email": "john@example.com"},
)

# Using a client for connection pooling
with httpx.Client(base_url="https://api.example.com") as client:
    users = client.get("/users").json()
    user = client.get("/users/1").json()

# Async requests
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com/users")
    data = response.json()
```

---

## orjson

Fast JSON library (10x faster than stdlib json).

**Documentation:** https://github.com/ijl/orjson

**Usage:**

```python
import orjson
from datetime import datetime
from uuid import UUID

# Serialize to bytes (not str!)
data = {"name": "John", "created": datetime.now(), "id": UUID("12345678-1234-5678-1234-567812345678")}
json_bytes = orjson.dumps(data)  # Returns bytes

# Options for pretty printing and sorting
json_bytes = orjson.dumps(
    data,
    option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS,
)

# Deserialize
data = orjson.loads(json_bytes)
data = orjson.loads('{"name": "John"}')  # Also accepts str

# Custom serialization
def default(obj):
    if isinstance(obj, CustomClass):
        return obj.to_dict()
    raise TypeError

json_bytes = orjson.dumps(data, default=default)
```

---

## Rich

Beautiful terminal output with colors, tables, progress bars, and more.

**Documentation:** https://rich.readthedocs.io/

**Usage:**

```python
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel

console = Console()

# Pretty print with syntax highlighting
print("[bold red]Error:[/bold red] Something went wrong")
print({"name": "John", "scores": [95, 87, 92]})  # Auto-formatted dicts

# Tables
table = Table(title="Users")
table.add_column("ID", style="cyan")
table.add_column("Name", style="magenta")
table.add_column("Email", style="green")
table.add_row("1", "John Doe", "john@example.com")
table.add_row("2", "Jane Smith", "jane@example.com")
console.print(table)

# Progress bars
for item in track(range(100), description="Processing..."):
    process(item)

# Panels and formatting
console.print(Panel("Important message", title="Notice", border_style="yellow"))

# Logging handler
from rich.logging import RichHandler
import logging
logging.basicConfig(handlers=[RichHandler()])
```
{%- if cookiecutter.async %}

---

## uvloop

Ultra-fast asyncio event loop (2-4x faster than default).

**Documentation:** https://uvloop.readthedocs.io/

**Usage:**

uvloop is automatically configured when available. For manual setup:

```python
import asyncio
import uvloop

# Option 1: Set as default policy
uvloop.install()

# Option 2: Create a specific loop
async def main():
    await some_async_function()

uvloop.run(main())
```
{%- endif %}
