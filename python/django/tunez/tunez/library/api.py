"""
This module houses the main view functions for the library explorer
"""
from rest_framework.decorators import api_view
from tunez.helpers import get_response
from .library import MusicLib
from django.http import HttpResponse
from os.path import exists
from os import system


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
        return get_response(sorted(Library.lib.get_artists()))

    @staticmethod
    @api_view()
    def albums(_request, artist):
        """
        Return a list of all the albums by this artist.
        """
        return get_response(sorted(Library.lib.get_albums(artist)))

    @staticmethod
    @api_view()
    def tracks(_request, artist, album):
        """
        Return a list of all the tracks in this album.
        """
        return get_response(sorted(Library.lib.get_tracks(artist, album)))

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

    @staticmethod
    @api_view()
    def random_album(_request):
        """
        Select and return a random artist and album
        """
        artist = Library.lib.get_random_artists(1)[0]
        album = Library.lib.get_random_albums(artist, 1)[0]
        return get_response({"artist": artist, "album": album})

    @staticmethod
    @api_view(['GET'])
    def folder_enqueue(_request, artist, album):
        """
        Add the specified album to the end of the playlist
        """
        path = Library.lib.get_album_path(artist, album)
        if exists(path):
            system('audacious -e "{0}"'.format(path))
        else:
            return get_response({"message": "No such album"})

    @staticmethod
    @api_view(['GET'])
    def folder_play(_request, artist, album):
        """
        Open and play the specified album
        """
        path = Library.lib.get_album_path(artist, album)
        if exists(path):
            system('audacious -E "{0}"'.format(path))
        else:
            return get_response({"message": "No such album"})
