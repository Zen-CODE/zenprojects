from fastapi.testclient import TestClient
from app.main import app
from unittest import TestCase

client = TestClient(app)


class LibraryTests(TestCase):
    """ Class holding the library API tests."""

    def test_get_artists(self):
        """ Test get_artists returns a list of artists. """
        response = client.get("/library/artists")
        assert response.status_code == 200
        artists = response.json()["artists"]
        assert len(artists) > 500
        assert "In Flames" in artists

    def test_get_albums_with_valid_artist(self):
        """Test get_albums returns a list of albums given a valid artist."""
        response = client.get("/library/albums/BT")
        assert response.status_code == 200
        albums = response.json()["albums"]
        assert len(albums) > 2
        assert "Escm" in albums

    def test_get_albums_with_invalid_artist(self):
        """Test get_albums returns a 404 given a invalid artist."""
        response = client.get("/library/albums/Blah")
        assert response.status_code == 404

    def test_get_cover_with_valid_album(self):
        """Test get_cover returns a en a invalid artist."""
        response = client.get("/library/cover/BT/Escm")
        assert response.status_code == 200
        assert response.headers['content-type'] == "image/png"
        assert response.headers['content-length'] == "31610"

    def test_get_cover_with_invalid_album(self):
        """Test get_cover returns a en a invalid artist."""
        response = client.get("/library/cover/xxx/xxx")
        assert response.status_code == 404
