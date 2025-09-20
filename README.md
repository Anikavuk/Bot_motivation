# Установка приложения в Windows без pip

1. Откройте PowerShell с правами администратора и наберите:  
   `irm https://astral.sh/uv/install.ps1 | iex`  
2. Проверить установлен uv:  
   `uv --version`  
   _Должно выйти uv 0.8.18 (c4c47814a 2025-09-17)_  
3. Добавление uv в PATH:  
3.1. После установки uv, если команда uv не распознаётся, нужно добавить путь к uv в переменную окружения PATH.  
Найдите расположение установленного uv, обычно:  
`C:\Users\<пользователь>\.uv\bin`  
3.2. Добавьте этот путь в системный PATH:  
Откройте Панель управления → Система → Дополнительные параметры системы → Переменные среды.  
В разделе «Переменные пользователя» найдите Path → Изменить → Добавить новый путь -> вставьте путь к uv  
(C:\Users\<пользователь>\.uv\bin). Сохраните изменения.  
Перезапустите PowerShell или терминал, чтобы изменения вступили в силу.
4. Рекомендация (можно пропустить) по проверке uv в PATH после установки на Windows:  
4.1. Откройте новый экземпляр PowerShell или командной строки (чтобы обновились переменные среды).  
4.2. Выполните команду:  
`uv --version`  
4.3. Если uv установился и путь в PATH корректен, вы увидите вывод с версией uv, например:  
`uv 0.8.18 (c4c47814a 2025-09-17)`  
4.4. Если Windows не распознаёт команду uv и выдаёт ошибку типа:  
'uv' не является внутренней или внешней командой, выполняемой программой или пакетным файлом.  
Значит, путь не добавлен или добавлен неверно. Проверьте переменную PATH командой:  
`echo $Env:PATH`  
Убедитесь, что там присутствует путь к папке с uv.exe (обычно C:\Users\<пользователь>\.uv\bin).
5. Проверьте в PowerShell список установленных версий Python через uv командой:  
   `uv python list`  
6. Спулльте проект в локальную папку:  
   4.1. Создайте папку для проекта  
   4.2. Зайдите в IDE (желательно в PyCharm) в папку проекта  
   4.3. В терминале наберите команды:  
   `git init`  
   `git remote add origin https://github.com/Asenim/prediction-app`  
   `git fetch origin`  
   `git checkout -b origin/main`  
   `git pull origin main`  
   _Должны появиться все папки приложения_  
7. Создайте окружение с uv:  
   `uv venv`  
8. Активируйте окружение:  
8.1. Используется в cmd.exe (командная строка Windows)  
`.\.venv\Scripts\activate.bat`  
8.2. Используется в PowerShell:  
`.\.venv\Scripts\Activate.ps1`
9. Установить зависимости:  
   `uv sync`  
10. Проверка  
    `uv pip list`  
11. В PyCharm добавьте окружение  
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
3. Установка uv через pip. Откройте PowerShell или cmd (лучше с правами администратора) и выполните команду:    
   `pip install uv`
4. Проверьте установлен uv:  
   `uv --version`  
   _Должно выйти uv 0.8.18 (c4c47814a 2025-09-17)_
5. В проекте терминала PyCharm создайте окружение:  
   `uv venv .venv`
6. Активируйте окружение:  
6.1. Используется в cmd.exe (командная строка Windows)  
`.\.venv\Scripts\activate.bat`  
6.2. Используется в PowerShell:  
`.\.venv\Scripts\Activate.ps1`
7. Установить зависимости:  
   `uv sync`
8. Проверка  
   `uv pip list`
9. В PyCharm добавьте окружение  
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
