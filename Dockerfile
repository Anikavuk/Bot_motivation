FROM postgres:15.2

# Устанавливаем переменные окружения по умолчанию (опционально — можно переопределить при запуске)
ENV DB_USER=prediction_user
ENV DB_PASSWORD=save
ENV POSTGRES_DB=prediction_bot

# Порт 5432 уже открыт в базовом образе, но можно явно указать:
EXPOSE 5432
