def test_health(client):
    response = client.get("/api/health")
    assert response.get_json() == {"status": "OK"}
