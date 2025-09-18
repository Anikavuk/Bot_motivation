# Установка приложения в Windows без pip

1. Откройте PowerShell с правами администратора и наберите:
   `powershell -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"`
2. Проверить установлен uv:
   `uv --version`
   _Должно выйти uv 0.8.18 (c4c47814a 2025-09-17)_
3. Проверьте список установленных версий Python через uv командой:
   `uv python list`
4. Спулльте проект в локальную папку:
   4.1. Создайте папку для проекта
   4.2. Зайдите в IDE (желательно в PyCharm) в папку проекта
   4.3. В терминале наберите команды:
   `git init`
   `git remote add origin https://github.com/Asenim/prediction-app`
   `git fetch origin`
   `git checkout -b origin/main`
   `git pull origin main`
   _Должны появиться все папки приложения_
5. Создайте окружение с uv:
   `uv venv`
6. Активируйте окружение:
   `.\.venv\Scripts\Activate.ps1`
7. Установить зависимости:
   `uv sync`
8. Проверка
   `uv pip list`
9. В PyCharm добавьте окружение
   `File -> Settings -> Project: твой проект -> Python  Interpreter -> Add Interpreter`
   _В нижнем правом углу должно появиться Python c вашей версией и в скобках ваше окружение_

# Установка приложения в Windows с помощью pip

1. Создайте папку для проекта в PyCharm
2. В терминале наберите команды:
   `git init`
   `git remote add origin https://github.com/Asenim/prediction-app`
   `git fetch origin`
   `git checkout -b origin/main`
   `git pull origin main`
   _Должны появиться все папки приложения_
3. В cmd от имени администратора наберите:
   `pip install uv`
4. В проекте терминала PyCharm создайте окружение:
   `uv venv .venv`
5. Активируйте окружение:
   `.\.venv\Scripts\Activate.ps1`
6. Установить зависимости:
   `uv sync`
7. Проверка
   `uv pip list`
8. В PyCharm добавьте окружение
   `File -> Settings -> Project: твой проект -> Python  Interpreter -> Add Interpreter`
   _В нижнем правом углу должно появиться Python c вашей версией и в скобках ваше окружение_

# Создайте в корневой папке проекта файл .env и скопируйте в него данные:

`DB_NAME=prediction_bot`
`DB_USER=prediction_user`
`DB_PASSWORD=save`
`DB_HOST=localhost`
`DB_PORT=5433`
`DB_ECHO=True`

# Запустите Docker

`docker-compose -f docker-compose.dev.yaml up -d`

Подключитесь к базе данных в контейнере:

`docker exec -it prediction_bot psql -U prediction_user -d prediction_db`

# Команда для миграций

`alembic revision --autogenerate -m "Проверка"`

## Применить миграцию:

`alembic upgrade head`
