# ==============================================================================
# Stage 1: Build & Dependencies stage
# ==============================================================================
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# ==============================================================================
# Stage 2: Final Slim Runtime Stage
# ==============================================================================
FROM python:3.11-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH \
    DJANGO_SETTINGS_MODULE=resumeforge.settings

# Install runtime dependencies for psycopg2 and pdf processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application source code
COPY . .

# Expose port 8000 for web service
EXPOSE 8000

# Default entrypoint runs production gunicorn
CMD ["gunicorn", "resumeforge.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
