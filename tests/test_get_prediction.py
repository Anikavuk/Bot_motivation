import uuid
from datetime import datetime, timezone

from src.app.core.config_run import web_app
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from src.app.services.motivation_ai import HuggingFacePredictor


@pytest.mark.asyncio
async def test_get_prediction_creates_user_and_new_prediction(
    mock_user_service,
    mock_prediction_service,
    override_dependency,
):
    """Если пользователя нет — создаётся новый, и генерируется новое предсказание"""

    name = "Анна"
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
            await async_client.get("/")
            response = await async_client.post("/get_prediction", data={"name": name})

    # Проверяем
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert fake_prediction_text in response.text

    mock_user_service.get_user_by_uuid.assert_awaited_once()
    args, _ = mock_user_service.get_user_by_uuid.call_args
    called_uuid = args[0]
    # Убедимся, что передан валидный UUID
    uuid.UUID(called_uuid)  # выбросит ValueError, если не UUID

    # Проверка вызовов
    mock_user_service.create_user.assert_awaited_once()
    mock_user_service.get_date_prediction.assert_awaited_once()
    mock_prediction_service.get_prediction_for_user.assert_awaited_once_with(
        fake_user.id
    )
    mock_prediction_service.save_prediction_in_db.assert_awaited_once_with(
        fake_prediction_text, fake_user.id
    )
