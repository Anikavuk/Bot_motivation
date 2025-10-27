FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS builder

WORKDIR /src

# Копируем файл проекта с зависимостями
COPY pyproject.toml uv.lock ./

# Создаем виртуальное окружение Python 3.11
RUN uv venv --python 3.11 /venv

# Активируем виртуальное окружение и устанавливаем зависимости через uv sync
RUN PATH="/venv/bin:$PATH" uv sync --locked

# --- Финальный образ ---
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /venv /venv
COPY . .

ENV PATH="/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
