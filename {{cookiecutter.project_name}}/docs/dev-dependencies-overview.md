# Development Dependencies Overview

This document covers the development and testing dependencies included in this project.

## Table of Contents

- [pytest](#pytest)
- [Ruff](#ruff)
- [mypy](#mypy)
- [Hypothesis](#hypothesis)
- [time-machine](#time-machine)
- [RESPX](#respx)
- [Faker](#faker)

---

## pytest

Testing framework with powerful fixtures and plugins.

**Documentation:** https://docs.pytest.org/

**Running tests:**

```shell
# Run all tests
uv run pytest

# Run specific file/directory
uv run pytest tests/test_module.py
uv run pytest tests/unit/

# Run specific test
uv run pytest tests/test_module.py::test_function
uv run pytest tests/test_module.py::TestClass::test_method

# Run with markers
uv run pytest -m "not slow"
uv run pytest -m "integration"

# Parallel execution
uv run pytest -n auto

# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x

# Show local variables in tracebacks
uv run pytest -l
```

**Writing tests:**

```python
import pytest

def test_simple():
    assert 1 + 1 == 2

class TestUser:
    def test_creation(self):
        user = User(name="John")
        assert user.name == "John"

    @pytest.mark.parametrize(("input", "expected"), [
        ("hello", "HELLO"),
        ("World", "WORLD"),
    ])
    def test_uppercase(self, input: str, expected: str):
        assert input.upper() == expected

@pytest.fixture
def user():
    return User(name="Test User")

def test_with_fixture(user):
    assert user.name == "Test User"
```

---

## Ruff

Extremely fast Python linter and formatter.

**Documentation:** https://docs.astral.sh/ruff/

**Commands:**

```shell
# Check for issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .
```

**Configuration (in pyproject.toml):**

```toml
[tool.ruff]
line-length = {{cookiecutter.format_line_length}}
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
ignore = ["E501"]  # Line too long

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # Allow assert in tests
```

---

## mypy

Static type checker for Python.

**Documentation:** https://mypy.readthedocs.io/

**Commands:**

```shell
# Check types
uv run mypy src/

# Check specific file
uv run mypy src/module.py

# Show error codes
uv run mypy src/ --show-error-codes

# Generate HTML report
uv run mypy src/ --html-report mypy-report
```

**Common type patterns:**

```python
from typing import Optional, Union, TypeVar, Generic
from collections.abc import Callable, Sequence

def greet(name: str) -> str:
    return f"Hello, {name}"

def process(items: list[int]) -> dict[str, int]:
    return {"sum": sum(items), "count": len(items)}

def maybe_value(value: str | None) -> str:
    return value or "default"

T = TypeVar("T")

def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None
```

---

## Hypothesis

Property-based testing that generates test cases automatically.

**Documentation:** https://hypothesis.readthedocs.io/

**Usage:**

```python
from hypothesis import given, strategies as st, assume, settings

@given(st.integers(), st.integers())
def test_addition_commutative(a: int, b: int):
    assert a + b == b + a

@given(st.lists(st.integers()))
def test_sorted_list_is_sorted(items: list[int]):
    result = sorted(items)
    assert all(result[i] <= result[i + 1] for i in range(len(result) - 1))

@given(st.text(min_size=1))
def test_string_not_empty(s: str):
    assume(s.strip())  # Skip empty/whitespace strings
    assert len(s) > 0

# Custom strategies
@given(st.builds(User, name=st.text(min_size=1), age=st.integers(min_value=0, max_value=150)))
def test_user_creation(user: User):
    assert user.age >= 0

# Adjust settings
@settings(max_examples=1000, deadline=None)
@given(st.binary())
def test_expensive_operation(data: bytes):
    process(data)
```

---

## time-machine

Fast, powerful time mocking.

**Documentation:** https://github.com/adamchainz/time-machine

**Usage:**

```python
import time_machine
from datetime import datetime, timezone

@time_machine.travel("2024-01-15 10:30:00")
def test_with_fixed_time():
    now = datetime.now()
    assert now.year == 2024
    assert now.month == 1
    assert now.day == 15

@time_machine.travel("2024-01-15 10:30:00", tick=False)
def test_time_frozen():
    start = datetime.now()
    time.sleep(1)
    end = datetime.now()
    assert start == end  # Time didn't move

def test_with_context_manager():
    with time_machine.travel("2024-06-01"):
        assert datetime.now().month == 6

# Travel to specific timezone
@time_machine.travel(datetime(2024, 1, 15, tzinfo=timezone.utc))
def test_utc_time():
    pass

# Use as fixture
@pytest.fixture
def frozen_time():
    with time_machine.travel("2024-01-15") as traveller:
        yield traveller

def test_with_traveller(frozen_time):
    assert datetime.now().day == 15
    frozen_time.shift(days=1)
    assert datetime.now().day == 16
```

---

## RESPX

Mock HTTPX requests in tests.

**Documentation:** https://lundberg.github.io/respx/

**Usage:**

```python
import httpx
import respx
from respx import MockRouter

@respx.mock
def test_api_call():
    respx.get("https://api.example.com/users/1").respond(
        json={"id": 1, "name": "John"}
    )

    response = httpx.get("https://api.example.com/users/1")
    assert response.json()["name"] == "John"

@respx.mock
def test_with_patterns():
    # Match any user ID
    respx.get(url__regex=r"https://api.example.com/users/\d+").respond(
        json={"id": 1, "name": "User"}
    )

    # Match with query params
    respx.get("https://api.example.com/search", params={"q": "test"}).respond(
        json={"results": []}
    )

@respx.mock
async def test_async_call():
    respx.get("https://api.example.com/data").respond(json={"key": "value"})

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        assert response.json()["key"] == "value"

# Using as fixture
@pytest.fixture
def mocked_api(respx_mock: MockRouter):
    respx_mock.get("https://api.example.com/health").respond(200)
    return respx_mock

def test_with_fixture(mocked_api: MockRouter):
    mocked_api.get("https://api.example.com/users").respond(json=[])
    response = httpx.get("https://api.example.com/users")
    assert response.json() == []
```

---

## Faker

Generate fake data for testing.

**Documentation:** https://faker.readthedocs.io/

**Usage:**

```python
from faker import Faker

fake = Faker()

# Basic data
name = fake.name()  # "John Smith"
email = fake.email()  # "john.smith@example.com"
address = fake.address()  # Full address
phone = fake.phone_number()  # Phone number

# Specific data types
fake.uuid4()  # UUID
fake.date_of_birth()  # Date
fake.credit_card_number()  # Credit card
fake.ipv4()  # IP address
fake.url()  # URL
fake.text(max_nb_chars=200)  # Lorem ipsum text

# Localized data
fake_de = Faker("de_DE")
fake_de.name()  # German name

# Reproducible results
Faker.seed(12345)
fake.name()  # Always same result with same seed

# With pytest fixture
@pytest.fixture
def fake():
    return Faker()

def test_user_creation(fake):
    user = User(name=fake.name(), email=fake.email())
    assert "@" in user.email
```

**With factory_boy:**

```python
import factory
from faker import Faker

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    created_at = factory.LazyFunction(fake.date_time_this_year)
```

---

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [Real Python Tutorials](https://realpython.com/)
- [Python Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
