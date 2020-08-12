"""
This module houses a VLC audio component that supports the Kivy `Sound`
interface.
"""
from vlc import EventType, Instance
from logging import getLogger


logger = getLogger(__name__)


class Sound():
    '''
    Singleton Sound instance for playing audio files via the VLC backend.
    '''
    volume = 1.0
    """ Volume  between 0 and 1.0 """

    filename = ""
    """ The full path to the currently playing track (if applicable). """

    state = "stopped"
    """
    The state of the currently playing track. Is one of:
        ["state", "volume", "position", "filename"]

    Note: We track this manually rather that the sounds `get_state` value as
         the returned value does not immediately reflect changes.
    """

    _player = None
    """ Reference to the player instance. """

    _instance = None
    """ Reference to the VLC Instance. """

    @staticmethod
    def _track_finished(*args):
        """ Event fired when the track is finished. """
        logger.info("sound_vlc.py: _track_finished called.")
        Sound.stop(event=True)

    @staticmethod
    def _load_player(filename):
        """ Unload the VLC Media player if it not already unloaded """
        Sound.unload()

        logger.info(f"Sound: Loading player for {filename}")
        if Sound._instance is None:
            Sound._instance = Instance()

        Sound._player = player = Sound._instance.media_player_new()
        media = player.set_mrl(filename)
        player.event_manager().event_attach(
            EventType.MediaPlayerEndReached, Sound._track_finished)
        media.parse()  # Determine duration
        Sound._length = media.get_duration() / 1000.0
        media.release()
        Sound.filename = filename

    @staticmethod
    def unload():
        """ Unload the VLC Media _player if is not already unloaded """
        if Sound._player is not None:
            logger.info("Sound: Unloading player")
            player = Sound._player
            player.event_manager().event_detach(
                EventType.MediaPlayerEndReached)
            if player.is_playing():
                player.stop()
            player.release()
            Sound._player = None
            Sound.filename, Sound.state = "", "stopped"

    @staticmethod
    def play(filename=None):
        """ Play the audio file """
        if filename is None:
            if Sound._player:
                Sound._player.play()
            else:
                return
        else:
            Sound._load_player(filename)
            Sound.set_volume(Sound.volume)
            Sound._player.play()
        Sound.state = "playing"

    @staticmethod
    def stop(event=False):
        """ Stop any currently playing audio file """
        if not event and Sound._player:
            Sound._player.stop()
        Sound.state = "stopped"

    @staticmethod
    def pause():
        """ Play or pause the playing audio file """
        if Sound._player:
            if Sound.state == "playing":
                Sound._player.pause()
                Sound.state = "paused"
            else:
                Sound._player.play()
                Sound.state = "playing"

    @staticmethod
    def set_position(value):
        """ Set the player to the given position between 0 and 1. """
        if Sound._player:
            # value = position / Sound.length
            value = min(1.0, value) if value > 0 else 0
            Sound._player.set_position(value)

    @staticmethod
    def get_state():
        """
        Return the state a dict with the following keys:
        * state, volume, position, filename
        """
        # state = Sound._player.get_state()).split(".")[1]
        # State can be one of:
        #     'NothingSpecial', 'Opening', 'Buffering', 'Playing', 'Paused',
        #     'Stopped', 'Ended', 'Error'
        if Sound._player:
            position = max(Sound._player.get_position(), 0)
        else:
            position = 0.0
        return {"state": Sound.state,
                "volume": Sound.volume,
                "position": position,
                "filename": Sound.filename}

    @staticmethod
    def set_volume(value):
        """
        The volume of the currently playing sound, where the value is between
        0 and 1.
        """
        value = min(1.0, value) if value > 0 else 0
        Sound.volume = value
        if Sound._player:
            Sound._player.audio_set_volume(int(value * 100.0))


# if __name__ == "__main__":
    # from time import sleep

    # file = "/home/fruitbat/Music/Avenged Sevenfold/Hail To The King/"\
    #     "01 - Shepherd Of Fire.mp3"
    # Sound.play(file)
    # Sound.set_volume(0.5)
    # Sound.set_position(0.2)
    # for i in range(12):
    #     print(f"State={Sound.get_state()}")
    #     sleep(1)
    #     if i % 3:
    #         Sound.pause()
    #     elif i == 9:
    #         Sound.stop()
