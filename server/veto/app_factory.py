import os
import os.path
from pathlib import Path

from flask import Flask, send_from_directory

CLIENT_DIRECTORY = str(
    Path(__file__).resolve().parent.parent.parent / "client" / "build"
)


def is_client_asset_path(app, path):
    return path != "" and os.path.exists(os.path.join(CLIENT_DIRECTORY, path))


def create_app():
    # Sideline the static folder to facilitate proper handling of routes on
    # both the client and the server side.
    app = Flask(__name__, static_folder="invalid")

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "devkey"),
    )

    # This route should be defined last. It's only useful if the client has
    # been built (i.e the client/build directory exists), and so is only really
    # useful in production, or for testing production-like scenarios. It's
    # designed to redirect all routes not otherwise specified to the client
    # where client-side routing will take over.
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def index(path):
        if is_client_asset_path(app, path):
            return send_from_directory(CLIENT_DIRECTORY, path)
        return send_from_directory(CLIENT_DIRECTORY, "index.html")

    return app
