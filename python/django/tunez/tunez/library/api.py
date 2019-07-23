"""
This module houses the main view functions for the library explorer
"""
from rest_framework.decorators import api_view
from .library import MusicLib
from django.http import HttpResponse
from os.path import exists, expanduser
from os import system
from rest_framework.response import Response
from tunez.player.mplayer import Messages


class Library(object):
    """
    This class handles the sending of command and the retrieving of state from
    the currently running MPris2 Media player.
    """
    lib = MusicLib(expanduser("~/Music/"))

    @staticmethod
    @api_view()
    def artists(_request):
        """
        Return a list of all the artists in our music collection.
        """
        return Response(sorted(Library.lib.get_artists()))

    @staticmethod
    @api_view()
    def albums(_request, artist):
        """
        Return a list of all the albums by this artist.
        """
        return Response(sorted(Library.lib.get_albums(artist)))

    @staticmethod
    @api_view()
    def tracks(_request, artist, album):
        """
        Return a list of all the tracks in this album.
        """
        return Response(sorted(Library.lib.get_tracks(artist, album)))

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
        return Response({"message": "No cover found"})

    @staticmethod
    @api_view()
    def random_album(_request):
        """
        Select and return a random artist and album
        """
        artist = Library.lib.get_random_artists(1)[0]
        album = Library.lib.get_random_albums(artist, 1)[0]
        return Response({"artist": artist, "album": album})

    @staticmethod
    @api_view(['GET'])
    def folder_enqueue(_request, artist, album):
        """
        Add the specified album to the end of the playlist
        """
        path = Library.lib.get_album_path(artist, album)
        Messages.add_message("album queued", "Album queued: {0} - {1}".format(
            artist, album))
        if exists(path):
            system('audacious -e "{0}"'.format(path))
            return Response({"message": "Enqueue instruction sent"}
                            )
        else:
            return Response({"message": "No such album"})

    @staticmethod
    @api_view(['GET'])
    def folder_play(_request, artist, album):
        """
        Open and play the specified album
        """
        path = Library.lib.get_album_path(artist, album)
        if exists(path):
            system('audacious -E "{0}"'.format(path))
            return Response({"message": "Play folder instruction sent"})
        else:
            return Response({"message": "No such album"})

    @staticmethod
    @api_view(['GET'])
    def search(_request, term):
        """
        Search for all albums which match this term, either in the artist
        name of the album name, then return one on them randomly.

        Returns:
             A dictionary with the artist and album as keys if found. Return an
             empty dictionary otherwise.
        """
        return Response(Library.lib.search(term))
