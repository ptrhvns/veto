import pytest
from veto.app_factory import create_app

APP_CONFIG_DEFAULT = {"DEBUG": True, "TESTING": True}


@pytest.fixture
def app():
    return create_app(APP_CONFIG_DEFAULT)


@pytest.fixture
def app_fn():
    def fn(config=None):
        return create_app(
            {**APP_CONFIG_DEFAULT, **config} if config else APP_CONFIG_DEFAULT
        )

    return fn


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
