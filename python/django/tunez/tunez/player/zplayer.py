"""
This class houses the Django TUnexz interface to the ZenPlayer app
"""
from os import environ
from requests import get


class ZPlayer:
    """
    Houses the class that interfaces with the ZenPlayer application.
    """
    def __init__(self):
        super().__init__()
        self.address = environ["ZP_URL"]
        """ The URL of the ZenPlayer endpoint """

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
        resp = get(self.address + "/zenplayer/get_state")
        return resp.json()

    def previous_track(self):
        """
        Go back to the previous track.
        """
        get(self.address + "/zenplayer/play_previous")

    def play_pause(self):
        """
        Play the track if the player is currently paused, otherwise pause it.
        """
        get(self.address + "/zenplayer/play_pause")

    def stop(self):
        """
        Stop the track.
        """
        get(self.address + "/zenplayer/stop")

    def next_track(self):
        """
        Advance to the next track
        """
        get(self.address + "/zenplayer/play_next")

    def volume_up(self):
        """
        Turn  the volume up.
        """
        get(self.address + "/zenplayer/volume_up")

    def volume_down(self):
        """
        Turn the volume down.
        """
        get(self.address + "/zenplayer/volume_down")

    def volume_set(self, value):
        """
        Set the volume of the player where value from  0 to 1.
        """
        get(self.address + "/zenplayer/volume_set", params={"volume": value})

    def cover(self):
        """
        Return the album cover art if available, otherwise return False.
        """
        # TODO