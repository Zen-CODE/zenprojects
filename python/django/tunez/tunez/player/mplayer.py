"""
This module provides functions for controlling the currently active MPRIS2
player.
"""
from mpris2 import get_players_uri, Player
from urllib.parse import urlparse, unquote
from os.path import exists, sep
from logging import getLogger
from .cloud_firestore import NowPlaying
from threading import Thread
from datetime import datetime, timedelta
from socket import gethostname
from dbus.exceptions import DBusException

logger = getLogger(__name__)


class Messages:
    """
    This class manages the message queue around delivering messages to separate
    clients, ensuring that each client gets all messages once and exactly once.
    """
    _clients = {}
    """ A dictionary used to store and lookup the message queues for each client
    """

    @staticmethod
    def add_message(msg_type, text):
        """
        Add the specified message to the queue for each client.

        :param msg_type: The type of message. One of 'track changed' or
                        'album queued'
        :param text: The message to display in the React front-end
        :return: None
        """
        [queue.append({'msg_type': msg_type, 'text': text})
         for queue in Messages._clients.values()]

    @staticmethod
    def ensure_client(ip):
        """
        Ensure this client exists and is registered for receiving messages.

        :param ip: The identifier used lookup and store messages in the queue
        :return: None
        """
        if ip not in Messages._clients.keys():
            Messages._clients[ip] = []

    @staticmethod
    def get_message(ip, state):
        """
        Add any outstanding messages for the specified IP to the payload.

        :param ip: The ip address of the client
        :param state: The state to add the message to (if required)
        :return: None
        """
        messages = Messages._clients[ip]
        if len(messages) > 0:
            state["message"] = messages.pop()


class MPlayer(object):
    """
    This object sends command to the active MPRIS2 player, and retrieves
    information from it.
    """
    state = ""
    """ Tracks the state of the current player """

    track_url = ""
    """ Track the the currently playing song"""

    machine = gethostname()
    """ Get the machine name of the current audio host """

    @staticmethod
    def _get_player():
        """ Return a Player instance of the currently active MPRIS2 player. """
        try:
            uri = next(get_players_uri())
            return Player(dbus_interface_info={'dbus_uri': uri})
        except (StopIteration, DBusException):
            return None

    def change_volume(self, val):
        """
        Change the volume by the specified increment. This should be a number
        between 0 and 1 and is added to the current volume.
        """
        vol = self.get_player_value("Volume", None)
        if vol is not None:
            self.set_player_value("Volume", vol + val)

    @staticmethod
    def _get_from_filename(filename):
        """ Return the artist and album based on the file name"""
        if filename:
            parts = unquote(filename).split(sep)
            return parts[-3], parts[-2], parts[-1]
        else:
            return "", "", ""

    def set_player_value(self, property, value=None):
        """
         Set the value of the specified property to the given value. If no
        value is specified, the prop is assumed to be a function called
        directly.
        """
        player = self._get_player()
        if player is None:
            print("No player found...")
        elif value is None:
            getattr(player, property)()
        else:
            setattr(player, property, value)

    def get_player_value(self, key, default, metadata=False):
        """
        Retrieve the specified value from the player. If it fails, return the
        default value
        """
        player = self._get_player()
        if player is None:
            print("Unable to accesss media player")
        else:
            try:
                if metadata:
                    return player.Metadata[key]
                else:
                    return getattr(player, key)
            except (KeyError, AttributeError):
                return default

    @staticmethod
    def _add_message(ip, track_url, state):
        """ Add a message to the *payload* dictionary if appropriate and write
        events to BigQuery if required.

        Note: We use the full track url i.s.o. the 'track' property to avoid
              the rare case that two different tracks have the same file name.
        """
        Messages.ensure_client(ip)
        if track_url != MPlayer.track_url or state["state"] != MPlayer.state:
            MPlayer.track_url = track_url
            MPlayer.state = state['state']
            Messages.add_message("track changed",
                                 "Now playing - {0} ({1})".format(
                                        state['track'], state['state']))
            Thread(target=lambda: MPlayer._write_to_db(state)).start()
            logger.info("State written to DB")

        Messages.get_message(ip, state)
        return state

    @staticmethod
    def _write_to_db(state):
        """
        Write the current "Now Playing" status to our cloud FireStore. We do so
        in a background thread to try and avoid locking when we get stale
        transport errors.
        """
        def save_to_fs():
            """ Save to firestore """
            NowPlaying(artist=state["artist"], album=state["album"],
                       track=state["track"], state=state['state'],
                       machine=MPlayer.machine,
                       datetime=datetime.now() - timedelta(hours=2)).save()

        Thread(target=save_to_fs).start()

    def get_state(self, ip):
        """ Return a dictionary containing information on the audio player's
        status.


        :param ip: The IP address of the client
        :return: A dict containing the following values:

            * volume: float between 0 and 1
            * status: one of 'Playing', 'Paused' or 'Stopped'.
            * position: a float between 0 and 1
            * artist
            * album
            * track
        """
        gpv = self.get_player_value
        length = gpv("mpris:length", 0, True)
        if length is None:
            pos, track_url, artist, album, track = 0, "", "", "", ""
        else:
            pos = float(gpv("Position", 0)) / float(length) if length > 0 else 0
            track_url = gpv("xesam:url", "", True)
            artist, album, track = self._get_from_filename(track_url)

        return self._add_message(ip, track_url, {
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
        self.set_player_value("Previous")

    def play_pause(self):
        """
        Play the track if the player is currently paused, otherwise pause it.
        """
        self.set_player_value("PlayPause")

    def stop(self):
        """
        Stop the track.
        """
        self.set_player_value("Stop")

    def next_track(self):
        """
        Advance to the next track
        """
        self.set_player_value("Next")

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
        self.set_player_value("Volume", float(value))

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
