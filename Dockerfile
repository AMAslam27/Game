# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry

# Install dependencies first for better layer caching.
COPY pyproject.toml poetry.lock* ./

RUN --mount=type=cache,target=/root/.cache/pypoetry \
    --mount=type=cache,target=/root/.cache/pip \
    poetry install --only main --no-root

COPY . .

ENTRYPOINT ["python", "runner.py"]
CMD []