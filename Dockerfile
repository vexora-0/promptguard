FROM python:3.11-slim

# Create user with UID 1000 (REQUIRED by HF Spaces)
RUN useradd -m -u 1000 user

WORKDIR /app

# Install Python dependencies first (better caching)
RUN pip install --no-cache-dir \
    "fastapi>=0.115.0" \
    "pydantic>=2.0.0" \
    "uvicorn[standard]>=0.24.0" \
    "requests>=2.31.0" \
    "openai>=1.0.0"

# Copy project files with correct ownership
COPY --chown=user promptguard/ /app/promptguard/
COPY --chown=user README.md /app/

# Switch to non-root user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=/app

EXPOSE 7860

CMD ["uvicorn", "promptguard.server.app:app", "--host", "0.0.0.0", "--port", "7860"]
