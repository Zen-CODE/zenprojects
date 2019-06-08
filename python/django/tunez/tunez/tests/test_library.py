"""
This module contains test for the library API for Tunez application
"""
from django.test import Client
from django.test import TestCase


class TestLibrary(TestCase):
    """
    Test the Tunez library API
    """
    def setUp(self):
        self.client = Client()

    def test_artists(self):
        """ Test that the library returns artists. """
        response = self.client.get("/library/artists")
        artists = response.json()
        assert len(artists) > 10
        assert "In Flames" in artists
        print("Library - Artists test passed...")

    def test_albums(self):
        """ Test that the library returns albums for an artist. """
        response = self.client.get("/library/albums/In Flames")
        albums = response.json()
        assert len(albums) > 10
        assert "Battles" in albums
        print("Library - Albums test passed...")

    def test_tracks(self):
        """ Test that the library returns tracks given an artist and an album.
        """
        response = self.client.get("/library/tracks/In Flames/Battles")
        tracks = response.json()
        assert "04 - The Truth.mp3" in tracks
        print("Library - Albums test passed...")
