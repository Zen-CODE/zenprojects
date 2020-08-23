from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_artists():
    response = client.get("/library/artists")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}