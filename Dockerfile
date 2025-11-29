
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS runtime

WORKDIR /app

RUN apt update && apt install -y make

COPY . .

RUN uv sync --locked

EXPOSE 8000
