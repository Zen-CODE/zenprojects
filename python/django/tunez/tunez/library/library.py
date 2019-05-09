from os import listdir
from os.path import join, isdir, basename, exists
from random import sample
from glob import glob


class MusicLib(object):
    """
    Class for fetching information about our music library, as an experiment
    in jupyter
    """

    def __init__(self, path):
        self.path = path

    def get_artists(self):
        """ Return a list of artists. """
        return [name for name in listdir(self.path) if
                isdir(join(self.path, name))]

    def get_random_artists(self, number):
        """ Return a random list of *number* artists. """
        artists = self.get_artists()
        return sample(artists, number)

    def get_random_albums(self, artist, number):
        """ Return a random list of *number* albums by *artist*. """
        albums = self.get_albums(artist)
        if albums:
            return sample(albums, number)
        else:
            raise (Exception("No albums found for {0}".format(artist)))

    def get_albums(self, artist):
        """ Return a list of albums for the *artist*. """
        path = join(self.path, artist)
        if exists(path):
            return [name for name in listdir(path) if isdir(join(path, name))]
        else:
            return []

    def get_cover(self, artist, album):
        """
        Return the album cover for the specified album or null string
        if it does not exist.
        """
        path = join(self.path, artist, album)
        pattern = "cover.*"
        matches = glob(join(path, pattern))
        return matches[0] if matches else ""

    def get_album_path(self, artist, album):
        """ Return the full path to the specified album. """
        return join(self.path, artist, album)

    @staticmethod
    def _get_any_matches(path, *exts):
        """ Return the first valid files matching the extentions
        in the path specified."""
        for ext in exts:
            matches = glob(join(path, ext))
            if matches:
                return matches
        return None

    def get_tracks(self, artist, album):
        """
        Return a list of the album tracks
        """

        def get_name(fname):
            """"Return the nice, cleaned name of the track"""
            return basename(fname)  # [:-4]

        path = join(self.path, artist, album)
        matches = self._get_any_matches(
            path, "*.mp3", "*.ogg", "*.m4a", "*.wma")
        if matches:
            return sorted([get_name(f) for f in matches])
        else:
            return []

