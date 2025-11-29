FROM ghcr.io/astral-sh/uv:python3.13-trixie AS builder

WORKDIR /build

# Копируем файл проекта с зависимостями
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Активируем виртуальное окружение и устанавливаем зависимости через uv sync
RUN uv sync --locked

# --- Финальный образ ---
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS runtime

WORKDIR /app

RUN apt update && apt install -y make

COPY --from=builder /build/.venv .venv
COPY . .

EXPOSE 8000
