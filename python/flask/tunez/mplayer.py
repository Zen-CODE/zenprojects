"""
This module provides functions for controlling the currently active MPRIS2
player.
"""

from mpris2 import get_players_uri, Player
from urllib.parse import urlparse, unquote
from os.path import exists


class MPlayer(object):
    """
    This object sends command to the active MPRIS2 player, and retrieves
    information from it.
    """

    def __init__(self):
        super(MPlayer, self).__init__()
        uri = next(get_players_uri())
        self.mp2_player = Player(dbus_interface_info={'dbus_uri': uri})

    def change_volume(self, val):
        """
        Change the volume by the specified increment. This should be a number
        between 0 and 1 and is added to the current volume.
        """
        self.mp2_player.Volume += val

    def get_state(self):
        """ Return a dictionary containing information on the audio players
        current status.
        """
        return {"volume": self.mp2_player.Volume}

    def previous_track(self):
        """
        Go back to the previous track.
        """
        self.mp2_player.Previous()

    def play_pause(self):
        """
        Play the track if the player is currently paused, otherwise pause it.
        """
        self.mp2_player.PlayPause()

    def stop(self):
        """
        Stop the track.
        """
        self.mp2_player.Stop()

    def next_track(self):
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

    def cover(self):
        """
        Return the album cover art if available, otherwise return False.
        """

        def get_cover(url):
            """ Return the path to the cover art """
            parsed = urlparse(url)
            if parsed.scheme == 'file':
                return unquote(parsed.path)
            else:
                return "Music/audio_icon.png"

        data = self.mp2_player.Metadata
        fname = get_cover(str(data['mpris:artUrl']))
        if exists(fname):
            return fname
        else:
            return False
