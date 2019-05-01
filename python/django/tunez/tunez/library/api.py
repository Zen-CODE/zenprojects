"""
This module houses the main view functions for the library explorer
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
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
        response = Response(Library.lib.get_artists())
        response["Access-Control-Allow-Origin"] = "*"
        return response
