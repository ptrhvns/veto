import os
import os.path
import random


def build_client_path(app, *subpaths):
    return os.path.join(app.config["CLIENT_DIR"], *subpaths)


def read_file(filename) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


def get_random_filename(directory):
    return random.choice(os.listdir(directory))


def test_index_with_no_filename(app, client):
    response = client.get("/")
    file_data = read_file(build_client_path(app, "index.html"))
    assert response.status_code == 200
    assert response.data == file_data


def test_index_with_filename(app, client):
    subpaths = ["static", "js"]
    directory = build_client_path(app, *subpaths)
    basename = get_random_filename(directory)
    file_data = read_file(build_client_path(app, directory, basename))
    relative_url = "/".join(subpaths + [basename])
    response = client.get(f"/{relative_url}")
    assert response.status_code == 200
    assert response.data == file_data
