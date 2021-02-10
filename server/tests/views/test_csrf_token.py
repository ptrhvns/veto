from veto.csrf_protection import CSRF_TOKEN_NAME


def test_responds_with_csrf_token(client):
    response = client.get("/api/csrf_token")
    assert response.status_code == 200
    assert CSRF_TOKEN_NAME in response.get_json()
