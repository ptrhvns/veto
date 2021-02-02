import os
from pathlib import Path


class AppConfig:
    def as_bool(self, value):
        return value.lower() in ["1", "t", "true", "yes"]

    CLIENT_DIR = str(Path(__file__).resolve().parent.parent.parent / "client" / "build")

    @property
    def FLASK_DEBUG(self):
        return self.as_bool(os.getenv("FLASK_DEBUG", default="False"))

    SECRET_KEY = os.getenv("SECRET_KEY", "facefeed")
    SESSION_COOKIE_SAMESITE = "Lax"
