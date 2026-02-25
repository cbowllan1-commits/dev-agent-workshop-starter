import pytest
from fastapi.testclient import TestClient

from src.database import Database
from src.main import app


@pytest.fixture(autouse=True)
def reset_db():
    Database.reset()
    yield
    Database.reset()


@pytest.fixture
def client():
    return TestClient(app)
