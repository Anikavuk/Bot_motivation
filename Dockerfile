FROM ghcr.io/astral-sh/uv:python3.13-trixie AS builder

WORKDIR /src

# Копируем файл проекта с зависимостями
COPY pyproject.toml uv.lock ./

# Создаем виртуальное окружение Python 3.11
RUN uv venv --python 3.13 /venv

# Активируем виртуальное окружение и устанавливаем зависимости через uv sync
uv sync --locked

# --- Финальный образ ---
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y make

COPY --from=builder /.venv /.venv
COPY ../.. .

EXPOSE 8000
