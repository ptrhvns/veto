import os
import os.path
import random

from veto.app_factory import CLIENT_DIR


def build_client_path(*subpaths):
    return os.path.join(CLIENT_DIR, *subpaths)


def read_file(filename) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


def get_random_filename(directory):
    return random.choice(os.listdir(directory))


def test_index_with_no_filename(client):
    response = client.get("/")
    file_data = read_file(build_client_path("index.html"))
    assert response.status_code == 200
    assert response.data == file_data


def test_index_with_filename(client):
    subpaths = ["static", "js"]
    directory = build_client_path(*subpaths)
    basename = get_random_filename(directory)
    file_data = read_file(build_client_path(directory, basename))
    relative_url = "/".join(subpaths + [basename])
    response = client.get(f"/{relative_url}")
    assert response.status_code == 200
    assert response.data == file_data
