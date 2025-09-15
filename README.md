# Содержание файла .env:

`DB_NAME=prediction_bot
DB_USER=prediction_user
DB_PASSWORD=save
DB_HOST=localhost
DB_PORT=5433
DB_ECHO=True`

# Создание и активирование виртуально окружения:

## Установи uv:

`pip install uv

## Проверь версию:

uv --version`

## Создай виртуальное окружение в папке .venv

`uv venv`

## Установи зависимости:

`uv sync`

## Активировать среду

`.venv\Scripts\activate`

# Docker

## Запуск:

`docker-compose -f docker-compose.dev.yaml up -d`

## Далее подключение к БД в контейнере можно делать примерно так:

`docker exec -it prediction_bot psql -U prediction_user -d prediction_db`
