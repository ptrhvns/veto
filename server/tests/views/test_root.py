from ..support.client_assets import build_client_path, read_file


def test_responds_with_client_index_html(app, client):
    response = client.get("/")
    file_data = read_file(build_client_path(app, "index.html"))
    assert response.status_code == 200
    assert response.data == file_data
