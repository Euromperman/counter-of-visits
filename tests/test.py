from unittest.mock import patch

from app.main import app


def test_status_200():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Hello DevOps"
    
    


def test_health():
    with patch("app.main.redis_client.ping", return_value=True):
        client = app.test_client()
        response = client.get("/health")

        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}