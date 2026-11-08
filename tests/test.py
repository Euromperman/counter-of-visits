from app.main import app


def test_status_200():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Hello DevOps"