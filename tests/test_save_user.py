from app.core.config_run import web_app
import pytest
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_save_user_creates_new_user(mock_user_service, override_dependency):
    """Если пользователя нет — создаётся новый"""
    name = "TestUser"
    session_uuid = "test_uuid"

    # Убедимся, что сервис возвращает None — значит, пользователь не найден
    mock_user_service.get_user_by_uuid.return_value = None
    # Используем ASGI-транспорт для асинхронного клиента (FastAPI/Starlette)
    transport = ASGITransport(app=web_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        response = await async_client.post(
            "/save_user", data={"name": name, "session_uuid": session_uuid}
        )

    # Проверяем HTTP-статус ответа: должен быть 200 OK
    assert response.status_code == 200
    # Проверяем, что имя пользователя передано в шаблон и отображается
    assert name in response.text
    # Проверяем, что UUID передан в шаблон (например, в скрытое поле формы)
    assert session_uuid in response.text

    # Проверяем, что метод get_user_by_uuid был вызван ровно один раз с правильным аргументом
    mock_user_service.get_user_by_uuid.assert_awaited_once_with(session_uuid)
    # Проверяем, что create_user был вызван один раз (подтверждаем создание)
    mock_user_service.create_user.assert_awaited_once()
    # Проверяем, что update_user_name НЕ был вызван (пользователь новый!)
    mock_user_service.update_user_name.assert_not_called()


#
# @pytest.mark.asyncio
# async def test_save_user_updates_existing_user(
#     mock_user_service, mock_prediction_service, mock_db_dependency
# ):
#     """Если пользователь уже есть — обновляется имя"""
#     name = "TestUser"
#     session_uuid = "test_uuid"
#
#     # Мокаем существующего пользователя
#     existing_user = type("User", (), {"id": 1})
#     mock_user_service.get_user_by_uuid.return_value = existing_user
#
#     transport = ASGITransport(app=web_app)
#     async with AsyncClient(transport=transport, base_url="http://test") as async_client:
#         response = await async_client.post(
#             "/save_user", data={"name": name, "session_uuid": session_uuid}
#         )
#
#     assert response.status_code == 200
#     # Проверяем, что новое имя отображается в ответе
#     assert name in response.text
#
#     mock_user_service.get_user_by_uuid.assert_awaited_once_with(session_uuid)
#     mock_user_service.update_user_name.assert_called_once_with(user_id=1, new_name=name)
#     mock_user_service.create_user.assert_not_called()
#
#
# @pytest.mark.asyncio
# async def test_save_user_sets_cookie(mock_user_service, mock_prediction_service, mock_db_dependency):
#     """Проверка, что cookie устанавливается корректно"""
#     name = "Мария"
#     session_uuid = "abc123"
#
#     mock_user_service.get_user_by_uuid.return_value = None
#
#     transport = ASGITransport(app=web_app)
#     async with AsyncClient(transport=transport, base_url="http://test") as async_client:
#         response = await async_client.post(
#             "/save_user", data={"name": name, "session_uuid": session_uuid}
#         )
#
#     # Получаем заголовок Set-Cookie из ответа
#     set_cookie = response.headers.get("set-cookie")
#     # Проверяем, что заголовок Set-Cookie присутствует
#     assert set_cookie is not None
#     # Проверяем, что в заголовке установлен нужный session_id
#     assert f"session_id={session_uuid}" in set_cookie
#     # Проверяем наличие атрибута HttpOnly (защита от XSS)
#     assert "httponly" in set_cookie.lower()
#     # Проверяем наличие SameSite=Lax (защита от CSRF)
#     assert "samesite=lax" in set_cookie.lower()
#     # Проверяем срок жизни cookie: 1 год (31536000 секунд)
#     assert "max-age=31536000" in set_cookie.lower()
#     # Проверяем, что cookie доступна по всем путям сайта
#     assert "path=/" in set_cookie.lower()
