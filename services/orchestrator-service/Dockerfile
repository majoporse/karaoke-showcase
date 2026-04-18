FROM ghcr.io/astral-sh/uv:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    nodejs \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

WORKDIR /app


# 1. Change ownership of the workdir BEFORE syncing
RUN chown appuser:appuser /app
USER appuser

# 2. Copy dependency files as the appuser
COPY --chown=appuser:appuser pyproject.toml uv.lock .python-version ./
COPY --chown=appuser:appuser ./clients ./clients

# 3. Install dependencies 
# Running this as 'appuser' ensures the venv is owned by the user running the app
RUN uv sync --frozen 

# 4. Copy the rest of the application code
COPY --chown=appuser:appuser . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use --frozen to skip the startup check entirely
CMD ["uv", "run", "--frozen", "python", "main.py"]
