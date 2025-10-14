from fastapi.testclient import TestClient
from app.core.config_run import web_app
import pytest


@pytest.fixture
def client():
    return TestClient(web_app)
