"""
This module houses a VLC audio component that supports the Kivy `Sound`
interface.
"""
from vlc import EventType, Instance, MediaPlayer
from logging import getLogger


logger = getLogger(__name__)


class Sound():
    '''

    '''
    _player = None
    _instance = None

    # State variables
    volume = 1
    """ Volume  between 0 and 1.0 """
    length = 0
    """ Length of the track in seconds """
    position = 0

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
        Sound.length = media.get_duration() / 1000.0
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
                Sound._player.pause()
            else:
                pass
        else:
            Sound._load_player(filename)
            Sound._player.play()

    @staticmethod
    def stop(event=False):
        """ Stop any currently playing audio file """
        if Sound._player and Sound._player.is_playing():
            Sound._player.pause()

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

    # def get_pos(self):
    #     """ Return the position in seconds the currently playing track """
    #     if self._player is not None and self.state == "play":
    #         return self._player.get_position() * self._length
    #     return 0

    @staticmethod
    def set_volume(value):
        """
        The volume of the currently playing sound, where the value is between
        0 and 1.
        """
        if Sound._player:
            value = min(1.0, value) if value > 0 else 0
            Sound._player.audio_set_volume(int(value * 100.0))
            Sound.volume = value

    # def _get_length(self):
    #     """ Getter method to fetch the track length """
    #     return self._length


if __name__ == "__main__":
    from time import sleep

    file = "/home/fruitbat/Music/Various/Music With Attitude/04 - " \
           "dEUS - Everybody's Weird.mp3"
    # Use the `KIVY_AUDIO=vlcplayer` setting in environment variables to use
    # our provider
    Sound.play(file)
    Sound.set_volume(0.5)
    Sound.set_position(0.2)

    sleep(5)
    Sound.stop()
    sleep(5)
