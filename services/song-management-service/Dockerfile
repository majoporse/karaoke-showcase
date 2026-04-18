# ================================
# STAGE 1: Base
# ================================
FROM ghcr.io/astral-sh/uv:bookworm-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

WORKDIR /app
ENV HOME=/app
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/app/venv
ENV UV_CACHE_DIR=/app/.uv_cache

# ================================
# STAGE 2: Builder
# ================================
FROM base AS builder

# Install build dependencies needed for C extensions like asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY .python-version pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

# ================================
# STAGE 3: Runtime
# ================================
FROM base AS runtime

# Create necessary directories and set ownership of entire /app
RUN mkdir -p /app && \
    chown -R appuser:appuser /app

# Copy virtual environment from builder with correct ownership
COPY --from=builder --chown=appuser:appuser /app /app

# Copy application code with correct ownership
COPY --chown=appuser:appuser . .

# Expose port
EXPOSE 8003

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

# Run the application
CMD ["uv", "run", "--frozen", "python", "main.py"]