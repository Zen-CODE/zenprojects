"""
This module houses the main view functions for the media player controller
"""
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .mplayer import MPlayer
from rest_framework.response import Response


class Player(object):
    """
    This class handles the sending of command and the retrieving of state from
    the currently running MPris2 Media player.
    """
    mplayer = MPlayer()

    @staticmethod
    def call(name):
        """
        Call the MPlayer function with the given name and return the response.
        """
        getattr(Player.mplayer, name)()
        return Response(Player.mplayer.get_state())

    @staticmethod
    @api_view()
    def previous(_request):
        """
        Go to the previous track in the playlist and return the player state.
        """
        return Player.call("previous_track")

    @staticmethod
    @api_view()
    def play_pause(_request):
        """
        Play or pause the current audio player and return the player state.
        """
        return Player.call("play_pause")

    @staticmethod
    @api_view()
    def next(_request):
        """
        Advance to the next track in the playlist and return the player state.
        """
        return Player.call("next_track")

    @staticmethod
    @api_view()
    def stop(_request):
        """
        Stop the player and return the player state.
        """
        return Player.call("stop")

    @staticmethod
    @api_view()
    def volume_up(_request):
        """
        Turn the volume of the player up and return the player state.
        """
        return Player.call("volume_up")

    @staticmethod
    @api_view()
    def volume_down(_request):
        """
        Turn the volume of the player up and return the player state.
        """
        return Player.call("volume_down")

    @staticmethod
    @api_view()
    def volume_set(_request, volume):
        """
        Set the volume to a value between 0 and 1.
        """
        Player.mplayer.volume_set(volume)
        return Response(Player.mplayer.get_state())

    @staticmethod
    @api_view()
    def state(_request):
        """
        Return the player state.
        """
        return Player.call("get_state")

    @staticmethod
    @api_view()
    def cover(_request):
        """
        Return the cover of the currently player album.
        """
        _cover = Player.mplayer.cover()
        with open(_cover, "rb") as f:
            return HttpResponse(f.read(), content_type="image/" + _cover[-3:])

