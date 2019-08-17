"""
This module houses the main view functions for the media player controller
"""
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .mplayer import MPlayer, Messages
from rest_framework.response import Response
from django.shortcuts import redirect
from os.path import exists


def redirect_view(request):
    """
    Redirect the request for the root URL to the react index.html

    :param request: The Django request object
    :return: The re-direct response
    """
    return redirect('/react/index.html')

class Player(object):
    """
    This class handles the sending of command and the retrieving of state from
    the currently running MPris2 Media player.
    """
    mplayer = MPlayer()

    @staticmethod
    def call(name, request):
        """
        Call the MPlayer function with the given name and return the state.

        Args:
            name: a string giving the name of the function to call
            request: The Django request object. This is used to customize the
                     response for each source IP
        Returns:
            A Response object containing player state
        """
        getattr(Player.mplayer, name)()
        ip = Player._get_ip(request)
        return Response(Player.mplayer.get_state(ip))


    @staticmethod
    @api_view()
    def previous(request):
        """
        Go to the previous track in the playlist and return the player state.
        """
        return Player.call("previous_track", request)

    @staticmethod
    @api_view()
    def play_pause(request):
        """
        Play or pause the current audio player and return the player state.
        """
        return Player.call("play_pause", request)

    @staticmethod
    @api_view()
    def next(request):
        """
        Advance to the next track in the playlist and return the player state.
        """
        return Player.call("next_track", request)

    @staticmethod
    @api_view()
    def stop(request):
        """
        Stop the player and return the player state.
        """
        return Player.call("stop", request)

    @staticmethod
    @api_view()
    def volume_up(request):
        """
        Turn the volume of the player up and return the player state.
        """
        return Player.call("volume_up", request)

    @staticmethod
    @api_view()
    def volume_down(request):
        """
        Turn the volume of the player up and return the player state.
        """
        return Player.call("volume_down", request)

    @staticmethod
    @api_view()
    def volume_set(request, volume):
        """
        Set the volume to a value between 0 and 1.
        """
        Player.mplayer.volume_set(volume)
        ip = Player._get_ip(request)
        return Response(Player.mplayer.get_state(ip))

    @staticmethod
    def _get_ip(request):
        """ Retrieve the IP added of the client for the specified request. """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        else:
            return request.META.get('REMOTE_ADDR')

    @staticmethod
    @api_view()
    def message_add(request, msg_type, msg):
        """
        Add a message to the message queue
        """
        Messages.ensure_client(Player._get_ip(request))
        Messages.add_message(msg_type, msg)
        return Response({})

    @staticmethod
    @api_view()
    def state(request):
        """
        Return the player state.
        """
        ip = Player._get_ip(request)
        return Response(Player.mplayer.get_state(ip))

    @staticmethod
    @api_view()
    def cover(_request):
        """
        Return the cover of the currently player album.
        """
        _cover = Player.mplayer.cover()
        if exists(_cover):
            with open(_cover, "rb") as f:
                return HttpResponse(f.read(),
                                    content_type="image/" + _cover[-3:])
        else:
            return Response("Cover not found.", 400)
