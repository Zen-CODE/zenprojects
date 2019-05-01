"""
This module houses the main view functions for the library explorer
"""
from rest_framework.decorators import api_view
from tunez.helpers import get_response
from .library import MusicLib


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
