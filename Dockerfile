# ---- Build stage ----
FROM python:3.14-slim AS builder

# Install uv (pinned version, copied from official image = fast, no curl needed)
COPY --from=ghcr.io/astral-sh/uv:0.12.7 /uv /uvx /bin/

# Enable bytecode compilation for faster startup, and use copy mode
# (avoids issues with symlinks across the two stages)
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies first, using the lockfile — this layer only
# rebuilds when pyproject.toml/uv.lock change, not on every code change
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Now copy the actual project code and install it too
COPY --parents app frontend/dist pyproject.toml uv.lock /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# ---- Runtime stage ----
FROM python:3.14-slim AS runtime

# Create non-root user
RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

# Allow app to write logs to /output folder
RUN mkdir -p /app/output && chown app:app /app/output

# Copy just the built virtual environment and app code — no uv, no build tools
COPY --from=builder --chown=app:app /app /app

# Put the venv on PATH so `python`/entrypoint scripts resolve correctly
ENV PATH="/app/.venv/bin:$PATH"

USER app

ENTRYPOINT ["python", "-m", "fastapi", "run"]
