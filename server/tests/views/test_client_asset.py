from ..support.client_assets import build_client_path, get_random_filename, read_file


def test_responds_with_client_asset(app, client):
    subpaths = ["static", "js"]
    directory = build_client_path(app, *subpaths)
    basename = get_random_filename(directory)
    file_data = read_file(build_client_path(app, directory, basename))
    relative_url = "/".join(subpaths + [basename])
    response = client.get(f"/{relative_url}")
    assert response.status_code == 200
    assert response.data == file_data
