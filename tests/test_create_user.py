import re
import uuid
import pytest
from fastapi.testclient import TestClient

from app.core.config_run import web_app

client = TestClient(web_app)


def test_index_without_session_cookie():
    """Тест загрузки стартовой страницы index без session_uuid"""
    # Отправляем GET запрос к главное странице "/"
    response = client.get("/")
    # Проверяем статус ответа от сервера
    assert response.status_code == 200

    # Проверяем cookie session_id в ответе
    # Получаем значение заголовка Set-Cookie из HTTP-ответа
    set_cookie_header = response.headers.get("set-cookie")
    # Проверяем, что заголовок Set-Cookie присутствует в ответе
    assert set_cookie_header is not None
    # Проверяем, что в значении Set-Cookie содержится строка session_id=
    assert "session_id=" in set_cookie_header
    # Проверяем, что атрибут HttpOnly присутствует (в любом регистре).
    assert "httponly" in set_cookie_header.lower()
    # Проверяем, что установлен атрибут SameSite=Lax.
    assert "samesite=lax" in set_cookie_header.lower()
    # Проверяем, что срок жизни cookie — 31 536 000 секунд.
    assert "max-age=31536000" in set_cookie_header.lower()
    # Проверяем, что cookie будет доступна на всех путях сайта (/).
    assert "path=/" in set_cookie_header.lower()


def test_index_with_existing_session_cookie():
    existing_uuid = str(uuid.uuid4())
    client.cookies.set("session_id", existing_uuid)
    response = client.get("/")
    assert response.status_code == 200

    content = response.text
    # Проверяем, что в шаблон передан наш UUID
    assert existing_uuid in content

    # Проверяем cookie в заголовках ответа
    set_cookie_header = response.headers.get("set-cookie")
    assert set_cookie_header is not None
    assert f"session_id={existing_uuid}" in set_cookie_header
    assert "httponly" in set_cookie_header.lower()
    assert "samesite=lax" in set_cookie_header.lower()

    assert "max-age=31536000" in set_cookie_header.lower()
    assert "path=/" in set_cookie_header.lower()


def test_create_user_with_form_uuid():
    """Если в форме передан session_uuid, он должен использоваться"""
    test_uuid = str(uuid.uuid4())
    client.cookies.set("session_id", test_uuid)

    # Затем вызывай запрос без параметра cookies
    response = client.post("/create_user")

    assert response.status_code == 200
    assert response.cookies.get("session_id") == test_uuid

    # Проверяем, что шаблон получил этот UUID
    assert test_uuid in response.text


def test_create_user_with_cookie_no_form():
    """Если нет данных в форме, но есть cookie — используем значение из cookie"""
    existing_uuid = str(uuid.uuid4())
    client.cookies.set("session_id", existing_uuid)
    response = client.post("/create_user")

    assert response.status_code == 200
    assert response.cookies.get("session_id") == existing_uuid
    assert existing_uuid in response.text


def test_create_user_form_overrides_cookie():
    cookie_uuid = str(uuid.uuid4())
    form_uuid = str(uuid.uuid4())
    client.cookies.set("session_id", cookie_uuid)
    response = client.post(
        "/create_user",
        data={"session_uuid": form_uuid},
    )

    assert response.status_code == 200
    assert response.cookies.get("session_id") == form_uuid
    assert form_uuid in response.text
    assert cookie_uuid not in response.text


def test_create_user_generates_new_uuid():
    """Если нет ни формы, ни cookie — генерируем новый UUID"""
    response = client.post("/create_user")

    assert response.status_code == 200

    # Проверяем, что установлен cookie
    new_uuid = response.cookies.get("session_id")
    assert new_uuid is not None

    # Проверяем, что это валидный UUID
    try:
        uuid.UUID(new_uuid)
    except ValueError:
        pytest.fail(f"Invalid UUID format: {new_uuid}")

    # Проверяем, что он передан в шаблон
    assert new_uuid in response.text


def test_create_user_sets_correct_cookie_attributes():
    """Проверка, что cookie установлена с правильными атрибутами"""
    test_uuid = str(uuid.uuid4())
    client.cookies.set("session_id", test_uuid)

    response = client.post("/create_user")

    set_cookie = response.headers.get("set-cookie")
    assert set_cookie is not None

    # Проверяем ключевые атрибуты
    assert f"session_id={test_uuid}" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "samesite=lax" in set_cookie.lower()

    assert "Max-Age=31536000" in set_cookie
    assert "Path=/" in set_cookie


def test_create_user_hidden_input_contains_uuid():
    """Проверяем, что UUID передаётся в скрытом поле формы"""
    test_uuid = str(uuid.uuid4())
    client.cookies.set("session_id", test_uuid)

    response = client.post("/create_user")

    content = response.text
    match = re.search(
        r'<input[^>]+name="session_uuid"[^>]+value="([0-9a-f-]{36})"', content
    )

    assert match is not None, "UUID not found in hidden input"
    assert match.group(1) == test_uuid


def test_create_user_cookie_is_httponly():
    """Cookie должна быть HttpOnly для защиты от XSS"""
    response = client.post("/create_user")

    set_cookie = response.headers["set-cookie"]
    assert "HttpOnly" in set_cookie, "Cookie should be HttpOnly"
    assert "httponly" in set_cookie.lower()
