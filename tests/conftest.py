from unittest.mock import AsyncMock
import pytest

from src.app.auth.user_service import UserService
from src.app.core.config_run import web_app
from src.app.services.prediction_service import PredictionService
from tests.fake_settings import fake_settings


@pytest.fixture(autouse=True)
def patch_settings(monkeypatch):
    def mock_get_settings():
        return fake_settings

    monkeypatch.setattr("src.app.core.settings.get_settings", mock_get_settings)


@pytest.fixture()
def mock_user_service():
    user_service = AsyncMock()
    user_service.get_user_by_uuid = AsyncMock(return_value=None)
    user_service.create_user = AsyncMock()
    user_service.update_user_name = AsyncMock()
    user_service.get_date_prediction = AsyncMock(return_value=None)
    return user_service


@pytest.fixture()
def mock_prediction_service(monkeypatch):
    service = AsyncMock()
    service.get_prediction_for_user = AsyncMock(return_value=None)
    service.save_prediction_in_db = AsyncMock()
    return service


@pytest.fixture()
def override_dependency(mock_user_service, mock_prediction_service):
    """Автоматически подменяет зависимости во всех тестах"""
    web_app.dependency_overrides[UserService] = lambda: mock_user_service
    web_app.dependency_overrides[PredictionService] = lambda: mock_prediction_service

    yield
    web_app.dependency_overrides.clear()
