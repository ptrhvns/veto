import os

from flask import safe_join


def is_client_asset(app, filename):
    path = safe_join(app.config["CLIENT_DIR"], filename)
    return filename != "" and os.path.exists(path)
