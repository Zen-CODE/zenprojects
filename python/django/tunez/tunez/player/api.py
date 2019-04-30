"""
This module houses the main view functions for the media player controller
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .mplayer import MPlayer


class Player(object):
    """
    This class handles the sending of command and the retrieving of state from
    the currently running MPris2 Media player.
    """
    mplayer = MPlayer()

    @staticmethod
    def call(name):
        """
        Call the MPlayer function with the given name and return the response
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
    def state(_request):
        """
        Return the player state.
        """
        return Player.call("get_state")
