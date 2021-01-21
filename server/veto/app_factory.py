import os
import os.path
from pathlib import Path

import werkzeug
from flask import Flask, render_template, request, safe_join, send_from_directory

CLIENT_DIR = str(Path(__file__).resolve().parent.parent.parent / "client" / "build")


def is_client_asset(filename):
    return filename != "" and os.path.exists(safe_join(CLIENT_DIR, filename))


def create_app(config=None):
    # Rename the static folder to prevent those routes from interferring with
    # client routing. If a static folder becomes necessary in the future,
    # routing (e.g. client handling 404s) will have to be rethought.
    app = Flask(__name__, static_folder="unused")

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "devkey"),
    )

    if config:
        app.config.from_mapping(config)

    @app.route("/api/health")
    def health():
        return {"msg": "OK"}

    # This route should be defined last. It's only used with the client
    # production build (i.e the client/build directory exists). It lets the
    # client handle routing not otherwise specified by the server.
    @app.route("/", defaults={"filename": ""})
    @app.route("/<path:filename>")
    def index(filename):
        f = filename if is_client_asset(filename) else "index.html"
        return send_from_directory(CLIENT_DIR, f)

    @app.errorhandler(werkzeug.exceptions.InternalServerError)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_html:
            return render_template("errors/500.html"), 500
        else:
            return {
                "msg": "We couldn't fulfill your request due to an unexpected error."
            }, 500

    return app
