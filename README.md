# Содержание файла .env:

`DB_NAME=prediction_bot`

`DB_USER=prediction_user`

`DB_PASSWORD=save`

`DB_HOST=localhost`

`DB_PORT=5433`

`DB_ECHO=True`

# Создание и активирование виртуально окружения:

## Установи uv:

`pip install uv`

## Рекомендуемый способ установки для Windows

`iwr https://astral.sh/uv/install.ps1 -useb | iex`

## Проверь версию:

`uv --version`

## Создай виртуальное окружение в папке .venv

`uv venv`

## Активировать среду

`.venv\Scripts\activate`

## Установи зависимости:

`uv sync`

# Docker

## Запуск:

`docker-compose -f docker-compose.dev.yaml up -d`

## Далее подключение к БД в контейнере можно делать примерно так:

`docker exec -it prediction_bot psql -U prediction_user -d prediction_db`

# Команда для миграций

## Запусти докер, и набери команду:

`alembic revision --autogenerate -m "Проверка"`

## Примени миграцию:

`alembic upgrade head`
