# Lambda API Dockerfile
# Multi-stage build for AWS Lambda Python runtime

FROM amazon/aws-lambda-python:3.12 AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /var/task

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock README.md ./

# Install dependencies without the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY src ./src

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Runtime stage
FROM amazon/aws-lambda-python:3.12 AS runtime

# Copy installed packages and source from builder
COPY --from=builder /var/task /var/task

# Set Python path to include virtual environment and source
ENV PYTHONPATH="/var/task/.venv/lib/python3.12/site-packages:/var/task/src"

# Lambda handler
CMD ["{{cookiecutter.package_name}}_api.lambda_handler.handler"]
