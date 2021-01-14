import os
import os.path
from pathlib import Path

from flask import Flask, send_from_directory

CLIENT_DIR = str(Path(__file__).resolve().parent.parent.parent / "client" / "build")


def is_client_asset(filename):
    return filename != "" and os.path.exists(os.path.join(CLIENT_DIR, filename))


def create_app():
    # Rename the static folder to prevent those routes from interferring with
    # client routing.
    app = Flask(__name__, static_folder="unused")

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "devkey"),
    )

    # This route should be defined last. It's only used once the client has
    # been built for production (i.e the client/build). It lets the client
    # handle routing not otherwise specified in the server.
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:filename>")
    def index(filename):
        f = filename if is_client_asset(filename) else "index.html"
        return send_from_directory(CLIENT_DIR, f)

    return app
