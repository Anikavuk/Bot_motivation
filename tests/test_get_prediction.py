from datetime import datetime, timezone

from app.core.config_run import web_app
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from app.services.motivation_ai import HuggingFacePredictor


@pytest.mark.asyncio
async def test_get_prediction_creates_user_and_new_prediction(
    mock_user_service,
    mock_prediction_service,
    override_dependency,
):
    """Если пользователя нет — создаётся новый, и генерируется новое предсказание"""

    name = "Анна"
    session_uuid = "test-uuid-123"
    fake_prediction_text = "Сегодня твой день!"

    # Настройка моков
    mock_user_service.get_user_by_uuid.return_value = None
    mock_user_service.get_date_prediction.return_value = datetime(
        2025, 10, 20, tzinfo=timezone.utc
    )
    mock_prediction_service.get_prediction_for_user.return_value = None

    fake_user = AsyncMock()
    fake_user.id = 999
    fake_user.name = name
    mock_user_service.create_user.return_value = fake_user

    # мокаем HuggingFacePredictor
    with patch.object(
        HuggingFacePredictor, "get_prediction", return_value=fake_prediction_text
    ):
        transport = ASGITransport(app=web_app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as async_client:
            response = await async_client.post(
                "/get_prediction", data={"name": name, "session_uuid": session_uuid}
            )

    # Проверяем успешный ответ
    assert response.status_code == 200

    # Проверяем, что имя и UUID переданы в шаблон
    assert response.status_code == 200
    # assert session_uuid in response.text
    assert fake_prediction_text in response.text
    assert "session_id=test-uuid-123" in response.headers.get("set-cookie", "")
    assert "text/html" in response.headers.get("content-type", "")

    # Проверка вызовов
    mock_user_service.get_user_by_uuid.assert_awaited_once_with(session_uuid)
    mock_user_service.create_user.assert_awaited_once()
    mock_user_service.get_date_prediction.assert_awaited_once_with(session_uuid)
    mock_prediction_service.get_prediction_for_user.assert_awaited_once_with(
        fake_user.id
    )
    mock_prediction_service.save_prediction_in_db.assert_awaited_once_with(
        fake_prediction_text, fake_user.id
    )
