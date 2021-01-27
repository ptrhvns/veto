from flask import current_app, send_from_directory

from .utils import is_client_asset


def client_asset(filename):
    f = filename if is_client_asset(current_app, filename) else "index.html"
    return send_from_directory(current_app.config["CLIENT_DIR"], f)


def health():
    return {"msg": "OK"}


def root():
    return send_from_directory(current_app.config["CLIENT_DIR"], "index.html")
