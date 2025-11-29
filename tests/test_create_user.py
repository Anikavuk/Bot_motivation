from fastapi.testclient import TestClient

from prediction_app.core.config_run import web_app

client = TestClient(web_app)


def test_create_user_returns_html():
    response = client.get("/create_user")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<html" in response.text.lower()


def test_create_user_sets_session_cookie():
    response = client.get("/create_user")
    assert "session" in response.cookies
    session_cookie = response.cookies.get("session")
    assert session_cookie is not None and session_cookie != ""


def test_create_user_creates_session_id():
    # Первый запрос - получить cookie
    response1 = client.get("/create_user")
    assert "session" in response1.cookies

    # Второй запрос с тем же cookie
    response2 = client.get("/create_user")
    assert response2.status_code == 200
