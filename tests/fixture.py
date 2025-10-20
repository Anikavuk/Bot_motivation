from unittest.mock import AsyncMock
import pytest

from app.auth.user_service import UserService
from app.core.config_run import web_app
from app.services.prediction_service import PredictionService
from tests.conftest import fake_settings


@pytest.fixture(autouse=True)
def patch_settings(monkeypatch):
    # monkeypatch.setattr("app.core.settings.settings", lambda: fake_settings)
    # monkeypatch.setattr("app.core.db_dependency.settings", fake_settings)
    monkeypatch.setattr("app.core.settings.settings", fake_settings)


@pytest.fixture(autouse=True)
def mock_user_service(monkeypatch):
    user_service = AsyncMock()
    user_service.get_user_by_uuid = AsyncMock(return_value=None)
    user_service.create_user = AsyncMock()
    user_service.update_user_name = AsyncMock()
    user_service.get_date_prediction = AsyncMock()

    monkeypatch.setattr("app.auth.user_service.UserService", lambda: user_service)
    return user_service


@pytest.fixture(autouse=True)
def mock_prediction_service(monkeypatch):
    service = AsyncMock()
    service.get_prediction_for_user = AsyncMock(return_value=None)
    service.save_prediction_in_db = AsyncMock()
    monkeypatch.setattr(
        "app.services.prediction_service.PredictionService", lambda: service
    )
    return service


# @pytest.fixture(autouse=True)
# def mock_db_dependency(monkeypatch):
#     db_mock = AsyncMock()
#     db_mock.db_session = AsyncMock()
#     monkeypatch.setattr("app.core,db_dependency.DBDependency", lambda: db_mock)
#     return db_mock


@pytest.fixture()
def override_dependency(mock_user_service, mock_prediction_service):
    """Автоматически подменяет зависимости во всех тестах"""
    web_app.dependency_overrides[UserService] = lambda: mock_user_service
    web_app.dependency_overrides[PredictionService] = lambda: mock_prediction_service
    # web_app.dependency_overrides[DBDependency] = lambda: mock_db_dependency

    yield
    web_app.dependency_overrides.clear()
