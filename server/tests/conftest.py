import pytest
from veto.app_factory import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
