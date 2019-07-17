"""
This module provides functions for controlling the currently active MPRIS2
player.
"""
from mpris2 import get_players_uri, Player
from urllib.parse import urlparse, unquote
from os.path import exists, sep
from logging import getLogger
from .cloud_sql import NowPlaying
from threading import Thread
from datetime import datetime

logger = getLogger(__name__)


class MPlayer(object):
    """
    This object sends command to the active MPRIS2 player, and retrieves
    information from it.
    """
    state = ""
    """ Tracks the state of the current player """

    track_url = ""
    """ Track the the currently playing song"""

    messages = []
    """ A list of messages waiting to be send to the clients. """

    def __init__(self):
        super(MPlayer, self).__init__()
        try:
            uri = next(get_players_uri())
            self.mp2_player = Player(dbus_interface_info={'dbus_uri': uri})
        except StopIteration:
            self.mp2_player = None

    def change_volume(self, val):
        """
        Change the volume by the specified increment. This should be a number
        between 0 and 1 and is added to the current volume.
        """
        self.mp2_player.Volume += val

    @staticmethod
    def _get_from_filename(filename):
        """ Return the artist and album based on the file name"""
        if filename:
            parts = unquote(filename).split(sep)
            return parts[-3], parts[-2], parts[-1]
        else:
            return "", "", ""

    def get_player_value(self, key, default, metadata=False):
        """
        Retrieve the specified value from the player. If it fails, return the
        default value
        """
        try:
            if metadata:
                return self.mp2_player.Metadata[key]
            else:
                return getattr(self.mp2_player, key)
        except (KeyError, AttributeError):
            return default

    @staticmethod
    def _add_message(track_url, state):
        """ Add a message to the *payload* dictionary if appropriate and write
        events to BigQuery if required.

        Note: We use the full track url i.s.o. the 'track' property to avoid
              the rare case that two different tracks have the same file name.
        """
        if track_url != MPlayer.track_url or state["state"] != MPlayer.state:
            MPlayer.track_url = track_url
            MPlayer.state = state['state']
            MPlayer.messages.append({"type": "track changed",
                                    "text": "Now playing - {0} ({1})".format(
                                        state['track'], state['state'])})
            Thread(target=lambda: MPlayer._write_to_db(state)).start()
            logger.info("State written to DB")

        if len(MPlayer.messages) > 0:
            state["message"] = MPlayer.messages.pop()
            logger.info("Message: {0}".format(state['message']))
        return state

    @staticmethod
    def _write_to_db(state):
        """ Write the current "Now Playing" status to our cloud DB """
        NowPlaying(artist=state["artist"], album=state["album"],
                   track=state["track"], state=state['state'],
                   datetime=datetime.now()).save()

    def get_state(self):
        """ Return a dictionary containing information on the audio player's
        status. Values in this dict are:

            * volume: float between 0 and 1
            * status: one of 'Playing', 'Paused' or 'Stopped'.
        """
        gpv = self.get_player_value
        length = gpv("mpris:length", 0, True)
        pos = float(self.mp2_player.Position) / float(length) if length > 0 \
            else 0
        track_url = gpv("xesam:url", "", True)
        artist, album, track = self._get_from_filename(track_url)

        return self._add_message(track_url, {
            "volume": gpv("Volume", 0),
            "state": gpv("PlaybackStatus", "stopped"),
            "position": pos,
            "artist": artist,
            "album": album,
            "track": track
        })

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

    def volume_set(self, value):
        """
        Set the volume of the player where value from  0 to 1.
        """
        self.mp2_player.Volume = float(value)

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

        fname = get_cover(self.get_player_value('mpris:artUrl',
                                                "Music/audio_icon.png", True))
        if exists(fname):
            return fname
        else:
            return False
