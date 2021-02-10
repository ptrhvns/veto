from http import HTTPStatus

import werkzeug


def test_internal_server_error(app, client):
    route = "/test_internal_server_error"

    @app.route(route)
    def invalid():
        raise werkzeug.exceptions.InternalServerError()

    response = client.get(route, headers={"Accept": "application/json"})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert response.mimetype == "application/json"

    response = client.get(route, headers={"Accept": "text/html"})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert response.mimetype == "text/html"

    response = client.get(route, headers={"Accept": "*/*"})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert response.mimetype == "text/html"

    response = client.get(route)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert response.mimetype == "application/json"
