from unittest.mock import patch
import pytest
from httpx import AsyncClient, ASGITransport

from app.services.motivation_ai import HuggingFacePredictor


#
@pytest.mark.asyncio
async def test_get_prediction_creates_user_and_new_prediction(
    mock_user_service, mock_prediction_service
):
    """Если пользователя нет — создаётся новый, и генерируется новое предсказание"""
    from app.core.config_run import web_app

    name = "Анна"
    session_uuid = "test-uuid-123"
    fake_prediction_text = "Сегодня твой день!"

    # Мокируем отсутствие пользователя
    mock_user_service.get_user_by_uuid.return_value = None

    # Мокируем отсутствие даты предсказания
    mock_user_service.get_date_prediction.return_value = None

    # Мокируем отсутствие сохранённого предсказания
    mock_prediction_service.get_prediction_for_user.return_value = None

    # Подменяем метод get_prediction у HuggingFacePredictor
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
    assert name in response.text
    assert session_uuid in response.text
    assert fake_prediction_text in response.text

    # Проверяем вызовы сервисов
    mock_user_service.get_user_by_uuid.assert_awaited_once_with(session_uuid)
    mock_user_service.create_user.assert_awaited_once()
    mock_user_service.get_date_prediction.assert_awaited_once_with(session_uuid)
    mock_prediction_service.get_prediction_for_user.assert_awaited_once()
    mock_prediction_service.save_prediction_in_db.assert_awaited_once_with(
        response_text=fake_prediction_text,
        user_id=mock_user_service.create_user.return_value.id,
    )
