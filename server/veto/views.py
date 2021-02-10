from flask import current_app, send_from_directory

from .csrf_protection import CSRF_TOKEN_NAME, set_csrf_token
from .utils import is_client_asset


def client_asset(filename):
    f = filename if is_client_asset(current_app, filename) else "index.html"
    return send_from_directory(current_app.config["CLIENT_DIR"], f)


def csrf_token():
    return {CSRF_TOKEN_NAME: set_csrf_token()}


def health():
    return {"status": "OK"}


def root():
    return send_from_directory(current_app.config["CLIENT_DIR"], "index.html")
