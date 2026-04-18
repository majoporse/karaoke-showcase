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
# Set Hugging Face cache location explicitly
ENV HF_HOME=/app/.cache/huggingface

# ================================
# STAGE 2: Builder
# ================================
FROM base AS builder

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtualenv
RUN uv sync --frozen --no-install-project

# ================================
# STAGE 3: Runtime
# ================================
FROM base AS runtime

RUN mkdir -p /app/.cache/huggingface && \
    chown -R appuser:appuser /app

# Copy the entire app directory (including .venv and pre-downloaded models)
COPY --from=builder --chown=appuser:appuser /app /app

COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Run the application using uv
CMD ["uv", "run", "--frozen", "python", "main.py"]