"""
This module provides functions for controlling the currently active MPRIS2
player.
"""

from mpris2 import get_players_uri
from mpris2 import Player
# from urllib.parse import urlparse, unquote


class Player(object):
    """
    This object sends command to the active MPRIS2 player, and retrieves
    information from it.
    """

    def __init__(self):
        super(Player, self).__init__()
        uri = next(get_players_uri())
        self.mp2_player = Player(dbus_interface_info={'dbus_uri': uri})

    def change_volume(self, val):
        """
        Change the volume by the specified increment. This should be a number
        between 0 and 1 and is added to the current volume.
        """
        self.mp2_player.Volume += val

    def previous(self):
        """
        Go back to the previous track.
        """
        self.mp2_player.Previous()

    def play_pause(self):
        """
        Play the track if the player is currently paused, otherwise pause it.
        """
        self.mp2_player.PlayPause()

    def next(self):
        """
        Advance to the next track
        """
        self.mp2_player.Next()

    def volume_up(self):
        """
        Turn  the volume up.
        """
        self.change_volume(0.05)

    def volume_down(self):
        """
        Turn the volume down.
        """
        self.change_volume(-0.05)
