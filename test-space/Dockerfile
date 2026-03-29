FROM python:3.11-slim

RUN useradd -m -u 1000 user
RUN pip install --no-cache-dir fastapi uvicorn

COPY --chown=user app.py /app/app.py

USER user
WORKDIR /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
