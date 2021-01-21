import os
import os.path
from pathlib import Path

import werkzeug
from flask import Flask, render_template, request, safe_join, send_from_directory

CLIENT_DIR = str(Path(__file__).resolve().parent.parent.parent / "client" / "build")


def is_client_asset(filename):
    return filename != "" and os.path.exists(safe_join(CLIENT_DIR, filename))


def create_app(config=None):
    app = Flask(__name__, static_folder="unused")

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "devkey"),
    )

    if config:
        app.config.from_mapping(config)

    @app.route("/api/health")
    def health():
        return {"msg": "OK"}

    @app.route("/<path:filename>")
    def client_asset(filename):
        f = filename if is_client_asset(filename) else "index.html"
        return send_from_directory(CLIENT_DIR, f)

    @app.route("/")
    def root():
        return send_from_directory(CLIENT_DIR, "index.html")

    @app.errorhandler(werkzeug.exceptions.InternalServerError)
    def internal_server_error(e):
        msg = "We couldn't fulfill your request due to an unexpected error."
        code = 500

        if request.accept_mimetypes.accept_html:
            return render_template("errors/500.jinja", msg=msg), code
        else:
            return {"msg": msg}, code

    return app
