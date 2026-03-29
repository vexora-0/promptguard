FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY promptguard/ /app/promptguard/
COPY README.md /app/

# Install Python dependencies
RUN pip install --no-cache-dir \
    "fastapi>=0.115.0" \
    "pydantic>=2.0.0" \
    "uvicorn[standard]>=0.24.0" \
    "requests>=2.31.0" \
    "openai>=1.0.0"

# HF Spaces expects port 7860 by default, but we declared app_port: 8000
EXPOSE 8000

# Set Python path so imports work
ENV PYTHONPATH="/app"

# Run server - bind to 0.0.0.0 for HF Spaces
CMD ["python", "-m", "uvicorn", "promptguard.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
