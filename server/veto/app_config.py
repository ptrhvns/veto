import os
from pathlib import Path


class AppConfig:
    def as_bool(self, value):
        return value.lower() in ["1", "t", "true", "yes"]

    CLIENT_DIR = str(Path(__file__).resolve().parent.parent.parent / "client" / "build")
    SECRET_KEY = os.getenv("SECRET_KEY", "facefeed")

    @property
    def SESSION_COOKIE_HTTPONLY(self):
        return self.as_bool(os.getenv("SESSION_COOKIE_HTTPONLY", default="True"))
