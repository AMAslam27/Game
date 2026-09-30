# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry

# Install dependencies first (better layer caching): this layer only
# rebuilds when pyproject.toml / poetry.lock change, not on every code edit.
# The cache mount persists downloaded wheels (incl. the large CUDA packages)
# across builds, so only the *first* build pays the full download cost.
COPY pyproject.toml poetry.lock* ./
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install --only main --no-root

COPY . .

ENTRYPOINT ["python", "runner.py"]
CMD []