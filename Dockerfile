FROM python:3.10.8-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN pip install -r requirements.txt

FROM base AS final

COPY . .

CMD uvicorn app:app --host $UVICORN_HOST --port $UVICORN_PORT --workers $UVICORN_MAX_WORKERS