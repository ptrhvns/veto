import werkzeug


def test_internal_server_error(app, client):
    route = "/test_internal_server_error"

    @app.route(route)
    def invalid():
        raise werkzeug.exceptions.InternalServerError()

    response = client.get(route, headers={"Accept": "application/json"})
    assert response.mimetype == "application/json"

    response = client.get(route, headers={"Accept": "text/html"})
    assert response.mimetype == "text/html"

    response = client.get(route, headers={"Accept": "*/*"})
    assert response.mimetype == "text/html"

    response = client.get(route)
    assert response.mimetype == "application/json"
