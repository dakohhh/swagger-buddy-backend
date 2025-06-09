# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

# Set build arguments and environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# Install system build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${POETRY_HOME}/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/poetry \
    poetry config installer.max-workers 10 && \
    poetry install --no-interaction --no-root --only main && \
    poetry export -f requirements.txt --output requirements.txt

# Copy application files to builder stage
COPY ./migrations ./migrations
COPY ./settings ./settings
COPY ./app ./app
COPY ./alembic.ini ./alembic.ini
COPY ./entrypoint.sh ./entrypoint.sh

# Stage 2: Runtime
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHON_ENV=production

# Install runtime system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to non-root user
RUN useradd -m -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy dependencies from builder and install them
COPY --from=builder /app/requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files from builder
COPY --from=builder /app/migrations ./migrations
COPY --from=builder /app/settings ./settings
COPY --from=builder /app/alembic.ini ./alembic.ini
COPY --from=builder /app/entrypoint.sh ./entrypoint.sh

# Copy application code from builder
COPY --from=builder --chown=appuser:appuser /app/app ./app

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 4000

# Command to run the application
ENTRYPOINT [ "./entrypoint.sh" ]
