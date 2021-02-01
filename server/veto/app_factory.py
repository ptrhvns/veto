from flask import Flask
from flask_talisman import Talisman
from werkzeug.exceptions import InternalServerError

from . import views
from .app_config import AppConfig
from .error_handlers import internal_server_error


def config_app(app, config=None):
    app.config.from_object(AppConfig())
    if config:
        app.config.from_mapping(config)


def init_app_extensions(app):
    Talisman(app)


def add_url_rules(app):
    app.add_url_rule("/api/health", "health", views.health)
    app.add_url_rule("/<path:filename>", "client_asset", views.client_asset)
    app.add_url_rule("/", "root", views.root)


def register_error_handlers(app):
    app.register_error_handler(InternalServerError, internal_server_error)


def create_app(config=None):
    # Sideline static_folder to prevent route conflicts with client.
    app = Flask("veto", static_folder="unused")

    config_app(app, config)
    init_app_extensions(app)
    add_url_rules(app)
    register_error_handlers(app)
    return app
