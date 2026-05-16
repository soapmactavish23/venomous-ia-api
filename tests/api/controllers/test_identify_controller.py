import base64
from io import BytesIO

from src.core.server.server import app


def basic_auth_header(username="admin", password="123456"):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {
        "Authorization": f"Basic {token}"
    }


def test_health_should_return_up():
    client = app.test_client()

    response = client.get("/api/Health")

    assert response.status_code == 200
    assert response.json["status"] == "UP"


def test_identify_without_auth_should_return_401():
    client = app.test_client()

    response = client.post("/api/identify")

    assert response.status_code == 401


def test_identify_without_required_fields_should_return_400():
    client = app.test_client()

    response = client.post(
        "/api/identify",
        headers=basic_auth_header(),
        data={},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["message"] == "Input payload validation failed"
    assert "errors" in response.json