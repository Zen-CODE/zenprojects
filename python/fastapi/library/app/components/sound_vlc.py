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

    _player = None
    """ Reference to the player instance. """

    _instance = None
    """ Reference to the VLC Instance. """

    @staticmethod
    def _track_finished(*args):
        """ Event fired when the track is finished. """
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

    @staticmethod
    def play(filename=None):
        """ Play the audio file """
        if filename is None:
            if Sound._player:
                Sound._player.play()
            else:
                return False
        else:
            Sound._load_player(filename)
            Sound.set_volume(Sound.volume)
            Sound._player.play()

    @staticmethod
    def stop(event=False):
        """ Stop any currently playing audio file """
        if not event:
            if Sound._player and Sound._player.is_playing():
                Sound._player.stop()

    @staticmethod
    def pause():
        """ Play or pause the playing audio file """
        if Sound._player:
            Sound._player.pause()

    @staticmethod
    def set_position(value):
        """ Set the player to the given position as a value between 0 and 1. """
        if Sound._player:
            # value = position / Sound.length
            value = min(1.0, value) if value > 0 else 0
            Sound._player.set_position(value)

    @staticmethod
    def get_state():
        """
        Return the state a dict with "state", "volume" and "position" keys.
        State can be one of:
            'NothingSpecial', 'Opening', 'Buffering', 'Playing', 'Paused',
            'Stopped', 'Ended', 'Error'
        """
        if Sound._player:
            player = Sound._player
            state = str(Sound._player.get_state()).split(".")[1]
            position = player.get_position()
        else:
            state, position = "Stopped", 0.0
        return {"state": state,
                "volume": Sound.volume,
                "position": position}

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


if __name__ == "__main__":
    from time import sleep

    file = "/home/fruitbat/Music/Avenged Sevenfold/Hail To The King/"\
        "01 - Shepherd Of Fire.mp3"
    Sound.play(file)
    # Sound.set_volume(0.5)
    Sound.set_position(0.2)
    # for i in range(12):
    #     print(f"State={Sound.get_state()}")
    #     sleep(1)
    #     if i % 3:
    #         Sound.pause()
    #     elif i == 9:
    #         Sound.stop()
