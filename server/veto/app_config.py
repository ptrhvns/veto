import os
from pathlib import Path


class AppConfig:
    def as_bool(self, value):
        return value.lower() in ["1", "t", "true", "yes"]

    CLIENT_DIR = str(Path(__file__).resolve().parent.parent.parent / "client" / "build")

    @property
    def FLASK_DEBUG(self):
        return self.as_bool(os.getenv("FLASK_DEBUG", default="False"))

    # SECRET_KEY must be set as it's used by app.
    SECRET_KEY = os.environ["SECRET_KEY"]

    # Some SESSION_* configs are handled by the flask-talisman package.
    SESSION_COOKIE_SAMESITE = "Lax"
