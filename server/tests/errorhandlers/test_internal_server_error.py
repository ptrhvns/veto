import werkzeug


def test_internal_server_error(app, client):
    @app.route("/invalid")
    def invalid():
        raise werkzeug.exceptions.InternalServerError()

    response = client.get("/invalid", headers={"Accept": "application/json"})
    assert response.mimetype == "application/json"

    response = client.get("/invalid", headers={"Accept": "text/html"})
    assert response.mimetype == "text/html"

    response = client.get("/invalid")
    assert response.mimetype == "text/html"
