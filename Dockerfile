FROM ghcr.io/astral-sh/uv:python3.13-trixie AS builder

WORKDIR /build

# Копируем файл проекта с зависимостями
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Активируем виртуальное окружение и устанавливаем зависимости через uv sync
RUN uv sync --locked

# --- Финальный образ ---
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y make

COPY --from=builder /build/.venv .venv
COPY . .

EXPOSE 8000
