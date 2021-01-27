import werkzeug
from flask import Flask

from .app_config import AppConfig
from .error_handlers import internal_server_error
from .views import client_asset, health, root


def configure_app(app, config=None):
    app.config.from_object(AppConfig())
    if config:
        app.config.from_mapping(config)


def register_routes(app):
    app.add_url_rule("/api/health", "health", health)
    app.add_url_rule("/<path:filename>", "client_asset", client_asset)
    app.add_url_rule("/", "root", root)


def register_error_handlers(app):
    app.register_error_handler(
        werkzeug.exceptions.InternalServerError, internal_server_error
    )


def create_app(config=None):
    app = Flask(__name__, static_folder="unused")
    configure_app(app, config)
    register_routes(app)
    register_error_handlers(app)
    return app
