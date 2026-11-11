FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/ /app/backend/
COPY docs/ /app/docs/

RUN pip install --no-cache-dir \
    sqlalchemy \
    pydantic \
    pydantic-settings \
    fastapi \
    uvicorn \
    torch \
    psutil \
    pyyaml \
    jinja2 \
    soundfile \
    pydub \
    python-multipart \
    requests \
    httpx

EXPOSE 3900

ENV PYTHONPATH=/app/backend
ENV API_HOST=0.0.0.0
ENV API_PORT=3900

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3900"]
