import os
import os.path
import random


def build_client_path(app, *subpaths):
    return os.path.join(app.config["CLIENT_DIR"], *subpaths)


def get_random_filename(directory):
    return random.choice(os.listdir(directory))


def read_file(filename) -> bytes:
    with open(filename, "rb") as f:
        return f.read()
