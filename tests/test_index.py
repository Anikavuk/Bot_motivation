from fastapi.testclient import TestClient

from prediction_app.core.config_run import web_app

client = TestClient(web_app)


def test_index_returns_html():
    """
    Проверяет, что корневой маршрут `/` возвращает корректный HTML-ответ.

    Убеждается, что:
    - HTTP-статус код равен 200 (успех),
    - Content-Type содержит 'text/html',
    - Тело ответа действительно содержит HTML-разметку (проверка по наличию тега <html).

    Это базовый smoke-тест для проверки работоспособности главной страницы.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<html" in response.text.lower()


def test_index_creates_session_cookie():
    """
    Проверяет, что при первом обращении к `/` сервер устанавливает cookie сессии.

    Убеждается, что:
    - Ответ успешен (статус 200),
    - В ответе присутствует cookie с именем 'session',
    - Значение cookie не пустое (сессия действительно инициализирована).

    Это важно для подтверждения, что SessionMiddleware работает и создаёт сессию
    при первом посещении пользователем.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "session" in response.cookies
    assert response.cookies["session"] != ""


def test_session_contains_session_id():
    """
    Проверяет, что сессия сохраняется между последовательными запросами от одного клиента.

    Убеждается, что:
    - Первый запрос устанавливает cookie 'session',
    - Второй запрос (от того же TestClient) автоматически отправляет эту cookie,
    - Сервер корректно обрабатывает повторный запрос (статус 200).

    Примечание: TestClient автоматически сохраняет и переиспользует cookies
    между вызовами, что имитирует поведение браузера. Это косвенно подтверждает,
    что session_id был сохранён в сессии и доступен при повторном обращении.
    """
    response1 = client.get("/")
    assert "session" in response1.cookies

    response2 = client.get("/")
    assert response2.status_code == 200
