import pytest
from httpx import ASGITransport, AsyncClient

from prediction_app.core.config_run import web_app


@pytest.mark.asyncio
async def test_save_user_creates_new_user(mock_user_service, override_dependency):
    """Если пользователя нет — создаётся новый"""
    name = "TestUser"

    # Убедимся, что сервис возвращает None — значит, пользователь не найден
    mock_user_service.get_user_by_uuid.return_value = None
    # Используем ASGI-транспорт для асинхронного клиента (FastAPI/Starlette)
    transport = ASGITransport(app=web_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        await async_client.get("/")
        response = await async_client.post("/save_user", data={"name": name})

    # Проверяем HTTP-статус ответа: должен быть 200 OK
    assert response.status_code == 200
    # Проверяем, что имя пользователя передано в шаблон и отображается
    assert name in response.text
    # Проверяем, что create_user был вызван один раз (подтверждаем создание)
    mock_user_service.create_user.assert_awaited_once()
    mock_user_service.create_user.assert_called_once()
    # Проверяем, что update_user_name НЕ был вызван (пользователь новый!)
    mock_user_service.update_user_name.assert_not_called()


@pytest.mark.asyncio
async def test_save_user_updates_existing_user(mock_user_service, override_dependency):
    """Если пользователь уже есть — обновляется имя"""
    name = "TestUser"

    # Мокаем существующего пользователя
    existing_user = type("User", (), {"id": 1})
    mock_user_service.get_user_by_uuid.return_value = existing_user

    transport = ASGITransport(app=web_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        await async_client.get("/")

        response = await async_client.post("/save_user", data={"name": name})

    assert response.status_code == 200
    assert name in response.text
    # Проверяем вызовы:
    mock_user_service.get_user_by_uuid.assert_awaited_once()  # с UUID из сессии
    mock_user_service.update_user_name.assert_called_once_with(user_id=1, new_name=name)
    mock_user_service.create_user.assert_not_called()  # НЕ создаём нового


@pytest.mark.asyncio
async def test_save_user_sets_cookie(mock_user_service, override_dependency):
    """Проверка, что cookie устанавливается корректно"""
    name = "Мария"

    mock_user_service.get_user_by_uuid.return_value = None

    transport = ASGITransport(app=web_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        await async_client.get("/")

        response = await async_client.post("/save_user", data={"name": name})

    set_cookie = response.headers.get("set-cookie")
    assert set_cookie is not None, "Ожидалась установка cookie через Set-Cookie"
    cookie_lower = set_cookie.lower()
    assert "httponly" in cookie_lower
    assert "samesite=lax" in cookie_lower
    assert "max-age=31536000" in cookie_lower
    assert "path=/" in cookie_lower
