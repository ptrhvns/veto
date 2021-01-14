import os
import os.path
from pathlib import Path

from flask import Flask, safe_join, send_from_directory

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

    @app.route("/api/signup", methods=("GET", "POST"))
    def signup():
        return {"msg": "This has not been implemented yet."}

    # This route should be defined last. It's only used with the client
    # production build (i.e the client/build directory exists). It lets the
    # client handle routing not otherwise specified by the server.
    @app.route("/", defaults={"filename": ""})
    @app.route("/<path:filename>")
    def index(filename):
        f = filename if is_client_asset(filename) else "index.html"
        return send_from_directory(CLIENT_DIR, f)

    return app
