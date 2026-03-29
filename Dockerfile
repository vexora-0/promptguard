FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files (repo root -> /app, so promptguard/ becomes /app/promptguard/)
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    "fastapi>=0.115.0" \
    "pydantic>=2.0.0" \
    "uvicorn[standard]>=0.24.0" \
    "requests>=2.31.0" \
    "openai>=1.0.0"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Set Python path so imports work
ENV PYTHONPATH="/app"

# Run server
CMD ["uvicorn", "promptguard.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
