import os
import os.path

from flask import Flask, send_from_directory


def create_app():
    app = Flask(
        __name__,
        static_folder="../../client/build",
        static_url_path="/",
    )

    app.config.from_mapping(SECRET_KEY=(os.getenv("SECRET_KEY", "devkey")))

    # This route is only useful if the client has been built (i.e the client/build
    # directory exists), and so is only really useful in production, or for testing
    # production-like scenarios. It's designed to redirect all routes not otherwise
    # specified to the client where client-side routing will take over.
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def index(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    return app
