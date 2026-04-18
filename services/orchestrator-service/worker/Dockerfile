# ================================
# STAGE 1: Base
# ================================
FROM ghcr.io/astral-sh/uv:bookworm-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    nodejs \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

WORKDIR /app
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/app/venv
ENV UV_CACHE_DIR=/app/.uv_cache
ENV HOME=/app

# ================================
# STAGE 2: Builder
# ================================
FROM base AS builder

# Copy all application code (needed for local path dependencies)
COPY pyproject.toml uv.lock .python-version ./
COPY ./clients ./clients

# Install dependencies
RUN uv sync --frozen --no-install-project

# ================================
# STAGE 3: Runtime
# ================================
FROM base AS runtime

# Create necessary directories
RUN mkdir -p /app/venv /app/.uv_cache

# Copy virtual environment from builder
COPY --from=builder /app/venv /app/venv
COPY --from=builder /app/.uv_cache /app/.uv_cache

# Copy application code
COPY . .


# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Run the RQ worker
CMD ["uv", "run", "python", "worker.py"]
