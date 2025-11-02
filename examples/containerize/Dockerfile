# This is a multi-stage build.
# Using multi-stage allows for a nimble image generation
# and you can use this straight into production.
#
# REMINDER: make sure to double check, verify, and test the
# base image that you will be using. 
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

# Enable bytecode compilation for better startup performance
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies in a virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy application code (excluding .venv)
COPY . .

# Copy any other necessary files
# COPY ./config ./config

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Final stage - minimal runtime image
FROM python:3.14-slim-bookworm

# Create non-root user for security
RUN groupadd -r appuser && \
    useradd -r -g appuser -m -s /bin/bash appuser && \
    mkdir -p /app && chown -R appuser:appuser /app

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code
COPY --from=builder --chown=appuser:appuser /app /app

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Security: Run as non-root user
USER appuser
    
# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Expose port
EXPOSE 8000

# This sample uses uvicorn with production settings.
# REMINDERS: 
# Change "airblog" to the name of your app.py if you are going to adopt this Dockerfile as is.
# If you are exposing a different port, make sure to update EXPOSE and --port as well.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers", "--forwarded-allow-ips", "*"]