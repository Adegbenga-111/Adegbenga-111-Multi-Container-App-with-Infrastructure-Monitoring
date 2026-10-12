# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build-essential for C-extensions, then clean apt cache to save space
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment and install packages
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ==========================================
# STAGE 2: Final Production Image
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Create a non-root system user for security
RUN useradd -u 1001 -m appuser

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application files and update ownership to non-root user
COPY --chown=appuser:appuser . .

# Switch to the non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check (Swapped from 'requests' module to standard library 'urllib.request')
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

