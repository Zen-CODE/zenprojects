"""
This module houses the main view functions for the library explorer
"""
from rest_framework.decorators import api_view
from tunez.helpers import get_response
from .library import MusicLib
from django.http import HttpResponse


class Library(object):
    """
    This class handles the sending of command and the retrieving of state from
    the currently running MPris2 Media player.
    """
    lib = MusicLib("/home/fruitbat/Music/")

    @staticmethod
    @api_view()
    def artists(_request):
        """
        Return a list of all the artists in our music collection.
        """
        return get_response(Library.lib.get_artists())

    @staticmethod
    @api_view()
    def albums(_request, artist):
        """
        Return a list of all the albums by this artist.
        """
        return get_response(Library.lib.get_albums(artist))

    @staticmethod
    @api_view()
    def tracks(_request, artist, album):
        """
        Return a list of all the tracks in this album.
        """
        return get_response(Library.lib.get_tracks(artist, album))

    @staticmethod
    @api_view()
    def cover(_request, artist, album):
        """
        Return a list of all the tracks in this album.
        """
        _cover = Library.lib.get_cover(artist, album)
        if _cover:
            with open(_cover, "rb") as f:
                return HttpResponse(f.read(),
                                    content_type="image/" + _cover[-3:])
        return get_response({"message": "No cover found"})
