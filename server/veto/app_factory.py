from flask import Flask
from flask_talisman import Talisman
from werkzeug.exceptions import InternalServerError

from . import app_config, csrf_protection, error_handlers, views


def setup_app_config(app, config=None):
    app.config.from_object(app_config.AppConfig())

    if config:
        app.config.from_mapping(config)


def build_content_security_policy(app):
    return {
        "connect-src": "'self' data:",
        "default-src": "'self' data:",
        "font-src": "'self' data:",
        "frame-src": "'self' data:",
        "img-src": "'self' data:",
        "media-src": "'self' data:",
        "object-src": "'self' data:",
        "script-src": "'self' data: 'unsafe-inline'",
        "style-src": "'self' data: 'unsafe-inline'",
    }


def setup_app_extensions(app):
    Talisman(
        app,
        content_security_policy=(
            None if app.debug else build_content_security_policy(app)
        ),
    )


def setup_app_callbacks(app):
    app.before_request(csrf_protection.protect_request_from_csrf)


def setup_app_url_rules(app):
    # API routes.
    app.add_url_rule("/api/csrf_token", "csrf_token", views.csrf_token, methods=["GET"])
    app.add_url_rule("/api/health", "health", views.health, methods=["GET"])

    # Client asset routes for single-page application. Client handles 404s.
    app.add_url_rule(
        "/<path:filename>", "client_asset", views.client_asset, methods=["GET"]
    )
    app.add_url_rule("/", "root", views.root, methods=["GET"])


def setup_app_error_handlers(app):
    app.register_error_handler(
        InternalServerError, error_handlers.internal_server_error
    )


def create_app(config=None):
    # Sideline static_folder to prevent client route conflicts (e.g. 404s).
    app = Flask("veto", static_folder="unused")

    setup_app_config(app, config)
    setup_app_extensions(app)
    setup_app_callbacks(app)
    setup_app_url_rules(app)
    setup_app_error_handlers(app)

    return app
