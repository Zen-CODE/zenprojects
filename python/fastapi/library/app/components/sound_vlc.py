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
    instance = None

    volume = 100
    length = 0

    @staticmethod
    def _track_finished(*args):
        """ Event fired when the track is finished. """
        Sound.stop(event=True)

    @staticmethod
    def _load_player(filename):
        """ Unload the VLC Media player if it not already unloaded """
        Sound.unload()

        logger.info(f"Sound: Loading player for {filename}")
        if Sound.instance is None:
            Sound.instance = Instance()

        Sound._player = player = Sound.instance.media_player_new()
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

    # def seek(self, position):
    #     """ Set the player to the given position in seconds """
    #     if self._player:
    #         value = position / self._length
    #         self._player.set_position(value)

    # def get_pos(self):
    #     """ Return the position in seconds the currently playing track """
    #     if self._player is not None and self.state == "play":
    #         return self._player.get_position() * self._length
    #     return 0

    # def on_volume(self, instance, volume):
    #     """
    #     Respond to the setting of the volume. This value is fraction between
    #     0 and 1.
    #      """
    #     self._set_volume(volume)

    # def _set_volume(self, value):
    #     """
    #     The volume of the currently playing sound, where the value is between
    #     0 and 1.
    #     """
    #     if self._player:
    #         vol = 100 if abs(value) >= 1.0 else 100 * abs(value)
    #         self._player.audio_set_volume(int(vol))

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
    sleep(5)
    Sound.stop()
    sleep(5)
